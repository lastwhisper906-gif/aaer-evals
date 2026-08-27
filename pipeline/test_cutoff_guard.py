"""cutoff_guard 테스트. v0: 허용 / 차단(예외) / 경계일 허용 / 양쪽 모두 로그.
v1 추가: 중복 case_id fail-closed / EDGAR accession 역조회(일치·불일치·미보유)."""
import json

import pytest

from cutoff_guard import (
    CutoffGuardError,
    CutoffViolationError,
    assert_payload_pre_cutoff,
    load_document,
)

CUTOFF = "2014-06-05"  # 예: 폭로일 2014-06-06의 전일
ACCESSION = "0001234567-14-000001"


@pytest.fixture
def env(tmp_path):
    registry = tmp_path / "candidates.json"
    registry.write_text(json.dumps({"candidates": [
        {"case_id": "T01", "ticker": "AAA", "cutoff_date": CUTOFF},
        {"case_id": "T02", "ticker": "BBB", "cutoff_date": "UNRESOLVED"},
    ]}), encoding="utf-8")
    doc = tmp_path / "doc.txt"
    doc.write_text("10-K body", encoding="utf-8")
    log = tmp_path / "logs" / "access_log.jsonl"
    edgar = tmp_path / "aaer-data"
    sub_dir = edgar / "AAA" / "edgar"
    sub_dir.mkdir(parents=True)
    (sub_dir / "CIK0001234567.json").write_text(json.dumps({"filings": {"recent": {
        "accessionNumber": [ACCESSION], "filingDate": ["2014-01-01"], "form": ["10-K"],
    }, "files": []}}), encoding="utf-8")
    return {"registry": registry, "doc": doc, "log": log, "edgar": edgar}


def read_log(log):
    return [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()]


def load(env, doc_date, case_id="T01", **kwargs):
    return load_document(case_id, env["doc"], doc_date,
                         registry_path=env["registry"], log_path=env["log"],
                         edgar_data_dir=env["edgar"], **kwargs)


@pytest.fixture
def completed_payload():
    return {
        "financial_series_point_in_time": {
            "Revenue": [{"filed": "2014-01-01"}],
        },
        "filing_chronology": [{"form": "10-K", "filing_date": "2014-01-01"}],
    }


def test_completed_payload_pre_cutoff_passes(completed_payload):
    assert_payload_pre_cutoff(completed_payload, CUTOFF)


def test_completed_payload_post_cutoff_series_raises(completed_payload):
    completed_payload["financial_series_point_in_time"]["Revenue"][0]["filed"] = "2014-06-06"
    with pytest.raises(CutoffGuardError):
        assert_payload_pre_cutoff(completed_payload, CUTOFF)


def test_completed_payload_post_cutoff_chronology_raises(completed_payload):
    completed_payload["filing_chronology"][0]["filing_date"] = "2014-06-06"
    with pytest.raises(CutoffGuardError):
        assert_payload_pre_cutoff(completed_payload, CUTOFF)


def test_completed_payload_cutoff_boundary_passes(completed_payload):
    completed_payload["financial_series_point_in_time"]["Revenue"][0]["filed"] = CUTOFF
    completed_payload["filing_chronology"][0]["filing_date"] = CUTOFF
    assert_payload_pre_cutoff(completed_payload, CUTOFF)


def test_completed_payload_missing_scanned_key_raises(completed_payload):
    del completed_payload["filing_chronology"]
    with pytest.raises(CutoffGuardError):
        assert_payload_pre_cutoff(completed_payload, CUTOFF)


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


def test_duplicate_case_id_fails_closed(env):
    env["registry"].write_text(json.dumps({"candidates": [
        {"case_id": "T01", "ticker": "AAA", "cutoff_date": CUTOFF},
        {"case_id": "T01", "ticker": "AAA", "cutoff_date": "2020-01-01"},
    ]}), encoding="utf-8")
    with pytest.raises(CutoffGuardError, match="중복"):
        load(env, "2014-01-01")


def test_accession_crosscheck_pass(env):
    assert load(env, "2014-01-01", accession_no=ACCESSION) == "10-K body"
    entry = read_log(env["log"])[-1]
    assert entry["verdict"] == "allowed" and "cross-checked" in entry["reason"]
    assert entry["accession_no"] == ACCESSION


