# LLM Evaluation & Repository Validation Mini-Harness

A reproducible portfolio project for evaluating structured LLM-style outputs against explicit test cases. It uses saved examples, so no API key or network access is required.

## What it demonstrates
- A versioned JSON evaluation dataset
- A deterministic evaluator with explicit pass/fail criteria
- Validation of malformed JSON and missing fields
- Unit tests for normal behavior and edge cases
- A CLI report with per-case results and an overall pass rate
- GitHub Actions CI on pushes and pull requests

## Requirements
- Python 3.10+
- pytest

## Run locally (Windows Git Bash)
```bash
python -m pip install -r requirements.txt
python evaluate.py
python -m pytest -q
```

The CLI exits with code 1 if any evaluation case fails. The test command exits nonzero if a test fails.

## Evaluation contract
Each output must be a JSON object with non-empty string fields `label` and `answer`. Each dataset case defines an `expected_label` and zero or more `required_terms`. A case passes only if the output is valid JSON, has valid required fields, matches the expected label (case-insensitively), and contains all required terms in the answer (case-insensitively).

This is a transparent baseline rubric, not a full measure of semantic correctness, factuality, safety, or overall answer quality. Keyword matching can produce false positives and false negatives. Production evaluation should use a carefully designed dataset, human review or calibrated graders, and model/prompt version tracking.

## Structure
- `evaluator.py` — validation and scoring logic
- `evaluate.py` — CLI runner
- `dataset.json` — fixed example cases
- `tests/test_evaluator.py` — unit tests
- `.github/workflows/tests.yml` — CI workflow

## Reproducibility
These are deterministic fixtures, not live model generations. Do not claim that a real model was evaluated unless you add a model integration and actually run it.
