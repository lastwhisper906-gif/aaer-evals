"""Every numeric fact, counted twice: once by the extractor, once from the file.

The second count is the point. `expected.json` is drafted from the extractor's
own first run, so a test that only compared the two would agree with itself.
`_count_by_hand` re-reads the instance with nothing but ElementTree and the
selection rule as the input spec words it, and that is what the expected value
is held to.
"""

from __future__ import annotations

import datetime as dt
import gzip
import json
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from src import cutoff_guard, extract_numbers
from src.fetch_fixtures import TICKERS

FIXTURES = Path(__file__).resolve().parent / "fixtures"
FORMS = ("10-K", "10-Q")


def expected(ticker: str) -> dict:
    return json.loads((FIXTURES / ticker / "expected.json").read_text())


def _raw(path: Path) -> bytes:
    """The document's bytes. Documents over 2 MB are stored gzipped; the gzip
    magic number says so without asking the manifest or importing src."""
    data = path.read_bytes()
    return gzip.decompress(data) if data[:2] == b"\x1f\x8b" else data


def _count_by_hand(path: Path) -> int:
    """The input spec's rule, applied to the raw file: a us-gaap or dei element
    carrying a unitRef. No import from src."""
    root = ET.fromstring(_raw(path))
    return sum(1 for element in root.iter()
               if element.get("unitRef")
               and ("/us-gaap/" in element.tag or "/dei/" in element.tag))


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form", FORMS)
def test_the_expected_count_is_what_the_instance_contains(ticker, form):
    row = cutoff_guard.one_document(ticker, form, "xbrl_instance")
    assert _count_by_hand(row["full_path"]) == expected(ticker)["numbers"][form]["fact_count"]


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form", FORMS)
def test_the_extractor_finds_every_fact_and_no_others(ticker, form):
    payload = extract_numbers.extract(ticker, (form,))
    assert len(payload["facts"]) == expected(ticker)["numbers"][form]["fact_count"]


@pytest.mark.parametrize("ticker", TICKERS)
def test_no_fact_comes_from_outside_the_two_namespaces(ticker):
    payload = extract_numbers.extract(ticker, FORMS)
    assert sorted({fact["prefix"] for fact in payload["facts"]}) == ["dei", "us-gaap"]


@pytest.mark.parametrize("ticker", TICKERS)
def test_every_fact_records_what_it_came_from(ticker):
    payload = extract_numbers.extract(ticker, FORMS)
    accessions = {document["accession"] for document in payload["documents"]}
    for fact in payload["facts"]:
        assert fact["source_accession"] in accessions
        assert fact["filing_date"] <= payload["cutoff"]
        assert fact["unit"]
        assert isinstance(fact["context"], dict)
        assert fact["nil"] or fact["value"] is not None


@pytest.mark.parametrize("ticker", TICKERS)
def test_fact_ids_are_unique(ticker):
    facts = extract_numbers.extract(ticker, FORMS)["facts"]
    ids = [fact["id"] for fact in facts]
    assert len(set(ids)) == len(ids)


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_later_filing_wins_and_the_earlier_one_says_so(ticker):
    """The 10-Q re-reports the 10-K's year-end balance sheet. Same fact, two
    filings: the 10-Q is later, so it wins and the 10-K fact carries
    superseded_by."""
    payload = extract_numbers.extract(ticker, FORMS)
    by_accession = {document["accession"]: document["filing_date"]
                    for document in payload["documents"]}
    assert len(by_accession) == 2, "this test needs the two filings to be distinct"
    later = max(by_accession, key=lambda accession: (by_accession[accession], accession))

    superseded = [fact for fact in payload["facts"] if "superseded_by" in fact]
    assert superseded, f"{ticker}: the two filings share no fact — nothing was tested"
    for fact in superseded:
        assert fact["superseded_by"] == later
        assert fact["source_accession"] != later

    surviving = {extract_numbers.identity(fact): fact
                 for fact in payload["facts"] if "superseded_by" not in fact}
    for fact in superseded:
        winner = surviving[extract_numbers.identity(fact)]
        assert winner["source_accession"] == later
        assert winner["filing_date"] >= fact["filing_date"]


