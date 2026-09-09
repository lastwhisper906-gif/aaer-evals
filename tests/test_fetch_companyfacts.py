"""The fetched companyfacts against the XBRL instances already on record.

The expected values are not this fetcher's output. They are the numbers in the
XBRL instances `src/fetch_fixtures.py` committed before this branch existed:
every `us-gaap` element in those instances that carries a `unitRef` and a value
is looked up in the company's companyfacts document and matched by value. Two
documents EDGAR served, compared against each other; the fetcher passes when it
has carried one of them across without changing a number.

Nothing is tolerated by a band. Every difference is listed in the failure
message. These classes of difference are legitimate, and each is named here and
asserted **from both sides**, so that naming a class cannot become a way of not
looking. Every us-gaap element in every instance falls into exactly one of them
or is checked, and `test_every_us_gaap_fact_falls_into_one_bucket` is what makes
that an arithmetic identity rather than a hope:

* **A fact reported against a segment.** Companyfacts holds the entity-wide
  value alone. Asserted the other way too: of the `(tag, unit, period)` keys
  this fixture set reports *only* against a segment, companyfacts must hold a
  row for none of them, and there must be `SEGMENT_ONLY_KEYS` of them. A class
  that also swallowed undimensioned facts would show up here as a row that
  exists, or as a class that had grown.
* **A same-day duration.** A context whose `startDate` equals its `endDate` --
  a settlement on 2026-04-03, a stock split on 2024-12-12 -- is a duration of
  no length, and companyfacts carries no row for one. Asserted both ways: every
  such group is absent, and every absence is such a group.
* **Duplication inside one filing.** An instance reports the same tag, unit and
  period in the statement and again in a note; companyfacts records it once. So
  the instance side is grouped, and where a group holds more than one value the
  filing reported the same fact at two roundings -- companyfacts keeps the
  precise one, and each other value must be that value rounded to its own
  `decimals`, which is checked rather than assumed.
* **A filing companyfacts has not loaded.** Two of the thirty-six instances in
  this fixture set are in no companyfacts row at all; see
  `NOT_YET_IN_COMPANYFACTS`. That is a gap in the source, not a difference in a
  value, and it is recorded by accession so a third one fails this file.
* **A fact that states there is no value**, `xsi:nil`. There is nothing to look
  up. A fact that is not nil and whose text is not a number would be a
  comparison this file cannot make, so it is listed rather than passed over.

Company-extension tags are absent from companyfacts by design, as
`docs/INPUT_SPEC.md` says. They are also outside the claim: the judge is over
`us-gaap`, which is the namespace companyfacts holds.
"""

from __future__ import annotations

import functools
import gzip
import hashlib
import json
from collections import defaultdict
from pathlib import Path

import pytest

from src import fetch_companyfacts
from src.extract_numbers import facts_from_instance
from src.fetch_fixtures import TICKERS

FIXTURES = Path(__file__).resolve().parent / "fixtures"
INSTANCE_ROLES = ("xbrl_instance", "prior_period_xbrl_instance")

# A gzipped fixture says so in its first two bytes, so a reader never has to ask
# the manifest what it is holding.
GZIP_MAGIC = b"\x1f\x8b"

# Companyfacts is built from filings as EDGAR loads them, and on the day this
# fixture set was fetched two filings had not been loaded: neither accession
# appears in any row of its company's companyfacts. Recorded rather than
# skipped, because it is the source's own gap and the trend table will have to
# read those two quarters out of the instance.
NOT_YET_IN_COMPANYFACTS = {
    ("CARR", "10-Q", "0001783180-26-000032"),   # filed 2026-07-28
    ("LFUS", "10-Q", "0001628280-26-050481"),   # filed 2026-07-29
}

# How big the two exclusions are over this frozen fixture set, counted by
# `test_the_segment_class_is_the_size_it_is` and
# `test_the_same_day_class_is_the_size_it_is`. A class that is allowed to grow
# without anyone noticing is a class a real miss can hide inside.
SEGMENT_ONLY_KEYS = 3544
SAME_DAY_GROUPS = 16


