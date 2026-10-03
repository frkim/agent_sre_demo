#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/_env.sh
source "${SCRIPT_DIR}/_env.sh"

REQUESTS="${REQUESTS:-20}"
WEB_URL="${WEB_URL:-$(get_web_url)}"
if [[ -z "${WEB_URL}" ]]; then
  echo "ERROR: could not resolve web URL. Set WEB_URL or deploy the app first." >&2
  exit 1
fi

PRODUCTS_JSON="$(curl -fsS "${WEB_URL}/api/v1/products?category=Climbing&pageSize=50" || true)"
mapfile -t PRODUCT_IDS < <(jq -r '.items[]?.id // empty' <<<"${PRODUCTS_JSON}" 2>/dev/null || true)

if (( ${#PRODUCT_IDS[@]} == 0 )); then
  echo "WARNING: could not discover Climbing products; falling back to product IDs 1..20."
  PRODUCT_IDS=(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20)
fi

echo "==> Triggering climbing product detail failures through ${WEB_URL} (${REQUESTS} requests)"
for i in $(seq 1 "${REQUESTS}"); do
  id="${PRODUCT_IDS[$(( (i - 1) % ${#PRODUCT_IDS[@]} ))]}"
  code="$(curl -sS -o /dev/null -w '%{http_code}' "${WEB_URL}/api/v1/products/${id}" || true)"
  printf '  request %02d product=%s HTTP %s\n' "${i}" "${id}" "${code}"
done

echo
echo "The '${APP_EXCEPTION_ALERT}' alert fires within about 5-10 minutes, or use scripts/ask-agent.sh to skip alert latency."
