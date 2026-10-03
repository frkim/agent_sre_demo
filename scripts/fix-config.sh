#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/_env.sh
source "${SCRIPT_DIR}/_env.sh"

echo "==> Restoring INVENTORY_BACKEND=builtin on ${API_APP}"
az containerapp update \
  --resource-group "${RG}" \
  --name "${API_APP}" \
  --set-env-vars "INVENTORY_BACKEND=builtin" \
  --output none

WEB_URL="$(get_web_url)"
echo "  Storefront: ${WEB_URL}"
echo "  The banner returns to green once the new revision takes traffic."
