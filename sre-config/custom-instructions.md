# Contoso Trek operations — global instructions

Contoso Trek is an outdoor-gear storefront running on Azure Container Apps. These instructions apply to every investigation in resource group `${RG}` for environment `${ENV_NAME}`.

## Telemetry facts

Application telemetry flows from the API through OpenTelemetry into Application Insights and the workspace-based Log Analytics tables `AppRequests`, `AppExceptions`, and `AppTraces`.

`AppRoleName` is the Container App name (`ca-trek-api-<env>`), not the container name. Always match with:

```kusto
| where AppRoleName startswith "ca-trek-api"
```

## Fault classes

| Symptom | Class | Correct response |
| --- | --- | --- |
| HTTP 500, unhandled exception in `AppExceptions` | Code defect | File a GitHub issue with the exact `file:line`. Do not change Azure resources. |
| HTTP 503, `CONFIG_ERROR` in `AppTraces`, `/health/live` still 200 | Platform configuration fault | Restore `INVENTORY_BACKEND=builtin` on the API Container App, then verify recovery. |

A restart, scale change, or redeploy is not a valid fix for either scenario. Preserve evidence, classify the symptom, and only take the action assigned to that class.

## Evidence standard

State root cause as a specific artifact: a `file:line`, an environment variable value, or a named Activity Log change. Always include the time window and affected request count.