# --- reading the two records -------------------------------------------------

def manifest(ticker: str) -> dict:
    return json.loads((FIXTURES / ticker / "manifest.json").read_text())


def stored_bytes(ticker: str, entry: dict) -> bytes:
    data = (FIXTURES / ticker / entry["path"]).read_bytes()
    return gzip.decompress(data) if entry["stored"] == "gzip" else data


def companyfacts_entry(ticker: str) -> dict:
    rows = [entry for entry in manifest(ticker)["documents"]
            if (entry["form"], entry["role"])
            == (fetch_companyfacts.FORM, fetch_companyfacts.ROLE)]
    assert len(rows) == 1, f"{ticker}: {len(rows)} companyfacts rows in the manifest"
    return rows[0]


def unit_name(unit: str) -> str:
    """The instance writes `iso4217:USD`; companyfacts keys the same unit `USD`."""
    return "/".join("*".join(measure.split(":")[-1] for measure in part.split("*"))
                    for part in unit.split("/"))


@functools.lru_cache(maxsize=None)
def record(ticker: str) -> dict:
    """One company's companyfacts, read once and kept as what these tests ask it.

    `index` is `(tag, unit, accession, start, end)` → the values companyfacts
    records under it, over `us-gaap` alone. The twelve documents are ninety
    megabytes of JSON before they are parsed, so what is held is that index and
    the dates, not the document.
    """
    document = json.loads(stored_bytes(ticker, companyfacts_entry(ticker)))
    as_of = manifest(ticker)["as_of"]
    index: dict[tuple, list] = defaultdict(list)
    latest, late = "", []
    for namespace, concepts in document["facts"].items():
        for tag, concept in concepts.items():
            for unit, rows in concept["units"].items():
                for row in rows:
                    latest = max(latest, row["filed"])
                    if row["filed"] > as_of:
                        late.append(f"{namespace}:{tag} [{unit}] {row['accn']} "
                                    f"filed {row['filed']}")
                    if namespace == "us-gaap":
                        index[(tag, unit, row["accn"],
                               row.get("start"), row["end"])].append(float(row["val"]))
    return {"index": {key: tuple(values) for key, values in index.items()},
            "latest_filed": latest, "filed_after_the_cutoff": late,
            "names": {name: document[name]
                      for name in ("ticker", "cik", "as_of", "url")}}


def instance_facts(ticker: str, entry: dict) -> list[dict]:
    """Every us-gaap element carrying a unit in one committed XBRL instance."""
    return [fact for fact in
            facts_from_instance(stored_bytes(ticker, entry),
                                accession=entry["accession"],
                                filing_date=entry["filing_date"], form=entry["form"])
            if fact["prefix"] == "us-gaap"]


# --- the comparison ----------------------------------------------------------

def key_of(fact: dict) -> tuple:
    context = fact["context"]
    return (fact["tag"], unit_name(fact["unit"]), context.get("start"),
            context.get("end") or context.get("instant"))


def has_a_segment(fact: dict) -> bool:
    context = fact["context"]
    return bool(context.get("segment") or context.get("typed_segment"))


def same_day(key: tuple) -> bool:
    """A duration whose start and end are one day: no length, and no row."""
    _, _, start, end = key
    return start is not None and start == end


def undimensioned_groups(facts: list[dict]) -> dict[tuple, list[dict]]:
    """The entity-wide facts, gathered by the key companyfacts records them under."""
    grouped: dict[tuple, list[dict]] = defaultdict(list)
    for fact in facts:
        if not has_a_segment(fact):
            grouped[key_of(fact)].append(fact)
    return dict(grouped)


def looked_up(grouped: dict[tuple, list[dict]]) -> dict[tuple, list[dict]]:
    """Of those, the ones this file looks up: an instant, or a duration with length."""
    return {key: members for key, members in grouped.items() if not same_day(key)}


