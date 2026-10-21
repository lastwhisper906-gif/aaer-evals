"""What every published run shows, one row per run per analysis: a table, no
thresholds (`docs/improve_loop.md`, step 1).

Each row is read off files the run already holds -- `input_manifest.json`,
the four analyses, `grade.json` -- and names what happened: how many items
the gate dropped and for which reasons, in the gate's own words with the
item's particulars cut off; how many of the analysis's blocks (areas,
sections, readings) stand empty; how long its lists are; the grader's score
and dealbreakers; how many times the write-time hook spoke; the tokens, cost
and model. Nothing here says whether any of that is a problem: the model
reads the table and says what it means, and `measure` says whether a remedy
worked.

    .venv/bin/python -m src.improve.mine --runs runs            # JSON lines
    .venv/bin/python -m src.improve.mine --runs runs --table    # markdown
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

try:
    from src import interpreter_pin
except ImportError:  # invoked as a plain script
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
    from src import interpreter_pin

# the analysis each agent writes into the run, as the run publishes it
ANALYSES = {"accounting-analyst": "analysis_accounting.json",
            "financial-analyst": "analysis_financial.json",
            "valuation-analyst": "assumptions.json",
            "valuation-analyst-second-pass": "analysis_valuation.json"}
# the keys of each analysis whose value is a block of named entries (an entry
# the gate dropped is `{"dropped": reason}`), and whose value is a list
BLOCKS = ("areas", "sections", "readings")
SINGLE = ("dupont", "path_to_distress", "value_range", "price_position",
          "market_implied_growth", "accounting_adjustments")
LISTS = ("anomalies", "adjustments", "reconciliation", "most_sensitive")
# the metrics `measure` watches, by row key, and the direction that is better
WATCHED = {"dropped_count": "down", "empty_blocks": "down", "anomalies": "up",
           "grade_score": "up", "grade_dealbreakers": "down"}

_PROSE_KEY = re.compile(r"^(?:[a-z_]+: )+")      # "revenue_growth_year_one: reason: ..." too


def reason_class(reason) -> str:
    """The gate's reason with the item's particulars cut off, so two drops for
    the same rule fall in one class whatever item they fell from: the prose key
    it opens with goes, a quoted id or a `{path}` it opens with goes, and the
    text is cut at the first quote or brace that follows a space (an apostrophe
    inside a word, as in "analyst's", is not a quote)."""
    text = _PROSE_KEY.sub("", str(reason or "")).strip()
    text = re.sub(r"^(?:'[^']*'|\"[^\"]*\"|\{[^}]*\})\s*", "", text)
    text = re.split(r"\s['\"{]", text, maxsplit=1)[0].strip().rstrip(":")
    return text[:90] or "(no reason)"


def _load(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def analysis_facts(analysis: dict) -> dict:
    """The counts one analysis file shows."""
    dropped = analysis.get("dropped_items") or []
    facts = {"dropped_count": len(dropped),
             "drops_by_reason": dict(Counter(reason_class(row.get("reason"))
                                             for row in dropped if isinstance(row, dict)))}
    blocks = empty = 0
    for key in BLOCKS:
        block = analysis.get(key)
        if isinstance(block, dict):
            for entry in block.values():
                blocks += 1
                empty += isinstance(entry, dict) and "dropped" in entry
    for key in SINGLE:
        entry = analysis.get(key)
        if entry is not None:
            blocks += 1
            empty += isinstance(entry, dict) and "dropped" in entry
    facts["blocks"], facts["empty_blocks"] = blocks, empty
    for key in LISTS:
        if key in analysis:
            facts[key] = len(analysis[key]) if isinstance(analysis[key], list) else None
    outcomes = Counter(row.get("outcome") for row in analysis.get("reconciliation") or []
                       if isinstance(row, dict))
    if outcomes:
        facts["reconciliation_outcomes"] = dict(outcomes)
    return facts


def agent_facts(entry: dict | None) -> dict:
    """What the manifest records of one agent's call."""
    if not isinstance(entry, dict):
        return {"recorded": False}
    return {"recorded": True, "result": entry.get("result"),
            "model_served": entry.get("model_served"),
            "attempts": len(entry.get("attempts") or []) or entry.get("attempt"),
            "output_tokens": entry.get("output_tokens"), "cost_usd": entry.get("cost_usd"),
            "seconds": entry.get("seconds"),
            "gate_feedback_rounds": len(entry.get("gate_feedback") or [])}


