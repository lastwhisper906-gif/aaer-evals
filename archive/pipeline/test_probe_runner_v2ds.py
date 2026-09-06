"""probe_runner --v2-dateshift 배선 테스트 (Q-F05, 무호출) — 렌더 이동·로그 명명·기본 off."""
import json

import probe_runner as pr
import cli_client
import date_shift


class FakeResult:
    ok = True
    structured = {"company_guess": "unknown", "confidence": "low"}
    fail_reason = None


def _capture(monkeypatch, calls):
    def fake_call_model(model, system, user, schema, log_dir, log_name,
                        forbid_markers=None, **kw):
        calls.append({"user": user, "log_name": log_name})
        return FakeResult()
    monkeypatch.setattr(cli_client, "call_model", fake_call_model)


def _fake_payload(case, perturb):
    assert perturb is True
    return {"_k_internal": 1,
            "case": {"case_id": case["case_id"], "company_name": "Co", "ticker": "TK",
                     "cutoff_date": "2015-06-30"},
            "financial_series_point_in_time": {
                "t": [{"start": "2014-01-01", "end": "2014-12-31",
                       "filed": "2015-02-15", "value": 1, "accession": "0001-15-000001"}]},
            "filing_chronology": [{"filing_date": "2015-02-15", "form": "10-K"}]}


def test_v2ds_shifts_render_and_isolates_log(tmp_path, monkeypatch):
    calls = []
    _capture(monkeypatch, calls)
    monkeypatch.setattr(pr.bp, "build_payload", _fake_payload)
    case = {"case_id": "case_99"}
    pr.probe_case("recognition", case, tmp_path, tmp_path, v2_dateshift=True)
    sent = json.loads(calls[0]["user"])
    off = date_shift.offset_for_case("case_99")
    assert sent["case"]["cutoff_date"] == date_shift.shift_date("2015-06-30", off)
    assert sent["financial_series_point_in_time"]["t"][0]["accession"] == "acc-001"
    assert "0001-15-000001" not in calls[0]["user"]
    assert calls[0]["log_name"] == "probe_recognition_v2ds_case_99"  # D70 교훈


def test_default_off_preserves_v1_render(tmp_path, monkeypatch):
    calls = []
    _capture(monkeypatch, calls)
    monkeypatch.setattr(pr.bp, "build_payload", _fake_payload)
    pr.probe_case("recognition", {"case_id": "case_99"}, tmp_path, tmp_path)
    sent = json.loads(calls[0]["user"])
    assert sent["case"]["cutoff_date"] == "2015-06-30"          # 원본 유지
    assert sent["financial_series_point_in_time"]["t"][0]["accession"] == "0001-15-000001"
    assert calls[0]["log_name"] == "probe_recognition_case_99"  # v1 명명 불변


def test_v1_result_does_not_satisfy_v2ds_run(tmp_path, monkeypatch):
    (tmp_path / "case_99.json").write_text(
        json.dumps(FakeResult.structured), encoding="utf-8")
    calls = []
    _capture(monkeypatch, calls)
    monkeypatch.setattr(pr.bp, "build_payload", _fake_payload)

    result = pr.probe_case(
        "recognition", {"case_id": "case_99"}, tmp_path, tmp_path,
        v2_dateshift=True)

    assert result["status"].startswith("OK")
    assert len(calls) == 1
    assert (tmp_path / "case_99_v2ds.json").exists()


def test_rate_limit_cancels_queued_probes(tmp_path, monkeypatch):
    """R2-11: 레이트 리밋 발생 시 대기 큐를 취소해야 한다 — Executor.__exit__
    소진으로 이미 리밋 걸린 구독에 잔여 프로브가 계속 발사되면 안 된다."""
    import sys
    cases = {"cases": [{"case_id": f"case_{i:02d}"} for i in range(1, 21)]}
    cases_path = tmp_path / "cases.json"
    cases_path.write_text(json.dumps(cases), encoding="utf-8")

    executed = []

    def limited_probe(kind, case, out, log_dir, v2_dateshift=False, **kw):
        executed.append(case["case_id"])
        raise cli_client.RateLimitedError("usage limit reached")

    monkeypatch.setattr(pr, "probe_case", limited_probe)
    monkeypatch.setattr(pr.cli_client, "assert_no_metered_credentials", lambda: None)
    monkeypatch.setattr(pr.cli_client, "require_clean_tree", lambda: None)
    monkeypatch.setattr(sys, "argv",
                        ["probe_runner.py", "--recognition", "--concurrency", "1",
                         "--cases", str(cases_path),
                         "--out-root", str(tmp_path / "probe_out")])
    assert pr.main() == 3
    assert len(executed) == 1, (
        f"리밋 후에도 {len(executed) - 1}건이 추가 발사됨 — 큐 미취소")


