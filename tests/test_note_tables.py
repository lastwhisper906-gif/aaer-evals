"""A note table's facts are the ones tagged inside it, never ones that share a number.

The planted filing below is built for the cases the committed ones may not
hold: two tables that print the same number for two different facts, one table
printed twice, a text fact and a nil fact inside a table, a dimensional fact, a
fact the instance does not carry, a paragraph no table renders to, and a table
of the prior filing. Each paragraph's text is what `src/clean_text.py`, the
renderer `input_notes.md` is written with, makes of the planted table, as the
bundle's paragraphs are made; the expected facts are the ones planted in each
table, read off this file.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src import clean_text, note_tables

ACCESSION = "0000000000-26-000001"
PRIOR = "0000000000-26-000000"


def table(*rows: str) -> str:
    return "<table>" + "".join(f"<tr>{row}</tr>" for row in rows) + "</table>"


def number(fact_id: str, name: str, context: str, shown: str, *, sign: str = "") -> str:
    sign_attribute = f' sign="{sign}"' if sign else ""
    return (f'<td><ix:nonFraction id="{fact_id}" name="{name}" contextRef="{context}" '
            f'unitRef="usd" decimals="-3" scale="3" format="ixt:num-dot-decimal"'
            f'{sign_attribute}>{shown}</ix:nonFraction></td>')


# Two tables print 1,000: the first is inventory, the second a reserve.
INVENTORY = table("<td>Inventory</td>" + number("f-1", "us-gaap:InventoryNet", "now", "1,000"),
                  "<td>Prior</td>" + number("f-2", "us-gaap:InventoryNet", "then", "900"))
RESERVE = table("<td>Reserve</td>" + number("f-3", "zzzz:ReturnsReserve", "now", "1,000"),
                "<td>Note</td><td><ix:nonNumeric id=\"f-4\" name=\"zzzz:ReserveBasis\" "
                "contextRef=\"now\">estimated</ix:nonNumeric></td>",
                "<td>Nil</td>" + "<td><ix:nonFraction id=\"f-5\" name=\"zzzz:Other\" "
                "contextRef=\"now\" unitRef=\"usd\" xsi:nil=\"true\"/></td>")
# A segment's revenue, against a member, and a fact the instance never carried.
SEGMENT = table("<td>Segment</td>" + number("f-6", "us-gaap:Revenues", "segment", "250"),
                "<td>Lost</td>" + number("f-99", "us-gaap:Revenues", "now", "7"),
                "<td>Backlog</td>" + number("f-9", "us-gaap:RevenueRemainingPerformanceObligation",
                                            "band", "40"),
                "<td>Price</td>" + number("f-10", "us-gaap:ShareBasedCompensationArrangementBy"
                                          "ShareBasedPaymentAwardOptionsExercisePrice", "now",
                                          "191.20"),
                "<td>Volatility</td>" + number("f-11", "us-gaap:FairValueAssumptionsExpected"
                                               "Volatility", "now", "0.3"),
                # Western Digital's shape: a cap price per a unit the filer
                # defines, and a strike price in plain dollars
                "<td>Cap</td>" + number("f-12", "us-gaap:DerivativeCapPrice", "now", "50.41"),
                "<td>Strike</td>" + number("f-13", "us-gaap:DerivativePriceRiskOption"
                                           "StrikePrice", "now", "37.74"),
                # a per-share amount whose name names no price: Apple's shape
                "<td>Grant</td>" + number("f-14", "us-gaap:ShareBasedCompensationArrangementBy"
                                          "ShareBasedPaymentAwardEquityInstrumentsOtherThan"
                                          "OptionsGrantsInPeriodWeightedAverageGrantDate"
                                          "FairValue", "now", "258.16"),
                # amounts in plain dollars worked out from the share price: an
                # intrinsic value, and the fair value of the awards that vested
                "<td>Intrinsic</td>" + number("f-15", "us-gaap:ShareBasedCompensationArrangement"
                                              "ByShareBasedPaymentAwardOptionsOutstanding"
                                              "IntrinsicValue", "now", "8,123"),
                "<td>Vested</td>" + number("f-16", "us-gaap:ShareBasedCompensationArrangement"
                                           "ByShareBasedPaymentAwardEquityInstrumentsOther"
                                           "ThanOptionsVestedInPeriodTotalFairValue", "now",
                                           "6,457"),
                # the option model's dividend yield: the dividend over the price
                "<td>Yield</td>" + number("f-17", "us-gaap:ShareBasedCompensationArrangement"
                                          "ByShareBasedPaymentAwardFairValueAssumptions"
                                          "ExpectedDividendRate", "now", "0.0006"))

INLINE = f"""<html xmlns="http://www.w3.org/1999/xhtml"
 xmlns:ix="http://www.xbrl.org/2013/inlineXBRL"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><body>
