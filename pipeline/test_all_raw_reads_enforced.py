"""벌크 corpus 읽기 게이트웨이의 정적·행동 계약."""
import ast
import datetime
import json
from pathlib import Path

import pytest

import build_payload
import cutoff_guard
import payload_v2_extract


PIPELINE = Path(__file__).resolve().parent


# 함수 단위 오염(taint) 시드 — 코퍼스 루트를 가리키는 이름.
CORPUS_ROOT_NAMES = frozenset({"DATA_DIR", "data_dir"})

# 매칭되는 원시 읽기 형태. R16-1 이전 판은 {read_text, open, load}를 *속성 호출로만*
# 봤고, 그래서 read_bytes·iterdir·builtin open(path)·json.load(open(path))이 전부
# 통과했다 — build_payload.py에 실제 가드 우회를 주입해도 0 red였다.
RAW_READ_ATTRS = frozenset({"read_text", "read_bytes", "open", "load", "iterdir"})
# builtin 호출 형태(수신자가 없어 속성 규칙이 닿지 않는다): open(path)
RAW_READ_BUILTINS = frozenset({"open"})


def _tainted_names(node, roots) -> set[str]:
    """함수 안에서 코퍼스 루트로부터 파생된 이름 집합 (고정점까지 전파)."""
    tainted = set(roots)
    changed = True
    while changed:
        changed = False
        for child in ast.walk(node):
            targets, value = [], None
            if isinstance(child, ast.Assign):
                targets, value = child.targets, child.value
            elif isinstance(child, ast.AnnAssign):
                targets, value = [child.target], child.value
            elif isinstance(child, (ast.For, ast.comprehension)):
                targets, value = [child.target], child.iter
            if value is None:
                continue
            names = {n.id for n in ast.walk(value) if isinstance(n, ast.Name)}
            if names & tainted:
                for target in targets:
                    for name in (n.id for n in ast.walk(target) if isinstance(n, ast.Name)):
                        if name not in tainted:
                            tainted.add(name)
                            changed = True
    return tainted


def _raw_read_functions(source: str, roots=CORPUS_ROOT_NAMES) -> list[str]:
    tree = ast.parse(source)
    violations = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        tainted = _tainted_names(node, roots)
        raw_call = False
        for call in (n for n in ast.walk(node) if isinstance(n, ast.Call)):
            func = call.func
            arg_names = {n.id
                         for a in (*call.args, *(k.value for k in call.keywords))
                         for n in ast.walk(a) if isinstance(n, ast.Name)}
            if isinstance(func, ast.Attribute) and func.attr in RAW_READ_ATTRS:
                receiver_names = {n.id for n in ast.walk(func.value)
                                  if isinstance(n, ast.Name)}
                raw_call = raw_call or bool((receiver_names | arg_names) & tainted)
            elif isinstance(func, ast.Name) and func.id in RAW_READ_BUILTINS:
                raw_call = raw_call or bool(arg_names & tainted)
        if raw_call:
            violations.append(node.name)
    return violations


OLD_SOURCE = '''
def load_pit_series(ticker, cutoff):
    xbrl_dir = DATA_DIR / ticker / "xbrl"
    for path in xbrl_dir.glob("*.json"):
        data = json.loads(path.read_text())
'''

_SRC_READ_BYTES = '''
def load_pit_series(ticker, cutoff):
    blob = (DATA_DIR / ticker / "xbrl" / "CIK1.json").read_bytes()
'''

_SRC_ITERDIR = '''
def load_pit_series(ticker, cutoff):
    return sorted((DATA_DIR / ticker / "xbrl").iterdir())
'''

_SRC_PATH_OPEN = '''
def load_pit_series(ticker, cutoff):
    handle = (DATA_DIR / ticker / "xbrl" / "CIK1.json").open()
'''

_SRC_BUILTIN_OPEN = '''
def load_pit_series(ticker, cutoff):
    for name in os.listdir(DATA_DIR / ticker / "xbrl"):
        handle = open(DATA_DIR / ticker / "xbrl" / name)
'''

_SRC_JSON_LOAD_OPEN = '''
def load_pit_series(ticker, cutoff):
    for name in os.listdir(DATA_DIR / ticker / "xbrl"):
        data = json.load(open(DATA_DIR / ticker / "xbrl" / name))
'''

# 형태별 양성 대조 — 한 형태당 소스 하나. 대조가 없는 형태가 R16-1이 막으려는 결함
# 그 자체이므로, 커버리지는 test_every_matched_read_form_has_a_positive_control이
# RAW_READ_ATTRS | RAW_READ_BUILTINS와의 집합 동일성으로 강제한다.
CONTROL_SOURCES = {
    "read_text": (OLD_SOURCE, {"read_text"}),
    "read_bytes": (_SRC_READ_BYTES, {"read_bytes"}),
    "iterdir": (_SRC_ITERDIR, {"iterdir"}),
    "path_open": (_SRC_PATH_OPEN, {"open"}),
    "builtin_open": (_SRC_BUILTIN_OPEN, {"open"}),
    "json_load_open": (_SRC_JSON_LOAD_OPEN, {"load", "open"}),
}


