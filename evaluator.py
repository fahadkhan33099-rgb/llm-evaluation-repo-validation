"""Deterministic evaluation for structured LLM-style response fixtures."""
from __future__ import annotations
import json
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class EvaluationResult:
    case_id: str
    passed: bool
    checks_passed: int
    checks_total: int
    reasons: tuple[str, ...]

def evaluate_case(case: dict[str, Any]) -> EvaluationResult:
    """Evaluate one case using JSON validity, required fields, and rubric checks."""
    case_id = str(case.get("id", "unknown"))
    reasons: list[str] = []
    checks_total = 3
    checks_passed = 0

    raw_output = case.get("output")
    try:
        parsed = json.loads(raw_output) if isinstance(raw_output, str) else None
    except (json.JSONDecodeError, TypeError):
        parsed = None

    if not isinstance(parsed, dict):
        return EvaluationResult(case_id, False, 0, checks_total, ("Output must be a JSON object.",))
    checks_passed += 1

    label, answer = parsed.get("label"), parsed.get("answer")
    if not (isinstance(label, str) and label.strip() and isinstance(answer, str) and answer.strip()):
        return EvaluationResult(case_id, False, checks_passed, checks_total,
                                ("JSON must contain non-empty string fields 'label' and 'answer'.",))
    checks_passed += 1

    expected_label = case.get("expected_label")
    label_ok = isinstance(expected_label, str) and label.casefold() == expected_label.casefold()
    required_terms = case.get("required_terms", [])
    if not isinstance(required_terms, list) or not all(isinstance(term, str) for term in required_terms):
        return EvaluationResult(case_id, False, checks_passed, checks_total,
                                ("'required_terms' must be a list of strings.",))
    missing = [term for term in required_terms if term.casefold() not in answer.casefold()]

    if not label_ok:
        reasons.append(f"Label mismatch: expected {expected_label!r}, got {label!r}.")
    if missing:
        reasons.append("Missing required terms: " + ", ".join(repr(term) for term in missing) + ".")
    if label_ok and not missing:
        checks_passed += 1
    return EvaluationResult(case_id, checks_passed == checks_total, checks_passed, checks_total, tuple(reasons))

def evaluate_dataset(dataset: list[dict[str, Any]]) -> list[EvaluationResult]:
    """Evaluate every case in dataset order."""
    return [evaluate_case(case) for case in dataset]
