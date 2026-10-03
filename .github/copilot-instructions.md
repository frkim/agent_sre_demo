# Copilot instructions

Contoso Trek is an Azure SRE Agent demo: FastAPI API + Vue/Vuetify frontend on Azure Container Apps, operated by a Microsoft.App SRE Agent.

## How to work here

- Match existing patterns and keep changes focused.
- Respect ownership: do not edit `src/**` when working on infrastructure/automation.
- Use managed identities and Azure RBAC; never hardcode secrets.
- Use protected package feeds only: `packagefeedproxy.microsoft.io` for PyPI, npm, and NuGet.
- For SRE Agent data-plane calls, assert JSON responses because invalid paths can return HTTP 200 HTML.
- Do not disable alerts, scale apps, or redeploy as a fix for scenario 1 code exceptions.
- Scenario 2 remediation is restoring `INVENTORY_BACKEND=builtin` on `ca-trek-api-<env>`.

## Validation

Run targeted validation before finishing:

```bash
az bicep build --file infra/main.bicep
az bicep lint --file infra/main.bicep
find scripts -name '*.sh' -print0 | xargs -0 -n1 bash -n
```

Also run shellcheck when available.
