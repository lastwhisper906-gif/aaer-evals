"""What followed the anomalies, for runs at least sixty trading days old.

For each run whose cutoff is at least sixty trading days before today, on the
exchange calendar the regression grader works by rule (weekends, the holidays,
the closures listed by hand). The window starts after reaction day two, which the
inputs may have seen (`docs/HOW_WE_WORK.md` §4, the cutoff re-check). Where the
run holds a market table, reaction day two is day two of its latest window. Where
it holds none, the manifest records no acceptance time, so day zero is taken at
its latest, the next trading day after the filing date (an acceptance after the
close), and day two is two trading days on. It records:
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
from evals.regression.mechanical import is_trading_day, market_reaction_day_two, trading_days_from

TRADING_DAYS = 60


def _trading_days_after(day: dt.date, count: int) -> dt.date:
    """The `count`-th trading day after `day`, on the exchange calendar."""
    return trading_days_from(day + dt.timedelta(days=1), count)[-1]


def last_day_an_input_may_see(run: Path, cutoff: dt.date) -> dt.date:
    """Reaction day two: day two of the market table's latest window where the run
    holds one; else, with no acceptance time on record, day zero at its latest is
    the first trading day after the filing date and day two the third."""
    # the table's latest day two, as its windows record it -- never its self-declared
    # cutoff, which the regression check holds to the same windows
    day_two = market_reaction_day_two(load(run / "input_market.json"))
    if day_two is not None:
        return day_two
    return _trading_days_after(cutoff, 3)


def first_outcome_day(run: Path, cutoff: dt.date) -> dt.date:
    return _trading_days_after(last_day_an_input_may_see(run, cutoff), 1)
LEDGER = REPO / "events" / "ledger.jsonl"


def trading_days_between(start: dt.date, end: dt.date) -> int:
    """Trading days after `start` up to and including `end`, on the exchange calendar."""
    days = (end - start).days
    return sum(1 for i in range(1, days + 1) if is_trading_day(start + dt.timedelta(i)))


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
        last_seen = last_day_an_input_may_see(run, cutoff)
        first = first_outcome_day(run, cutoff)
        age = trading_days_between(last_seen, today)
        row = {"run": run_name(run), "cutoff": str(cutoff),
               "last_day_an_input_may_see": str(last_seen), "first_outcome_day": str(first),
               "trading_days_in_window": age}
        if age < TRADING_DAYS:
            row["status"] = "pending"
        else:
            by_frame = {"accounting": len((load(run / "analysis_accounting.json") or {})
                                          .get("anomalies") or []),
                        "finance": len((load(run / "analysis_financial.json") or {})
                                       .get("anomalies") or [])}
            row.update(status="aged", anomalies=by_frame,
                       events=len(events_for(manifest.get("ticker"), last_seen, ledger)),
                       abnormal_return="unavailable: no price series past the cutoff is "
                                       "committed in the repository")
        rows.append(row)
    aged = [r for r in rows if r["status"] == "aged"]
    return {"status": f"{len(aged)} aged, {len(rows) - len(aged)} pending"
                      + ("" if event_rows(ledger) else "; no company event row in the ledger yet"),
            "score": None, "runs": rows}
