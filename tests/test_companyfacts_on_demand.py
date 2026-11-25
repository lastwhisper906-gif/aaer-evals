"""companyfacts on demand: the record fetched, cut at the cutoff row by row, and
read three ways — first reported, as of the cutoff, and the derived fourth
quarter.

The record served here is Apple's, committed as
`tests/fixtures/AAPL/companyfacts.json.gz` and served gzipped by a planted local
server, the way data.sec.gov serves it. Every expected value is found by
`tests/companyfacts_source.py`, which opens the committed file with `gzip` and
`json` and imports nothing from `src/`, and the ones that name a filing were
also read by eye off the record's rows, quoted beside them. The tag chain is the
one `src/tag_continuity_map_v0.1.json` records for Apple's top line: the 10-Q
filed 2018-08-01 is the last under `SalesRevenueNet`, the 10-K filed 2018-11-05
the only one under `Revenues`, and the 10-Q filed 2019-01-30 the first under
`RevenueFromContractWithCustomerExcludingAssessedTax`.
"""

from __future__ import annotations

import gzip
import hashlib
import json
from pathlib import Path

import pytest

from src import company_facts, cutoff_guard, fourth_quarter
from src.edgar_client import EdgarClient
from tests import companyfacts_source as source
from tests.planted_edgar import DIRECT, SAMPLE_CONTACT, serve

FIXTURES = Path(__file__).resolve().parent / "fixtures"
CIK = "0000320193"
PATH = f"/api/xbrl/companyfacts/CIK{CIK}.json"
CHAIN = ("us-gaap:SalesRevenueNet", "us-gaap:Revenues",
         "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax")
QUARTER = "2017-10-01..2017-12-30"

# The record's four rows for the quarter, read by eye:
#   SalesRevenueNet  88293000000  0000320193-18-000007  10-Q  filed 2018-02-02
#   Revenues         88293000000  0000320193-18-000145  10-K  filed 2018-11-05
#   RevenueFromContractWithCustomerExcludingAssessedTax
#                    88293000000  0000320193-19-000010  10-Q  filed 2019-01-30
#                    88293000000  0000320193-19-000119  10-K  filed 2019-10-31
FIRST = {"accession": "0000320193-18-000007", "form": "10-Q", "filed": "2018-02-02",
         "tag": "us-gaap:SalesRevenueNet", "value": 88293000000}
COMPARATIVE_OF_2019 = "0000320193-19-000010"
LATEST_BY_2019 = {"accession": "0000320193-19-000119", "form": "10-K", "filed": "2019-10-31",
                  "tag": "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax",
                  "value": 88293000000}


def committed_record() -> dict:
    return source.record("AAPL")


@pytest.fixture
def server():
    for planted in serve(default=None):
        planted.bodies[PATH] = (gzip.compress(json.dumps(committed_record()).encode()), "gzip")
        yield planted


def plant(server, record: dict) -> None:
    server.bodies[PATH] = (gzip.compress(json.dumps(record).encode()), "gzip")


def fetched(tmp_path, server, cutoff):
    client = EdgarClient(environ={"EDGAR_USER_AGENT": SAMPLE_CONTACT,
                                  "AAER_CACHE": str(tmp_path)},
                         opener=DIRECT, sleep=lambda seconds: None)
    return company_facts.fetch(client, CIK, cutoff=cutoff,
                               base=server.url + "/api/xbrl/companyfacts/")


def independent(cutoff: str) -> list[dict]:
    """The independent reader's rows for the quarter under every name in the chain."""
    rows = []
    for tag in CHAIN:
        name = tag.split(":")[1]
        rows += [dict(row, tag=tag) for row in
                 source.for_period(source.inside(source.rows("AAPL", name), cutoff), QUARTER)]
    return rows


def pick(reading: dict) -> dict:
    return {key: reading[key] for key in ("accession", "form", "filed", "tag", "value")}


def test_the_chain_is_the_one_the_map_records():
    assert company_facts.chain("AAPL", "revenue") == CHAIN


def test_the_url_is_edgars():
    assert company_facts.facts_url(CIK) == \
        "https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json"
    assert company_facts.facts_url(320193) == company_facts.facts_url(CIK)


def test_one_request_with_the_declared_contact(tmp_path, server):
    fetched(tmp_path, server, "2019-12-31")
    assert [path for path, _ in server.seen] == [PATH]
    assert server.seen[0][1]["User-Agent"] == SAMPLE_CONTACT


