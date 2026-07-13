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
