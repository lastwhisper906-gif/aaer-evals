"""The market labels: each reader item against the market table, in Python.

The owner's decision of 2026-10-06 turned the two comparers into code. Their
label was always mechanical -- did the reaction window move the way the item
points, not at all, or the other way -- so a model reading a table it was told
not to do arithmetic on was a model guessing at a sign. This file reads the sign.

For every item of the two reader reports that carries an `id`, and for every
reaction window the market table records, one label:

| Label | When |
|---|---|
| `priced_in` | the window's abnormal return is outside the band and has the sign the item's `expected_direction` points to |
| `not_priced` | the abnormal return is inside the band, or there is no window, or the window carries no abnormal return, or the item names no direction |
| `opposite_direction` | the abnormal return is outside the band and has the other sign |

**The direction is read mechanically.** A reader's `expected_direction` is
`up`, `down` or `none` (`.claude/agents/numbers-reader.md`,
`.claude/agents/notes-text-reader.md`). `up` points to a positive abnormal
return and `down` to a negative one. Nothing here asks whether a rise in that
account is good or bad news for the shares; that would be a judgment, and the
decision was that the label is not one. An item whose direction is `none`, is
missing, or is anything else is `not_priced`, with the reason written beside it.

**The abnormal return is the window's own.** `src/market.py` writes each window
with `reaction_window`, the sum of the abnormal returns from reaction day zero
through reaction day two, and that sum is what is read. Every window is labelled
on its own and none is added to another: `docs/INPUT_SPEC.md` §4 records the
earnings-release window and the filing window separately, and so does this.

**The band.** `NEAR_ZERO_BAND` is how far from zero a three-day abnormal return
has to be before it counts as a move. Nothing in this repository fixes it -- not
`docs/CHECKLIST.md` §3, not `docs/INPUT_SPEC.md` §4, not `rules/` -- so it is a
default set here on 2026-10-06, under `CLAUDE.md`'s "proceed with the default and
leave one line", and every labels file writes the band it used beside its labels
so a later rules version that moves it is read against the one each run had.

**Short interest is a separate field and never moves a label.** The comparer
prompts folded it in ("the crowded-signal rule"); the decision keeps it apart.
For each window, the row of reaction day zero is read: when the table carries a
short-interest ratio and its two-year median there, `above_two_year_median` is
the ratio against the median, strictly, as `src/market.py` reads it; when it
does not, the field is written as missing with the reason. The series is read
out of the market table and from nowhere else, because the table is where
`src/market.py` attaches each FINRA report by its publication date, and a second
route in would be a route around that.

**No market table, no file.** A run with no `input_market.json` gets nothing
written: `write` hands back a record saying so, and every item's label stays
`absent`, as `docs/CHECKLIST.md` §3 says -- `absent` is not one of the three
labels and nothing here writes it.

    python3.12 -m src.market_labels --run runs/{ticker}/{accession}

Exit 0 when the file was written or there was no market table to write it from,
2 when the run cannot be labelled, 3 on the wrong interpreter.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import re
import sys
from pathlib import Path

try:
    from src import agent_inputs, cutoff_guard, interpreter_pin, market
except ImportError:  # invoked as a plain script: python3.12 src/market_labels.py
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import agent_inputs, cutoff_guard, interpreter_pin, market

BAD_INPUT = 2

PRICED_IN = "priced_in"
NOT_PRICED = "not_priced"
OPPOSITE_DIRECTION = "opposite_direction"
LABELS = (PRICED_IN, NOT_PRICED, OPPOSITE_DIRECTION)

# One percent of the share price, summed over reaction days zero to two. A
# default chosen in this file on 2026-10-06, not drawn from a filing, a rules
# file or a study: see the module docstring. A return whose distance from zero
# is no more than this is inside the band.
NEAR_ZERO_BAND = 0.01
NEAR_ZERO_BAND_SOURCE = (
    "a default set in src/market_labels.py on 2026-10-06; no document or rules "
    "file in this repository fixes it")

# What each reader direction points the abnormal return to.
DIRECTION_SIGN = {"up": 1, "down": -1}

# After the close, day zero is the next trading day: at most a weekend and one
# holiday away, four calendar days. The slack `windows` leaves, since the rows
# are the only calendar it has (see its docstring).
MOST_DAYS_TO_DAY_ZERO = 4

MARKET_TABLE = agent_inputs.MARKET_TABLE
READER_REPORTS = agent_inputs.READER_REPORTS
LABELS_FILE = "market_labels.json"
VERSUS_MARKET = "_versus_market"

NO_MARKET_TABLE = (f"the run holds no {MARKET_TABLE}, so there is no market to label "
                   "against; nothing is written and every item's label stays absent")
MANIFEST = "input_manifest.json"
NO_GATE_RECORD = ("{what}, so there is no record that the quote gate ran; an item the "
                  "gate dropped may still sit in the run-root report, and only the "
                  "drop list keeps it out of the labels. Nothing is written")


class MarketLabelError(Exception):
    """The run cannot be labelled from what it holds. Never turns into a label."""


# --- the reader reports --------------------------------------------------------

def report_items(text: str) -> list[dict]:
    """Every item in a report's fenced JSON blocks, in the order written.

    A block may hold one item or a list of them -- the notes reader has written
    forty in one list -- and a block that does not parse is passed over.
    """
    items = []
    for block in re.findall(r"```json\s*(.*?)```", text, re.S):
        try:
            item = json.loads(block)
        except ValueError:
            continue
        items += [one for one in (item if isinstance(item, list) else [item])
                  if isinstance(one, dict)]
    return items


# --- one label -----------------------------------------------------------------

def _number(value) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return float(value) if math.isfinite(value) else None


def label(expected_direction, abnormal_return, *, band: float = NEAR_ZERO_BAND
          ) -> tuple[str, str]:
    """The label for one item in one window, and the reason in words."""
    sign = DIRECTION_SIGN.get(expected_direction) if isinstance(expected_direction, str) else None
    if sign is None:
        return NOT_PRICED, (f"the item's expected_direction is {expected_direction!r}, "
                            "not up or down, so it points to no sign")
    moved = _number(abnormal_return)
    if moved is None:
        return NOT_PRICED, "the window carries no abnormal return"
    if abs(moved) <= band:
        return NOT_PRICED, (f"the abnormal return is within {band} of zero, the "
                            "near-zero band")
    if (moved > 0) == (sign > 0):
        return PRICED_IN, f"the abnormal return has the sign {expected_direction} points to"
    return OPPOSITE_DIRECTION, f"the abnormal return has the sign against {expected_direction}"


# --- the windows ---------------------------------------------------------------

def _row_on(table: dict, day: str) -> dict | None:
    return next((row for row in table.get("rows") or []
                 if isinstance(row, dict) and row.get("date") == day), None)


def short_interest(table: dict, day: str) -> dict:
    """Whether the short-interest ratio is above its two-year median on `day`.

    Read off the table's row for that day. Missing, with the reason, when the
    table has no row for the day or the row carries no ratio or no median --
    which is what `src/market.py` writes when no FINRA report had been
    published by then.
    """
    row = _row_on(table, day)
    if row is None:
        return {"date": day, "missing": f"the market table has no row for {day}"}
    ratio = _number(row.get("short_interest_ratio"))
    median = _number(row.get("short_interest_two_year_median"))
    if ratio is None or median is None:
        return {"date": day, "missing": (
            f"the market table carries no short-interest ratio and two-year median "
            f"on {day}: no short-interest series was given for that day")}
    above = ratio > median
    stated = row.get("short_interest_above_median")
    if stated is not None and stated is not above:
        raise MarketLabelError(
            f"the row for {day} says short interest above median is {stated!r}, "
            f"and its ratio {ratio!r} against its median {median!r} says {above!r}")
    return {"date": day, "above_two_year_median": above,
            "ratio": ratio, "two_year_median": median}


def windows(table: dict, *, run_cutoff: str | None = None) -> list[dict]:
    """Each recorded window: its kind, its day zero, its abnormal return, its short interest.

    Every window is held to `src/market.py`'s own definition of its days, read off
    the window's acceptance stamp and the table's rows (the trading calendar the
    table carries): day zero is the acceptance day when EDGAR accepted before the
    close and the next trading day when after it (`market.reaction_day_zero`), days
    one and two are the next two rows, the window's `filing_date` is one EDGAR can
    put on that acceptance (`market.filing_dates_for`), the table's cutoff is day
    two of the latest window, and no row lies past it. A window with no acceptance
    stamp cannot say its day zero and is refused.

    The rows are the only calendar on the record, so a table missing the row for
    its own day zero would otherwise be checked against itself: day zero would
    move to the next row the table does have, and the window would reach one
    trading day past the real reaction day two and pass. Beside the day zero
    read off the rows, then, the acceptance is held to the calendar it implies:
    when EDGAR accepted before the four o'clock close on a weekday, the
    acceptance day is day zero and has to be a row; when after the close, day
    zero has to lie within four calendar days of the acceptance, which is what a
    weekend and one holiday can take. The four days are the slack this leaves:
    a row missing on a Monday after a Friday close reads as a holiday here, and
    only the market module's own calendar can tell the two apart.

    Given the run's own cutoff (the filing date), the filing window's
    `filing_date` must be it: a table counted for some other filing is refused.
    Every other window is an earlier filing's -- the earnings release before the
    10-Q -- so one whose `filing_date` is after the run's cutoff is refused too:
    it is not an input, and it would otherwise carry the table's cutoff and the
    late-row limit out to its own day two. A table whose window sum disagrees
    with the rows it sums is refused as well: that is two answers to one
    question.
    """
    cutoff = table.get("cutoff")
    dates = sorted(str(row.get("date")) for row in table.get("rows") or [] if isinstance(row, dict))
    if dates and not (isinstance(cutoff, str) and cutoff):
        raise MarketLabelError("the market table names no cutoff, so nothing holds its rows")
    late = [day for day in dates if cutoff and day > cutoff]
    if late:
        raise MarketLabelError(
            f"the market table holds rows past its cutoff {cutoff}: {', '.join(late)}")
    calendar = [dt.date.fromisoformat(day) for day in dates]
    latest_day_two = None
    for window in table.get("windows") or []:
        kind, days = window.get("kind"), [str(d) for d in window.get("days") or []]
        if not days:
            raise MarketLabelError(f"the {kind} window names no days")
        if not window.get("accepted"):
            raise MarketLabelError(f"the {kind} window carries no acceptance stamp, so "
                                   "nothing says which day is its day zero")
        try:
            day_zero = market.reaction_day_zero(window["accepted"], calendar)
            permitted = market.filing_dates_for(window["accepted"])
            when = market._acceptance(window["accepted"])   # the exchange's clock
        except market.MarketError as exc:
            raise MarketLabelError(f"the {kind} window: {exc}") from exc
        # the row check beside the day zero read off the rows: see the docstring
        before_close = when.time() < market.MARKET_CLOSE
        gap = (day_zero - when.date()).days
        if before_close and when.date().weekday() < 5 and day_zero != when.date():
            raise MarketLabelError(
                f"the {kind} window: no row for its acceptance day {when.date()}, so its "
                f"day zero {day_zero} is a trading day late")
        if not before_close and gap > MOST_DAYS_TO_DAY_ZERO:
            raise MarketLabelError(
                f"the {kind} window: day zero {day_zero} is {gap} days after the "
                f"acceptance {window['accepted']}, more than a weekend and a holiday")
        at = calendar.index(day_zero)
        expected = [day.isoformat() for day in calendar[at:at + 3]]
        if len(expected) < 3:
            raise MarketLabelError(f"the {kind} window: the rows end before reaction day two")
        if days != expected or str(window.get("day_zero")) != expected[0]:
            raise MarketLabelError(
                f"the {kind} window's days {days} are not reaction days zero to two "
                f"{expected} of its acceptance {window['accepted']}")
        filed = str(window.get("filing_date"))
        if filed not in {d.isoformat() for d in permitted}:
            raise MarketLabelError(
                f"the {kind} window's filing date {filed} is not one EDGAR puts on an "
                f"acceptance at {window['accepted']}")
        if run_cutoff is not None and kind == "filing" and filed != run_cutoff:
            raise MarketLabelError(
                f"the filing window is for a filing dated {filed}, not this run's cutoff "
                f"{run_cutoff}: it is some other filing's table")
        if run_cutoff is not None and kind != "filing" and filed > run_cutoff:
            raise MarketLabelError(
                f"the {kind} window is for a filing dated {filed}, after the run's cutoff "
                f"{run_cutoff}: every window but the filing's is an earlier filing's, and "
                "a later one is not an input")
        latest_day_two = max(latest_day_two or expected[2], expected[2])
    if latest_day_two is not None and cutoff != latest_day_two:
        raise MarketLabelError(
            f"the table's cutoff {cutoff} is not reaction day two of its latest window "
            f"{latest_day_two}")
    found = []
    for window in table.get("windows") or []:
        kind, days = window.get("kind"), window.get("days") or []
        if not days:
            raise MarketLabelError(f"the {kind} window names no days")
        moved = _number(window.get("reaction_window"))
        if moved is not None:
            rows = [_row_on(table, day) for day in days]
            parts = [_number(row.get("abnormal_return")) if row else None for row in rows]
            if None in parts or not math.isclose(sum(parts), moved,
                                                 rel_tol=1e-9, abs_tol=1e-12):
                raise MarketLabelError(
                    f"the {kind} window's abnormal return {moved!r} is not the sum of "
                    f"its days' rows {parts!r}")
        found.append({"window": kind, "day_zero": days[0], "days": list(days),
                      "abnormal_return": moved,
                      "short_interest": short_interest(table, days[0])})
    return found


# --- every item ----------------------------------------------------------------

def item_labels(item: dict, report: str, recorded: list[dict], *,
                band: float = NEAR_ZERO_BAND) -> dict:
    """One reader item, labelled once per window, or once for having none."""
    direction = item.get("expected_direction")
    if recorded:
        labelled = []
        for window in recorded:
            said, why = label(direction, window["abnormal_return"], band=band)
            labelled.append({"window": window["window"],
                             "abnormal_return": window["abnormal_return"],
                             "label": said, "reason": why})
    else:
        labelled = [{"window": None, "abnormal_return": None, "label": NOT_PRICED,
                     "reason": "the market table records no reaction window"}]
    return {"id": f"{item['id']}{VERSUS_MARKET}", "upstream_item_id": item["id"],
            "report": report, "expected_direction": direction, "labels": labelled}


def labels(reports: dict[str, list[dict]], table: dict, *,
           band: float = NEAR_ZERO_BAND, dropped: set[str] | None = None,
           run_cutoff: str | None = None) -> dict:
    """The labels document for one run, from its reader items and its market table.

    `dropped` is the quote gate's drop list (`input_manifest.json`, `dropped_items`):
    an item the gate dropped keeps its place in a list block of the run-root report,
    so it is read here and set aside by id, never labelled, because a label cites
    the item and nothing downstream may cite an item that failed its quote.
    """
    if not isinstance(table, dict):
        raise MarketLabelError("the market table is not an object")
    recorded = windows(table, run_cutoff=run_cutoff)
    items, unlabelled = [], []
    for report in READER_REPORTS:
        for item in reports.get(report) or []:
            if not (isinstance(item.get("id"), str) and item["id"]):
                unlabelled.append({"report": report,
                                   "reason": "the item carries no id to cite"})
            elif item["id"] in (dropped or set()):
                unlabelled.append({"report": report, "id": item["id"],
                                   "reason": "dropped by the quote gate; nothing cites it"})
            else:
                items.append(item_labels(item, report, recorded, band=band))
    return {"ticker": table.get("ticker"), "cutoff": table.get("cutoff"),
            "near_zero_band": band, "near_zero_band_source": NEAR_ZERO_BAND_SOURCE,
            "windows": recorded, "items": items, "not_labelled": unlabelled}


# --- the run directory ---------------------------------------------------------

def _load(run: Path, name: str) -> str:
    try:
        return cutoff_guard.load_bundle_file(run, name)
    except cutoff_guard.CutoffGuardError as exc:
        raise MarketLabelError(str(exc)) from exc


def write(run) -> dict:
    """`market_labels.json` in the run directory, or the record of why not.

    Returns `{"written": True, "path": ..., "items": n}` or, with no market
    table, `{"written": False, "reason": ...}` and nothing on disk. The file is
    written once: the same bytes again change nothing, other bytes are refused.

    The quote gate's record is required. The run-root copy of a reader report
    keeps a whole list block whenever one of its items stood, so an item the
    gate dropped can still be in it, and the drop list in `input_manifest.json`
    (`dropped_items`, written by `src.quote_gate`) is the only thing that keeps
    it out of the labels. A run with no manifest, or a manifest with no
    `dropped_items` list, has no record that the gate ran, and is refused rather
    than read as "nothing dropped".
    """
    run = Path(run)
    if not run.is_dir():
        raise MarketLabelError(f"{run} is not a run directory")
    if not (run / MARKET_TABLE).is_file():
        return {"written": False, "reason": NO_MARKET_TABLE}
    try:
        table = json.loads(_load(run, MARKET_TABLE))
    except ValueError as exc:
        raise MarketLabelError(f"{MARKET_TABLE} does not read as JSON: {exc}") from exc
    reports = {name: report_items(_load(run, name)) for name in READER_REPORTS}
    manifest_path = run / MANIFEST
    if not manifest_path.is_file():
        raise MarketLabelError(NO_GATE_RECORD.format(what=f"the run holds no {MANIFEST}"))
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except ValueError as exc:
        raise MarketLabelError(f"{MANIFEST} does not read as JSON: {exc}") from exc
    if not isinstance(manifest, dict) or not isinstance(manifest.get("dropped_items"), list):
        raise MarketLabelError(NO_GATE_RECORD.format(
            what=f"{MANIFEST} carries no dropped_items list"))
    dropped = {row.get("item_id") for row in manifest["dropped_items"]
               if isinstance(row, dict) and row.get("item_id")}
    document = labels(reports, table, dropped=dropped, run_cutoff=manifest.get("cutoff"))
    text = json.dumps(document, indent=2, sort_keys=True) + "\n"
    target = run / LABELS_FILE
    if target.is_symlink():
        raise MarketLabelError(f"{target} is a symlink; the labels are a file of the run")
    if target.exists():
        if target.read_text(encoding="utf-8") != text:
            raise MarketLabelError(
                f"{target} is already on record with different content. A run "
                "directory is append-only; a correction is a new run")
    else:
        target.write_text(text, encoding="utf-8")
    return {"written": True, "path": str(target), "items": len(document["items"])}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="label every reader item against the run's market table")
    parser.add_argument("--run", required=True, help="the run directory")
    args = parser.parse_args(argv)
    try:
        result = write(Path(args.run))
    except (MarketLabelError, OSError) as exc:
        print(f"market_labels: {exc}", file=sys.stderr)
        return BAD_INPUT
    if result["written"]:
        print(f"market_labels: {result['items']} items labelled -> {result['path']}")
    else:
        print(f"market_labels: no market table -- {result['reason']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(interpreter_pin.enforce() or main())
