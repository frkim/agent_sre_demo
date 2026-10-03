"""Build the narrated Azure SRE Agent demo video.

Steps: TTS per scene (edge-tts, with subtitle boundaries) -> render cards / record scroll scenes with
Playwright (Edge) -> ffmpeg per-scene segments -> concat -> MP4 with soft subtitles + SRT sidecar.
Usage: python build_video.py [--only scene_id ...]
"""

from __future__ import annotations

import asyncio
import html
import json
import subprocess
import sys
from pathlib import Path

import edge_tts
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
OUT = HERE / "build"
CLIPS = HERE / "clips"
SCENES_DIR = HERE / "scenes"
VOICE = "en-US-AndrewMultilingualNeural"
RATE = "+4%"
W, H, FPS = 1920, 1080, 30
LEAD = 0.5   # seconds of silence before narration
TAIL = 0.9   # seconds after narration

CARD_CSS = """
*{box-sizing:border-box}body{margin:0;width:1920px;height:1080px;font-family:'Segoe UI',system-ui,sans-serif;color:#fff;
background:radial-gradient(circle at 85% 15%,#1a5fa8 0,#0b2a4a 45%,#061626 100%);overflow:hidden}
.frame{position:absolute;inset:0;padding:110px 140px;display:flex;flex-direction:column}
.kicker{font-size:30px;letter-spacing:3px;text-transform:uppercase;color:#7cc7ff;font-weight:600}
h1{font-size:84px;line-height:1.08;margin:18px 0 22px;font-weight:700}
.sub{font-size:38px;color:#c7d8ea;margin:0 0 30px;max-width:1500px}
ul{margin:10px 0 0;padding:0;list-style:none}li{font-size:38px;line-height:1.35;margin:0 0 22px;padding-left:52px;position:relative;color:#e9f1f9}
li:before{content:'';position:absolute;left:0;top:16px;width:22px;height:22px;border-radius:6px;background:linear-gradient(135deg,#0078d4,#50e6ff)}
.stats{display:flex;gap:34px;margin-top:20px}.stat{flex:1;background:rgba(255,255,255,.07);border:1px solid rgba(124,199,255,.35);border-radius:22px;padding:30px 34px}
.stat b{display:block;font-size:66px;color:#50e6ff}.stat span{font-size:28px;color:#c7d8ea}
pre{font-family:'Cascadia Code',Consolas,monospace;font-size:27px;line-height:1.4;background:#030c16;border:1px solid #1f4a72;border-radius:18px;padding:28px 34px;color:#d6f5d6;white-space:pre-wrap;margin:0}
.foot{position:absolute;left:140px;right:140px;bottom:60px;display:flex;justify-content:space-between;font-size:24px;color:#7f9ab3}
.flow{display:flex;align-items:center;gap:16px;margin-top:40px;flex-wrap:nowrap}
.box{background:rgba(255,255,255,.08);border:2px solid #3a8ee6;border-radius:20px;padding:20px 22px;font-size:27px;text-align:center}
.box small{display:block;font-size:22px;color:#a9c4de;margin-top:6px}.arrow{font-size:46px;color:#50e6ff}
.two{display:grid;grid-template-columns:1fr 1fr;gap:50px;margin-top:10px}
.pill{display:inline-block;background:#0078d4;border-radius:999px;padding:6px 20px;font-size:26px;margin-right:10px}
"""


def card(kicker: str, title: str, sub: str = "", body: str = "") -> str:
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{CARD_CSS}</style></head><body><div class='frame'>"
            f"<div class='kicker'>{kicker}</div><h1>{title}</h1>" + (f"<p class='sub'>{sub}</p>" if sub else "")
            + body + "</div><div class='foot'><span>Azure SRE Agent · live demo</span><span>github.com/frkim/agent_sre_demo</span></div></body></html>")


