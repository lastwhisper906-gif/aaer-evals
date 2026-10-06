"""What followed the anomalies, for runs at least sixty trading days old.

For each run whose cutoff is at least sixty trading days before today (weekdays,
which counts market holidays as trading days, so a run is called old a few days
early at most). The window starts on the first weekday after the cutoff: the cutoff
is the filing date, an acceptance time is not on the record, and a filing accepted
after the close is first traded on the next day, so the filing day itself is never
counted. It records:
- the anomalies listed, by frame (accounting; finance);
- events: company event rows of events/ledger.jsonl for the run's ticker dated
  after the cutoff. A company event row carries `ticker`, `date` and `event`; the
  ledger's process rows (a lens verdict, a night's bookkeeping, which carry `at`
  and no `event`) are not events that happened to the company and never count;
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


EVENT_KEYS = ("ticker", "date", "event")


def is_company_event(row) -> bool:
    return isinstance(row, dict) and all(isinstance(row.get(key), str) and row[key]
                                         for key in EVENT_KEYS)


def event_rows(ledger: Path) -> list[dict]:
    if not ledger.is_file():
        return []
    rows = []
    for line in ledger.read_text(encoding="utf-8").splitlines():
        try:
            row = json.loads(line)
        except ValueError:
            continue
        if is_company_event(row):
            rows.append(row)
    return rows


def events_for(ticker: str, after: dt.date, ledger: Path = LEDGER) -> list[dict]:
    out = []
    for row in event_rows(ledger):
        if row["ticker"] != ticker:
            continue
        try:
            when = dt.date.fromisoformat(row["date"][:10])
        except ValueError:
            continue
        if when > after:
            out.append(row)
    return out


def grade(runs: list[Path], today: dt.date | None = None, ledger: Path = LEDGER) -> dict:
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
                       events=len(events_for(manifest.get("ticker"), cutoff, ledger)),
                       abnormal_return="unavailable: no price series past the cutoff is "
                                       "committed in the repository")
        rows.append(row)
    aged = [r for r in rows if r["status"] == "aged"]
    return {"status": f"{len(aged)} aged, {len(rows) - len(aged)} pending"
                      + ("" if event_rows(ledger) else "; no company event row in the ledger yet"),
            "score": None, "runs": rows}
