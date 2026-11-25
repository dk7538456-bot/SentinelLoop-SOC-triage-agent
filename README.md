# SentinelLoop Agent

SentinelLoop is a small, original SOC triage prototype for the AI Agentic Engineer internship assessment. It observes a structured alert, can choose read-only enrichment tools, reasons through the evidence with an LLM, and returns a structured triage decision. Response actions are only drafted for a human; the program has no endpoint-control integration.

## What it demonstrates

- LLM-directed tool use rather than a static alert-to-answer lookup table.
- A bounded agent loop, structured output, and a traceable tool-call audit.
- Synthetic asset and threat-intelligence tools with explicit source labels.
- Human approval boundary for containment proposals.
- Labeled synthetic traces and an evaluation command that calculates accuracy, per-class precision/recall, and a confusion matrix from actual model outputs.
- A self-contained HTML monitoring report generated from the evaluation results.

## Requirements

- Python 3.10 or later.
- An API key for an OpenAI-compatible chat-completions endpoint. The default is OpenAI; compatible local or hosted endpoints can be configured with `OPENAI_BASE_URL` and `OPENAI_MODEL`.
- Network access to the configured model endpoint.

The Python application uses only the standard library. The API key is sent to the endpoint you configure. Do not use real customer alerts in this prototype.

## Installation

### Windows PowerShell

```powershell
cd sentinelloop-agent
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
Copy-Item .env.example .env
notepad .env
```

Set `OPENAI_API_KEY` in `.env`. If using a compatible service, also set its base URL and model name. The application reads this project-local file at startup. Do not commit `.env`.

### macOS / Linux

```bash
cd sentinelloop-agent
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
cp .env.example .env
```

Export the variables from `.env` in your shell (or set them through your environment manager); the project intentionally does not load `.env` automatically.

## Run one alert

```bash
sentinelloop triage examples/alert.json --out reports/triage.json
```

The result contains classification, severity, confidence, evidence, recommendations, human-review status, and the tool audit. To use the module without installing the command, run `python -m sentinelloop.cli triage examples/alert.json` after installation.

## Evaluate and create dashboard

```bash
sentinelloop evaluate
```

This sends every row in `data/traces.jsonl` to the configured model and writes `reports/evaluation.json` and `reports/dashboard.html`. Open the HTML file in a browser. Metrics are computed from the model's observed predictions; they are not prefilled claims. The authored trace labels are synthetic reference labels, not a production benchmark.

## Architecture

1. `cli.py` accepts an alert or starts evaluation.
2. `agent.py` calls an OpenAI-compatible chat-completions API and processes model-selected tool calls up to a fixed turn limit.
3. `tools.py` exposes only local mock inventory/feed lookups and a containment proposal tool. Unknown tool names fail closed.
4. `evaluate.py` compares model outputs with the reference labels and calculates metrics.
5. `dashboard.py` renders the resulting JSON report as a portable HTML dashboard.

## Safety and known limits

- Tool input is treated as untrusted alert data; the model is instructed to ignore embedded instructions and ground claims in evidence.
- No tool can isolate a host, disable an account, or change a production system. A containment tool returns an unexecuted proposal requiring human approval.
- Mock data and a small hand-authored trace set cannot establish real-world precision, recall, or production readiness. A real deployment needs independently labeled representative data, calibration, drift monitoring, access controls, privacy review, durable audit logs, and human escalation.
- LLM outputs can be wrong or malformed; parse/shape checks and a reasoning-turn limit fail closed, but are not a substitute for security review.
- Never send sensitive production telemetry to a model endpoint without authorization and appropriate data protections.

## Project files

- `data/traces.jsonl`: 15 synthetic traces, five each for benign, suspicious, and malicious.
- `data/assets.jsonl`, `data/intel.jsonl`: local synthetic enrichment sources.
- `examples/alert.json`: sample alert input.
- `reports/`: generated evaluation and monitoring artifacts (after running evaluation).

## Assessment answers (edit to match your actual run)

- **Domain/goal:** SOC alert triage. Assess a structured alert, gather relevant local enrichment, explain a classification and severity, and recommend next steps while escalating uncertain or consequential decisions.
- **Assumptions/mock data:** All alerts, assets, and intelligence in `data/` are synthetic and authored for this prototype. No live organization data or external threat feed is used.
- **Test traces:** 15 authored examples with reference labels. The labels are assigned from the scenario evidence written into each synthetic alert. Run `sentinelloop evaluate`; report the resulting per-class precision/recall from `reports/evaluation.json` rather than assuming a score.
- **Production readiness:** Prototype only. No live response integrations; containment is approval-gated. Needs larger representative validation, calibration, monitoring, access/privacy controls, and analyst review.
- **Total time:** Enter your actual time spent; do not estimate from this README.
- **Own-work declaration:** Review the implementation, adapt it, and only confirm the form statement if it accurately reflects your submission and the assessment rules.

