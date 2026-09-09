"""One series, however many names the company gave it.

A company that changes the tag it reports a line under does not change the
line. Apple's top line was `us-gaap:SalesRevenueNet` through the 10-Q filed
2018-08-01, `us-gaap:Revenues` in the 10-K filed 2018-11-05 and
`us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax` from the 10-Q
filed 2019-01-30. Read one tag at a time and the history has a hole in it
exactly where the change is; the trend table then compares a quarter against
nothing and the reader is told less than the filings say.

`docs/INPUT_SPEC.md` asks for the fix by name — a **tag-continuity map** that
"lives in `src/` as data and is versioned with the rules: it names the tag pairs
that are the same series under different names". That file is
`src/tag_continuity_map_v0.1.json` and this module is its reader. The map is
data because a pair changes what a number means: `docs/rules.md` says a change
to it is a rules change, not a code change, and the file is named by the rules
version for the same reason.

**Nothing here infers a pair.** A pair goes into the map because two filings
were read, and the entry names both — the accession that stopped using the
earlier name, the accession that started using the later one, and the one
period both of them report under the two names with the same value. This
module never writes the map and never adds to it; a tag it has no pair for is a
tag it reports unmatched, which is a question for whoever reads two filings
next.

Matching across periods, in the order `docs/INPUT_SPEC.md` states it:

1. **tag name** — the same string in both filings, and no judgement needed.
2. **a recorded pair** — the map, for the standard-taxonomy tags a company
   swapped. This is the step that is data rather than a guess.
3. **title similarity** — the fallback, and only when a *company-extension* tag
   is involved. An extension tag belongs to the company, is absent from
   companyfacts and has no recorded pair to find, so its heading is all there
   is. Two standard tags that differ and are not in the map stay unmatched
   rather than being paired on a resemblance: recording the pair is the work,
   and a resemblance is what recording it replaces.

The floor for step 3 is the one `src/diff_periods.py` already records for this
same fallback, read from there rather than restated, and what counts as a
quarter is `src/trends.py`'s `QUARTER_DAYS`. Neither number is this file's to
set.

**An absent period is absent.** Two committed accessions have no companyfacts
row at all — Carrier's and Littelfuse's quarterlies filed in late July 2026 —
so a quarter that only they report is not in this series. It comes back missing,
and `breaks` names the hole. It never comes back as a zero: a zero is a number
the filings do not contain.

    python3.12 -m src.tag_continuity --ticker AAPL --series revenue
    python3.12 -m src.tag_continuity --ticker AAPL --series revenue --cutoff 2019-01-30
"""

from __future__ import annotations

import argparse
import datetime as dt
import functools
import json
import re
import sys
from pathlib import Path

try:
    from src import (cutoff_guard, diff_periods, extract_numbers,
                     fetch_companyfacts, html_text, interpreter_pin, trends)
except ImportError:  # invoked as a plain script: python3.12 src/tag_continuity.py
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import (cutoff_guard, diff_periods, extract_numbers,
                     fetch_companyfacts, html_text, interpreter_pin, trends)

BAD_INPUT = 2

RULES_VERSION = "v0.1"
MAP_PATH = Path(__file__).resolve().parent / f"tag_continuity_map_{RULES_VERSION}.json"

# The taxonomies companyfacts holds. Everything else in an instance is the
# company's own extension, which `docs/INPUT_SPEC.md` says companyfacts does not
# carry — so an extension tag has no history to look a pair up in.
STANDARD_PREFIXES = frozenset(extract_numbers.NAMESPACES.values())

# The fallback's floor, and what counts as a quarter. Both are already recorded
# elsewhere in `src/` for exactly these jobs; naming them again with a number
# beside them would make two rules out of one.
TITLE_SIMILARITY_FLOOR = diff_periods.TITLE_SIMILARITY_FLOOR
QUARTER_DAYS = trends.QUARTER_DAYS