@pytest.mark.parametrize("form", sorted(CONTROL_SOURCES), ids=sorted(CONTROL_SOURCES))
def test_scanner_flags_raw_read_form(form):
    source, _ = CONTROL_SOURCES[form]
    assert _raw_read_functions(source) == ["load_pit_series"], form


def test_every_matched_read_form_has_a_positive_control():
    covered = set().union(*(forms for _, forms in CONTROL_SOURCES.values()))
    assert covered == set(RAW_READ_ATTRS | RAW_READ_BUILTINS)


def test_ast_scanner_catches_old_source_and_passes_modules():
    assert _raw_read_functions(OLD_SOURCE) == ["load_pit_series"]
    for path in PIPELINE.glob("*.py"):
        if path.name.startswith("test_") or path.name == "cutoff_guard.py":
            continue
        assert not _raw_read_functions(path.read_text(encoding="utf-8")), path.name


def _fixture(tmp_path, *, cutoff="2020-01-31", fact_filed="2020-01-01",
             filing_date="2020-01-01", listed="old-submissions-001.json"):
    ticker, case_id = "TST", "C1"
    registry = tmp_path / "cases.json"
    registry.write_text(json.dumps({"cases": [{"case_id": case_id, "ticker": ticker,
                                                "cutoff_date": cutoff}]}), encoding="utf-8")
    edgar = tmp_path / ticker / "edgar"
    xbrl = tmp_path / ticker / "xbrl"
    edgar.mkdir(parents=True)
    xbrl.mkdir(parents=True)
    accession = "0000000000-20-000001"
    submissions = {"filings": {"recent": {"form": ["8-K"],
                    "filingDate": [filing_date], "accessionNumber": [accession],
                    "items": ["1.01"]}, "files": [{"name": listed}]}}
    (edgar / "CIK1.json").write_text(json.dumps(submissions), encoding="utf-8")
    fact = {"filed": fact_filed, "accn": accession, "end": "2019-12-31", "val": 1}
    companyfacts = {"facts": {"us-gaap": {"Assets": {"units": {"USD": [fact]}}}}}
    (xbrl / "CIK1.json").write_text(json.dumps(companyfacts), encoding="utf-8")
    return case_id, ticker, registry


def test_xbrl_filters_logs_and_fixture_log_is_isolated(tmp_path):
    cid, ticker, registry = _fixture(tmp_path, fact_filed="2020-02-01",
                                     filing_date="2020-02-01")
    default = cutoff_guard.DEFAULT_LOG
    before = (default.stat().st_mtime_ns, default.stat().st_size) if default.exists() else None
    rows, metadata = cutoff_guard.load_xbrl_facts(
        cid, ticker, "2020-01-31", data_dir=tmp_path, registry_path=registry)
    assert rows == []
    assert metadata["namespaces"] == ["us-gaap"]
    records = [json.loads(line) for line in
               (tmp_path / "access_log.jsonl").read_text(encoding="utf-8").splitlines()]
    assert any(record["reason"] == "xbrl_accession_index" for record in records)
    assert records[-1]["facts_dropped_post_cutoff"] == 1
    after = (default.stat().st_mtime_ns, default.stat().st_size) if default.exists() else None
    assert after == before


def test_xbrl_accession_date_mismatch_fails(tmp_path):
    cid, ticker, registry = _fixture(tmp_path, fact_filed="2020-01-01",
                                     filing_date="2020-01-02")
    with pytest.raises(cutoff_guard.CutoffGuardError):
        cutoff_guard.load_xbrl_facts(cid, ticker, "2020-01-31",
                                     data_dir=tmp_path, registry_path=registry)


def test_cutoff_mismatch_fails(tmp_path):
    cid, ticker, registry = _fixture(tmp_path)
    with pytest.raises(cutoff_guard.CutoffGuardError):
        cutoff_guard.load_xbrl_facts(cid, ticker, "2020-02-01",
                                     data_dir=tmp_path, registry_path=registry)


def test_chronology_filters_but_preserves_pre_filter_listing(tmp_path):
    cid, ticker, registry = _fixture(tmp_path, cutoff="2019-01-01",
                                     filing_date="2020-01-01")
    rows, metadata = cutoff_guard.load_edgar_chronology(
        cid, ticker, datetime.date(2019, 1, 1), data_dir=tmp_path,
        registry_path=registry)
    assert rows == []
    assert metadata["listed_subfiles"] == ["old-submissions-001.json"]


def test_string_ticker_resolves_and_enforces(tmp_path, monkeypatch):
    cid, ticker, registry = _fixture(tmp_path, fact_filed="2020-02-01",
                                     filing_date="2020-02-01")
    monkeypatch.setattr(build_payload, "EVALUATEE_CASES", registry)
    assert build_payload.load_pit_series(ticker, datetime.date(2020, 1, 31),
                                         data_dir=tmp_path) == {}
    with pytest.raises(cutoff_guard.CutoffGuardError):
        build_payload.load_pit_series("UNKNOWN", datetime.date(2020, 1, 31),
                                      data_dir=tmp_path)
    with pytest.raises(cutoff_guard.CutoffGuardError):
        build_payload.load_pit_series(ticker, datetime.date(2020, 2, 1),
                                      data_dir=tmp_path)


