---
marp: true
size: 16:9
paginate: true
title: Azure SRE Agent customer session
style: |
  section{font-family:"Aptos","Segoe UI",Arial,sans-serif;background:linear-gradient(135deg,#F7FAFF,#fff 62%,#EAF4FF);color:#172033;padding:48px 64px}section::after{color:#6A7A90;font-size:16px}h1{color:#002050;font-size:40px;line-height:1.05;margin:0 0 18px}h2,h3{color:#0078D4}p,li{font-size:19px;line-height:1.28}.lead{font-size:29px;line-height:1.17}.small,.small li,.small p{font-size:14.5px}.xsmall,.xsmall li,.xsmall p{font-size:12px}.grid2{display:grid;grid-template-columns:1fr 1fr;gap:22px}.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.card{background:#fff;border:1px solid #C7D7EA;border-radius:18px;padding:16px 18px;box-shadow:0 10px 22px rgba(0,32,80,.08)}.card p,.card li{font-size:16.5px}.stat{font-size:52px;font-weight:800;color:#0078D4;line-height:.95}.badge{display:inline-block;border-radius:999px;padding:6px 12px;background:#E6F2FB;color:#004578;font-weight:700;font-size:15px}.source{position:absolute;left:64px;right:64px;bottom:24px;color:#5F6B7A;font-size:11px;line-height:1.15}section.title,section.divider,section.closing{color:white;background:radial-gradient(circle at 82% 10%,#50E6FF 0,rgba(80,230,255,.12) 30%,transparent 45%),linear-gradient(135deg,#002050,#004578 45%,#0078D4)}section.title h1,section.divider h1,section.closing h1{color:white;font-size:56px}section.title p,section.divider p,section.closing p{color:#EAF4FF}section.title .card p,section.title .card li,section.divider .card p,section.divider .card li,section.closing .card p,section.closing .card li{color:#172033}table{width:100%;border-collapse:collapse;font-size:13.5px}th{background:#E6F2FB;color:#002050}th,td{border:1px solid #C7D7EA;padding:6px 8px;vertical-align:top}pre{background:#091E42;color:#EAF4FF;border-radius:14px;padding:13px 15px;font-size:14px}code{background:#EEF4FB;border-radius:5px;padding:1px 4px;font-size:.85em}pre code{background:transparent;color:#EAF4FF}.diagram{display:block;margin:8px auto 0;max-width:100%;max-height:455px}.timeline{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}.step{background:#fff;border-top:8px solid #0078D4;border-radius:16px;padding:14px;box-shadow:0 8px 18px rgba(0,32,80,.08)}.step p{font-size:15px}.quote{font-size:27px;line-height:1.18;color:#002050;font-weight:650}.metric{border-left:8px solid #0078D4}
---

<!-- _class: title -->

# Azure SRE Agent

<p class="lead">A 90-minute customer / partner session on agentic operations, governed autonomy, and the Contoso Trek demo.</p><span class="badge">Azure Container Apps</span> <span class="badge">Azure Monitor</span> <span class="badge">GitHub</span> <span class="badge">SRE Agent</span>

<!-- Presenter notes: Open with outcomes: faster triage, less toil, and safer automation. Say numbers are cited or marked for verification. -->

---

# 90-minute flow

<table><tr><th>Time</th><th>Segment</th><th>Outcome</th></tr><tr><td>0–10</td><td>Opening and on-call problem</td><td>Shared urgency</td></tr><tr><td>10–30</td><td>What it is + architecture</td><td>Operating model</td></tr><tr><td>30–50</td><td>Governance, benefits, pricing, limits</td><td>Adoption confidence</td></tr><tr><td>50–80</td><td>Live demos 1–4</td><td>Evidence in action</td></tr><tr><td>80–90</td><td>FAQ and CTA</td><td>Agree next steps</td></tr></table>

<!-- Presenter notes: Keep the first half crisp so demos start on time. -->

---

<!-- _class: divider -->

# The on-call problem

<p class="lead">Too much signal, too little context, and too many late-night decisions made under pressure.</p>

<!-- Presenter notes: Transition from pain to need. -->

---

# Why incidents still take too long

<div class="grid2"><div class="card"><h3>Context switching</h3><p>Telemetry, resource state, code, work items, runbooks, and chat history live in different tools.</p></div><div class="card"><h3>Manual correlation</h3><p>Engineers reconstruct topology, recent changes, and prior fixes while the incident clock runs.</p></div><div class="card"><h3>Approval anxiety</h3><p>Teams want automation, but not unbounded production changes.</p></div><div class="card"><h3>Knowledge loss</h3><p>Lessons from one incident rarely become searchable guidance for the next one.</p></div></div>

<!-- Presenter notes: Ask which pain hurts most. -->

---

<!-- _class: divider -->

# What Azure SRE Agent is

<p class="lead">A Microsoft-managed agentic AI service for cloud operations, incident response, and reliability workflows.</p>

<!-- Presenter notes: Definition slide. -->

---

# Product in one sentence

<p class="lead">Azure SRE Agent connects to Azure resources, observability tools, incident platforms, and source-code repos so teams investigate and respond from one grounded workspace.</p><div class="grid3"><div class="card"><h3>Automate incidents</h3><p>Alert → query → correlate → root cause → mitigation proposal or action.</p></div><div class="card"><h3>Automate workflows</h3><p>Scheduled tasks run proactive checks and compliance sweeps.</p></div><div class="card"><h3>Investigate & advise</h3><p>Natural-language Q&A with connected evidence and citations.</p></div></div><p class="source">Source: <a href="https://learn.microsoft.com/en-us/azure/sre-agent/overview">Azure SRE Agent overview</a>.</p>

<!-- Presenter notes: Use the three official usage patterns. -->

---

# Timeline and maturity

<div class="timeline"><div class="step"><h3>May 2025</h3><p>Public preview announced at Microsoft Build.</p></div><div class="step"><h3>Mar 2026</h3><p>General availability with new capabilities.</p></div><div class="step"><h3>Mid 2026</h3><p>Azure Connector Namespace public preview.</p></div><div class="step"><h3>Aug 2026</h3><p>30-day trial GA, VNet GA, Live Reports preview.</p></div></div><p class="source">Sources: <a href="https://www.microsoft.com/releasecommunications/api/v2/azure/rss/494483">Preview</a>; <a href="https://www.microsoft.com/releasecommunications/api/v2/azure/rss/558321">GA</a>; <a href="https://www.microsoft.com/releasecommunications/api/v2/azure/rss/569760">Aug update</a>; <a href="https://devblogs.microsoft.com/azure-sdk/power-azure-sre-agent-with-connector-namespace/">Connector Namespace</a>.</p>

<!-- Presenter notes: Avoid unverified Ignite date details. -->

---

# Newest capabilities to know

<div class="grid2"><div class="card"><h3>Live Reports (preview)</h3><p>Saved, reusable, auto-refreshing operational dashboards created from chat.</p></div><div class="card"><h3>VNet integration (GA)</h3><p>Route outbound traffic through customer VNet, NSG, DNS, and firewall.</p></div><div class="card"><h3>30-day trial (GA)</h3><p>Always-on charges waived for new customers, up to three agents; consumption still applies.</p></div><div class="card"><h3>Connector Namespace (preview)</h3><p>Managed MCP server hosting; early catalog includes Azure SQL, Cosmos DB, GitLab, Jira, PagerDuty.</p></div></div><p class="source">Sources: <a href="https://learn.microsoft.com/en-us/azure/sre-agent/live-reports">Live Reports</a>; <a href="https://learn.microsoft.com/en-us/azure/sre-agent/network-integration">VNet</a>; <a href="https://learn.microsoft.com/en-us/azure/sre-agent/evaluate">Trial</a>; <a href="https://devblogs.microsoft.com/azure-sdk/power-azure-sre-agent-with-connector-namespace/">Connector Namespace</a>.</p>

<!-- Presenter notes: Customers may have seen older preview material. -->

---

<!-- _class: divider -->

# Architecture and how it works

<p class="lead">Signals enter; context is gathered; governed agents act or advise; memory improves the next run.</p>

<!-- Presenter notes: Set up the visual architecture. -->

---

# Operating model

![h:410 class:diagram](diagrams/sre-agent-architecture.svg)

<!-- Presenter notes: Walk left to right from signal to governed outcome. -->

---

# Incident response loop

![w:1000 class:diagram](diagrams/incident-loop.svg)

<!-- Presenter notes: Use this to explain the two demos. -->

---

# Incident platforms and response plans

<div class="grid2"><div class="card"><h3>Platforms</h3><p>Azure Monitor, PagerDuty, and ServiceNow. Only one active incident platform at a time.</p></div><div class="card"><h3>Azure Monitor details</h3><p>Scanner checks every 1 minute, up to 250 alerts per API call, status sync every 5 minutes, merge lookback 7 days.</p></div></div><p class="source">Sources: <a href="https://learn.microsoft.com/en-us/azure/sre-agent/incident-platforms">Incident platforms</a>; <a href="https://learn.microsoft.com/en-us/azure/sre-agent/azure-monitor-alerts">Azure Monitor alerts</a>; <a href="https://learn.microsoft.com/en-us/azure/sre-agent/incident-response-plans">Response plans</a>.</p>

<!-- Presenter notes: Response plans route by filters to custom agents and run modes. -->

---

# Memory and knowledge

<div class="grid3"><div class="card"><h3>Past incidents</h3><p>Automatic learning captures symptoms, working steps, root cause, and pitfalls.</p></div><div class="card"><h3>User memories</h3><p>Commands #remember, #retrieve, and #forget store explicit facts.</p></div><div class="card"><h3>Knowledge base</h3><p>Uploaded runbooks and docs become searchable, cited operational context.</p></div></div><p class="source">Source: <a href="https://learn.microsoft.com/en-us/azure/sre-agent/memory">Memory and knowledge</a>.</p>

<!-- Presenter notes: Tie this to uploaded runbooks. -->

---

# Skills, custom agents, response plans

<div class="grid3"><div class="card"><h3>Skills</h3><p>Reusable procedures with optional tools and files; auto-loaded when relevant.</p></div><div class="card"><h3>Custom agents</h3><p>Specialists with prompts, tools, connectors, and skills.</p></div><div class="card"><h3>Response plans</h3><p>Route matching incidents to the right specialist and autonomy level.</p></div></div><p class="source">Sources: <a href="https://learn.microsoft.com/en-us/azure/sre-agent/overview">Overview</a>; <a href="https://learn.microsoft.com/en-us/azure/sre-agent/incident-response-plans">Response plans</a>.</p>

<!-- Presenter notes: Introduce code-investigator and platform-operator. -->

---

# Connectors, triggers, collaboration

<div class="grid2 small"><div class="card"><h3>MCP connectors</h3><p>Datadog, Splunk, New Relic, Dynatrace, Elasticsearch, GitHub; 80-tool budget; 60-second heartbeat.</p></div><div class="card"><h3>HTTP triggers</h3><p>Webhook endpoints for CI/CD and external monitoring systems.</p></div><div class="card"><h3>Scheduled tasks</h3><p>Recurring natural-language investigations that create full threads.</p></div><div class="card"><h3>Teams / Outlook</h3><p>Post updates to Teams or send summaries by email; managed connectors add preview governance.</p></div></div><p class="source">Sources: <a href="https://learn.microsoft.com/en-us/azure/sre-agent/mcp-connectors">MCP</a>; <a href="https://learn.microsoft.com/en-us/azure/sre-agent/http-triggers">HTTP triggers</a>; <a href="https://learn.microsoft.com/en-us/azure/sre-agent/scheduled-tasks">Scheduled tasks</a>.</p>

<!-- Presenter notes: Azure is native; external systems are connector mediated. -->

---

# Code Access and developer workflow

<div class="grid2">
<div class="card"><h3>Code Access</h3><p>Configured by PAT with <code>PUT /api/v2/repos/{name}</code> so the agent can search code and read files by path/branch.</p></div>
<div class="card"><h3>GitHub MCP connector</h3><p>Agent connector type <code>Mcp</code> at <code>https://api.githubcopilot.com/mcp/</code>; selected tools are exposed as <code>github_*</code>.</p></div>
<div class="card"><h3>Selected tools</h3><p><code>issue_write</code>, <code>issue_read</code>, <code>search_issues</code>, <code>add_issue_comment</code>, <code>search_code</code>, commits, file reads, and <code>assign_copilot_to_issue</code>.</p></div>
<div class="card"><h3>Developer hand-off</h3><p>The code investigator de-duplicates, files the issue with file:line, then assigns GitHub Copilot coding agent for a draft PR.</p></div>
</div>
<p class="source">Source: live demo configuration and <a href="https://learn.microsoft.com/en-us/azure/sre-agent/github-connector">GitHub connector docs</a>.</p>

<!-- Presenter notes: Update this from the live deployment: the demo uses Code Access plus GitHub MCP, not a generic GitHub connector-only story. -->

---

# From incident to pull request

<div class="grid3">
<div class="card"><h3>1. SRE Agent</h3><p>Correlates alert, telemetry, stack trace, source, and prior knowledge.</p></div>
<div class="card"><h3>2. GitHub issue</h3><p>Searches existing issues, avoids duplicates, and writes impact + stack + file:line.</p></div>
<div class="card"><h3>3. Copilot coding agent</h3><p><code>github_assign_copilot_to_issue</code> opens a draft PR for human review.</p></div>
</div>
<div class="card" style="margin-top:18px"><strong>Human control point:</strong> the PR is reviewed and merged by the team; SRE Agent observes post-deploy signals to verify recovery.</div>

<!-- Presenter notes: Make the hand-off concrete: incident response creates a developer-ready issue and Copilot coding agent drafts, but humans review the PR. -->

---

<!-- _class: divider -->

# Governance and security

<p class="lead">Autonomy is useful only when the blast radius is explicit and auditable.</p>

<!-- Presenter notes: Confidence section. -->

---

# Governance stack

![h:390 class:diagram](diagrams/governance-stack.svg)

<!-- Presenter notes: Four independent gates must align. -->

---

# Roles and separation of duties

<table><tr><th>Role</th><th>Best-fit responsibility</th></tr><tr><td>SRE Agent Reader</td><td>View threads, logs, and incidents.</td></tr><tr><td>SRE Agent Standard User</td><td>Chat, run diagnostics, request actions, scheduled tasks, knowledge uploads.</td></tr><tr><td>SRE Agent Author</td><td>Create custom agents and response plans; configure incident management.</td></tr><tr><td>SRE Agent Administrator</td><td>Approve actions, manage connectors, delete resources, full control.</td></tr></table><p class="source">Source: <a href="https://learn.microsoft.com/en-us/azure/sre-agent/user-roles">User roles</a>.</p>

<!-- Presenter notes: Map roles to personas. -->

---

# Run modes and RBAC are different

<div class="grid2"><div class="card"><h3>Run mode</h3><p>Review is default; Administrator approves/denies Azure infrastructure writes. Autonomous executes immediately within permissions.</p></div><div class="card"><h3>Permission level</h3><p>Reader grants read diagnostics and OBO fallback; Privileged grants resource-type contributor roles on selected resource groups.</p></div></div><p class="source">Sources: <a href="https://learn.microsoft.com/en-us/azure/sre-agent/run-modes">Run modes</a>; <a href="https://learn.microsoft.com/en-us/azure/sre-agent/permissions">Permissions</a>.</p>

<!-- Presenter notes: The agent needs both workflow and resource access. -->

---

# Data, network, audit posture

<div class="grid3"><div class="card"><h3>Data use</h3><p>Microsoft does not use customer data to train AI models; data is tenant/subscription isolated.</p></div><div class="card"><h3>Residency</h3><p>Conversation/content data is stored and processed in the selected Azure region.</p></div><div class="card"><h3>Network</h3><p>VNet integration is GA and optional: Unrestricted, Limited, or Azure VNet.</p></div></div><p class="source">Sources: <a href="https://learn.microsoft.com/en-us/azure/sre-agent/data-privacy">Data privacy</a>; <a href="https://learn.microsoft.com/en-us/azure/sre-agent/network-integration">Network integration</a>.</p>

<!-- Presenter notes: If EU comes up, explain provider choices. -->

---

<!-- _class: divider -->

# Benefits

<p class="lead">Faster investigation, lower toil, safer repeatability — with cited Microsoft and customer proof points.</p>

<!-- Presenter notes: Move to value. -->

---

# Quantified proof points

<div class="grid3"><div class="card metric"><div class="stat">3,000+</div><p>Internal Microsoft services scaled on Azure SRE Agent.</p></div><div class="card metric"><div class="stat">1.5M+</div><p>Incidents processed internally at Microsoft.</p></div><div class="card metric"><div class="stat">50%</div><p>Up to half resolved autonomously in Microsoft internal usage.</p></div></div><div class="card" style="margin-top:16px"><strong>Customer signal:</strong> InEight reported 80% reduction in incident investigation time and 80% reduction in build-failure triage time.</div><p class="source">Source: <a href="https://developer.microsoft.com/blog/try-azure-sre-agent-with-no-always-on-charges/">Microsoft Developer blog, Aug 2026</a>.</p>

<!-- Presenter notes: Use official stats only. -->

---

<!-- _class: divider -->

# Pricing and cost controls

<p class="lead">AAUs make agent cost visible: fixed always-on plus variable active-flow consumption.</p>

<!-- Presenter notes: Signal that AAU unit prices are now verified and region-specific. -->

---

# Pricing model

<div class="grid2">
<div class="card"><h3>Always-on flow</h3><p><strong>4 AAUs per agent-hour</strong> from creation until deletion. Stopping pauses active flow, not always-on billing.</p></div>
<div class="card"><h3>Verified AAU unit price</h3><p>Retail Prices API, queried 2026-10-03: East US / East US 2 <strong>$0.10</strong>; France Central / Sweden Central <strong>$0.11</strong>; West Europe <strong>$0.14</strong> effective 2026-10-01; France Central <strong>EUR 0.10</strong>.</p></div>
</div>
<div class="card"><strong>Quote discipline:</strong> prices vary by region and currency; confirm current values in the Azure pricing calculator for customer quotes.</div>
<p class="source">Sources: <a href="https://learn.microsoft.com/en-us/azure/sre-agent/pricing-billing">Pricing and billing</a>; <a href="https://prices.azure.com/api/retail/prices?$filter=meterName%20eq%20%27SRE%20Agent%20Unit%27">Azure Retail Prices API</a> queried 2026-10-03.</p>

<!-- Presenter notes: State the now-verified Retail Prices API values, but keep quote discipline because pricing can vary by region and currency. -->

---

# Active-flow AAU rates per 1M tokens

<table><tr><th>Model</th><th>Input</th><th>Output</th><th>Cache read</th><th>Cache write</th></tr><tr><td>Claude Opus 4.6</td><td>100</td><td>500</td><td>10</td><td>125</td></tr><tr><td>GPT 5.3 Codex</td><td>35</td><td>280</td><td>3.5</td><td>0</td></tr><tr><td>GPT 5.2</td><td>35</td><td>280</td><td>3.5</td><td>0</td></tr></table><p class="small"><strong>Official examples:</strong> quick question ≈ 3.8 AAUs (Claude) / 1.3 (GPT 5.3 Codex); incident investigation ≈ 35.3 / 11.7; full remediation ≈ 86.5 / 30.1.</p><p class="source">Source: <a href="https://learn.microsoft.com/en-us/azure/sre-agent/pricing-billing">Pricing and billing</a>.</p>

<!-- Presenter notes: Explain cache reads are cheaper. -->

---

# Worked monthly estimate

<div class="grid2 small">
<div class="card"><h3>Always-on floor</h3><p>4 AAU × 730 h = <strong>2,920 AAU/month</strong> ≈ <strong>$292</strong> in East US or <strong>$321</strong> in France Central.</p></div>
<div class="card"><h3>20 investigations/month</h3><p>GPT-5.3 Codex example: 11.7 × 20 ≈ <strong>234 AAU</strong> ≈ <strong>$23</strong> East US / <strong>$26</strong> France Central.</p></div>
<div class="card"><h3>Claude investigation mix</h3><p>Claude Opus example: 35.3 × 20 ≈ <strong>706 AAU</strong> ≈ <strong>$71</strong> East US / <strong>$78</strong> France Central.</p></div>
<div class="card"><h3>Small-team monthly shape</h3><p>1 agent + 20 GPT investigations + 10 GPT remediations + 100 quick questions ≈ <strong>3,585 AAU</strong> ≈ <strong>$359</strong> East US / <strong>$394</strong> France Central.</p></div>
</div>
<div class="card"><strong>Hours comparison:</strong> break-even hours = monthly agent cost ÷ your loaded on-call engineering cost/hour. At an illustrative $100/hour, the small-team East US shape breaks even at about 3.6 saved hours/month.</div>
<p class="source">Sources: <a href="https://learn.microsoft.com/en-us/azure/sre-agent/pricing-billing">Pricing and billing</a>; <a href="https://prices.azure.com/api/retail/prices?$filter=meterName%20eq%20%27SRE%20Agent%20Unit%27">Azure Retail Prices API</a> queried 2026-10-03.</p>

<!-- Presenter notes: Show how AAUs translate into dollars and compare to on-call hours using the customer’s actual loaded labor rate. -->

---

# Budget cap and trial

<div class="grid2"><div class="card"><h3>Monthly active-flow limit</h3><p>Configurable 500 to 1,000,000 AAUs. Hitting it pauses chat/actions; always-on billing continues.</p></div><div class="card"><h3>30-day trial</h3><p>Always-on charges waived for up to 3 new agents. Active-flow charges still apply; deleted agents still count.</p></div></div><p class="source">Sources: <a href="https://learn.microsoft.com/en-us/azure/sre-agent/pricing-billing">Pricing and billing</a>; <a href="https://learn.microsoft.com/en-us/azure/sre-agent/evaluate">Evaluate</a>.</p>

<!-- Presenter notes: Deletion is the only full stop. -->

---

<!-- _class: divider -->

# Limits and quotas

<p class="lead">Adoption planning needs the sharp edges on the table early.</p>

<!-- Presenter notes: Limits are design inputs. -->

---

# Selected published limits

<table><tr><th>Area</th><th>Limit / fact</th></tr><tr><td>Regions</td><td>22 confirmed supported Azure regions; one deployment region; cannot change after creation.</td></tr><tr><td>MCP tools</td><td>80 tools per agent; 60-second health heartbeat; new tools detected within 5 minutes.</td></tr><tr><td>Knowledge</td><td>.md/.txt only; max 50 MB per file; up to 1,000 files per custom agent instance.</td></tr><tr><td>GitHub OAuth</td><td>10 OAuth tokens per agent.</td></tr><tr><td>Incidents</td><td>One active incident platform per agent.</td></tr></table><p class="source">Sources: <a href="https://learn.microsoft.com/en-us/azure/sre-agent/supported-regions">Regions</a>; <a href="https://learn.microsoft.com/en-us/azure/sre-agent/mcp-connectors">MCP</a>; <a href="https://learn.microsoft.com/en-us/azure/sre-agent/github-connector">GitHub</a>; <a href="https://learn.microsoft.com/en-us/azure/sre-agent/incident-platforms">Incident platforms</a>.</p>

<!-- Presenter notes: No public concurrent incident/chat cap found. -->

---

# Preview / verify items

<ul>
<li><strong>Preview:</strong> Managed connectors, Connector Namespace, Live Reports, and control/data-plane REST APIs have preview caveats in current docs.</li>
<li><strong>Verify before automation:</strong> exact API version, service-principal auto-admin behavior, and concurrent-thread quotas.</li>
<li><strong>Quote discipline:</strong> AAU prices are verified for the listed regions, but prices vary by region/currency; confirm current values in the calculator for customer quotes.</li>
</ul>
<p class="source">Sources: <a href="https://learn.microsoft.com/en-us/azure/sre-agent/api-reference">API reference</a>; <a href="https://prices.azure.com/api/retail/prices?$filter=meterName%20eq%20%27SRE%20Agent%20Unit%27">Azure Retail Prices API</a>.</p>

<!-- Presenter notes: Remove the old unresolved price verification item and keep quote discipline plus remaining technical verify items. -->

---

<!-- _class: divider -->

# Live demo runway

<p class="lead">Contoso Trek: an outdoor-gear storefront on Azure Container Apps with Azure SRE Agent as operator.</p>

<!-- Presenter notes: Switch to demo mode. -->

---

<!-- _class: divider -->

# Demo 1 — deploy from GitHub Actions

<p class="lead">Show the deployment story: source, workflow, Bicep, images, agent resource, and smoke test.</p>

<!-- Presenter notes: Open GitHub Actions and Azure portal. -->

---

# Demo 1 talk-track

<div class="grid2"><div class="card"><h3>Show</h3><ul><li><code>.github/workflows/deploy.yml</code></li><li><code>scripts/deploy.sh</code></li><li>Bicep modules under <code>infra/</code></li><li>GitHub Actions run summary</li></ul></div><div class="card"><h3>Say</h3><p>The agent is deployed and configured like any Azure resource: versioned, reviewed, and repeatable.</p></div></div><pre><code>bash scripts/deploy.sh
bash scripts/configure-agent.sh
bash scripts/smoke-test.sh</code></pre>

<!-- Presenter notes: If deployed, show workflow summary instead of waiting. -->

---

# Agent config as code

<div class="grid2"><div class="card"><h3>Response plans</h3><p><code>app-exception</code> → <code>code-investigator</code><br><code>availability</code> → <code>platform-operator</code></p></div><div class="card"><h3>Least privilege by tool grant</h3><p>Code investigator: no Azure write tools. Platform operator: Azure CLI write but no terminal/GitHub. Read-back verification reports <code>phantom=none</code>.</p></div></div><pre><code>sre-config/agent-config.json
sre-config/skills/*.md
sre-config/instructions/*.md
sre-config/knowledge-base/*.md</code></pre>

<!-- Presenter notes: The guardrail is not just prompt text; it is verified tool grants per subagent with no phantom tools. -->

---

<!-- _class: divider -->

# Demo 2 — code defect to GitHub issue

<p class="lead">A Climbing product detail throws HTTP 500; the agent identifies the source defect and files an issue.</p>

<!-- Presenter notes: No Azure action can fix this class of problem. -->

---

# Demo 2 steps and expected outcome

<div class="grid2 small"><div class="card"><h3>Run</h3><pre><code>REQUESTS=20 bash scripts/trigger-errors.sh</code></pre><p>Wait 5–10 minutes for the alert, or use <code>scripts/ask-agent.sh</code> to skip alert latency.</p></div><div class="card"><h3>Expected</h3><ul><li>Agent follows AppExceptions and stack trace.</li><li>Searches existing issues to avoid duplicates.</li><li>Files GitHub issue with impact, stack excerpt, file:line, suggested fix.</li><li>Hands off to Copilot coding agent with <code>github_assign_copilot_to_issue</code> for a draft PR.</li></ul></div></div>

<!-- Presenter notes: While waiting, show the GitHub MCP connector tools and explain that the PR remains human-reviewed. -->

---

<!-- _class: divider -->

# Demo 3 — config fault to autonomous fix

<p class="lead">A bad Container App environment variable causes 503s; the agent restores known-good configuration and verifies recovery.</p>

<!-- Presenter notes: This is scoped autonomous repair. -->

---

# Demo 3 steps and expected outcome

<div class="grid2 small"><div class="card"><h3>Run</h3><pre><code>BAD_INVENTORY_BACKEND=cosmosdb-prod bash scripts/break-config.sh</code></pre><p>The availability alert fires in about 5–10 minutes.</p></div><div class="card"><h3>Expected</h3><ul><li>Finds <code>CONFIG_ERROR</code> traces.</li><li>Correlates Activity Log / revision change.</li><li>Runs <code>az containerapp update ... INVENTORY_BACKEND=builtin</code>.</li><li>Verifies <code>/health/ready</code> and status return green.</li></ul></div></div>

<!-- Presenter notes: If delayed, run fix-config and narrate expected evidence. -->

---

<!-- _class: divider -->

# Demo 4 — chat, scheduled task, Q&A with the agent

<p class="lead">Use the agent as a reliability analyst before and after alerts.</p>

<!-- Presenter notes: This can fill time during alert latency. -->

---

# Demo 4 prompts

<pre><code>bash scripts/ask-agent.sh "Summarize Contoso Trek health and recent errors. Cite evidence."

bash scripts/ask-agent.sh "Create a concise readiness report for ca-trek-api and ca-trek-web."

bash scripts/ask-agent.sh "What recurring scheduled task would you recommend for this workload?"</code></pre><div class="card"><strong>Show at sre.azure.com:</strong> chat thread, evidence links, tool calls, and scheduled task management.</div>

<!-- Presenter notes: Ask one customer-supplied question. -->

---

<!-- _class: divider -->

# Getting started

<p class="lead">Pilot safely: choose scope, seed knowledge, measure outcomes, then expand autonomy.</p>

<!-- Presenter notes: From demo to adoption. -->

---

# Prerequisites and deployment choices

<div class="grid2"><div class="card"><h3>Azure prerequisites</h3><p>Microsoft.App provider registered; Owner or Contributor + User Access Administrator; supported region; monitoring available.</p></div><div class="card"><h3>Automation paths</h3><p>Portal for evaluation; Bicep / ARM / Terraform AzAPI; Azure Developer CLI recipes; GitHub Actions for Contoso Trek.</p></div></div><p class="source">Sources: <a href="https://learn.microsoft.com/en-us/azure/sre-agent/evaluate">Evaluate</a>; <a href="https://learn.microsoft.com/en-us/azure/sre-agent/deploy-iac">Deploy IaC</a>; <a href="https://learn.microsoft.com/en-us/azure/sre-agent/supported-regions">Regions</a>.</p>

<!-- Presenter notes: Partners can package repeatable deployment. -->

---

# Contoso Trek repo quick start

<pre><code># validate/deploy/configure/smoke-test
bash scripts/deploy.sh
bash scripts/configure-agent.sh
bash scripts/smoke-test.sh

# break/fix scenarios
REQUESTS=20 bash scripts/trigger-errors.sh
BAD_INVENTORY_BACKEND=cosmosdb-prod bash scripts/break-config.sh
bash scripts/fix-config.sh</code></pre><p class="small">Default environment: <code>demo</code>; default location: <code>francecentral</code>; resource group: <code>rg-sre-agent-demo-demo</code>.</p>

<!-- Presenter notes: Commands come directly from the repo. -->

---

# Adoption roadmap

<div class="grid3"><div class="card"><h3>Crawl</h3><p>Reader + Review. Connect telemetry, import runbooks, ask questions, measure triage time.</p></div><div class="card"><h3>Walk</h3><p>Review on scoped resource groups. Add response plans, scheduled tasks, GitHub/ADO issue flow.</p></div><div class="card"><h3>Run</h3><p>Autonomous for narrow tasks. Allow safe, reversible repairs on non-prod or tightly scoped production resources.</p></div></div>

<!-- Presenter notes: Choose one service, two alerts, one runbook, one metric. -->

---

# Competitive landscape: fair positioning

<div class="grid2 small"><div class="card"><h3>Strong Azure-native fit</h3><p>Deep native access to ARM, Resource Graph, Azure Monitor, App Insights, Log Analytics, AKS, Container Apps, App Service, and Functions.</p></div><div class="card"><h3>Connector-mediated multi-tool fit</h3><p>MCP, HTTP triggers, and managed connectors reach non-Azure telemetry and SaaS workflows.</p></div><div class="card"><h3>Competitor strengths</h3><p>PagerDuty: incident orchestration; Datadog: telemetry-native AI; cloud-neutral agents: multi-cloud-first posture.</p></div><div class="card"><h3>Azure differentiator</h3><p>Governed autonomy + Azure control plane + IaC-managed config + persistent memory.</p></div></div><p class="source">Competitive claims are directional and based on third-party context in the research brief; validate for procurement use.</p>

<!-- Presenter notes: Be balanced and fair. -->

---

<!-- _class: closing -->

# Call to action

<p class="lead">Pick one high-signal service, two recurring incident types, and a Reader + Review pilot.</p><div class="grid3"><div class="card"><h3>Week 1</h3><p>Deploy agent, connect Azure Monitor, upload runbooks.</p></div><div class="card"><h3>Week 2</h3><p>Configure response plans and GitHub/ADO workflow.</p></div><div class="card"><h3>Week 3–4</h3><p>Measure MTTR, toil, false positives, and candidate autonomous repairs.</p></div></div>

<!-- Presenter notes: Ask for pilot workload, owner, approver, and success metrics. -->

---

# Resources

<ul><li>Docs: <a href="https://learn.microsoft.com/en-us/azure/sre-agent/overview">https://learn.microsoft.com/en-us/azure/sre-agent/overview</a></li><li>Product page: <a href="https://azure.microsoft.com/en-us/products/sre-agent/">https://azure.microsoft.com/en-us/products/sre-agent/</a></li><li>Pricing model: <a href="https://learn.microsoft.com/en-us/azure/sre-agent/pricing-billing">pricing-billing doc</a></li><li>Retail Prices API: <a href="https://prices.azure.com/api/retail/prices">https://prices.azure.com/api/retail/prices</a></li><li>Portal: <a href="https://sre.azure.com">https://sre.azure.com</a></li><li>Contoso Trek assets: <code>infra/</code>, <code>scripts/</code>, <code>sre-config/</code>, <code>src/</code></li><li>Session materials: <code>docs/session/</code></li></ul>

<!-- Presenter notes: Pricing values are verified from the Retail Prices API; quotes should still confirm current calculator values. -->

---

# Sources used in this deck

<div class="xsmall"><ul><li>Microsoft Learn Azure SRE Agent docs: overview, pricing, evaluation, roles, run modes, permissions, memory, connectors, incidents, response plans, scheduled tasks, triggers, hooks, policies, network, privacy, regions, API, IaC, Live Reports.</li><li>Azure Updates RSS: May 2025 preview, Mar 2026 GA, Aug 2026 trial / VNet / Live Reports announcement.</li><li>Microsoft Developer blog: internal scale and InEight proof points.</li><li>Microsoft Azure SDK Dev Blog: Azure Connector Namespace.</li><li>Local demo contract and repository scripts/configuration.</li></ul></div><p class="source">Full links are in <code>docs/session/README.md</code> and the research brief.</p>

<!-- Presenter notes: Traceability slide; do not linger unless asked. -->
