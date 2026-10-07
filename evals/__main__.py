"""`make eval` and `make eval-quick`.

    python -m evals                      every run; regression and capability;
                                         appends one line to evals/scoreboard.jsonl
    python -m evals --runs runs/NVDA     the runs under the given paths only
    python -m evals --quick              regression only, on the runs this branch
                                         changed against origin/main; no scoreboard

Exit status: 1 on any regression failure, or a capability score below a floor set in
evals/thresholds.json; 0 otherwise.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

from evals.capability import (consistency, golden, grader_agreement, memorization, outcomes,
                              rubric_score)
from evals.common import EVALS, FAIL, PASS, REPO, Result, find_runs, load, run_name
from evals.golden_format import GoldenFormatError
from evals.regression import coverage, mechanical

SCOREBOARD = REPO / "evals" / "scoreboard.jsonl"
THRESHOLDS = EVALS / "thresholds.json"      # the running graders' own floors


def changed_runs(base: str = "origin/main") -> list[Path]:
    try:
        out = subprocess.run(["git", "diff", "--name-only", f"{base}...HEAD", "--", "runs/"],
                             cwd=REPO, capture_output=True, text=True, check=True).stdout
        dirty = subprocess.run(["git", "status", "--porcelain", "--", "runs/"], cwd=REPO,
                               capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return []
    names = out.splitlines() + [line[3:] for line in dirty.splitlines()]
    dirs = {Path(*Path(name).parts[:3]) for name in names if len(Path(name).parts) >= 3}
    return find_runs([REPO / d for d in sorted(dirs) if (REPO / d).is_dir()]) if dirs else []


def regression(runs: list[Path]) -> list[Result]:
    # the run checks first; the hand-worked case, which runs the branch's
    # calculator in a process of its own, last
    results = []
    for run in runs:
        results += mechanical.grade(run) + coverage.grade(run)
    return results


def capability(runs: list[Path], cases: list | None = None) -> dict:
    per_run = {run_name(run): coverage.rates(run) for run in runs}
    means = {}
    for key in next(iter(per_run.values()), {}):
        means[f"coverage.{key}"] = sum(r[key] for r in per_run.values()) / len(per_run)
    grades = [rubric_score.check(g, anomaly_ids(run))
              for run in runs for g in [load(run / "grade.json")] if isinstance(g, dict)]
    graded = [g["score"] for g in grades if g["score"] is not None]
    disagreeing = sum(not g["agrees"] for g in grades)
    unreadable = sum(bool(g["unreadable"]) for g in grades)
    filings = [v for v in (mechanical.valuation_quotes_from_filings(run) for run in runs)
               if v is not None]
    means["valuation_quotes_from_filings"] = sum(filings) / len(filings) if filings else None
    return {
        "coverage": {"per_run": per_run, "means": means},
        "golden": golden.grade(runs, cases=cases),
        "grader_agreement": grader_agreement.grade(runs, cases=cases),
        "analysis_grader": {"status": f"{len(graded)} of {len(runs)} runs graded; "
                                      f"{disagreeing} where the grader's own score differs "
                                      f"from the rubric's formula; {unreadable} grade.json the "
                                      "formula cannot read",
                            "score": sum(graded) / len(graded) if graded else None,
                            "gated": False},
        "consistency": consistency.grade(runs, cases=cases),
        "outcomes": outcomes.grade(runs),
        "memorization": memorization.grade(runs),
    }


def anomaly_ids(run: Path) -> set[str]:
    """Every anomaly id the two frames' analyses list: what a grade must cover."""
    out = set()
    for name in ("analysis_accounting.json", "analysis_financial.json"):
        for a in (load(run / name) or {}).get("anomalies") or []:
            if isinstance(a, dict) and isinstance(a.get("id"), str):
                out.add(a["id"])
    return out


def floors_failed(scores: dict, thresholds: dict | None = None) -> list[str]:
    """`thresholds` is what main() read before any branch code ran; read here only
    when called on its own."""
    thresholds = load(THRESHOLDS) or {} if thresholds is None else thresholds
    failed = []
    for name, floor in (thresholds.get("capability") or {}).items():
        value = scores.get(name)
        if value is None or value < floor:
            failed.append(f"{name}: {value} below the floor {floor}")
    return failed


def flat_scores(cap: dict) -> dict:
    out = dict(cap["coverage"]["means"])
    for name in ("golden", "grader_agreement", "analysis_grader", "consistency"):
        out[name] = cap[name].get("score")
    return out


def commit() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=REPO,
                              capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="grade run directories")
    parser.add_argument("--runs", nargs="*", help="paths holding runs (default: runs/)")
    parser.add_argument("--quick", action="store_true", help="regression on changed runs only")
    parser.add_argument("--no-scoreboard", action="store_true")
    parser.add_argument("--json", action="store_true", help="print the full result as JSON")
    args = parser.parse_args(argv)

    # The owner's floors and approved cases are read into memory before anything
    # of the tree under judgment runs (the hand-worked case runs its calculator),
    # so nothing that code does to the files on disk reaches this grading.
    thresholds = load(THRESHOLDS) or {}
    try:
        cases = golden.approved_cases()
    except GoldenFormatError as exc:
        cases = exc
    if args.quick:
        runs = changed_runs()
    else:
        runs = find_runs([Path(p) for p in args.runs] if args.runs else None)
    results = regression(runs)
    if args.quick:
        results += mechanical.check_hand_worked_cases()
    else:
        # every run file is read into the capability scores before the branch's
        # calculator runs: nothing that code does on disk reaches this grading
        cap = capability(runs, cases)
        results += mechanical.check_hand_worked_cases()
    failed = [r for r in results if r.status == FAIL]
    passed = sum(r.status == PASS for r in results)
    print(f"regression: {passed} pass, {len(failed)} fail, "
          f"{len(results) - passed - len(failed)} not applicable, over {len(runs)} run(s)")
    for r in failed:
        print(f"  FAIL {r.grader} {r.run}: {r.detail}")
        for f in r.failures[:5]:
            print(f"       {f}")
    if args.quick:
        return 1 if failed else 0

    scores = flat_scores(cap)
    print("capability (reported; gated only where evals/thresholds.json sets a floor):")
    for name, value in scores.items():
        print(f"  {name}: {'n/a' if value is None else round(value, 3)}")
    for name in ("golden", "grader_agreement", "analysis_grader", "consistency", "outcomes",
                 "memorization"):
        print(f"  {name}: {cap[name]['status']}")
    below = floors_failed(scores, thresholds)
    for line in below:
        print(f"  BELOW FLOOR {line}")
    if args.json:
        print(json.dumps({"regression": [r.as_dict() for r in results], "capability": cap},
                         indent=1, default=str))
    if not args.no_scoreboard:
        with SCOREBOARD.open("a", encoding="utf-8") as out:
            out.write(json.dumps({
                "date": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "commit": commit(), "runs": [run_name(r) for r in runs],
                "regression": {"pass": passed, "fail": len(failed),
                               "failures": [f"{r.grader} {r.run}" for r in failed]},
                "capability": scores, "below_floor": below}, sort_keys=True) + "\n")
    return 1 if failed or below else 0


if __name__ == "__main__":
    sys.exit(main())
