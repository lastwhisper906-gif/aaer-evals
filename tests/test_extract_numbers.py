"""Every numeric fact, counted twice: once by the extractor, once from the file.

The second count is the point. A count drafted from the extractor's own first
run and then compared to that extractor would agree with itself. `_count_by_hand`
re-reads the instance with nothing but ElementTree and the selection rule as the
input spec words it, and that is what the expected value is held to — which is
what `expected_values.json` records as its source.
"""

from __future__ import annotations

import datetime as dt
import gzip
import json
import xml.etree.ElementTree as ET
from decimal import Decimal
from pathlib import Path

import pytest

from src import cutoff_guard, extract_numbers
from src.fetch_fixtures import TICKERS
from tests.expected_values import value

FIXTURES = Path(__file__).resolve().parent / "fixtures"
FORMS = ("10-K", "10-Q")


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
    assert counted == value(ticker, f"numbers.{form}.fact_count")


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form", FORMS)
def test_the_extractor_finds_every_fact_and_no_others(ticker, form):
    payload = extract_numbers.extract(ticker, (form,))
    assert len(payload["facts"]) == value(ticker, f"numbers.{form}.fact_count")


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


def _typed_by_hand(path: Path) -> int:
    """Every `xbrldi:typedMember` in the instance, counted from the file."""
    root = ET.fromstring(_raw(path))
    return sum(1 for element in root.iter()
               if element.tag == "{http://xbrl.org/2006/xbrldi}typedMember")


@pytest.mark.parametrize("ticker", TICKERS)
def test_a_typed_member_is_part_of_the_context(ticker):
    """A typed member is the other half of a dimension: instead of naming a
    member of a domain it carries a value in a child element. Reading only
    `explicitMember` left those contexts looking empty."""
    payload = extract_numbers.extract(ticker, FORMS)
    carried = [fact for fact in payload["facts"] if fact["context"].get("typed_segment")]
    if not carried:
        pytest.skip(f"{ticker}'s instances use no typed member")
    for fact in carried:
        for member in fact["context"]["typed_segment"]:
            assert member["dimension"] and member["element"]
            assert member["value"] != ""


def test_nvidias_repeated_cash_equivalents_are_not_a_restatement():
    """Six of these carried a `superseded_by` pointing at a 10-Q fact in a
    different context — a restatement that never happened. The 10-Q states them
    under `StatementOfFinancialPositionLocationBalanceAxis`, a typed dimension
    the extractor could not see, so they read as the same fact as the 10-K's."""
    facts = extract_numbers.extract("NVDA", FORMS)["facts"]
    here = [fact for fact in facts
            if fact["tag"] == "CashEquivalentsAtCarryingValue"
            and fact["context"].get("instant") == "2026-01-25"]
    assert here
    assert not [fact for fact in here if "superseded_by" in fact]


def test_cienas_amortized_cost_components_are_distinguishable():
    """The total and its components all read `{"instant": …, "segment": []}` and
    were indistinguishable in `input_numbers.json`."""
    facts = extract_numbers.extract("CIEN", FORMS)["facts"]
    here = [fact for fact in facts
            if fact["tag"] == "AvailableForSaleDebtSecuritiesAmortizedCostBasis"
            and fact["context"].get("instant") == "2026-05-02"]
    contexts = {json.dumps(fact["context"], sort_keys=True) for fact in here}
    assert len(contexts) >= 7, sorted(contexts)
    typed = [fact for fact in here if fact["context"].get("typed_segment")]
    assert {fact["number"] for fact in typed} == {110563000.0, 157619000.0, 200248000.0}
    # And the parts are no longer read as consolidated totals.
    assert not [fact for fact in typed if extract_numbers.usable(fact)]


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


# --- the id a fact prints on its row -----------------------------------------
#
# `docs/INPUT_SPEC.md` §2 gives a numeric fact the id
# `{accession}:facts:{tag}:{period}`, and the trend table already prints that
# shape for every fact it reads. Each fact now prints it too, as `paragraph_id`,
# so the numbers reader copies the id off the row instead of composing it. The
# expected ids below are that shape filled in by hand from the planted context.

