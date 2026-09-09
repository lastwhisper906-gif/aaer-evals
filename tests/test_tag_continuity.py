"""Apple changed the name of its top line twice, and the series does not break.

The company is Apple and the filings are named here because the expected values
are read off them:

    10-Q  0000320193-18-000100  filed 2018-08-01
        us-gaap:SalesRevenueNet
    10-K  0000320193-18-000145  filed 2018-11-05
        us-gaap:Revenues
    10-Q  0000320193-19-000010  filed 2019-01-30
        us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax

Each of the three reports the top line under exactly one of those three names
and under neither of the other two; the first test below is the assertion that
says so. Nothing in this file takes a tag name from `src/tag_continuity.py`; the
names above are what EDGAR's companyfacts record says those three accessions
filed, read here by `revenue_rows`, which imports nothing from `src/` and does
not know the map exists.

**Why a map and not a resemblance.** `us-gaap:Revenues` and
`us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax`, read as titles
and scored by the ratio the fallback itself uses, come to 0.24 — nowhere near
the 0.70 that fallback needs, so no similarity rule would ever join them. They
are one series because two filings say so, and that is a thing to write down
rather than to compute, which is what the map is.

**The change is a hole, and it is measured.** As of 2019-01-30, the cutoff the
10-Q filed that day sets, following the newer name alone gives two quarters with
three missing between them, and following the older name alone stops one quarter
short of the newest. Both are asserted, so "unbroken" is a claim with something
standing against it.

**A quarter two filings disagree about keeps both numbers.** ESCO Technologies
reported the quarter ended 2018-12-31 as 182,597,000 and, a year later, as
163,365,000. The later filing wins and the earlier number is kept beside it,
because `docs/INPUT_SPEC.md` calls that difference a trace and not a tolerance.

**An absent quarter stays absent.** Carrier's 10-Q filed 2026-07-28 is in no
companyfacts row — EDGAR's own lag, recorded in
`tests/test_fetch_companyfacts.py::NOT_YET_IN_COMPANYFACTS` — so the quarter it
reports is not in this series. It comes back missing and never as a zero.
"""

from __future__ import annotations

import gzip
import json
from pathlib import Path

import pytest

from src import diff_periods, tag_continuity
from tests import expected_values

FIXTURES = Path(__file__).resolve().parent / "fixtures"

# --- what the filings say ----------------------------------------------------
#
# Read off Apple's companyfacts record, one accession at a time. The three names
# and the three accessions are the expected values of this file; everything
# below is held against them.

TICKER = "AAPL"
SERIES = "revenue"
UNIT = "USD"

SALES_REVENUE_NET = "us-gaap:SalesRevenueNet"
REVENUES = "us-gaap:Revenues"
REVENUE_FROM_CONTRACTS = "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"

QUARTERLY_10Q = "0000320193-18-000100"        # filed 2018-08-01
ANNUAL_10K = "0000320193-18-000145"           # filed 2018-11-05
NEXT_10Q = "0000320193-19-000010"             # filed 2019-01-30

REPORTED_UNDER = {
    QUARTERLY_10Q: SALES_REVENUE_NET,
    ANNUAL_10K: REVENUES,
    NEXT_10Q: REVENUE_FROM_CONTRACTS,
}
THE_THREE_NAMES = (SALES_REVENUE_NET, REVENUES, REVENUE_FROM_CONTRACTS)

# The cutoff the last of the three filings sets: the filing date of the report
# that triggers the run (`CLAUDE.md`). Nothing filed later may enter.
CUTOFF = "2019-01-30"

# Every quarter Apple's revenue series holds at that cutoff from the first one
# the 10-K restated onwards, as companyfacts records it: the period, the value,
# the name it was filed under and the accession that filed it. Where a quarter
# was filed more than once the latest filing at or before the cutoff is the one
# written here, which is the rule `docs/INPUT_SPEC.md` states for a period
# reported more than once.
NINE_QUARTERS = [
    ("2016-09-25", "2016-12-31", 78351000000, REVENUES, ANNUAL_10K),
    ("2017-01-01", "2017-04-01", 52896000000, REVENUES, ANNUAL_10K),
    ("2017-04-02", "2017-07-01", 45408000000, REVENUES, ANNUAL_10K),
    ("2017-07-02", "2017-09-30", 52579000000, REVENUES, ANNUAL_10K),
    ("2017-10-01", "2017-12-30", 88293000000, REVENUE_FROM_CONTRACTS, NEXT_10Q),
    ("2017-12-31", "2018-03-31", 61137000000, REVENUES, ANNUAL_10K),
    ("2018-04-01", "2018-06-30", 53265000000, REVENUES, ANNUAL_10K),
    ("2018-07-01", "2018-09-29", 62900000000, REVENUES, ANNUAL_10K),
    ("2018-09-30", "2018-12-29", 84310000000, REVENUE_FROM_CONTRACTS, NEXT_10Q),
]

