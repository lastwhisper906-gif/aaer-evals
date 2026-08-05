import copy
import json
from pathlib import Path

from jsonschema import Draft7Validator

from aaer_eval.output_contract_v2 import validate_v2


ROOT = Path(__file__).resolve().parents[1]
V1_PATH = ROOT / "schemas" / "llm_output.json"
V2_PATH = ROOT / "schemas" / "llm_output_v2.json"
OLD_NAME = "misstatement_probability"
NEW_NAME = "misstatement_risk_score"
IDS = [f"CL{index}" for index in range(1, 9)]


def _load(path):
    return json.loads(path.read_text(encoding="utf-8"))


# Supersedes the v2.0 rename-only structural diff lock: D-P73 Phase 2 now
# intentionally requires v2.1 hard constraints beyond the authorized rename.
def test_v2_1_schema_hard_constraints():
    schema = _load(V2_PATH)
    meta = schema["$defs"]["pipeline_meta"]
    output = schema["$defs"]["model_output"]["properties"]
    checklist = output["checklist"]

    assert schema["description"].startswith("v2.1 (D-P73 Phase 2")
    assert "primary metrics: AUC, permutation, rank correlation" in schema["description"]
    assert "ECE/Brier not computed for v2 outputs (D-P73)" in schema["description"]
    assert "fingerprint" in schema["required"]
    assert "fingerprint" in meta["required"]
    assert meta["properties"]["case_id"]["pattern"] == "^case_[0-9]{2}$"
    assert meta["properties"]["pipeline_version"]["pattern"] == "^[0-9a-f]{7,40}$"
    assert meta["properties"]["fingerprint"]["properties"]["pipeline_commit"]["pattern"] == "^[0-9a-f]{7,40}$"
    assert meta["properties"]["documents_used"]["items"]["properties"]["accession_no"]["pattern"] == "^[0-9]{10}-[0-9]{2}-[0-9]{6}$"
    assert checklist["minItems"] == checklist["maxItems"] == 8
    assert checklist["items"]["properties"]["item_id"]["enum"] == IDS
    assert output["overall"]["properties"]["top_signals"]["items"]["enum"] == IDS
    Draft7Validator.check_schema(schema)


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


def _record(score=50, tier="watch"):
    accession = "0000000000-00-000001"
    checklist = []
    for item_id in IDS:
        checklist.append({
            "item_id": item_id,
            "question": "closed question",
            "finding": "no_flag",
            "confidence": "high",
            "evidence": [{
                "quote": "Metric=1 (FY2025)",
                "source_accession_no": accession,
                "location": "Metric FY2025",
            }],
        })
    return {
        "case_id": "case_01",
        "run_id": "run-1",
        "model": "model-1",
        "pipeline_version": "abcdef0",
        "run_timestamp": "2026-08-05T00:00:00Z",
        "documents_used": [{
            "accession_no": accession,
            "form_type": "10-K",
            "filing_date": "2026-08-04",
        }],
        "fingerprint": {
            "case_input_sha256": "x", "payload_sha256": "x",
            "system_prompt_sha256": "x", "schema_sha256": "x",
            "model_requested": "model-1", "harness_version_actual": "1",
            "pipeline_commit": "abcdef0",
        },
        "checklist": checklist,
        "misstatement_risk_score": score,
        "mechanism_hypotheses": [{
            "affected_line_items": ["Revenue"],
            "direction": "timing_shift",
            "accounting_treatment": "recognition timing",
            "rationale_evidence": [{
                "quote": "Metric=1 (FY2025)",
                "source_accession_no": accession,
                "location": "Metric FY2025",
            }],
        }],
        "overall": {"risk_tier": tier, "top_signals": ["CL1"]},
    }


def test_valid_record_passes_schema_and_semantics():
    record = _record()
    assert list(Draft7Validator(_load(V2_PATH)).iter_errors(record)) == []
    assert validate_v2(record) == []


def test_computed_evidence_passes_schema():
    record = _record()
    evidence = record["checklist"][0]["evidence"][0]
    evidence["source_accession_no"] = "computed"
    evidence["computed_by"] = "python"
    assert list(Draft7Validator(_load(V2_PATH)).iter_errors(record)) == []


def test_v2_mechanism_hypothesis_trigger_uses_risk_score():
    validator = Draft7Validator(_load(V2_PATH))
    low_record = _record(30)
    low_record["mechanism_hypotheses"] = []
    assert list(validator.iter_errors(low_record)) == []

    triggered_record = _record(45)
    triggered_record["mechanism_hypotheses"] = []
    errors = list(validator.iter_errors(triggered_record))
    assert errors
    assert any(
        list(error.absolute_path) == ["mechanism_hypotheses"] for error in errors
    )


def test_missing_checklist_id_fires():
    record = _record()
    record["checklist"][-1]["item_id"] = "CL7"
    assert any("exactly" in error for error in validate_v2(record))


def test_duplicate_checklist_id_fires():
    record = _record()
    record["checklist"][-1]["item_id"] = "CL1"
    assert any("each appear once" in error for error in validate_v2(record))


def test_seven_item_list_fails_schema():
    record = _record()
    record["checklist"].pop()
    assert list(Draft7Validator(_load(V2_PATH)).iter_errors(record))


def test_nine_item_list_fails_schema():
    record = _record()
    record["checklist"].append(copy.deepcopy(record["checklist"][0]))
    assert list(Draft7Validator(_load(V2_PATH)).iter_errors(record))


def test_high_score_requires_elevated_tier():
    assert any("requires elevated" in error for error in validate_v2(_record(70, "watch")))


def test_low_score_forbids_elevated_tier():
    assert any("forbids elevated" in error for error in validate_v2(_record(39, "elevated")))


def test_top_signal_must_appear_in_checklist():
    record = _record()
    record["checklist"][-1]["item_id"] = "CL7"
    record["overall"]["top_signals"] = ["CL8"]
    assert any("top_signals" in error for error in validate_v2(record))


def test_fingerprint_absent_fails_schema():
    record = _record()
    del record["fingerprint"]
    errors = list(Draft7Validator(_load(V2_PATH)).iter_errors(record))
    assert any("fingerprint" in error.message for error in errors)
