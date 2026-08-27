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
        return _Resp(_synthetic_companyfacts(i))

    monkeypatch.setattr(fxf, "fetch", fake_fetch)
    dest = tmp_path / "data_forward"
    assert fxf.fetch_forward(cycle / "universe.json", dest) == 0
    assert (dest / "fetch_log.jsonl").exists()
    assert len(served) == 12

    # (3) build — universe → 피평가자 케이스 파일 (화이트리스트 계약 준수)
    payload = bei.build_forward(cycle / "universe.json", CUTOFF)
    assert len(payload["cases"]) == 12
    for case in payload["cases"]:
        bp.assert_case_whitelisted(case)
        assert case["cutoff_date"] == CUTOFF

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

    # (5) validate — 전 구간 정합, 신규 코드 0으로 PASS
    errs = forward_validate.validate(cycle)
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