<ix:nonNumeric id="t-1" name="us-gaap:InventoryDisclosureTextBlock" contextRef="now">
{INVENTORY}{RESERVE}</ix:nonNumeric>
<ix:nonNumeric id="t-2" name="us-gaap:SegmentReportingDisclosureTextBlock" contextRef="now">
{SEGMENT}{INVENTORY.replace('id="f-1"', 'id="f-7"').replace('id="f-2"', 'id="f-8"')}
</ix:nonNumeric></body></html>""".encode()

INSTANCE = f"""<xbrl xmlns="http://www.xbrl.org/2003/instance"
 xmlns:xbrli="http://www.xbrl.org/2003/instance"
 xmlns:xbrldi="http://xbrl.org/2006/xbrldi"
 xmlns:us-gaap="http://fasb.org/us-gaap/2025"
 xmlns:zzzz="http://example.com/zzzz/20260630"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<xbrli:context id="now"><xbrli:period><xbrli:instant>2026-06-30</xbrli:instant></xbrli:period></xbrli:context>
<xbrli:context id="then"><xbrli:period><xbrli:instant>2025-12-31</xbrli:instant></xbrli:period></xbrli:context>
<xbrli:context id="segment"><xbrli:entity><xbrli:segment>
<xbrldi:explicitMember dimension="us-gaap:StatementBusinessSegmentsAxis">zzzz:WidgetsMember</xbrldi:explicitMember>
</xbrli:segment></xbrli:entity>
<xbrli:period><xbrli:startDate>2026-04-01</xbrli:startDate><xbrli:endDate>2026-06-30</xbrli:endDate></xbrli:period></xbrli:context>
<xbrli:context id="band"><xbrli:entity><xbrli:segment>
<xbrldi:typedMember dimension="us-gaap:RevenueRemainingPerformanceObligationExpectedTimingOfSatisfactionStartDateAxis"><us-gaap:date.domain>2027-07-01</us-gaap:date.domain></xbrldi:typedMember>
</xbrli:segment></xbrli:entity>
<xbrli:period><xbrli:instant>2026-06-30</xbrli:instant></xbrli:period></xbrli:context>
<xbrli:unit id="usd"><xbrli:measure>iso4217:USD</xbrli:measure></xbrli:unit>
<xbrli:unit id="usdPerShare"><xbrli:divide><xbrli:unitNumerator><xbrli:measure>iso4217:USD</xbrli:measure></xbrli:unitNumerator><xbrli:unitDenominator><xbrli:measure>xbrli:shares</xbrli:measure></xbrli:unitDenominator></xbrli:divide></xbrli:unit>
<xbrli:unit id="pure"><xbrli:measure>xbrli:pure</xbrli:measure></xbrli:unit>
<xbrli:unit id="usdPerUnit"><xbrli:divide><xbrli:unitNumerator><xbrli:measure>iso4217:USD</xbrli:measure></xbrli:unitNumerator><xbrli:unitDenominator><xbrli:measure>zzzz:Unit</xbrli:measure></xbrli:unitDenominator></xbrli:divide></xbrli:unit>
<us-gaap:InventoryNet id="f-1" contextRef="now" unitRef="usd" decimals="-3">1000000</us-gaap:InventoryNet>
<us-gaap:InventoryNet id="f-2" contextRef="then" unitRef="usd" decimals="-3">900000</us-gaap:InventoryNet>
<zzzz:ReturnsReserve id="f-3" contextRef="now" unitRef="usd" decimals="-3">1000000</zzzz:ReturnsReserve>
<zzzz:ReserveBasis id="f-4" contextRef="now">estimated</zzzz:ReserveBasis>
<zzzz:Other id="f-5" contextRef="now" unitRef="usd" xsi:nil="true"/>
<us-gaap:Revenues id="f-6" contextRef="segment" unitRef="usd" decimals="-3">250000</us-gaap:Revenues>
<us-gaap:RevenueRemainingPerformanceObligation id="f-9" contextRef="band" unitRef="usd" decimals="-3">40000</us-gaap:RevenueRemainingPerformanceObligation>
<us-gaap:ShareBasedCompensationArrangementByShareBasedPaymentAwardOptionsExercisePrice id="f-10" contextRef="now" unitRef="usdPerShare" decimals="2">191.20</us-gaap:ShareBasedCompensationArrangementByShareBasedPaymentAwardOptionsExercisePrice>
<us-gaap:FairValueAssumptionsExpectedVolatility id="f-11" contextRef="now" unitRef="pure" decimals="3">0.3</us-gaap:FairValueAssumptionsExpectedVolatility>
<us-gaap:DerivativeCapPrice id="f-12" contextRef="now" unitRef="usdPerUnit" decimals="2">50.41</us-gaap:DerivativeCapPrice>
<us-gaap:DerivativePriceRiskOptionStrikePrice id="f-13" contextRef="now" unitRef="usd" decimals="2">37.74</us-gaap:DerivativePriceRiskOptionStrikePrice>
<us-gaap:ShareBasedCompensationArrangementByShareBasedPaymentAwardEquityInstrumentsOtherThanOptionsGrantsInPeriodWeightedAverageGrantDateFairValue id="f-14" contextRef="now" unitRef="usdPerShare" decimals="2">258.16</us-gaap:ShareBasedCompensationArrangementByShareBasedPaymentAwardEquityInstrumentsOtherThanOptionsGrantsInPeriodWeightedAverageGrantDateFairValue>
<us-gaap:ShareBasedCompensationArrangementByShareBasedPaymentAwardOptionsOutstandingIntrinsicValue id="f-15" contextRef="now" unitRef="usd" decimals="-3">8123000</us-gaap:ShareBasedCompensationArrangementByShareBasedPaymentAwardOptionsOutstandingIntrinsicValue>
<us-gaap:ShareBasedCompensationArrangementByShareBasedPaymentAwardEquityInstrumentsOtherThanOptionsVestedInPeriodTotalFairValue id="f-16" contextRef="now" unitRef="usd" decimals="-3">6457000</us-gaap:ShareBasedCompensationArrangementByShareBasedPaymentAwardEquityInstrumentsOtherThanOptionsVestedInPeriodTotalFairValue>
<us-gaap:ShareBasedCompensationArrangementByShareBasedPaymentAwardFairValueAssumptionsExpectedDividendRate id="f-17" contextRef="now" unitRef="pure" decimals="4">0.0006</us-gaap:ShareBasedCompensationArrangementByShareBasedPaymentAwardFairValueAssumptionsExpectedDividendRate>
<us-gaap:InventoryNet id="f-7" contextRef="now" unitRef="usd" decimals="-3">1000000</us-gaap:InventoryNet>
<us-gaap:InventoryNet id="f-8" contextRef="then" unitRef="usd" decimals="-3">900000</us-gaap:InventoryNet>
</xbrl>""".encode()


def rendered(html_table: str) -> str:
    """The paragraph `input_notes.md` carries for a table, as the bundle makes it."""
    paragraphs = clean_text.clean_stream(html_table)["paragraphs"]
    assert len(paragraphs) == 1
    return paragraphs[0]


def bare(html_table: str) -> str:
    """The table as the instance's text block holds it: no inline tags."""
    import re
    return re.sub(r"</?ix:[^>]*>", "", html_table)