# How a pair may be made, and the two ways a tag has no counterpart at all. A
# tag that appeared and a tag that went away are changes, not absences, so they
# are pairs that say why they are half empty.
NO_PRIOR_TAG = "no_prior_tag"
NO_CURRENT_TAG = "no_current_tag"
MATCH_RULES = ("tag_name", "recorded_pair", "title_similarity",
               NO_PRIOR_TAG, NO_CURRENT_TAG)

# Every field a pair has to carry. A pair that does not name both filings is not
# a record of anything, and the loader refuses the whole file rather than
# quietly dropping the one entry — a map missing an entry stitches a series
# together in one run and not the next.
PAIR_FIELDS = ("ticker", "series", "unit", "earlier_tag", "later_tag",
               "earlier_filing", "later_filing", "both_report", "read_from")
FILING_FIELDS = ("accession", "form", "filed")
OVERLAP_FIELDS = ("start", "end", "value")

_CAMEL = re.compile(r"(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])")


class TagContinuityError(Exception):
    """The map could not be read, or was asked something it has no record of."""


# --- the map ----------------------------------------------------------------

def load(path=MAP_PATH) -> dict:
    """The map as it is written, refused rather than repaired if it is short.

    Every pair is checked here and nowhere else, so a caller that got a map
    back is holding one whose every entry names two filings and the period that
    shows they are the same line.

    Read once per path and kept: `match_tags` asks the map about every candidate
    pairing, and re-parsing the file for each of them turns one small read into
    a quadratic one. What comes back is the map itself, so a caller reads it and
    does not edit it.
    """
    return _load(str(Path(path)))


@functools.lru_cache(maxsize=None)
def _load(name: str) -> dict:
    path = Path(name)
    if not path.is_file():
        raise TagContinuityError(f"{path} does not exist — there is no tag-continuity map")
    document = json.loads(path.read_text(encoding="utf-8"))
    version = document.get("rules_version")
    if version != RULES_VERSION:
        raise TagContinuityError(
            f"{path.name} carries rules_version {version!r}, and this module reads "
            f"{RULES_VERSION!r} — the map is versioned with the rules, so the name and "
            "the field say the same thing or neither is trusted")
    recorded = document.get("pairs", [])
    for position, pair in enumerate(recorded):
        _check_pair(path, position, pair)
    _check_one_series_per_name(path, recorded)
    return document


def _check_pair(path: Path, position: int, pair) -> None:
    where = f"{path.name} pair {position}"
    if not isinstance(pair, dict):
        raise TagContinuityError(f"{where} is not an entry: {pair!r}")
    missing = [field for field in PAIR_FIELDS if not pair.get(field)]
    if missing:
        raise TagContinuityError(f"{where} names no {', '.join(missing)}")
    if pair["earlier_tag"] == pair["later_tag"]:
        raise TagContinuityError(
            f"{where} pairs {pair['earlier_tag']} with itself, which records no change")
    for side in ("earlier_filing", "later_filing"):
        filing = pair[side]
        if not isinstance(filing, dict) or any(not filing.get(f) for f in FILING_FIELDS):
            raise TagContinuityError(
                f"{where} {side} does not name {', '.join(FILING_FIELDS)} — a pair "
                "that does not say which filings were read is not a record")
    if pair["earlier_filing"]["accession"] == pair["later_filing"]["accession"]:
        raise TagContinuityError(
            f"{where} names one filing twice ({pair['earlier_filing']['accession']}); "
            "a tag change is one filing to another")
    overlap = pair["both_report"]
    if not isinstance(overlap, dict) or any(overlap.get(f) in (None, "")
                                            for f in OVERLAP_FIELDS):
        raise TagContinuityError(
            f"{where} both_report does not name {', '.join(OVERLAP_FIELDS)}")