# The one quarter missing from Apple's record between 2008 and the cutoff, and
# it is missing because no filing reports a period starting 2008-06-29 — the
# record's own hole, a decade before either name changed.
THE_ONE_HOLE_IN_THE_RECORD = {"after": "2008-06-28", "before": "2008-09-28",
                              "days_missing": 91}

# A quarter three of ESCO Technologies' filings report and two of them disagree
# about, as companyfacts records it under
# us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax:
#
#   0001104659-19-068679  filed 2019-11-29   182,597,000
#   0001104659-20-012461  filed 2020-02-07   163,365,000
#   0001104659-20-130486  filed 2020-11-30   163,365,000
#
# The latest filing wins and the number it replaced is kept beside it.
ESCO = "ESE"
RESTATED_QUARTER = ("2018-10-01", "2018-12-31")
RESTATED_AS = (163365000, "0001104659-20-130486")
FIRST_REPORTED_AS = (182597000, "0001104659-19-068679")

# Carrier's 10-Q filed 2026-07-28, and the newest quarter its companyfacts record
# does hold. The quarter that 10-Q reports is in no row of it.
CARRIER = "CARR"
CARRIER_10Q_NOT_LOADED = "0001783180-26-000032"
CARRIER_NEWEST_QUARTER = ("2026-01-01", "2026-03-31", 5341000000)


# --- a second reader, for the tests alone ------------------------------------

def companyfacts(ticker: str) -> dict:
    """One company's companyfacts document, opened without help from `src/`.

    `src/tag_continuity.py` reads this same file through the date gate and then
    filters it. Asserting its output against its own reading of the source would
    assert that it agrees with itself, so this reads the bytes and the JSON the
    plain way and nothing else.
    """
    return json.loads(gzip.decompress(
        (FIXTURES / ticker / "companyfacts.json.gz").read_bytes()))


def revenue_rows(ticker: str, accession: str | None = None) -> dict[str, list[dict]]:
    """Every USD duration row reported under any of the three names.

    Narrowed to one filing when an accession is given, which is how the name a
    filing used is read: the rows that name it, and no others.
    """
    facts = companyfacts(ticker)["facts"]
    found: dict[str, list[dict]] = {}
    for namespace, concepts in facts.items():
        for tag, concept in concepts.items():
            name = f"{namespace}:{tag}"
            if name not in THE_THREE_NAMES:
                continue
            rows = [row for row in concept["units"].get(UNIT, [])
                    if row.get("start")
                    and (accession is None or row["accn"] == accession)]
            if rows:
                found[name] = rows
    return found


def accessions_in(ticker: str) -> set[str]:
    """Every accession named anywhere in one companyfacts record."""
    return {row["accn"]
            for concepts in companyfacts(ticker)["facts"].values()
            for concept in concepts.values()
            for rows in concept["units"].values()
            for row in rows}


def as_tuples(points: list[dict]) -> list[tuple]:
    return [(point["start"], point["end"], point["value"],
             point["tag"], point["accession"]) for point in points]


# --- the two tag names, read off the two filings -----------------------------

@pytest.mark.parametrize("accession", sorted(REPORTED_UNDER))
def test_each_filing_reports_revenue_under_one_name_and_not_the_others(accession):
    reported = revenue_rows(TICKER, accession)
    assert sorted(reported) == [REPORTED_UNDER[accession]], (
        f"{accession} reports its top line under {sorted(reported)}; the record "
        f"read by hand says {REPORTED_UNDER[accession]} and nothing else")


def test_the_three_names_are_three_different_names():
    # Otherwise the test above passes on a company that changed nothing.
    assert len(set(REPORTED_UNDER.values())) == 3


# --- the map -----------------------------------------------------------------

def recorded_pairs() -> list[tuple]:
    return [(pair["earlier_tag"], pair["later_tag"],
             pair["earlier_filing"]["accession"], pair["later_filing"]["accession"])
            for pair in tag_continuity.pairs(TICKER, SERIES)]