def named(key: tuple) -> str:
    tag, unit, start, end = key
    return f"{tag} [{unit}] {start + '..' if start else 'at '}{end}"


def compare(grouped: dict[tuple, list[dict]], index: dict,
            accession: str) -> tuple[int, list[str]]:
    """Look every group up in companyfacts. One line per difference, all of them."""
    matched, differences = 0, []
    for key in sorted(grouped):
        members = grouped[key]
        tag, unit, start, end = key
        values = set(index.get((tag, unit, accession, start, end), ()))
        filed = sorted({member["number"] for member in members})
        if not values:
            differences.append(f"{named(key)}: no companyfacts row under "
                               f"{accession}; the instance filed {filed}")
            continue
        if len(values) != 1:
            differences.append(f"{named(key)}: companyfacts holds {sorted(values)} "
                               f"under one accession; the instance filed {filed}")
            continue
        recorded = values.pop()
        if recorded not in filed:
            differences.append(f"{named(key)}: companyfacts says {recorded}, the "
                               f"instance filed {filed}")
            continue
        matched += 1
        for member in members:
            if member["number"] == recorded:
                continue
            try:
                rounded = round(recorded, int(member["decimals"]))
            except (TypeError, ValueError):
                rounded = None
            if rounded != member["number"]:
                differences.append(
                    f"{named(key)}: the instance also filed {member['number']} at "
                    f"decimals={member['decimals']!r}, which is not {recorded} "
                    f"rounded to it")
    return matched, differences


@functools.lru_cache(maxsize=None)
def comparison(ticker: str) -> dict:
    """Every committed instance of one company, held against its companyfacts."""
    index = record(ticker)["index"]
    loaded = {key[2] for key in index}
    report = {"instances": 0, "us_gaap_facts": 0, "matched": 0, "groups": 0,
              "checked": 0, "differences": [], "unreadable": [],
              "no_value": 0, "in_an_unloaded_filing": 0, "unloaded": [],
              "against_a_segment": 0, "in_a_same_day_period": 0,
              "same_day": [], "same_day_with_a_row": [],
              "dimensional_only": 0, "dimensional_with_a_row": []}

    for entry in manifest(ticker)["documents"]:
        if entry["role"] not in INSTANCE_ROLES:
            continue
        report["instances"] += 1
        accession = entry["accession"]
        facts = instance_facts(ticker, entry)
        report["us_gaap_facts"] += len(facts)
        report["no_value"] += sum(1 for fact in facts if fact["nil"])
        report["unreadable"].extend(
            f"{entry['role']} {named(key_of(fact))}: value {fact['value']!r} is not a number"
            for fact in facts if not fact["nil"] and fact["number"] is None)
        numeric = [fact for fact in facts if fact["number"] is not None]

        if accession not in loaded:
            report["unloaded"].append((entry["form"], accession, entry["filing_date"]))
            report["in_an_unloaded_filing"] += len(numeric)
            continue

        segmented = {key_of(fact) for fact in numeric if has_a_segment(fact)}
        report["against_a_segment"] += sum(1 for fact in numeric if has_a_segment(fact))
        undimensioned = undimensioned_groups(numeric)
        # A key the instance reports only against a segment: companyfacts holds
        # the entity-wide value alone, so there must be no row under it.
        for key in sorted(segmented - set(undimensioned)):
            report["dimensional_only"] += 1
            tag, unit, start, end = key
            if index.get((tag, unit, accession, start, end)):
                report["dimensional_with_a_row"].append(f"{entry['role']} {named(key)}")
        for key in sorted(key for key in undimensioned if same_day(key)):
            tag, unit, start, end = key
            report["same_day"].append(f"{entry['role']} {named(key)}")
            report["in_a_same_day_period"] += len(undimensioned[key])
            if index.get((tag, unit, accession, start, end)):
                report["same_day_with_a_row"].append(f"{entry['role']} {named(key)}")

        payable = looked_up(undimensioned)
        matched, differences = compare(payable, index, accession)
        report["groups"] += len(payable)
        report["matched"] += matched
        report["checked"] += sum(len(members) for members in payable.values())
        report["differences"].extend(f"{entry['role']} {line}" for line in differences)
    return report