PARAGRAPHS = [
    (f"{ACCESSION}:notes:1", "Inventories consist of the following."),
    (f"{ACCESSION}:notes:2", rendered(bare(INVENTORY))),
    (f"{ACCESSION}:notes:3", rendered(bare(RESERVE))),
    (f"{ACCESSION}:notes:4", rendered(bare(SEGMENT))),
    (f"{ACCESSION}:notes:5", "| Not | a table the filing holds |"),
    (f"{PRIOR}:notes:9", rendered(bare(INVENTORY))),
    (f"{ACCESSION}:notes:6", f"[same as prior period, unchanged from {PRIOR}:notes:9]"),
]


@pytest.fixture(scope="module")
def found() -> dict:
    return note_tables.tables(PARAGRAPHS, INLINE, INSTANCE, accession=ACCESSION)


def ids(entry: dict) -> list[str]:
    return [cell["fact"].split(":", 1)[1] for cell in entry["facts"]]


def test_a_number_printed_in_two_tables_goes_to_the_table_that_tags_it(found):
    assert ids(found["tables"]["notes_2"])[:2] == ["f-1", "f-2"]
    assert ids(found["tables"]["notes_3"]) == ["f-3", "f-5"]
    reserve = found["tables"]["notes_3"]["facts"][0]
    assert (reserve["concept"], reserve["value"], reserve["instant"]) == \
        ("zzzz:ReturnsReserve", 1_000_000.0, "2026-06-30")