@pytest.mark.parametrize("cutoff", ["2017-11-03", "2018-06-30", "2019-12-31"])
def test_the_cut_keeps_exactly_the_rows_filed_by_the_cutoff(tmp_path, server, cutoff):
    document = fetched(tmp_path, server, cutoff)
    kept = sorted((ns, tag, unit, json.dumps(row, sort_keys=True))
                  for ns, concepts in document["facts"].items()
                  for tag, concept in concepts.items()
                  for unit, rows in concept["units"].items() for row in rows)
    # every row filed by the cutoff, as filed, less EDGAR's cross-filing `frame`
    expected = sorted((ns, tag, unit, json.dumps({k: v for k, v in row.items() if k != "frame"},
                                                 sort_keys=True))
                      for ns, concepts in committed_record()["facts"].items()
                      for tag, concept in concepts.items()
                      for unit, rows in concept["units"].items()
                      for row in source.inside(rows, cutoff))
    assert kept == expected
    assert max(json.loads(row[3])["filed"] for row in kept) <= cutoff


def test_the_first_value_is_the_earliest_filing_under_any_name(tmp_path, server):
    document = fetched(tmp_path, server, "2019-12-31")
    reading = company_facts.first_xbrl_value(document, CHAIN, QUARTER, cutoff="2019-12-31")
    rows = independent("2019-12-31")
    earliest = min(rows, key=lambda row: (row["filed"], row["accn"]))
    assert pick(reading) == FIRST == {"accession": earliest["accn"], "form": earliest["form"],
                                      "filed": earliest["filed"], "tag": earliest["tag"],
                                      "value": earliest["val"]}
    assert reading["accession"] != COMPARATIVE_OF_2019
    assert reading["conflicting"] == []


def test_the_first_value_is_not_found_under_one_name_alone(tmp_path, server):
    """Read under the name of 2019 alone, the quarter dates to 2019's comparative."""
    document = fetched(tmp_path, server, "2019-12-31")
    alone = company_facts.first_xbrl_value(document, CHAIN[-1:], QUARTER, cutoff="2019-12-31")
    assert alone["accession"] == COMPARATIVE_OF_2019


def test_the_as_of_value_is_the_latest_filing_by_the_cutoff(tmp_path, server):
    document = fetched(tmp_path, server, "2019-12-31")
    reading = company_facts.as_of_cutoff_value(document, CHAIN, QUARTER, cutoff="2019-12-31")
    rows = independent("2019-12-31")
    latest = max(rows, key=lambda row: (row["filed"], row["accn"]))
    assert pick(reading) == LATEST_BY_2019 == {
        "accession": latest["accn"], "form": latest["form"], "filed": latest["filed"],
        "tag": latest["tag"], "value": latest["val"]}


def test_before_any_restatement_the_two_readings_agree(tmp_path, server):
    document = fetched(tmp_path, server, "2018-06-30")
    first = company_facts.first_xbrl_value(document, CHAIN, QUARTER, cutoff="2018-06-30")
    as_of = company_facts.as_of_cutoff_value(document, CHAIN, QUARTER, cutoff="2018-06-30")
    assert pick(first) == pick(as_of) == FIRST
    assert len(independent("2018-06-30")) == 1


def test_a_revised_value_is_first_in_one_reading_and_latest_in_the_other(tmp_path, server):
    """Planted: the 10-K of 2019 states the quarter 7,000,000 higher."""
    record = committed_record()
    revised = json.loads(json.dumps(record))
    rows = revised["facts"]["us-gaap"]["RevenueFromContractWithCustomerExcludingAssessedTax"][
        "units"]["USD"]
    [row] = [r for r in rows if r["accn"] == LATEST_BY_2019["accession"]
             and r.get("start") == "2017-10-01" and r["end"] == "2017-12-30"]
    row["val"] = 88300000000
    plant(server, revised)
    document = fetched(tmp_path, server, "2019-12-31")
    assert company_facts.first_xbrl_value(document, CHAIN, QUARTER,
                                         cutoff="2019-12-31")["value"] == 88293000000
    assert company_facts.as_of_cutoff_value(document, CHAIN, QUARTER,
                                           cutoff="2019-12-31")["value"] == 88300000000


def test_one_filing_stating_the_period_twice_is_a_conflict_not_a_pick(tmp_path, server):
    """Planted: the 10-Q of 2018-02-02 also states the quarter under `Revenues`, differently."""
    record = json.loads(json.dumps(committed_record()))
    record["facts"]["us-gaap"]["Revenues"]["units"]["USD"].append(
        {"start": "2017-10-01", "end": "2017-12-30", "val": 88000000000,
         "accn": FIRST["accession"], "fy": 2018, "fp": "Q1", "form": "10-Q",
         "filed": FIRST["filed"]})
    plant(server, record)
    reading = company_facts.first_xbrl_value(fetched(tmp_path, server, "2019-12-31"),
                                             CHAIN, QUARTER, cutoff="2019-12-31")
    assert reading["value"] is None
    assert reading["conflicting"] == [
        {"accession": FIRST["accession"], "form": "10-Q", "tag": "us-gaap:Revenues",
         "value": 88000000000},
        {"accession": FIRST["accession"], "form": "10-Q", "tag": "us-gaap:SalesRevenueNet",
         "value": 88293000000}]
    assert reading["accession"] == FIRST["accession"]


