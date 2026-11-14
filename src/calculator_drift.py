"""Which published calculator figures the calculator of today would print differently.

A run under `runs/` stands as published: the directory is append-only, and a
correction is a new run beside it (CLAUDE.md). When a rule of `src/calculator.py`
changes -- a trailing year or a differenced quarter held to one scope of its
term -- the published figures do not move, but the owner should be able to see
which ones the rule would have moved. This module recomputes every committed
run's `calculator_filings_only.json` (the view both analysts read) and its
`calculator.json` (the final file, with the accounting analyst's adjustments and
the valuation analyst's assumptions the run holds) from the run's own bundle and
the fixture store, as `src/run_analysis.py` computed them, and prints every
numeric leaf whose value changed, old and new, by run, file and path. It writes
nothing under `runs/`.

    .venv/bin/python -m src.calculator_drift [--root runs] [--store tests/fixtures]

It opens no filing and no fixture itself: the record is read by the calculator,
through the cutoff gate, and a run's manifest through the gate's bundle reader.

The price and beta a run read are in its published `calculator.json` under
`market`, exactly as `calculator.market_inputs` returned them, and are handed
back to the calculator as that run's market data, so the priced sections
recompute from the run's own inputs. A leaf is a number under `value` (or any other numeric
field) at a path present in the published file; a cell that had a number and is
now missing, or was missing and now has a number, is a change too. A path the
published file never held -- a section added since the run -- is not a change
and is not listed.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from src import calculator, cutoff_guard

FINAL = "calculator.json"


def committed_runs(root: Path) -> list[Path]:
    """Every run directory under `root` that holds the published filings-only view."""
    return sorted(path.parent for path in root.glob(f"*/*/{calculator.FILINGS_ONLY}"))


def trigger(run: Path) -> dict:
    """The triggering filing of a run, from its own manifest: a rerun's directory
    name is not its accession, so the manifest's `accession` names it."""
    manifest = json.loads(cutoff_guard.load_bundle_file(run, "input_manifest.json"))
    accession = manifest["accession"]
    form, report_date = next((document["form"], document["report_date"])
                             for document in manifest["documents"]
                             if document.get("accession") == accession)
    return {"ticker": run.parent.name, "cutoff": manifest["cutoff"], "period_end": report_date,
            "form": form, "accession": accession}


def _written(run: Path, name: str) -> dict | None:
    """A file the run itself wrote -- a calculator stage, an analyst's checked
    output -- or None where it wrote none."""
    path = run / name
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else None


def recompute(run: Path, store: Path) -> dict:
    """The filings-only view of one run, from its bundle and the store, as today's
    calculator prints it."""
    named = trigger(run)
    return calculator.filings_only(calculator.calculate(**named, fixtures_root=store, bundle=run))


def recompute_final(run: Path, store: Path) -> dict:
    """The run's `calculator.json` as today's calculator prints it: the accounting
    analyst's adjustments, the valuation analyst's assumptions and the market
    data (price and beta) are the run's own, read from its published files."""
    named = trigger(run)
    published = _written(run, FINAL) or {}
    return calculator.calculate(**named, fixtures_root=store, bundle=run,
                                market_data=published.get("market"),
                                accounting=_written(run, "analysis_accounting.json"),
                                assumptions=_written(run, "assumptions.json"))


def numeric_leaves(node, prefix: str = "") -> dict[str, float]:
    """Every number in a payload, by its dotted path (a list index is a number)."""
    out: dict[str, float] = {}
    if isinstance(node, bool):
        return out
    if isinstance(node, (int, float)):
        out[prefix] = node
    elif isinstance(node, dict):
        for key, value in node.items():
            out.update(numeric_leaves(value, f"{prefix}.{key}" if prefix else str(key)))
    elif isinstance(node, list):
        for position, value in enumerate(node):
            out.update(numeric_leaves(value, f"{prefix}.{position}" if prefix else str(position)))
    return out