def grade_facts(grade: dict | None) -> dict:
    if not isinstance(grade, dict):
        return {"grade_score": None, "grade_dealbreakers": None}
    dealbreakers = grade.get("dealbreakers") or []
    return {"grade_score": grade.get("score"), "grade_dealbreakers": len(dealbreakers),
            "grade_dealbreaker_kinds": dict(Counter(row.get("kind") for row in dealbreakers
                                                    if isinstance(row, dict)))}


def rows_of(run: Path) -> list[dict]:
    """One row per analysis the run holds; none for a directory with no manifest."""
    run = Path(run)
    manifest = _load(run / "input_manifest.json")
    if not isinstance(manifest, dict):
        return []
    grade = grade_facts(_load(run / "grade.json"))
    stages = manifest.get("analysis_stages") or {}
    quote_gate = (stages.get("quote_gate") or {}).get("dropped") if isinstance(stages, dict) else None
    rows = []
    for agent, name in ANALYSES.items():
        analysis = _load(run / name)
        if not isinstance(analysis, dict):
            continue
        row = {"run": str(run), "ticker": manifest.get("ticker"), "form": manifest.get("form"),
               "filing_date": manifest.get("filing_date"), "agent": agent, "file": name,
               "quote_gate_dropped": quote_gate}
        row.update(analysis_facts(analysis))
        row.update(agent_facts((manifest.get("agents") or {}).get(agent)))
        row.update(grade)
        rows.append(row)
    return rows


def runs_under(root: Path) -> list[Path]:
    """Every run directory under `root`: a directory holding a manifest, or
    `root` itself when it is one."""
    root = Path(root)
    if (root / "input_manifest.json").is_file():
        return [root]
    return sorted(p.parent for p in root.glob("*/*/input_manifest.json"))


def table(rows: list[dict]) -> str:
    """The rows as one markdown table, the drop classes as a count each."""
    head = ["run", "agent", "dropped", "empty/blocks", "anomalies", "adjustments",
            "grade", "dealbreakers", "hook rounds", "output tokens", "cost", "model"]
    lines = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    for row in rows:
        run = f"{row.get('ticker')} {Path(row['run']).name}"
        lines.append("| " + " | ".join(str(v) if v is not None else "" for v in (
            run, row["agent"], row["dropped_count"], f"{row['empty_blocks']}/{row['blocks']}",
            row.get("anomalies"), row.get("adjustments"), row.get("grade_score"),
            row.get("grade_dealbreakers"), row.get("gate_feedback_rounds"),
            row.get("output_tokens"), row.get("cost_usd"), row.get("model_served"))) + " |")
    classes: Counter = Counter()
    for row in rows:
        for reason, count in row.get("drops_by_reason", {}).items():
            classes[(row["file"], reason)] += count
    if classes:
        lines += ["", "| file | drop reason | items |", "|---|---|---|"]
        lines += [f"| {name} | {reason} | {count} |"
                  for (name, reason), count in classes.most_common()]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="what every run shows, one row per analysis")
    parser.add_argument("--runs", nargs="+", required=True,
                        help="run directories, or roots holding <ticker>/<accession>/")
    parser.add_argument("--table", action="store_true", help="markdown instead of JSON lines")
    args = parser.parse_args(argv)
    code = interpreter_pin.enforce()
    if code:
        return code
    rows = [row for root in args.runs for run in runs_under(Path(root)) for row in rows_of(run)]
    if args.table:
        sys.stdout.write(table(rows))
    else:
        for row in rows:
            print(json.dumps(row, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
