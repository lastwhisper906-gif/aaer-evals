"""api_client 스캐폴드 무호출 테스트 (freeze 개정 #3, D38) — 네트워크 0."""
import json
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import api_client  # noqa: E402
import cli_client  # noqa: E402


def _clean_env(monkeypatch):
    monkeypatch.delenv("AAER_RAW_API_APPROVED", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)


def test_guard_blocks_without_owner_switch(monkeypatch):
    """소유자 스위치 부재 → 호출 이전에 예외 (우발 종량 과금 차단)."""
    _clean_env(monkeypatch)
    with pytest.raises(RuntimeError, match="Q-R02"):
        api_client.assert_raw_api_approved()


def test_guard_blocks_without_key(monkeypatch):
    _clean_env(monkeypatch)
    monkeypatch.setenv("AAER_RAW_API_APPROVED", "1")
    with pytest.raises(RuntimeError, match="ANTHROPIC_API_KEY"):
        api_client.assert_raw_api_approved()


def test_call_model_api_refuses_before_approval(monkeypatch, tmp_path):
    """call_model_api도 첫 줄에서 가드 — 페이로드 송출·SDK import 이전."""
    _clean_env(monkeypatch)
    with pytest.raises(RuntimeError, match="미승인"):
        api_client.call_model_api("claude-sonnet-5", "sys", "{}", {"type": "object"},
                                  log_dir=tmp_path, log_name="t")


def test_payload_guard_is_frozen_reuse(monkeypatch, tmp_path):
    """가드 통과 후에도 동결 guard_payload가 금지 마커를 차단."""
    monkeypatch.setenv("AAER_RAW_API_APPROVED", "1")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-not-used")
    with pytest.raises(cli_client.PayloadGuardError):
        api_client.call_model_api(
            "claude-sonnet-5", "sys", '{"x": "beneish"}', {"type": "object"},
            log_dir=tmp_path, log_name="t",
            forbid_markers=cli_client.EVALUATEE_FORBIDDEN_MARKERS)


def test_callresult_interface_identical():
    """CallResult는 동결 cli_client의 것을 그대로 사용 — 인터페이스 동일성."""
    assert api_client.CallResult is cli_client.CallResult


# ── R2-3: 3채널 가드 패리티 (cli arm 거울 — payload·system·schema) ────────

GUARD_CHANNELS = ("user_payload", "system_prompt", "schema")


@pytest.mark.parametrize("channel", GUARD_CHANNELS)
def test_marker_in_any_channel_raises_before_sdk_import(monkeypatch, tmp_path, channel):
    """마커가 어느 채널에 있어도 SDK import 이전 PayloadGuardError —
    anthropic 미설치(INV-11) 환경에서 ImportError가 아닌 가드 예외가 그 증거."""
    monkeypatch.setenv("AAER_RAW_API_APPROVED", "1")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-not-used")
    args = {"user_payload": '{"revenue": 100}', "system_prompt": "SYSTEM",
            "schema": {"type": "object"}}
    if channel == "schema":
        args["schema"] = {"type": "object", "description": "beneish rubric"}
    else:
        args[channel] = args[channel] + " beneish"
    with pytest.raises(cli_client.PayloadGuardError):
        api_client.call_model_api(
            "claude-sonnet-5", args["system_prompt"], args["user_payload"],
            args["schema"], log_dir=tmp_path, log_name="t",
            forbid_markers=cli_client.EVALUATEE_FORBIDDEN_MARKERS)


# ── R2-3: runner_api composed 기록 재검증·카나리 runmeta (runner 거울) ────

def _api_result(structured):
    from types import SimpleNamespace
    return SimpleNamespace(ok=True, structured=structured, fail_reason=None,
                           served_models=["claude-sonnet-5"])


def _stub_payload():
    return {"_k_internal": 1.0, "_variant": "original",
            "case": {"company_name": "Example", "ticker": "EX"},
            "financial_series_point_in_time": {
                "Revenue": [{"accession": "a", "form": "10-K", "filed": "2020-01-01"}]},
            "filing_chronology": []}


def _run_case_api(monkeypatch, tmp_path, structured):
    import copy
    import runner_api
    monkeypatch.setattr(runner_api.bp, "build_payload",
                        lambda case, perturb: copy.deepcopy(_stub_payload()))
    monkeypatch.setattr(runner_api, "call_model_api",
                        lambda *a, **k: _api_result(structured))
    monkeypatch.setattr(runner_api, "freeze_state", lambda: {"head": "a" * 40})
    case = {"case_id": "case_99", "company_name": "Example", "ticker": "EX",
            "cik": "1", "cutoff_date": "2020-01-01"}
    out_dir, log_dir = tmp_path / "runs", tmp_path / "logs"
    result = runner_api.run_case_api(case, False, out_dir, log_dir, None)
    return result, out_dir / "case_99.json", log_dir / "runmeta_api_original_case_99.json"


def _valid_model_output():
    evidence = {"quote": "Revenue=1 (FY2020)", "source_accession_no": "a",
                "location": "Revenue FY2020"}
    return {"checklist": [{"item_id": "CL1", "question": "q", "finding": "no_flag",
                           "confidence": "low", "evidence": [evidence]}],
            "misstatement_probability": 20, "mechanism_hypotheses": [],
            "overall": {"risk_tier": "clear", "top_signals": []}}


def test_runner_api_schema_invalid_composed_record_not_written(monkeypatch, tmp_path):
    bad = _valid_model_output()
    bad["misstatement_probability"] = 130
    result, out_path, meta_path = _run_case_api(monkeypatch, tmp_path, bad)
    assert result["status"] == "FAIL (schema_violation: misstatement_probability)"
    assert not out_path.exists(), "스키마 무효 composed 기록이 기록됨"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    assert meta["fail_reason"] == "schema_violation: misstatement_probability"


def test_runner_api_canary_hit_recorded_in_runmeta(monkeypatch, tmp_path):
    hit = _valid_model_output()
    hit["overall"]["top_signals"] = ["canary 9fa11f98-dead-beef"]
    result, out_path, meta_path = _run_case_api(monkeypatch, tmp_path, hit)
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    assert meta["canary_hit"] is True


def test_runner_api_valid_record_written_and_passes(monkeypatch, tmp_path):
    result, out_path, meta_path = _run_case_api(monkeypatch, tmp_path,
                                                _valid_model_output())
    assert result["status"].startswith("OK p=20")
    assert out_path.exists()
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    assert meta["canary_hit"] is False