def test_the_map_records_the_two_changes_the_three_filings_show():
    assert recorded_pairs() == [
        (SALES_REVENUE_NET, REVENUES, QUARTERLY_10Q, ANNUAL_10K),
        (REVENUES, REVENUE_FROM_CONTRACTS, ANNUAL_10K, NEXT_10Q),
    ]


def test_the_period_each_pair_cites_is_in_both_filings_under_both_names():
    """The evidence each entry carries, checked against the source it names."""
    for pair in tag_continuity.pairs():
        overlap = pair["both_report"]
        for tag, filing in ((pair["earlier_tag"], pair["earlier_filing"]),
                            (pair["later_tag"], pair["later_filing"])):
            rows = revenue_rows(pair["ticker"], filing["accession"]).get(tag, [])
            matching = [row for row in rows
                        if row["start"] == overlap["start"]
                        and row["end"] == overlap["end"]]
            assert [row["val"] for row in matching] == [overlap["value"]], (
                f"{filing['accession']} does not report {tag} for "
                f"{overlap['start']}..{overlap['end']} as {overlap['value']}")


def test_every_pair_says_where_it_was_read():
    """The same provenance check every expected value in this project passes."""
    for pair in tag_continuity.pairs():
        assert expected_values.unsourced(pair["read_from"]) == "", pair["earlier_tag"]


def test_the_map_is_named_for_the_rules_version_it_declares():
    # docs/rules.md: the map moves with the rules and is named by the version.
    assert tag_continuity.MAP_PATH.name == \
        f"tag_continuity_map_{tag_continuity.load()['rules_version']}.json"


def test_a_pair_that_does_not_name_both_filings_is_refused(tmp_path):
    """The whole file is refused, not the one entry: a map that drops an entry
    stitches a series together in one run and not the next."""
    document = json.loads(tag_continuity.MAP_PATH.read_text(encoding="utf-8"))
    document["pairs"][0].pop("earlier_filing")
    written = tmp_path / "tag_continuity_map_v0.1.json"
    written.write_text(json.dumps(document), encoding="utf-8")
    with pytest.raises(tag_continuity.TagContinuityError):
        tag_continuity.load(written)


def test_a_name_recorded_in_two_series_is_refused(tmp_path):
    """`series_of` would answer with whichever pair came first, which is a wrong
    answer given quietly."""
    document = json.loads(tag_continuity.MAP_PATH.read_text(encoding="utf-8"))
    document["pairs"].append(dict(document["pairs"][0], series="cost_of_revenue"))
    written = tmp_path / "tag_continuity_map_v0.1.json"
    written.write_text(json.dumps(document), encoding="utf-8")
    with pytest.raises(tag_continuity.TagContinuityError, match="one name is one series"):
        tag_continuity.load(written)


def test_the_committed_map_loads(tmp_path):
    """The control on the test above: the refusal is about the missing field."""
    document = json.loads(tag_continuity.MAP_PATH.read_text(encoding="utf-8"))
    written = tmp_path / "tag_continuity_map_v0.1.json"
    written.write_text(json.dumps(document), encoding="utf-8")
    assert tag_continuity.load(written)["pairs"] == document["pairs"]


# --- the series --------------------------------------------------------------

def revenue_series(cutoff: str = CUTOFF) -> list[dict]:
    return tag_continuity.series_quarters(TICKER, SERIES, cutoff)


def from_the_restated_quarters(points: list[dict]) -> list[dict]:
    """The window the nine quarters cover: everything ending in 2016Q4 or after."""
    return [point for point in points if point["end"] >= NINE_QUARTERS[0][1]]


def test_the_series_is_unbroken_across_the_change():
    window = from_the_restated_quarters(revenue_series())
    assert as_tuples(window) == NINE_QUARTERS
    assert tag_continuity.breaks(window) == []


def test_the_window_holds_a_change():
    # Zero breaks is only worth asserting if the window crosses a change.
    names = {point["tag"] for point in from_the_restated_quarters(revenue_series())}
    assert names == {REVENUES, REVENUE_FROM_CONTRACTS}


def test_the_joined_series_reaches_back_under_the_oldest_name():
    """Both pairs carry: the series starts under the name Apple used in 2009 and
    runs to the newest quarter with one hole in it, and that hole is in the
    record rather than at either change."""
    points = revenue_series()
    assert points[0]["tag"] == SALES_REVENUE_NET
    assert points[-1]["end"] == NINE_QUARTERS[-1][1]
    assert tag_continuity.breaks(points) == [THE_ONE_HOLE_IN_THE_RECORD]


