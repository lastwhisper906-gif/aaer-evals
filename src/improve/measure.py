"""Does a remedy work? Reruns, on copies outside the tree, and one fixed rule
(`docs/improve_loop.md`, steps 3 and 4). Four commands:

    draw     the held-out runs: drawn by Python from the published runs that
             are not held-in, the seed recorded; never chosen by the proposer
    plan     what a `run` would cost, from the manifests' per-agent cost; a
             plan over the budget named is refused, and nothing is run
    run      copy each run, call the named agents again `--repeats` times,
             gate what they wrote, grade if asked, and print one metrics row
             per run, agent and repeat (the row `mine` would print)
    compare  baseline rows against candidate rows under the acceptance rule;
             the verdict is the judge, and it is written here and nowhere else

The acceptance rule. For one run, one agent and one metric, the baseline's
repeats give a mean and a spread (highest less lowest); the candidate's give a
mean. The candidate *moves* the metric when its mean is better than the
baseline's by more than the spread, and *regresses* it when its mean is worse
by more than the spread. An edit is accepted when it moves its target metric
on every held-in run it names and regresses no watched metric on any run,
held-in or held-out. Better and worse are `mine.WATCHED`'s directions. A
spread of zero with one repeat each side reads any difference as a move, so a
one-repeat measurement is reported as such in the verdict.

The model is an alias, `fable` by the owner's decision of 2026-10-21 (Opus from
2026-10-14 to then); a
version string is refused, so a run never pins what the next model replaces.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import random
import re
import shutil
import sys
from pathlib import Path

try:
    from src import interpreter_pin
    from src.improve import mine
except ImportError:  # invoked as a plain script
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
    from src import interpreter_pin
    from src.improve import mine

BAD_INPUT = 2
OVER_BUDGET = 3
DEFAULT_MODEL = "fable"
GATE_KIND = {"accounting-analyst": "accounting", "financial-analyst": "financial",
             "valuation-analyst": "assumptions", "valuation-analyst-second-pass": "valuation"}


class MeasureError(Exception):
    """A plan or a comparison that cannot be made as asked. Never repaired."""


def alias_only(model: str) -> str:
    if re.search(r"\d", model or ""):
        raise MeasureError(f"the model is an alias such as {DEFAULT_MODEL!r}, never a version: {model!r}")
    return model


# --- draw -------------------------------------------------------------------------------

def draw(root: Path, held_in: list[str], count: int, seed: int | None = None) -> dict:
    """`count` held-out runs from the runs under `root` that are not held-in, by
    a seeded shuffle; the seed is in the answer so the draw is reproducible and
    on record, and the proposer never names them."""
    held = {str(Path(p).resolve()) for p in held_in}
    pool = sorted(str(run.resolve()) for run in mine.runs_under(root)
                  if str(run.resolve()) not in held)
    seed = random.SystemRandom().randrange(1 << 30) if seed is None else seed
    chosen = random.Random(seed).sample(pool, min(count, len(pool)))
    return {"seed": seed, "pool": len(pool), "held_out": sorted(chosen)}


# --- plan -------------------------------------------------------------------------------

def _manifest(run: Path) -> dict:
    try:
        return json.loads((Path(run) / "input_manifest.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise MeasureError(f"{run}: no manifest to plan from: {exc}") from exc


def plan(runs: list[Path], agents: list[str], repeats: int, *, grade: bool = False) -> dict:
    """What `run` would cost: each agent's recorded cost on each run, times the
    repeats, plus the grader's recorded cost on each run when grading is
    asked. A run whose manifest has no cost for an agent is named, not guessed."""
    lines, total, unknown = [], 0.0, []
    for run in runs:
        manifest = _manifest(run)
        recorded = manifest.get("agents") or {}
        for agent in agents:
            cost = (recorded.get(agent) or {}).get("cost_usd")
            if not isinstance(cost, (int, float)):
                unknown.append(f"{run}:{agent}")
                continue
            lines.append({"run": str(run), "agent": agent, "each": cost, "times": repeats})
            total += cost * repeats
        if grade:
            try:
                grader = json.loads((Path(run) / "grade.json").read_text(encoding="utf-8")).get("grader") or {}
            except (OSError, ValueError, AttributeError):
                grader = {}
            cost = grader.get("cost_usd")
            if isinstance(cost, (int, float)):
                lines.append({"run": str(run), "agent": "analysis-grader", "each": cost, "times": repeats})
                total += cost * repeats
            else:
                unknown.append(f"{run}:analysis-grader")
    return {"estimate_usd": round(total, 2), "lines": lines, "unknown": unknown}


# --- run --------------------------------------------------------------------------------

def rerun(run: Path, agent: str, *, model: str, grade: bool) -> Path:
    """One agent called again on `run` (a copy), its file gated into the run
    root as the pipeline gates it, and the run graded if asked. Returns the
    run. Imports the pipeline here so the rule above is importable without it."""
    from src import run_analysis
    logs = run.parent / f".{run.name}.logs"
    logs.mkdir(exist_ok=True)
    record = run_analysis.run_agent(run, agent, logs, model, check=False)
    if record.get("result") != "written":
        raise MeasureError(f"{run} {agent}: the call did not write ({record.get('reason')})")
    checked = run_analysis.check_analysis(run, agent, GATE_KIND[agent])
    run_analysis.write_json(run / mine.ANALYSES[agent], checked)
    if grade:
        from src import grade_run
        (run / "grade.json").unlink(missing_ok=True)      # the copy's, never a published one
        grade_run.grade(run)
    return run


def _copy(run: Path, work: Path, repeat: int) -> Path:
    target = work / Path(run).parent.name / f"{Path(run).name}-r{repeat}"
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(run, target)
    return target


def measure(runs: list[Path], agents: list[str], repeats: int, *, work: Path, model: str,
            grade: bool = False, workers: int = 4, rerun=rerun) -> list[dict]:
    """Every (run, agent, repeat) on a copy, in parallel; the rows `mine` reads
    off each copy, each tagged with its source run and its repeat."""
    alias_only(model)
    jobs = [(run, agent, repeat) for run in runs for repeat in range(1, repeats + 1)
            for agent in agents]
    copies = {(str(run), repeat): _copy(Path(run), work, repeat)
              for run in runs for repeat in range(1, repeats + 1)}
    rows: list[dict] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, min(workers, len(jobs)))) as pool:
        futures = {pool.submit(rerun, copies[(str(run), repeat)], agent, model=model,
                               grade=grade and agent == agents[-1]): (run, agent, repeat)
                   for run, agent, repeat in jobs}
        for future in concurrent.futures.as_completed(futures):
            run, agent, repeat = futures[future]
            future.result()
    for (run, repeat), copy in copies.items():
        for row in mine.rows_of(copy):
            if row["agent"] in agents:
                rows.append(dict(row, source=run, repeat=repeat))
    return rows


# --- compare ----------------------------------------------------------------------------

def _mean(values: list) -> float | None:
    values = [v for v in values if isinstance(v, (int, float))]
    return sum(values) / len(values) if values else None


def _spread(values: list) -> float | None:
    values = [v for v in values if isinstance(v, (int, float))]
    return max(values) - min(values) if values else None


def _signed(metric: str, baseline: float, candidate: float) -> float:
    """Positive when the candidate is better, by the metric's direction."""
    delta = candidate - baseline
    return delta if mine.WATCHED[metric] == "up" else -delta


