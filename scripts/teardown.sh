#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/_env.sh
source "${SCRIPT_DIR}/_env.sh"

if [[ "${CONFIRM_TEARDOWN:-}" != "${ENV_NAME}" ]]; then
  echo "ERROR: set CONFIRM_TEARDOWN=${ENV_NAME} to delete ${RG}." >&2
  exit 2
fi

echo "==> Deleting resource group ${RG}"
az group delete --name "${RG}" --yes --no-wait
echo "Deletion started."