def test_the_record_has_no_period_starting_where_that_hole_is():
    """The hole above is companyfacts', not this module's: no filing reports any
    period beginning the day after the quarter before it ended."""
    starts = {row["start"] for rows in revenue_rows(TICKER).values() for row in rows}
    assert THE_ONE_HOLE_IN_THE_RECORD["before"] in starts
    assert "2008-06-29" not in starts


def test_the_newer_name_alone_leaves_three_quarters_missing():
    alone = tag_continuity.quarters(tag_continuity.history(TICKER, CUTOFF),
                                    (REVENUE_FROM_CONTRACTS,), UNIT)
    assert as_tuples(alone) == [NINE_QUARTERS[4], NINE_QUARTERS[8]]
    assert tag_continuity.breaks(alone) == [
        {"after": "2017-12-30", "before": "2018-09-30", "days_missing": 273}]


def test_the_older_name_alone_stops_one_quarter_short():
    alone = tag_continuity.quarters(tag_continuity.history(TICKER, CUTOFF),
                                    (REVENUES,), UNIT)
    assert alone[-1]["end"] == "2018-09-29"
    assert NINE_QUARTERS[8][1] not in {point["end"] for point in alone}


def test_the_oldest_name_alone_stops_two_quarters_short():
    alone = tag_continuity.quarters(tag_continuity.history(TICKER, CUTOFF),
                                    (SALES_REVENUE_NET,), UNIT)
    assert alone[-1]["end"] == "2018-06-30"


def test_the_cutoff_is_applied_to_the_rows():
    """Nothing filed after the cutoff is in the series, whatever the record holds."""
    filed = {point["filed"] for point in revenue_series()}
    assert max(filed) <= CUTOFF
    assert max({point["filed"] for point in revenue_series(cutoff=None)}) > CUTOFF


# --- a quarter two filings disagree about ------------------------------------

def test_three_filings_report_that_quarter_and_two_of_them_disagree():
    rows = [row for row in revenue_rows(ESCO)[REVENUE_FROM_CONTRACTS]
            if (row["start"], row["end"]) == RESTATED_QUARTER]
    assert sorted((row["filed"], row["val"]) for row in rows) == [
        ("2019-11-29", FIRST_REPORTED_AS[0]),
        ("2020-02-07", RESTATED_AS[0]),
        ("2020-11-30", RESTATED_AS[0])]


def test_the_latest_filing_wins_and_the_number_it_replaced_is_kept():
    """Nothing is averaged, tolerated or dropped: `docs/INPUT_SPEC.md` calls a
    later value that differs from the first-reported one a trace to keep."""
    points = tag_continuity.quarters(tag_continuity.history(ESCO),
                                     (REVENUE_FROM_CONTRACTS,), UNIT)
    point = next(one for one in points
                 if (one["start"], one["end"]) == RESTATED_QUARTER)
    assert (point["value"], point["accession"]) == RESTATED_AS
    assert [(row["value"], row["accession"]) for row in point["superseded"]] \
        == [FIRST_REPORTED_AS]


# --- a quarter no companyfacts row covers ------------------------------------

def test_carriers_unloaded_quarterly_is_in_no_companyfacts_row():
    assert CARRIER_10Q_NOT_LOADED not in accessions_in(CARRIER)


def test_a_quarter_no_row_covers_is_absent_and_never_a_zero():
    points = tag_continuity.quarters(tag_continuity.history(CARRIER),
                                     (REVENUE_FROM_CONTRACTS,), UNIT)
    start, end, value = CARRIER_NEWEST_QUARTER
    newest = points[-1]
    assert (newest["start"], newest["end"], newest["value"]) == (start, end, value)
    assert not [point for point in points if point["end"] > end]
    assert not [point for point in points if point["value"] == 0]


# --- matching one period's tags against the period before --------------------
#
# The fixtures below are built here rather than read off a filing, and the
# reason is stated so it is not mistaken for a shortcut: no company-extension
# tag in the twelve committed 10-Q pairs is a rename. Every extension tag that
# is in one of a company's two committed quarterlies and not the other is a
# disclosure that appeared or went away — none of them reports a period and a
# value that a differently-named tag in the other filing also reports, which is
# the only thing that would let a rename be read off the pair. The rule still
# has to exist, because `docs/INPUT_SPEC.md` asks for it, so it is exercised on
# tags written the way a filer writes them.

FILER = "gnrc"    # a company's own prefix; what the rule reads is that it is one
INVENTORY = "us-gaap:InventoryNet"


