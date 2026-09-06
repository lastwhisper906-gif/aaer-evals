"""R2-5: fp-sibling(case_NN.fp-XXXX.json) 제외 — 모든 case_*.json 소비자.

runner.py는 stale-superseded 출력을 fp-sibling 파일명으로 기록하며, 이는
`case_*.json` 글롭에 걸린다. 소비자별로 케이스당 정본 1건의 결정론적
읽기를 검증한다 (이중 채점·이중 집계·파일시스템 순서 비결정 방지, INV-02).
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
for sub in ("pipeline", "scoring", "tools", "analysis"):
    sys.path.insert(0, str(REPO / sub))

import grader_runner as gr  # noqa: E402
import reproduce_analysis as ra  # noqa: E402
import wave2_analyze  # noqa: E402


def _write(root: Path, relative: str, value: dict) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def _pair(root: Path, directory: str, cid: str, canonical_p: int, stale_p: int) -> None:
    _write(root, f"{directory}/{cid}.json",
           {"case_id": cid, "misstatement_probability": canonical_p})
    _write(root, f"{directory}/{cid}.fp-deadbeef.json",
           {"case_id": cid, "misstatement_probability": stale_p})


def test_grader_iter_run_files_skips_fp_siblings(tmp_path):
    _pair(tmp_path, "runs", "case_01", 50, 99)
    _write(tmp_path, "runs/case_02.json", {"case_id": "case_02"})
    files = gr.iter_run_files(tmp_path / "runs", "case_*.json")
    assert [p.name for p in files] == ["case_01.json", "case_02.json"]


def test_wave2_load_scores_reads_one_deterministic_record(tmp_path):
    _pair(tmp_path, "scores", "case_01", 50, 99)
    _write(tmp_path, "mapping.json", {"mapping": {"case_01": "T01"}})
    scores = wave2_analyze.load_scores(str(tmp_path / "scores"),
                                       str(tmp_path / "mapping.json"))
    assert scores == {"T01": 50}


def test_wave2_load_wave1_scores_no_double_count(tmp_path, monkeypatch):
    _write(tmp_path, "scoring/id_mapping.json",
           {"mapping": {"case_01": "T07", "case_02": "C01"}})
    _pair(tmp_path, "runs/main", "case_01", 50, 99)
    _pair(tmp_path, "runs/rp09/scores", "case_02", 30, 88)
    monkeypatch.chdir(tmp_path)
    fraud, control = wave2_analyze.load_wave1_scores()
    assert fraud == [50], "fp-sibling이 이중 집계됨"
    assert control == [30]


def test_reproduce_load_p_and_grades_skip_fp_siblings(tmp_path):
    _pair(tmp_path, "d", "case_01", 50, 99)
    p = ra.load_p(str(tmp_path / "d"))
    grades = ra.load_grades(str(tmp_path / "d"))
    assert p == {"case_01": 50}
    assert list(grades) == ["case_01"]


# 주: 스키마 스위프의 fp-sibling 취급은 R3-12에서 '포함'으로 결정 —
# pipeline/test_output_schema_enforcement.py::test_fp_sibling_is_swept_for_schema_validity
# 가 관할한다. 이 파일은 소비자(집계·채점·재현) 제외만 다룬다.


# ── R4-5: 마지막 세 분석기 (analyze_rp07·analyze_hardening·power_precompute) ─

def test_remaining_analyzer_load_p_skip_siblings(tmp_path, monkeypatch):
    import analyze_hardening
    import analyze_rp07
    import power_precompute_rp09
    _pair(tmp_path, "d", "case_01", 50, 99)
    for mod in (analyze_rp07, power_precompute_rp09):
        monkeypatch.setattr(mod, "REPO", tmp_path)
        assert mod.load_p("d") == {"case_01": 50}, mod.__name__
    monkeypatch.setattr(analyze_hardening, "REPO", tmp_path)
    assert analyze_hardening.load_p("d") == {"case_01": 50}
