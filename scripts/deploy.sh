#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
# shellcheck source=scripts/_env.sh
source "${SCRIPT_DIR}/_env.sh"

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || { echo "ERROR: missing required command '$1'." >&2; exit 1; }
}

jwt_claim() {
  local token payload padded mod
  token="$1"
  payload="${token#*.}"
  payload="${payload%%.*}"
  mod=$(( ${#payload} % 4 ))
  padded="${payload}"
  if [[ ${mod} -eq 2 ]]; then padded="${payload}=="; elif [[ ${mod} -eq 3 ]]; then padded="${payload}="; elif [[ ${mod} -eq 1 ]]; then padded="${payload}==="; fi
  printf '%s' "${padded}" | tr '_-' '/+' | base64 -d 2>/dev/null | jq -r '.oid // empty'
}

resolve_deployer_principal_id() {
  local token oid client_id
  token="$(az account get-access-token --query accessToken --output tsv)"
  oid="$(jwt_claim "${token}" || true)"
  if [[ -n "${oid}" ]]; then
    printf '%s\n' "${oid}"
    return 0
  fi
  client_id="${AZURE_CLIENT_ID:-$(az account show --query user.name --output tsv 2>/dev/null || true)}"
  if [[ -n "${client_id}" ]]; then
    az ad sp show --id "${client_id}" --query id --output tsv 2>/dev/null && return 0
  fi
  az ad signed-in-user show --query id --output tsv
}

resolve_principal_type() {
  local user_type
  user_type="$(az account show --query user.type --output tsv 2>/dev/null || true)"
  if [[ "${user_type}" == "user" ]]; then
    printf 'User\n'
  else
    printf 'ServicePrincipal\n'
  fi
}

current_image_or_placeholder() {
  local app_name image
  app_name="$1"
  image="$(az containerapp show --resource-group "${RG}" --name "${app_name}" --query "properties.template.containers[0].image" --output tsv 2>/dev/null || true)"
  if [[ -z "${image}" || "${image}" == "null" ]]; then
    image="${PLACEHOLDER_IMAGE}"
  fi
  printf '%s\n' "${image}"
}

deploy_bicep() {
  local api_image web_image principal_id principal_type
  api_image="$1"
  web_image="$2"
  principal_id="$3"
  principal_type="$4"
  az deployment group create \
    --resource-group "${RG}" \
    --template-file "${REPO_ROOT}/infra/main.bicep" \
    --parameters \
      environmentName="${ENV_NAME}" \
      location="${LOCATION}" \
      apiImage="${api_image}" \
      webImage="${web_image}" \
      owner="${OWNER}" \
      costCenter="${COST_CENTER}" \
      deployerPrincipalId="${principal_id}" \
      deployerPrincipalType="${principal_type}" \
    --output json
}

wait_containerapp_healthy() {
  local app_name deadline state running
  app_name="$1"
  deadline=$((SECONDS + 600))
  echo "==> Waiting for ${app_name} revision to become healthy..."
  while (( SECONDS < deadline )); do
    state="$(az containerapp revision list --resource-group "${RG}" --name "${app_name}" --query "[?properties.active].[-1].properties.healthState" --output tsv 2>/dev/null || true)"
    running="$(az containerapp revision list --resource-group "${RG}" --name "${app_name}" --query "[?properties.active].[-1].properties.runningState" --output tsv 2>/dev/null || true)"
    if [[ "${state}" == "Healthy" || "${running}" == "Running" ]]; then
      echo "  ${app_name}: ${state:-${running}}"
      return 0
    fi
    sleep 10
  done
  echo "ERROR: ${app_name} did not become healthy before timeout." >&2
  az containerapp revision list --resource-group "${RG}" --name "${app_name}" --output table || true
  return 1
}

require_cmd az
require_cmd docker
require_cmd jq
require_cmd git

cd "${REPO_ROOT}"
GIT_SHA="$(git rev-parse --short=12 HEAD)"
DEPLOYER_PRINCIPAL_ID="${DEPLOYER_PRINCIPAL_ID:-$(resolve_deployer_principal_id)}"
DEPLOYER_PRINCIPAL_TYPE="${DEPLOYER_PRINCIPAL_TYPE:-$(resolve_principal_type)}"

TAGS=("env=${ENV_NAME}" "workload=trek" "owner=${OWNER}" "costCenter=${COST_CENTER}" "dataClassification=demo")

echo "==> Creating or updating resource group ${RG} in ${LOCATION}"
az group create --name "${RG}" --location "${LOCATION}" --tags "${TAGS[@]}" --output none

FIRST_API_IMAGE="${API_IMAGE:-$(current_image_or_placeholder "${API_APP}")}"
FIRST_WEB_IMAGE="${WEB_IMAGE:-$(current_image_or_placeholder "${WEB_APP}")}"

echo "==> First infrastructure pass (preserve existing images or placeholder)"
FIRST_OUTPUT="$(deploy_bicep "${FIRST_API_IMAGE}" "${FIRST_WEB_IMAGE}" "${DEPLOYER_PRINCIPAL_ID}" "${DEPLOYER_PRINCIPAL_TYPE}")"
printf '%s\n' "${FIRST_OUTPUT}" > "${REPO_ROOT}/.sre-deploy-outputs.json"
ACR_NAME="$(jq -r '.properties.outputs.acrName.value' <<<"${FIRST_OUTPUT}")"
ACR_LOGIN_SERVER="$(jq -r '.properties.outputs.acrLoginServer.value' <<<"${FIRST_OUTPUT}")"

if [[ -z "${ACR_NAME}" || "${ACR_NAME}" == "null" ]]; then
  echo "ERROR: deployment did not return an ACR name." >&2
  exit 1
fi

echo "==> Building and pushing images to ${ACR_LOGIN_SERVER}"
az acr login --name "${ACR_NAME}"
API_IMAGE_FINAL="${ACR_LOGIN_SERVER}/trek-api:${GIT_SHA}"
WEB_IMAGE_FINAL="${ACR_LOGIN_SERVER}/trek-web:${GIT_SHA}"
docker build --pull -t "${API_IMAGE_FINAL}" "${REPO_ROOT}/src/api"
docker build --pull -t "${WEB_IMAGE_FINAL}" "${REPO_ROOT}/src/web"
docker push "${API_IMAGE_FINAL}"
docker push "${WEB_IMAGE_FINAL}"

echo "==> Second infrastructure pass (deploy built images)"
FINAL_OUTPUT="$(deploy_bicep "${API_IMAGE_FINAL}" "${WEB_IMAGE_FINAL}" "${DEPLOYER_PRINCIPAL_ID}" "${DEPLOYER_PRINCIPAL_TYPE}")"
printf '%s\n' "${FINAL_OUTPUT}" > "${REPO_ROOT}/.sre-deploy-outputs.json"

wait_containerapp_healthy "${API_APP}"
wait_containerapp_healthy "${WEB_APP}"

WEB_URL="$(jq -r '.properties.outputs.webUrl.value' <<<"${FINAL_OUTPUT}")"
AGENT_ENDPOINT="$(jq -r '.properties.outputs.agentEndpoint.value // empty' <<<"${FINAL_OUTPUT}")"

echo
printf 'Web URL: %s\n' "${WEB_URL}"
printf 'API app: %s\n' "${API_APP}"
printf 'Web app: %s\n' "${WEB_APP}"
printf 'ACR: %s (%s)\n' "${ACR_NAME}" "${ACR_LOGIN_SERVER}"
printf 'SRE Agent: %s\n' "${AGENT_NAME}"
if [[ -n "${AGENT_ENDPOINT}" && "${AGENT_ENDPOINT}" != "null" ]]; then
  printf 'SRE Agent endpoint: %s\n' "${AGENT_ENDPOINT}"
else
  echo 'SRE Agent endpoint: pending (ARM properties.agentEndpoint not populated yet)'
fi
