"""Size tonight's batch from the record: Fable tokens available over the median Fable
tokens a filing has cost.

The nightly worker runs this before it takes run items (docs/routines/nightly-worker.md)
and writes the calculation into the morning report. Every published run's
`input_manifest.json` records each agent's tokens; the Fable tokens of a filing are
the input, cache-write, cache-read and output tokens of every attempt a Fable
model served, over every agent -- a failed attempt counted, an attempt served by
another model not. A filing with no Fable-served attempt on record counts for
nothing, and a run the limit stopped, an analyst failed, or an error left
unfinished is not published and is not on record: the nightly crew commits a run
only when `finish` wrote its record (`docs/needs_judgment.md`).

A run that fell back to Opus at the limit (the owner's decision of 2026-10-07,
`src/run_analysis.py --on-fable-limit opus`) finished and is published; its
manifest carries `model_fallback`, each fallback attempt's row says it asked for
Opus, and only its Fable-served attempts count toward the median -- a fallback
attempt's tokens are on record and are not Fable tokens. A run that carried the
batch's fallback from its first call (`--carry-fallback-from`) asked Fable for
nothing, so it costs no Fable token and is not on record. `size` reports how
many filings of the record fell back, so the morning report can say the median
stands over filings that did not all run on Fable to the end. Under
`--on-fable-limit stop` a run that answers the limit exits
`src.run_analysis.LIMIT_REACHED` (4; 3 is the interpreter pin's), and the batch
stops there.

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


def fable_served(row: dict, record: dict) -> bool:
    """Whether one attempt was served by Fable, read by the one predicate the
    runner uses: off the model that served it; for a row with none on record (a
    call that failed before any model answered), off what the row asked for,
    and for an older row that says neither, off what the agent asked for."""
    served = row.get("model_served")
    if served:
        return run_analysis.is_fable(served)
    return run_analysis.is_fable(row.get("model_requested") or record.get("model_requested"))


def agent_tokens(record: dict) -> int:
    """One agent's Fable tokens: summed over every attempt the record lists that
    Fable served, so a call that failed before it passed costs what it cost and
    a fallback attempt on Opus costs no Fable token; an older record with no
    `attempts` list is read off its own fields."""
    attempts = record.get("attempts")
    rows = attempts if isinstance(attempts, list) and attempts else [record]
    return sum((row.get(key) or 0) for row in rows
               if isinstance(row, dict) and fable_served(row, record)
               for key in TOKEN_KEYS)


def fable_tokens(manifest: dict) -> int:
    """The Fable tokens of every agent on record, attempt by attempt."""
    return sum(agent_tokens(record)
               for record in (manifest.get("agents") or {}).values()
               if isinstance(record, dict))


def published(manifest: dict) -> bool:
    """Whether the manifest is a finished run's: `finish` wrote it (`analysed_utc`),
    no `analysis_failure` and no `fable_limit_reached`. A run the limit stopped,
    an analyst failed, or an error left before `finish`, cost fewer tokens than a
    filing costs, and would pull the median down."""
    return (isinstance(manifest, dict) and run_analysis.FINISH_MARKER in manifest
            and manifest.get("analysis_failure") is None
            and manifest.get("fable_limit_reached") is None)


def published_manifests(root: Path):
    """Each published run under a directory of `<ticker>/<accession>` runs the
    caller names, as `src/analysis_scorecard.py` reads them: manifests are the
    run's own record, not a gated document."""
    for path in sorted(Path(root).glob("*/*/input_manifest.json")):
        try:
            manifest = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if published(manifest):
            yield f"{path.parent.parent.name}/{path.parent.name}", manifest


def on_record(root: Path) -> dict[str, int]:
    """Fable tokens per published filing that cost any. A stopped or failed run
    is not a published filing and is not counted."""
    out = {}
    for name, manifest in published_manifests(root):
        tokens = fable_tokens(manifest)
        if tokens:
            out[name] = tokens
    return out


def fell_back(root: Path) -> list[str]:
    """The published filings whose manifest records a fallback to Opus."""
    return [name for name, manifest in published_manifests(root)
            if run_analysis.recorded_fallback(manifest)]


def size(available: int, record: dict[str, int], fell_back: list[str] | tuple[str, ...] = ()
         ) -> dict:
    """The batch, and the calculation in words; the two say the same thing.
    `fell_back` names the filings that fell back to Opus; the ones in the record
    are counted and named, since their Fable tokens are a part of a filing's."""
    fallen = sorted(name for name in fell_back if name in record)
    if not record:
        return {"batch": 1, "median_per_filing": None, "filings_on_record": 0, "fell_back": 0,
                "fell_back_filings": [],
                "calculation": "no published filing on record cost any Fable tokens, so the "
                               "batch is one filing, and its record sizes the next night"}
    median = statistics.median(record.values())
    batch = int(available // median) if median else 0
    return {"batch": batch, "median_per_filing": median, "filings_on_record": len(record),
            "available": available, "fell_back": len(fallen), "fell_back_filings": fallen,
            "calculation": f"{available:,} Fable tokens available ÷ median {median:,.0f} per "
                           f"filing over {len(record)} filing(s) on record = {batch} filing(s)"
                           + (f"; {len(fallen)} of them fell back to {run_analysis.FALLBACK_MODEL}"
                              f" at the limit ({', '.join(fallen)}) and count their Fable-served "
                              "attempts only" if fallen else "")}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="size tonight's Fable batch from the record")
    parser.add_argument("--available", type=int, required=True, help="Fable tokens left tonight")
    parser.add_argument("--root", required=True, help="a directory of <ticker>/<accession> runs")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    code = interpreter_pin.enforce()
    if code:
        return code
    root = Path(args.root)
    out = size(args.available, on_record(root), fell_back(root))
    print(json.dumps(out, indent=1) if args.json else out["calculation"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
