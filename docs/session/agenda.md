# Azure SRE Agent — 90-minute run of show

| Time | Segment | Presenter action | Slides | Demo step | Fallback |
| --- | --- | --- | --- | --- | --- |
| 0:00–0:03 | Welcome | Introduce purpose, attendees, and expected decisions. | 1–2 | None | Use slide 2 as the compact agenda if running late. |
| 0:03–0:10 | On-call problem | Align on on-call pain: toil, MTTR, alert fatigue, approval anxiety, and lost knowledge. | 3–4 | None | Skip discussion and move to product definition. |
| 0:10–0:20 | What Azure SRE Agent is | Explain usage patterns and timeline from preview to GA to Aug 2026 updates. | 5–8 | None | Keep timeline to one minute if audience already knows the product. |
| 0:20–0:30 | Architecture / how it works | Walk operating model, incident loop, incident platforms, memory, skills, response plans, connectors, Code Access, and the incident-to-PR hand-off. | 9–17 | None | Use slides 10–11 and 17 only if time is tight. |
| 0:30–0:42 | Governance and security | Cover roles, Review vs Autonomous, Reader vs Privileged, data privacy, network, policies, and hooks. | 18–22 | None | Jump to slide 19 for the core control message. |
| 0:42–0:50 | Benefits, pricing, limits | Use official proof points; explain verified AAU pricing, active-flow examples, budget cap, trial, and limits. | 23–32 | None | Remind that prices vary by region/currency; confirm calculator values for quotes. |
| 0:50–0:58 | Demo 1: deploy and configure | Show GitHub Actions `deploy.yml`, `scripts/deploy.sh`, Bicep, and `scripts/configure-agent.sh`; run or show prior summary. | 33–36 | `bash scripts/deploy.sh`; `bash scripts/configure-agent.sh`; `bash scripts/smoke-test.sh` | If deployment is slow, show existing workflow summary and resource group. |
| 0:58–1:08 | Demo 2: code defect to issue and PR | Trigger Climbing product HTTP 500s; show thread at `sre.azure.com`, GitHub issue with file:line, and Copilot coding agent draft PR hand-off. | 37–38 | `REQUESTS=20 bash scripts/trigger-errors.sh` | Use `scripts/ask-agent.sh` or `docs/session/video/sre-agent-demo.mp4` if alert latency exceeds 10 minutes. |
| 1:08–1:18 | Demo 3: config fault to autonomous fix | Break `INVENTORY_BACKEND`; show red banner, correlation, Azure CLI repair, and green recovery. | 39–40 | `BAD_INVENTORY_BACKEND=cosmosdb-prod bash scripts/break-config.sh` | Run `bash scripts/fix-config.sh` manually and narrate expected evidence. |
| 1:18–1:24 | Demo 4: chat / scheduled task / Q&A | Ask health/readiness prompts; show how scheduled tasks are created and reviewed. | 41–42 | `bash scripts/ask-agent.sh "Summarize Contoso Trek health and recent errors. Cite evidence."` | Use prepared outputs from a prior successful run. |
| 1:24–1:28 | Adoption roadmap and competitive framing | Recommend Reader + Review pilot and fair competitive framing. | 43–47 | None | Skip competitive slide unless asked. |
| 1:28–1:30 | Close | Confirm pilot candidate, owner, governance approver, next workshop, and share resources. | 48–50 | None | Send README, FAQ, demo script, and plan B video link as follow-up. |

## Buffers and Q&A

- Keep a 5-minute buffer inside the demo block for Azure Monitor alert latency.
- Use direct chat prompts or `docs/session/video/sre-agent-demo.mp4` if alert latency exceeds 10 minutes.
- Do not live-debug deployment failures; show validated outputs and move to the reliability scenario.
- Pricing is now verified from the Azure Retail Prices API: East US/East US 2 $0.10 per AAU; France Central/Sweden Central $0.11; West Europe $0.14; France Central EUR 0.10. Prices vary by region/currency; confirm in the calculator for quotes.