PRINTED = b"""<xbrl xmlns="http://www.xbrl.org/2003/instance"
          xmlns:xbrldi="http://xbrl.org/2006/xbrldi"
          xmlns:us-gaap="http://fasb.org/us-gaap/2025">
      <context id="at"><period><instant>2025-09-27</instant></period></context>
      <context id="over"><period><startDate>2025-06-29</startDate>
        <endDate>2025-09-27</endDate></period></context>
      <context id="by_member"><entity><segment>
        <xbrldi:explicitMember dimension="srt:ProductOrServiceAxis"
          >us-gaap:ServiceMember</xbrldi:explicitMember>
      </segment></entity><period><startDate>2025-06-29</startDate>
        <endDate>2025-09-27</endDate></period></context>
      <context id="by_value"><entity><segment>
        <xbrldi:typedMember dimension="us-gaap:StatementOfFinancialPositionLocationBalanceAxis"
          ><us-gaap:BalanceSheetLocation>us-gaap:CashAndCashEquivalentsAtCarryingValue</us-gaap:BalanceSheetLocation
        ></xbrldi:typedMember>
      </segment></entity><period><instant>2025-09-27</instant></period></context>
      <unit id="usd"><measure>iso4217:USD</measure></unit>
      <unit id="chf"><measure>iso4217:CHF</measure></unit>
      <unit id="usd_per_share"><divide>
        <unitNumerator><measure>iso4217:USD</measure></unitNumerator>
        <unitDenominator><measure>xbrli:shares</measure></unitDenominator>
      </divide></unit>
      <us-gaap:AccountsReceivableNetCurrent contextRef="at" unitRef="usd" id="a"
        decimals="-6">29508000000</us-gaap:AccountsReceivableNetCurrent>
      <us-gaap:Revenues contextRef="over" unitRef="usd" id="b"
        decimals="-6">102466000000</us-gaap:Revenues>
      <us-gaap:Revenues contextRef="by_member" unitRef="usd" id="c"
        decimals="-6">28750000000</us-gaap:Revenues>
      <us-gaap:CashEquivalentsAtCarryingValue contextRef="by_value" unitRef="usd" id="d"
        decimals="-6">1000000</us-gaap:CashEquivalentsAtCarryingValue>
      <us-gaap:AccountsReceivableNetCurrent contextRef="at" unitRef="usd" id="e"
        decimals="-6">29508000000</us-gaap:AccountsReceivableNetCurrent>
      <us-gaap:DerivativeNotionalAmount contextRef="at" unitRef="usd" id="f"
        decimals="-3">381083000</us-gaap:DerivativeNotionalAmount>
      <us-gaap:DerivativeNotionalAmount contextRef="at" unitRef="chf" id="g"
        decimals="-3">306200000</us-gaap:DerivativeNotionalAmount>
      <us-gaap:EarningsPerShareBasic contextRef="over" unitRef="usd_per_share" id="h"
        decimals="2">1.85</us-gaap:EarningsPerShareBasic>
    </xbrl>"""


def printed_facts() -> list[dict]:
    return extract_numbers.facts_from_instance(
        PRINTED, accession="0000320193-25-000079", filing_date="2025-10-31")


