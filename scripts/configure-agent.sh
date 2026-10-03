#!/usr/bin/env bash
set -euo pipefail
set +x

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
# shellcheck source=scripts/_env.sh
source "${SCRIPT_DIR}/_env.sh"

CONFIG_DIR="${REPO_ROOT}/sre-config"
CONFIG_FILE="${CONFIG_DIR}/agent-config.json"
WORK_DIR="${REPO_ROOT}/.sre-agent-work"
mkdir -p "${WORK_DIR}"
trap 'rm -rf "${WORK_DIR}"' EXIT

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || { echo "ERROR: missing required command '$1'." >&2; exit 1; }
}

render_file() {
  sed \
    -e "s|\${GITHUB_REPO}|${GITHUB_REPOSITORY:-the connected repository}|g" \
    -e "s|\${RG}|${RG}|g" \
    -e "s|\${ENV_NAME}|${ENV_NAME}|g" \
    "$1"
}

json_body_ok() {
  local file first
  file="$1"
  first="$(tr -d '\r\n\t ' < "${file}" | cut -c1)"
  [[ "${first}" == "{" || "${first}" == "[" ]]
}

api_call() {
  local method path body_file out_file status url
  method="$1"
  path="$2"
  body_file="${3:-}"
  out_file="${4:-${WORK_DIR}/response.json}"
  url="${AGENT_ENDPOINT}${path}"
  if [[ -n "${body_file}" ]]; then
    status="$(curl -sS -o "${out_file}" -w '%{http_code}' -X "${method}" "${url}" -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" --data-binary "@${body_file}" || echo '000')"
  else
    status="$(curl -sS -o "${out_file}" -w '%{http_code}' -X "${method}" "${url}" -H "Authorization: Bearer ${TOKEN}" || echo '000')"
  fi
  case "${status}" in
    200|201|202|204)
      if [[ "${status}" != "204" ]] && ! json_body_ok "${out_file}"; then
        echo "WARNING: ${method} ${path} returned HTTP ${status} but not JSON; check for an invalid API route." >&2
        head -c 200 "${out_file}" >&2 || true
        echo >&2
        return 2
      fi
      return 0
      ;;
    *)
      echo "WARNING: ${method} ${path} returned HTTP ${status}." >&2
      head -c 400 "${out_file}" >&2 || true
      echo >&2
      return 1
      ;;
  esac
}

resolve_endpoint_and_token() {
  local deadline
  deadline=$((SECONDS + 600))
  while (( SECONDS < deadline )); do
    AGENT_ENDPOINT="$(get_agent_endpoint)"
    if [[ -n "${AGENT_ENDPOINT}" && "${AGENT_ENDPOINT}" != "null" ]]; then
      TOKEN="$(az account get-access-token --resource 'https://azuresre.dev' --query accessToken --output tsv 2>/dev/null || true)"
      if [[ -n "${TOKEN}" ]]; then
        if api_call GET "/api/v2/agent/tools" "" "${WORK_DIR}/tools-probe.json"; then
          return 0
        fi
      fi
    fi
    echo "  Agent endpoint or data-plane RBAC not ready yet; retrying..."
    sleep 15
  done
  return 1
}

frontmatter_value() {
  local key file
  key="$1"
  file="$2"
  sed -n "s/^${key}: //p" "${file}" | head -n 1
}

connect_code_access() {
  if [[ -z "${GITHUB_REPOSITORY:-}" || -z "${SRE_AGENT_GITHUB_PAT:-}" ]]; then
    echo "  Skipping Code Access and GitHub connector: GITHUB_REPOSITORY and SRE_AGENT_GITHUB_PAT are required."
    return 0
  fi

  local repo_name branch body_file connector_body
  repo_name="${GITHUB_REPOSITORY##*/}"
  branch="${GITHUB_BRANCH:-main}"
  body_file="${WORK_DIR}/code-access.json"
  jq -n \
    --arg name "${repo_name}" \
    --arg url "https://github.com/${GITHUB_REPOSITORY}" \
    --arg pat "${SRE_AGENT_GITHUB_PAT}" \
    --arg branch "${branch}" \
    '{name: $name, type: "CodeRepo", properties: {url: $url, type: "GitHub", pat: $pat, branch: $branch}}' > "${body_file}"

  echo "==> Connecting Code Access for ${GITHUB_REPOSITORY} (${branch})"
  api_call PUT "/api/v2/repos/${repo_name}" "${body_file}" "${WORK_DIR}/code-access-response.json" || echo "  WARNING: Code Access failed; configure it in Builder > Code Access."

  # GitHub issue/PR operations come from the GitHub MCP server exposed as an agent connector.
  # Tools surface as "github_<tool>"; only the read + issue tools below are visible to the agent.
  connector_body="${WORK_DIR}/github-connector.json"
  jq -n \
    --arg repo "${GITHUB_REPOSITORY}" \
    --arg auth "Bearer ${SRE_AGENT_GITHUB_PAT}" \
    --argjson tools "$(jq -c '.githubMcpTools // [] | map("github_" + .)' "${CONFIG_FILE}")" \
    '{name: "github", type: "AgentConnector", properties: {dataConnectorType: "Mcp", dataSource: $repo,
      extendedProperties: {type: "http", endpoint: "https://api.githubcopilot.com/mcp/", authType: "CustomHeaders",
        Authorization: $auth, toolsVisibleToMetaAgent: $tools, selectedTools: $tools},
      identity: "", keyVaultUri: null, endpoint: null, source: "Agent"}}' > "${connector_body}"
  echo "==> Connecting GitHub MCP connector (issues, code search)"
  api_call PUT "/api/v2/extendedAgent/connectors/github" "${connector_body}" "${WORK_DIR}/github-connector-response.json" || echo "  WARNING: GitHub MCP connector failed; add it in Builder > Connectors."
  rm -f "${connector_body}" "${WORK_DIR}/github-connector-response.json"
}