# ── R1-14: 프로브 멱등 skip의 구성 fingerprint ────────────────────────────

def _probe_once(tmp_path, monkeypatch, calls, **kw):
    _capture(monkeypatch, calls)
    monkeypatch.setattr(pr.bp, "build_payload", _fake_payload)
    return pr.probe_case("recognition", {"case_id": "case_99"}, tmp_path, tmp_path, **kw)


def test_same_config_rerun_skips_via_fingerprint(tmp_path, monkeypatch):
    calls = []
    assert _probe_once(tmp_path, monkeypatch, calls)["status"].startswith("OK")
    assert (tmp_path / "fp_case_99.json").exists()
    result = _probe_once(tmp_path, monkeypatch, calls)
    assert result["status"] == "skip (멱등 — fingerprint 일치)"
    assert len(calls) == 1, "동일 구성 재실행이 재호출함"


def test_changed_config_fails_not_skips(tmp_path, monkeypatch):
    """R1-14: stale-but-valid 출력이 바뀐 구성을 조용히 충족하면 안 된다 —
    동결 경로 보호상 덮어쓰기 대신 FAIL."""
    calls = []
    assert _probe_once(tmp_path, monkeypatch, calls)["status"].startswith("OK")
    monkeypatch.setattr(pr, "RECOG_TASK", pr.RECOG_TASK + " CHANGED")
    result = _probe_once(tmp_path, monkeypatch, calls)
    assert result["status"].startswith("FAIL (config_changed")
    assert len(calls) == 1


def test_legacy_output_without_sidecar_fails_unless_accepted(tmp_path, monkeypatch):
    calls = []
    assert _probe_once(tmp_path, monkeypatch, calls)["status"].startswith("OK")
    (tmp_path / "fp_case_99.json").unlink()  # 동결 트리 판형: 사이드카 부재
    result = _probe_once(tmp_path, monkeypatch, calls)
    assert result["status"].startswith("FAIL (stale_legacy_probe")
    accepted = _probe_once(tmp_path, monkeypatch, calls, accept_legacy_probe=True)
    assert accepted["status"].startswith("skip (legacy probe ACCEPTED")
    assert len(calls) == 1


def test_frozen_root_refuses_new_case_file_without_call(tmp_path, monkeypatch):
    """R2-29: 기본 out-root(동결 트리) 아래 신규 케이스 파일 생성은 호출도
    쓰기도 없이 FAIL; 비동결 경로는 종전대로 기록."""
    def forbidden_call(*a, **k):
        raise AssertionError("동결 루트 신규 파일인데 모델 호출 발생")
    monkeypatch.setattr(cli_client, "call_model", forbidden_call)
    monkeypatch.setattr(pr.bp, "build_payload", _fake_payload)
    frozen = tmp_path / "probe_results"
    monkeypatch.setattr(pr, "FROZEN_PROBE_ROOTS", (frozen,))
    res = pr.probe_case("recognition", {"case_id": "case_98"},
                        frozen / "recognition", tmp_path / "logs")
    assert "frozen_root_new_file" in res["status"]
    assert not (frozen / "recognition" / "case_98.json").exists()
    # 비동결 out-root — 종전대로 기록된다
    calls = []
    _capture(monkeypatch, calls)
    out = tmp_path / "fresh" / "recognition"
    res = pr.probe_case("recognition", {"case_id": "case_98"}, out, tmp_path / "logs")
    assert res["status"].startswith("OK") and (out / "case_98.json").exists()


def test_verbatim_with_v2ds_is_a_parse_error(monkeypatch, capsys):
    """R1-15: --verbatim + --v2-dateshift 조합은 무이동 verbatim을 _v2ds
    파일명으로 오표기하던 침묵 결함 — parser.error로 즉시 거부."""
    import sys
    import pytest
    monkeypatch.setattr(sys, "argv",
                        ["probe_runner.py", "--verbatim", "--v2-dateshift"])
    with pytest.raises(SystemExit) as exc:
        pr.main()
    assert exc.value.code == 2  # argparse 사용 오류
    assert "recognition 전용" in capsys.readouterr().err