def compare(baseline: list[dict], candidate: list[dict], *, held_in: list[str],
            target: str) -> dict:
    """The verdict and the table behind it. Rows are `measure`'s, each with
    `source`, `agent` and `repeat`. The rule is the module docstring's."""
    if target not in mine.WATCHED:
        raise MeasureError(f"the target is one of {', '.join(mine.WATCHED)}: {target!r}")
    held = {str(Path(p).resolve()) for p in held_in}
    keys = sorted({(row["source"], row["agent"]) for row in baseline}
                  | {(row["source"], row["agent"]) for row in candidate})
    cells, moved, regressed = [], [], []
    for source, agent in keys:
        base = [r for r in baseline if r["source"] == source and r["agent"] == agent]
        cand = [r for r in candidate if r["source"] == source and r["agent"] == agent]
        where = "held_in" if str(Path(source).resolve()) in held else "held_out"
        for metric in mine.WATCHED:
            b, c = [r.get(metric) for r in base], [r.get(metric) for r in cand]
            b_mean, c_mean, spread = _mean(b), _mean(c), _spread(b)
            cell = {"source": source, "agent": agent, "where": where, "metric": metric,
                    "baseline": b, "candidate": c, "baseline_mean": b_mean,
                    "candidate_mean": c_mean, "spread": spread, "reading": "unmeasured"}
            if b_mean is not None and c_mean is not None:
                signed = _signed(metric, b_mean, c_mean)
                if signed > spread:
                    cell["reading"] = "moved"
                elif -signed > spread:
                    cell["reading"] = "regressed"
                else:
                    cell["reading"] = "within spread"
                if metric == target and where == "held_in":
                    moved.append(cell["reading"] == "moved")
                if cell["reading"] == "regressed":
                    regressed.append(f"{source} {agent} {metric}")
            cells.append(cell)
    one_repeat = all(len(r) <= 1 for r in ([x["baseline"] for x in cells] + [x["candidate"] for x in cells]))
    accepted = bool(moved) and all(moved) and not regressed
    return {"accepted": accepted, "target": target,
            "target_moved_on_every_held_in_run": bool(moved) and all(moved),
            "held_in_runs_measured": sum(moved), "regressions": regressed,
            "one_repeat": one_repeat, "cells": cells}


