"""Render an SRE Agent thread (GET /api/v1/threads/{id}/messages) as a styled HTML timeline."""

from __future__ import annotations

import html
import json
import re
import sys
from datetime import datetime
from pathlib import Path

CSS = """
*{box-sizing:border-box} body{margin:0;font-family:'Segoe UI',system-ui,sans-serif;background:#0b1f33;color:#e8eef5}
.wrap{width:1500px;margin:0 auto;padding:40px 0 400px}
header{display:flex;align-items:center;gap:18px;margin-bottom:26px}
header .logo{width:56px;height:56px;border-radius:14px;background:linear-gradient(135deg,#0078d4,#50e6ff);display:grid;place-items:center;font-weight:700;font-size:26px}
header h1{font-size:34px;margin:0} header p{margin:4px 0 0;color:#9fb6cc;font-size:20px}
.msg{display:grid;grid-template-columns:110px 1fr;gap:18px;margin:12px 0}
.time{color:#7f9ab3;font-size:18px;padding-top:14px;font-variant-numeric:tabular-nums}
.card{background:#12304d;border:1px solid #1f4a72;border-radius:14px;padding:14px 20px;font-size:21px;line-height:1.45}
.card.alert{background:#4a1520;border-color:#a4262c}
.card.reason{background:#0f2840;border-style:dashed;color:#b9cde0;font-style:italic}
.card.tool{background:#102a1e;border-color:#2e7d4f}
.card.final{background:#0d3b2a;border-color:#3fb37f}
.tag{display:inline-block;font-size:15px;font-weight:700;letter-spacing:.5px;padding:3px 10px;border-radius:999px;margin-bottom:8px;text-transform:uppercase}
.t-alert{background:#a4262c}.t-reason{background:#2b4f74}.t-tool{background:#2e7d4f}.t-agent{background:#0078d4}.t-final{background:#3fb37f;color:#04231a}
code,pre{font-family:'Cascadia Code',Consolas,monospace;font-size:18px} pre{white-space:pre-wrap;background:#081726;padding:10px 14px;border-radius:8px;margin:8px 0 0}
code{background:#081726;padding:1px 6px;border-radius:5px}
a{color:#7cc7ff} h2,h3{margin:6px 0} ul,ol{margin:6px 0 6px 24px;padding:0} table{border-collapse:collapse;margin:6px 0}td,th{border:1px solid #2b4f74;padding:4px 10px}
"""


def redact(text: str) -> str:
    """Hide connection-string material that tools may echo (keys, secrets, tokens)."""
    text = re.sub(r"(InstrumentationKey=)[^;\s\"]+", r"\1••••••••", text, flags=re.I)
    return re.sub(r"((?:AccountKey|SharedAccessKey|Password|token)=)[^;\s\"]+", r"\1••••••••", text, flags=re.I)


def md(text: str) -> str:
    """Tiny markdown subset -> HTML (headings, bold, code, links, lists, fenced code)."""
    out, in_code, buf, in_list = [], False, [], None
    for raw in text.splitlines():
        if raw.strip().startswith("```"):
            if in_code:
                out.append("<pre>" + html.escape("\n".join(buf)) + "</pre>")
                buf, in_code = [], False
            else:
                in_code = True
            continue
        if in_code:
            buf.append(raw)
            continue
        line = html.escape(raw)
        line = re.sub(r"`([^`]+)`", r"<code>\1</code>", line)
        line = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", line)
        line = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', line)
        m_ol, m_ul = re.match(r"^\s*\d+\.\s+(.*)", line), re.match(r"^\s*[-*]\s+(.*)", line)
        kind = "ol" if m_ol else "ul" if m_ul else None
        if in_list and kind != in_list:
            out.append(f"</{in_list}>")
            in_list = None
        if kind:
            if not in_list:
                out.append(f"<{kind}>")
                in_list = kind
            out.append(f"<li>{(m_ol or m_ul).group(1)}</li>")
        elif line.startswith("## "):
            out.append(f"<h2>{line[3:]}</h2>")
        elif line.startswith("### "):
            out.append(f"<h3>{line[4:]}</h3>")
        elif line.startswith("|"):
            if re.match(r"^\|[\s\-|:]+\|$", raw.strip()):
                continue
            cells = [c.strip() for c in line.strip("|").split("|")]
            out.append("<table><tr>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr></table>")
        elif line.strip():
            out.append(f"<div>{line}</div>")
    if in_list:
        out.append(f"</{in_list}>")
    return "\n".join(out)