def tag(name: str, title: str | None = None) -> dict:
    return {"name": name} if title is None else {"name": name, "title": title}


def rule_for(matched: list[dict], name: str) -> str:
    return next(entry["matched_by"] for entry in matched
                if entry["current"] and entry["current"]["name"] == name)


def test_a_name_both_periods_use_pairs_by_name():
    matched = tag_continuity.match_tags([tag(INVENTORY)], [tag(INVENTORY)], TICKER)
    assert rule_for(matched, INVENTORY) == "tag_name"
    assert matched[0]["score"] == 1.0


def test_the_swapped_standard_name_pairs_through_the_map():
    matched = tag_continuity.match_tags([tag(REVENUE_FROM_CONTRACTS)],
                                        [tag(REVENUES)], TICKER)
    assert rule_for(matched, REVENUE_FROM_CONTRACTS) == "recorded_pair"
    assert matched[0]["prior"]["name"] == REVENUES


def test_no_resemblance_could_have_found_that_pair():
    """The number the docstring at the top of this file quotes, measured here so
    it is not a claim nobody checks: 0.24 against a floor of 0.70."""
    score = diff_periods.similarity(tag_continuity.title_of(tag(REVENUES)),
                                    tag_continuity.title_of(tag(REVENUE_FROM_CONTRACTS)))
    assert round(score, 2) == 0.24
    assert score < tag_continuity.TITLE_SIMILARITY_FLOOR


def test_two_standard_names_with_no_recorded_pair_stay_unmatched():
    goods, services = "us-gaap:SalesRevenueGoodsNet", "us-gaap:SalesRevenueServicesNet"
    matched = tag_continuity.match_tags([tag(services)], [tag(goods)], TICKER)
    assert rule_for(matched, services) == tag_continuity.NO_PRIOR_TAG


def test_the_same_two_titles_do_pair_when_one_is_the_companys_own_tag():
    """The control: the titles are similar enough, so the refusal above is the
    rule about standard tags and not a floor nobody reaches."""
    goods, services = f"{FILER}:SalesRevenueGoodsNet", "us-gaap:SalesRevenueServicesNet"
    assert diff_periods.similarity(
        tag_continuity.title_of(tag(goods)),
        tag_continuity.title_of(tag(services))) >= tag_continuity.TITLE_SIMILARITY_FLOOR
    matched = tag_continuity.match_tags([tag(services)], [tag(goods)], TICKER)
    assert rule_for(matched, services) == "title_similarity"


def test_a_renamed_extension_tag_pairs_on_its_title():
    was = f"{FILER}:RestructuringAndBusinessOptimizationExpense"
    now = f"{FILER}:BusinessOptimizationExpense"
    matched = tag_continuity.match_tags([tag(now)], [tag(was)], TICKER)
    assert rule_for(matched, now) == "title_similarity"
    assert matched[0]["prior"]["name"] == was
    assert matched[0]["score"] >= tag_continuity.TITLE_SIMILARITY_FLOOR


def test_every_name_pair_is_made_before_the_first_map_pair():
    """A filing that still reports the older name keeps it, and the newer name
    then has nothing to pair with — the map must not reach past a name match."""
    current = [tag(REVENUE_FROM_CONTRACTS), tag(REVENUES)]
    prior = [tag(REVENUES)]
    matched = tag_continuity.match_tags(current, prior, TICKER)
    assert rule_for(matched, REVENUES) == "tag_name"
    assert rule_for(matched, REVENUE_FROM_CONTRACTS) == tag_continuity.NO_PRIOR_TAG


def test_a_tag_the_new_period_dropped_is_reported_as_gone():
    matched = tag_continuity.match_tags([], [tag(INVENTORY)], TICKER)
    assert [entry["matched_by"] for entry in matched] == [tag_continuity.NO_CURRENT_TAG]
    assert matched[0]["prior"]["name"] == INVENTORY


def test_a_supplied_title_is_used_before_the_tags_own_name():
    assert tag_continuity.title_of(tag(INVENTORY, "Note 5 — Inventories")) \
        == "note 5 — inventories"
    assert tag_continuity.title_of(tag(INVENTORY)) == "inventory net"


def test_a_company_extension_tag_is_told_apart_from_a_standard_one():
    assert tag_continuity.is_extension(f"{FILER}:BusinessOptimizationExpense")
    assert not tag_continuity.is_extension(REVENUES)
    assert not tag_continuity.is_extension("dei:EntityCommonStockSharesOutstanding")