def test_accession_crosscheck_rejects_wrong_doc_date(env):
    # 신고 doc_date가 컷오프 안이어도 EDGAR filingDate와 다르면 통과 불가
    with pytest.raises(CutoffGuardError, match="EDGAR filingDate"):
        load(env, "2014-02-02", accession_no=ACCESSION)
    assert read_log(env["log"])[-1]["reason"] == "doc_date_mismatch_edgar"


def test_accession_crosscheck_unknown_accession_fails_closed(env):
    with pytest.raises(CutoffGuardError, match="미발견"):
        load(env, "2014-01-01", accession_no="0009999999-14-000009")


def test_accession_crosscheck_missing_submissions_fails_closed(env, tmp_path):
    with pytest.raises(CutoffGuardError, match="submissions JSON 없음"):
        load_document("T01", env["doc"], "2014-01-01", accession_no=ACCESSION,
                      registry_path=env["registry"], log_path=env["log"],
                      edgar_data_dir=tmp_path / "empty")
    assert read_log(env["log"])[-1]["reason"] == "edgar_crosscheck_unavailable"


# ── R1-13: EDGAR 병렬 배열 정렬성 fail-closed ─────────────────────────────

def _chronology_env(tmp_path, recent):
    registry = tmp_path / "candidates.json"
    registry.write_text(json.dumps({"candidates": [
        {"case_id": "T01", "ticker": "AAA", "cutoff_date": CUTOFF}]}), encoding="utf-8")
    sub_dir = tmp_path / "aaer-data" / "AAA" / "edgar"
    sub_dir.mkdir(parents=True)
    (sub_dir / "CIK0001234567.json").write_text(
        json.dumps({"filings": {"recent": recent, "files": []}}), encoding="utf-8")
    return {"registry": registry, "edgar": tmp_path / "aaer-data",
            "log": tmp_path / "logs" / "access_log.jsonl"}


def _chronology(env):
    from cutoff_guard import load_edgar_chronology
    return load_edgar_chronology("T01", "AAA", CUTOFF, data_dir=env["edgar"],
                                 registry_path=env["registry"], log_path=env["log"])


def test_chronology_truncated_parallel_arrays_fail_closed(tmp_path):
    """filingDate가 form보다 짧으면 zip이 뒤 제출을 침묵 절단 — 예외여야 한다."""
    env = _chronology_env(tmp_path, {
        "form": ["10-K", "8-K"], "filingDate": ["2014-01-01"],
        "accessionNumber": [ACCESSION, "0001234567-14-000002"], "items": ["", ""]})
    with pytest.raises(CutoffGuardError, match="병렬 배열 길이 불일치"):
        _chronology(env)


def test_chronology_short_accession_array_fails_not_none_collapse(tmp_path):
    """accessionNumber가 짧으면 종전에는 뒤 제출의 accession이 침묵 None."""
    env = _chronology_env(tmp_path, {
        "form": ["10-K", "8-K"], "filingDate": ["2014-01-01", "2014-02-01"],
        "accessionNumber": [ACCESSION], "items": ["", ""]})
    with pytest.raises(CutoffGuardError, match="병렬 배열 길이 불일치"):
        _chronology(env)


def test_chronology_items_length_mismatch_fails(tmp_path):
    env = _chronology_env(tmp_path, {
        "form": ["10-K", "8-K"], "filingDate": ["2014-01-01", "2014-02-01"],
        "accessionNumber": [ACCESSION, "0001234567-14-000002"], "items": [""]})
    with pytest.raises(CutoffGuardError, match="items 배열 길이 불일치"):
        _chronology(env)


def test_chronology_aligned_arrays_pass_and_absent_items_allowed(tmp_path):
    env = _chronology_env(tmp_path, {
        "form": ["10-K", "8-K"], "filingDate": ["2014-01-01", "2014-02-01"],
        "accessionNumber": [ACCESSION, "0001234567-14-000002"]})
    rows, meta = _chronology(env)
    assert [r["accessionNumber"] for r in rows] == [ACCESSION, "0001234567-14-000002"]
    assert all(r["items"] == "" for r in rows)


def test_submissions_index_truncated_arrays_fail_closed(tmp_path):
    """_submissions 인덱스 경로(교차 대조용 accession→filingDate)도 동일 강제."""
    env = _chronology_env(tmp_path, {
        "form": ["10-K"], "filingDate": ["2014-01-01", "2014-02-01"],
        "accessionNumber": [ACCESSION]})
    doc = tmp_path / "doc.txt"
    doc.write_text("10-K body", encoding="utf-8")
    with pytest.raises(CutoffGuardError, match="병렬 배열 길이 불일치"):
        load_document("T01", doc, "2014-01-01",
                      accession_no=ACCESSION, registry_path=env["registry"],
                      log_path=env["log"], edgar_data_dir=env["edgar"])


