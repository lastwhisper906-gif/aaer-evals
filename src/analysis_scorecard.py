"""The analyses beside the control and the baselines, one row per run, never merged.

The owner's decision of 2026-09-28 keeps the single-agent control and the six
formula baselines and asks for a scorecard that records all of them beside the
three analysts. This is that table. It counts; it does not judge. There is no
column that adds the accounting, financial and valuation analyses together, no
column that ranks one company above another, and no column that turns a count
into a verdict — `docs/CHECKLIST.md` §9, "No count is a verdict".

What it can say today is what each layer produced and what the gates dropped,
beside what the control produced from the whole bundle alone and what each
formula said. What it cannot say yet is which was right: the outcomes at 60,
120 and 250 trading days arrive from `events/` and prices, and the rows that
score against them are added the day the first horizon expires.

    python3.12 -m src.analysis_scorecard --root <directory of runs> --out scorecard.md
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from src import interpreter_pin
except ImportError:  # invoked as a plain script
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import interpreter_pin

BASELINES = ("beneish_m_score", "accruals_over_assets", "net_operating_assets",
             "piotroski_f_score", "altman_z_score", "ohlson_o_score")


def _load(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def row(run: Path) -> dict:
    """One run's counts, each read off the file that states it."""
    accounting = _load(run / "analysis_accounting.json") or {}
    financial = _load(run / "analysis_financial.json") or {}
    valuation = _load(run / "analysis_valuation.json")
    calculator = _load(run / "calculator.json") or {}
    # The control's gated files at the run root, as the analysts' are: the files it
    # wrote in its own directory still hold what the gate dropped.
    control_accounting = _load(run / "control_analysis_accounting.json") or {}
    control_financial = _load(run / "control_analysis_financial.json") or {}
    baselines = _load(run / "baselines.json") or {}
    reconciliation = accounting.get("reconciliation") or []
    band = (calculator.get("valuation") or {}).get("value_range_per_share") or {}
    return {
        "run": f"{run.parent.name}/{run.name}",
        "accounting_anomalies": len(accounting.get("anomalies") or []),
        "accounting_contradictions": sum(1 for item in reconciliation
                                         if item.get("outcome") == "contradicts"),
        "accounting_dropped": accounting.get("dropped_count"),
        "adjustments": len(accounting.get("adjustments") or []),
        "financial_anomalies": len(financial.get("anomalies") or []),
        "financial_dropped": financial.get("dropped_count"),
        "valuation": ("not computed" if not band else
                      f"{band.get('low'):,.2f} to {band.get('high'):,.2f} a share"),
        "valuation_reading": "written" if valuation else "none",
        "control_accounting_anomalies": len(control_accounting.get("anomalies") or []),
        "control_accounting_dropped": control_accounting.get("dropped_count"),
        "control_financial_anomalies": len(control_financial.get("anomalies") or []),
        "control_financial_dropped": control_financial.get("dropped_count"),
        **{name: ((baselines.get(name) or {}).get("value")) for name in BASELINES},
    }


def render(rows: list[dict]) -> str:
    columns = list(rows[0]) if rows else []
    lines = ["# The three analyses, the control and the baselines, side by side", "",
             "Counts only. No column adds the analyses together, ranks the companies or "
             "turns a count into a verdict; outcomes are scored when their horizons "
             "expire.", "",
             "| " + " | ".join(columns) + " |", "|" + "---|" * len(columns)]
    for one in rows:
        lines.append("| " + " | ".join("" if one[c] is None else
                                       (f"{one[c]:.3f}" if isinstance(one[c], float) else
                                        str(one[c])) for c in columns) + " |")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="analyses beside the control and baselines")
    parser.add_argument("--root", required=True, help="a directory of <ticker>/<accession> runs")
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)
    code = interpreter_pin.enforce()
    if code:
        return code
    root = Path(args.root)
    runs = sorted(path.parent for path in root.glob("*/*/calculator.json"))
    Path(args.out).write_text(render([row(run) for run in runs]), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
