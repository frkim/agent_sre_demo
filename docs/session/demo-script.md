# Azure SRE Agent — Contoso Trek live demo script

## Prerequisites

- Bash shell with `az`, `docker`, `jq`, `curl`, and `git`.
- Azure login completed for the target subscription.
- GitHub repository `frkim/agent_sre_demo` with Issues enabled.
- GitHub Actions configured with OIDC repo variables when available, otherwise the `AZURE_CREDENTIALS` secret.
- `SRE_AGENT_GITHUB_PAT` for Code Access and GitHub MCP connector setup.

```bash
export ENV_NAME=demo
export LOCATION=francecentral
```

Live deployment defaults:

- Region: `francecentral`.
- Resource group: `rg-sre-agent-demo-demo`.
- Agent: `sre-trek-demo`.
- Current web URL: `https://ca-trek-web-demo.proudocean-95776aec.francecentral.azurecontainerapps.io`.
- The web URL may change per environment; use the value printed in the GitHub Actions workflow summary or by `scripts/deploy.sh`.
- Portal: <https://sre.azure.com>.

## Demo 1 — Deploy from GitHub Actions and configure the agent

Show `.github/workflows/deploy.yml` stages: **validate → deploy → configure agent → smoke test**.
Azure login uses OIDC when repository variables are set; otherwise it uses the `AZURE_CREDENTIALS` secret.
Show `scripts/deploy.sh`, `infra/`, and `sre-config/agent-config.json`.
Point out that `app-exception` routes to `code-investigator` and `availability` routes to `platform-operator`.

Live commands:

```bash
bash scripts/deploy.sh
bash scripts/configure-agent.sh
bash scripts/smoke-test.sh
```

While waiting, say that `deploy.sh` creates/updates the resource group, performs a first Bicep pass, builds and pushes `trek-api` and `trek-web`, performs a second Bicep pass, and waits for healthy Container App revisions.
Say that `configure-agent.sh` resolves `properties.agentEndpoint`, obtains a token for `https://azuresre.dev`, configures Code Access with a PAT through `PUT /api/v2/repos/{name}`, configures the GitHub MCP connector at `https://api.githubcopilot.com/mcp/`, applies instructions, uploads knowledge, configures skills/subagents/response plans, and reads back configuration.

Least-privilege proof:

- `code-investigator`: no Azure write tools.
- `platform-operator`: Azure CLI write tools but no terminal/GitHub tools.
- Read-back verification reports `phantom=none`, proving configured tool names match the agent's actual tool roster.

Expected outcome: GitHub Actions succeeds; the resource group contains Container Apps, Log Analytics, Application Insights, ACR, action group, alerts, SRE Agent, and identities; storefront banner is green.
Fallback: show the latest successful workflow run and resource group.

## Demo 2 — Code defect: HTTP 500 to GitHub issue to Copilot draft PR

Scenario: Climbing product details throw `ZeroDivisionError` because unit price is calculated from `price / pack_size` and climbing products have `pack_size = 0`.
This is a code defect; no Azure change should be made.

GitHub integration used in this demo:

- Code Access: PAT-backed repository connection through `PUT /api/v2/repos/{name}`.
- GitHub MCP connector: `https://api.githubcopilot.com/mcp/`, agent connector type `Mcp`.
- Selected tools exposed as `github_<tool>`: `issue_write`, `issue_read`, `list_issues`, `search_issues`, `add_issue_comment`, `get_file_contents`, `search_code`, `list_commits`, `get_commit`, and `assign_copilot_to_issue`.

Trigger:

```bash
REQUESTS=20 bash scripts/trigger-errors.sh
```

The alert may take 5–10 minutes.
While waiting, show `sre-config/skills/diagnose-trek-app-exception.md`, KQL for `AppRequests` and `AppExceptions`, and the GitHub MCP selected tools.
At `sre.azure.com`, show the incident thread, evidence, source read, issue search, issue creation, and Copilot assignment.

Direct prompt fallback:

```bash
bash scripts/ask-agent.sh "Investigate recent HTTP 500 errors for Contoso Trek climbing product details. Use telemetry and Code Access, de-duplicate GitHub issues, identify the source file and line, file a GitHub issue if this is a code defect, then assign GitHub Copilot coding agent to draft a PR for human review."
```

Expected outcome:

1. `code-investigator` queries telemetry and reads source via Code Access.
2. It searches existing GitHub issues to avoid duplicates.
3. It opens a GitHub issue titled like `[SRE] HTTP 500 on climbing product details - ZeroDivisionError`, labels it `sre-agent` and `bug`, and includes impact/stack/file:line/suggested fix.
4. It calls `github_assign_copilot_to_issue`.
5. GitHub Copilot coding agent opens a draft PR for human review.
6. The summary states no Azure resource was modified.

## Demo 3 — Config fault: HTTP 503 to autonomous Azure CLI repair

Scenario: `INVENTORY_BACKEND` changes from `builtin` to unsupported `cosmosdb-prod`.
Catalog routes return HTTP 503 with `CONFIG_ERROR` traces.
`/health/live` intentionally stays 200 so the Container App readiness probe does not mask the app-level config fault; the storefront and telemetry make the outage visible.

Trigger:

```bash
BAD_INVENTORY_BACKEND=cosmosdb-prod bash scripts/break-config.sh
```

While waiting 5–10 minutes for the alert, show the red storefront banner, `sre-config/skills/repair-trek-inventory-config.md`, KQL for 503s and `CONFIG_ERROR`, Container App revisions, and Activity Log.

Expected agent repair:

```bash
az containerapp update   --resource-group "rg-sre-agent-demo-${ENV_NAME}"   --name "ca-trek-api-${ENV_NAME}"   --set-env-vars INVENTORY_BACKEND=builtin
```

Expected verification: live env var is `builtin`, latest revision is running/receiving traffic, `/health/ready` is 200, `/api/v1/status` is `operational`, and 503s stop after repair.

Manual reset:

```bash
bash scripts/fix-config.sh
bash scripts/smoke-test.sh
```

## Demo 4 — Chat, scheduled task, and Q&A with the agent

Prompts:

```bash
bash scripts/ask-agent.sh "Summarize Contoso Trek health and recent errors. Cite evidence."

bash scripts/ask-agent.sh "Create a concise readiness report for ca-trek-api and ca-trek-web. Include alerts, recent 5xx trends, and deployment changes."

bash scripts/ask-agent.sh "Recommend a recurring scheduled task for Contoso Trek that catches issues before alerts fire."
```

Show thread citations, tool calls, and scheduled-task management in `sre.azure.com`.

## Troubleshooting notes

- The API Container App readiness probe is intentionally on `/health/live`; this prevents the platform from hiding the app-level `INVENTORY_BACKEND` fault by replacing the revision before the SRE Agent can observe it.
- Use `/health/ready` and `/api/v1/status` for application recovery validation.
- If the workflow URL differs from the documented URL, use the workflow summary value.

## Plan B materials

The coordinator will add `docs/session/video/sre-agent-demo.mp4`, an English narrated 6–8 minute recording.
Use it if alert latency, network, or identity issues interrupt the live demo.
Optional supporting screenshots can go under `docs/session/video/screenshots/`.

## Reset checklist

```bash
bash scripts/fix-config.sh
bash scripts/smoke-test.sh
```

Close or annotate demo GitHub issues created during rehearsal.
Do not delete Azure resources during the customer session unless teardown is explicitly agreed.
