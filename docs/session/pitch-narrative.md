# Azure SRE Agent — pitch narrative

## 30-second elevator pitch

Azure SRE Agent is a Microsoft-managed agentic operations service that connects alerts, telemetry, Azure resource context, runbooks, memory, and source code so teams can investigate incidents faster and automate safe responses under explicit governance.
For an Azure-first operations team, it reduces on-call toil without handing production to an unbounded bot: start in Reader permissions and Review run mode, measure triage improvement, then graduate narrow, reversible repairs to autonomous execution.

## 2-minute pitch

Incidents still depend on humans stitching together alert payloads, dashboards, resource state, recent deployments, source code, tribal knowledge, and runbooks while the clock is running.
Azure SRE Agent shifts the model from manual tool-hopping to governed, evidence-driven agentic response.
It ingests incidents from Azure Monitor, PagerDuty, or ServiceNow; gathers context from Azure Monitor, Application Insights, Log Analytics, Resource Graph, ARM, GitHub, and Azure DevOps; remembers prior incidents and uploaded runbooks; and routes work to the right custom agent and skill.
In Review mode, it proposes Azure infrastructure actions for Administrator approval; in Autonomous mode, it executes only within configured RBAC and tool-policy boundaries.

In the Contoso Trek demo, the code-defect path uses Code Access plus a GitHub MCP connector: SRE Agent de-duplicates existing issues, files a GitHub issue with source file:line, then invokes `github_assign_copilot_to_issue` so GitHub Copilot coding agent opens a draft PR for human review.
For platform faults, a separate platform-operator subagent has Azure CLI write tools but no terminal or GitHub tools.

Microsoft reports internal use across 3,000+ services, 1.5M+ incidents processed, and up to 50% resolved autonomously.
InEight reported 80% reductions in incident investigation time and build-failure triage time.
The responsible pilot path is one service, two alert types, Reader + Review, seeded runbooks, GitHub/ADO issue flow, and metrics for MTTR, toil, and safe automation candidates.

## Narrative arc

1. **Problem:** On-call pain comes from context fragmentation, not lack of dashboards.
2. **Shift:** Azure SRE Agent turns fragmented evidence into a governed investigation and response loop.
3. **Trust:** Roles, run modes, RBAC, per-subagent tool grants, policies, hooks, network controls, and audit trail constrain action.
4. **Developer loop:** Incident → GitHub issue → Copilot coding agent draft PR → human-reviewed merge → SRE Agent verifies recovery.
5. **Proof:** Microsoft and customer proof points show measurable investigation and triage reduction.
6. **Economics:** AAUs make cost visible; verified regional AAU prices and budget caps support predictable pilots.
7. **Ask:** Start with a scoped Reader + Review pilot and measure before expanding autonomy.

## Persona messages

| Persona | Message | Anchor |
| --- | --- | --- |
| CTO / VP Engineering | Improve reliability execution without a platform re-org. | GA product; IaC deployable; Microsoft internal scale. |
| SRE lead | Reduce repetitive evidence gathering and make incident learning reusable. | Memory, knowledge, response plans, scheduled tasks. |
| Developer lead | Code defects become issues with stack trace, impact, source location, and Copilot coding agent draft PR hand-off. | GitHub Code Access + GitHub MCP connector; Demo 2. |
| Security / compliance | Autonomy is scoped by roles, Review mode, RBAC, per-subagent tool grants, tool policies, hooks, VNet, and audit. | Microsoft Learn governance docs; live read-back `phantom=none`. |
| Finance / FinOps | Cost has fixed and variable AAU components with verified regional prices, active-flow caps, and a 30-day always-on trial. | Pricing/billing docs and Retail Prices API. |

## Benefits with proof points

- Microsoft reports Azure SRE Agent scaled to 3,000+ internal services, processed more than 1.5M incidents, and resolved up to 50% autonomously. Source: https://developer.microsoft.com/blog/try-azure-sre-agent-with-no-always-on-charges/
- InEight reported 80% reduction in incident investigation time and 80% reduction in build-failure triage time. Source: https://developer.microsoft.com/blog/try-azure-sre-agent-with-no-always-on-charges/
- Pilot metrics to measure: MTTR, manual diagnostic steps, issue quality, time-to-developer handoff, repeat-incident rate, draft-PR turnaround, and avoided escalations.

