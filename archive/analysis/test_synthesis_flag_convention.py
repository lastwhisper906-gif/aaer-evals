"""C1B-01 divergence lock: synthesis m_flag must equal the frozen baseline rule.

The 2026-08-05 C1B review found synthesis.py flagging m <= -1.78 while the
frozen rule (scoring/baselines/screens.py flag_minus_1_78, docs/
baseline_screens.md) is m > -1.78. This test pins the two rules together so
they can never diverge silently again (D-P70).
"""
import importlib.util
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "analysis"))
spec = importlib.util.spec_from_file_location("synthesis", REPO / "analysis" / "synthesis.py")


def test_m_flag_matches_frozen_baseline_rule():
    src = (REPO / "analysis" / "synthesis.py").read_text(encoding="utf-8")
    assert "int(m > M_FLAG)" in src and "int(m <= M_FLAG)" not in src
    frozen = (REPO / "scoring" / "baselines" / "screens.py").read_text(encoding="utf-8")
    assert "m > -1.78" in frozen  # the rule this file must mirror


def test_median_uses_statistics_median():
    src = (REPO / "analysis" / "synthesis.py").read_text(encoding="utf-8")
    assert "statistics.median" in src
    assert "sorted(fr)[len(fr) // 2]" not in src
