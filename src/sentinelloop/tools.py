"""Read-only mock enrichment and approval-gated response planning tools."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"

TOOL_DEFINITIONS = [
    {"type": "function", "function": {"name": "lookup_asset", "description": "Look up an endpoint or account in the local mock asset inventory.",
      "parameters": {"type": "object", "properties": {"identifier": {"type": "string"}}, "required": ["identifier"], "additionalProperties": False}}},
    {"type": "function", "function": {"name": "search_intel", "description": "Search the local mock threat-intelligence feed for an indicator.",
      "parameters": {"type": "object", "properties": {"indicator": {"type": "string"}}, "required": ["indicator"], "additionalProperties": False}}},
    {"type": "function", "function": {"name": "draft_containment", "description": "Draft a containment proposal for human review; this tool does not perform containment.",
      "parameters": {"type": "object", "properties": {"target": {"type": "string"}, "reason": {"type": "string"}}, "required": ["target", "reason"], "additionalProperties": False}}},
]


def _records(filename: str) -> list[dict[str, Any]]:
    path = DATA / filename
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def run_tool(name: str, args: dict[str, Any]) -> dict[str, Any]:
    if name == "lookup_asset":
        key = str(args.get("identifier", "")).casefold()
        hits = [x for x in _records("assets.jsonl") if key in str(x).casefold()]
        return {"matches": hits[:5], "source": "synthetic local inventory"}
    if name == "search_intel":
        key = str(args.get("indicator", "")).casefold()
        hits = [x for x in _records("intel.jsonl") if key and key in str(x).casefold()]
        return {"matches": hits[:5], "source": "synthetic local feed"}
    if name == "draft_containment":
        return {"status": "proposal_pending_human_approval", "target": args.get("target"),
                "reason": args.get("reason"), "executed": False}
    raise ValueError(f"Tool not allowed: {name}")
