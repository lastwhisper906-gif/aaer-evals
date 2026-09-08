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


def _instances(ticker: str, form: str) -> list:
    """Both instances a filing set holds for this form, oldest first."""
    rows = [row for role in extract_numbers.INSTANCE_ROLES
            for row in cutoff_guard.documents(ticker, form=form, role=role)]
    return sorted(rows, key=lambda row: (row["filing_date"], row["accession"]))


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form", FORMS)
def test_the_expected_count_is_what_the_instances_contain(ticker, form):
    """Both instances, counted from the files. The prior-period instance is the
    previous quarter's own XBRL, stored beside the current one and listed in the
    same fixture manifest; `note_history.py` and `diff_periods.py` have always
    read it and this module did not, so `input_trends.json` reported quarters as
    missing whose facts were in a document the manifest listed as an input."""
    counted = sum(_count_by_hand(row["full_path"]) for row in _instances(ticker, form))
    assert counted == expected(ticker)["numbers"][form]["fact_count"]


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form", FORMS)
def test_the_extractor_finds_every_fact_and_no_others(ticker, form):
    payload = extract_numbers.extract(ticker, (form,))
    assert len(payload["facts"]) == expected(ticker)["numbers"][form]["fact_count"]


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form", FORMS)
def test_every_instance_the_record_holds_for_that_form_is_read(ticker, form):
    payload = extract_numbers.extract(ticker, (form,))
    assert {(row["role"], row["accession"]) for row in payload["documents"]} == \
        {(row["role"], row["accession"]) for row in _instances(ticker, form)}


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
    """The 10-Q re-reports the 10-K's year-end balance sheet. Same fact in more
    than one filing: the latest one that carries it wins, and the earlier ones
    say so.

    Three filings reach this now, not two — the 10-K, the previous quarter's
    instance and the current one. The winner is therefore not "the newest of the
    three": a fact the 10-K and the previous quarter both carry and the current
    quarter does not is superseded by the previous quarter. Eleven of the twelve
    companies have such facts, so the property is stated per fact rather than
    per filing.
    """
    payload = extract_numbers.extract(ticker, FORMS)
    by_accession = {document["accession"]: document["filing_date"]
                    for document in payload["documents"]}
    assert len(by_accession) == 3, "the 10-K and two quarters"

    latest_carrying: dict[tuple, tuple[str, str]] = {}
    for fact in payload["facts"]:
        key = extract_numbers.identity(fact)
        here = (fact["filing_date"], fact["source_accession"])
        if latest_carrying.get(key) is None or here > latest_carrying[key]:
            latest_carrying[key] = here

    superseded = [fact for fact in payload["facts"] if "superseded_by" in fact]
    assert superseded, f"{ticker}: the filings share no fact — nothing was tested"
    for fact in superseded:
        winner = latest_carrying[extract_numbers.identity(fact)]
        assert fact["superseded_by"] == winner[1]
        assert fact["source_accession"] != winner[1]
        assert fact["filing_date"] <= winner[0]

    # And nothing surviving has a later counterpart: an unmarked fact is the
    # newest report of itself.
    for fact in payload["facts"]:
        if "superseded_by" in fact:
            continue
        assert latest_carrying[extract_numbers.identity(fact)][1] == \
            fact["source_accession"]


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
