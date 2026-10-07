"""Size tonight's batch from the record: Fable tokens available over the median Fable
tokens a filing has cost.

The nightly worker runs this before it takes run items (docs/routines/nightly-worker.md)
and writes the calculation into the morning report. Every published run's
`input_manifest.json` records each agent's tokens; the Fable tokens of a filing are
the input, cache-write, cache-read and output tokens of every agent that a Fable
model served, every attempt counted. A filing with no Fable agent on record
counts for nothing, and a run the limit stopped, an analyst failed, or an error
left unfinished is not published and is not on record: the nightly crew commits a
run only when `finish` wrote its record (`docs/needs_judgment.md`).
A run that answers the limit exits `src.run_analysis.LIMIT_REACHED` (4; 3 is the
interpreter pin's), and the batch stops there.

    python3.12 -m src.fable_batch --available 3000000 --root runs
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path

try:
    from src import interpreter_pin, run_analysis
except ImportError:  # invoked as a plain script
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import interpreter_pin, run_analysis

TOKEN_KEYS = ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens",
              "output_tokens")


def agent_tokens(record: dict) -> int:
    """One agent's tokens: summed over every attempt the record lists, so a call
    that failed before it passed costs what it cost; an older record with no
    `attempts` list is read off its own fields."""
    attempts = record.get("attempts")
    rows = attempts if isinstance(attempts, list) and attempts else [record]
    return sum((row.get(key) or 0) for row in rows if isinstance(row, dict)
               for key in TOKEN_KEYS)


def fable_tokens(manifest: dict) -> int:
    """The tokens of every agent a Fable model served, read by the one predicate
    the runner uses for its retry budget and its limit reading."""
    return sum(agent_tokens(record)
               for record in (manifest.get("agents") or {}).values()
               if isinstance(record, dict) and run_analysis.is_fable(record.get("model_served")))


def published(manifest: dict) -> bool:
    """Whether the manifest is a finished run's: `finish` wrote it (`analysed_utc`),
    no `analysis_failure` and no `fable_limit_reached`. A run the limit stopped,
    an analyst failed, or an error left before `finish`, cost fewer tokens than a
    filing costs, and would pull the median down."""
    return (isinstance(manifest, dict) and run_analysis.FINISH_MARKER in manifest
            and manifest.get("analysis_failure") is None
            and manifest.get("fable_limit_reached") is None)


def on_record(root: Path) -> dict[str, int]:
    """Fable tokens per published filing that cost any, under a directory of
    `<ticker>/<accession>` runs the caller names, as `src/analysis_scorecard.py`
    reads them: manifests are the run's own record, not a gated document. A
    stopped or failed run is not a published filing and is not counted."""
    out = {}
    for path in sorted(Path(root).glob("*/*/input_manifest.json")):
        try:
            manifest = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if not published(manifest):
            continue
        tokens = fable_tokens(manifest)
        if tokens:
            out[f"{path.parent.parent.name}/{path.parent.name}"] = tokens
    return out


def size(available: int, record: dict[str, int]) -> dict:
    """The batch, and the calculation in words; the two say the same thing."""
    if not record:
        return {"batch": 1, "median_per_filing": None, "filings_on_record": 0,
                "calculation": "no published filing on record cost any Fable tokens, so the "
                               "batch is one filing, and its record sizes the next night"}
    median = statistics.median(record.values())
    batch = int(available // median) if median else 0
    return {"batch": batch, "median_per_filing": median, "filings_on_record": len(record),
            "available": available,
            "calculation": f"{available:,} Fable tokens available ÷ median {median:,.0f} per "
                           f"filing over {len(record)} filing(s) on record = {batch} filing(s)"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="size tonight's Fable batch from the record")
    parser.add_argument("--available", type=int, required=True, help="Fable tokens left tonight")
    parser.add_argument("--root", required=True, help="a directory of <ticker>/<accession> runs")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    code = interpreter_pin.enforce()
    if code:
        return code
    out = size(args.available, on_record(Path(args.root)))
    print(json.dumps(out, indent=1) if args.json else out["calculation"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
