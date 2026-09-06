"""R1-20: reproduce A3 — draws 실재 + 통계 부재/수 불일치의 명시 FAIL."""
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "tools"))
import reproduce_analysis as ra  # noqa: E402


def test_a3_stats_missing_predicate():
    """draws 실재 + a3_sampling 부재 → FAIL check 등록 조건 참."""
    assert ra.a3_stats_missing({}, draws_exist=True)
    assert ra.a3_stats_missing({"other": 1}, draws_exist=True)
    assert not ra.a3_stats_missing({"a3_sampling": {}}, draws_exist=True)
    assert not ra.a3_stats_missing({}, draws_exist=False)  # 부재는 실패가 아님 (원 규약)


def test_real_tree_101_checks_green():
    """실트리: draw-수 ↔ per_draw_stats-수 일치 check가 등록되어 총 101/101 —
    zip 절단으로 조용히 줄어들면 여기서 100/100로 회귀해 red."""
    out = subprocess.run([sys.executable, str(REPO / "tools/reproduce_analysis.py")],
                         capture_output=True, text=True)
    assert out.returncode == 0, out.stdout[-800:]
    assert "101/101" in out.stdout, out.stdout[-200:]
