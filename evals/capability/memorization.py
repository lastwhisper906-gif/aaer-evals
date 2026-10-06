"""Lookahead and memorization: is a run's filing inside its models' training data?

LLM forecasts on historical data are inflated by memorization, and the effect
vanishes after the training cutoff (docs/structure_changes.md, 2026-10-06). A run is
**forward** (clean) when its filing date is after the training cutoff of every model
that served it, and **historical** otherwise. A historical run needs a probe: an
anonymized re-run plus a "what happened next" question, reported beside its score.
The probe is a model run, so `make eval` only reports whether one is on record
(`memorization_probe.json` in the run directory).

TRAINING_CUTOFF holds the dates the owner has a source for. A model missing from it
is "unknown", never assumed clean.
"""

from __future__ import annotations

import datetime as dt
from pathlib import Path

from evals.common import load, run_name

# model id -> last month of training data, and where the date comes from
TRAINING_CUTOFF = {
    "claude-opus-5-5": ("2026-06", "the model's own system card line: knowledge cutoff June 2026"),
}


def classify(run: Path) -> dict:
    manifest = load(run / "input_manifest.json") or {}
    filed = manifest.get("filing_date") or manifest.get("cutoff")
    models = sorted({r.get("model_served") for r in (manifest.get("agents") or {}).values()
                     if r.get("model_served")})
    unknown = [m for m in models if m not in TRAINING_CUTOFF]
    row = {"run": run_name(run), "filed": filed, "models": models}
    if unknown:
        row["status"] = "unknown"
        row["detail"] = f"no training cutoff on record for {unknown}"
    else:
        last = max(TRAINING_CUTOFF[m][0] for m in models) if models else None
        historical = last is not None and filed[:7] <= last
        row["status"] = "historical" if historical else "forward"
    if row["status"] != "forward":
        probe = load(run / "memorization_probe.json")
        row["probe"] = probe.get("result") if isinstance(probe, dict) else "not run"
    return row


def grade(runs: list[Path]) -> dict:
    rows = [classify(run) for run in runs]
    counts = {s: sum(r["status"] == s for r in rows) for s in ("forward", "historical", "unknown")}
    return {"status": ", ".join(f"{v} {k}" for k, v in counts.items()), "score": None,
            "runs": rows}