def _parent(payload, path: str):
    """The dict or list that holds the leaf at `path` in `payload`, or None."""
    node = payload
    for key in path.split(".")[:-1]:
        if isinstance(node, list):
            if not key.isdigit() or int(key) >= len(node):
                return None
            node = node[int(key)]
        elif isinstance(node, dict) and key in node:
            node = node[key]
        else:
            return None
    return node


def changed_leaves(old: dict, new: dict) -> list[dict]:
    """Each numeric leaf of `old` that `new` prints differently or no longer prints,
    and each number `new` prints in a cell `old` held without one."""
    before, after = numeric_leaves(old), numeric_leaves(new)
    out = []
    for path, value in before.items():
        if path not in after:
            out.append({"path": path, "old": value, "new": None})
        elif after[path] != value:
            out.append({"path": path, "old": value, "new": after[path]})
    for path, value in after.items():
        if path in before:
            continue
        holder = _parent(old, path)
        # a cell that was missing and now has a number; a key the published file
        # never held, in a cell that had its number, is a field added since
        if isinstance(holder, dict) and "missing" in holder:
            out.append({"path": path, "old": None, "new": value})
    return sorted(out, key=lambda row: row["path"])


def drift(run: Path, store: Path) -> list[dict]:
    """The changed leaves of one run, in its filings-only view and in its
    calculator.json, each with the run's name and the file."""
    name = f"{run.parent.name}/{run.name}"
    rows = []
    for file, fresh in ((calculator.FILINGS_ONLY, recompute), (FINAL, recompute_final)):
        published = _written(run, file)
        if published is None:
            continue
        rows.extend({"run": name, "file": file, **row}
                    for row in changed_leaves(published, fresh(run, store)))
    return rows


def report(root: Path, store: Path, *, scope_rule: bool = True,
           last_fiscal_year_rung: bool = True) -> list[dict]:
    """Every run's changed leaves. With `scope_rule=False` the calculator's scope
    rule for a trailing year and a quarter is off, and with
    `last_fiscal_year_rung=False` the cost of debt's last-fiscal-year rung is: the
    controls, which say what today's calculator would print differently without
    each, so that a list's difference from its control is that rule's alone."""
    was = calculator.SCOPE_RULE, calculator.LAST_FISCAL_YEAR_RUNG
    calculator.SCOPE_RULE, calculator.LAST_FISCAL_YEAR_RUNG = scope_rule, last_fiscal_year_rung
    try:
        rows = []
        for run in committed_runs(root):
            rows.extend(drift(run, store))
    finally:
        calculator.SCOPE_RULE, calculator.LAST_FISCAL_YEAR_RUNG = was
    return rows


def _number(value) -> str:
    if value is None:
        return "missing"
    if isinstance(value, float) and value.is_integer():
        return f"{int(value):,}"
    return f"{value:,.6g}" if isinstance(value, float) else f"{value:,}"


def printed(rows: list[dict]) -> str:
    """The list as the command prints it: a count per run, then one line per leaf."""
    lines = []
    runs = sorted({row["run"] for row in rows})
    for run in runs:
        own = [row for row in rows if row["run"] == run]
        lines.append(f"{run}: {len(own)} changed")
        for row in own:
            lines.append(f"  {row.get('file', calculator.FILINGS_ONLY)} {row['path']}: "
                         f"{_number(row['old'])} -> {_number(row['new'])}")
    if not rows:
        lines.append("no published figure changes")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default="runs", help="a directory of <ticker>/<accession> runs")
    parser.add_argument("--store", default=str(cutoff_guard.FIXTURES))
    parser.add_argument("--json", action="store_true", help="print the rows as JSON lines")
    parser.add_argument("--control", action="store_true",
                        help="recompute with the scope rule and the last-fiscal-year rung off: "
                             "what moves for any other reason")
    args = parser.parse_args(argv)
    root, store = Path(args.root), Path(args.store)
    rows = report(root, store, scope_rule=not args.control,
                  last_fiscal_year_rung=not args.control)
    if args.json:
        for row in rows:
            print(json.dumps(row))
    else:
        print(printed(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())
