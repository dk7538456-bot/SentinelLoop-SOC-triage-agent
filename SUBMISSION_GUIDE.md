# Form response notes

Use these only after you have reviewed the code and performed the run yourself. Replace bracketed or run-dependent information with what actually happened.

## Domain / goal

SOC alert triage: the agent inspects a structured security alert, chooses local enrichment tools when useful, and returns an evidence-backed classification, severity, and recommended next steps. Any containment remains a human-reviewed proposal.

## Assumptions / mock data

All alerts, inventory records, and threat-feed entries are synthetic and included in the repository. The prototype assumes a single JSON alert and an OpenAI-compatible LLM endpoint. It does not ingest live telemetry or execute response actions.

## Total time spent

Enter your actual total time in hours: **[fill in honestly]**.

## Synthetic / test traces

Upload `data/traces.jsonl`. It contains 15 manually authored scenarios, five per reference class (benign, suspicious, malicious). Labels are assigned from the evidence stated in each scenario; they are teaching examples, not independently adjudicated production data.

## Monitoring report / dashboard

Configure the model, run `sentinelloop evaluate`, then upload the generated `reports/dashboard.html` (or the `reports/evaluation.json` report if the form accepts JSON). The run calculates metrics from actual model predictions. Do not upload an unrun template or claim metrics before you have executed it.

## Write-up

The approach uses a bounded LLM tool-use loop. The model selects read-only mock enrichment tools, returns a JSON assessment, and leaves consequential response proposals for human approval. The evaluator computes accuracy, class-wise precision/recall, and a confusion matrix on a small synthetic trace set. Precision/recall from this set are only a smoke-test signal; the set is too small and synthetic to support production claims. Production readiness would require representative independently labeled data, calibration, drift monitoring, secure logging, access and privacy controls, and analyst oversight.

## How traces were generated / labeled

The 15 traces were authored as synthetic, self-contained scenarios and assigned reference labels based on the described evidence and context. They contain no real person, customer, host, or threat-intelligence data. Because the examples are hand-authored and few, the resulting metrics can be optimistic and should not be generalized.

## Original work confirmation

The project files here were authored for this request. Review, understand, and adapt the work before submission. Only select the form's own-work confirmation if you can truthfully make that declaration under the assessment rules.
