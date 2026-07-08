"""build_earliness_snapshots 검증 — 선정(캐시 불요) + 그리드/가드(합성 픽스처, 캐시 불요).

핵심: 실 캐시 없이도 (a) 적격 선정이 커밋 산출물만으로 결정론적이고 (b) 그리드+
cutoff_guard 통합이 합성 EDGAR 픽스처에서 look-ahead를 fail-closed로 막는지 증명.
"""
import datetime as dt
import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
sys.path.insert(0, str(REPO / "pipeline"))

import build_earliness_snapshots as be  # noqa: E402
import build_payload as bp              # noqa: E402
import cutoff_guard                     # noqa: E402


# ---------- 선정 (캐시 불요, 커밋 산출물) ----------

def test_select_eligible_counts_and_membership():
    elig = be.select_eligible()
    by = {e["case_id"]: e for e in elig}
    fraud = {c for c, e in by.items() if e["group"] == "fraud"}
    ctrl = {c for c, e in by.items() if e["group"] == "control"}
    assert len(fraud) == 13 and len(ctrl) == 8
    # 사전등록 detected 7 (wave-2) + 6 (wave-1) 포함
    for c in ["case_39", "case_40", "case_59", "case_60", "case_61", "case_65", "case_66"]:
        assert c in fraud
    for c in ["case_01", "case_02", "case_08", "case_09", "case_12", "case_13"]:
        assert c in fraud
    # 제외: MON(06)·LOGI(03, p=42)·CSC(52,40)·BRX(67,20)
    for c in ["case_06", "case_03", "case_52", "case_67"]:
        assert c not in fraud
    # 대조군은 detected 여부와 무관하게 8 전부 (Ryder case_10 p=58 FP도 포함)
    assert "case_10" in ctrl


def test_snapshot_case_uses_base_id_and_snapshot_cutoff():
    e = {"case_id": "case_39", "ticker": "OSIR", "cik": "1",
         "company_name": "OSIRIS", "revelation_cutoff": "2015-11-05"}
    snap = be.eg.Snapshot(j=3, cutoff=dt.date(2015, 2, 2), boundary_filed=dt.date(2015, 2, 1))
    sc = be.snapshot_case(e, snap)
    assert sc["case_id"] == "case_39_s3" and sc["base_id"] == "case_39"
    assert sc["cutoff_date"] == "2015-02-02"
    assert sc["ticker"] == "OSIR"


# ---------- 그리드 + 가드 (합성 EDGAR 픽스처, 캐시 불요) ----------

def _fixture_edgar(tmp_path, ticker, forms_dates, accns=None):
    d = tmp_path / ticker / "edgar"
    d.mkdir(parents=True)
    forms = [f for f, _ in forms_dates]
    dates = [dt_ for _, dt_ in forms_dates]
    body = {"form": forms, "filingDate": dates,
            "accessionNumber": accns or [f"{i:018d}" for i in range(len(forms))]}
    (d / f"CIK{ticker}.json").write_text(json.dumps({"filings": {"recent": body}}),
                                         encoding="utf-8")
    return tmp_path


def test_build_case_grid_on_synthetic_cache(tmp_path, monkeypatch):
    filings = [("10-K", "2013-03-01"), ("10-Q", "2013-08-01"), ("10-Q", "2014-05-01"),
               ("8-K", "2014-06-15"), ("10-K", "2014-08-01")]
    root = _fixture_edgar(tmp_path, "TST", filings)
    monkeypatch.setattr(bp, "DATA_DIR", root)
    e = {"case_id": "case_99", "ticker": "TST", "cik": "1",
         "company_name": "T", "revelation_cutoff": "2015-01-01"}
    grid = be.build_case_grid(e, max_snapshots=8, day_offset=1)
    # 정기 제출 4건(10-K/10-Q) → 최신 8/1(10-K)이 j=1. 8-K(6/15)는 경계 아님.
    assert [s.boundary_filed.isoformat() for s in grid.snapshots] == \
        ["2014-08-01", "2014-05-01", "2013-08-01", "2013-03-01"]
    # 모든 스냅샷 컷오프 <= 폭로 (불변)
    assert all(s.cutoff <= dt.date(2015, 1, 1) for s in grid.snapshots)


def _rev_reg(tmp_path, base_id, revelation):
    reg = tmp_path / "rev_reg.json"
    reg.write_text(json.dumps({"candidates": [{"case_id": base_id, "cutoff_date": revelation}]}),
                   encoding="utf-8")
    return reg


def test_guard_snapshot_allows_within_revelation(tmp_path):
    # 스냅샷 컷오프(2015-08-01)가 폭로(2015-11-05) 이하 → allowed + access log 기록.
    reg = _rev_reg(tmp_path, "case_39", "2015-11-05")
    log = tmp_path / "access_log.jsonl"
    sc = {"case_id": "case_39_s3", "base_id": "case_39", "ticker": "OSIR",
          "cutoff_date": "2015-08-01"}
    assert be.guard_snapshot(reg, "case_39", sc, log) == "allowed"
    assert '"verdict": "allowed"' in log.read_text(encoding="utf-8")  # smoke-test 요건 a


def test_guard_snapshot_fails_closed_past_revelation(tmp_path):
    # 스냅샷 컷오프가 폭로 경계를 넘으면 fail-closed (§5-1 look-ahead 차단) — 캐시 불요.
    reg = _rev_reg(tmp_path, "case_39", "2015-11-05")
    log = tmp_path / "access_log.jsonl"
    sc = {"case_id": "case_39_s1", "base_id": "case_39", "ticker": "OSIR",
          "cutoff_date": "2015-11-06"}
    with pytest.raises(cutoff_guard.CutoffViolationError):
        be.guard_snapshot(reg, "case_39", sc, log)