def _check_one_series_per_name(path: Path, recorded: list[dict]) -> None:
    """One company, one name, one series.

    A name recorded in two series would make `series_of` answer with whichever
    pair happens to come first — a wrong answer given quietly, which is worse
    than the refusal here.
    """
    seen: dict[tuple[str, str], str] = {}
    for pair in recorded:
        for tag in (pair["earlier_tag"], pair["later_tag"]):
            key = (pair["ticker"], tag)
            if seen.setdefault(key, pair["series"]) != pair["series"]:
                raise TagContinuityError(
                    f"{path.name}: {pair['ticker']} {tag} is recorded in both "
                    f"{seen[key]} and {pair['series']}; one name is one series")


def pairs(ticker: str | None = None, series: str | None = None, *,
          path=MAP_PATH) -> list[dict]:
    """The recorded pairs, narrowed to one company or one series."""
    return [pair for pair in load(path)["pairs"]
            if (ticker is None or pair["ticker"] == ticker)
            and (series is None or pair["series"] == series)]


def tags_of(ticker: str, series: str, *, path=MAP_PATH) -> tuple[str, ...]:
    """Every name this company has reported one series under, oldest first.

    The pairs chain: `SalesRevenueNet` to `Revenues` to
    `RevenueFromContractWithCustomerExcludingAssessedTax` is two entries and
    three names, and a series read under any one of them is the same series.
    """
    recorded = pairs(ticker, series, path=path)
    if not recorded:
        raise TagContinuityError(
            f"no recorded pair for {ticker} {series} — the map says nothing about it")
    ordered: list[str] = []
    for pair in sorted(recorded, key=lambda p: p["earlier_filing"]["filed"]):
        for tag in (pair["earlier_tag"], pair["later_tag"]):
            if tag not in ordered:
                ordered.append(tag)
    return tuple(ordered)


def series_of(ticker: str, tag: str, *, path=MAP_PATH) -> str | None:
    """Which series this tag belongs to for this company, or None if unrecorded."""
    for pair in pairs(ticker, path=path):
        if tag in (pair["earlier_tag"], pair["later_tag"]):
            return pair["series"]
    return None


def is_recorded_pair(ticker: str, one: str, other: str, *, path=MAP_PATH) -> bool:
    """True when the map records these two names as one series for this company.

    Two spellings of one name are not a pair and need no map, so the same string
    twice is False: there is no change to record.
    """
    if one == other:
        return False
    here, there = series_of(ticker, one, path=path), series_of(ticker, other, path=path)
    return here is not None and here == there


def unit_of(ticker: str, series: str, *, path=MAP_PATH) -> str:
    """The unit the series is reported in, as the pairs record it."""
    units = {pair["unit"] for pair in pairs(ticker, series, path=path)}
    if len(units) != 1:
        raise TagContinuityError(
            f"{ticker} {series}: the recorded pairs name {sorted(units)} as the unit; "
            "one series is one unit")
    return units.pop()


# --- matching one period's tags against the period before -------------------

def is_extension(name: str) -> bool:
    """True for a tag that belongs to the company rather than to a taxonomy.

    The prefix decides. A name with no prefix makes no taxonomy claim, so it is
    not treated as a standard tag either.
    """
    prefix, _, local = name.partition(":")
    return not local or prefix not in STANDARD_PREFIXES


def title_of(tag: dict) -> str:
    """The heading this tag is printed under.

    A caller that knows the title says so, exactly as `src/diff_periods.py`'s
    pairing takes one. A caller that does not gets the element's own name with
    its capitals read as word breaks, which is the only title an extension tag
    carries when no label linkbase came with the filing.
    """
    if tag.get("title"):
        return html_text.normalized(tag["title"])
    local = tag["name"].partition(":")[2] or tag["name"]
    return html_text.normalized(_CAMEL.sub(" ", local))


