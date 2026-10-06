"""How often the analysis-grader agrees with the owner, on the golden filings.

The owner's golden case says which findings must be made (must_find) and which must
not be claimed (must_not_claim). The analysis-grader writes `grade.json` into a run
with a verdict for each anomaly: supported, unsupported or unclear. For every golden
item that matches an anomaly in a graded run:
- a must_find match agrees when the grader called that anomaly supported;
- a must_not_claim match agrees when the grader called it unsupported.

Agreement = agreeing items / matched items. The grader's own scores are reported,
never gated, until this passes the floor the owner sets in thresholds.json under
`grader_agreement`.
"""

from __future__ import annotations

from pathlib import Path

from evals.capability import golden
from evals.common import load, run_name


def verdicts(run: Path) -> dict[str, str]:
    grade = load(run / "grade.json") or {}
    return {item.get("id"): item.get("verdict") for item in grade.get("items") or []
            if isinstance(item, dict)}


def grade(runs: list[Path] | None = None) -> dict:
    cases = golden.approved_cases()
    agree = total = 0
    rows = []
    for path, case in cases:
        for run in golden.runs_of(case["filing"]["accession"], runs):
            graded = verdicts(run)
            if not graded:
                continue
            candidates = golden.anomalies(run, case["frame"])
            for kind, wanted in (("must_find", "supported"), ("must_not_claim", "unsupported")):
                for item in case.get(kind) or []:
                    for anomaly in candidates:
                        if golden.matches(anomaly, item) and anomaly.get("id") in graded:
                            total += 1
                            agree += graded[anomaly["id"]] == wanted
                            rows.append({"run": run_name(run), "case": path.name, "kind": kind,
                                         "anomaly": anomaly["id"],
                                         "grader": graded[anomaly["id"]], "owner": wanted})
    if not cases:
        return {"status": "no approved cases", "score": None, "items": []}
    return {"status": "scored" if total else "no graded run of an approved case",
            "score": agree / total if total else None, "items": rows}
