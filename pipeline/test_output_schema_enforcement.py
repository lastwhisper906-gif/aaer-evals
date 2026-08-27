import copy
import json
from pathlib import Path
from types import SimpleNamespace

import jsonschema
import pytest

import runner


REPO_ROOT = Path(__file__).resolve().parent.parent


def _evidence():
    return {"quote": "Revenue=1 (FY2020)", "source_accession_no": "a", "location": "Revenue FY2020"}


def _hypothesis():
    return {
        "affected_line_items": ["Revenue"],
        "direction": "overstated",
        "accounting_treatment": "recognition timing",
        "rationale_evidence": [_evidence()],
    }


def _model_output():
    return {
        "checklist": [{
            "item_id": "CL1", "question": "q", "finding": "no_flag", "confidence": "low",
            "evidence": [_evidence()],
        }],
        "misstatement_probability": 20,
        "mechanism_hypotheses": [_hypothesis()],
        "overall": {"risk_tier": "clear", "top_signals": []},
    }


def _full_output(model_output):
    return {
        "case_id": "case_99", "run_id": "original-case_99-r1", "model": "claude-sonnet-5",
        "pipeline_version": "a" * 40, "run_timestamp": "2026-07-21T00:00:00+00:00",
        "documents_used": [{"accession_no": "a", "form_type": "10-K", "filing_date": "2020-01-01"}],
        **model_output,
    }


@pytest.fixture(params=["probability", "empty_evidence", "four_hypotheses", "conditional"])
def invalid_model_output(request):
    output = _model_output()
    if request.param == "probability":
        output["misstatement_probability"] = 130
    elif request.param == "empty_evidence":
        output["checklist"][0]["evidence"] = []
    elif request.param == "four_hypotheses":
        output["mechanism_hypotheses"] = [_hypothesis() for _ in range(4)]
    else:
        output["misstatement_probability"] = 55
        output["mechanism_hypotheses"] = []
    return output


def test_invalid_outputs_rejected_by_model_and_full_schemas(invalid_model_output):
    assert list(jsonschema.Draft7Validator(runner.MODEL_SCHEMA).iter_errors(invalid_model_output))
    assert list(jsonschema.Draft7Validator(runner.FULL_OUTPUT_SCHEMA).iter_errors(
        _full_output(invalid_model_output)))


def test_model_schema_is_derived_with_all_constraints():
    schema = runner.derive_model_schema(runner.FULL_OUTPUT_SCHEMA)
    properties = schema["properties"]
    assert properties["misstatement_probability"]["minimum"] == 0
    assert properties["misstatement_probability"]["maximum"] == 100
    assert properties["mechanism_hypotheses"]["maxItems"] == 3
    assert properties["checklist"]["minItems"] == 1
    assert properties["checklist"]["items"]["properties"]["evidence"]["minItems"] == 1
    assert properties["mechanism_hypotheses"]["items"]["properties"]["rationale_evidence"]["minItems"] == 1
    assert schema["allOf"][0]["if"]["properties"]["misstatement_probability"]["minimum"] == 40
    assert schema["allOf"][0]["then"]["properties"]["mechanism_hypotheses"]["minItems"] == 1


def test_run_case_revalidates_before_write(monkeypatch, tmp_path):
    invalid = _model_output()
    invalid["misstatement_probability"] = 130
    payload = {
        "_k_internal": 1.0,
        "_variant": "original",
        "case": {"company_name": "Example", "ticker": "EX"},
        "financial_series_point_in_time": {
            "Revenue": [{"accession": "a", "form": "10-K", "filed": "2020-01-01"}]
        },
        "filing_chronology": [],
    }
    monkeypatch.setattr(runner.bp, "build_payload", lambda case, perturb: copy.deepcopy(payload))
    monkeypatch.setattr(runner.cli_client, "call_model", lambda *args, **kwargs: SimpleNamespace(
        ok=True, structured=invalid, fail_reason=None, served_models=[runner.EVALUATEE_MODEL]))
    monkeypatch.setattr(runner, "freeze_state", lambda: {"head": "a" * 40})
    out_dir = tmp_path / "runs"
    log_dir = tmp_path / "logs"
    log_dir.mkdir()
    case = {"case_id": "case_99", "company_name": "Example", "ticker": "EX",
            "cik": "1", "cutoff_date": "2020-01-01"}

    result = runner.run_case(case, False, out_dir, log_dir)

    assert result["status"] == "FAIL (schema_violation: misstatement_probability)"
    assert not (out_dir / "case_99.json").exists()
    meta = json.loads((log_dir / "runmeta_original_case_99.json").read_text(encoding="utf-8"))
    assert meta["fail_reason"] == "schema_violation: misstatement_probability"


