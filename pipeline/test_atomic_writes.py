"""R1-12: 결과 기록 원자성 (tmp→replace, D67 판형) — runner·probe_runner.

크래시 창 시뮬레이션: .json.tmp 기록 중 OSError를 주입해 부분 기록이
정본 {cid}.json을 절대 오염시키지 않음을 검증한다 (부분 파일이 정본이
되면 멱등 skip이 영영 실패하고 fp-sibling 뒤로 가려진다).
"""
import copy
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

import cli_client
import probe_runner as pr
import runner


def _crash_mid_tmp_write(monkeypatch):
    real_write = Path.write_text

    def crashing(self, text, *args, **kwargs):
        if self.name.endswith(".json.tmp"):
            real_write(self, text[:10], *args, **kwargs)
            raise OSError("simulated crash mid-write")
        return real_write(self, text, *args, **kwargs)

    monkeypatch.setattr(Path, "write_text", crashing)


def _model_output():
    evidence = {"quote": "Revenue=1 (FY2020)", "source_accession_no": "a",
                "location": "Revenue FY2020"}
    return {"checklist": [{"item_id": "CL1", "question": "q", "finding": "no_flag",
                           "confidence": "low", "evidence": [evidence]}],
            "misstatement_probability": 20, "mechanism_hypotheses": [],
            "overall": {"risk_tier": "clear", "top_signals": []}}


def _stub_runner(monkeypatch):
    payload = {"_k_internal": 1.0, "_variant": "original",
               "case": {"company_name": "Example", "ticker": "EX"},
               "financial_series_point_in_time": {
                   "Revenue": [{"accession": "a", "form": "10-K", "filed": "2020-01-01"}]},
               "filing_chronology": []}
    monkeypatch.setattr(runner.bp, "build_payload",
                        lambda case, perturb: copy.deepcopy(payload))
    monkeypatch.setattr(runner.cli_client, "call_model", lambda *a, **k: SimpleNamespace(
        ok=True, structured=_model_output(), fail_reason=None,
        served_models=[runner.EVALUATEE_MODEL]))
    monkeypatch.setattr(runner, "freeze_state", lambda: {"head": "a" * 40})


CASE = {"case_id": "case_99", "company_name": "Example", "ticker": "EX",
        "cik": "1", "cutoff_date": "2020-01-01"}


def test_runner_write_is_atomic(monkeypatch, tmp_path):
    _stub_runner(monkeypatch)
    out_dir, log_dir = tmp_path / "runs", tmp_path / "logs"
    log_dir.mkdir()
    result = runner.run_case(CASE, False, out_dir, log_dir)
    assert result["status"].startswith("OK")
    record = json.loads((out_dir / "case_99.json").read_text(encoding="utf-8"))
    assert record["misstatement_probability"] == 20
    assert not list(out_dir.glob("*.tmp")), "tmp 파일이 정리되지 않음"


def test_runner_crash_mid_write_leaves_no_corrupt_canonical(monkeypatch, tmp_path):
    _stub_runner(monkeypatch)
    out_dir, log_dir = tmp_path / "runs", tmp_path / "logs"
    log_dir.mkdir()
    _crash_mid_tmp_write(monkeypatch)
    with pytest.raises(OSError, match="simulated crash"):
        runner.run_case(CASE, False, out_dir, log_dir)
    assert not (out_dir / "case_99.json").exists(), \
        "크래시 부분 기록이 정본 파일로 남음 — 멱등 skip을 영구 오염"


def _stub_probe(monkeypatch):
    monkeypatch.setattr(cli_client, "call_model", lambda *a, **k: SimpleNamespace(
        ok=True, structured={"company_guess": "unknown", "confidence": "low"},
        fail_reason=None))
    monkeypatch.setattr(pr.bp, "build_payload", lambda case, perturb: {
        "_k_internal": 1, "case": {"case_id": case["case_id"]},
        "financial_series_point_in_time": {}, "filing_chronology": []})


def test_probe_write_is_atomic(monkeypatch, tmp_path):
    _stub_probe(monkeypatch)
    result = pr.probe_case("recognition", {"case_id": "case_98"}, tmp_path, tmp_path)
    assert result["status"].startswith("OK")
    assert json.loads((tmp_path / "case_98.json").read_text(encoding="utf-8"))
    assert not list(tmp_path.glob("*.tmp"))


def test_probe_crash_mid_write_leaves_no_corrupt_canonical(monkeypatch, tmp_path):
    _stub_probe(monkeypatch)
    _crash_mid_tmp_write(monkeypatch)
    with pytest.raises(OSError, match="simulated crash"):
        pr.probe_case("recognition", {"case_id": "case_98"}, tmp_path, tmp_path)
    assert not (tmp_path / "case_98.json").exists()


def test_runner_canary_hit_fails_before_write(monkeypatch, tmp_path):
    """R2-13: 카나리 GUID 출력은 OK로 runs/에 실리지 않는다 — 기록 전 FAIL,
    runmeta 증거는 유지."""
    _stub_runner(monkeypatch)
    hit = _model_output()
    hit["overall"]["top_signals"] = ["canary 9fa11f98-dead-beef"]
    monkeypatch.setattr(runner.cli_client, "call_model", lambda *a, **k: SimpleNamespace(
        ok=True, structured=hit, fail_reason=None,
        served_models=[runner.EVALUATEE_MODEL]))
    out_dir, log_dir = tmp_path / "runs", tmp_path / "logs"
    log_dir.mkdir()
    result = runner.run_case(CASE, False, out_dir, log_dir)
    assert result["status"] == "FAIL (canary_hit)"
    assert not (out_dir / "case_99.json").exists(), "카나리 출력이 기록됨"
    meta = json.loads((log_dir / "runmeta_original_case_99.json").read_text(encoding="utf-8"))
    assert meta["canary_hit"] is True and meta["fail_reason"] == "canary_hit"
