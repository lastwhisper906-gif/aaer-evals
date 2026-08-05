import copy
import json
from pathlib import Path

from jsonschema import Draft7Validator


ROOT = Path(__file__).resolve().parents[1]
V1_PATH = ROOT / "schemas" / "llm_output.json"
V2_PATH = ROOT / "schemas" / "llm_output_v2.json"
OLD_NAME = "misstatement_probability"
NEW_NAME = "misstatement_risk_score"
V2_HEADER = (
    "v2 (D-P44a/D-P45, 2026-08-05): misstatement_probability → "
    "misstatement_risk_score 서수 개명 — v1.2는 wave-1/2 비교가능성을 위해 "
    "동결; 채택은 차기 FREEZE_REV에서. "
)
# The explicit vocabulary-ban criterion requires a probability-free equivalent.
RISK_DESCRIPTION = (
    "0–100 서수(ordinal) 위험 순위 — 보정된 발생 가능성 수치가 아니다. "
    "피평가자 노출 명칭은 중립(‘misstatement’), fraud 어휘 금지 (red-team #1)"
)


def _load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def _rename_tree(value):
    if isinstance(value, dict):
        return {
            key.replace(OLD_NAME, NEW_NAME): _rename_tree(child)
            for key, child in value.items()
        }
    if isinstance(value, list):
        return [_rename_tree(child) for child in value]
    if isinstance(value, str):
        return value.replace(OLD_NAME, NEW_NAME)
    return value


def _first_difference(expected, actual, path=""):
    if type(expected) is not type(actual):
        return path or "/"
    if isinstance(expected, dict):
        if expected.keys() != actual.keys():
            differing = sorted(expected.keys() ^ actual.keys())
            return f"{path}/{differing[0]}"
        for key in expected:
            difference = _first_difference(
                expected[key], actual[key], f"{path}/{key.replace('~', '~0').replace('/', '~1')}"
            )
            if difference:
                return difference
        return None
    if isinstance(expected, list):
        if len(expected) != len(actual):
            return path or "/"
        for index, (expected_item, actual_item) in enumerate(zip(expected, actual)):
            difference = _first_difference(
                expected_item, actual_item, f"{path}/{index}"
            )
            if difference:
                return difference
        return None
    return None if expected == actual else (path or "/")


def test_v2_diff_is_limited_to_authorized_changes():
    v1 = _load(V1_PATH)
    v2 = _load(V2_PATH)
    expected = _rename_tree(copy.deepcopy(v1))
    expected["description"] = V2_HEADER + expected["description"].replace(
        "status: v1.2", "status: v2.0", 1
    )
    expected["$defs"]["model_output"]["properties"][NEW_NAME][
        "description"
    ] = RISK_DESCRIPTION

    difference = _first_difference(expected, v2)
    assert difference is None, f"unauthorized v2 schema difference at {difference}"


def test_v1_contract_keeps_original_field_name():
    source = V1_PATH.read_text(encoding="utf-8")
    assert OLD_NAME in source
    assert "risk_score" not in source


def test_v2_schema_and_risk_description_hygiene():
    schema = _load(V2_PATH)
    description = schema["$defs"]["model_output"]["properties"][NEW_NAME][
        "description"
    ]
    assert "ordinal" in description or "서수" in description
    assert "확률" not in description
    assert "probability" not in description.lower()
    Draft7Validator.check_schema(schema)


def _minimal_instance(score):
    return {
        "case_id": "case-1",
        "run_id": "run-1",
        "model": "model-1",
        "pipeline_version": "commit-1",
        "run_timestamp": "2026-08-05T00:00:00Z",
        "documents_used": [
            {
                "accession_no": "0000000000-00-000001",
                "form_type": "10-K",
                "filing_date": "2026-08-04",
            }
        ],
        "checklist": [
            {
                "item_id": "item-1",
                "question": "닫힌 질문",
                "finding": "no_flag",
                "confidence": "high",
                "evidence": [
                    {
                        "quote": "Metric=1 (FY2025)",
                        "source_accession_no": "0000000000-00-000001",
                        "location": "Metric FY2025",
                    }
                ],
            }
        ],
        NEW_NAME: score,
        "mechanism_hypotheses": [],
        "overall": {"risk_tier": "watch", "top_signals": []},
    }


def test_v2_mechanism_hypothesis_trigger_uses_risk_score():
    validator = Draft7Validator(_load(V2_PATH))
    assert list(validator.iter_errors(_minimal_instance(30))) == []

    errors = list(validator.iter_errors(_minimal_instance(45)))
    assert errors
    assert any(list(error.absolute_path) == ["mechanism_hypotheses"] for error in errors)