def test_date_format_enforced_by_runner_and_output_validity(monkeypatch, tmp_path):
    payload = {
        "_k_internal": 1.0,
        "_variant": "original",
        "case": {"company_name": "Example", "ticker": "EX"},
        "financial_series_point_in_time": {
            "Revenue": [{"accession": "a", "form": "10-K", "filed": "not-a-date"}]
        },
        "filing_chronology": [],
    }
    monkeypatch.setattr(runner.bp, "build_payload", lambda case, perturb: copy.deepcopy(payload))
    monkeypatch.setattr(runner.cli_client, "call_model", lambda *args, **kwargs: SimpleNamespace(
        ok=True, structured=_model_output(), fail_reason=None,
        served_models=[runner.EVALUATEE_MODEL]))
    monkeypatch.setattr(runner, "freeze_state", lambda: {"head": "a" * 40})
    case = {"case_id": "case_99", "company_name": "Example", "ticker": "EX",
            "cik": "1", "cutoff_date": "2020-01-01"}
    log_dir = tmp_path / "logs"
    log_dir.mkdir()

    bad_output = _full_output(_model_output())
    bad_output["documents_used"][0]["filing_date"] = "not-a-date"
    assert not list(jsonschema.Draft7Validator(
        runner.FULL_OUTPUT_SCHEMA).iter_errors(bad_output))
    output_path = tmp_path / "output.json"
    output_path.write_text(json.dumps(bad_output), encoding="utf-8")

    bad_result = runner.run_case(case, False, tmp_path / "bad-runs", log_dir)
    assert bad_result["status"] == "FAIL (schema_violation: documents_used.0.filing_date)"
    assert not runner.cli_client.output_is_valid(output_path, runner.FULL_OUTPUT_SCHEMA)

    payload["financial_series_point_in_time"]["Revenue"][0]["filed"] = "2020-01-01"
    good_output = _full_output(_model_output())
    output_path.write_text(json.dumps(good_output), encoding="utf-8")

    good_result = runner.run_case(case, False, tmp_path / "good-runs", log_dir)
    assert good_result["status"].startswith("OK p=")
    assert runner.cli_client.output_is_valid(output_path, runner.FULL_OUTPUT_SCHEMA)


# R2-2: 쓰기 시점 검증(e1a5…) 이전에 커밋된 draw 기록 15건 — 스키마 위반이
# 알려진 채 동결됨(수정 금지, INV-06). 경로 + 실패 키워드를 명시 열거:
# 새 위반 기록(16번째)은 이 목록에 없으므로 스위프가 잡는다. 특성화는
# DECISIONS_PENDING.md DRAFT(ERRATA 후보) 참조 — 하류 소비는 스키마 유효한
# misstatement_probability 필드뿐.
PREVALIDATION_ALLOWLIST = {
    "runs/draw_k3/w1_controls/draw_2/case_24.json": "top_signals",
    "runs/draw_k3/w1_controls/draw_2/case_37.json": "top_signals",
    "runs/draw_k3/wave2/draw_2/case_45.json": "top_signals",
    "runs/draw_k3/wave2/draw_3/case_67.json": "evidence",
    "runs/hardening/draws/draw_3/case_14.json": "top_signals",
    "runs/hardening/draws/draw_4/case_12.json": "top_signals",
    "runs/hardening/draws/draw_5/case_12.json": "top_signals",
    "runs/hardening/draws/draw_5/case_13.json": "top_signals",
    "runs/holdout/mainscore_redraw/draw_5/case_73.json": "top_signals",
    "runs/rp07/draws/draw_3/case_08.json": "top_signals",
    "runs/rp07/draws/draw_3/case_12.json": "top_signals",
    "runs/rp07/draws/draw_5/case_09.json": "top_signals",
    "runs/rp07/draws/draw_5/case_12.json": "top_signals",
    "runs/wave2/perturbed_redraw/draw_2/case_66.json": "top_signals",
    "runs/wave2/perturbed_redraw/draw_3/case_66.json": "top_signals",
}


