# AGENTS.md

## Project overview

Contoso Trek is an Azure SRE Agent demo for an outdoor-gear storefront. The application runs as two Azure Container Apps: a Python FastAPI API and a Vue 3/Vuetify web frontend. The infrastructure provisions Azure Container Apps, ACR, Application Insights, Log Analytics, Azure Monitor alerts, and a Microsoft.App SRE Agent.

- **Frontend**: Vue 3 + Vuetify, nginx-unprivileged on port 8080
- **Backend**: Python 3.12 FastAPI on port 8080
- **Hosting**: Azure Container Apps consumption
- **Operations**: Azure SRE Agent with data-plane config from `sre-config/`

## Commands

| Task | Command |
| --- | --- |
| Validate Bicep | `az bicep build --file infra/main.bicep && az bicep lint --file infra/main.bicep` |
| Deploy demo | `bash scripts/deploy.sh` |
| Configure SRE Agent | `bash scripts/configure-agent.sh` |
| Smoke test | `bash scripts/smoke-test.sh` |
| Scenario 1 errors | `bash scripts/trigger-errors.sh` |
| Scenario 2 break/fix | `bash scripts/break-config.sh` / `bash scripts/fix-config.sh` |

Use the protected feeds for package restores:

- PyPI: `https://packagefeedproxy.microsoft.io/pypi/simple`
- npm: `https://packagefeedproxy.microsoft.io/npm/`
- NuGet: `https://packagefeedproxy.microsoft.io/nuget/v3/index.json`

## Ownership boundaries

- Infrastructure/automation owners may edit `infra/**`, `scripts/**`, `sre-config/**`, `.github/**`, and repository hygiene files.
- Do not touch `src/api` or `src/web` unless explicitly assigned application work.
- Do not create, modify, or delete Azure resources from agent sessions unless the user asks to deploy or run a scenario script.

## SRE Agent data-plane gotchas

- Unknown data-plane paths return HTTP 200 with HTML. Always assert JSON bodies and read back configuration.
- Use `/api/v2/extendedAgent/*` PUT routes for skills, subagents, and response plans.
- Upload knowledge through `POST /api/v1/AgentMemory/upload` multipart; connector uploads can fail indexing.
- Cross-check subagent tool grants against `GET /api/v2/agent/tools`; unknown tool names are accepted silently.
- Code Access uses `PUT /api/v2/repos/{repoName}` and the top-level `name` must equal the `{repoName}` path segment.
- Delete `quickstart_response_plan` so it does not swallow demo incidents.
- The deployer needs the built-in **SRE Agent Administrator** role on the agent resource for configuration.

## Standards

- Managed identities for Azure access; no secrets in code or logs.
- Tags on every Azure resource: `env`, `workload`, `owner`, `costCenter`, `dataClassification`.
- Smallest SKU that satisfies the demo; scale up only with evidence.
- Pin GitHub Actions to full commit SHAs and keep workflow permissions minimal.
- Run the smallest validation that covers your change and report results.
