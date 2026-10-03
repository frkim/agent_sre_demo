# Azure SRE Agent — FAQ

## 1. What is Azure SRE Agent?

Azure SRE Agent is a Microsoft-managed agentic AI service for operations workflows. It connects to Azure resources, observability tools, incident platforms, and source-code repositories to automate incidents, scheduled workflows, and grounded investigations. Source: https://learn.microsoft.com/en-us/azure/sre-agent/overview

## 2. Is it generally available?

Yes. The research brief cites the official Azure Updates RSS item announcing GA on March 11, 2026. Source: https://www.microsoft.com/releasecommunications/api/v2/azure/rss/558321

## 3. What changed in August 2026?

Microsoft announced the 30-day no-always-on-charge trial, GA of VNet integration, and public preview of Live Reports. Sources: https://www.microsoft.com/releasecommunications/api/v2/azure/rss/569760, https://learn.microsoft.com/en-us/azure/sre-agent/evaluate, https://learn.microsoft.com/en-us/azure/sre-agent/network-integration, https://learn.microsoft.com/en-us/azure/sre-agent/live-reports

## 4. Will it change production without approval?

Review mode is default for Azure infrastructure write actions and requires an SRE Agent Administrator to approve or deny. Autonomous mode is opt-in and still constrained by RBAC, per-subagent tool grants, and policies. Sources: https://learn.microsoft.com/en-us/azure/sre-agent/run-modes, https://learn.microsoft.com/en-us/azure/sre-agent/permissions

## 5. What is the difference between run mode and permissions?

Run mode controls approval workflow; permissions control resource access. The agent needs both workflow permission and resource permission to act. Sources: https://learn.microsoft.com/en-us/azure/sre-agent/run-modes, https://learn.microsoft.com/en-us/azure/sre-agent/permissions

## 6. What roles should we assign first?

Start least privilege: Readers for observers, Standard Users for operators, Authors for builders, Administrators for approvers and connector owners. Source: https://learn.microsoft.com/en-us/azure/sre-agent/user-roles

## 7. Can we pilot without touching production?

Yes. Use Reader permission level plus Review run mode so the agent investigates and proposes actions without broad write privileges. Sources: https://learn.microsoft.com/en-us/azure/sre-agent/permissions, https://learn.microsoft.com/en-us/azure/sre-agent/run-modes

## 8. Does Microsoft use our data to train models?

No. Microsoft documentation states customer data is not used to train AI models. Source: https://learn.microsoft.com/en-us/azure/sre-agent/data-privacy

## 9. Where is data stored?

Conversation history, prompts, responses, and resource analysis are stored and processed in the single Azure region selected at agent creation. Source: https://learn.microsoft.com/en-us/azure/sre-agent/data-privacy

## 10. Does it support VNet integration?

Yes. VNet integration is GA. Modes include Unrestricted, Limited, and Azure VNet. Source: https://learn.microsoft.com/en-us/azure/sre-agent/network-integration

## 11. What incident platforms are supported?

Azure Monitor, PagerDuty, and ServiceNow are supported. Only one incident platform is active per agent. Source: https://learn.microsoft.com/en-us/azure/sre-agent/incident-platforms

## 12. How fast does Azure Monitor ingestion happen?

The Azure Monitor alert scanner checks every 1 minute, supports up to 250 alerts per API call, and syncs status every 5 minutes. Source: https://learn.microsoft.com/en-us/azure/sre-agent/azure-monitor-alerts

## 13. What are response plans?

Response plans route incidents to a custom agent and autonomy level based on filters such as severity, service, type, and title keywords. Source: https://learn.microsoft.com/en-us/azure/sre-agent/incident-response-plans

## 14. What is memory?

SearchMemory spans past incidents, user memories, and knowledge base documents. Source: https://learn.microsoft.com/en-us/azure/sre-agent/memory

## 15. What are skills and subagents?

Skills are reusable procedures that can be auto-loaded; custom agents are specialists with prompts, tools, connectors, and skills. Sources: https://learn.microsoft.com/en-us/azure/sre-agent/overview, https://learn.microsoft.com/en-us/azure/sre-agent/incident-response-plans

## 16. How does GitHub integration work in this demo?