# --- command ----------------------------------------------------------------------------

def _rows(path: Path) -> list[dict]:
    try:
        return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]
    except (OSError, ValueError) as exc:
        raise MeasureError(f"{path}: not metrics rows: {exc}") from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="does a remedy work: draw, plan, run, compare")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("draw")
    p.add_argument("--runs-root", required=True)
    p.add_argument("--held-in", nargs="+", required=True)
    p.add_argument("--count", type=int, required=True)
    p.add_argument("--seed", type=int, default=None)
    p = sub.add_parser("plan")
    p.add_argument("--runs", nargs="+", required=True)
    p.add_argument("--agents", nargs="+", required=True)
    p.add_argument("--repeats", type=int, default=2)
    p.add_argument("--grade", action="store_true")
    p.add_argument("--budget-usd", type=float, required=True)
    p = sub.add_parser("run")
    p.add_argument("--runs", nargs="+", required=True)
    p.add_argument("--agents", nargs="+", required=True)
    p.add_argument("--repeats", type=int, default=2)
    p.add_argument("--grade", action="store_true")
    p.add_argument("--budget-usd", type=float, required=True)
    p.add_argument("--work", required=True, help="a directory outside the tree for the copies")
    p.add_argument("--model", default=DEFAULT_MODEL)
    p.add_argument("--workers", type=int, default=4)
    p = sub.add_parser("compare")
    p.add_argument("--baseline", required=True)
    p.add_argument("--candidate", required=True)
    p.add_argument("--held-in", nargs="+", required=True)
    p.add_argument("--target", required=True)
    args = parser.parse_args(argv)
    code = interpreter_pin.enforce()
    if code:
        return code
    try:
        if args.command == "draw":
            print(json.dumps(draw(Path(args.runs_root), args.held_in, args.count, args.seed)))
        elif args.command in ("plan", "run"):
            runs = [Path(r) for r in args.runs]
            for agent in args.agents:
                if agent not in GATE_KIND:
                    raise MeasureError(f"the gate reads {', '.join(GATE_KIND)}: {agent!r}")
            estimate = plan(runs, args.agents, args.repeats, grade=args.grade)
            print(json.dumps(estimate), file=sys.stderr)
            if estimate["estimate_usd"] > args.budget_usd:
                print(f"measure: the plan's {estimate['estimate_usd']} USD exceeds the budget "
                      f"{args.budget_usd}; nothing run", file=sys.stderr)
                return OVER_BUDGET
            if args.command == "run":
                work = Path(args.work).resolve()
                if work.is_relative_to(Path.cwd()) and (Path.cwd() / "CLAUDE.md").is_file():
                    raise MeasureError(f"--work {work} is inside the tree; the copies go outside it")
                for row in measure(runs, args.agents, args.repeats, work=work, model=args.model,
                                   grade=args.grade, workers=args.workers):
                    print(json.dumps(row, ensure_ascii=False))
        elif args.command == "compare":
            verdict = compare(_rows(Path(args.baseline)), _rows(Path(args.candidate)),
                              held_in=args.held_in, target=args.target)
            print(json.dumps(verdict, ensure_ascii=False, indent=1))
            return 0 if verdict["accepted"] else 1
    except MeasureError as exc:
        print(f"measure: {exc}", file=sys.stderr)
        return BAD_INPUT
    return 0


if __name__ == "__main__":
    sys.exit(main())