def test_a_fact_prints_its_id_in_the_shape_the_spec_gives():
    assert [fact["paragraph_id"] for fact in printed_facts()] == [
        "0000320193-25-000079:facts:AccountsReceivableNetCurrent:2025-09-27",
        "0000320193-25-000079:facts:Revenues:2025-06-29..2025-09-27",
        "0000320193-25-000079:facts:Revenues:2025-06-29..2025-09-27"
        ":srt:ProductOrServiceAxis=us-gaap:ServiceMember",
        "0000320193-25-000079:facts:CashEquivalentsAtCarryingValue:2025-09-27"
        ":us-gaap:StatementOfFinancialPositionLocationBalanceAxis"
        "=us-gaap:CashAndCashEquivalentsAtCarryingValue",
        "0000320193-25-000079:facts:AccountsReceivableNetCurrent:2025-09-27",
        "0000320193-25-000079:facts:DerivativeNotionalAmount:2025-09-27",
        "0000320193-25-000079:facts:DerivativeNotionalAmount:2025-09-27"
        ":unit=iso4217:CHF",
        "0000320193-25-000079:facts:EarningsPerShareBasic:2025-06-29..2025-09-27",
    ]


def test_an_amount_the_filing_also_states_in_another_currency_names_that_currency():
    """One notional, stated in dollars and again in Swiss francs, in one context.
    The dollar figure keeps the spec's shape; the franc figure adds its unit, or
    the two rows would answer to one id. A dollar-per-share unit is still dollars
    and adds nothing."""
    dollars, francs, per_share = printed_facts()[5:8]
    assert (dollars["unit"], francs["unit"]) == ("iso4217:USD", "iso4217:CHF")
    assert dollars["context"] == francs["context"]
    assert per_share["unit"] == "iso4217:USD/xbrli:shares"
    assert francs["paragraph_id"] == dollars["paragraph_id"] + ":unit=iso4217:CHF"


def test_the_printed_id_sits_beside_the_element_id():
    """`id` stays the element's own; `paragraph_id` is the one a reader copies."""
    fact = printed_facts()[0]
    assert list(fact)[:2] == ["id", "paragraph_id"]
    assert fact["id"] == "0000320193-25-000079:a"


def test_a_fact_reported_against_a_dimension_never_prints_its_totals_id():
    """The service revenue is not the revenue, so it cannot answer to its id."""
    total, part = printed_facts()[1:3]
    assert total["tag"] == part["tag"] and part["context"]["segment"]
    assert total["paragraph_id"] != part["paragraph_id"]


def test_a_fact_the_filing_printed_twice_prints_one_id_twice():
    """Two elements, one context, one value: one fact, and the element ids differ."""
    facts = printed_facts()
    assert facts[0]["id"] != facts[4]["id"]
    assert facts[0]["paragraph_id"] == facts[4]["paragraph_id"]


@pytest.mark.parametrize("ticker", TICKERS)
def test_one_printed_id_names_one_fact(ticker):
    """Every fact prints an id, and two facts printing the same one are the same
    fact -- the same concept, context and unit in the same filing -- printed
    more than once. The id is what the gate resolves, so an id naming two
    different facts would let a quote of one stand for the other.

    `identity` leaves out the value and its precision, so this does not say the
    rows print the same digits. The next test says what they do print."""
    facts = extract_numbers.extract(ticker, FORMS)["facts"]
    named: dict[str, set] = {}
    for fact in facts:
        assert isinstance(fact["paragraph_id"], str) and fact["paragraph_id"]
        named.setdefault(fact["paragraph_id"], set()).add(
            (fact["source_accession"],) + extract_numbers.identity(fact))
    assert [one for one, facts_named in named.items() if len(facts_named) > 1] == []


def _stands_for(fact: dict) -> tuple[Decimal, Decimal]:
    """The interval a filed value covers at its own `decimals`."""
    number = Decimal(fact["value"])
    if fact.get("decimals") in (None, "INF"):
        return number, number
    half = Decimal(5).scaleb(-int(fact["decimals"]) - 1)
    return number - half, number + half


