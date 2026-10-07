"""Size tonight's batch from the record: Fable tokens available over the median Fable
tokens a filing has cost.

The nightly worker runs this before it takes run items (docs/routines/nightly-worker.md)
and writes the calculation into the morning report. Every published run's
`input_manifest.json` records each agent's tokens; the Fable tokens of a filing are
the input, cache-write, cache-read and output tokens of every agent that a Fable
model served. A filing with no Fable agent on record counts for nothing, and a
run the limit stopped or an analyst failed is not published and is not on record.
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
    from src import interpreter_pin
except ImportError:  # invoked as a plain script
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import interpreter_pin

TOKEN_KEYS = ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens",
              "output_tokens")


def fable_tokens(manifest: dict) -> int:
    return sum(sum(record.get(key) or 0 for key in TOKEN_KEYS)
               for record in (manifest.get("agents") or {}).values()
               if str(record.get("model_served") or "").startswith("claude-fable"))


def published(manifest: dict) -> bool:
    """Whether the manifest is a finished run's: no `analysis_failure` and no
    `fable_limit_reached`. A run the limit stopped, or an analyst failed, cost
    fewer tokens than a filing costs, and would pull the median down."""
    return (isinstance(manifest, dict) and manifest.get("analysis_failure") is None
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
