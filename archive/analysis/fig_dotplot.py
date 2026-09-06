"""RP-10 계획 §2: 1차 시각화 — 30사 점수 점 플롯 전체 공개 (요약이 아니라 전 데이터).

출력: analysis/fig_dotplot_30firms.png
"""
import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DATA_PATH = REPO / "analysis/baseline_table.csv"
DEFAULT_OUT = REPO / "analysis/fig_dotplot_30firms.png"
SIDECAR_PATH = REPO / "analysis/fig_dotplot_30firms.sidecar.json"
INK, MUTED, GRID = "#1f2937", "#6b7280", "#e5e7eb"
FRAUD, CTRL = "#b3261e", "#2f5fa8"  # 2계열 — 범례 필수
X_LABEL = "Evaluatee risk score (0-100, ordinal; original frame)"
THRESHOLD_ANNOTATION = "flag threshold T=50\n(pre-frozen rubric)"
FRAUD_LABEL = "fraud (AAER ground truth, n=8)"
CONTROL_LABEL = "control (n=22)"


def _rows() -> list[dict]:
    with DATA_PATH.open(encoding="utf-8", newline="") as handle:
        rows = [r for r in csv.DictReader(handle)
                if r["llm_score"] not in ("", "None")]
    rows.sort(key=lambda r: float(r["llm_score"]))
    return rows


def _canonical_digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"),
                         ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def compute_sidecar() -> dict:
    rows = _rows()
    plotted_rows = [
        {key: row[key] for key in ("case_id", "group", "llm_score")}
        for row in rows
    ]
    return {
        "figure": "fig_dotplot_30firms.png",
        "data_sha256": _canonical_digest(plotted_rows),
        "xlabel": X_LABEL,
        "annotations": ([THRESHOLD_ANNOTATION]
                        + [row["ticker"] for row in rows]
                        + [FRAUD_LABEL, CONTROL_LABEL]),
        "generator": "analysis/fig_dotplot.py",
    }


def _write_sidecar(sidecar: dict) -> None:
    SIDECAR_PATH.write_text(
        json.dumps(sidecar, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--sidecar-only", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    sidecar = compute_sidecar()
    if args.sidecar_only:
        _write_sidecar(sidecar)
        return 0

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    rows = _rows()
    fig, ax = plt.subplots(figsize=(7.4, 8.2), dpi=160)
    ax.axvline(50, color=MUTED, lw=1, ls="--", zorder=1)
    ax.annotate(THRESHOLD_ANNOTATION, (50, len(rows) - 0.4),
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
    ax.set_xlabel(X_LABEL, color=INK)
    ax.set_title("All 30 firms, every score shown — 8 AAER fraud vs 22 matched controls",
                 fontsize=10.5, color=INK)
    ax.plot([], [], "o", color=FRAUD, label=FRAUD_LABEL)
    ax.plot([], [], "o", color=CTRL, label=CONTROL_LABEL)
    ax.legend(frameon=False, fontsize=9, loc="lower right")
    ax.grid(True, axis="x", color=GRID, lw=0.6, zorder=0)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    fig.tight_layout()
    fig.savefig(args.out, facecolor="white")
    plt.close(fig)
    _write_sidecar(sidecar)
    print(f"→ {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
