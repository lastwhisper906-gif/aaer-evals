"""R3-4: 게이트 §4 (1)–(5) 오프라인 리허설 — 창 안 신규 코드 0 증명.

mock 회사(픽스처 universe 12건)로 fetch(스텁)→build→source-manifest→
assemble(스텁 러너 출력)→validate 전 구간을 네트워크 0으로 관통한다
(INV-23 — 테스트·도구 기본 경로 모두 픽스처 전용).
"""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_evaluatee_inputs as bei
import fetch_xbrl_facts as fxf
import forward_common
import forward_source_manifest as fsm
import forward_assemble
import forward_validate
from test_forward_tools import PROTOCOL_FIXTURE, make_universe

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "pipeline"))
import build_payload as bp  # noqa: E402

CUTOFF = forward_common.SCREENING_CUTOFF  # 2026-11-15


class _Resp:
    def __init__(self, content: bytes):
        self.content = content


def _accn(i: int, post_cutoff: bool = False) -> str:
    # R4-7(b) 이후 인증은 실형태(10-2-6) accession만 인정한다
    return f"{i:010d}-26-{'999999' if post_cutoff else '000001'}"


def _synthetic_companyfacts(i: int) -> bytes:
    return json.dumps({"facts": {"us-gaap": {"Revenues": {"units": {"USD": [
        {"accn": _accn(i), "filed": "2026-10-01",
         "end": "2026-09-30", "val": 100 + i},
        # 컷오프 이후 제출 — source_manifest에서 걸러져야 한다
        {"accn": _accn(i, post_cutoff=True), "filed": "2026-12-01",
         "end": "2026-11-30", "val": 999},
    ]}}}}}).encode("utf-8")


def _synthetic_submissions(i: int) -> bytes:
    # R7-2: companyfacts의 모든 accn(컷오프 이후 포함)은 submissions 인덱스와
    # 교차 대조된다 — 두 accession 모두 filed 일치로 등재한다.
    return json.dumps({"filings": {"recent": {
        "accessionNumber": [_accn(i), _accn(i, post_cutoff=True)],
        "filingDate": ["2026-10-01", "2026-12-01"],
        "form": ["10-K", "8-K"],
        "items": ["", ""],
    }, "files": []}}).encode("utf-8")


def _model_output(rid: str, i: int) -> dict:
    evidence = {"quote": "Revenues=100 (FY2026)",
                "source_accession_no": _accn(i),
                "location": "Revenues FY2026"}
    return {
        "case_id": rid, "run_id": f"original-{rid}-r1", "model": "claude-sonnet-5",
        "pipeline_version": "a" * 40, "run_timestamp": "2026-11-16T00:00:00+00:00",
        "documents_used": [{"accession_no": _accn(i), "form_type": "10-K",
                            "filing_date": "2026-10-01"}],
        "checklist": [{"item_id": "CL1", "question": "q", "finding": "no_flag",
                       "confidence": "medium", "evidence": [evidence]}],
        "misstatement_probability": 30 + i,
        "mechanism_hypotheses": [],
        "overall": {"risk_tier": "watch", "top_signals": ["synthetic signal"]},
        # R3-7: 러너 call-time fingerprint — validate가 조립 해시와 대조
        "fingerprint": {"system_prompt_sha256": "f" * 64,
                        "schema_sha256": forward_common.sha256_file(
                            REPO / "schemas/llm_output.json"),
                        "pipeline_commit": "a" * 40,
                        "model_requested": "claude-sonnet-5"},
    }


@pytest.fixture()
def clean_env(monkeypatch):
    for var in forward_common.METERED_CREDENTIAL_VARS:
        monkeypatch.delenv(var, raising=False)


