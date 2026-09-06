"""RP-10 Phase 3.5: 암기-vs-분석 분해 산점도 (프로젝트의 가장 새로운 그림).

x = 원본 프레임 점수 (k=5 평균, runs/main + runs/rp07 — 동결)
y = 정체 교란 delta = 교란 평균 − 원본 평균 (음수 = 정체 제거가 점수를 깎음
    = 암기된-유죄 방향; 양수 = 유명 이름의 무죄 사전확률 방향)
오차 막대 = ±2·SE(Δmean) (RP-07 완결 분해 — 크기의 정직성)

출력: analysis/fig_memorization_decomposition.png  (결정론 — 시각 요소 고정)
"""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

REPO = Path(__file__).resolve().parents[1]

INK = "#1f2937"       # text tokens
MUTED = "#6b7280"
GRID = "#e5e7eb"
POINT = "#2f5fa8"     # 단일 시리즈 1색 (범례 불요 — 제목이 시리즈를 명명)


def main() -> int:
    s = json.loads((REPO / "scoring/rp07_stats.json").read_text())
    rows = []
    for d in s["delta_decomposition_completed"]:
        pc = s["per_case"][d["case_id"]]
        rows.append({"ticker": d["ticker"], "x": pc["orig_mean"],
                     "y": -d["delta_mean_orig_minus_pert"],  # pert − orig
                     "se2": 2 * d["se_delta_mean"]})

    fig, ax = plt.subplots(figsize=(7.2, 5.2), dpi=160)
    ax.axhline(0, color=MUTED, lw=1, zorder=1)
    ax.errorbar([r["x"] for r in rows], [r["y"] for r in rows],
                yerr=[r["se2"] for r in rows], fmt="o", ms=9,
                color=POINT, ecolor=MUTED, elinewidth=1.2, capsize=3, zorder=3)
    off = {"HTZ": (6, -4), "MON": (6, 4), "KHC": (6, 4), "SCOR": (6, 4),
           "OFIX": (6, 4), "LOGI": (6, -12), "ICON": (6, -12), "MRVL": (6, 4)}
    for r in rows:
        dx, dy = off.get(r["ticker"], (6, 4))
        ax.annotate(r["ticker"], (r["x"], r["y"]), textcoords="offset points",
                    xytext=(dx, dy), fontsize=9, color=INK)
    ax.annotate("Hertz −30.2pp: memorized guilt\n(removing identity drops the score)",
                (rows[[r["ticker"] for r in rows].index("HTZ")]["x"],
                 rows[[r["ticker"] for r in rows].index("HTZ")]["y"]),
                textcoords="offset points", xytext=(-150, -38), fontsize=8.5,
                color=INK, arrowprops={"arrowstyle": "-", "color": MUTED, "lw": 0.8})
    ax.annotate("Monsanto +15.8pp: famous-name\ninnocence prior (name suppresses score)",
                (rows[[r["ticker"] for r in rows].index("MON")]["x"],
                 rows[[r["ticker"] for r in rows].index("MON")]["y"]),
                textcoords="offset points", xytext=(30, 26), fontsize=8.5,
                color=INK, arrowprops={"arrowstyle": "-", "color": MUTED, "lw": 0.8})
    ax.set_xlabel("Base score, identity visible (original frame, k=5 mean)", color=INK)
    ax.set_ylabel("Identity-perturbation delta (perturbed − original, pp)", color=INK)
    ax.set_title("How much of the score is the NAME? — 8 fraud cases\n"
                 "(error bars = ±2·SE from k=5 redraws on both sides; above 0 = name suppressed the score)",
                 fontsize=10.5, color=INK)
    ax.grid(True, color=GRID, lw=0.6, zorder=0)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    for sp in ("left", "bottom"):
        ax.spines[sp].set_color(MUTED)
    ax.tick_params(colors=MUTED)
    fig.tight_layout()
    dest = REPO / "analysis/fig_memorization_decomposition.png"
    fig.savefig(dest, facecolor="white")
    print(f"→ {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
