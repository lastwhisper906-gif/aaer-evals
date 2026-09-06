import copy
import hashlib
import json
from types import SimpleNamespace

import runner


CASE = {"case_id": "case_99", "company_name": "Example", "ticker": "EX",
        "cik": "1", "cutoff_date": "2020-01-01"}
PAYLOAD = {
    "_k_internal": 1.0,
    "_variant": "original",
    "case": {"company_name": "Example", "ticker": "EX"},
    "financial_series_point_in_time": {
        "Revenue": [{"accession": "a", "form": "10-K", "filed": "2020-01-01"}]
    },
    "filing_chronology": [],
}
MODEL_OUTPUT = {
    "checklist": [{
        "item_id": "CL1", "question": "q", "finding": "no_flag", "confidence": "low",
        "evidence": [{"quote": "Revenue=1 (FY2020)", "source_accession_no": "a",
                      "location": "Revenue FY2020"}],
    }],
    "misstatement_probability": 20,
    "mechanism_hypotheses": [],
    "overall": {"risk_tier": "clear", "top_signals": []},
}


def _setup(monkeypatch):
    monkeypatch.setattr(runner.bp, "build_payload",
                        lambda case, perturb: copy.deepcopy(PAYLOAD))
    monkeypatch.setattr(runner, "freeze_state", lambda: {"head": "a" * 40})
    monkeypatch.setattr(runner, "get_harness_version", lambda: "claude-test")


def _call_result():
    return SimpleNamespace(ok=True, structured=copy.deepcopy(MODEL_OUTPUT), fail_reason=None,
                           served_models=[runner.EVALUATEE_MODEL])


def _run(monkeypatch, tmp_path, call_model=None, *, accept_legacy_output=False):
    _setup(monkeypatch)
    monkeypatch.setattr(runner.cli_client, "call_model", call_model or (lambda *a, **k: _call_result()))
    out_dir = tmp_path / "runs"
    log_dir = tmp_path / "logs"
    log_dir.mkdir(exist_ok=True)
    result = runner.run_case(
        CASE, False, out_dir, log_dir, accept_legacy_output=accept_legacy_output)
    return result, out_dir


def _run_with_payload(monkeypatch, tmp_path, payload, call_model=None, *,
                      head="a" * 40, harness="claude-test"):
    """R13-2: 구성(payload)만 바꾸거나 출처(head·harness)만 바꾼 재실행.

    `_run`은 매번 `_setup`으로 PAYLOAD·head·harness를 되돌리므로, 그 셋 중
    하나를 바꾸는 케이스는 반드시 이쪽을 써야 한다 (되돌려진 채 통과하면
    변별력 없는 테스트가 된다).
    """
    _setup(monkeypatch)
    monkeypatch.setattr(runner.bp, "build_payload",
                        lambda case, perturb: copy.deepcopy(payload))
    monkeypatch.setattr(runner, "freeze_state", lambda: {"head": head})
    monkeypatch.setattr(runner, "get_harness_version", lambda: harness)
    monkeypatch.setattr(runner.cli_client, "call_model",
                        call_model or (lambda *a, **k: _call_result()))
    out_dir = tmp_path / "runs"
    log_dir = tmp_path / "logs"
    log_dir.mkdir(exist_ok=True)
    return runner.run_case(CASE, False, out_dir, log_dir), out_dir


def _never_called(*args, **kwargs):
    raise AssertionError("call_model must not be called")


def test_identical_fingerprint_skips(monkeypatch, tmp_path):
    _, out_dir = _run(monkeypatch, tmp_path)
    result, _ = _run(monkeypatch, tmp_path, _never_called)
    assert result["status"].startswith("skip")


def test_changed_prompt_writes_versioned_sibling_without_touching_original(monkeypatch, tmp_path):
    _, out_dir = _run(monkeypatch, tmp_path)
    original = out_dir / "case_99.json"
    original_bytes = original.read_bytes()
    monkeypatch.setattr(runner, "TASK", runner.TASK + "\nChanged instruction.")

    result, _ = _run(monkeypatch, tmp_path)

    assert "stale-superseding" in result["status"]
    assert original.read_bytes() == original_bytes
    siblings = list(out_dir.glob("case_99.fp-*.json"))
    assert len(siblings) == 1
    assert json.loads(siblings[0].read_text())["fingerprint"]["system_prompt_sha256"] != \
        json.loads(original.read_text())["fingerprint"]["system_prompt_sha256"]