def test_gate_steps_dry_run_end_to_end(tmp_path, monkeypatch, clean_env):
    universe = make_universe(12)
    cycle = tmp_path / "forward/cycle_099"
    cycle.mkdir(parents=True)
    forward_common.write_json(cycle / "universe.json", universe)
    (cycle / "PROTOCOL.md").write_text(PROTOCOL_FIXTURE, encoding="utf-8")

    # (2) fetch — 스텁, 네트워크 0
    served = {}

    def fake_fetch(url):
        i = int(url.split("CIK")[1][:10]) - 1000
        served[url] = True
        if "/submissions/" in url:
            return _Resp(_synthetic_submissions(i))
        return _Resp(_synthetic_companyfacts(i))

    monkeypatch.setattr(fxf, "fetch", fake_fetch)
    dest = tmp_path / "data_forward"
    assert fxf.fetch_forward(cycle / "universe.json", dest) == 0
    # R15-1: 수집 로그는 dest가 아니라 정본 경로(git 관리)에 쓴다
    assert fxf.fetch_log_path().exists()
    assert not (dest / "fetch_log.jsonl").exists()
    assert len(served) == 24  # companyfacts 12 + submissions 12

    # R7-2: fetch 배치는 러너(cutoff_guard)가 읽는 {ticker}/{xbrl,edgar} 형태
    for r in universe["selected"]:
        cik10 = str(r["cik"]).zfill(10)
        assert (dest / r["ticker"] / "xbrl" / f"CIK{cik10}.json").exists()
        assert (dest / r["ticker"] / "edgar" / f"CIK{cik10}.json").exists()

    # R8-1: 쓴 파일마다 로그 행 — 수·kind·sha256 전건 정합 (submissions 포함)
    import hashlib as _hl
    log_rows = [json.loads(line) for line in
                fxf.fetch_log_path().read_text(encoding="utf-8").splitlines()]
    written = sorted(dest.glob("*/*/CIK*.json"))
    assert len(log_rows) == len(written) == 24
    by_path = {r["path"]: r for r in log_rows}
    for f in written:
        row = by_path[fxf.portable_path(f)]
        assert row["sha256"] == _hl.sha256(f.read_bytes()).hexdigest()
        assert row["kind"] == ("companyfacts" if f.parent.name == "xbrl"
                               else "submissions")

    # (3) build — universe → 피평가자 케이스 파일 (화이트리스트 계약 준수)
    payload = bei.build_forward(cycle / "universe.json", CUTOFF)
    assert len(payload["cases"]) == 12
    for case in payload["cases"]:
        bp.assert_case_whitelisted(case)
        assert case["cutoff_date"] == CUTOFF

    # (3b) R7-2: fetch가 쓴 corpus를 러너 경로(build_payload→cutoff_guard)가
    # 실제로 읽어 payload를 만든다 — fetch→payload 이음매 리허설. 창 안에서
    # 필요한 코드 수정 0을 여기서 증명한다 (네트워크 0, 픽스처 corpus 루트).
    monkeypatch.setattr(bp, "DATA_DIR", dest)
    for case in payload["cases"]:
        built = bp.build_payload(case)
        assert built["_variant"] == "original"
        series = built["financial_series_point_in_time"]
        assert series.get("Revenues"), f"{case['case_id']}: 빈 시계열 — 러너가 fetch 배치를 못 읽음"
        # 컷오프 이후(2026-12-01) 제출은 시계열·연대기 모두에서 배제
        assert all(v["filed"] <= CUTOFF for v in series["Revenues"])
        assert built["filing_chronology"] == [
            {"form": "10-K", "filing_date": "2026-10-01"}]

    # (2b) source_manifest 방출 — 컷오프 이후 accession은 배제
    sources = fsm.build_sources(dest, CUTOFF)
    forward_common.write_json(cycle / "source_manifest.json",
                              {"generated_by": "test", "cutoff": CUTOFF,
                               "sources": sources})
    accs = {s["accession_no"] for s in sources}
    assert len(accs) == 12
    assert all(a.endswith("-26-000001") for a in accs), "컷오프 이후 accession 누출"
    for s in sources:
        assert s["url"] and s["retrieval_date"] and s["sha256"] and s["filing_date"]

    # (4) 러너 출력 스텁 → assemble
    runs = tmp_path / "runs_forward"
    runs.mkdir()
    for i, r in enumerate(universe["selected"], start=1):
        (runs / f"{r['record_id']}.json").write_text(
            json.dumps(_model_output(r["record_id"], i)), encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["forward_assemble.py", "--cycle", str(cycle),
                                      "--runs", str(runs)])
    assert forward_assemble.main() == 0

    # (5) validate — 전 구간 정합, 신규 코드 0으로 PASS. runs_dir 전달로
    # R5-1 재해시 leg까지 리허설: assemble이 계산한 run_output_sha256와
    # validate의 실측 재해시 규약이 어긋나면 여기서 red (R6-6) — 창 안이
    # 아니라 지금 잡힌다. (실제 assemble 산출 해시 — 수기 해시 아님.)
    errs = forward_validate.validate(cycle, runs_dir=runs)
    assert errs == [], errs[:10]