def test_a_table_printed_twice_is_one_table_and_its_facts_are_listed_once(found):
    """The inventory table is printed again in the segment note under new ids:
    the same facts, so the paragraph keeps one cell for each."""
    assert len(found["tables"]["notes_2"]["facts"]) == 2
    assert found["tables"]["notes_2"]["paragraph"] == f"{ACCESSION}:notes:2"


def test_a_text_fact_is_not_a_cell_and_a_nil_fact_says_so(found):
    cells = found["tables"]["notes_3"]["facts"]
    assert "zzzz:ReserveBasis" not in {cell["concept"] for cell in cells}
    nil = next(cell for cell in cells if cell["concept"] == "zzzz:Other")
    assert nil["nil"] is True and nil["value"] is None


def test_a_dimensional_fact_carries_its_axes_and_a_missing_one_is_named(found):
    segment = found["tables"]["notes_4"]["facts"]
    assert segment[0] == {"concept": "us-gaap:Revenues", "value": 250_000.0,
                          "unit": "iso4217:USD", "start": "2026-04-01", "end": "2026-06-30",
                          "axes": {"us-gaap:StatementBusinessSegmentsAxis": "zzzz:WidgetsMember"},
                          "fact": f"{ACCESSION}:f-6"}
    assert found["not_in_the_instance"] == [f"{ACCESSION}:notes:4: f-99"]


def test_a_typed_member_is_carried_and_its_date_is_never_read_as_a_period(found):
    """A remaining-performance-obligation band starting 2027-07-01, a date after
    the filing that the filing states; written whole it would read as a period
    after the cutoff, which the owner's grader refuses."""
    from src import run_analysis

    band = next(cell for cell in found["tables"]["notes_4"]["facts"]
                if cell["fact"].endswith(":f-9"))
    assert band["axes"] == {
        "us-gaap:RevenueRemainingPerformanceObligationExpectedTimingOfSatisfactionStartDateAxis":
            "date.domain = 2027-07-01"}
    assert run_analysis.calculator_problems({"note_tables": found}, "2026-07-31") == []


def test_a_price_per_share_and_a_volatility_never_reach_the_analysts(found):
    concepts = {cell["concept"] for cell in found["tables"]["notes_4"]["facts"]}
    assert not any(word in name for name in concepts
                   for word in ("Price", "Volatility", "FairValue", "IntrinsicValue"))
    assert found["left_out_as_a_price"] == {"notes_4": 8}
    # and a value in dollars that is no equity award's stands: the segment's
    # revenue and the backlog band
    assert {"us-gaap:Revenues", "us-gaap:RevenueRemainingPerformanceObligation"} <= concepts
    for printed in ("258.16", "191.2", "50.41", "37.74"):
        assert printed not in json.dumps(found)