The demo uses Code Access configured by PAT through `PUT /api/v2/repos/{name}` plus a GitHub MCP connector at `https://api.githubcopilot.com/mcp/`. The code-investigator can search issues, file an issue with source file:line, and call `github_assign_copilot_to_issue` so GitHub Copilot coding agent opens a draft PR for human review.

## 17. Does it support Azure DevOps?

Yes. The research brief notes OAuth-based Azure DevOps connector capabilities and documentation indexing/search. Source: https://learn.microsoft.com/en-us/azure/sre-agent/overview

## 18. Can it work with non-Azure tools?

Yes through MCP connectors, managed connectors, and HTTP triggers. Sources: https://learn.microsoft.com/en-us/azure/sre-agent/mcp-connectors, https://learn.microsoft.com/en-us/azure/sre-agent/http-triggers, https://learn.microsoft.com/en-us/azure/sre-agent/managed-connectors

## 19. What MCP limits matter?

MCP budget is 80 tools per agent, health checks run every 60 seconds, and new tools are detected within 5 minutes. Source: https://learn.microsoft.com/en-us/azure/sre-agent/mcp-connectors

## 20. How is pricing calculated?

Pricing uses AAUs. Always-on is 4 AAUs per agent-hour; active flow is token-metered by type and model. Source: https://learn.microsoft.com/en-us/azure/sre-agent/pricing-billing

## 21. What is the verified AAU price?

Verified AAU prices from the Azure Retail Prices API: East US/East US 2 USD 0.10, France Central/Sweden Central USD 0.11, West Europe USD 0.14 effective 2026-10-01, and France Central EUR 0.10. Prices vary by region/currency; confirm current calculator values for formal quotes. Source: Azure Retail Prices API (https://prices.azure.com/api/retail/prices, meterName=SRE Agent Unit, serviceName Foundry Tools, productName Azure Agent Unit, queried 2026-10-03); pricing model source: https://learn.microsoft.com/en-us/azure/sre-agent/pricing-billing.

## 22. What do monthly examples look like?

Always-on floor is 2,920 AAU/month: about $292 East US or $321 France Central. 20 GPT-5.3 Codex investigations add about 234 AAU, or $23 East US / $26 France Central. 20 Claude Opus investigations add about 706 AAU, or $71 East US / $78 France Central. Prices vary by region/currency.

## 23. How do we control spend?

Set a monthly active-flow limit from 500 to 1,000,000 AAUs. Hitting it pauses chat/actions but always-on billing continues. Source: https://learn.microsoft.com/en-us/azure/sre-agent/pricing-billing

## 24. What does the 30-day trial include?

Always-on charges are waived for up to three new agents; active-flow consumption still applies. Source: https://learn.microsoft.com/en-us/azure/sre-agent/evaluate

## 25. Which regions are supported?

The research brief lists 22 supported regions; the agent deploys to one region and cannot be moved after creation. Source: https://learn.microsoft.com/en-us/azure/sre-agent/supported-regions

## 26. What preview limitations matter?

Managed connectors, Live Reports, Azure Connector Namespace, and control/data-plane REST APIs have preview caveats. Sources: https://learn.microsoft.com/en-us/azure/sre-agent/managed-connectors, https://learn.microsoft.com/en-us/azure/sre-agent/live-reports, https://devblogs.microsoft.com/azure-sdk/power-azure-sre-agent-with-connector-namespace/, https://learn.microsoft.com/en-us/azure/sre-agent/api-reference

## 27. How does the Contoso Trek demo prove boundaries?

The code-defect path creates a GitHub issue and Copilot draft PR without changing Azure resources. The config-fault path restores `INVENTORY_BACKEND=builtin` with Azure CLI and verifies recovery. Read-back shows per-subagent tool grants with `phantom=none`.

## 28. Why is the readiness probe on `/health/live`?

It is intentional for the demo: the config fault should remain visible to the storefront and SRE Agent instead of being hidden by platform readiness replacement. Use `/health/ready` and `/api/v1/status` to validate application recovery.

## 29. What should our first pilot look like?

Pick one Azure-hosted service, two alert types, Reader + Review, runbook upload, GitHub/ADO issue flow, and metrics for MTTR, toil, issue quality, draft-PR handoff quality, and candidate autonomous repairs.