def test_forward_build_requires_out_and_retro_default_unchanged(tmp_path, monkeypatch):
    """회고 기본 경로 회귀: 인자 없는 build()는 커밋본과 동일 payload를 만든다
    (바이트 대조는 test_build_evaluatee_inputs가 이미 상시 수행 — 여기서는
    forward 분기가 회고 경로를 건드리지 않았음을 이중 확인)."""
    payload, mapping = bei.build()
    committed = json.loads(
        (REPO / "data/evaluatee/cases.json").read_text(encoding="utf-8"))
    assert payload == committed


def test_refetch_does_not_duplicate_source_manifest(tmp_path, monkeypatch, clean_env):
    """R4-7(d): fetch 재시도(append 로그) 후 build가 record_id당 최신 행만
    채택 — 상충 sha256의 accession 이중 등재 금지."""
    universe = make_universe(12)
    upath = tmp_path / "universe.json"
    forward_common.write_json(upath, universe)

    def fake_fetch(url):
        i = int(url.split("CIK")[1][:10]) - 1000
        return _Resp(_synthetic_companyfacts(i))

    import fetch_xbrl_facts as fxf_mod
    monkeypatch.setattr(fxf_mod, "fetch", fake_fetch)
    dest = tmp_path / "data_forward"
    assert fxf_mod.fetch_forward(upath, dest) == 0
    single = fsm.build_sources(dest, CUTOFF)
    assert fxf_mod.fetch_forward(upath, dest) == 0  # 재시도 — 로그 append
    double = fsm.build_sources(dest, CUTOFF)
    assert double == single
    accs = [s["accession_no"] for s in double]
    assert len(accs) == len(set(accs)) == 12


def test_invalid_submissions_json_aggregates_failure_without_corrupt_write(
        tmp_path, monkeypatch, clean_env):
    """R8-6: 200 + 절단 본문 → 그 레코드만 실패 집계(exit 1), 손상 바이트는
    디스크에 남지 않고, 나머지 레코드는 정상 수집."""
    universe = make_universe(2)
    upath = tmp_path / "universe.json"
    forward_common.write_json(upath, universe)

    def fake_fetch(url):
        i = int(url.split("CIK")[1][:10]) - 1000
        if "/submissions/" in url:
            if i == 1:
                return _Resp(b'{"filings": {"recent"')  # 절단 JSON
            return _Resp(_synthetic_submissions(i))
        return _Resp(_synthetic_companyfacts(i))

    monkeypatch.setattr(fxf, "fetch", fake_fetch)
    dest = tmp_path / "d"
    assert fxf.fetch_forward(upath, dest) == 1
    r1, r2 = universe["selected"]
    assert not (dest / r1["ticker"] / "edgar" / "CIK0000001001.json").exists()
    assert (dest / r1["ticker"] / "xbrl" / "CIK0000001001.json").exists()
    assert (dest / r2["ticker"] / "edgar" / "CIK0000001002.json").exists()
    assert (dest / r2["ticker"] / "xbrl" / "CIK0000001002.json").exists()


def test_submissions_row_after_companyfacts_does_not_clobber_manifest(tmp_path):
    """R8-1 trap: record_id 키 최신-행 dedup에 submissions 행이 섞이면
    companyfacts 행을 클로버해 그 레코드의 매니페스트가 조용히 빈다 —
    build_sources는 kind=companyfacts 행만 소비해야 한다."""
    dest = tmp_path / "d"
    cf = dest / "TK01" / "xbrl" / "CIK0000001001.json"
    cf.parent.mkdir(parents=True)
    cf.write_bytes(_synthetic_companyfacts(1))
    sub = dest / "TK01" / "edgar" / "CIK0000001001.json"
    sub.parent.mkdir(parents=True)
    sub.write_bytes(_synthetic_submissions(1))
    rows = [{"record_id": "fw001-r01", "kind": "companyfacts", "cik": "0000001001",
             "url": "u-cf", "retrieval_date": "t1", "sha256": "s1", "path": str(cf)},
            # 뒤 행이 submissions — 무필터면 latest[rid]를 클로버한다
            {"record_id": "fw001-r01", "kind": "submissions", "cik": "0000001001",
             "url": "u-sub", "retrieval_date": "t2", "sha256": "s2", "path": str(sub)}]
    # R15-1: 픽스처 로그도 정본 경로에 둔다 (build_sources가 읽는 유일한 파일)
    log_path = fxf.fetch_log_path()
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(
        "\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    sources = fsm.build_sources(dest, CUTOFF)
    assert {s["accession_no"] for s in sources} == {_accn(1)}
    assert all(s["url"] == "u-cf" for s in sources)