def test_in_window_commit_does_not_break_resume(monkeypatch, tmp_path):
    """R13-2(a): 창 중간에 HEAD만 움직인 재개는 여전히 멱등이어야 한다.

    종전(전체 fingerprint 동등 비교)에는 완료분 전건이 재호출되어
    fp-sibling으로 떨어지고, forward_assemble이 "어느 런이 정본인지 모호"로
    조립을 거부했다 — 창을 잃는 교착. 변이: runner.py의 skip 판정을
    `existing.get("fingerprint") == fingerprint`로 되돌리면 red.
    """
    _, out_dir = _run(monkeypatch, tmp_path)
    original = out_dir / "case_99.json"
    original_bytes = original.read_bytes()

    # 창 중간 커밋 = pipeline_commit만 바뀐 상태 (출처 필드, 구성 정체 아님)
    result, _ = _run_with_payload(monkeypatch, tmp_path, PAYLOAD, _never_called,
                                  head="b" * 40)

    assert result["status"].startswith("skip")
    assert not list(out_dir.glob("case_99.fp-*.json"))
    assert original.read_bytes() == original_bytes


def test_harness_version_change_alone_does_not_break_resume(monkeypatch, tmp_path):
    """R13-2(a) 짝: 나머지 출처 필드(harness_version_actual)도 같은 취급."""
    _, out_dir = _run(monkeypatch, tmp_path)
    result, _ = _run_with_payload(monkeypatch, tmp_path, PAYLOAD, _never_called,
                                  harness="claude-test-2")
    assert result["status"].startswith("skip")
    assert not list(out_dir.glob("case_99.fp-*.json"))


def test_provenance_fields_are_still_recorded(monkeypatch, tmp_path):
    """R13-2(b): 비교에서 뺀 것이지 기록에서 뺀 것이 아니다 — 봉인 사슬이 읽는다."""
    _, out_dir = _run(monkeypatch, tmp_path)
    fingerprint = json.loads((out_dir / "case_99.json").read_text())["fingerprint"]
    assert fingerprint["pipeline_commit"] == "a" * 40
    assert fingerprint["harness_version_actual"] == "claude-test"
    for key in runner.CONFIG_IDENTITY_KEYS:
        assert fingerprint[key]


def test_config_change_still_forces_a_recall(monkeypatch, tmp_path):
    """R13-2(c): 완화가 "항상 skip"으로 퇴화하지 않는다 — payload가 바뀌면
    재호출되고 원본은 손대지 않은 채 sibling으로 간다."""
    _, out_dir = _run(monkeypatch, tmp_path)
    original = out_dir / "case_99.json"
    original_bytes = original.read_bytes()
    changed = copy.deepcopy(PAYLOAD)
    changed["filing_chronology"] = [{"form": "8-K", "filed": "2019-12-31"}]

    result, _ = _run_with_payload(monkeypatch, tmp_path, changed)

    assert "stale-superseding" in result["status"]
    assert original.read_bytes() == original_bytes
    assert len(list(out_dir.glob("case_99.fp-*.json"))) == 1


def test_in_window_commit_does_not_multiply_fp_siblings(monkeypatch, tmp_path):
    """R13-2: 교착이 sibling 층에서 재현되지 않는다 — 구성이 바뀌어 sibling이
    한 번 생긴 뒤 HEAD가 또 움직여도 sibling은 하나로 유지된다 (fp_siblings의
    '정본 모호' fail-closed를 다시 켜지 않는다)."""
    _, out_dir = _run(monkeypatch, tmp_path)
    changed = copy.deepcopy(PAYLOAD)
    changed["filing_chronology"] = [{"form": "8-K", "filed": "2019-12-31"}]
    _run_with_payload(monkeypatch, tmp_path, changed)
    assert len(list(out_dir.glob("case_99.fp-*.json"))) == 1

    # 같은 구성, 창 중간 커밋으로 HEAD만 이동한 재개
    result, _ = _run_with_payload(monkeypatch, tmp_path, changed, _never_called,
                                  head="b" * 40)
    assert result["status"].startswith("skip")
    assert len(list(out_dir.glob("case_99.fp-*.json"))) == 1