@pytest.mark.parametrize("ticker", TICKERS)
def test_rows_under_one_id_state_one_number_each_at_its_own_precision(ticker):
    """Rows under one id can print different digits. Where they do, each is the
    same number rounded to its own `decimals`: the intervals they cover overlap.
    A quote of either row stands under the id, and neither can carry a number
    the other contradicts."""
    named: dict[str, list[dict]] = {}
    for fact in extract_numbers.extract(ticker, FORMS)["facts"]:
        named.setdefault(fact["paragraph_id"], []).append(fact)
    contradicted = []
    for identifier, rows in named.items():
        if len({row["value"] for row in rows}) < 2:
            continue
        covered = [_stands_for(row) for row in rows]
        if max(low for low, _ in covered) > min(high for _, high in covered):
            contradicted.append(identifier)
    assert contradicted == []


def test_nvidias_goodwill_prints_to_the_million_and_to_the_hundred_million_under_one_id():
    """Read by hand from `tests/fixtures/NVDA/10-K/nvda-20260125_htm.xml`: two
    `us-gaap:Goodwill` elements in context c-11, unit usd -- `f-157`,
    20832000000 at decimals -6, and `f-554`, 20800000000 at decimals -8. One
    fact, two roundings, one id."""
    facts = extract_numbers.extract("NVDA", FORMS)["facts"]
    rows = {fact["id"]: fact for fact in facts
            if fact["id"] in ("0001045810-26-000021:f-157", "0001045810-26-000021:f-554")}
    assert {name: (row["value"], row["decimals"]) for name, row in rows.items()} == {
        "0001045810-26-000021:f-157": ("20832000000", "-6"),
        "0001045810-26-000021:f-554": ("20800000000", "-8")}
    assert {row["paragraph_id"] for row in rows.values()} == {
        "0001045810-26-000021:facts:Goodwill:2026-01-25"}


def test_the_receivables_row_the_numbers_reader_cited_prints_the_id_it_wrote():
    """The second pipeline check (PR #73) read NVDA's 10-Q 0001045810-26-000075.
    Its committed `input_numbers.json`, read by hand, holds the receivables
    balance as element `f-116`: `AccountsReceivableNetCurrent`, instant
    2026-07-26, value "63059000000". The numbers reader cited it as
    `0001045810-26-000075:facts:AccountsReceivableNetCurrent:2026-07-26`, the
    spec's shape, and the row printed no such id; now it does."""
    facts = extract_numbers.extract("NVDA", FORMS)["facts"]
    row = next(fact for fact in facts if fact["id"] == "0001045810-26-000075:f-116")
    assert (row["tag"], row["context"], row["value"]) == (
        "AccountsReceivableNetCurrent", {"instant": "2026-07-26", "segment": []},
        "63059000000")
    assert row["paragraph_id"] == \
        "0001045810-26-000075:facts:AccountsReceivableNetCurrent:2026-07-26"


def test_ttm_technologies_notional_in_francs_prints_its_own_id():
    """TTM Technologies' 10-Q 0001193125-26-335107, instance
    `tests/fixtures/TTMI/10-Q/ttmi-20260629_htm.xml.gz`, read by hand: context
    `C_5f828c03-...` is the instant 2026-06-18 with no segment, and in it
    `DerivativeNotionalAmount` is stated twice -- element `F_68ce2092-...` in
    `U_USD` as 381083000 and element `F_75cb79ee-...` in `U_CHF` (measure
    `iso4217:CHF`) as 306200000. Two amounts, so two ids."""
    facts = extract_numbers.extract("TTMI", FORMS)["facts"]
    accession = "0001193125-26-335107"
    by_element = {fact["id"]: fact for fact in facts}
    dollars = by_element[f"{accession}:F_68ce2092-e393-4a80-956e-09b2d810af09"]
    francs = by_element[f"{accession}:F_75cb79ee-0176-4104-a693-6d237b56dd92"]
    assert (dollars["value"], francs["value"]) == ("381083000", "306200000")
    assert dollars["paragraph_id"] == \
        "0001193125-26-335107:facts:DerivativeNotionalAmount:2026-06-18"
    assert francs["paragraph_id"] == \
        "0001193125-26-335107:facts:DerivativeNotionalAmount:2026-06-18:unit=iso4217:CHF"
