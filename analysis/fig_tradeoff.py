"""BN-19 headline threshold sweep from the committed decision table."""
import argparse
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
DATA_PATH = REPO / "analysis/decision_table.json"
DEFAULT_OUT = REPO / "analysis/fig_tradeoff.png"

INK, MUTED, GRID = "#1f2937", "#6b7280", "#e5e7eb"
TREATMENT, CONTROL = "#b3261e", "#2f5fa8"
X_LABEL = "Ordinal score threshold (0–100)"
Y_LABEL = "Rate"
TITLE = "Threshold tradeoff: AAER treatment cases and matched controls"
TREATMENT_LABEL = "Detection rate — AAER treatment cases"
CONTROL_LABEL = "False-positive rate — matched controls"
TEXT_STRINGS = (
    X_LABEL, Y_LABEL, TITLE, TREATMENT_LABEL, CONTROL_LABEL,
    "T≥50: {detected}/{n_treatment} detected; control rate {fpr:.3f}",
    "T=70: {detected}/{n_treatment} detected",
)


def _headline_layer(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        table = json.load(handle)
    layers = table.get("layers")
    if not isinstance(layers, dict):
        raise ValueError("decision table must contain a layers object")
    matches = [layer for layer in layers.values()
               if isinstance(layer, dict) and layer.get("n_treatment") == 12]
    if len(matches) != 1:
        raise ValueError(
            "expected exactly one layers-object entry with n_treatment == 12; "
            f"found {len(matches)}"
        )
    return matches[0]


def _rates_and_intervals(cells: list[dict], numerator: str,
                         denominator: str, interval: str):
    rates = [cell[numerator] / cell[denominator] for cell in cells]
    lower = [rate - cell[interval][0] for rate, cell in zip(rates, cells)]
    upper = [cell[interval][1] - rate for rate, cell in zip(rates, cells)]
    return rates, lower, upper


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    try:
        layer = _headline_layer(DATA_PATH)
        cells_by_threshold = {cell["threshold"]: cell for cell in layer["cells"]}
        cells = [cells_by_threshold[threshold] for threshold in (40, 50, 60, 70)]
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(f"fig_tradeoff: {exc}", file=sys.stderr)
        return 1

    thresholds = [cell["threshold"] for cell in cells]
    detected, detected_lo, detected_hi = _rates_and_intervals(
        cells, "detected", "n_treatment", "detected_ci95"
    )
    fpr, fpr_lo, fpr_hi = _rates_and_intervals(
        cells, "false_positives", "n_control", "fpr_ci95"
    )

    fig, ax = plt.subplots(figsize=(7.4, 4.8), dpi=160)
    ax.errorbar(thresholds, detected, yerr=[detected_lo, detected_hi],
                color=TREATMENT, marker="o", lw=1.8, capsize=4,
                label=TREATMENT_LABEL, zorder=3)
    ax.errorbar(thresholds, fpr, yerr=[fpr_lo, fpr_hi],
                color=CONTROL, marker="o", lw=1.8, capsize=4,
                label=CONTROL_LABEL, zorder=3)

    at_50 = cells_by_threshold[50]
    at_70 = cells_by_threshold[70]
    fpr_50 = at_50["false_positives"] / at_50["n_control"]
    ax.annotate(TEXT_STRINGS[5].format(
                    detected=at_50["detected"],
                    n_treatment=at_50["n_treatment"], fpr=fpr_50),
                (50, at_50["detected"] / at_50["n_treatment"]),
                xytext=(7, -38), textcoords="offset points", fontsize=8,
                color=INK, arrowprops={"arrowstyle": "-", "color": MUTED})
    ax.annotate(TEXT_STRINGS[6].format(
                    detected=at_70["detected"],
                    n_treatment=at_70["n_treatment"]),
                (70, at_70["detected"] / at_70["n_treatment"]),
                xytext=(-83, 20), textcoords="offset points", fontsize=8,
                color=INK, arrowprops={"arrowstyle": "-", "color": MUTED})

    ax.set_xticks(thresholds)
    ax.set_xlim(37, 73)
    ax.set_ylim(-0.03, 1.05)
    ax.set_xlabel(X_LABEL, color=INK)
    ax.set_ylabel(Y_LABEL, color=INK)
    ax.set_title(TITLE, fontsize=10.5, color=INK)
    ax.legend(frameon=False, fontsize=8.5, loc="center left")
    ax.grid(True, color=GRID, lw=0.6, zorder=0)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    fig.tight_layout()
    fig.savefig(args.out, facecolor="white", dpi=160)
    plt.close(fig)
    print(f"→ {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