def test_custom_registry_refused_for_real_corpus(tmp_path):
    _, _, registry = _fixture(tmp_path)
    with pytest.raises(cutoff_guard.CutoffGuardError):
        cutoff_guard.load_xbrl_facts("C1", "TST", "2020-01-31",
                                     data_dir=cutoff_guard.DEFAULT_EDGAR_DATA,
                                     registry_path=registry)


def test_repo_internal_fixture_does_not_create_access_log(tmp_path):
    fixture_dir = PIPELINE / "fixtures" / "data"
    log = fixture_dir / "access_log.jsonl"
    assert not log.exists()
    registry = {"cases": [{"case_id": "C1", "ticker": "TST",
                            "cutoff_date": "2015-06-30"}]}
    rows, _ = cutoff_guard.load_edgar_chronology(
        "C1", "TST", "2015-06-30", data_dir=fixture_dir,
        registry_path=registry)
    assert rows
    assert not log.exists()


def test_payload_v2_nondefault_registry_and_prefilter_namespaces(tmp_path, monkeypatch):
    cid, ticker, registry = _fixture(tmp_path, fact_filed="2020-02-01",
                                     filing_date="2020-02-01")
    evaluatee = tmp_path / "evaluatee"
    evaluatee.mkdir()
    nondefault = evaluatee / "cases_wave2.json"
    nondefault.write_text(registry.read_text(encoding="utf-8"), encoding="utf-8")
    monkeypatch.setattr(payload_v2_extract, "EVALUATEE_CASES", evaluatee / "cases.json")
    monkeypatch.setattr(payload_v2_extract, "CASE_FILES", ["cases_wave2.json"])
    case = {"case_id": cid, "ticker": ticker, "cutoff_date": "2020-01-31"}
    facts, coverage = payload_v2_extract.extract_share_facts(case, datetime.date(2020, 1, 31),
                                                              tmp_path, nondefault)
    assert facts == {}
    assert coverage["facts_namespaces_present"] == ["us-gaap"]
    facts, _ = payload_v2_extract.extract_share_facts(ticker, datetime.date(2020, 1, 31),
                                                       tmp_path, nondefault)
    assert facts == {}


def test_payload_v2_identical_registry_matches_collapse(tmp_path, monkeypatch):
    case = {"case_id": "C1", "ticker": "TST", "cutoff_date": "2020-01-31",
            "cik": "0000000001"}
    evaluatee = tmp_path / "evaluatee"
    evaluatee.mkdir()
    for name in ("cases.json", "cases_v2.json"):
        (evaluatee / name).write_text(json.dumps({"cases": [case]}), encoding="utf-8")
    monkeypatch.setattr(payload_v2_extract, "EVALUATEE_CASES", evaluatee / "cases.json")
    monkeypatch.setattr(payload_v2_extract, "CASE_FILES", ["cases.json", "cases_v2.json"])
    resolved, registry = payload_v2_extract._case_and_registry(
        "TST", datetime.date(2020, 1, 31), payload_v2_extract.DATA_DIR)
    assert resolved == case
    assert registry == evaluatee / "cases.json"


def test_payload_v2_disagreeing_registry_matches_fail(tmp_path, monkeypatch):
    evaluatee = tmp_path / "evaluatee"
    evaluatee.mkdir()
    for name, cutoff in (("cases.json", "2020-01-31"),
                         ("cases_v2.json", "2020-02-01")):
        case = {"case_id": name, "ticker": "TST", "cutoff_date": cutoff,
                "cik": "0000000001"}
        (evaluatee / name).write_text(json.dumps({"cases": [case]}), encoding="utf-8")
    monkeypatch.setattr(payload_v2_extract, "EVALUATEE_CASES", evaluatee / "cases.json")
    monkeypatch.setattr(payload_v2_extract, "CASE_FILES", ["cases.json", "cases_v2.json"])
    with pytest.raises(cutoff_guard.CutoffGuardError):
        payload_v2_extract._case_and_registry(
            "TST", datetime.date(2020, 1, 31), payload_v2_extract.DATA_DIR)


@pytest.mark.parametrize("extract", [payload_v2_extract.extract_8k_items,
                                      payload_v2_extract.extract_share_facts])
def test_payload_v2_unknown_ticker_wraps_guard_error(tmp_path, monkeypatch, extract):
    registry = tmp_path / "cases.json"
    registry.write_text(json.dumps({"cases": []}), encoding="utf-8")
    monkeypatch.setattr(payload_v2_extract, "EVALUATEE_CASES", registry)
    monkeypatch.setattr(payload_v2_extract, "CASE_FILES", ["cases.json"])
    with pytest.raises(payload_v2_extract.PayloadV2Error):
        extract("UNKNOWN", datetime.date(2020, 1, 31), payload_v2_extract.DATA_DIR)
