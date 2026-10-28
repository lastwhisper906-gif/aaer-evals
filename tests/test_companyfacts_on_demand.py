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
    expected = sorted((ns, tag, unit, json.dumps(row, sort_keys=True))
                      for ns, concepts in committed_record()["facts"].items()
                      for tag, concept in concepts.items()
                      for unit, rows in concept["units"].items()
                      for row in source.inside(rows, cutoff))
    assert kept == expected
    assert max(json.loads(row[3])["filed"] for row in kept) <= cutoff


def test_the_first_value_is_the_earliest_filing_under_any_name(tmp_path, server):
    document = fetched(tmp_path, server, "2019-12-31")
    reading = company_facts.first_xbrl_value(document, CHAIN, QUARTER)
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
    alone = company_facts.first_xbrl_value(document, CHAIN[-1:], QUARTER)
    assert alone["accession"] == COMPARATIVE_OF_2019


def test_the_as_of_value_is_the_latest_filing_by_the_cutoff(tmp_path, server):
    document = fetched(tmp_path, server, "2019-12-31")
    reading = company_facts.as_of_cutoff_value(document, CHAIN, QUARTER)
    rows = independent("2019-12-31")
    latest = max(rows, key=lambda row: (row["filed"], row["accn"]))
    assert pick(reading) == LATEST_BY_2019 == {
        "accession": latest["accn"], "form": latest["form"], "filed": latest["filed"],
        "tag": latest["tag"], "value": latest["val"]}


def test_before_any_restatement_the_two_readings_agree(tmp_path, server):
    document = fetched(tmp_path, server, "2018-06-30")
    first = company_facts.first_xbrl_value(document, CHAIN, QUARTER)
    as_of = company_facts.as_of_cutoff_value(document, CHAIN, QUARTER)
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
    assert company_facts.first_xbrl_value(document, CHAIN, QUARTER)["value"] == 88293000000
    assert company_facts.as_of_cutoff_value(document, CHAIN, QUARTER)["value"] == 88300000000


def test_one_filing_stating_the_period_twice_is_a_conflict_not_a_pick(tmp_path, server):
    """Planted: the 10-Q of 2018-02-02 also states the quarter under `Revenues`, differently."""
    record = json.loads(json.dumps(committed_record()))
    record["facts"]["us-gaap"]["Revenues"]["units"]["USD"].append(
        {"start": "2017-10-01", "end": "2017-12-30", "val": 88000000000,
         "accn": FIRST["accession"], "fy": 2018, "fp": "Q1", "form": "10-Q",
         "filed": FIRST["filed"]})
    plant(server, record)
    reading = company_facts.first_xbrl_value(fetched(tmp_path, server, "2019-12-31"),
                                             CHAIN, QUARTER)
    assert reading["value"] is None
    assert reading["conflicting"] == [88000000000, 88293000000]
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
                                             CHAIN, QUARTER)
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