def _llm_output_shaped_paths(root=REPO_ROOT):
    paths = set()
    for base in ("runs", "pilot"):
        for path in (root / base).rglob("*.json"):
            if ".fp-" in path.name:  # R2-5: stale-superseded fp-sibling 제외
                continue
            try:
                doc = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            if isinstance(doc, dict) and "misstatement_probability" in doc \
                    and "checklist" in doc:
                paths.add(path)
    return sorted(paths)


def test_all_committed_run_outputs_validate():
    paths = _llm_output_shaped_paths()
    assert len(paths) > 400, "스위프가 draw 트리를 놓침 — 발견 회귀"
    validator = jsonschema.Draft7Validator(
        runner.FULL_OUTPUT_SCHEMA, format_checker=jsonschema.FormatChecker())
    failures = []
    seen_allowlisted = {}
    for path in paths:
        relative = path.relative_to(REPO_ROOT).as_posix()
        errors = list(validator.iter_errors(json.loads(path.read_text(encoding="utf-8"))))
        if relative in PREVALIDATION_ALLOWLIST:
            seen_allowlisted[relative] = errors
            continue
        if errors:
            failures.append(f"{relative}: {errors[0].message}")
    assert not failures, "\n".join(failures)
    # 열거된 15건은 존재해야 하고(동결 확인), 기재된 이유로 실패해야 한다 —
    # 다른 이유의 새 위반이 허용목록 뒤에 숨지 못하게.
    assert set(seen_allowlisted) == set(PREVALIDATION_ALLOWLIST), \
        "허용목록 기재 기록이 트리에 없거나 스위프가 발견하지 못함"
    for relative, keyword in PREVALIDATION_ALLOWLIST.items():
        errors = seen_allowlisted[relative]
        assert errors and keyword in errors[0].json_path, \
            f"{relative}: 기재 이유({keyword}) 외의 스키마 상태"


# ── evaluatee_input 화이트리스트의 송출 지점 강제 (R1-5) ──────────────────

def test_ground_truth_field_blocked_before_model_call(monkeypatch, tmp_path):
    """오염된 케이스 파일의 ground-truth 필드는 call_model 도달 전에 차단."""
    calls = []
    monkeypatch.setattr(runner.cli_client, "call_model",
                        lambda *a, **k: calls.append(1))
    case = {"case_id": "case_98", "company_name": "Example", "ticker": "EX",
            "cik": "1", "cutoff_date": "2020-01-01",
            "first_revelation_date": "2021-05-01"}
    with pytest.raises(runner.bp.CaseWhitelistError):
        runner.run_case(case, False, tmp_path / "runs", tmp_path / "logs")
    assert calls == [], "화이트리스트 위반 케이스가 모델 호출에 도달"


@pytest.mark.parametrize("extra", ["group", "revelation_source", "scheme_summary"])
def test_whitelist_rejects_each_ground_truth_key(extra):
    case = {"case_id": "case_98", "company_name": "Example", "ticker": "EX",
            "cik": "1", "cutoff_date": "2020-01-01", extra: "x"}
    with pytest.raises(runner.bp.CaseWhitelistError):
        runner.bp.assert_case_whitelisted(case)


def test_whitelist_rejects_missing_required_and_accepts_exact_contract():
    with pytest.raises(runner.bp.CaseWhitelistError):
        runner.bp.assert_case_whitelisted({"case_id": "case_98"})
    runner.bp.assert_case_whitelisted(
        {"case_id": "case_98", "company_name": "Example", "ticker": "EX",
         "cik": "1", "cutoff_date": "2020-01-01"})
