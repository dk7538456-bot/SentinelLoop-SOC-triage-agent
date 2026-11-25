from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .agent import AgentError, TriageAgent

ROOT = Path(__file__).resolve().parents[2]


def read_jsonl(path: Path):
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.strip():
            try:
                yield json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on line {line_no} of {path}") from exc


def main() -> None:
    parser = argparse.ArgumentParser(prog="sentinelloop", description="LLM-guided security alert triage")
    sub = parser.add_subparsers(dest="command", required=True)
    triage = sub.add_parser("triage", help="Analyze one alert JSON file")
    triage.add_argument("alert", type=Path)
    triage.add_argument("--out", type=Path)
    evaluate = sub.add_parser("evaluate", help="Run the labeled synthetic trace set and build a report")
    evaluate.add_argument("--traces", type=Path, default=ROOT / "data" / "traces.jsonl")
    evaluate.add_argument("--out", type=Path, default=ROOT / "reports")
    args = parser.parse_args()
    try:
        agent = TriageAgent()
        if args.command == "triage":
            result = agent.analyze(json.loads(args.alert.read_text(encoding="utf-8")))
            rendered = json.dumps(result, indent=2, ensure_ascii=False)
            if args.out:
                args.out.parent.mkdir(parents=True, exist_ok=True)
                args.out.write_text(rendered + "\n", encoding="utf-8")
            print(rendered)
        else:
            from .evaluate import evaluate_dataset
            report = evaluate_dataset(agent, list(read_jsonl(args.traces)))
            args.out.mkdir(parents=True, exist_ok=True)
            (args.out / "evaluation.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
            from .dashboard import write_dashboard
            write_dashboard(report, args.out / "dashboard.html")
            print(f"Wrote evaluation and dashboard to {args.out.resolve()}")
    except (AgentError, OSError, ValueError, KeyError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(2)


if __name__ == "__main__":
    main()