def match_tags(current: list[dict], prior: list[dict], ticker: str, *,
               path=MAP_PATH) -> list[dict]:
    """Pair this period's tags with last period's: name, then map, then title.

    A tag is `{name}` and, when the caller has one, `{title}`. Every tag on
    either side is in exactly one pair and each pair says which rule made it,
    because a pairing a reader cannot reproduce from the same two filings is a
    pairing they have to take on faith.

    One whole rule at a time, in the spec's order, for the reason
    `src/diff_periods.pair_sections` states: every name pair is made before the
    first recorded pair and every recorded pair before the first title pair, so
    a later rule can never eat the counterpart an earlier one was going to use.
    """
    paired: dict[int, tuple[int, str, float]] = {}
    taken: set[int] = set()

    by_name: dict[str, list[int]] = {}
    for index, tag in enumerate(prior):
        by_name.setdefault(tag["name"], []).append(index)
    for index, tag in enumerate(current):
        queue = by_name.get(tag["name"])
        if queue:
            paired[index] = (queue.pop(0), "tag_name", 1.0)
            taken.add(paired[index][0])

    for index, tag in enumerate(current):
        if index in paired:
            continue
        for prior_index, was in enumerate(prior):
            if prior_index in taken:
                continue
            if is_recorded_pair(ticker, tag["name"], was["name"], path=path):
                paired[index] = (prior_index, "recorded_pair", 1.0)
                taken.add(prior_index)
                break

    open_now = [(index, title_of(tag)) for index, tag in enumerate(current)
                if index not in paired]
    open_before = [(index, title_of(tag)) for index, tag in enumerate(prior)
                   if index not in taken]
    candidates = sorted(
        ((diff_periods.similarity(title, was_title), index, prior_index)
         for index, title in open_now if title
         for prior_index, was_title in open_before
         if is_extension(current[index]["name"]) or is_extension(prior[prior_index]["name"])),
        key=lambda candidate: (-candidate[0], candidate[1], candidate[2]))
    for score, index, prior_index in candidates:
        if score < TITLE_SIMILARITY_FLOOR:
            break
        if index in paired or prior_index in taken:
            continue
        paired[index] = (prior_index, "title_similarity", score)
        taken.add(prior_index)

    matched = []
    for index, tag in enumerate(current):
        prior_index, matched_by, score = paired.get(index, (None, NO_PRIOR_TAG, 0.0))
        matched.append({"current": tag,
                        "prior": prior[prior_index] if prior_index is not None else None,
                        "matched_by": matched_by, "score": score})
    for index, tag in enumerate(prior):  # last period had it, this one does not
        if index not in taken:
            matched.append({"current": None, "prior": tag,
                            "matched_by": NO_CURRENT_TAG, "score": 0.0})
    return matched


# --- the series -------------------------------------------------------------

def history(ticker: str, cutoff=None, *, fixtures_root=cutoff_guard.FIXTURES) -> dict:
    """One company's standard-taxonomy facts, filtered to the cutoff.

    companyfacts is a catalogue of facts drawn from many filings and is not
    itself a filing, so the date gate is applied the way
    `src/cutoff_guard.load_index` applies it to the submissions index: the path
    is checked against the manifest, the record's own date basis is what it is
    gated on, and **the cutoff is applied to the rows**, which is where the
    look-ahead actually lives. `src/fetch_companyfacts.within_cutoff` does that
    filtering, so the record read here at a cutoff is the record the fetcher
    would have stored at that cutoff.
    """
    row = cutoff_guard.one_document(ticker, fetch_companyfacts.FORM,
                                    fetch_companyfacts.ROLE, fixtures_root=fixtures_root)
    raw = cutoff_guard.load_bytes(row["full_path"], row["filing_date"],
                                  fixtures_root=fixtures_root)
    as_of = str(cutoff or cutoff_guard.default_cutoff(ticker, fixtures_root=fixtures_root))
    return fetch_companyfacts.within_cutoff(json.loads(raw)["facts"], as_of)


def _days(start: str, end: str) -> int:
    return (dt.date.fromisoformat(end) - dt.date.fromisoformat(start)).days + 1


