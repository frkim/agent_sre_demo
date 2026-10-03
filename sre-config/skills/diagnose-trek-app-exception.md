---
name: diagnose-trek-app-exception
description: Load this skill when Contoso Trek returns HTTP 500, when an alert whose name contains "app-exception" fires, or when unhandled exceptions appear in AppExceptions for the ca-trek-api backend. It finds the exact source file and line, quantifies impact, and files a GitHub bug. Do not load it for HTTP 503 availability incidents.
---

# Diagnose a Contoso Trek application exception

Customers see HTTP 500 on product details and the API is recording unhandled exceptions. This is a code defect and must not be repaired with Azure control-plane changes.

## 1. Establish blast radius

```kusto
AppRequests
| where AppRoleName startswith "ca-trek-api"
| summarize Total=count(), Failed=countif(ResultCode == "500") by Name, bin(TimeGenerated, 5m)
| order by TimeGenerated desc
```

Record the impact window and count of failed requests.

## 2. Retrieve exception details

```kusto
AppExceptions
| where AppRoleName startswith "ca-trek-api"
| project TimeGenerated, ProblemId, OuterType, OuterMessage, Details, OperationId
| order by TimeGenerated desc
| take 20
```

The deliberate scenario produces `ZeroDivisionError` for climbing product details because unit price is calculated from `price / pack_size` and climbing products have `pack_size = 0`.

## 3. Correlate request and exception

```kusto
AppRequests
| where AppRoleName startswith "ca-trek-api" and ResultCode == "500"
| join kind=inner (AppExceptions | where AppRoleName startswith "ca-trek-api") on OperationId
| project TimeGenerated, Name, Url, OuterType, OuterMessage, Details
| order by TimeGenerated desc
```

## 4. Read source and identify the exact line

Use Code Access for `${GITHUB_REPO}`. Read the stack frame file and surrounding code. Root cause must be a real `file:line` and the throwing statement, not an inferred guess.

## 5. File the GitHub issue

Create an issue in `${GITHUB_REPO}` with labels `sre-agent` and `bug`.

Title format:

```text
[SRE] HTTP 500 on climbing product details - ZeroDivisionError
```

Body must include:

- Impact window and failed request count
- Reproduction path through the storefront
- Exception type and message
- Stack trace excerpt
- Source `file:line`
- Suggested minimal fix, such as guarding zero `pack_size` or representing climbing unit price without division
- Statement that no Azure resource was modified