def test_legacy_valid_output_fails_by_default(monkeypatch, tmp_path):
    _, out_dir = _run(monkeypatch, tmp_path)
    path = out_dir / "case_99.json"
    legacy = json.loads(path.read_text())
    legacy.pop("fingerprint")
    path.write_text(json.dumps(legacy), encoding="utf-8")
    legacy_bytes = path.read_bytes()

    result, _ = _run(monkeypatch, tmp_path, _never_called)
    assert result["status"].startswith("FAIL (stale_legacy_output")
    assert "--accept-legacy-output" in result["status"]
    assert path.read_bytes() == legacy_bytes
    assert not list(out_dir.glob("case_99.fp-*.json"))


def test_legacy_valid_output_skips_when_accepted(monkeypatch, tmp_path):
    _, out_dir = _run(monkeypatch, tmp_path)
    path = out_dir / "case_99.json"
    legacy = json.loads(path.read_text())
    legacy.pop("fingerprint")
    path.write_text(json.dumps(legacy), encoding="utf-8")

    result, _ = _run(
        monkeypatch, tmp_path, _never_called, accept_legacy_output=True)
    assert "ACCEPTED" in result["status"]


def test_new_output_embeds_computed_fingerprint(monkeypatch, tmp_path):
    result, out_dir = _run(monkeypatch, tmp_path)
    assert result["status"].startswith("OK")
    record = json.loads((out_dir / "case_99.json").read_text())
    payload = {key: PAYLOAD[key] for key in runner.MODEL_VISIBLE_KEYS}
    user_payload = json.dumps(payload, ensure_ascii=False)
    task = runner.TASK.format(company_name="Example", ticker="EX", cik_part=", CIK 1",
                              cutoff_date="2020-01-01")
    assert record["fingerprint"] == runner.compute_fingerprint(CASE, task, user_payload)


def test_stale_versioned_path_is_deterministic(monkeypatch, tmp_path):
    _, out_dir = _run(monkeypatch, tmp_path)
    original = out_dir / "case_99.json"
    record = json.loads(original.read_text())
    record["fingerprint"]["model_requested"] = "old-model"
    original.write_text(json.dumps(record), encoding="utf-8")

    _run(monkeypatch, tmp_path)
    sibling = next(out_dir.glob("case_99.fp-*.json"))
    sibling_bytes = sibling.read_bytes()
    first = json.loads(sibling.read_text())
    result, _ = _run(monkeypatch, tmp_path, _never_called)
    siblings = list(out_dir.glob("case_99.fp-*.json"))
    second = json.loads(siblings[0].read_text())

    assert result["status"] == "skip (멱등 — fp-sibling 일치)"
    assert sibling.read_bytes() == sibling_bytes
    assert len(siblings) == 1
    first.pop("run_timestamp")
    second.pop("run_timestamp")
    assert first == second
    # R13-2: sibling 경로명은 전체 fingerprint가 아니라 구성 정체에서 파생한다
    # (출처 필드가 움직일 때마다 같은 구성이 새 sibling을 낳지 않도록).
    canonical = json.dumps(runner.config_identity(second["fingerprint"]),
                           sort_keys=True, ensure_ascii=False)
    assert sibling.name == f"case_99.fp-{hashlib.sha256(canonical.encode()).hexdigest()[:8]}.json"


def test_harness_version_failure_is_fail_closed(monkeypatch):
    """R1-16: 버전 획득 실패가 'UNAVAILABLE'로 fingerprint에 들어가는 대신
    fail-closed 예외 — 단일 출처(enforce_harness_pin) 경유 증명."""
    import cli_client
    import pytest
    monkeypatch.setattr(cli_client, "_harness_version_actual", None)
    monkeypatch.setattr(cli_client, "CLAUDE_BIN", "/nonexistent/claude-binary")
    with pytest.raises(RuntimeError, match="fail-closed"):
        runner.get_harness_version()


def test_harness_version_reuses_pin_checked_measurement(monkeypatch):
    import cli_client
    monkeypatch.setattr(cli_client, "_harness_version_actual",
                        f"{cli_client.HARNESS_PIN} (test)")
    assert runner.get_harness_version() == f"{cli_client.HARNESS_PIN} (test)"
    assert "UNAVAILABLE" not in runner.get_harness_version()