def test_a_row_from_an_earnings_release_is_not_a_statement_value(tmp_path, server):
    """Planted: an 8-K row for the quarter, filed before the 10-Q."""
    record = json.loads(json.dumps(committed_record()))
    record["facts"]["us-gaap"]["SalesRevenueNet"]["units"]["USD"].append(
        {"start": "2017-10-01", "end": "2017-12-30", "val": 88000000000,
         "accn": "0000320193-18-000002", "fy": 2018, "fp": "Q1", "form": "8-K",
         "filed": "2018-02-01"})
    plant(server, record)
    reading = company_facts.first_xbrl_value(fetched(tmp_path, server, "2019-12-31"),
                                             CHAIN, QUARTER, cutoff="2019-12-31")
    assert pick(reading) == FIRST


def test_a_row_with_no_filing_date_is_refused(tmp_path, server):
    record = json.loads(json.dumps(committed_record()))
    del record["facts"]["us-gaap"]["SalesRevenueNet"]["units"]["USD"][0]["filed"]
    plant(server, record)
    with pytest.raises(cutoff_guard.CutoffGuardError):
        fetched(tmp_path, server, "2019-12-31")


@pytest.mark.parametrize("cutoff", ["", "garbage", "2019-13-01"])
def test_a_cutoff_that_is_not_a_date_is_refused_before_any_request(tmp_path, server, cutoff):
    with pytest.raises(cutoff_guard.CutoffGuardError):
        fetched(tmp_path, server, cutoff)
    assert server.seen == []


def test_the_fourth_quarter_is_the_year_less_the_nine_months(tmp_path, server):
    """Fiscal 2017, at the cutoff of the 10-K that closed it (filed 2017-11-03).

    By hand, from the record's rows read by eye: the year 2016-09-25..2017-09-30
    is 229,234,000,000 (`SalesRevenueNet`, the 10-K 0000320193-17-000070), the
    nine months 2016-09-25..2017-07-01 are 176,655,000,000 (the 10-Q
    0000320193-17-000009), so the fourth quarter 2017-07-02..2017-09-30 is
    229,234,000,000 - 176,655,000,000 = 52,579,000,000.
    """
    cutoff = "2017-11-03"
    year = source.one_value("AAPL", "SalesRevenueNet", "2016-09-25..2017-09-30", cutoff)
    nine = source.one_value("AAPL", "SalesRevenueNet", "2016-09-25..2017-07-01", cutoff)
    assert (year, nine, year - nine) == (229234000000, 176655000000, 52579000000)

    document = fetched(tmp_path, server, cutoff)
    payload = company_facts.fourth_quarters("AAPL", document, cutoff, url=server.url + PATH)
    [fiscal_2017] = [y for y in payload["fiscal_years"]
                     if y["fiscal_year"]["end"] == "2017-09-30"]
    revenue = fiscal_2017["measures"]["revenue"]
    assert (revenue["annual"], revenue["nine_months"], revenue["fourth_quarter"]) == \
        (year, nine, year - nine)
    assert revenue["fourth_quarter_period"] == {"start": "2017-07-02", "end": "2017-09-30",
                                                "days": 91}
    assert payload["source"]["path"] is None
    assert payload["source"]["url"] == server.url + PATH


def test_on_demand_and_committed_routes_derive_the_same_quarters(tmp_path, server):
    cutoff = "2019-12-31"
    on_demand = company_facts.fourth_quarters("AAPL", fetched(tmp_path, server, cutoff), cutoff)
    committed = fourth_quarter.fourth_quarters("AAPL", cutoff)
    assert on_demand["fiscal_years"] == committed["fiscal_years"]
    assert on_demand["source"]["duration_facts"] == committed["source"]["duration_facts"]


def test_a_record_with_rows_after_the_cutoff_is_refused_by_the_fourth_quarter():
    """The cut is not trusted: an uncut record handed straight in is refused."""
    with pytest.raises(fourth_quarter.FourthQuarterError, match="filed after the cutoff"):
        company_facts.fourth_quarters("AAPL", committed_record(), "2017-11-03")


def test_a_record_that_was_not_cut_is_refused_by_the_readings():
    """The readings take the cutoff and do not trust the cut: the committed record
    handed straight in holds the rows of 2018 and 2019 for the quarter."""
    for reading in (company_facts.first_xbrl_value, company_facts.as_of_cutoff_value):
        with pytest.raises(cutoff_guard.CutoffGuardError, match="filed after the cutoff"):
            reading(committed_record(), CHAIN, QUARTER, cutoff="2018-06-30")