def test_the_memo_prints_a_filing_unit_as_it_prints_the_calculators():
    """Apple's non-current intangible assets, 20,342 million: 203.4억 달러."""
    from src import memo

    assert memo.korean_number(20_342e6, "iso4217:USD") == "203.4억 달러" == \
        memo.korean_number(20_342e6, "USD")


def test_a_table_no_table_renders_to_is_unmatched_and_never_guessed(found):
    assert found["unmatched"] == [f"{ACCESSION}:notes:5"]
    assert "notes_5" not in found["tables"]


def test_prose_and_the_prior_filing_are_left_out(found):
    assert sorted(found["tables"]) == ["notes_2", "notes_3", "notes_4"]


def test_a_run_with_no_bundle_or_no_document_of_its_filing_says_what_is_missing(tmp_path):
    assert "missing" in note_tables.from_run("AAPL", ACCESSION, "2026-07-31",
                                             fixtures_root=tmp_path, bundle=None)
    run = tmp_path / "run"
    run.mkdir()
    (run / "input_notes.md").write_text("[x:notes:1]\nprose\n", encoding="utf-8")
    store = tmp_path / "store" / "ZZZZ"
    store.mkdir(parents=True)
    (store / "manifest.json").write_text(json.dumps(
        {"ticker": "ZZZZ", "cik": "0000000000", "documents": []}), encoding="utf-8")
    missing = note_tables.from_run("ZZZZ", ACCESSION, "2026-07-31",
                                   fixtures_root=tmp_path / "store", bundle=run)
    assert "no inline document and instance" in missing["missing"]


def planted_store(tmp_path: Path, inline: bytes) -> tuple[Path, Path]:
    """A store holding the planted filing's two documents, and a bundle."""
    store = tmp_path / "store"
    (store / "ZZZZ" / "10-Q").mkdir(parents=True)
    (store / "ZZZZ" / "10-Q" / "zzzz.htm").write_bytes(inline)
    (store / "ZZZZ" / "10-Q" / "zzzz_htm.xml").write_bytes(INSTANCE)
    documents = [{"form": "10-Q", "role": role, "accession": ACCESSION,
                  "filing_date": "2026-07-30", "path": f"10-Q/{name}", "stored": "raw"}
                 for role, name in (("primary_html", "zzzz.htm"),
                                    ("xbrl_instance", "zzzz_htm.xml"))]
    (store / "ZZZZ" / "manifest.json").write_text(json.dumps(
        {"ticker": "ZZZZ", "cik": "0000000000", "as_of": "2026-07-30",
         "documents": documents}), encoding="utf-8")
    run = tmp_path / "run"
    run.mkdir()
    (run / "input_notes.md").write_text(
        "".join(f"[{paragraph}]\n{text}\n\n" for paragraph, text in PARAGRAPHS),
        encoding="utf-8")
    return store, run


def test_a_run_reads_its_filing_through_the_gate(tmp_path):
    store, run = planted_store(tmp_path, INLINE)
    found = note_tables.from_run("ZZZZ", ACCESSION, "2026-07-31", fixtures_root=store,
                                 bundle=run)
    assert sorted(found["tables"]) == ["notes_2", "notes_3", "notes_4"]
    # a cutoff before the filing's date is refused by the gate, not read around
    refused = note_tables.from_run("ZZZZ", ACCESSION, "2026-07-29", fixtures_root=store,
                                   bundle=run)
    assert "tables" not in refused and "2026-07-30" in refused["missing"]


def test_an_inline_document_that_is_not_xml_is_named_not_raised(tmp_path):
    store, run = planted_store(tmp_path, INLINE.replace(b"</body>", b"<br></body>"))
    found = note_tables.from_run("ZZZZ", ACCESSION, "2026-07-31", fixtures_root=store,
                                 bundle=run)
    assert "not well-formed XML" in found["missing"]
