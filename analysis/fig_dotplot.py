"""RP-10 계획 §2: 1차 시각화 — 30사 점수 점 플롯 전체 공개 (요약이 아니라 전 데이터).

출력: analysis/fig_dotplot_30firms.png
"""
import csv
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
INK, MUTED, GRID = "#1f2937", "#6b7280", "#e5e7eb"
FRAUD, CTRL = "#b3261e", "#2f5fa8"  # 2계열 — 범례 필수


def main() -> int:
    rows = [r for r in csv.DictReader(open(REPO / "analysis/baseline_table.csv",
                                           encoding="utf-8"))
            if r["llm_score"] not in ("", "None")]
    rows.sort(key=lambda r: float(r["llm_score"]))
    fig, ax = plt.subplots(figsize=(7.4, 8.2), dpi=160)
    ax.axvline(50, color=MUTED, lw=1, ls="--", zorder=1)
    ax.annotate("flag threshold p=50\n(pre-frozen rubric)", (50, len(rows) - 0.4),
                fontsize=8, color=MUTED, ha="left", xytext=(52, len(rows) - 1.2),
                textcoords="data")
    for i, r in enumerate(rows):
        y = i
        fraud = r["group"] == "fraud"
        ax.plot([0, float(r["llm_score"])], [y, y], color=GRID, lw=0.8, zorder=1)
        ax.plot(float(r["llm_score"]), y, "o", ms=8,
                color=FRAUD if fraud else CTRL, zorder=3)
        ax.annotate(f"{r['ticker']}", (0, y), xytext=(-6, -2.5),
                    textcoords="offset points", ha="right", fontsize=8,
                    color=INK, fontweight="bold" if fraud else "normal")
    ax.set_yticks([])
    ax.set_xlim(0, 100)
    ax.set_ylim(-1, len(rows))
    ax.set_xlabel("Misstatement probability (evaluatee output, original frame)",
                  color=INK)
    ax.set_title("All 30 firms, every score shown — 8 AAER fraud vs 22 matched controls",
                 fontsize=10.5, color=INK)
    ax.plot([], [], "o", color=FRAUD, label="fraud (AAER ground truth, n=8)")
    ax.plot([], [], "o", color=CTRL, label="control (n=22)")
    ax.legend(frameon=False, fontsize=9, loc="lower right")
    ax.grid(True, axis="x", color=GRID, lw=0.6, zorder=0)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    fig.tight_layout()
    fig.savefig(REPO / "analysis/fig_dotplot_30firms.png", facecolor="white")
    print("→ analysis/fig_dotplot_30firms.png")
    return 0


if __name__ == "__main__":
    sys.exit(main())