def bullets(items: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def esc(text: str) -> str:
    return html.escape(text)


BREAK_OUT = """$ bash scripts/break-config.sh
==> Breaking Contoso Trek: setting INVENTORY_BACKEND=cosmosdb-prod on ca-trek-api-demo

  Broken at:    2026-10-03T09:12:18Z
  New revision: ca-trek-api-demo--0000004

The storefront banner turns red once the new revision takes traffic.
The 'alert-trek-availability-demo' alert fires within about 5-10 minutes."""

VERIFY_OUT = """==> Connecting Code Access for frkim/agent_sre_demo (main)
==> Connecting GitHub MCP connector (issues, code search)
==> Applying custom instructions · knowledge base · skills
==> Applying subagents · response plans
==> Verification summary
  Knowledge:   contoso-trek-environment.md indexed=true
  Skills:      diagnose-trek-app-exception, repair-trek-inventory-config
  Subagents:
    code-investigator tools=19 phantom=none azureWrite=false
    platform-operator tools=7  phantom=none azureWrite=true terminal=false
  Response plans:
    titleContains=app-exception -> code-investigator
    titleContains=availability  -> platform-operator"""

ARCH = ("<div class='flow'>"
        "<div class='box'>Customers<small>browser</small></div><div class='arrow'>→</div>"
        "<div class='box'>Web · Vue + Vuetify<small>Container App (external)</small></div><div class='arrow'>→</div>"
        "<div class='box'>API · FastAPI<small>Container App (internal)</small></div><div class='arrow'>→</div>"
        "<div class='box'>App Insights + Log Analytics<small>OpenTelemetry</small></div></div>"
        "<div class='flow'>"
        "<div class='box'>2 log alerts<small>HTTP 500 · HTTP 503</small></div><div class='arrow'>→</div>"
        "<div class='box' style='border-color:#50e6ff'>Azure SRE Agent<small>managed identity · least-privilege RBAC</small></div>"
        "<div class='arrow'>→</div><div class='box'>GitHub<small>Code Access + MCP: issues, Copilot</small></div>"
        "<div class='arrow'>+</div><div class='box'>Azure CLI<small>Container Apps Contributor</small></div></div>")

SCENES: list[dict] = [
    {"id": "intro", "kind": "card",
     "html": card("Azure SRE Agent · live demo", "From alert to fix,<br>autonomously",
                  "Two real production incidents on Azure Container Apps — and two very different, correct responses.",
                  "<div style='margin-top:30px'><span class='pill'>Generally available</span><span class='pill'>Azure Monitor</span>"
                  "<span class='pill'>GitHub + Copilot</span><span class='pill'>Least privilege</span></div>"),
     "text": "Hi, and welcome. In the next few minutes you'll watch Azure SRE Agent operate a real application on Azure. "
             "It will detect two different production incidents, find the root cause of each, and respond the right way: "
             "opening a GitHub issue for a code defect, and repairing Azure configuration for a platform fault. "
             "Everything you'll see was deployed and recorded live from this repository."},
    {"id": "what", "kind": "card",
     "html": card("What it is", "An AI site reliability engineer for Azure",
                  body=bullets(["Generally available since March 2026",
                                "Picks up incidents from Azure Monitor, PagerDuty or ServiceNow",
                                "Reads telemetry, resources and source code — then acts within the RBAC you grant",
                                "Runs in review or autonomous mode, with full audit of every action",
                                "Extensible: skills, subagents, MCP connectors, scheduled tasks, HTTP triggers"])),
     "text": "Azure SRE Agent is an AI site reliability engineer for Azure, generally available since March 2026. "
             "It picks up incidents from Azure Monitor, PagerDuty or ServiceNow, reads your telemetry, your resources and your code, "
             "and then acts, but only within the permissions you grant it. You choose review mode or autonomous mode, every action is audited, "
             "and you extend it with skills, subagents, MCP connectors and scheduled tasks."},
    {"id": "architecture", "kind": "card",
     "html": card("The demo environment", "Contoso Trek on Azure Container Apps", body=ARCH),
     "text": "Our test subject is Contoso Trek, an outdoor gear store. A Vue front end and a Python FastAPI back end run on Azure Container Apps, "
             "and send OpenTelemetry to Application Insights. Two log alerts watch for HTTP 500 and HTTP 503 errors, and route to the SRE Agent. "
             "The agent has its own managed identity with least-privilege roles, read access to the GitHub repository, "
             "and a GitHub MCP connector to file issues."},
    {"id": "pipeline", "kind": "clip", "clip": "actions",
     "text": "The whole environment is deployed by a GitHub Actions workflow. It validates the code, the Bicep and the scripts, "
             "deploys the infrastructure and the container images, configures the agent through its data plane API, "
             "and finishes with a smoke test. One push to main, and about six minutes later, everything is live."},
    {"id": "config", "kind": "card",
     "html": card("Agent configuration as code", "Instructions, skills, subagents and routing — in Git",
                  body=f"<pre>{esc(VERIFY_OUT)}</pre>"),
     "text": "The agent's behaviour lives in Git as well: global instructions, a knowledge base, two skills, two specialised subagents, "
             "and response plans that route each alert to the right subagent. Notice the tool grants. The code investigator has no Azure write tools. "
             "The platform operator can run Azure CLI writes, but has no terminal and no GitHub access. "
             "The script reads everything back to prove that what's deployed matches the source."},
    {"id": "storefront", "kind": "clip", "clip": "storefront",
     "text": "Here is the storefront. The banner at the top reflects live health: green means all systems operational. "
             "Search, sorting, filtering and product details all work as expected."},
    {"id": "s1", "kind": "card",
     "html": card("Scenario 1", "A code defect", "Some product pages return HTTP 500. No Azure setting can fix it.",
                  bullets(["Expected response: find the faulty line and open a GitHub issue",
                           "Must NOT restart, scale or reconfigure anything"])),
     "text": "Scenario one: a code defect. Some product pages fail with an HTTP 500. No Azure setting can fix this, "
             "so the right response is to find the faulty line of code and open a GitHub issue, without touching any Azure resource."},
    {"id": "failure", "kind": "clip", "clip": "failure",
     "text": "Let's open a climbing harness. The product fails to load, and the banner turns amber. "
             "The exception lands in Application Insights, and a few minutes later the Azure Monitor alert fires."},
    {"id": "transcript_s1", "kind": "scroll", "html_file": "transcript_s1.html",
     "text": "This is the agent's own investigation thread, retrieved from its API. The alert arrives, and the code investigator subagent takes over. "
             "It loads its diagnostic skill and searches the knowledge base. It queries Log Analytics for the blast radius and the stack trace, "
             "then reads the source code: main dot py and catalog dot py. It searches GitHub for an existing issue, finds none, and files a new one. "
             "Then it hands the fix to GitHub Copilot coding agent, and closes the alert. "
             "From alert to issue and pull request: about two and a half minutes, with no human involved, and no Azure resource modified."},
    {"id": "github_issue", "kind": "clip", "clip": "github_issue",
     "text": "Here is the issue the agent opened. It has the impact window, the number of failed requests, the root cause with a permalink "
             "to catalog dot py, line one hundred nineteen, the stack trace excerpt, and a suggested fix. It is labelled, and assigned to Copilot."},
    {"id": "github_pr", "kind": "clip", "clip": "github_pr",
     "text": "And GitHub Copilot coding agent has already opened a draft pull request: a guarded division, plus regression tests. "
             "A human reviews and merges it. The SRE agent diagnoses; Copilot writes the code; your team stays in control."},
    {"id": "s2", "kind": "card",
     "html": card("Scenario 2", "A platform fault", "The catalog returns HTTP 503 after a bad configuration change. The code is fine.",
                  bullets(["Expected response: correlate with the change and repair the Container App",
                           "Must NOT open a code ticket or redeploy the image"])),
     "text": "Scenario two is the opposite case: a platform fault. A bad configuration change takes the catalog down with HTTP 503 errors. "
             "The code is fine, so the right response is to repair the Azure configuration."},
    {"id": "break", "kind": "card",
     "html": card("Injecting the fault", "A one-line configuration change", body=f"<pre>{esc(BREAK_OUT)}</pre>"),
     "text": "We simulate a risky change: one environment variable on the API container app now points to an inventory backend "
             "that this build doesn't support. Container Apps rolls out a new revision."},
    {"id": "outage", "kind": "clip", "clip": "outage",
     "text": "Within seconds, the banner turns red. The catalog is empty, and every catalog request returns HTTP 503. "
             "This is a full outage for customers."},
    {"id": "transcript_s2", "kind": "scroll", "html_file": "transcript_s2.html",
     "text": "The availability alert fires, and this time the response plan routes it to the platform operator subagent. "
             "It confirms the 503 errors and the configuration error in the logs, checks the Activity Log to find the change that caused it, "
             "and restores the correct value with an Azure CLI update. Then it verifies that the new revision is healthy and the catalog is serving again."},
    {"id": "recovered", "kind": "clip", "clip": "recovered",
     "text": "And the storefront is back to green. No redeploy, no code change, and no engineer paged in the middle of the night."},
    {"id": "governance", "kind": "card",
     "html": card("Trust and control", "Autonomy you can govern",
                  body=bullets(["Managed identity with built-in roles scoped to the resource group",
                                "Per-subagent tool grants: diagnose-only vs. fix-only",
                                "Review mode for approvals, autonomous mode where you're confident",
                                "Every query, command and tool call is visible in the thread",
                                "Configuration as code: reviewed, versioned, verified"])),
     "text": "What makes this safe is governance. The agent uses a managed identity with built-in roles, scoped to one resource group. "
             "Each subagent only has the tools it needs. Start in review mode, where a human approves each action, and move to autonomous mode "
             "where you're confident. And every query and command is visible in the thread for audit."},
    {"id": "pricing", "kind": "card",
     "html": card("Pricing", "Pay per Azure Agent Unit (AAU)",
                  body="<div class='stats'><div class='stat'><b>4 AAU / h</b><span>always-on, per agent<br>≈ 2,920 AAU per month</span></div>"
                       "<div class='stat'><b>$0.10–0.11</b><span>per AAU (East US / France Central,<br>Azure Retail Prices, Oct 2026)</span></div>"
                       "<div class='stat'><b>≈ $292 / mo</b><span>always-on baseline (East US)<br>+ token-based active usage</span></div></div>"
                       + bullets(["Active flow: e.g. ~12 AAU (GPT) to ~35 AAU (Claude) per incident investigation",
                                  "Monthly AAU cap from 500 to 1,000,000 · 30-day trial waives always-on charges"])),
     "text": "Pricing is based on Azure Agent Units. Each agent consumes four units per hour while it exists, which is about two thousand nine hundred units a month, "
             "or roughly two hundred ninety dollars at ten cents per unit in East US. On top of that, active work is metered by tokens: "
             "an incident investigation costs roughly twelve to thirty-five units depending on the model. "
             "You can cap monthly usage, and a thirty-day trial waives the always-on charge. Always confirm regional prices in the calculator."},
    {"id": "limits", "kind": "card",
     "html": card("Know the limits", "Plan for these",
                  body=bullets(["Available in 22+ Azure regions; data stays in the agent's region",
                                "It can only act where its identity has RBAC — by design",
                                "Alert-driven flows inherit alert latency (5–10 min for log alerts)",
                                "Up to 80 MCP tools per agent; GitHub OAuth limited to 10 tokens",
                                "Some features (Live Reports, Connector Namespace) are still in preview"])),
     "text": "Plan for a few limits. The agent is available in more than twenty Azure regions. It can only act where its identity has permissions, which is the point. "
             "Alert-driven flows inherit your alert latency, typically five to ten minutes for log alerts. Connectors have tool budgets, "
             "and some newer features are still in preview."},
    {"id": "outro", "kind": "card",
     "html": card("Get started", "Try it on your own workload",
                  body=bullets(["Fork github.com/frkim/agent_sre_demo and run the deploy workflow",
                                "Start in review mode on one resource group",
                                "Encode your runbooks as skills; route alerts with response plans",
                                "Learn more: learn.microsoft.com/azure/sre-agent · sre.azure.com"])),
     "text": "To get started, fork this repository and run the deploy workflow, or point the agent at one of your own resource groups in review mode. "
             "Encode your runbooks as skills, and route your alerts with response plans. Thanks for watching."},
]


async def tts(scene: dict) -> None:
    mp3, srt = OUT / f"{scene['id']}.mp3", OUT / f"{scene['id']}.srt"
    if mp3.exists() and srt.exists() and (OUT / f"{scene['id']}.txt").read_text(encoding="utf-8") == scene["text"]:
        return
    comm = edge_tts.Communicate(scene["text"], VOICE, rate=RATE, boundary="SentenceBoundary")
    sub = edge_tts.SubMaker()
    with mp3.open("wb") as fh:
        async for chunk in comm.stream():
            if chunk["type"] == "audio":
                fh.write(chunk["data"])
            elif chunk["type"] in ("WordBoundary", "SentenceBoundary"):
                sub.feed(chunk)
    srt.write_text(sub.get_srt(), encoding="utf-8")
    (OUT / f"{scene['id']}.txt").write_text(scene["text"], encoding="utf-8")


def duration(path: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def render_visuals(scenes: list[dict]) -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge")
        for s in scenes:
            if s["kind"] == "card":
                page = browser.new_page(viewport={"width": W, "height": H})
                f = SCENES_DIR / f"card_{s['id']}.html"
                f.write_text(s["html"], encoding="utf-8")
                page.goto(f.as_uri())
                page.wait_for_timeout(400)
                page.screenshot(path=str(OUT / f"{s['id']}.png"))
                page.close()
            elif s["kind"] == "scroll":
                total = duration(OUT / f"{s['id']}.mp3") + LEAD + TAIL
                ctx = browser.new_context(viewport={"width": W, "height": H}, record_video_dir=str(OUT / "_rec"),
                                          record_video_size={"width": W, "height": H})
                page = ctx.new_page()
                page.goto((SCENES_DIR / s["html_file"]).as_uri())
                page.wait_for_timeout(300)
                hold = 2500
                ms = int(total * 1000) - 2 * hold
                page.wait_for_timeout(hold)
                page.evaluate("""(ms) => new Promise(res => { const max = document.body.scrollHeight - innerHeight; const t0 = performance.now();
                    function step(t){ const k = Math.min(1,(t-t0)/ms); const e = k<.5?2*k*k:1-Math.pow(-2*k+2,2)/2; scrollTo(0, max*e);
                    if(k<1) requestAnimationFrame(step); else res(); } requestAnimationFrame(step); })""", ms)
                page.wait_for_timeout(hold + 500)
                video = page.video
                ctx.close()
                target = OUT / f"{s['id']}.webm"
                target.unlink(missing_ok=True)
                Path(video.path()).rename(target)
        browser.close()


def ffmpeg(*args: str) -> None:
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *args], check=True)


