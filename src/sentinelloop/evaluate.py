from __future__ import annotations

from collections import Counter
from typing import Any


def evaluate_dataset(agent, rows: list[dict[str, Any]]) -> dict[str, Any]:
    labels = {"benign", "suspicious", "malicious"}
    matrix = Counter()
    predictions = []
    for row in rows:
        result = agent.analyze(row["alert"])
        truth = row["label"]
        predicted = str(result.get("classification", "unknown")).lower()
        if truth not in labels:
            raise ValueError(f"Unsupported ground-truth label: {truth}")
        matrix[(truth, predicted)] += 1
        predictions.append({"trace_id": row["id"], "expected": truth, "predicted": predicted,
                            "correct": truth == predicted, "severity": result.get("severity"),
                            "confidence": result.get("confidence"), "human_review": result.get("needs_human_review"),
                            "rationale": result.get("rationale"), "tool_calls": len(result.get("tool_audit", []))})
    total = len(predictions)
    correct = sum(x["correct"] for x in predictions)
    per_class = {}
    for label in sorted(labels):
        tp = matrix[(label, label)]
        fp = sum(matrix[(other, label)] for other in labels if other != label)
        fn = sum(matrix[(label, other)] for other in labels if other != label) + matrix[(label, "unknown")]
        per_class[label] = {"precision": tp / (tp + fp) if tp + fp else 0.0,
                            "recall": tp / (tp + fn) if tp + fn else 0.0,
                            "support": sum(1 for row in predictions if row["expected"] == label)}
    return {"model": agent.model, "dataset": "synthetic authored SOC traces", "total": total,
            "accuracy": correct / total if total else 0.0, "per_class": per_class,
            "confusion_matrix": {truth: {pred: matrix[(truth, pred)] for pred in sorted(labels)} for truth in sorted(labels)},
            "predictions": predictions,
            "limitations": ["Synthetic traces do not estimate real-world performance.",
                            "Small authored set; validate against a larger independently labeled corpus before deployment.",
                            "All containment remains a proposal and requires human approval."]}
