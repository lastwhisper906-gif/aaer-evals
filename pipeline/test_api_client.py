"""api_client 스캐폴드 무호출 테스트 (freeze 개정 #3, D38) — 네트워크 0."""
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
