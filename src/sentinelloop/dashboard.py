from __future__ import annotations

import html
import json
from pathlib import Path


def render_dashboard(report: dict) -> str:
    cards = "".join(f'<div class="card"><span>{html.escape(k.title())} precision / recall</span><strong>{v["precision"]:.1%} / {v["recall"]:.1%}</strong><small>n={v["support"]}</small></div>' for k, v in report["per_class"].items())
    rows = "".join(f'<tr><td>{html.escape(str(x["trace_id"]))}</td><td>{html.escape(x["expected"])}</td><td>{html.escape(x["predicted"])}</td><td>{"Yes" if x["correct"] else "No"}</td><td>{html.escape(str(x.get("severity") or ""))}</td></tr>' for x in report["predictions"])
    limitations = "".join(f'<li>{html.escape(item)}</li>' for item in report["limitations"])
    return f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>SentinelLoop Monitoring Report</title>
<style>body{{font:16px system-ui;background:#f4f7fb;color:#172033;margin:0}}main{{max-width:1050px;margin:40px auto;padding:0 22px}}header,.panel,.card{{background:white;border:1px solid #e2e8f0;border-radius:14px;padding:22px;margin-bottom:18px}}h1{{margin:0 0 7px}}.muted,small{{color:#607086}}.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:14px}}.card{{margin:0;display:grid;gap:8px}}.card strong{{font-size:24px}}table{{width:100%;border-collapse:collapse}}td,th{{padding:10px;text-align:left;border-bottom:1px solid #e5eaf0}}.score{{font-size:30px;font-weight:700;color:#2563eb}}</style>
<main><header><h1>SentinelLoop Monitoring Report</h1><div class="muted">LLM-guided SOC alert triage · model {html.escape(str(report['model']))} · {html.escape(report['dataset'])}</div><p><span class="score">{report['accuracy']:.1%}</span> accuracy across {report['total']} labeled traces</p></header>
<section class="cards">{cards}</section><section class="panel"><h2>Trace outcomes</h2><table><thead><tr><th>Trace</th><th>Expected</th><th>Predicted</th><th>Correct</th><th>Severity</th></tr></thead><tbody>{rows}</tbody></table></section>
<section class="panel"><h2>Limitations and operational notes</h2><ul>{limitations}</ul><p>Containment is never executed by this prototype. All proposed response actions need human approval.</p></section></main></html>'''


def write_dashboard(report: dict, path: Path) -> None:
    path.write_text(render_dashboard(report), encoding="utf-8")