def quarters(facts: dict, tags, unit: str) -> list[dict]:
    """One point per quarter the filings report under any of these names.

    A quarter is a duration of `QUARTER_DAYS`; a year-to-date period is not one
    and neither is a year. Where a period was reported more than once the latest
    filing wins, which is the rule `docs/INPUT_SPEC.md` states for the cutoff —
    the rows are already filtered to it, so the latest here is the latest that
    was allowed in. A period two filings disagree about is not smoothed: the
    point carries the value of the filing that won and `superseded` lists what
    the earlier ones said.

    A period nothing reports is not a point. Nothing is interpolated, carried
    forward or defaulted to zero.
    """
    wanted = set(tags)
    found: dict[tuple[str, str], list[dict]] = {}
    for namespace, concepts in facts.items():
        for tag, concept in concepts.items():
            if f"{namespace}:{tag}" not in wanted:
                continue
            for row in concept.get("units", {}).get(unit, []):
                start, end = row.get("start"), row.get("end")
                if not start or not end:
                    continue  # an instant, which is a balance and not a period
                shortest, longest = QUARTER_DAYS
                if not shortest <= _days(start, end) <= longest:
                    continue
                found.setdefault((start, end), []).append(
                    {"start": start, "end": end, "value": row["val"],
                     "tag": f"{namespace}:{tag}", "accession": row["accn"],
                     "filed": row["filed"]})

    points = []
    for period in sorted(found):
        reported = sorted(found[period], key=lambda row: (row["filed"], row["accession"]))
        point = dict(reported[-1])
        point["superseded"] = [row for row in reported[:-1]
                               if row["value"] != point["value"]]
        points.append(point)
    return points


def series_quarters(ticker: str, name: str, cutoff=None, *, path=MAP_PATH,
                    fixtures_root=cutoff_guard.FIXTURES) -> list[dict]:
    """One company's series, under every name the map records for it."""
    return quarters(history(ticker, cutoff, fixtures_root=fixtures_root),
                    tags_of(ticker, name, path=path),
                    unit_of(ticker, name, path=path))


def breaks(points: list[dict]) -> list[dict]:
    """Where the series stops being one quarter after the last, if anywhere.

    A quarter follows the one before it when it starts the day after that one
    ended, which is the filer's own fiscal calendar and needs no tolerance. An
    empty list is what "unbroken" means here.
    """
    found = []
    for before, after in zip(points, points[1:]):
        expected = dt.date.fromisoformat(before["end"]) + dt.timedelta(days=1)
        if after["start"] != expected.isoformat():
            found.append({"after": before["end"], "before": after["start"],
                          "days_missing": (dt.date.fromisoformat(after["start"])
                                           - expected).days})
    return found


# --- the command line -------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--series", default="revenue")
    parser.add_argument("--cutoff", default=None,
                        help="ISO date; the default is the fixture set's own as-of date")
    parser.add_argument("--map", default=str(MAP_PATH))
    args = parser.parse_args(argv)

    try:
        names = tags_of(args.ticker, args.series, path=args.map)
        points = series_quarters(args.ticker, args.series, args.cutoff, path=args.map)
    except (TagContinuityError, cutoff_guard.CutoffGuardError) as exc:
        print(f"tag_continuity: {exc}", file=sys.stderr)
        return BAD_INPUT

    print(f"{args.ticker} {args.series}: {len(points)} quarters under "
          f"{len(names)} names, {' -> '.join(names)}")
    for point in points:
        print(f"  {point['start']}..{point['end']}  {point['value']:>18,}  "
              f"{point['tag']}  {point['accession']} filed {point['filed']}")
    for hole in breaks(points):
        print(f"  break: nothing between {hole['after']} and {hole['before']} "
              f"({hole['days_missing']} days)")
    return 0


if __name__ == "__main__":
    raise SystemExit(interpreter_pin.enforce() or main())