def segment(s: dict) -> Path:
    audio = OUT / f"{s['id']}.mp3"
    a_dur = duration(audio) + LEAD + TAIL
    seg = OUT / f"seg_{s['id']}.mp4"
    afilter = f"[1:a]adelay={int(LEAD * 1000)}:all=1,apad,aresample=48000[a]"
    venc = ["-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-r", str(FPS),
            "-c:a", "aac", "-b:a", "160k", "-ac", "2"]
    if s["kind"] == "card":
        ffmpeg("-loop", "1", "-framerate", str(FPS), "-i", str(OUT / f"{s['id']}.png"), "-i", str(audio),
               "-filter_complex", f"[0:v]scale={W}:{H},format=yuv420p[v];{afilter}", "-map", "[v]", "-map", "[a]",
               "-t", f"{a_dur:.2f}", *venc, str(seg))
    else:
        src = CLIPS / f"{s['clip']}.webm" if s["kind"] == "clip" else OUT / f"{s['id']}.webm"
        v_dur = duration(src)
        total = max(v_dur, a_dur)
        pad = max(0.0, total - v_dur) + 0.5
        ffmpeg("-i", str(src), "-i", str(audio), "-filter_complex",
               f"[0:v]fps={FPS},scale={W}:{H},tpad=stop_mode=clone:stop_duration={pad:.2f},format=yuv420p[v];{afilter}",
               "-map", "[v]", "-map", "[a]", "-t", f"{total:.2f}", *venc, str(seg))
    return seg


