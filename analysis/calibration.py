"""RP-10 Phase 3.4: 보정 — ECE(10-bin) + 신뢰도 다이어그램 + 확신-정오 AUROC.

정의 (사전 명시):
  예측 확률 = misstatement_probability/100 (모델의 유일한 확률 출력),
  라벨 = fraud 1 / control 0 (원본 프레임 30사).
  확신 = |p − 50|/50 (플래그 임계로부터의 거리), 정오 = 임계 판정의 정오.
  "확신이 무정보"라는 귀무 결과도 보고 대상 발견이다.
출력: analysis/calibration.json + analysis/fig_reliability.png
"""
import csv
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
INK, MUTED, GRID, BAR = "#1f2937", "#6b7280", "#e5e7eb", "#2f5fa8"


def main() -> int:
    rows = list(csv.DictReader(open(REPO / "analysis/baseline_table.csv", encoding="utf-8")))
    pts = [(float(r["llm_score"]) / 100, 1 if r["group"] == "fraud" else 0)
           for r in rows if r["llm_score"] not in ("", "None")]
    n = len(pts)

    bins = [[] for _ in range(10)]
    for p, y in pts:
        bins[min(9, int(p * 10))].append((p, y))
    ece = 0.0
    diag = []
    for i, b in enumerate(bins):
        if not b:
            diag.append(None)
            continue
        conf = sum(p for p, _ in b) / len(b)
        acc = sum(y for _, y in b) / len(b)
        ece += len(b) / n * abs(acc - conf)
        diag.append({"bin": f"{i/10:.1f}-{(i+1)/10:.1f}", "n": len(b),
                     "mean_pred": round(conf, 3), "frac_fraud": round(acc, 3)})

    correct = [(abs(p - 0.5) / 0.5, 1 if ((p >= 0.5) == (y == 1)) else 0) for p, y in pts]
    pos = [c for c, ok in correct if ok]
    neg = [c for c, ok in correct if not ok]
    if pos and neg:
        gt = sum(1 for a in pos for b in neg if a > b)
        eq = sum(1 for a in pos for b in neg if a == b)
        auroc = (gt + 0.5 * eq) / (len(pos) * len(neg))
    else:
        auroc = None

    out = {"n": n, "ece_10bin": round(ece, 4), "reliability_bins": diag,
           "confidence_definition": "|p-50|/50, 정오 = p>=50 임계 판정의 정오",
           "auroc_confidence_vs_correctness": None if auroc is None else round(auroc, 4),
           "note": "라벨 기저율 8/30 = 0.267 — 완전 보정이면 fraud 비율이 예측 확률을 따라야 함"}
    (REPO / "analysis/calibration.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

    xs, accs, ns = [], [], []
    for i, d in enumerate(diag):
        if d:
            xs.append(i / 10 + 0.05)
            accs.append(d["frac_fraud"])
            ns.append(d["n"])
    fig, ax = plt.subplots(figsize=(5.6, 4.4), dpi=160)
    ax.plot([0, 1], [0, 1], color=MUTED, lw=1, ls="--", label="perfect calibration")
    ax.bar(xs, accs, width=0.09, color=BAR, zorder=3)
    for x, a, m in zip(xs, accs, ns):
        ax.annotate(f"n={m}", (x, a), textcoords="offset points", xytext=(0, 4),
                    ha="center", fontsize=8, color=INK)
    ax.set_xlabel("Predicted misstatement probability (bin)", color=INK)
    ax.set_ylabel("Observed fraud fraction", color=INK)
    ax.set_title(f"Reliability diagram, 30 firms — ECE(10-bin) = {ece:.3f}",
                 fontsize=10.5, color=INK)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.05)
    ax.grid(True, color=GRID, lw=0.6, zorder=0)
    ax.legend(frameon=False, fontsize=8.5)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    fig.tight_layout()
    fig.savefig(REPO / "analysis/fig_reliability.png", facecolor="white")
    print(json.dumps(out, ensure_ascii=False, indent=1)[:600])
    return 0


if __name__ == "__main__":
    sys.exit(main())