# ── R1-17: 신뢰 레지스트리 명시 열거 ──────────────────────────────────────

def test_unlisted_cases_like_file_is_not_trusted(tmp_path):
    """이름 패턴 자기-신뢰 차단: data/evaluatee/에 떨어진 미등재 cases_*.json은
    실제 corpus 접근 신뢰를 얻지 못한다 (fail-closed)."""
    from cutoff_guard import DEFAULT_EDGAR_DATA, _fixture_settings, REPO_ROOT
    rogue = REPO_ROOT / "data" / "evaluatee" / "cases_rogue_selftrust.json"
    with pytest.raises(CutoffGuardError, match="비기본 레지스트리"):
        _fixture_settings(DEFAULT_EDGAR_DATA, rogue, "logs/x.jsonl")


def test_listed_case_files_remain_trusted():
    from cutoff_guard import TRUSTED_CASE_FILES, _fixture_settings, DEFAULT_EDGAR_DATA, REPO_ROOT
    assert set(TRUSTED_CASE_FILES) == {
        "cases.json", "cases_wave2.json", "cases_holdout.json",
        "cases_holdout_controls.json", "cases_v2.json", "cases_forward_001.json"}
    for name in TRUSTED_CASE_FILES:
        registry = REPO_ROOT / "data" / "evaluatee" / name
        _fixture_settings(DEFAULT_EDGAR_DATA, registry, "logs/x.jsonl")  # 무예외


def test_forward_registry_trusted_toward_real_corpus_path(monkeypatch, tmp_path):
    """R7-1: 서명된 런북 명령(runner --cases data/evaluatee/cases_forward_001.json)이
    봉인 창 안에서 파이프라인 diff 없이 실행 가능함을 오프라인으로 증명 —
    forward 레지스트리는 실제 corpus 루트를 향한 신뢰 술어를 통과한다."""
    import cutoff_guard
    fixture_corpus = tmp_path / "aaer-data"
    fixture_corpus.mkdir()
    monkeypatch.setattr(cutoff_guard, "DEFAULT_EDGAR_DATA", fixture_corpus)
    registry = cutoff_guard.REPO_ROOT / "data" / "evaluatee" / "cases_forward_001.json"
    # 신뢰 거부(비기본 레지스트리) 예외 없이 corpus 루트가 그대로 반환되어야 한다.
    data_dir, _log_path = cutoff_guard._fixture_settings(
        fixture_corpus, registry, tmp_path / "x.jsonl")
    assert data_dir == fixture_corpus


def test_trusted_case_files_are_committed_clean_in_git():
    """R8-2: 신뢰는 커밋 diff로 가시화되어야 한다 (R1-17 원칙) — 신뢰 이름
    자리에 미추적/변경 파일이 있으면 실패. 커밋 전의 파일이 이름만으로
    실제 corpus 접근을 자기-신뢰하는 창을 닫는다. cases_forward_001.json이
    런북 §4(3)대로 빌드+커밋되면 자동으로 통과한다 (테스트 수정 불요)."""
    import subprocess
    from cutoff_guard import REPO_ROOT, TRUSTED_CASE_FILES
    tracked = set(subprocess.run(
        ["git", "ls-files", "data/evaluatee"], cwd=REPO_ROOT,
        capture_output=True, text=True, check=True).stdout.split())
    dirty = set()
    for line in subprocess.run(
            ["git", "status", "--porcelain", "data/evaluatee"], cwd=REPO_ROOT,
            capture_output=True, text=True, check=True).stdout.splitlines():
        dirty.add(line[3:].strip().strip('"'))
    offenders = []
    for name in TRUSTED_CASE_FILES:
        rel = f"data/evaluatee/{name}"
        exists = (REPO_ROOT / rel).exists()
        if exists and (rel not in tracked or rel in dirty):
            offenders.append(rel)
    assert not offenders, (
        f"신뢰 레지스트리 이름 자리에 미추적/미커밋 변경 파일: {offenders} — "
        "커밋 없이 실제 corpus 접근 신뢰를 얻을 수 없다 (R8-2)")