# --- the record is on disk and hashed ---------------------------------------

@pytest.mark.parametrize("ticker", TICKERS)
def test_every_company_has_a_companyfacts_record_with_its_hash(ticker):
    entry = companyfacts_entry(ticker)
    raw = stored_bytes(ticker, entry)
    assert len(raw) == entry["bytes"], f"{ticker} {entry['path']}: length changed"
    assert hashlib.sha256(raw).hexdigest() == entry["sha256"], \
        f"{ticker} {entry['path']}: content changed"
    assert entry["url"] == fetch_companyfacts.COMPANYFACTS_URL.format(
        cik=manifest(ticker)["cik"])


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_record_names_the_company_it_is_filed_under(ticker):
    """A document fetched under the wrong CIK would land in the right directory."""
    book = manifest(ticker)
    assert record(ticker)["names"] == {
        "ticker": ticker, "cik": book["cik"], "as_of": book["as_of"],
        "url": companyfacts_entry(ticker)["url"]}


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_stored_file_says_it_is_gzipped_without_being_asked(ticker):
    entry = companyfacts_entry(ticker)
    head = (FIXTURES / ticker / entry["path"]).read_bytes()[:2]
    assert (head == GZIP_MAGIC) == (entry["stored"] == "gzip"), \
        f"{ticker} {entry['path']}: stored={entry['stored']!r}, first bytes {head!r}"


@pytest.mark.parametrize("ticker", TICKERS)
def test_no_fact_in_the_record_was_filed_after_the_cutoff(ticker):
    late = record(ticker)["filed_after_the_cutoff"]
    assert not late, (f"{ticker}: {len(late)} facts filed after "
                      f"{manifest(ticker)['as_of']}:\n" + "\n".join(late[:20]))


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_recorded_date_is_the_latest_filing_the_record_carries(ticker):
    entry = companyfacts_entry(ticker)
    assert entry["filing_date"] == record(ticker)["latest_filed"]
    assert entry["date_basis"] == fetch_companyfacts.DATE_BASIS


def test_a_fact_filed_after_the_cutoff_is_dropped_and_its_concept_with_it():
    """The filter, on a document built here so the expected output is planted."""
    served = {
        "Revenues": {"units": {"USD": [
            {"start": "2026-01-01", "end": "2026-03-31", "val": 10,
             "accn": "before", "filed": "2026-04-30"},
            {"start": "2026-04-01", "end": "2026-06-30", "val": 20,
             "accn": "after", "filed": "2026-09-02"},
        ]}},
        "OnlyEverFiledLater": {"units": {"USD": [
            {"end": "2026-06-30", "val": 30, "accn": "after", "filed": "2026-09-02"},
        ]}},
    }
    kept = fetch_companyfacts.within_cutoff({"us-gaap": served}, "2026-09-01")
    assert list(kept["us-gaap"]) == ["Revenues"]
    assert [row["accn"] for row in kept["us-gaap"]["Revenues"]["units"]["USD"]] \
        == ["before"]
    assert fetch_companyfacts.latest_filed(kept) == "2026-04-30"
    assert fetch_companyfacts.undated({"us-gaap": served}) == []


# --- the judge ---------------------------------------------------------------

@pytest.mark.parametrize("ticker", TICKERS)
def test_every_us_gaap_fact_in_the_instance_is_in_companyfacts_at_the_same_value(ticker):
    report = comparison(ticker)
    assert not report["unreadable"], \
        f"{ticker}: a us-gaap fact carries a unit and a value that is not a number:\n" \
        + "\n".join(report["unreadable"])
    assert not report["differences"], (
        f"{ticker}: {len(report['differences'])} of {report['groups']} "
        f"tag/unit/period groups differ between the instance and companyfacts:\n"
        + "\n".join(report["differences"]))
    assert report["matched"] == report["groups"]
    assert report["groups"] > 0