def test_a_superseded_fact_is_kept_not_dropped():
    """The record has to show the replacement, not just the replacement's value."""
    payload = extract_numbers.extract("AAPL", FORMS)
    superseded = [fact for fact in payload["facts"] if "superseded_by" in fact]
    assert superseded
    for fact in superseded:
        assert fact["value"] is not None or fact["nil"]


def test_a_repeat_inside_one_filing_is_not_a_supersession():
    """A filing does not supersede itself: the count has to stay the count the
    instance supports, which is what the independent recount checks."""
    facts = extract_numbers.facts_from_instance(
        b"""<xbrl xmlns="http://www.xbrl.org/2003/instance"
                  xmlns:us-gaap="http://fasb.org/us-gaap/2025">
              <context id="c1"><period><instant>2025-01-01</instant></period></context>
              <unit id="usd"><measure>iso4217:USD</measure></unit>
              <us-gaap:Assets contextRef="c1" unitRef="usd" id="a">1</us-gaap:Assets>
              <us-gaap:Assets contextRef="c1" unitRef="usd" id="b">1</us-gaap:Assets>
            </xbrl>""",
        accession="0000000000-00-000000", filing_date="2025-01-02")
    merged = extract_numbers.apply_point_in_time(facts)
    assert len(merged) == 2
    assert not any("superseded_by" in fact for fact in merged)


def test_the_segment_is_part_of_a_fact_identity():
    """Two dimensions of one period are not the same fact."""
    facts = extract_numbers.facts_from_instance(
        b"""<xbrl xmlns="http://www.xbrl.org/2003/instance"
                  xmlns:xbrldi="http://xbrl.org/2006/xbrldi"
                  xmlns:us-gaap="http://fasb.org/us-gaap/2025">
              <context id="plain"><period><instant>2025-01-01</instant></period></context>
              <context id="dimensional"><entity><segment>
                <xbrldi:explicitMember dimension="us-gaap:StatementClassOfStockAxis"
                  >us-gaap:CommonStockMember</xbrldi:explicitMember>
              </segment></entity><period><instant>2025-01-01</instant></period></context>
              <unit id="usd"><measure>iso4217:USD</measure></unit>
              <us-gaap:Assets contextRef="plain" unitRef="usd" id="a">1</us-gaap:Assets>
              <us-gaap:Assets contextRef="dimensional" unitRef="usd" id="b">2</us-gaap:Assets>
            </xbrl>""",
        accession="0000000000-00-000000", filing_date="2025-01-02")
    assert extract_numbers.identity(facts[0]) != extract_numbers.identity(facts[1])
    assert facts[1]["context"]["segment"] == [
        {"dimension": "us-gaap:StatementClassOfStockAxis", "member": "us-gaap:CommonStockMember"}]


def test_a_nil_fact_is_recorded_as_nil_and_not_as_zero():
    facts = extract_numbers.facts_from_instance(
        b"""<xbrl xmlns="http://www.xbrl.org/2003/instance"
                  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                  xmlns:us-gaap="http://fasb.org/us-gaap/2025">
              <context id="c1"><period><instant>2025-01-01</instant></period></context>
              <unit id="usd"><measure>iso4217:USD</measure></unit>
              <us-gaap:CommitmentsAndContingencies contextRef="c1" unitRef="usd"
                 id="a" xsi:nil="true"/>
            </xbrl>""",
        accession="0000000000-00-000000", filing_date="2025-01-02")
    assert facts[0]["nil"] is True
    assert facts[0]["value"] is None and facts[0]["number"] is None


def test_the_extractor_goes_through_the_cutoff_gate():
    """A cutoff before the filing date refuses the run rather than filtering it."""
    with pytest.raises(cutoff_guard.CutoffViolationError):
        extract_numbers.extract("AAPL", ("10-K",), cutoff=dt.date(2020, 1, 1))
