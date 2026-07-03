"""cutoff_guard v0 테스트. 시나리오: 허용 / 차단(예외) / 경계일 허용 / 양쪽 모두 로그."""
import json

import pytest

from cutoff_guard import CutoffGuardError, CutoffViolationError, load_document

CUTOFF = "2014-06-05"  # 예: 폭로일 2014-06-06의 전일


@pytest.fixture
def env(tmp_path):
    registry = tmp_path / "candidates.json"
    registry.write_text(json.dumps({"candidates": [
        {"case_id": "T01", "cutoff_date": CUTOFF},
        {"case_id": "T02", "cutoff_date": "UNRESOLVED"},
    ]}), encoding="utf-8")
    doc = tmp_path / "doc.txt"
    doc.write_text("10-K body", encoding="utf-8")
    log = tmp_path / "logs" / "access_log.jsonl"
    return {"registry": registry, "doc": doc, "log": log}


def read_log(log):
    return [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()]


def load(env, doc_date, case_id="T01"):
    return load_document(case_id, env["doc"], doc_date,
                         registry_path=env["registry"], log_path=env["log"])


def test_allowed_load_returns_content_and_logs(env):
    assert load(env, "2014-01-01") == "10-K body"
    (entry,) = read_log(env["log"])
    assert entry["verdict"] == "allowed" and entry["case_id"] == "T01"
    assert "timestamp" in entry and entry["doc_date"] == "2014-01-01"


def test_violation_raises_exception_not_filter(env):
    with pytest.raises(CutoffViolationError) as exc:
        load(env, "2014-06-06")  # 폭로 당일 = 컷오프 다음날 → 차단
    assert exc.value.case_id == "T01"
    assert str(exc.value.doc_date) == "2014-06-06"
    assert str(exc.value.cutoff_date) == CUTOFF


def test_boundary_doc_date_equal_to_cutoff_is_allowed(env):
    assert load(env, CUTOFF) == "10-K body"
    assert read_log(env["log"])[-1]["verdict"] == "allowed"


def test_log_written_on_both_outcomes(env):
    load(env, "2014-01-01")
    with pytest.raises(CutoffViolationError):
        load(env, "2015-01-01")
    verdicts = [e["verdict"] for e in read_log(env["log"])]
    assert verdicts == ["allowed", "blocked"]
    assert read_log(env["log"])[1]["reason"] == "cutoff_violation"


def test_unresolved_cutoff_and_unknown_case_fail_closed(env):
    with pytest.raises(CutoffGuardError):
        load(env, "2000-01-01", case_id="T02")  # UNRESOLVED → 아무리 오래된 문서도 차단
    with pytest.raises(CutoffGuardError):
        load(env, "2000-01-01", case_id="T99")
    assert [e["reason"] for e in read_log(env["log"])] == ["cutoff_unresolved", "unknown_case_id"]
