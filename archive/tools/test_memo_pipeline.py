"""memo 파이프라인 일반화(P1+P3) 게이트 테스트 — 무호출.

세 가지를 강제한다:
1. 상수·로직 상속: memo_run의 INSTRUCTION/SCHEMA가 blind_memo_run과 동일,
   memo_extract의 HTML→텍스트가 blind_memo_extract와 소스 동일,
   memo_verify의 매칭 4함수가 blind_memo_verify와 소스 동일.
2. GIL 재현 게이트: memo_run이 조립한 annual/combined 페이로드의 sha256이
   동결 blind_memo_run.build_payload 출력과 동일. 동결 실행은 페이로드
   해시를 기록하지 않았으므로(call_*.json은 호출 메타만 보존) 기대 해시는
   "동결 원본 모듈의 build_payload를 커밋된 입력(data/gil/*.txt·registry·
   flags_annual.json) 위에서 인프로세스 실행"해 유도한다 — 원본 코드가
   기대값의 단일 출처다. ~/aaer-data/GIL 부재 환경(CI)에서는 skip
   (cutoff_guard의 EDGAR filingDate 교차검증이 로컬 submissions JSON 필요).
3. 판정 큐 라우팅: VERIFIED는 침묵, 비-VERIFIED만 4택 체크리스트 블록.
"""
from __future__ import annotations

import hashlib
import inspect
import json
from pathlib import Path

import pytest

import blind_memo_extract as bme
import blind_memo_run as bmr
import blind_memo_verify as bmv
import memo_extract as me
import memo_run as mr
import memo_verify as mv

REPO = Path(__file__).resolve().parents[1]
GIL_RAW = Path.home() / "aaer-data" / "GIL"


def test_instruction_and_schema_inherited_byte_identical():
    assert mr.INSTRUCTION == bmr.INSTRUCTION
    assert mr.SCHEMA == bmr.SCHEMA


def test_extract_logic_inherited_source_identical():
    assert inspect.getsource(me.html_to_text) == inspect.getsource(bme.html_to_text)
    assert inspect.getsource(me.FilingTextExtractor) == inspect.getsource(bme.FilingTextExtractor)
    assert me.BLOCK_TAGS == bme.BLOCK_TAGS


def test_verify_matching_inherited_source_identical():
    for fn in ("normalize", "best_window", "check_quote", "status_of"):
        assert inspect.getsource(getattr(mv, fn)) == inspect.getsource(getattr(bmv, fn)), fn


def _gil_cfg(tmp_path: Path) -> "mr.MemoConfig":
    return mr.MemoConfig(
        registry=REPO / "data/gil/registry.json",
        case_id="OUT-GIL-V1",
        docs_manifest=REPO / "data/gil/memo_docs.json",
        out=tmp_path,
        prior_flags_path=REPO / "runs/gil_memo_v1/flags_annual.json",
    )


@pytest.mark.skipif(not GIL_RAW.exists(),
                    reason="~/aaer-data/GIL 부재 (CI) — EDGAR 교차검증 원본 없음")
def test_gil_reproduction_gate(tmp_path):
    """일반화가 아무것도 바꾸지 않았다는 증명 — 페이로드 바이트 동일."""
    cfg = _gil_cfg(tmp_path)

    frozen_annual = bmr.build_payload(bmr.ANNUAL_DOCS)
    new_annual, prior_a = mr.stage_payload(cfg, "annual")
    assert prior_a is False
    assert hashlib.sha256(new_annual.encode()).hexdigest() == \
        hashlib.sha256(frozen_annual.encode()).hexdigest()

    prior = json.loads((REPO / "runs/gil_memo_v1/flags_annual.json").read_text())
    frozen_combined = bmr.build_payload(bmr.COMBINED_DOCS, prior_flags=prior)
    new_combined, prior_c = mr.stage_payload(cfg, "combined")
    assert prior_c is True
    assert hashlib.sha256(new_combined.encode()).hexdigest() == \
        hashlib.sha256(frozen_combined.encode()).hexdigest()


@pytest.mark.skipif(not GIL_RAW.exists(),
                    reason="~/aaer-data/GIL 부재 (CI) — EDGAR 교차검증 원본 없음")
def test_gil_dry_run_writes_manifest_and_no_outputs(tmp_path):
    cfg = _gil_cfg(tmp_path)
    manifest = mr.dry_run(cfg, ["annual", "combined"])
    assert set(manifest["stages"]) == {"annual", "combined"}
    for st in manifest["stages"].values():
        assert len(st["payload_sha256"]) == 64
        assert st["est_input_tokens"] == st["chars"] // 4
        assert all(d["cutoff_verdict"] == "allowed" for d in st["documents"])
    assert (tmp_path / "DRYRUN_MANIFEST.json").exists()
    assert not (tmp_path / "flags_annual.json").exists()  # 호출 산출물 없음 = 무호출


def test_adjudication_queue_routes_only_non_verified(tmp_path):
    corpus_raw = ("The company reported revenue of $100 million in fiscal 2025. "
                  "Receivables grew to $40 million at year end.")
    corpora = {"doc.txt": mv.normalize(corpus_raw)}
    rows = []
    for i, (quote, title) in enumerate(
            [("revenue of $100 million in fiscal 2025", "ok-flag"),
             ("the auditors resigned amid an investigation", "bad-flag")], 1):
        res = mv.check_quote(quote, corpora)
        rows.append({"flag": i, "flag_title": title, "quote_no": 1, "quote": quote,
                     "claimed_location": "doc p.1", "status": mv.status_of(res), **res})
    assert rows[0]["status"] == "VERIFIED" and rows[1]["status"] == "NOT FOUND"

    qpath = tmp_path / "adjudication_queue.md"
    n = mv.write_adjudication_queue(qpath, "flags_test.json", rows, corpora)
    text = qpath.read_text(encoding="utf-8")
    assert n == 1
    assert "bad-flag" in text and "ok-flag" not in text  # VERIFIED는 침묵
    for opt in mv.VERDICT_OPTIONS:
        assert opt in text
    assert "수기 판정 소요" in text and "서명" in text


def test_adjudication_queue_empty_when_all_verified(tmp_path):
    corpora = {"doc.txt": mv.normalize("alpha beta gamma")}
    rows = [{"flag": 1, "flag_title": "f", "quote_no": 1, "quote": "alpha beta",
             "claimed_location": "d", "status": "VERIFIED",
             "exact": True, "similarity": 1.0, "matched_doc": "doc.txt"}]
    n = mv.write_adjudication_queue(tmp_path / "q.md", "f.json", rows, corpora)
    assert n == 0
    assert "판정 대상 없음" in (tmp_path / "q.md").read_text(encoding="utf-8")