@pytest.mark.parametrize("ticker", TICKERS)
def test_every_us_gaap_fact_falls_into_one_bucket(ticker):
    """Checked, or in one of the named classes. Nothing quietly in neither."""
    report = comparison(ticker)
    buckets = {name: (len(report[name]) if isinstance(report[name], list)
                      else report[name])
               for name in ("no_value", "unreadable", "in_an_unloaded_filing",
                            "against_a_segment", "in_a_same_day_period", "checked")}
    assert sum(buckets.values()) == report["us_gaap_facts"], (
        f"{ticker}: {report['us_gaap_facts']} us-gaap facts in the instances, "
        f"{sum(buckets.values())} accounted for — "
        + ", ".join(f"{name}={count}" for name, count in buckets.items()))


def test_the_comparison_reports_a_value_that_was_changed():
    """The positive control. Three assertions above say a set is empty; this is
    what makes that mean the comparison looked."""
    ticker = "AAPL"
    entry = next(row for row in manifest(ticker)["documents"]
                 if (row["form"], row["role"]) == ("10-K", "xbrl_instance"))
    grouped = looked_up(undimensioned_groups(
        [fact for fact in instance_facts(ticker, entry)
         if fact["number"] is not None]))
    index = record(ticker)["index"]
    matched, differences = compare(grouped, index, entry["accession"])
    assert not differences and matched == len(grouped)

    key = ("RevenueFromContractWithCustomerExcludingAssessedTax", "USD",
           "2024-09-29", "2025-09-27")
    assert key in grouped, "the tag this control changes is no longer in the instance"
    tag, unit, start, end = key
    doctored = dict(index)
    doctored[(tag, unit, entry["accession"], start, end)] = (1.0,)
    matched, differences = compare(grouped, doctored, entry["accession"])
    assert matched == len(grouped) - 1
    assert len(differences) == 1
    assert "companyfacts says 1.0" in differences[0]
    assert "416161000000" in differences[0]

    missing = {row: value for row, value in index.items()
               if row != (tag, unit, entry["accession"], start, end)}
    matched, differences = compare(grouped, missing, entry["accession"])
    assert len(differences) == 1 and "no companyfacts row" in differences[0]


# --- the classes of difference, from both sides ------------------------------

def test_the_filings_companyfacts_has_not_loaded_are_the_two_on_record():
    found = {(ticker, form, accession) for ticker in TICKERS
             for form, accession, _ in comparison(ticker)["unloaded"]}
    assert found == NOT_YET_IN_COMPANYFACTS
    assert sum(comparison(ticker)["instances"] for ticker in TICKERS) == 36


@pytest.mark.parametrize("ticker", TICKERS)
def test_a_fact_reported_only_against_a_segment_has_no_companyfacts_row(ticker):
    report = comparison(ticker)
    assert not report["dimensional_with_a_row"], (
        f"{ticker}: companyfacts holds a row for a key the instance reports only "
        f"against a segment:\n" + "\n".join(report["dimensional_with_a_row"]))


def test_the_segment_class_is_the_size_it_is():
    """A class nobody sizes is a class that can quietly grow to cover a miss."""
    total = sum(comparison(ticker)["dimensional_only"] for ticker in TICKERS)
    assert total == SEGMENT_ONLY_KEYS


@pytest.mark.parametrize("ticker", TICKERS)
def test_a_same_day_duration_has_no_companyfacts_row(ticker):
    report = comparison(ticker)
    assert not report["same_day_with_a_row"], (
        f"{ticker}: companyfacts holds a row for a duration of no length:\n"
        + "\n".join(report["same_day_with_a_row"]))


def test_the_same_day_class_is_the_size_it_is():
    total = sum(len(comparison(ticker)["same_day"]) for ticker in TICKERS)
    assert total == SAME_DAY_GROUPS