apply_custom_instructions() {
  local rel src body
  rel="$(jq -r '.customInstructions' "${CONFIG_FILE}")"
  src="${CONFIG_DIR}/${rel}"
  body="${WORK_DIR}/custom-instructions.json"
  render_file "${src}" | jq -Rs '{instructions: .}' > "${body}"
  echo "==> Applying custom instructions"
  api_call PUT "/api/v2/agent/customInstructions" "${body}" "${WORK_DIR}/custom-instructions-response.json" || true
}

upload_knowledge() {
  local args rel staged status out_file
  echo "==> Uploading knowledge base"
  args=()
  while IFS= read -r rel; do
    staged="${WORK_DIR}/$(basename "${rel}")"
    render_file "${CONFIG_DIR}/${rel}" > "${staged}"
    args+=( -F "files=@$(basename "${rel}");type=text/plain" )
    echo "  ${rel}"
  done < <(jq -r '.knowledgeBase[]' "${CONFIG_FILE}")

  if (( ${#args[@]} == 0 )); then
    return 0
  fi
  out_file="${WORK_DIR}/knowledge-upload-response.json"
  # Upload from inside WORK_DIR: relative paths keep curl portable across Git Bash and Linux.
  status="$(cd "${WORK_DIR}" || exit 1; curl -sS -o "$(basename "${out_file}")" -w '%{http_code}' -X POST "${AGENT_ENDPOINT}/api/v1/AgentMemory/upload" -H "Authorization: Bearer ${TOKEN}" -F "triggerIndexing=true" "${args[@]}" || true)"
  status="${status:-000}"
  case "${status}" in
    200|201|202)
      if json_body_ok "${out_file}"; then echo "  Knowledge uploaded."; else echo "  WARNING: knowledge upload did not return JSON."; fi
      ;;
    *)
      echo "  WARNING: knowledge upload returned HTTP ${status}."
      head -c 400 "${out_file}" || true
      echo
      ;;
  esac
}

apply_skills() {
  local rel path skill_id desc content body
  echo "==> Applying skills"
  while IFS= read -r rel; do
    path="${CONFIG_DIR}/${rel}"
    skill_id="$(frontmatter_value name "${path}")"
    desc="$(frontmatter_value description "${path}")"
    content="$(render_file "${path}" | awk 'BEGIN { d = 0 } /^---$/ { d++; next } d >= 2 { print }')"
    body="${WORK_DIR}/skill-${skill_id}.json"
    jq -n --arg id "${skill_id}" --arg desc "${desc}" --arg content "${content}" \
      '{name: $id, type: "Skill", tags: [], properties: {name: $id, description: $desc, tools: [], skillContent: $content, additionalFiles: [], sourcePluginInstallation: null}}' > "${body}"
    api_call PUT "/api/v2/extendedAgent/skills/${skill_id}" "${body}" "${WORK_DIR}/skill-${skill_id}-response.json" \
      && echo "  ${skill_id}: applied" || echo "  WARNING: ${skill_id}: apply failed"
  done < <(jq -r '.skills[]' "${CONFIG_FILE}")
}

apply_subagents() {
  local sub name handoff tools instructions body
  echo "==> Applying subagents"
  while IFS= read -r sub; do
    name="$(jq -r '.name' <<<"${sub}")"
    handoff="$(jq -r '.handoffDescription' <<<"${sub}")"
    tools="$(jq -c '.tools' <<<"${sub}")"
    instructions="$(render_file "${CONFIG_DIR}/$(jq -r '.instructions' <<<"${sub}")")"
    body="${WORK_DIR}/agent-${name}.json"
    jq -n --arg name "${name}" --arg handoff "${handoff}" --arg instructions "${instructions}" --argjson tools "${tools}" \
      '{name: $name, type: "ExtendedAgent", tags: [], owner: "", properties: {instructions: $instructions, handoffDescription: $handoff, handoffs: [], tools: $tools, mcpTools: [], allowParallelToolCalls: true, enableSkills: true}}' > "${body}"
    api_call PUT "/api/v2/extendedAgent/agents/${name}" "${body}" "${WORK_DIR}/agent-${name}-response.json" \
      && echo "  ${name}: configured" || echo "  WARNING: ${name}: configure failed"
  done < <(jq -c '.subagents[]' "${CONFIG_FILE}")
}

apply_response_plans() {
  local plan id name title agent body
  echo "==> Applying response plans"
  curl -sS -o /dev/null -X DELETE "${AGENT_ENDPOINT}/api/v1/incidentPlayground/filters/quickstart_response_plan" -H "Authorization: Bearer ${TOKEN}" || true
  while IFS= read -r plan; do
    id="$(jq -r '.id' <<<"${plan}")"
    name="$(jq -r '.name' <<<"${plan}")"
    title="$(jq -r '.titleContains' <<<"${plan}")"
    agent="$(jq -r '.handlingAgent' <<<"${plan}")"
    body="${WORK_DIR}/plan-${id}.json"
    jq -n --arg id "${id}" --arg name "${name}" --arg titleContains "${title}" --arg agent "${agent}" \
      '{name: $id, type: "IncidentFilter", tags: [], properties: {name: $name, incidentPlatform: "AzMonitor", priorities: ["Sev0", "Sev1", "Sev2", "Sev3", "Sev4"], titleContains: $titleContains, titleContainsAll: [], titleContainsAny: [], titleNotContains: [], handlingAgent: $agent, agentMode: "autonomous", maxAutomatedInvestigationAttempts: 3, mergeEnabled: false, mergeWindowHours: 3, isEnabled: true}}' > "${body}"
    api_call PUT "/api/v2/extendedAgent/incidentFilters/${id}" "${body}" "${WORK_DIR}/plan-${id}-response.json" \
      && echo "  ${id} -> ${agent}" || echo "  WARNING: ${id}: configure failed"
  done < <(jq -c '.responsePlans[]' "${CONFIG_FILE}")
}

verify_configuration() {
  local kb_json roster agents filters skills
  echo "==> Verification summary"

  kb_json="${WORK_DIR}/kb-files.json"
  for _ in 1 2 3 4 5 6; do
    api_call GET "/api/v1/AgentMemory/files" "" "${kb_json}" || true
    if jq -e '[.files[]? | select((.isIndexed // false) == false)] | length == 0' "${kb_json}" >/dev/null 2>&1; then
      break
    fi
    sleep 5
  done
  echo "  Knowledge:"
  jq -r '.files[]? | "    \(.name) indexed=\(.isIndexed)"' "${kb_json}" 2>/dev/null || echo "    unavailable"

  skills="${WORK_DIR}/skills-readback.json"
  api_call GET "/api/v2/extendedAgent/skills" "" "${skills}" || true
  echo "  Skills:"
  while IFS= read -r rel; do
    local skill_id remote_chars
    skill_id="$(frontmatter_value name "${CONFIG_DIR}/${rel}")"
    remote_chars="$(jq -r --arg n "${skill_id}" '.value[]? | select(.name == $n) | (.properties.skillContent // "") | length' "${skills}" 2>/dev/null || true)"
    echo "    ${skill_id} chars=${remote_chars:-missing}"
  done < <(jq -r '.skills[]' "${CONFIG_FILE}")

  roster="${WORK_DIR}/tools.json"
  agents="${WORK_DIR}/agents-readback.json"
  api_call GET "/api/v2/agent/tools" "" "${roster}" || true
  api_call GET "/api/v2/extendedAgent/agents" "" "${agents}" || true
  echo "  Subagents:"
  jq -r --slurpfile roster "${roster}" '
    (($roster[0].data // $roster[0].value // []) | map(.name)) as $known
    | .value[]?
    | .properties.tools as $t
    | ($t - $known) as $phantom
    | "    \(.name) tools=\($t | length) phantom=\(if ($phantom | length) == 0 then "none" else ($phantom | join(",")) end) azureWrite=\($t | index("RunAzCliWriteCommands") != null) terminal=\($t | index("RunInTerminal") != null)"' "${agents}" 2>/dev/null || echo "    unavailable"

  filters="${WORK_DIR}/filters-readback.json"
  api_call GET "/api/v2/extendedAgent/incidentFilters" "" "${filters}" || true
  echo "  Response plans:"
  jq -r '.value[]? | select(.properties.isEnabled) | "    \(.name) titleContains=\(.properties.titleContains) -> \(.properties.handlingAgent)"' "${filters}" 2>/dev/null || echo "    unavailable"
}

require_cmd az
require_cmd curl
require_cmd jq
[[ -f "${CONFIG_FILE}" ]] || { echo "ERROR: ${CONFIG_FILE} not found." >&2; exit 1; }

echo "==> Resolving SRE Agent endpoint for ${AGENT_NAME}"
if ! resolve_endpoint_and_token; then
  echo "ERROR: SRE Agent endpoint or data-plane RBAC was not ready after waiting. Re-run scripts/configure-agent.sh in a few minutes." >&2
  exit 1
fi
printf '  Endpoint: %s\n' "${AGENT_ENDPOINT}"

connect_code_access
apply_custom_instructions
upload_knowledge
apply_skills
apply_subagents
apply_response_plans
verify_configuration

echo "==> SRE Agent configuration complete."
