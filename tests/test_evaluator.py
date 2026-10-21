import json
from evaluator import evaluate_case, evaluate_dataset

def test_valid_case_passes():
    case = {"id":"valid", "expected_label":"support", "required_terms":["reset","password"],
            "output":json.dumps({"label":"Support","answer":"Reset your password here."})}
    result = evaluate_case(case)
    assert result.passed is True
    assert result.checks_passed == 3

def test_label_mismatch_fails():
    case = {"id":"label-mismatch", "expected_label":"policy", "required_terms":["refund"],
            "output":json.dumps({"label":"support","answer":"Refund details are here."})}
    result = evaluate_case(case)
    assert result.passed is False
    assert any("Label mismatch" in reason for reason in result.reasons)

def test_missing_required_term_fails():
    case = {"id":"missing-term", "expected_label":"support", "required_terms":["password","reset"],
            "output":json.dumps({"label":"support","answer":"Contact the help desk."})}
    result = evaluate_case(case)
    assert result.passed is False
    assert any("Missing required terms" in reason for reason in result.reasons)

def test_malformed_json_fails_safely():
    result = evaluate_case({"id":"broken-json","expected_label":"support","required_terms":[],"output":'{"label":'})
    assert result.passed is False
    assert "Output must be a JSON object." in result.reasons

def test_missing_fields_fails():
    result = evaluate_case({"id":"missing-fields","expected_label":"support","required_terms":[],
                            "output":json.dumps({"label":"support"})})
    assert result.passed is False
    assert any("non-empty string fields" in reason for reason in result.reasons)

def test_dataset_results_preserve_order():
    dataset = [
        {"id":"a","expected_label":"x","required_terms":[],"output":'{"label":"x","answer":"ok"}'},
        {"id":"b","expected_label":"x","required_terms":[],"output":"not json"}
    ]
    results = evaluate_dataset(dataset)
    assert [r.case_id for r in results] == ["a","b"]
    assert [r.passed for r in results] == [True,False]
