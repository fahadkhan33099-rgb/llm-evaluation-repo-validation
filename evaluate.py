"""Run the bundled evaluation dataset and print a compact report."""
import json
from pathlib import Path
from evaluator import evaluate_dataset

def main() -> int:
    dataset = json.loads(Path("dataset.json").read_text(encoding="utf-8"))
    if not isinstance(dataset, list):
        raise ValueError("dataset.json must contain a JSON list of cases")
    results = evaluate_dataset(dataset)
    for result in results:
        status = "PASS" if result.passed else "FAIL"
        print(f"{status} {result.case_id} ({result.checks_passed}/{result.checks_total} checks)")
        for reason in result.reasons:
            print(f"  - {reason}")
    passed = sum(result.passed for result in results)
    total = len(results)
    rate = passed / total * 100 if total else 0.0
    print(f"\nEvaluation summary: {passed}/{total} passed ({rate:.1f}%)")
    return 0 if total > 0 and passed == total else 1

if __name__ == "__main__":
    raise SystemExit(main())
