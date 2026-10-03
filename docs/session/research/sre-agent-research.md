# Azure SRE Agent — Research Brief for Customer Session
**Compiled:** October 2, 2026 | **Purpose:** 1.5-hour customer session (deck + demo)
**Product:** Azure SRE Agent — portal: https://sre.azure.com | Docs: https://learn.microsoft.com/en-us/azure/sre-agent/ | Product page: https://azure.microsoft.com/en-us/products/sre-agent/

> Methodology note: All facts below are sourced from official Microsoft documentation (learn.microsoft.com, azure.microsoft.com, devblogs.microsoft.com, developer.microsoft.com, Azure Updates RSS/release-communications) wherever possible. Where only third-party/analyst sources were found, or Microsoft text was ambiguous/truncated, the item is explicitly flagged **[verify]**. Doc "ms.date"/"updated_at" metadata is cited where it helps establish recency.

---

## 1. Product status & timeline

| Date | Milestone | Source |
|---|---|---|
| **May 19, 2025** (17:15 UTC) | **Public preview announced** at Microsoft Build 2025 — "Azure SRE agent is a new agentic AI service that can free developers from the constant stress of late-night alerts by monitoring production systems 24/7, responding to incidents in real time, and autonomously troubleshooting issues." Category tags on the official release note: "In preview," "Features," "Microsoft Build." | Azure Updates RSS item 494483: https://www.microsoft.com/releasecommunications/api/v2/azure/rss/494483 |
| **~Oct/Nov 2025** (Ignite 2025 timeframe) | Public preview **expanded to all customers, no sign-up/waitlist required**; additional integration/extensibility capabilities (custom subagents, more connectors, governance controls) added. Exact single authoritative date not found on an official Microsoft page in this research pass — secondary aggregator (azurelook.com) places it in the Ignite 2025 window. **[verify exact date]** | https://azurelook.com/azure-update/expanding-the-public-preview-of-the-azure-sre-agent/ ; https://azurelook.com/azure-update/in-preview-public-preview-new-integration-and-extensibility-capabilities-to-azure-sre-agent/ |
| **March 11, 2026** (17:45 UTC) | **General Availability (GA)** — official Azure Updates entry: "[Launched] Generally Available: Azure SRE Agent with new capabilities." Description: "Azure SRE Agent is now generally available. This AI-powered operations agent helps teams improve uptime, reduce incident impact, and cut operational toil by accelerating diagnosis and automating response workflows. The GA release introduces deep context g[athering]…" (description truncated in feed). | Azure Updates RSS item 558321: https://www.microsoft.com/releasecommunications/api/v2/azure/rss/558321 ; see also https://techcommunity.microsoft.com/blog/appsonazureblog/a-paradigm-shift-in-cloud-operations-with-azure-sre-agent/4533244 |
| **June 2–3, 2026** (reported) | Microsoft Build 2026 — moved to San Francisco; SRE Agent featured in sessions/demos (per secondary reporting). Note: some secondary sources list May 19–22, 2026 — conflicting; treat exact Build 2026 dates as **[verify]**. | https://windowsreport.com/microsoft-shares-the-dates-for-its-build-2026-developer-conference/ ; https://www.livemint.com/technology/tech-news/satya-nadella-reveals-microsoft-build-2026-dates-flagship-developer-event-shifts-to-san-francisco-11772603203718.html |
| **Build 2026 (mid-2026)** | **Azure Connector Namespace** enters public preview — a managed MCP-server-hosting platform that removes the operational burden of self-hosting MCP servers for SRE Agent (and other agents). Catalog includes Azure SQL, Azure Cosmos DB MCP servers, GitLab, Jira, PagerDuty. GA "estimated for the end of 2026." | https://devblogs.microsoft.com/azure-sdk/power-azure-sre-agent-with-connector-namespace/ |
| **August 26, 2026** (16:50 UTC) | Official Azure Updates: **"[Launched] Generally Available: Azure SRE Agent 30-Day Trial."** Bundled with this announcement: (1) **30-day no-always-on-charge trial** for new customers (up to 3 agents), (2) **GA of VNet integration** (agent can route outbound traffic through customer VNet with NSG/DNS/firewall applied), (3) **Public preview of Live Reports** (saved, reusable, auto-refreshing operational dashboards built from chat). | Azure Updates RSS item 569760: https://www.microsoft.com/releasecommunications/api/v2/azure/rss/569760 ; full post: https://developer.microsoft.com/blog/try-azure-sre-agent-with-no-always-on-charges/ |
| Ongoing (docs dated through **Sept 18, 2026**) | Most-recently-updated doc pages found in this research: `supported-regions` (updated_at 2026-09-18), `evaluate` (2026-09-25), `overview` (2026-08-27), `managed-connectors` preview (2026-08-20), `live-reports` preview (2026-08-25). No announcements found dated September or October 2026 beyond doc-freshness updates. | learn.microsoft.com/en-us/azure/sre-agent/ (page metadata) |

**Newest features (chronological, most recent first) — for a "what's new" slide:**
1. **Live Reports (public preview, Aug 2026)** — natural-language-authored, saved dashboards that refresh from connected data without re-spending tokens on each view (only authoring/model-assisted-analysis consumes AAUs; plain data refresh does not). Supports Kusto, MCP connectors, work items, charts/tables/status indicators; 5-minute connector result caching; sandboxed iframe with validated tool manifest for security; optional action buttons (acknowledge incident, open work item). — https://learn.microsoft.com/en-us/azure/sre-agent/live-reports
2. **VNet integration — GA (Aug 2026)** — three network control modes: Unrestricted (default), Limited (wildcard allow-list), Azure VNet (full egress routing through delegated subnet with your NSG/DNS/firewall). — https://learn.microsoft.com/en-us/azure/sre-agent/network-integration
3. **30-Day free trial — GA (Aug 2026)** — waives always-on charges for new customers, up to 3 agents, 30 days per agent from creation. — https://learn.microsoft.com/en-us/azure/sre-agent/evaluate
4. **Azure Connector Namespace (public preview, mid-2026)** — managed MCP server hosting (Azure SQL, Cosmos DB, GitLab, Jira, PagerDuty MCP servers), removing self-hosting burden; "bring-your-own server" support in development. — https://devblogs.microsoft.com/azure-sdk/power-azure-sre-agent-with-connector-namespace/
5. **Managed connectors (preview)** — governed SaaS connectors: Google Drive, SharePoint, Notion, Confluence, Trello, Planner, Box, Dropbox, Office 365 Outlook, Teams, Gmail, OneNote, Power BI — with per-operation allow-listing and parameter locking (user-defined vs. agent-defined). — https://learn.microsoft.com/en-us/azure/sre-agent/managed-connectors
6. **GA (March 11, 2026)** with "deep context" gathering capabilities (description truncated in official feed; implies enhanced cross-source correlation at GA). — RSS 558321 (above)
7. **Agent hooks** (Stop, PostToolUse events; prompt-based or command/script-based) for governance checkpoints. — https://learn.microsoft.com/en-us/azure/sre-agent/agent-hooks
8. **Tool access policies** (Allow/Ask/Deny at Global/Custom-agent/Thread scope) — https://learn.microsoft.com/en-us/azure/sre-agent/tool-access-policies
9. **HTTP triggers** — named webhook endpoints to invoke the agent from CI/CD, Datadog, Dynatrace, Jira, Splunk, Grafana, etc. — https://learn.microsoft.com/en-us/azure/sre-agent/http-triggers
10. **Custom agents / Agent Canvas / subagent builder** with handoff chains, `/agent` invocation, YAML definitions (`system_prompt`, `handoff_description`, `tools`, `connectors`, `enable_skills`/`allowed_skills`). — https://learn.microsoft.com/en-us/azure/sre-agent/sub-agents

---

## 2. Core capabilities

### How it works (operating model)
SRE Agent connects to Azure resources, observability tools, incident platforms, and source-code repos so engineers investigate with full context in one place. It gathers signals, compares current issues to prior investigations, and runs governed automation within configured permissions, run modes, and policies. Three usage patterns: **(1) Automate incidents** (alert → query → correlate → root cause → mitigation proposal), **(2) Automate scheduled workflows** (proactive health checks/compliance sweeps), **(3) Investigate & advise** (natural-language Q&A with grounded, cited answers). — https://learn.microsoft.com/en-us/azure/sre-agent/overview

Five **extension points**: Skills, Custom agents, Python tools, MCP servers, Agent hooks. — same source.

