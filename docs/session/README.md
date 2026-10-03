# Azure SRE Agent customer session materials

This folder contains English materials for a 90-minute customer/partner session on Azure SRE Agent and the Contoso Trek demo.

## Files

| File | Purpose |
| --- | --- |
| `deck/azure-sre-agent.md` | Marp source deck with inline Azure-themed styling and speaker notes on every slide. |
| `deck/diagrams/*.mmd` | Mermaid source for deck diagrams. |
| `deck/diagrams/*.svg` | Rendered diagram images used by Marp. |
| `deck/azure-sre-agent.pptx` | Exported PowerPoint deck. |
| `deck/azure-sre-agent.pdf` | Exported PDF deck. |
| `deck/azure-sre-agent.html` | Exported HTML deck. |
| `agenda.md` | 90-minute run-of-show with slide numbers, demo steps, buffers, and fallbacks. |
| `pitch-narrative.md` | Executive narrative, persona messages, proof points, pricing talk-track, objections, and CTA. |
| `demo-script.md` | Live demo script with exact repo commands, outcomes, reset, and Plan B. |
| `faq.md` | 20+ customer Q&As with citations. |
| `video/sre-agent-demo.mp4` | 7½-minute English-narrated recording of the live demo (embedded subtitles) — Plan B. |
| `video/README.md` | Video storyboard, provenance, and rebuild instructions. |
| `research/sre-agent-research.md` | Cited research brief (status, features, pricing, limits, competitors) behind every claim. |

## Export commands

Run from the repository root.

```bash
npx --yes @mermaid-js/mermaid-cli -i docs/session/deck/diagrams/sre-agent-architecture.mmd -o docs/session/deck/diagrams/sre-agent-architecture.svg
npx --yes @mermaid-js/mermaid-cli -i docs/session/deck/diagrams/incident-loop.mmd -o docs/session/deck/diagrams/incident-loop.svg
npx --yes @mermaid-js/mermaid-cli -i docs/session/deck/diagrams/governance-stack.mmd -o docs/session/deck/diagrams/governance-stack.svg

npx --yes @marp-team/marp-cli docs/session/deck/azure-sre-agent.md --pptx -o docs/session/deck/azure-sre-agent.pptx --allow-local-files
npx --yes @marp-team/marp-cli docs/session/deck/azure-sre-agent.md --pdf -o docs/session/deck/azure-sre-agent.pdf --allow-local-files
npx --yes @marp-team/marp-cli docs/session/deck/azure-sre-agent.md --html -o docs/session/deck/azure-sre-agent.html --allow-local-files
```

The workstation npm configuration should use the Microsoft-protected feed: `https://packagefeedproxy.microsoft.io/npm/`.

## Pricing note

Verified AAU prices from the Azure Retail Prices API: East US/East US 2 USD 0.10, France Central/Sweden Central USD 0.11, West Europe USD 0.14 effective 2026-10-01, and France Central EUR 0.10. Prices vary by region/currency; confirm current calculator values for formal quotes.
Use the Retail Prices API values for examples and confirm current calculator values for formal customer quotes.
Source: Azure Retail Prices API (https://prices.azure.com/api/retail/prices, meterName=SRE Agent Unit, serviceName Foundry Tools, productName Azure Agent Unit, queried 2026-10-03); pricing model source: https://learn.microsoft.com/en-us/azure/sre-agent/pricing-billing.

## Primary source links

- Azure SRE Agent overview: https://learn.microsoft.com/en-us/azure/sre-agent/overview
- Pricing and billing: https://learn.microsoft.com/en-us/azure/sre-agent/pricing-billing
- Azure Retail Prices API: https://prices.azure.com/api/retail/prices
- Evaluate / 30-day trial: https://learn.microsoft.com/en-us/azure/sre-agent/evaluate
- Data privacy: https://learn.microsoft.com/en-us/azure/sre-agent/data-privacy
- User roles: https://learn.microsoft.com/en-us/azure/sre-agent/user-roles
- Run modes: https://learn.microsoft.com/en-us/azure/sre-agent/run-modes
- Permissions: https://learn.microsoft.com/en-us/azure/sre-agent/permissions
- Memory: https://learn.microsoft.com/en-us/azure/sre-agent/memory
- MCP connectors: https://learn.microsoft.com/en-us/azure/sre-agent/mcp-connectors
- GitHub connector: https://learn.microsoft.com/en-us/azure/sre-agent/github-connector
- Incident platforms: https://learn.microsoft.com/en-us/azure/sre-agent/incident-platforms
- Response plans: https://learn.microsoft.com/en-us/azure/sre-agent/incident-response-plans
- Scheduled tasks: https://learn.microsoft.com/en-us/azure/sre-agent/scheduled-tasks
- HTTP triggers: https://learn.microsoft.com/en-us/azure/sre-agent/http-triggers
- Live Reports: https://learn.microsoft.com/en-us/azure/sre-agent/live-reports
- Network integration: https://learn.microsoft.com/en-us/azure/sre-agent/network-integration
- Supported regions: https://learn.microsoft.com/en-us/azure/sre-agent/supported-regions
- API reference: https://learn.microsoft.com/en-us/azure/sre-agent/api-reference
- Deploy with IaC: https://learn.microsoft.com/en-us/azure/sre-agent/deploy-iac
- Microsoft Developer blog proof points: https://developer.microsoft.com/blog/try-azure-sre-agent-with-no-always-on-charges/
- Azure Connector Namespace blog: https://devblogs.microsoft.com/azure-sdk/power-azure-sre-agent-with-connector-namespace/

## Remaining verify items

- Exact Ignite 2025 preview-expansion date.
- Whether a service principal that creates an agent via IaC is auto-granted SRE Agent Administrator (this repo assigns the role explicitly in Bicep, so the demo does not depend on it).
- Detailed Ecolab and 40.5-hours-to-3-minutes claims before quoting.
- Whether Grafana/Jira are native MCP connectors or webhook/HTTP-trigger-only.
- Any explicit max concurrent incidents/chat threads limit.
- SRE-Agent-specific Responsible AI Transparency Note, if published after the research brief.
