#!/usr/bin/env bash
# Shared environment resolution for Contoso Trek demo scripts. Source this file.

# shellcheck disable=SC2034
if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  echo "Source this file from another script: source scripts/_env.sh" >&2
  exit 1
fi

ENV_NAME="${ENV_NAME:-${AZURE_ENV_NAME:-demo}}"
LOCATION="${LOCATION:-${AZURE_LOCATION:-francecentral}}"
RG="${RG:-${AZURE_RESOURCE_GROUP:-rg-sre-agent-demo-${ENV_NAME}}}"
OWNER="${OWNER:-${AZURE_TAG_OWNER:-frkim}}"
COST_CENTER="${COST_CENTER:-${AZURE_TAG_COST_CENTER:-demo}}"

API_APP="ca-trek-api-${ENV_NAME}"
WEB_APP="ca-trek-web-${ENV_NAME}"
CONTAINER_ENV="cae-trek-${ENV_NAME}"
APPI_NAME="appi-trek-${ENV_NAME}"
LAW_NAME="log-trek-${ENV_NAME}"
AGENT_NAME="sre-trek-${ENV_NAME}"
ACTION_GROUP="ag-sre-trek-${ENV_NAME}"
APP_EXCEPTION_ALERT="alert-trek-app-exception-${ENV_NAME}"
AVAILABILITY_ALERT="alert-trek-availability-${ENV_NAME}"
PLACEHOLDER_IMAGE="mcr.microsoft.com/k8se/quickstart:latest"

get_web_fqdn() {
  az containerapp show --resource-group "${RG}" --name "${WEB_APP}" --query "properties.configuration.ingress.fqdn" --output tsv 2>/dev/null || true
}

get_web_url() {
  local fqdn
  fqdn="$(get_web_fqdn)"
  if [[ -n "${fqdn}" ]]; then
    printf 'https://%s\n' "${fqdn}"
  fi
}

get_api_fqdn() {
  az containerapp show --resource-group "${RG}" --name "${API_APP}" --query "properties.configuration.ingress.fqdn" --output tsv 2>/dev/null || true
}

get_agent_endpoint() {
  local subscription_id
  subscription_id="$(az account show --query id --output tsv)"
  az rest \
    --method GET \
    --url "https://management.azure.com/subscriptions/${subscription_id}/resourceGroups/${RG}/providers/Microsoft.App/agents/${AGENT_NAME}?api-version=2026-01-01" \
    --query "properties.agentEndpoint" \
    --output tsv 2>/dev/null || true
}
