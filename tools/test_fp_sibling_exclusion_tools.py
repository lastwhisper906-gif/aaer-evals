"""R3-5: fp-sibling 제외 — R2-5가 놓친 세 소비자 (tools/ 층).

apply_rp13_finalization(blanket 확정·잔존 스캔) · build_rp13_workbench
(채점 dir 글롭) · e2_generate_cases(wave-2 로스터). 판형은
analysis/test_fp_sibling_exclusion.py와 동일.
"""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import apply_rp13_finalization as rp13
import build_rp13_workbench as wb
import e2_generate_cases as e2

REPO = Path(__file__).resolve().parents[1]


def _plant(tmp_path):
    d = tmp_path / "grades"
    d.mkdir()
    (d / "case_01.json").write_text('{"a": 1}', encoding="utf-8")
    (d / "case_01.fp-deadbeef.json").write_text('{"a": 2}', encoding="utf-8")
    (d / "case_02.json").write_text('{"a": 3}', encoding="utf-8")
    return d


def test_rp13_finalization_grade_files_skips_siblings(tmp_path):
    d = _plant(tmp_path)
    names = [Path(p).name for p in rp13.grade_files(d)]
    assert names == ["case_01.json", "case_02.json"]


def test_workbench_grade_files_skips_siblings(tmp_path):
    d = _plant(tmp_path)
    names = [Path(p).name for p in wb.grade_files(d)]
    assert names == ["case_01.json", "case_02.json"]


def test_e2_roster_identical_with_planted_sibling(tmp_path):
    """소비자 수준: 실데이터 사본에 fp-sibling을 심어도 로스터가 불변 —
    sibling 1건이 실험군 행을 이중 생성하면 안 된다."""
    fixture = tmp_path / "repo"
    for rel in ("data/candidates/candidates.json",
                "data/candidates/candidates_wave2.json",
                "data/evaluatee/cases.json", "data/evaluatee/cases_wave2.json",
                "scoring/id_mapping.json", "scoring/id_mapping_wave2.json",
                "analysis/baseline_table.csv"):
        dst = fixture / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(REPO / rel, dst)
    scores_src = REPO / "runs/wave2/scores"
    scores_dst = fixture / "runs/wave2/scores"
    scores_dst.mkdir(parents=True)
    for p in sorted(scores_src.glob("case_*.json")):
        shutil.copy(p, scores_dst / p.name)

    baseline = e2.derive_roster(fixture)

    victim = sorted(scores_dst.glob("case_*.json"))[0]
    record = json.loads(victim.read_text(encoding="utf-8"))
    record["misstatement_probability"] = 99  # 플래그 확정 값 — 걸리면 행이 는다
    (scores_dst / f"{victim.stem}.fp-deadbeef.json").write_text(
        json.dumps(record), encoding="utf-8")

    assert e2.derive_roster(fixture) == baseline, "fp-sibling이 로스터를 바꿈"
