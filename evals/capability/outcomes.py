"""What followed the anomalies, for runs at least sixty trading days old.

For each run whose cutoff is at least sixty trading days before today (weekdays,
which counts market holidays as trading days, so a run is called old a few days
early at most):
- the anomalies listed, by frame (accounting; finance);
- events: rows of events/ledger.jsonl for the run's ticker dated after the cutoff;
- the abnormal return over the sixty days, when a committed price series past the
  cutoff exists; otherwise "unavailable", with the reason.

Younger runs are "pending". Nothing here is a verdict: it is the record the outcome
scoring will read once enough runs have aged.
"""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

from evals.common import REPO, load, run_name

TRADING_DAYS = 60
LEDGER = REPO / "events" / "ledger.jsonl"


def weekdays_between(start: dt.date, end: dt.date) -> int:
    days = (end - start).days
    return sum(1 for i in range(1, days + 1) if (start + dt.timedelta(i)).weekday() < 5)


def events_for(ticker: str, after: dt.date) -> list[dict]:
    if not LEDGER.is_file():
        return []
    out = []
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        try:
            row = json.loads(line)
        except ValueError:
            continue
        when = str(row.get("date") or row.get("at") or "")[:10]
        if row.get("ticker") == ticker and when and dt.date.fromisoformat(when) > after:
            out.append(row)
    return out


def grade(runs: list[Path], today: dt.date | None = None) -> dict:
    today = today or dt.date.today()
    rows = []
    for run in runs:
        manifest = load(run / "input_manifest.json") or {}
        cutoff = dt.date.fromisoformat(manifest["cutoff"])
        age = weekdays_between(cutoff, today)
        row = {"run": run_name(run), "cutoff": str(cutoff), "trading_days_since": age}
        if age < TRADING_DAYS:
            row["status"] = "pending"
        else:
            by_frame = {"accounting": len((load(run / "analysis_accounting.json") or {})
                                          .get("anomalies") or []),
                        "finance": len((load(run / "analysis_financial.json") or {})
                                       .get("anomalies") or [])}
            row.update(status="aged", anomalies=by_frame,
                       events=len(events_for(manifest.get("ticker"), cutoff)),
                       abnormal_return="unavailable: no price series past the cutoff is "
                                       "committed in the repository")
        rows.append(row)
    aged = [r for r in rows if r["status"] == "aged"]
    return {"status": f"{len(aged)} aged, {len(rows) - len(aged)} pending", "score": None,
            "runs": rows}
