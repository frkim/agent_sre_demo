---
name: repair-trek-inventory-config
description: Load this skill when Contoso Trek catalog availability is degraded, when an alert whose name contains "availability" fires, or when ca-trek-api returns HTTP 503 with CONFIG_ERROR traces. It confirms an inventory backend configuration fault, correlates the activity log change, restores INVENTORY_BACKEND=builtin, and verifies recovery. Do not load it for HTTP 500 or AppExceptions incidents.
---

# Repair Contoso Trek inventory configuration

Catalog routes are returning HTTP 503. This is a platform configuration fault only when the API logs `CONFIG_ERROR` and no unhandled exception explains the symptom.

## 1. Confirm outage and start time

```kusto
AppRequests
| where AppRoleName startswith "ca-trek-api"
| summarize Requests=count(), Unavailable=countif(ResultCode == "503") by bin(TimeGenerated, 5m)
| order by TimeGenerated desc
```

## 2. Read the app-reported reason

```kusto
AppTraces
| where AppRoleName startswith "ca-trek-api"
| where Message has "CONFIG_ERROR" or Message has "INVENTORY_BACKEND"
| order by TimeGenerated desc
| take 20
```

If the evidence shows unhandled exceptions instead, stop and hand off to the application exception path.

## 3. Compare live configuration against baseline

```bash
az containerapp show -g ${RG} -n ca-trek-api-${ENV_NAME} --query "properties.template.containers[0].env" -o table
```

Known-good value: `INVENTORY_BACKEND=builtin`.

## 4. Correlate with the change

```bash
az containerapp revision list -g ${RG} -n ca-trek-api-${ENV_NAME} \
  --query "[].{name:name, created:properties.createdTime, active:properties.active, traffic:properties.trafficWeight}" -o table
```

```bash
az monitor activity-log list -g ${RG} --offset 6h \
  --query "[?contains(operationName.value, 'Microsoft.App/containerApps/write')].{time:eventTimestamp, caller:caller, status:status.value}" -o table
```

Name the caller and timestamp in the incident summary.

## 5. Remediate

```bash
az containerapp update -g ${RG} -n ca-trek-api-${ENV_NAME} --set-env-vars INVENTORY_BACKEND=builtin
```

Do not open a GitHub issue or request a code change for this incident.

## 6. Verify recovery

1. Re-read environment variables and confirm `INVENTORY_BACKEND=builtin`.
2. Confirm the latest revision is running and receiving traffic.
3. Confirm `GET /health/ready` returns 200.
4. Confirm `GET /api/v1/status` reports `operational`.
5. Re-run the request query and confirm 503s stop after the repair.

Post the command run and the recovery evidence in the incident thread.
