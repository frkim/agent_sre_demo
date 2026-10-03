#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/_env.sh
source "${SCRIPT_DIR}/_env.sh"

WEB_URL="${WEB_URL:-$(get_web_url)}"
if [[ -z "${WEB_URL}" ]]; then
  echo "ERROR: could not resolve web URL. Set WEB_URL or deploy the app first." >&2
  exit 1
fi

DEADLINE=$((SECONDS + 300))
LAST_STATUS=""

echo "==> Smoke testing ${WEB_URL}"
while (( SECONDS < DEADLINE )); do
  web_code="$(curl -k -sS -o /dev/null -w '%{http_code}' "${WEB_URL}" || true)"
  api_status_json="$(curl -k -fsS "${WEB_URL}/api/v1/status" 2>/dev/null || true)"
  status="$(jq -r '.status // empty' <<<"${api_status_json}" 2>/dev/null || true)"
  products_code="$(curl -k -sS -o /dev/null -w '%{http_code}' "${WEB_URL}/api/v1/products?pageSize=1" || true)"
  LAST_STATUS="web=${web_code} status=${status:-missing} products=${products_code}"
  if [[ "${web_code}" == "200" && "${status}" == "operational" && "${products_code}" == "200" ]]; then
    echo "  OK: ${LAST_STATUS}"
    exit 0
  fi
  echo "  Waiting: ${LAST_STATUS}"
  sleep 10
done

echo "ERROR: smoke test failed after ~5 minutes (${LAST_STATUS})." >&2
exit 1