def test_filings_of_one_day_that_disagree_are_a_conflict_not_a_pick(tmp_path, server):
    """Super Micro's allowance for doubtful accounts at 2016-06-30, read by eye off
    its committed record: four filings dated 2019-05-17 state it, the 10-Q/A
    0001375365-19-000033 at 2,000 and the 10-Q/As -000035 and -000037 and the
    10-K -000039 at 2,413,000. No earlier filing states it, so the first day's
    four filings disagree, and their accession numbers are not the order they
    were made in."""
    plant(server, source.record("SMCI"))
    document = fetched(tmp_path, server, "2019-05-17")
    tag = ("us-gaap:AllowanceForDoubtfulAccountsReceivable",)
    reading = company_facts.first_xbrl_value(document, tag, "2016-06-30", cutoff="2019-05-17")
    rows = source.for_period(source.inside(source.rows(
        "SMCI", "AllowanceForDoubtfulAccountsReceivable", every_form=True), "2019-05-17"),
        "2016-06-30")
    assert reading["value"] is None and reading["accession"] is None
    assert reading["filed"] == "2019-05-17"
    assert [(c["accession"], c["value"]) for c in reading["conflicting"]] == \
        sorted((row["accn"], row["val"]) for row in rows) == [
            ("0001375365-19-000033", 2000), ("0001375365-19-000035", 2413000),
            ("0001375365-19-000037", 2413000), ("0001375365-19-000039", 2413000)]


def test_acceptance_stamps_order_one_days_filings(tmp_path, server):
    """American Superconductor's cash at 2008-03-31, read by eye: the 10-Q/A
    0000950123-11-086248 states 70,674,000 and the 10-K 0000950123-11-086249
    states 67,834,000, both dated 2011-09-23. Without their acceptance order
    both readings are the conflict; with stamps the test plants (the 10-Q/A
    accepted first), the first reading is the 10-Q/A's and the latest the 10-K's."""
    plant(server, source.record("AMSC"))
    document = fetched(tmp_path, server, "2011-12-31")
    tag = ("us-gaap:CashAndCashEquivalentsAtCarryingValue",)
    unordered = company_facts.first_xbrl_value(document, tag, "2008-03-31", cutoff="2011-12-31")
    assert unordered["value"] is None
    assert [(c["accession"], c["value"]) for c in unordered["conflicting"]] == [
        ("0000950123-11-086248", 70674000), ("0000950123-11-086249", 67834000)]
    stamps = {"0000950123-11-086248": "2011-09-23T16:01:00-04:00",
              "0000950123-11-086249": "2011-09-23T16:05:00-04:00"}
    first = company_facts.first_xbrl_value(document, tag, "2008-03-31", cutoff="2011-12-31",
                                           accepted=stamps)
    latest = company_facts.as_of_cutoff_value(document, tag, "2008-03-31",
                                              cutoff="2011-12-31", accepted=stamps)
    assert (first["accession"], first["value"]) == ("0000950123-11-086248", 70674000)
    assert (latest["accession"], latest["value"]) == ("0000950123-11-086249", 67834000)


def test_an_instant_is_read_by_its_date_alone(tmp_path, server):
    """Apple's cash at 2017-09-30, read by eye: 20,289,000,000 in the 10-K
    0000320193-17-000070 filed 2017-11-03, then in every quarterly through the
    10-Q 0000320193-19-000010 filed 2019-01-30."""
    document = fetched(tmp_path, server, "2019-12-31")
    tag = ("us-gaap:CashAndCashEquivalentsAtCarryingValue",)
    first = company_facts.first_xbrl_value(document, tag, "2017-09-30", cutoff="2019-12-31")
    latest = company_facts.as_of_cutoff_value(document, tag, "2017-09-30", cutoff="2019-12-31")
    assert (first["accession"], first["filed"], first["value"]) == \
        ("0000320193-17-000070", "2017-11-03", 20289000000)
    assert (latest["accession"], latest["filed"], latest["value"]) == \
        ("0000320193-19-000010", "2019-01-30", 20289000000)


def test_the_cut_record_carries_no_frame_and_names_what_it_was_cut_from(tmp_path, server):
    """A frame is EDGAR's label across all filings: in the committed record
    Apple's quarter ending 2017-12-30 is framed `CY2017Q4` on the row filed
    2019-10-31, which a cut at 2019-06-30 leaves out."""
    document = fetched(tmp_path, server, "2019-06-30")
    assert not any("frame" in row for concepts in document["facts"].values()
                   for concept in concepts.values()
                   for rows in concept["units"].values() for row in rows)
    served = gzip.decompress(server.bodies[PATH][0])
    assert document["read_from"] == {
        "url": server.url + PATH, "sha256": hashlib.sha256(served).hexdigest(),
        "bytes": len(served), "cutoff": "2019-06-30"}