### Incident response & incident platforms
- Supported incident platforms: **Azure Monitor** (native, no credentials needed — uses the agent's managed identity), **PagerDuty** (API access key), **ServiceNow** (basic auth or OAuth 2.0, with real connectivity validation at setup). Only **one incident platform active at a time**; switching disconnects the current one. — https://learn.microsoft.com/en-us/azure/sre-agent/incident-platforms
- **Azure Monitor alerts**: scanner checks every **1 minute**; up to **250 alerts per API call**; initial scan lookback **1 day**, max scan window **29 days**; merge lookback **7 days** (repeat firings from same rule merge into one thread); status sync every **5 minutes**. Requires **Monitoring Contributor** role at subscription scope. Severities Sev0 (Critical) → Sev4 (Verbose). — https://learn.microsoft.com/en-us/azure/sre-agent/azure-monitor-alerts
- **PagerDuty**: scanner polls every minute, picks up incidents **within 1–2 minutes** of firing; priority mapping P1–P5 → agent severity 1–5; status sync Triggered→Acknowledged→Resolved; tracks agent-mitigated vs. agent-assisted vs. human-resolved. — https://learn.microsoft.com/en-us/azure/sre-agent/pagerduty-incidents
- **ServiceNow**: scanner polls every minute; supports assignment-group scoping, category/priority filtering (Critical→Planning); can update incident fields (assignment group, category, impact) directly from chat. — https://learn.microsoft.com/en-us/azure/sre-agent/servicenow-incidents
- **Rich incident cards** in chat show severity badge, timestamp, title (platform-prefixed), status, description, response plan. — https://learn.microsoft.com/en-us/azure/sre-agent/incident-platforms
- **Incident response plans**: route incidents to a specific **custom agent + autonomy level** based on filters — severity/priority (multiselect), impacted service, incident type (Default/Major/Security), title-contains keyword. Plans can be toggled on/off without deletion. — https://learn.microsoft.com/en-us/azure/sre-agent/incident-response-plans

### Autonomous vs. review modes (run modes) and access levels
- **Run modes** (per response plan or per scheduled task): **Review** (default) — agent proposes, an **SRE Agent Administrator** must Approve/Deny for Azure infrastructure write actions (Azure CLI, ARM operations); other actions (emails, Teams posts, external data queries) proceed per agent reasoning unless governed by Hooks/Tool Access Policies. **Autonomous** — agent executes immediately and reports results; best for non-prod/trusted recurring tasks. — https://learn.microsoft.com/en-us/azure/sre-agent/run-modes
- Run modes ≠ permissions: *"Run modes control the approval workflow… [Permissions] control resource access… The agent needs both conditions satisfied to act."* — same source.
- **Permission levels** (chosen at agent creation, applied to the managed identity on selected resource groups): **Reader** (core monitoring + resource-type reader roles; prompts for temporary elevation via OBO when write access is needed) vs. **Privileged** (core monitoring + resource-type-specific *contributor* roles, e.g., Container App Contributor if Container Apps detected). Always-assigned baseline roles regardless of level: Reader (RG), Log Analytics Reader (RG), Monitoring Reader (RG), Monitoring Contributor (subscription). No resource groups assigned at creation ⇒ **zero permissions** by default. — https://learn.microsoft.com/en-us/azure/sre-agent/permissions
- **On-behalf-of (OBO)**: when the managed identity lacks permission, the agent can temporarily use the requesting user's Entra credentials for that one action (not retained). Only **SRE Agent Administrators** can authorize OBO; **Standard Users cannot**; **personal Microsoft accounts (MSA) cannot authorize OBO at all** — only work/school (Entra ID) accounts. — same source.
- ARM-level `actionConfiguration.mode` enum: `Autonomous | ReadOnly | Review`; `actionConfiguration.accessLevel`: `High | Low`. — https://learn.microsoft.com/en-us/azure/templates/microsoft.app/agents

### Memory / knowledge base
- **Unified `SearchMemory`** spans three sources simultaneously: **past incidents** (prior resolution steps), **user memories** (explicitly saved facts), **knowledge base** (uploaded runbooks/docs) — responses include clickable citations. — https://learn.microsoft.com/en-us/azure/sre-agent/memory
- **Automatic learning**: 30 minutes after a thread goes quiet, the agent extracts symptoms, steps that worked, root cause, and pitfalls, and indexes them; prioritizes same-resource history first.
- **Knowledge directory**: `memories/synthesizedKnowledge/` with an always-loaded `overview.md` (~2,000-character budget) plus topic files (`architecture.md` ~1,500 chars, `team.md` ~500, `logs.md` ~1,500, `deployment.md` ~1,000, `auth.md` ~800, `debugging.md` ~1,000, `queries/*.md` ~1,000 each).
- **User memories**: chat commands `#remember`, `#retrieve`, `#forget` for discrete, explicit facts (distinct from auto-learned knowledge files).
- **Knowledge base uploads** (agent-level, via Builder): documents become searchable automatically. (See §4 Limits for file-size/type caps.)

### Custom instructions, skills, subagents (custom agents)
- **Skills** = reusable procedures (`SKILL.md`) + optional attached tools (Azure CLI, Kusto, Python, MCP) + supporting files; **auto-loaded** by the agent when relevant — no explicit invocation needed. — https://learn.microsoft.com/en-us/azure/sre-agent/skills
- **Custom agents** ("subagents") = explicit, invoked via `/agent` slash command; built in **Builder → Agent Canvas**; YAML definition includes `name`, `system_prompt`, `handoff_description`, `tools`, `connectors`, `enable_skills`/`allowed_skills`. Several specialist agents ship ready-made; you can build your own. Support **handoff chains** (one custom agent hands off to the next, sharing the **same conversation context** — no "clean slate"). Patterns: Domain Expert (VM/AKS/Network expert), Task Specialist (Log Analyzer, Cost Optimizer, Security Scanner), Workflow Executor. Agent Canvas has **Canvas view, Table view, Test playground**. — https://learn.microsoft.com/en-us/azure/sre-agent/sub-agents
- Custom-agent **knowledge base**: supports **Markdown (.md) / text (.txt) only**, **max 50 MB per file**, **up to 1,000 files per custom agent instance**. — same source.
- Custom instructions are set via the `system_prompt` field on a custom agent (there is no separate dedicated "custom instructions" doc page found; it's part of the Agent Canvas / sub-agents workflow). **[verify there is no additional top-level "custom instructions" setting beyond system_prompt / skills]**

### Response plans / incident filters
Covered above under Incident response. Filter criteria: Severity/Priority (multiselect), Impacted service, Incident type, Title-contains keyword. Each plan = Incident filter + Custom agent handler (agent + run mode). — https://learn.microsoft.com/en-us/azure/sre-agent/incident-response-plans

### Scheduled tasks
Natural-language-defined, recurring investigations (not literal cron jobs) — each run creates a full conversation thread using connectors/tools/knowledge/memory; can catch sub-threshold trends (e.g., "error rate trending up 15% day-over-day" before alerting fires). Managed from **Scheduled tasks** in the left nav; can be created/edited from portal or chat. — https://learn.microsoft.com/en-us/azure/sre-agent/scheduled-tasks

### HTTP triggers
Named webhook endpoints, each with a unique URL, a configured prompt, an assigned agent (default or custom), and an autonomy level. External `POST` with optional JSON body (merged into the prompt as context). Execution history logs timestamp/thread link/success-failure; can be enabled/disabled (disabled → 404). Built for CI/CD failures, Datadog/Dynatrace/Jira/Splunk/Grafana webhooks. — https://learn.microsoft.com/en-us/azure/sre-agent/http-triggers

### MCP connectors
- MCP = open standard (modelcontextprotocol.io) wrapping external services as agent-callable tools. Two transports: **Streamable-HTTP** (remote/SaaS, e.g., Datadog, GitHub, New Relic) and **stdio** (local processes). Auto-discovery of tools; namespaced tool registration (e.g., `my-datadog_list_metrics`) to avoid collisions; **60-second health-check heartbeat** with auto-recovery; new tools on a connected server detected automatically **within 5 minutes**. **Tool capacity: 80 tools per agent** with a color-coded budget bar. — https://learn.microsoft.com/en-us/azure/sre-agent/mcp-connectors
- Preconfigured/native partner MCP connectors mentioned across docs: **Datadog, Splunk, New Relic, Dynatrace, Elasticsearch, GitHub**. (Grafana and Jira appear as HTTP-trigger/webhook sources and Connector-Namespace catalog items rather than confirmed native MCP connectors — **[verify Grafana/Jira native-MCP vs. webhook-only status]**.)

### Code Access / GitHub & Azure DevOps integration, hand-off to Copilot coding agent
- **GitHub connector** — three distinct connection types usable together: **Code Access** (Builder > Code Access: code search, file read by path/branch, error-to-source correlation, semantic code search), **GitHub Connector** (Builder > Connectors: create/list issues, open/merge PRs, trigger/track GitHub Actions workflows), **GitHub MCP** (full GitHub tool catalog via MCP with approval policies). Auth: **OAuth** (github.com only, **limit 10 tokens per agent**), **PAT** (fine-grained, `repo` scope), **BYO GitHub App** (private key in Key Vault; **required** for GitHub Enterprise Cloud `<tenant>.ghe.com`). — https://learn.microsoft.com/en-us/azure/sre-agent/github-connector
- **Azure DevOps**: OAuth-based connector; Azure DevOps **Documentation** connector indexes/searches wikis; agent can be pointed at failed pipelines (build/release/stage failures) plus PR/branch events to proactively find what a recent change broke. — https://learn.microsoft.com/en-us/azure/sre-agent/evaluate ; https://learn.microsoft.com/en-us/azure/sre-agent/connectors
- **GitHub Copilot coding agent hand-off**: Pattern described across Microsoft Reactor sessions and community workshops — SRE Agent investigates/root-causes an incident, pauses in Review mode for human approval, creates a GitHub Issue / Azure Boards work item with the investigation summary, and a human (or policy) triggers **GitHub Copilot coding agent** to draft a PR referencing the incident; PR is reviewed/merged by a human, and SRE Agent observes post-deploy signals to verify recovery. A GA launch video is titled **"Root Cause Analysis with Code Context: Azure SRE Agent + GitHub Integration — GA Launch."** This hand-off flow is best documented in community/partner content rather than a single official Learn page — **[verify exact productized "hand-off" mechanism / whether it's a point-and-click feature vs. a manual/scripted pattern]**. — https://github.com/microsoft/sre-agent (videos section); https://developer.microsoft.com/en-us/reactor/events/27562/ ("Azure SRE Agent and App Modernisation with GitHub Copilot"); https://stochasticcoder.com/2026/04/29/beyond-the-alert-building-self-healing-pipelines-with-azure-sre-agent-and-github-copilot/ (third-party)

### Teams / Outlook connectors
Built-in **collaboration-tool connectors**: "Send notification (Teams)" (post findings/updates to Teams channels) and "Send email (Outlook)" (email investigation summaries/reports). Richer governed versions — **Office 365 Outlook** and **Teams** — are also available as **Managed Connectors** (preview) with per-operation allow-listing and parameter locking. — https://learn.microsoft.com/en-us/azure/sre-agent/connectors ; https://learn.microsoft.com/en-us/azure/sre-agent/managed-connectors

### Kusto / Azure Data Explorer connectors
Built-in connector category "Data sources": **Database query (ADX)** — run predefined KQL against Kusto clusters; **Database indexing (ADX)** — auto-learns Kusto schema so the agent can generate queries dynamically. Even without a connector, Log Analytics/Application Insights (which are Kusto-based) are queryable natively via managed identity. — https://learn.microsoft.com/en-us/azure/sre-agent/connectors

### Python / terminal tools
**Code execution** tool category: Python and shell execution in **sandboxed environments**, built-in (no setup). Custom tools can also be authored as Kusto, Python, Link, and HTTP tools in the Builder UI. Agent hooks can likewise be implemented as **Command** (bash/Python script in a sandbox) or **Prompt** (LLM-evaluated) checks. — https://learn.microsoft.com/en-us/azure/sre-agent/tools ; https://learn.microsoft.com/en-us/azure/sre-agent/agent-hooks

### Knowledge graph / resource discovery
- Built-in **Azure Resource Graph** access discovers resources/relationships/topology across subscriptions (no connector needed) — "blast radius" / dependency mapping for incident impact analysis. — https://learn.microsoft.com/en-us/azure/sre-agent/connectors ; https://learn.microsoft.com/en-us/azure/sre-agent/diagnose-azure-observability
- ARM schema exposes a dedicated **`knowledgeGraphConfiguration`** block on the `Microsoft.App/agents` resource (`identity`, `managedResources[]`) — i.e., the knowledge graph is a first-class, declaratively configured control-plane concept, not just an emergent behavior. — https://learn.microsoft.com/en-us/azure/templates/microsoft.app/agents
- Combined with the **memory/knowledge** system (synthesized knowledge files) and **Live Reports**, this forms a persistent, queryable model of "what exists" (topology) + "what we know" (learnings) + "what's happening now" (telemetry).

### Supported Azure services
Built-in, no-connector-required diagnostic/operational tools cover: **Azure Monitor / Application Insights / Log Analytics / Azure Resource Graph / Azure Resource Manager (ARM) & Azure CLI** (read + modify **any** Azure resource type) and **AKS** (kubectl commands, cluster/node-pool/pod/workload diagnostics). Named resource types with deeper diagnostics: **Azure Container Apps, Azure Functions (Function Apps), Azure App Service** (web app health, memory, custom domains, 500-error analysis, availability), plus specialized tools for **CPU profiling, API Management diagnostics, deployment verification, reliability assessment, remediation actions**, and Grafana-integrated visualization/chart generation. **Azure SQL** and **Cosmos DB** are supported through the general Resource Graph/ARM + Monitor path and (per the Connector Namespace catalog) dedicated MCP servers for deeper query access. — https://learn.microsoft.com/en-us/azure/sre-agent/tools ; https://learn.microsoft.com/en-us/azure/sre-agent/diagnose-azure-observability ; https://devblogs.microsoft.com/azure-sdk/power-azure-sre-agent-with-connector-namespace/ — **[verify granular Azure SQL/Cosmos DB "native tool" depth vs. generic ARM/Monitor coverage — no dedicated Learn page found enumerating a full per-service capability matrix]**

### Non-Azure observability sources
Native/partner **MCP connectors** confirmed in official docs: **Datadog, Splunk, New Relic, Dynatrace, Elasticsearch**. **Grafana** appears as a visualization/dashboard integration target and HTTP-trigger source; **Jira** appears as an HTTP-trigger source and a planned Connector Namespace catalog entry. — https://learn.microsoft.com/en-us/azure/sre-agent/mcp-connectors ; https://learn.microsoft.com/en-us/azure/sre-agent/http-triggers ; https://devblogs.microsoft.com/azure-sdk/power-azure-sre-agent-with-connector-namespace/

### Models used
- Two selectable **providers**: **Azure OpenAI** (GPT-5 family, e.g., GPT-5, GPT-5.2) and **Anthropic** (Claude family, e.g., Claude Opus 4.5/4.6, Claude Sonnet 4.6). You pick the **provider**; **the agent automatically selects the best model within that provider per task** — described in docs as "Your agent automatically selects the best model within your chosen provider. No manual model configuration is needed," i.e., the "Automatic" behavior the user referenced is the *default and only* mode — there is no manual per-model picker exposed. — https://learn.microsoft.com/en-us/azure/sre-agent/model-provider-selection
- Provider defaults by region: **Anthropic default** in East US 2 / Australia East (commercial, non-EU); **Azure OpenAI default** in Sweden Central / UK South and generally **for EU/EFTA/UK** customers (Anthropic is opt-in there, and is **excluded from EU Data Boundary** commitments). **Anthropic is not available at all in Government clouds (GCC/GCC High/DoD) or sovereign clouds** — Azure OpenAI is forced there. — https://learn.microsoft.com/en-us/azure/sre-agent/data-privacy ; https://learn.microsoft.com/en-us/azure/sre-agent/model-provider-selection
- Pricing-table model names actually billed (slightly different vintage labels than the provider-selection page, reflecting that the catalog updates over time): **Claude Opus 4.6, GPT 5.3 Codex, GPT 5.2**. — https://learn.microsoft.com/en-us/azure/sre-agent/pricing-billing

---

## 3. PRICING in detail

**Unit of measure:** **Azure Agent Units (AAUs)** — "a standardized measure of agentic processing used across all prebuilt Azure agents." Two components make up the monthly bill. — https://learn.microsoft.com/en-us/azure/sre-agent/pricing-billing

### Always-on flow (fixed cost)
| Component | Rate |
|---|---|
| Always-on flow | **4 AAUs per agent-hour** |

- Accrues from **agent creation** until the agent is **deleted** — independent of usage. Stopping an agent halts active-flow but **not** always-on billing; only **deletion** stops always-on charges. — same source.
- **List price of 1 AAU was reported by a web-search aggregator as $0.10 USD** (⇒ implies $0.40/agent-hour always-on) — **this exact USD figure was not independently confirmed on an official Microsoft Learn/pricing page fetch in this research pass; treat as [verify] and confirm live on the Azure Pricing Calculator before quoting to a customer.** The official `azure.microsoft.com/en-us/pricing/details/sre-agent/` page did not render pricing content via fetch (returned a generic "talk to sales" placeholder) — **use the live Azure Pricing Calculator link below at demo time for authoritative, region-specific numbers.**
- Pricing calculator / official pricing page: https://azure.microsoft.com/en-us/pricing/details/sre-agent/ (consistently referenced from Learn docs as the source of truth for current rates — fetch this live before the customer session).

### Active flow (variable cost) — token-to-AAU conversion
Every token is metered by type: **Input, Output, Cache read, Cache write.** Total active-flow AAUs for a task = sum across all four types.

**AAU rates per 1,000,000 tokens, by model** (as published on the pricing-billing Learn page):

| Model | Input | Output | Cache read | Cache write |
|---|---|---|---|---|
| Claude Opus 4.6 | 100 AAUs | 500 AAUs | 10 AAUs | 125 AAUs |
| GPT 5.3 Codex | 35 AAUs | 280 AAUs | 3.5 AAUs | 0 AAUs |
| GPT 5.2 | 35 AAUs | 280 AAUs | 3.5 AAUs | 0 AAUs |

*Note: "Azure might add more models and providers in the future. Azure sets AAU rates and might update them as new models are released."* — https://learn.microsoft.com/en-us/azure/sre-agent/pricing-billing

### Worked examples (from the official docs, Claude Opus 4.6 / GPT 5.3 Codex)

| Scenario | Input | Output | Cache read | Cache write | **Claude Opus 4.6 AAUs** | **GPT 5.3 Codex AAUs** | Example prompt |
|---|---|---|---|---|---|---|---|
| Quick question | ~20K | ~2K | ~15K | ~5K | **~3.8** | **~1.3** | "Show me recent alerts" |
| Incident investigation | ~200K | ~15K | ~150K | ~50K | **~35.3** | **~11.7** | Automated incident from Azure Monitor |
| Full remediation | ~500K | ~40K | ~400K | ~100K | **~86.5** | **~30.1** | "Diagnose and fix the failing deployment" |

**Worked math (Claude Opus 4.6, "quick question"):**
| Token type | Tokens | Rate/1M | AAUs |
|---|---|---|---|
| Input | 20K | 100 | 2.0 |
| Output | 2K | 500 | 1.0 |
| Cache read | 15K | 10 | 0.15 |
| Cache write | 5K | 125 | 0.625 |
| **Total** | | | **3.775 AAUs** |

— https://learn.microsoft.com/en-us/azure/sre-agent/pricing-billing

### Monthly cost framing (illustrative — build live with the pricing calculator for the customer's region)
A simple monthly estimate = **(always-on AAUs/hr × 730 hrs) + (active-flow AAUs per task × tasks/month)** × price-per-AAU. Example shape only (confirm $/AAU live): if always-on = 4 AAU/hr × 730 hrs/month ≈ **2,920 AAUs/month** just to keep one agent provisioned, *before* any usage — this is a useful "floor cost" talking point, but get the live $/AAU from the calculator rather than quoting the unverified $0.10/AAU figure found in secondary sources.

### Free allowance / trial
- **30-day evaluation trial**, GA'd August 26, 2026: **always-on charges waived** for up to **3 agents per account**; **active-flow/consumption charges still apply** during the trial. Trial clock starts the day you create your first agent and ends 30 days later (**per-agent trial window**, i.e., each new agent gets its own 30 days). **Deleted agents still count toward the 3-agent cap.** No feature gating during trial — only a billing difference. When the trial ends, **standard pricing (including always-on) applies automatically with no re-confirmation step**; only deleting the agent before trial-end avoids the charge. A portal banner shows remaining trial time. — https://learn.microsoft.com/en-us/azure/sre-agent/evaluate
- Costs included in the standard price: agent compute/orchestration, conversation/knowledge-base storage, AI model usage, Azure-service integration. **Separate charges may apply** for: Azure Monitor logs/metrics consumption, third-party integrations, data egress. — https://learn.microsoft.com/en-us/azure/sre-agent/faq

### Billing controls & monitoring
- **Monthly AAU allocation limit**: configurable in **Settings > Agent consumption**; **min 500, max 1,000,000 AAUs**, applies to **active flow only** (always-on billing is unaffected and continues even if the limit is hit). Hitting the limit makes the agent **unavailable for chat/actions** until next month (always-on keeps billing). Limit **increases** take effect immediately; **decreases** take effect next billing month.
- Dashboards: **Monthly AAU limit**, **Total active-flow consumption** (donut by thread type: Chats/Incidents/Scheduled tasks/Triggers), **Daily active-flow consumption** (stacked bar), **Consumption by thread** (per-thread AAU cost table).
- Action-vs-billing table: **Set budget limit (hit)** → active flow stops, always-on continues, resets automatically next month. **Stop agent** → active flow stops, always-on continues, resume via Settings > Basics > Start. **Delete agent** → both stop permanently; only way to fully zero out costs.
- Cost tips (official): add skills/knowledge/persistent memory to reduce wasted tokens; filter incidents with response plans; batch with scheduled tasks instead of continuous polling; test in chat/Playground before automating; stop idle agents; delete unused agents. — all from https://learn.microsoft.com/en-us/azure/sre-agent/pricing-billing

---

## 4. LIMITS & quotas

| Area | Limit / detail | Source |
|---|---|---|
| **Supported regions (22 confirmed)** | Australia East, Brazil South, Canada Central, Central India, Central US, East Asia, East US 2, France Central, Italy North, Japan East, Japan West, Korea Central, North Central US, South Africa North, South India, Southeast Asia, Spain Central, Sweden Central, UK South, West Central US, West US 2, West US 3. (Resource provider: **Microsoft.App**; resource type **Microsoft.App/agents**.) If the Region dropdown is empty for your subscription, you must submit a registration request via GitHub Issues. | https://learn.microsoft.com/en-us/azure/sre-agent/supported-regions |
| **Agent-to-region binding** | Each agent deploys to **exactly one region in one subscription**; it can still *manage* resources in any region/subscription where its managed identity has RBAC. No multi-region agent deployment; region can't be changed after creation. | same source |
| **Trial agent cap** | **Up to 3 agents per account** during the 30-day evaluation trial (deleted agents still count against the cap). | https://learn.microsoft.com/en-us/azure/sre-agent/evaluate |
| **Active-flow AAU allocation** | Configurable **min 500 / max 1,000,000 AAUs per month** per agent. | https://learn.microsoft.com/en-us/azure/sre-agent/pricing-billing |
| **MCP tool capacity** | **80 tools per agent** (budget bar with color-coded warnings as you approach the cap). | https://learn.microsoft.com/en-us/azure/sre-agent/mcp-connectors |
| **MCP health/discovery cadence** | 60-second health-check heartbeat; new tools on a connected server auto-detected within **5 minutes**. | same source |
| **Custom-agent knowledge base** | File types: **.md / .txt only**; **max 50 MB per file**; **up to 1,000 files per custom agent instance**. | https://learn.microsoft.com/en-us/azure/sre-agent/sub-agents |
| **GitHub OAuth tokens** | **Limit of 10 tokens per agent** (OAuth connection type). | https://learn.microsoft.com/en-us/azure/sre-agent/github-connector |
| **Azure Monitor alert scanner** | Scan interval 1 min; **250 alerts per API call**; initial lookback 1 day; **max scan window 29 days**; merge lookback 7 days; status sync every 5 min. | https://learn.microsoft.com/en-us/azure/sre-agent/azure-monitor-alerts |
| **Incident platforms concurrency** | Only **one incident platform active at a time** per agent (Azure Monitor, PagerDuty, ServiceNow are mutually exclusive — switching disconnects the previous one). | https://learn.microsoft.com/en-us/azure/sre-agent/incident-platforms |
| **Concurrent incidents / chat-thread caps** | **No explicit numeric "max concurrent incidents" or "max concurrent chat threads" limit was found published** on official SRE Agent docs in this research pass. Practical throughput is governed by the AAU consumption limit and underlying Container Apps compute, not a stated hard cap. **[verify — not publicly documented as of this research]** | n/a |
| **Live Reports data freshness** | Connector results may be served from a cache of **up to 5 minutes** old; "Reload" forces a fresh pull. | https://learn.microsoft.com/en-us/azure/sre-agent/live-reports |
| **Resource groups per agent** | No fixed numeric cap found; agent can be scoped to **any number of resource groups** selected at creation/modification — permissions propagate automatically when a resource group is added, and are fully revoked when removed (you **cannot** remove individual permissions, only entire resource groups). | https://learn.microsoft.com/en-us/azure/sre-agent/permissions |
| **Data residency** | Agent **stores and processes all conversation/content data in the single Azure region** selected at creation, regardless of where the managed resources live. Inference for Anthropic/Azure OpenAI models **may occur outside** that region; **EU-data-boundary (EUDB) agents using Azure OpenAI keep inference within the EU data boundary**; **Anthropic is never covered by EUDB** (data may be processed in the US). **Anthropic is unavailable entirely in GCC/GCC High/DoD and sovereign clouds** (Azure OpenAI is the forced default there). | https://learn.microsoft.com/en-us/azure/sre-agent/data-privacy |
| **RBAC roles (4 built-in, agent-scoped)** | **SRE Agent Reader** (view threads/logs/incidents only), **SRE Agent Standard User** (chat, diagnostics, request actions, scheduled tasks, knowledge uploads, repo connectors — but **cannot** approve actions, create custom agents, or delete resources), **SRE Agent Author** (create custom agents, author response plans, configure incident management — but **cannot** chat, approve actions, upload knowledge, or add repo connectors **in the portal**, due to missing `memory/write`/`threads/write` data actions — though ARM `extendedAgents` paths can work for Authors), **SRE Agent Administrator** (full control: approve actions, manage connectors, delete resources). Data-plane/API-reference doc lists a slightly different 3-role shorthand: **SRE Agent Administrator / SRE Agent User / SRE Agent Reader** — treat "Standard User" and "User" as the same role, naming varies slightly across docs. | https://learn.microsoft.com/en-us/azure/sre-agent/user-roles ; https://learn.microsoft.com/en-us/azure/sre-agent/api-reference |
| **Required permissions to CREATE an agent** | **Owner**, or **Contributor + User Access Administrator**, on the subscription or target resource group; **Microsoft.App resource provider must be registered** for the subscription. | https://learn.microsoft.com/en-us/azure/sre-agent/faq ; https://learn.microsoft.com/en-us/azure/sre-agent/evaluate |
| **Auto-granted role on creation** | **The user who creates the agent automatically receives the SRE Agent Administrator role.** Whether a **service principal** used for IaC/CI-CD creation is likewise auto-granted Administrator was **not explicitly confirmed** in fetched docs — treat as **[verify]**, and explicitly assign the role to any automation identity as a safe default. | https://learn.microsoft.com/en-us/azure/sre-agent/user-roles |
| **Identity model** | Each agent gets an automatically-created **user-assigned managed identity (UAMI)** — confirmed as UAMI, not system-assigned. ARM schema's `AgentIdentity.initialSponsorGroupId` field is **required**, suggesting an Entra group "sponsors"/owns the identity lifecycle. | https://learn.microsoft.com/en-us/azure/sre-agent/permissions ; https://learn.microsoft.com/en-us/azure/templates/microsoft.app/agents |
| **Networking** | **VNet integration is GA** (as of Aug 26, 2026) — **not required**; default is **Unrestricted** (public internet egress). Three modes: Unrestricted / Limited (wildcard URL allow-list) / Azure VNet (full egress through a delegated subnet, your NSG/firewall/private DNS apply, reaches private-endpoint resources). Switchable at any time on a running agent; settings persist across mode changes; **when VNet is connected, the other mode cards are disabled** until you disconnect. | https://learn.microsoft.com/en-us/azure/sre-agent/network-integration ; https://learn.microsoft.com/en-us/azure/sre-agent/faq |
| **Known/preview limitations** | **Managed connectors** feature is explicitly labeled **"(preview)."** **Azure Connector Namespace** is in **public preview**, GA "estimated end of 2026." **Live Reports** is in **public preview**. The **control-plane and data-plane REST APIs** are explicitly flagged: *"Both the control plane and data plane APIs are currently in preview. Endpoint paths, request/response shapes may change."* ARM API version in active use for data-plane auth flows: **`2025-05-01-preview`**; the Bicep/ARM template schema reference lists a newer **`2026-01-01`** API version as the "Latest" — i.e., **two live API versions coexist**; confirm which one is GA vs. preview before building automation. | https://learn.microsoft.com/en-us/azure/sre-agent/api-reference ; https://learn.microsoft.com/en-us/azure/templates/microsoft.app/agents ; https://learn.microsoft.com/en-us/azure/sre-agent/managed-connectors |

---

## 5. Security & governance

- **Data handling / where data is processed**: Conversation history, prompts, responses, and resource analysis are **stored and processed in the single Azure region the agent is deployed to**, regardless of where the actual managed Azure resources live. **Inference** (the literal model call) for Anthropic or Azure OpenAI **may occur outside that region**; EU-data-boundary agents using **Azure OpenAI** keep inference inside the EU boundary. **Microsoft does not use customer data to train AI models**; data is used "only to provide its functionality and to improve and debug the service." Data is **isolated by tenant and Azure subscription boundaries**. — https://learn.microsoft.com/en-us/azure/sre-agent/data-privacy
- **Non-Microsoft model provider governance**: **Anthropic operates as a non-Microsoft provider managed by Microsoft**, "under Microsoft's oversight with contractual safeguards and technical and organizational measures." Microsoft **Product Terms** and the **Data Protection Addendum (DPA)** apply. See Microsoft's subprocessor list via the Service Trust Portal (aka.ms/subprocessor) and Data Access Management page (microsoft.com/trust-center/privacy/data-access). — same source
- **Entra (identity) auth**: Every agent gets an automatic **user-assigned managed identity**; it "authenticates and interacts with your Azure resources… without you needing to manage secrets or credentials." Control-plane (ARM) uses standard Azure auth (interactive login, service principal, managed identity); data-plane requires a **separate OAuth token scoped to audience `https://azuresre.dev`**. — https://learn.microsoft.com/en-us/azure/sre-agent/permissions ; https://learn.microsoft.com/en-us/azure/sre-agent/api-reference
- **Approval workflows / least-privilege guidance**: Three independent control layers must each be satisfied — **(1) User roles** (Azure IAM on the agent resource — who can chat/approve/configure), **(2) Run modes** (Review vs. Autonomous — whether the agent asks first), **(3) Agent permissions** (RBAC on managed resource groups, with OBO as a Reader-mode fallback). Microsoft's explicit guidance: start new agents at **Reader** permission level and use **Review** run mode for production; graduate to Privileged/Autonomous only for trusted, well-tested scenarios/non-prod. — https://learn.microsoft.com/en-us/azure/sre-agent/user-roles ; https://learn.microsoft.com/en-us/azure/sre-agent/run-modes ; https://learn.microsoft.com/en-us/azure/sre-agent/permissions
- **Audit**: Execution history is logged for HTTP triggers (timestamp, thread link, success/failure); scheduled-task and incident threads form a persistent, reviewable conversation record; Agent Hooks (PostToolUse) can be used specifically to **audit tool usage** and inject/record extra context around every tool call. Tool Access Policies provide a declarative allow/ask/deny rule-audit surface (global/custom-agent/thread scope). — https://learn.microsoft.com/en-us/azure/sre-agent/agent-hooks ; https://learn.microsoft.com/en-us/azure/sre-agent/tool-access-policies
- **Guardrails against unwanted production changes**: Review mode shows explicit **Approve/Deny** buttons specifically for **Azure infrastructure operations** (CLI/ARM writes); only **SRE Agent Administrators** can approve. **Tool access policies** let admins hard-**Deny** classes of actions globally (e.g., `bash(az * delete *)`), which **cannot be overridden** by lower-scoped Allow rules. **Agent hooks** add a second layer — a "Stop" hook can reject an agent's self-declared "done" state and force continued work; a "PostToolUse" hook can block a tool's result from being used. — https://learn.microsoft.com/en-us/azure/sre-agent/tool-access-policies ; https://learn.microsoft.com/en-us/azure/sre-agent/agent-hooks
- **Governed skill distribution**: Platform teams can publish approved skills to a **private GitHub repository via the Private Plugins Marketplace**; all agents in a tenant then install only from that governed, version-pinned catalog. — https://learn.microsoft.com/en-us/azure/sre-agent/overview
- **Network isolation**: VNet integration (GA Aug 2026) routes outbound traffic through a delegated subnet; customer NSG rules and private DNS apply; reaches private endpoints/internal APIs like any normal VNet-joined workload. Three selectable modes (Unrestricted/Limited/Azure VNet), switchable live. — https://learn.microsoft.com/en-us/azure/sre-agent/network-integration
- **Infrastructure as Code**: Agent + network config + identity + tool policies are all deployable via **Bicep/ARM/Terraform/Azure CLI/azd** through the same CI/CD pipelines as any other Azure resource — this is itself a governance control (version-controlled, reviewable configuration). — https://learn.microsoft.com/en-us/azure/sre-agent/overview ; https://learn.microsoft.com/en-us/azure/sre-agent/deploy-iac
- **Responsible AI**: No dedicated **SRE-Agent-specific Transparency Note** was located on Microsoft Learn in this research pass (Microsoft Foundry Agent Service has one; SRE Agent's RAI posture is implied via the data-privacy/non-Microsoft-provider-governance page rather than a standalone named document). **[verify — recommend checking learn.microsoft.com/azure/sre-agent for a Transparency Note before the session, and cross-reference Microsoft's general Responsible AI principles/Transparency Report at microsoft.com/en-us/corporate-responsibility/topics/responsible-ai/reports/transparency-report/]**

---

## 6. Deployment / automation

### ARM resource type & API versions
- **Resource type:** `Microsoft.App/agents` (confirms this sits under the Azure Container Apps resource provider, `Microsoft.App`, which must be **registered** on the subscription before agent creation). — https://learn.microsoft.com/en-us/azure/templates/microsoft.app/agents ; https://learn.microsoft.com/en-us/azure/sre-agent/faq
- **API versions seen in active use:**
  - **`2025-05-01-preview`** — used in the official API-reference doc's example data-plane `az rest` call to read `properties.agentEndpoint`; explicitly flagged as **preview**.
  - **`2026-01-01`** — listed as the **"Latest"** version on the Bicep/ARM/Terraform-AzAPI template reference page (alongside a `2026-01-01` change-log entry).
  - Both appear live/current in October 2026 documentation; **confirm with the customer's target subscription which version their tooling resolves to before a demo.** — https://learn.microsoft.com/en-us/azure/sre-agent/api-reference ; https://learn.microsoft.com/en-us/azure/templates/microsoft.app/agents

### Key Bicep/ARM properties (`Microsoft.App/agents`, `properties` object)
```bicep
resource symbolicname 'Microsoft.App/agents@2026-01-01' = {
  identity: {
    type: 'string'                       // e.g. UserAssigned
    userAssignedIdentities: { '{id}': {} }
  }
  location: 'string'
  name: 'string'                         // pattern ^[A-Za-z]([-A-Za-z0-9]{0,30}[A-Za-z0-9])$
  properties: {
    actionConfiguration: {
      accessLevel: 'High' | 'Low'
      identity: 'string'
      mode: 'Autonomous' | 'ReadOnly' | 'Review'
    }
    agentIdentity: {
      initialSponsorGroupId: 'string'    // required
    }
    agentSpaceId: 'string'
    defaultModel: {
      name: 'string'
      provider: 'string'                 // e.g. OpenAI / Anthropic
    }
    incidentManagementConfiguration: {
      connectionKey: 'string'
      connectionName: 'string'
      connectionUrl: 'string'
      oboUser: 'string'
      type: 'string'                     // AzureMonitor | PagerDuty | ServiceNow
    }
    knowledgeGraphConfiguration: {
      identity: 'string'
      managedResources: [ 'string' ]      // resource-group / resource IDs
    }
    logConfiguration: {
      applicationInsightsConfiguration: {
        appId: 'string'
        connectionString: 'string'
      }
    }
    upgradeChannel: 'Stable' | 'Preview'
  }
  tags: { '{key}': 'string' }
}
```
— https://learn.microsoft.com/en-us/azure/templates/microsoft.app/agents

### Data-plane API
- **Base URL pattern:** `https://{name}--{id}.{hash}.{region}.azuresre.ai` — returned at runtime in `properties.agentEndpoint` from a `GET` on the ARM control-plane resource. Example deploy output also shows a friendlier form like `https://my-agent.eastus2.azuresre.ai`.
- **Token audience:** **`https://azuresre.dev`** — **confirmed directly in official docs** (user's "believed to be" note is correct): *"The data plane requires a separate token with audience `https://azuresre.dev`."* Example: `az account get-access-token --resource https://azuresre.dev`.
- **Sample call:** `curl -H "Authorization: Bearer $TOKEN" "$ENDPOINT/api/v1/threads"`.
- — https://learn.microsoft.com/en-us/azure/sre-agent/api-reference

### RBAC for API callers (service principal to call data-plane API)
- The API reference doc lists **3 data-plane RBAC roles**: **SRE Agent Administrator**, **SRE Agent User**, **SRE Agent Reader** — assigned the same way as any Azure role (`az role assignment create --role "SRE Agent Administrator" --scope <agent-resource-id>`).
- **Does a service principal need an explicit role assignment, or is it auto-granted Administrator like a human creator?** The docs only state *"the **user** who creates the agent automatically receives the SRE Agent Administrator role"* — this is phrased around interactive user creation. **Whether an identity (service principal) that creates the agent via IaC/CI-CD automatically receives the same auto-grant was not explicitly confirmed — treat as [verify] and, as a safe default for automation, explicitly assign `SRE Agent Administrator` (or the minimum role needed) to the calling service principal/managed identity as part of the deployment pipeline.**
- — https://learn.microsoft.com/en-us/azure/sre-agent/user-roles ; https://learn.microsoft.com/en-us/azure/sre-agent/api-reference

### Official samples, labs, and IaC tooling
- **GitHub community hub:** https://github.com/microsoft/sre-agent — official resources hub: issues/feedback, curated docs/video links, and a **`labs/`** folder.
- **Hands-on lab** (`labs/` → `starter-lab`): deploy an SRE Agent connected to a sample app ("Grubify") with a **single `azd up`**; agent then autonomously diagnoses/remediates. Prereqs: Azure CLI 2.60+, Azure Developer CLI (azd) 1.9+, Git, Python 3.10+; requires **Owner** on the subscription (for RBAC assignments) and `az provider register -n Microsoft.App --wait`. Bicep-provisioned resources include the SRE Agent (`Microsoft.App/agents`), Container Apps (API + frontend), Log Analytics, Application Insights, metric/log alert rules, and the managed identity. Deployment time **~8–12 minutes**. — https://github.com/microsoft/sre-agent/tree/main/labs (note: lab repo itself is hosted separately at `github.com/dm-chelupati/sre-agent-lab`, referenced from the labs README)
- The user's expected path `labs/zava-aks-postgres` was **not found verbatim** in this research pass (the confirmed example lab folder is `starter-lab`, deploying a sample called "Grubify," not "Zava"/AKS/Postgres) — **[verify — the zava-aks-postgres lab may exist under a different path, in a different branch, or may have been renamed/retired; re-check the repo directly before referencing it in the deck]**.
- **IaC templates repo:** `sre-agent/sreagent-templates` provides **four deploy backends**: **Bicep, Terraform, PowerShell, Azure Developer CLI (azd)** — confirming **Terraform support exists** (via Terraform 1.5+ and presumably the AzAPI provider, consistent with the "Terraform AzAPI reference" naming on the ARM template page). Workflow: `./bin/new-agent.sh --recipe azmon-lawappinsights ...` generates config from a **prebuilt recipe** (Azure Monitor, PagerDuty, Dynatrace recipes confirmed; "Microsoft regularly adds new recipes"), then `./bin/deploy.sh my-agent/` deploys (**~3 minutes**). Day-2 tooling: `clone-agent.sh` (replicate an agent's config to a new name/RG — e.g., prod→staging), export/diff/verify tooling. Azure permissions needed: **Owner**, or **Contributor + User Access Administrator**. — https://learn.microsoft.com/en-us/azure/sre-agent/deploy-iac
- **Azure Connector Namespace sample**: `github.com/microsoft/sql-server-samples` → `samples/applications/azure-sql-mcp` deploys an Azure SQL MCP server via `azd up`, connectable to SRE Agent; supported Connector-Namespace regions at preview: **West Central US, Central US, East Asia, North Europe**. — https://devblogs.microsoft.com/azure-sdk/power-azure-sre-agent-with-connector-namespace/

### Logging / Application Insights integration
ARM `logConfiguration.applicationInsightsConfiguration` (`appId`, `connectionString`) lets the agent resource itself emit operational telemetry to a customer's own Application Insights instance — useful for monitoring the agent as a platform component, separate from the resources it investigates. — https://learn.microsoft.com/en-us/azure/templates/microsoft.app/agents

---

## 7. Benefits / value

### Microsoft's own internal usage (official, from developer.microsoft.com blog, Aug 2026)
> "Azure SRE Agent has scaled to over **3,000 internal Microsoft services**, processing more than **1.5 million incidents** with up to **50% resolved autonomously** without human intervention."
— https://developer.microsoft.com/blog/try-azure-sre-agent-with-no-always-on-charges/ (links through to techcommunity.microsoft.com/blog/appsonazureblog/a-paradigm-shift-in-cloud-operations-with-azure-sre-agent/4533244 for the full narrative — that page did not render full text via fetch in this pass, but the summary stat above is directly quoted from the official developer blog.)

### Customer-named outcomes (official)
- **InEight**: **80% reduction in incident investigation time** and **80% reduction in build-failure triage time**. — https://developer.microsoft.com/blog/try-azure-sre-agent-with-no-always-on-charges/
- **Zafin** and **Provation** are also named as customers seeing "similar impact" in the same official post (specific numbers for these two were not broken out in the excerpt fetched). — same source
- **Ecolab**: Microsoft customer-story page title *"Ecolab embraces agentic AI and streamlines root-cause analysis with [Azure SRE Agent]"* confirms this is an official Microsoft customer story, but the **full narrative/quantified stats (e.g., "30–40 daily alerts down to <10") came from a secondary AI-generated search summary, not a direct page fetch** (the official customer-story page returned only Microsoft's generic tagline on fetch in this pass) — **[verify the specific alert-volume and MTTR numbers directly at https://www.microsoft.com/en/customers/story/25633-ecolab-azure before quoting them to a customer]**.
- The oft-repeated **"40.5 hours → 3 minutes" MTTR** statistic appears in multiple secondary/analyst sources (e.g., beri.net) attributed loosely to "Microsoft's own internal environments," but **could not be traced to a specific, directly-fetched official Microsoft page in this research pass** — **[verify before using in a deck; prefer the confirmed "3,000 services / 1.5M incidents / 50% autonomous" stat set, which is officially sourced]**.

### Positioning vs. competitors
*(Caveat: the comparisons below are synthesized from independent analyst/blog content, not official Microsoft competitive materials — use directionally, verify specifics, and avoid presenting them as Microsoft's own claims.)*
- **PagerDuty AIOps / PagerDuty SRE Agent**: Positioned as strong at cross-tool incident **orchestration and communication**, with runbook-driven recommendations; remediation is typically **approval-gated** rather than fully autonomous; value scales with how deeply a customer has instrumented PagerDuty's event pipeline. — https://www.fundesk.io/ai-sre-agents-explained-platform-comparison-2026 (third-party)
- **Datadog Bits AI SRE**: GA since 2025 per third-party reporting; deeply integrated with Datadog's own telemetry (logs/metrics/traces/events/changes); supports a spectrum from diagnosis-only to fully autonomous repair with post-remediation health-check verification; most valuable to shops already standardized on Datadog. — same source
- **AWS "DevOps Agent"**: Third-party comparison claims strong CI/CD and auto-remediation coverage within AWS, usage-based pricing (~$0.0083/agent-second cited by one blog — **unverified, third-party**), and an emphasis on explainability via SageMaker Clarify; best for AWS-native shops. — https://iancloud.ai/blog/aws-devops-agent-vs-azure-sre-agent-2026-ga-hyperscaler-copilot-comparison-multi-cloud-byok-audit-trail-active-operational-layer (third-party, **unverified pricing figure**)
- **Google Gemini Cloud Assist**: Reported as GCP-centric, leaning on Gemini's grounding/explainability/content-safety stack; described as newer to agentic ops automation specifically vs. AWS/Azure. — third-party
- **Resolve.ai / Cleric**: Positioned by third parties as **cloud-neutral / multi-cloud-first** alternatives, potentially attractive to customers who explicitly don't want to anchor on one hyperscaler's agent; documentation of their safety/governance practices is reported as less mature than the hyperscaler offerings. — third-party
- **Azure SRE Agent's differentiated pitch** (synthesizing official capability docs above, not third-party spin): deepest **native, no-connector** access to the full Azure control plane + Resource Graph + Azure Monitor stack; **governed autonomy** via the Run-Modes/Permissions/Tool-Access-Policies/Agent-Hooks four-layer model; **first-class IaC** (Bicep/Terraform/azd) so the agent itself is managed like any other Azure resource; and a **persistent, self-authored knowledge graph + memory system** that compounds in value over time rather than resetting per-incident.

### Relationship to adjacent Microsoft AI products
- **GitHub Copilot coding agent**: SRE Agent is positioned as the "ops-side" investigator that hands qualifying fixes to **GitHub Copilot coding agent** for code-level remediation via PRs — see §2 "Code Access / GitHub" above. The two are complementary, not overlapping: SRE Agent diagnoses infra/ops issues across telemetry+resources; Copilot coding agent authors code changes.
- **Azure Copilot / Microsoft Foundry**: SRE Agent is built on the same `Microsoft.App/agents` platform family as other "prebuilt Azure agents" (the pricing docs explicitly describe AAUs as "used across all prebuilt Azure agents," implying a shared agent-hosting substrate alongside things like Foundry Agent Service). A dedicated page mapping SRE Agent's exact relationship to Microsoft Foundry / Azure Copilot branding was **not located** in this pass — **[verify positioning language the account team should use if a customer asks "is this a Foundry agent?"]**.

---

## 8. Objections & FAQ material for a seller

**"Will it change production without me knowing?"**
No by default. **Review mode is the default run mode** and shows explicit Approve/Deny for any Azure infrastructure write action; only an **SRE Agent Administrator** can approve. Even in Autonomous mode, actions are scoped by the **Permission level** (Reader vs. Privileged) granted to the managed identity, and can be further hard-blocked tenant-wide by **Tool Access Policies** (`Deny` rules, global scope only, cannot be overridden). — https://learn.microsoft.com/en-us/azure/sre-agent/run-modes ; https://learn.microsoft.com/en-us/azure/sre-agent/tool-access-policies

**"What stops it from hallucinating a fix and running it?"**
Responses are **grounded with clickable citations** back to the actual logs/metrics/past-incident source. **Agent Hooks** add a "Stop" checkpoint that can reject an incomplete/unjustified final answer and force the agent to keep investigating, and a "PostToolUse" checkpoint that can audit or block a tool's result before it's used. Destructive commands can be explicitly denied via glob-pattern Tool Access Policies (e.g., `bash(az * delete *)`). — https://learn.microsoft.com/en-us/azure/sre-agent/agent-hooks ; https://learn.microsoft.com/en-us/azure/sre-agent/memory

**"Is our data used to train Microsoft's or Anthropic's models?"**
No. **"Microsoft doesn't use your data to train AI models,"** and the data-privacy page states **Anthropic likewise doesn't** use it for training; data is used only to run/debug/improve the service and is **tenant/subscription-isolated**. — https://learn.microsoft.com/en-us/azure/sre-agent/data-privacy

**"Where does our data actually live, especially if we're in the EU?"**
All content/history is stored & processed in the **single Azure region** you pick at creation. For **EU/EFTA/UK customers, Azure OpenAI is the default provider** and keeps inference inside the **EU Data Boundary**; **Anthropic is available only as an explicit opt-in** and is **never** covered by the EU Data Boundary (prompts may be processed in the US) — the portal shows an explicit consent notice if you opt in. **Anthropic is unavailable entirely** in GCC/GCC High/DoD/sovereign clouds. — https://learn.microsoft.com/en-us/azure/sre-agent/data-privacy

**"Is the cost predictable, or can this run away on us?"**
Two-part model (fixed always-on + variable active-flow) is designed to be bounded: set a **monthly active-flow AAU allocation cap (500–1,000,000)** in Settings; hitting it **pauses chat/automation** (not always-on billing) until next month or a manual increase. Track spend live via **Agent consumption** dashboards (by thread type, by day, by individual thread) or Azure Cost Management. **Delete** (not just stop) is the only way to fully zero out charges. New customers get a **30-day trial with always-on waived** to pilot risk-free (consumption still applies). — https://learn.microsoft.com/en-us/azure/sre-agent/pricing-billing ; https://learn.microsoft.com/en-us/azure/sre-agent/evaluate

**"We're multi-cloud / have non-Azure telemetry — is this Azure-only?"**
No. Native **MCP connectors** reach **Datadog, Splunk, New Relic, Dynatrace, Elasticsearch, GitHub** today, plus the generic **MCP standard** lets you wire in effectively any system (databases, APIs, monitoring platforms). **HTTP triggers** let any webhook-capable external tool (CI/CD, Grafana, Jira, Datadog, Dynatrace) kick off an investigation. That said, the agent's **deepest, zero-setup capability is Azure-native** (ARM/Resource Graph/Monitor); non-Azure resources are reached via connectors/MCP rather than built-in tools — be transparent that Azure resources get first-class treatment and everything else is "excellent, connector-mediated" rather than equally native. — https://learn.microsoft.com/en-us/azure/sre-agent/mcp-connectors ; https://learn.microsoft.com/en-us/azure/sre-agent/http-triggers ; https://learn.microsoft.com/en-us/azure/sre-agent/connectors

**"What if we want to pilot without touching production at all?"**
Use **Reader permission level** (read-only RBAC; the agent prompts for temporary On-Behalf-Of elevation if it ever needs to act, and only an Administrator can grant that elevation) combined with **Review run mode** — per the FAQ: *"Can I try the agent without affecting production systems? Yes, use Azure SRE Agent in Reader mode."* — https://learn.microsoft.com/en-us/azure/sre-agent/faq ; https://learn.microsoft.com/en-us/azure/sre-agent/permissions

**"Do we need a service mesh / VNet overhaul to adopt this?"**
No. **VNet integration is optional** (GA since Aug 2026) and purely additive for customers who need egress control/private-endpoint reachability/audit trails. Default **Unrestricted mode already covers**: investigating publicly reachable resources, Azure CLI/kubectl against public endpoints, Log Analytics/App Insights (if public access enabled), GitHub/Jira/Slack-class SaaS connectors, scheduled tasks, response plans, and all MCP connectors. — https://learn.microsoft.com/en-us/azure/sre-agent/faq ; https://learn.microsoft.com/en-us/azure/sre-agent/network-integration

---

## Top 15 facts for slides

1. **GA since March 11, 2026** (public preview since Build, May 19, 2025) — a mature, ~10-month-GA product as of this session. (RSS 558321; RSS 494483)
2. **Pricing is 100% usage-transparent via Azure Agent Units (AAUs)**: a small fixed "always-on" fee (4 AAUs/agent-hour) + token-metered "active flow" — confirm live $/AAU on the Azure Pricing Calculator before quoting numbers. (learn.microsoft.com/.../pricing-billing)
3. **New customers get a 30-day trial with always-on charges waived**, up to 3 agents — zero-risk pilot. (learn.microsoft.com/.../evaluate)
4. **Microsoft runs this on itself at massive scale**: 3,000+ internal services, 1.5M+ incidents processed, up to 50% resolved with zero human touch. (developer.microsoft.com blog, Aug 2026)
5. **Customer-proven ROI**: InEight reports **80% reduction** in both incident-investigation time and build-failure triage time. (developer.microsoft.com blog, Aug 2026)
6. **Review mode is the safety-first default** — the agent always asks an Administrator to Approve/Deny before any Azure infrastructure write action; Autonomous mode is opt-in. (learn.microsoft.com/.../run-modes)
7. **Four-layer governance stack**: User Roles (who can act) → Run Modes (ask vs. act) → Agent Permissions/RBAC (what it can touch) → Tool Access Policies & Agent Hooks (hard deny-lists + audit/validation checkpoints). (learn.microsoft.com/.../user-roles, run-modes, permissions, tool-access-policies, agent-hooks)
8. **No training on your data** — by Microsoft or by Anthropic (for customers who opt into Claude models); data is tenant/subscription-isolated. (learn.microsoft.com/.../data-privacy)
9. **EU customers get Azure OpenAI as the EU-Data-Boundary-compliant default**; Anthropic/Claude is an explicit opt-in that's never EUDB-covered, and isn't offered at all in government/sovereign clouds. (learn.microsoft.com/.../data-privacy, model-provider-selection)
10. **Deep, zero-setup Azure coverage out of the box**: ARM/Resource Graph, Azure Monitor, Application Insights, Log Analytics, AKS kubectl diagnostics, Container Apps, App Service, Functions — no connector required, just RBAC. (learn.microsoft.com/.../tools, connectors)
11. **Native incident-platform integrations**: Azure Monitor (credential-free), PagerDuty, ServiceNow — alerts picked up within 1–2 minutes and auto-correlated across every connected data source. (learn.microsoft.com/.../incident-platforms, pagerduty-incidents, servicenow-incidents)
12. **Extensible by design**: Skills (auto-loaded procedures), Custom Agents/subagents (explicit `/agent` specialists with handoff chains), 80-tool-budget MCP connectors (Datadog/Splunk/New Relic/Dynatrace/Elasticsearch/GitHub natively), HTTP triggers for any webhook tool. (learn.microsoft.com/.../skills, sub-agents, mcp-connectors, http-triggers)
13. **It gets smarter over time, for free**: automatic post-incident learning (symptoms/fix/root cause/pitfalls) indexed into a persistent knowledge graph + `#remember`/`#retrieve` memory commands — no manual training pipeline. (learn.microsoft.com/.../memory)
14. **Everything is Infrastructure-as-Code**: deploy via Bicep, Terraform, PowerShell, or azd, with one-command recipes (`./bin/new-agent.sh --recipe azmon-lawappinsights`) and day-2 clone/export/diff tooling — the agent itself is a version-controlled Azure resource (`Microsoft.App/agents`). (learn.microsoft.com/.../deploy-iac; github.com/microsoft/sre-agent)
15. **Newest capability (Aug 2026): Live Reports** — describe a recurring dashboard once in chat, and it refreshes with live data on every open, at near-zero ongoing token cost (only model-assisted analysis consumes AAUs, plain data refresh doesn't). Also new: VNet integration GA and Azure Connector Namespace (managed MCP hosting) in preview. (learn.microsoft.com/.../live-reports, network-integration; devblogs.microsoft.com connector-namespace post)

---

## Sources

### Official Microsoft — Learn documentation (learn.microsoft.com/en-us/azure/sre-agent/)
- Overview: https://learn.microsoft.com/en-us/azure/sre-agent/overview
- General FAQ: https://learn.microsoft.com/en-us/azure/sre-agent/faq
- Pricing and billing: https://learn.microsoft.com/en-us/azure/sre-agent/pricing-billing
- Evaluate (30-day trial): https://learn.microsoft.com/en-us/azure/sre-agent/evaluate
- Run modes: https://learn.microsoft.com/en-us/azure/sre-agent/run-modes
- Agent permissions: https://learn.microsoft.com/en-us/azure/sre-agent/permissions
- User roles and permissions (RBAC): https://learn.microsoft.com/en-us/azure/sre-agent/user-roles
- Custom agents (sub-agents / subagent builder): https://learn.microsoft.com/en-us/azure/sre-agent/sub-agents
- Skills: https://learn.microsoft.com/en-us/azure/sre-agent/skills
- Memory and knowledge: https://learn.microsoft.com/en-us/azure/sre-agent/memory
- Connectors (overview): https://learn.microsoft.com/en-us/azure/sre-agent/connectors
- MCP connectors and tools: https://learn.microsoft.com/en-us/azure/sre-agent/mcp-connectors
- Managed connectors (preview): https://learn.microsoft.com/en-us/azure/sre-agent/managed-connectors
- GitHub connector: https://learn.microsoft.com/en-us/azure/sre-agent/github-connector
- Incident platforms: https://learn.microsoft.com/en-us/azure/sre-agent/incident-platforms
- Azure Monitor alerts: https://learn.microsoft.com/en-us/azure/sre-agent/azure-monitor-alerts
- PagerDuty incident indexing: https://learn.microsoft.com/en-us/azure/sre-agent/pagerduty-incidents
- ServiceNow incident indexing: https://learn.microsoft.com/en-us/azure/sre-agent/servicenow-incidents
- Incident response plans: https://learn.microsoft.com/en-us/azure/sre-agent/incident-response-plans
- Scheduled tasks: https://learn.microsoft.com/en-us/azure/sre-agent/scheduled-tasks
- HTTP triggers: https://learn.microsoft.com/en-us/azure/sre-agent/http-triggers
- Tools: https://learn.microsoft.com/en-us/azure/sre-agent/tools
- Agent hooks: https://learn.microsoft.com/en-us/azure/sre-agent/agent-hooks
- Tool access policies: https://learn.microsoft.com/en-us/azure/sre-agent/tool-access-policies
- Network integration (VNet): https://learn.microsoft.com/en-us/azure/sre-agent/network-integration
- Data residency and privacy: https://learn.microsoft.com/en-us/azure/sre-agent/data-privacy
- Model provider selection: https://learn.microsoft.com/en-us/azure/sre-agent/model-provider-selection
- Supported regions: https://learn.microsoft.com/en-us/azure/sre-agent/supported-regions
- API reference (control/data plane, RBAC, auth): https://learn.microsoft.com/en-us/azure/sre-agent/api-reference
- Deploy with infrastructure as code: https://learn.microsoft.com/en-us/azure/sre-agent/deploy-iac
- Live Reports (preview): https://learn.microsoft.com/en-us/azure/sre-agent/live-reports
- Diagnose with Azure observability: https://learn.microsoft.com/en-us/azure/sre-agent/diagnose-azure-observability

### Official Microsoft — ARM/Bicep/Terraform schema reference
- Microsoft.App/agents — Bicep, ARM template & Terraform AzAPI reference: https://learn.microsoft.com/en-us/azure/templates/microsoft.app/agents

### Official Microsoft — Azure Updates / release communications (authoritative dates)
- [In preview] Public Preview: Introducing Azure SRE Agent (pubDate 2025-05-19): https://www.microsoft.com/releasecommunications/api/v2/azure/rss/494483
- [Launched] Generally Available: Azure SRE Agent with new capabilities (pubDate 2026-03-11): https://www.microsoft.com/releasecommunications/api/v2/azure/rss/558321
- [Launched] Generally Available: Azure SRE Agent 30-Day Trial (pubDate 2026-08-26): https://www.microsoft.com/releasecommunications/api/v2/azure/rss/569760

### Official Microsoft — blogs and product/marketing pages
- Try Azure SRE Agent with no always-on charges (developer.microsoft.com, Aug 2026 — confirmed internal-usage stats & InEight/Zafin/Provation): https://developer.microsoft.com/blog/try-azure-sre-agent-with-no-always-on-charges/
- Power Azure SRE Agent with Connector Namespace (devblogs.microsoft.com/azure-sdk): https://devblogs.microsoft.com/azure-sdk/power-azure-sre-agent-with-connector-namespace/
- A paradigm shift in cloud operations with Azure SRE Agent (techcommunity.microsoft.com — linked from the official trial blog; full content not fully retrievable via fetch in this pass): https://techcommunity.microsoft.com/blog/appsonazureblog/a-paradigm-shift-in-cloud-operations-with-azure-sre-agent/4533244
- Azure SRE Agent product page: https://azure.microsoft.com/en-us/products/sre-agent/
- Azure SRE Agent pricing page (confirm live numbers here before the session): https://azure.microsoft.com/en-us/pricing/details/sre-agent/
- Ecolab customer story (verify specific stats directly): https://www.microsoft.com/en/customers/story/25633-ecolab-azure

### Official Microsoft — GitHub
- Community hub, videos, and hands-on labs: https://github.com/microsoft/sre-agent (see `/labs` folder; GA-launch and Build-session videos linked from the README)
- Azure Connector Namespace Azure SQL MCP sample: https://github.com/microsoft/sql-server-samples/tree/main/samples/applications/azure-sql-mcp

### Third-party / secondary sources used only for context, flagged [verify] in-text where relied upon
- azurelook.com (Azure-update aggregator — GA and preview-expansion summaries): https://azurelook.com/azure-update/announcing-general-availability-for-the-azure-sre-agent/ ; https://azurelook.com/azure-update/expanding-the-public-preview-of-the-azure-sre-agent/
- beri.net (MTTR "40.5 hours → 3 minutes" claim — unverified against an official page): https://www.beri.net/article/ai-sre-agents-35000-incidents-autonomous-operations-on-call-burnout-enterprise-2026
- Competitive comparisons (AWS DevOps Agent, Gemini Cloud Assist, Resolve.ai, Cleric pricing/positioning — all unverified, analyst opinion): https://www.fundesk.io/ai-sre-agents-explained-platform-comparison-2026 ; https://iancloud.ai/blog/aws-devops-agent-vs-azure-sre-agent-2026-ga-hyperscaler-copilot-comparison-multi-cloud-byok-audit-trail-active-operational-layer
- GitHub Copilot coding-agent hand-off pattern (community workshop / blog, not an official productized feature page): https://stochasticcoder.com/2026/04/29/beyond-the-alert-building-self-healing-pipelines-with-azure-sre-agent-and-github-copilot/ ; https://developer.microsoft.com/en-us/reactor/events/27562/
- Microsoft Build 2026 conference dates (conflicting secondary reports): https://windowsreport.com/microsoft-shares-the-dates-for-its-build-2026-developer-conference/

### Open items flagged [verify] before the customer session
1. Exact live **$/AAU** and any regional price variance — pull from the Azure Pricing Calculator (azure.microsoft.com/en-us/pricing/details/sre-agent/) at demo prep time; the $0.10/AAU figure circulating in secondary sources was not independently confirmed on an official page in this pass.
2. Exact date of the **Ignite 2025 preview-expansion** announcement (narrowed to the Oct/Nov 2025 window but not pinned to a specific official RSS item in this pass).
3. Whether a **service principal** that creates an agent via IaC is auto-granted `SRE Agent Administrator` the same way an interactive human creator is.
4. Whether `labs/zava-aks-postgres` exists in the microsoft/sre-agent repo (only `labs/starter-lab`, deploying a sample called "Grubify," was confirmed).
5. The precise **"40.5 hours → 3 minutes"** MTTR statistic and the detailed **Ecolab** alert-volume numbers — re-confirm against the official customer-story page before quoting.
6. Whether **Grafana** and **Jira** are native MCP connectors or webhook/HTTP-trigger-only integrations.
7. Any explicit, numeric **"max concurrent incidents"** or **"max concurrent chat threads"** limit (none found published as of this research).
8. A dedicated **Responsible AI Transparency Note** specific to Azure SRE Agent (not located; general Microsoft RAI principles apply by reference).