## Pricing talk-track and cost example

Azure SRE Agent uses Azure Agent Units (AAUs).
Monthly bill has two parts:

1. **Always-on flow:** 4 AAUs per agent-hour from creation until deletion.
2. **Active flow:** token-based AAUs by input, output, cache read, and cache write; rates vary by model.

Verified AAU prices from the Azure Retail Prices API: East US/East US 2 USD 0.10, France Central/Sweden Central USD 0.11, West Europe USD 0.14 effective 2026-10-01, and France Central EUR 0.10. Prices vary by region/currency; confirm current calculator values for formal quotes.
Source: Azure Retail Prices API (https://prices.azure.com/api/retail/prices, meterName=SRE Agent Unit, serviceName Foundry Tools, productName Azure Agent Unit, queried 2026-10-03); pricing model source: https://learn.microsoft.com/en-us/azure/sre-agent/pricing-billing.

Worked examples:

- **Always-on floor:** 4 AAU × 730 h = 2,920 AAU/month ≈ **$292/month East US** or **$321/month France Central**.
- **20 GPT-5.3 Codex incident investigations:** 11.7 AAU × 20 ≈ 234 AAU ≈ **$23 East US** or **$26 France Central**.
- **20 Claude Opus investigations:** 35.3 AAU × 20 ≈ 706 AAU ≈ **$71 East US** or **$78 France Central**.
- **Small-team monthly shape:** one agent + 20 GPT investigations + 10 GPT remediations + 100 quick questions ≈ 3,585 AAU ≈ **$359 East US** or **$394 France Central**.
- **On-call hours comparison:** break-even hours = monthly agent cost ÷ customer loaded on-call engineering cost/hour. At an illustrative $100/hour, the small-team East US shape breaks even at about **3.6 saved hours/month**; replace with the customer's internal labor rate.

Controls: active-flow monthly allocation is 500 to 1,000,000 AAUs; hitting it pauses chat/actions but always-on continues; deleting stops both components; the 30-day trial waives always-on charges for up to three agents while active-flow charges still apply.

## Limits to state honestly

- Agent deploys to exactly one supported region and cannot move regions after creation.
- One incident platform is active per agent at a time.
- MCP capacity is 80 tools per agent.
- Custom-agent knowledge files are Markdown/text only, max 50 MB per file, up to 1,000 files per custom agent instance.
- Managed connectors, Live Reports, Azure Connector Namespace, and REST APIs have preview caveats.
- No public numeric max concurrent incidents/chat threads limit was found; validate production sizing with Microsoft.
- Prices vary by region/currency; confirm current calculator values for formal customer quotes.

## Objection handling

| Objection | Response |
| --- | --- |
| Data privacy | Microsoft docs state customer data is not used to train AI models and is tenant/subscription isolated. Conversation/content data is stored and processed in the selected Azure region; inference behavior depends on provider and region. |
| Will it change prod? | Review mode is default for Azure infrastructure writes and requires Administrator approval. RBAC, per-subagent tool grants, and tool policies further constrain actions. |
| Cost predictability | Use verified AAU rates, active-flow caps, dashboards, scoped response plans, and the trial. Always-on continues until deletion. |
| Hallucinations | Require cited evidence, use memory/knowledge, deny destructive actions, and use hooks/policies to audit or stop tool use. |
| Multi-cloud | Azure-native depth is the differentiator; non-Azure telemetry comes through MCP, managed connectors, and HTTP triggers. |
| Competitors | PagerDuty and Datadog have strengths in incident orchestration and telemetry-native workflows; cloud-neutral agents may fit non-Azure-first estates. Azure SRE Agent is strongest where Azure control-plane depth and governed IaC-managed autonomy matter. |

## Closing CTA

Agree a four-week pilot: select one Azure-hosted service and two alert types; create one agent in Reader + Review mode; upload runbooks; configure response plans; connect GitHub or Azure DevOps; measure MTTR, toil, issue quality, Copilot draft-PR handoff quality, and candidate autonomous repairs.
