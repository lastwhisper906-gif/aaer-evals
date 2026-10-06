"""Golden filings run three times: how stable are the analysts' findings? (pass^k)

For each approved golden case, every published run of its filing is compared with
every other:
- `anomaly_overlap`: the Jaccard overlap of the (area, id) pairs two runs listed,
  averaged over the pairs of runs; 1.0 means the same anomalies every time;
- `area_overlap`: the same over the areas alone, which forgives a reworded id;
- `value_spread`: (highest base value a share - lowest) / their mean, over the runs
  that computed one; 0.0 means the same value every time.

Run as a module it exits 0 only when every approved case has at least three runs,
which is queue item eight's eval command.
"""

from __future__ import annotations

import itertools
import sys
from pathlib import Path

from evals.capability import golden
from evals.common import load, run_name

RUNS_WANTED = 3


def _pairs(run: Path) -> tuple[set, set]:
    pairs = set()
    for name in ("analysis_accounting.json", "analysis_financial.json"):
        for a in (load(run / name) or {}).get("anomalies") or []:
            if isinstance(a, dict):
                pairs.add((a.get("area"), a.get("id")))
    return pairs, {area for area, _ in pairs}


def _jaccard(a: set, b: set) -> float:
    return len(a & b) / len(a | b) if a | b else 1.0


def base_value(run: Path):
    scenario = (((load(run / "calculator.json") or {}).get("valuation") or {})
                .get("scenarios") or {}).get("base") or {}
    return scenario.get("value_per_share")


def grade(runs: list[Path] | None = None, cases=None) -> dict:
    rows = []
    cases = golden.approved_cases() if cases is None else cases
    if isinstance(cases, Exception):
        return {"status": "error", "detail": str(cases), "score": None, "rows": []}
    for path, case in cases:
        found = golden.runs_of(case["filing"]["accession"], runs)
        row = {"case": path.name, "runs": [run_name(r) for r in found]}
        if len(found) >= 2:
            sets = [_pairs(r) for r in found]
            pairs = list(itertools.combinations(sets, 2))
            row["anomaly_overlap"] = sum(_jaccard(a[0], b[0]) for a, b in pairs) / len(pairs)
            row["area_overlap"] = sum(_jaccard(a[1], b[1]) for a, b in pairs) / len(pairs)
            values = [v for v in map(base_value, found) if isinstance(v, (int, float))]
            if len(values) >= 2:
                mean = sum(values) / len(values)
                row["value_spread"] = (max(values) - min(values)) / mean if mean else None
        rows.append(row)
    scored = [r["anomaly_overlap"] for r in rows if "anomaly_overlap" in r]
    return {"status": "scored" if scored else ("no approved cases" if not rows
                                               else "fewer than two runs per case"),
            "score": sum(scored) / len(scored) if scored else None, "cases": rows}


def main() -> int:
    result = grade()
    short = [r for r in result["cases"] if len(r["runs"]) < RUNS_WANTED]
    for row in result["cases"]:
        print(f"{row['case']}: {len(row['runs'])} runs; overlap {row.get('anomaly_overlap')}; "
              f"value spread {row.get('value_spread')}")
    if not result["cases"]:
        print("no approved golden case")
        return 1
    if short:
        print(f"{len(short)} case(s) with fewer than {RUNS_WANTED} runs")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
