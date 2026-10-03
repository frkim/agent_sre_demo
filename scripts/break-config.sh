#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/_env.sh
source "${SCRIPT_DIR}/_env.sh"

BAD_INVENTORY_BACKEND="${BAD_INVENTORY_BACKEND:-cosmosdb-prod}"

echo "==> Breaking Contoso Trek: setting INVENTORY_BACKEND=${BAD_INVENTORY_BACKEND} on ${API_APP}"
az containerapp update \
  --resource-group "${RG}" \
  --name "${API_APP}" \
  --set-env-vars "INVENTORY_BACKEND=${BAD_INVENTORY_BACKEND}" \
  --output none

REVISION="$(az containerapp show --resource-group "${RG}" --name "${API_APP}" --query "properties.latestRevisionName" --output tsv)"
WEB_URL="$(get_web_url)"

echo
echo "  Broken at:    $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
echo "  New revision: ${REVISION}"
echo "  Storefront:   ${WEB_URL}"
echo
echo "The storefront banner turns red once the new revision takes traffic."
echo "The '${AVAILABILITY_ALERT}' alert fires within about 5-10 minutes and platform-operator restores INVENTORY_BACKEND=builtin."
