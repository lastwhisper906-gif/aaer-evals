"""build_payload look-ahead 필터 CI 강제 (합성 픽스처, 캐시 불요, CI 상주).

test_build_payload.py는 ~/aaer-data 부재 시 전량 skip → CI에서 컷오프 필터가
검증되지 않던 A2 공백을 메운다. bp.DATA_DIR을 합성 코퍼스로 monkeypatch해
filed>cutoff 항목이 load_pit_series·load_filing_chronology에서 제외되는지 확인."""
import datetime as dt
import json

import build_payload as bp


def _corpus(tmp_path, ticker="TST"):
    xb = tmp_path / ticker / "xbrl"; ed = tmp_path / ticker / "edgar"
    xb.mkdir(parents=True); ed.mkdir(parents=True)
    facts = {"facts": {"us-gaap": {"Revenues": {"units": {"USD": [
        {"val": 1000, "filed": "2019-02-01", "start": "2018-01-01", "end": "2018-12-31",
         "accn": "0000000000-00-000001", "form": "10-K"},
        # filed AFTER cutoff — 반드시 제외돼야 함
        {"val": 1200, "filed": "2020-02-01", "start": "2019-01-01", "end": "2019-12-31",
         "accn": "0000000000-00-000002", "form": "10-K"},
    ]}}}}}
    (xb / "CIK0000000001.json").write_text(json.dumps(facts), encoding="utf-8")
    subs = {"filings": {"recent": {
        "form": ["10-K", "10-Q", "10-K"],
        "filingDate": ["2019-02-01", "2019-08-01", "2020-02-01"],  # 마지막은 cutoff 이후
        "accessionNumber": ["0000000000-00-000001", "0000000000-00-000003",
                            "0000000000-00-000002"]}}}
    (ed / "CIK0000000001.json").write_text(json.dumps(subs), encoding="utf-8")
    return tmp_path


def test_load_pit_series_excludes_post_cutoff(tmp_path, monkeypatch):
    monkeypatch.setattr(bp, "DATA_DIR", _corpus(tmp_path))
    cutoff = dt.date(2019, 12, 31)
    series = bp.load_pit_series("TST", cutoff)
    facts = [v for vals in series.values() for v in vals]
    assert facts, "필터가 전부를 지우면 안 됨 (컷오프 이전 1건 존재)"
    for v in facts:
        assert dt.date.fromisoformat(v["filed"]) <= cutoff, f"look-ahead: {v['filed']} > {cutoff}"
    assert all(v["value"] != 1200 for v in facts)  # 2020-02-01 filed 항목 부재


def test_load_filing_chronology_excludes_post_cutoff(tmp_path, monkeypatch):
    monkeypatch.setattr(bp, "DATA_DIR", _corpus(tmp_path))
    cutoff = dt.date(2019, 12, 31)
    chrono = bp.load_filing_chronology("TST", cutoff)
    assert chrono
    for r in chrono:
        assert dt.date.fromisoformat(r["filing_date"]) <= cutoff
    assert "2020-02-01" not in {r["filing_date"] for r in chrono}


def test_full_payload_build_respects_cutoff(tmp_path, monkeypatch):
    monkeypatch.setattr(bp, "DATA_DIR", _corpus(tmp_path))
    case = {"case_id": "case_99", "ticker": "TST", "cik": "0000000001",
            "company_name": "T", "cutoff_date": "2019-12-31"}
    p = bp.build_payload(case)
    for vals in p["financial_series_point_in_time"].values():
        for v in vals:
            assert dt.date.fromisoformat(v["filed"]) <= dt.date(2019, 12, 31)
