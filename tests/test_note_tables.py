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
                "<td>Lost</td>" + number("f-99", "us-gaap:Revenues", "now", "7"))

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
<xbrli:unit id="usd"><xbrli:measure>iso4217:USD</xbrli:measure></xbrli:unit>
<us-gaap:InventoryNet id="f-1" contextRef="now" unitRef="usd" decimals="-3">1000000</us-gaap:InventoryNet>
<us-gaap:InventoryNet id="f-2" contextRef="then" unitRef="usd" decimals="-3">900000</us-gaap:InventoryNet>
<zzzz:ReturnsReserve id="f-3" contextRef="now" unitRef="usd" decimals="-3">1000000</zzzz:ReturnsReserve>
<zzzz:ReserveBasis id="f-4" contextRef="now">estimated</zzzz:ReserveBasis>
<zzzz:Other id="f-5" contextRef="now" unitRef="usd" xsi:nil="true"/>
<us-gaap:Revenues id="f-6" contextRef="segment" unitRef="usd" decimals="-3">250000</us-gaap:Revenues>
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
    assert segment == [{"concept": "us-gaap:Revenues", "value": 250_000.0,
                        "unit": "iso4217:USD", "start": "2026-04-01", "end": "2026-06-30",
                        "axes": {"us-gaap:StatementBusinessSegmentsAxis": "zzzz:WidgetsMember"},
                        "fact": f"{ACCESSION}:f-6"}]
    assert found["not_in_the_instance"] == [f"{ACCESSION}:notes:4: f-99"]


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