def srt_time(t: float) -> str:
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}"


def parse_srt(text: str) -> list[tuple[float, float, str]]:
    cues = []
    for block in text.strip().split("\n\n"):
        lines = block.strip().splitlines()
        if len(lines) < 3:
            continue
        a, b = lines[1].split(" --> ")
        def secs(x: str) -> float:
            h, m, rest = x.strip().split(":")
            s, ms = rest.replace(".", ",").split(",")
            return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000
        cues.append((secs(a), secs(b), " ".join(lines[2:])))
    return cues


def main() -> None:
    OUT.mkdir(exist_ok=True)
    only = set(sys.argv[sys.argv.index("--only") + 1:]) if "--only" in sys.argv else None
    todo = [s for s in SCENES if not only or s["id"] in only]

    async def run_tts() -> None:
        for s in todo:
            await tts(s)
    asyncio.run(run_tts())
    render_visuals(todo)
    for s in todo:
        segment(s)
        print("segment", s["id"])

    concat = OUT / "concat.txt"
    concat.write_text("".join(f"file '{(OUT / f'seg_{s['id']}.mp4').as_posix()}'\n" for s in SCENES), encoding="utf-8")
    master = OUT / "master.mp4"
    ffmpeg("-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(master))

    cues, offset, n = [], 0.0, 0
    for s in SCENES:
        for a, b, text in parse_srt((OUT / f"{s['id']}.srt").read_text(encoding="utf-8")):
            n += 1
            cues.append(f"{n}\n{srt_time(offset + LEAD + a)} --> {srt_time(offset + LEAD + b)}\n{text}\n")
        offset += duration(OUT / f"seg_{s['id']}.mp4")
    srt = HERE / "sre-agent-demo.en.srt"
    srt.write_text("\n".join(cues), encoding="utf-8")
    final = HERE / "sre-agent-demo.mp4"
    ffmpeg("-i", str(master), "-i", str(srt), "-map", "0", "-map", "1", "-c", "copy", "-c:s", "mov_text",
           "-metadata:s:s:0", "language=eng", "-movflags", "+faststart", str(final))
    print(f"final {final} {duration(final):.1f}s")
    json.dump([{"id": s["id"], "text": s["text"]} for s in SCENES], (HERE / "narration.json").open("w", encoding="utf-8"), indent=2)


if __name__ == "__main__":
    main()
