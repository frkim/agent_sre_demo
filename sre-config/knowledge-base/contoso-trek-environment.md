# Contoso Trek environment

Reference facts for the Azure SRE Agent demo. These names are authoritative for environment `${ENV_NAME}` in resource group `${RG}`.

## Topology

| Component | Resource | Notes |
| --- | --- | --- |
| Storefront UI | Container App `ca-trek-web-${ENV_NAME}` | External ingress. nginx serves Vue and proxies `/api/*` to the API. |
| API | Container App `ca-trek-api-${ENV_NAME}` | Internal ingress only, port 8080. Container name is `trek-api`. |
| Telemetry | Application Insights `appi-trek-${ENV_NAME}` + Log Analytics `log-trek-${ENV_NAME}` | Workspace-based telemetry. |
| Registry | `acrtrek*` | Holds `trek-api` and `trek-web` images. |
| SRE Agent | `sre-trek-${ENV_NAME}` | Routes AzMonitor incidents to response plans. |
| Action group | `ag-sre-trek-${ENV_NAME}` | Azure Monitor alerts dispatch here. |

Both Container Apps run single revision mode with min 1 / max 1 replica for a predictable demo.

## API routes

| Route | Expected behavior |
| --- | --- |
| `GET /health/live` | 200 even when inventory config is invalid. |
| `GET /health/ready` | 200 when ready, 503 when `INVENTORY_BACKEND` is invalid. |
| `GET /api/v1/status` | `operational`, `degraded`, or `outage` with backend and recent error facts. |
| `GET /api/v1/products?category=Climbing` | Lists climbing products. |
| `GET /api/v1/products/{id}` | Product detail. Climbing products deliberately throw a `ZeroDivisionError` because `pack_size = 0`. |

## Known-good configuration

The API reads inventory from the `INVENTORY_BACKEND` environment variable.

**Known-good value: `INVENTORY_BACKEND=builtin`.** Any unsupported value, such as `cosmosdb-prod`, makes catalog routes return HTTP 503 with `CONFIG_ERROR` traces.

Read live configuration:

```bash
az containerapp show -g ${RG} -n ca-trek-api-${ENV_NAME} --query "properties.template.containers[0].env" -o table
```

Repair command:

```bash
az containerapp update -g ${RG} -n ca-trek-api-${ENV_NAME} --set-env-vars INVENTORY_BACKEND=builtin
```

## Alerts

| Alert | Fires on | Meaning |
| --- | --- | --- |
| `alert-trek-app-exception-${ENV_NAME}` | Any row in `AppExceptions` where `AppRoleName startswith "ca-trek-api"` | Code defect. Customers see HTTP 500 on product detail. |
| `alert-trek-availability-${ENV_NAME}` | More than 3 HTTP 503 responses in `AppRequests` where `AppRoleName startswith "ca-trek-api"` | Platform configuration fault. Catalog is down. |

Both log-search rules use 5-minute windows and 5-minute frequency. Allow several minutes for alert latency, or start a chat thread with the agent for demos.

## Useful KQL

Recent exceptions:

```kusto
AppExceptions
| where AppRoleName startswith "ca-trek-api"
| project TimeGenerated, ProblemId, OuterType, OuterMessage, Details, OperationId
| order by TimeGenerated desc
```

Availability:

```kusto
AppRequests
| where AppRoleName startswith "ca-trek-api"
| summarize Requests=count(), Errors=countif(ResultCode startswith "5") by ResultCode, bin(TimeGenerated, 5m)
| order by TimeGenerated desc
```

Configuration traces:

```kusto
AppTraces
| where AppRoleName startswith "ca-trek-api"
| where Message has "CONFIG_ERROR" or Message has "INVENTORY_BACKEND"
| order by TimeGenerated desc
```

## Runbook links

- Scenario 1 runbook: `sre-config/skills/diagnose-trek-app-exception.md`
- Scenario 2 runbook: `sre-config/skills/repair-trek-inventory-config.md`
- GitHub repository for issue filing: `${GITHUB_REPO}`