def render(thread_file: Path, title: str, subtitle: str, out: Path, max_reason_chars: int = 260) -> None:
    data = json.loads(thread_file.read_text(encoding="utf-8-sig"))
    items = data["value"] if isinstance(data, dict) and "value" in data else data
    items = sorted(items, key=lambda m: m["timeStamp"])
    rows = []
    for i, m in enumerate(items):
        ts = datetime.fromisoformat(m["timeStamp"].replace("Z", "+00:00")).strftime("%H:%M:%S")
        text = redact(m.get("text") or "")
        if text.startswith("```incident-alert"):
            alert = json.loads(text.split("\n", 1)[1].rsplit("```", 1)[0])
            body = (f"<span class='tag t-alert'>Azure Monitor alert · {html.escape(alert['severity'])}</span>"
                    f"<div><b>{html.escape(alert['alertRule'])}</b></div><div>{html.escape(alert['description'])}</div>"
                    f"<div style='color:#f3b8bc;font-size:17px'>Fired {html.escape(alert['firedAt'])}</div>")
            cls = "alert"
        elif m.get("messageType") == "Reasoning":
            snippet = re.sub(r"\*\*([^*]+)\*\*\s*", r"\1 — ", text.strip(), count=1)
            snippet = snippet[:max_reason_chars] + ("…" if len(snippet) > max_reason_chars else "")
            body = f"<span class='tag t-reason'>Reasoning</span><div>{html.escape(snippet)}</div>"
            cls = "reason"
        elif m.get("azCliExecution"):
            ex = m["azCliExecution"]
            fn = json.loads(ex.get("originalFunctionCall") or "{}").get("Name", "Azure CLI")
            outp = redact((ex.get("output") or ex.get("error") or "").strip())
            outp = outp[:400] + ("…" if len(outp) > 400 else "")
            body = (f"<span class='tag t-tool'>{html.escape(fn)} · {html.escape(ex.get('status', ''))}</span>"
                    f"<pre>$ {html.escape(ex['command'])}</pre>" + (f"<pre>{html.escape(outp)}</pre>" if outp else ""))
            cls = "tool"
        elif m.get("mcpToolExecution"):
            ex = m["mcpToolExecution"]
            params = {k: v for k, v in (ex.get("parameters", {}).get("raw") or {}).items() if k not in ("body",)}
            body = (f"<span class='tag t-tool'>GitHub MCP · {html.escape(ex['displayName'])} · {html.escape(ex['status'])}</span>"
                    f"<pre>{html.escape(json.dumps(params, ensure_ascii=False)[:500])}</pre>")
            cls = "tool"
        elif m.get("readFileResult") or m.get("memorySearchResult") or m.get("grepSearchResult"):
            body = f"<span class='tag t-tool'>Tool</span><div>{html.escape(text)}</div>"
            cls = "tool"
        elif not text.strip():
            continue
        else:
            final = i == len(items) - 1 or "complete" in text[:60].lower()
            body = f"<span class='tag {'t-final' if final else 't-agent'}'>{'Summary' if final else 'Azure SRE Agent'}</span>" + md(text)
            cls = "final" if final else ""
        rows.append(f"<div class='msg'><div class='time'>{ts}</div><div class='card {cls}'>{body}</div></div>")
    page = (f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body><div class='wrap'>"
            f"<header><div class='logo'>SRE</div><div><h1>{html.escape(title)}</h1><p>{html.escape(subtitle)}</p></div></header>"
            + "\n".join(rows) + "</div></body></html>")
    out.write_text(page, encoding="utf-8")


if __name__ == "__main__":
    render(Path(sys.argv[1]), sys.argv[2], sys.argv[3], Path(sys.argv[4]))
