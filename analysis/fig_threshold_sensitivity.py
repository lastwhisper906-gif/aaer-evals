"""Track 1: 플래그 임계 민감도 그림 — FPR-vs-t · TP-vs-t 코호트별.

입력: analysis/threshold_sensitivity.csv (threshold_sweep.py 선행 생성)
출력: analysis/fig_threshold_sensitivity.png
결정론·네트워크 없음. matplotlib Agg. 본 결과는 Claude 기반 단일 파이프라인에 한정.
"""
import csv
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
INK, MUTED, GRID = "#1f2937", "#6b7280", "#e5e7eb"
BAND = "#eef2ff"
# 코호트별 색 (3계열 — 범례 필수)
COLORS = {"wave-1 (8v22)": "#b3261e", "wave-2 (9v23)": "#2f5fa8",
          "holdout (3v0)": "#137a4c"}
PUBLISHED_T = 50


def load_rows():
    out = {}
    for r in csv.DictReader(open(REPO / "analysis/threshold_sensitivity.csv",
                                 encoding="utf-8")):
        out.setdefault(r["cohort"], []).append(r)
    for c in out.values():
        c.sort(key=lambda r: int(r["t"]))
    return out


def fnum(v):
    return float(v) if v not in ("", None) else None


def main() -> int:
    data = load_rows()
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.6, 8.4), dpi=160,
                                   sharex=True)

    for ax in (ax1, ax2):
        ax.axvspan(PUBLISHED_T - 5, PUBLISHED_T + 5, color=BAND, zorder=0)
        ax.axvline(PUBLISHED_T, color=MUTED, lw=1, ls="--", zorder=1)
        ax.grid(True, axis="both", color=GRID, lw=0.6, zorder=0)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)

    # 상단: FPR% vs t (Clopper-Pearson 상한을 옅게 음영). holdout 은 FPR n/a.
    for cohort, rows in data.items():
        ts = [int(r["t"]) for r in rows]
        fpr = [fnum(r["fpr_point_pct"]) for r in rows]
        if all(v is None for v in fpr):
            continue
        hi = [fnum(r["fpr_upper95_pct"]) for r in rows]
        lo = [fnum(r["fpr_lo_pct"]) for r in rows]
        col = COLORS[cohort]
        ax1.plot(ts, fpr, "-o", ms=5, color=col, zorder=3, label=cohort)
        ax1.fill_between(ts, lo, hi, color=col, alpha=0.10, zorder=1)
    ax1.set_ylabel("Control FPR % (point; band = CP 95%)", color=INK)
    ax1.set_title("Flag-threshold sensitivity — FPR and TP vs t "
                  "(shaded = published t=50 ±5)", fontsize=10.5, color=INK)
    ax1.legend(frameon=False, fontsize=8.5, loc="upper right")

    # 하단: TP (검출된 fraud 수) vs t + 민감도 보조축 라벨
    for cohort, rows in data.items():
        ts = [int(r["t"]) for r in rows]
        tp = [int(r["tp"]) for r in rows]
        nf = int(rows[0]["n_fraud"])
        col = COLORS[cohort]
        ax2.plot(ts, tp, "-o", ms=5, color=col, zorder=3,
                 label=f"{cohort} (n_fraud={nf})")
    ax2.set_ylabel("True positives (fraud flagged)", color=INK)
    ax2.set_xlabel("Flag threshold t (score >= t)", color=INK)
    ax2.legend(frameon=False, fontsize=8.5, loc="upper right")
    ax2.set_ylim(0, 9.5)

    fig.tight_layout()
    out = REPO / "analysis/fig_threshold_sensitivity.png"
    fig.savefig(out, facecolor="white")
    print(f"→ {out.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
