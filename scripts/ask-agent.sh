#!/usr/bin/env bash
set -euo pipefail
set +x

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/_env.sh
source "${SCRIPT_DIR}/_env.sh"

PROMPT="${1:-}"
OUTPUT_PATH="${2:-}"
if [[ -z "${PROMPT}" ]]; then
  echo "Usage: $0 \"<prompt>\" [output-json-path]" >&2
  exit 2
fi

AGENT_ENDPOINT="${SRE_AGENT_ENDPOINT:-$(get_agent_endpoint)}"
if [[ -z "${AGENT_ENDPOINT}" || "${AGENT_ENDPOINT}" == "null" ]]; then
  echo "ERROR: could not resolve SRE Agent endpoint." >&2
  exit 1
fi
TOKEN="$(az account get-access-token --resource 'https://azuresre.dev' --query accessToken --output tsv)"
WORK_DIR="${PWD}/.sre-agent-work"
mkdir -p "${WORK_DIR}"
CREATE_BODY="${WORK_DIR}/thread-create.json"
CREATE_RESPONSE="${WORK_DIR}/thread-create-response.json"
MESSAGES_RESPONSE="${WORK_DIR}/thread-messages-response.json"

jq -n --arg title "Contoso Trek demo chat" --arg text "${PROMPT}" '{title: $title, startMessage: {text: $text}}' > "${CREATE_BODY}"
status="$(curl -sS -o "${CREATE_RESPONSE}" -w '%{http_code}' -X POST "${AGENT_ENDPOINT}/api/v1/threads" -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" --data-binary "@${CREATE_BODY}" || echo '000')"
if [[ ! "${status}" =~ ^20 ]]; then
  echo "ERROR: thread create returned HTTP ${status}." >&2
  head -c 400 "${CREATE_RESPONSE}" >&2 || true
  echo >&2
  exit 1
fi
THREAD_ID="$(jq -r '.id // .threadId // .name // empty' "${CREATE_RESPONSE}")"
if [[ -z "${THREAD_ID}" ]]; then
  echo "ERROR: could not determine thread id from response." >&2
  cat "${CREATE_RESPONSE}" >&2
  exit 1
fi

echo "==> Thread ${THREAD_ID}"
last_count=0
stable=0
for _ in $(seq 1 90); do
  curl -sS -o "${MESSAGES_RESPONSE}" "${AGENT_ENDPOINT}/api/v1/threads/${THREAD_ID}/messages" -H "Authorization: Bearer ${TOKEN}"
  count="$(jq '[.messages[]?, .value[]?, .data[]?] | length' "${MESSAGES_RESPONSE}" 2>/dev/null || echo 0)"
  busy="$(jq -r '.status // .state // empty' "${MESSAGES_RESPONSE}" 2>/dev/null || true)"
  if [[ "${count}" == "${last_count}" && "${count}" != "0" ]]; then
    stable=$((stable + 1))
  else
    stable=0
  fi
  last_count="${count}"
  if (( stable >= 3 )) && [[ ! "${busy}" =~ [Rr]unning|[Ii]n[Pp]rogress|[Qq]ueued ]]; then
    break
  fi
  sleep 5
done

if [[ -n "${OUTPUT_PATH}" ]]; then
  mkdir -p "$(dirname "${OUTPUT_PATH}")"
  cp "${MESSAGES_RESPONSE}" "${OUTPUT_PATH}"
fi

jq -r 'def items: (.messages // .value // .data // []); items[]? | "--- \(.role // .author // .sender // "message") ---\n\(.content // .text // .message // (. | tostring))\n"' "${MESSAGES_RESPONSE}" 2>/dev/null || cat "${MESSAGES_RESPONSE}"
