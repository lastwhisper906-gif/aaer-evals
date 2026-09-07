"""The cleaner deletes and renders. It never rewrites — checked on all 72.

The containment property is the one that matters here, so it is parameterised
over every fixture document rather than a sample: the four HTML documents per
company directly, and the two XBRL instances through the HTML inside their
notes. Seventy-two documents, no exception carved out. (`submissions.json` is
an index of filings rather than one of the documents, and is not in the count.)

Everything else is asserted on named paragraphs from named filings, not on
synthetic strings, because a cleaner that works on a synthetic page number and
not on Apple's is a cleaner that does not work.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from src import clean_text, cutoff_guard, extract_notes, extract_numbers, html_text, split_sections
from src.fetch_fixtures import TICKERS
from tests import independent_text

FIXTURES = Path(__file__).resolve().parent / "fixtures"
HTML_DOCUMENTS = (("10-K", "primary_html"), ("10-Q", "primary_html"),
                  ("8-K", "primary_html"), ("8-K", "exhibit_99_1"))
INSTANCES = (("10-K", "xbrl_instance"), ("10-Q", "xbrl_instance"))


def expected(ticker: str) -> dict:
    return json.loads((FIXTURES / ticker / "expected.json").read_text())


def document(ticker: str, form: str, role: str) -> str:
    row = cutoff_guard.one_document(ticker, form, role)
    return cutoff_guard.load_document(row["full_path"], row["filing_date"])


def test_the_fixture_set_holds_seventy_two_documents():
    """The number the containment property is claimed over."""
    documents = [row for ticker in TICKERS
                 for row in cutoff_guard.documents(ticker)
                 if row["form"] != "submissions"]
    assert len(documents) == 72


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form,role", HTML_DOCUMENTS)
def test_every_kept_paragraph_is_the_documents_own_text(ticker, form, role):
    html = document(ticker, form, role)
    result = clean_text.clean(html)
    source = independent_text.Source(html)
    missing = source.missing(result["paragraphs"])
    assert not missing, f"{ticker} {form} {role}: {missing[:1]}"
    canonical = html_text.strip_tags(html)
    for paragraph in result["paragraphs"]:
        assert paragraph in canonical


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form,role", INSTANCES)
def test_every_kept_note_paragraph_is_the_notes_own_text(ticker, form, role):
    """The other 24 of the 72: an instance's text is the HTML inside its notes."""
    sections = extract_notes.extract(ticker, form)["sections"]
    assert sections
    for section in sections:
        result = clean_text.clean(section["html"])
        missing = independent_text.Source(section["html"]).missing(result["paragraphs"])
        assert not missing, f"{ticker} {form} {section['name']}: {missing[:1]}"


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form,role", HTML_DOCUMENTS)
def test_nothing_is_both_kept_and_dropped(ticker, form, role):
    result = clean_text.clean(document(ticker, form, role))
    assert len(result["paragraphs"]) + len(result["dropped"]) == \
        len(html_text.paragraphs(document(ticker, form, role)))
    for drop in result["dropped"]:
        assert drop["reason"]


# --- named paragraphs from named filings -----------------------------------

def _mdna(ticker: str) -> dict:
    section = split_sections.extract(ticker, "10-K", "mdna")
    return clean_text.clean_section(section["paragraphs"])


def _dropped_texts(result: dict, reason: str) -> list[str]:
    return [drop["text"] for drop in result["dropped"] if drop["reason"] == reason]


def test_apples_page_footer_disappears():
    """'Apple Inc. | 2025 Form 10-K | 21' is on the bottom of every page."""
    result = _mdna("AAPL")
    headers = _dropped_texts(result, "running_header")
    assert "Apple Inc. | 2025 Form 10-K | 21" in headers
    assert "Apple Inc. | 2025 Form 10-K | 22" in headers
    assert not [p for p in result["paragraphs"] if "2025 Form 10-K |" in p]


def test_seagates_table_of_contents_link_disappears():
    result = _mdna("STX")
    assert "Table of Contents" in _dropped_texts(result, "table_of_contents_link")
    assert not [p for p in result["paragraphs"]
                if html_text.normalized(p) == "table of contents"]


def test_qualcomms_page_numbers_disappear():
    """A run of bare numbers climbing through the section: 38, 39, 40 …"""
    result = _mdna("QCOM")
    pages = _dropped_texts(result, "page_number")
    assert {"38", "39"} <= set(pages)
    assert not [p for p in result["paragraphs"] if html_text.normalized(p) == "38"]


def test_a_bare_year_in_a_column_heading_is_not_a_page_number():
    """The rule that keeps the numbers: 2025 and 2024 sit side by side and do
    not climb, so they are data and they stay."""
    result = _mdna("QCOM")
    assert "2025" not in _dropped_texts(result, "page_number")
    assert "2024" not in _dropped_texts(result, "page_number")


def test_ciscos_forward_looking_disclaimer_disappears():
    result = _mdna("CSCO")
    boilerplate = _dropped_texts(result, "forward_looking_boilerplate")
    assert len(boilerplate) == 1
    assert boilerplate[0].startswith("This Annual Report on Form 10-K")
    assert "forward-looking statements" in boilerplate[0]
    assert not [p for p in result["paragraphs"]
                if p.startswith("This Annual Report on Form 10-K, including")]


def test_generacs_forward_looking_disclaimer_disappears():
    result = _mdna("GNRC")
    boilerplate = _dropped_texts(result, "forward_looking_boilerplate")
    assert len(boilerplate) == 1
    assert "forward-looking statements" in html_text.normalized(boilerplate[0])


def test_a_row_label_that_repeats_is_not_furniture():
    """'Income before income taxes' appears once per table in Littelfuse's
    MD&A. Deleting it would take the words the numbers belong to."""
    result = _mdna("LFUS")
    kept = {html_text.normalized(p) for p in result["paragraphs"]}
    assert "income before income taxes" in kept


# --- tables ----------------------------------------------------------------

def test_the_release_tables_come_out_as_pipe_rows_with_every_cell():
    """AAPL's 8-K exhibit 99.1 holds three tables and nothing is lost."""
    html = document("AAPL", "8-K", "exhibit_99_1")
    result = clean_text.clean(html)
    assert len(result["tables"]) == 3

    by_hand = len(re.findall(r"<t[dh][\s>]", html, re.IGNORECASE))
    assert sum(table["cell_count"] for table in result["tables"]) == by_hand

    first = result["tables"][0]
    assert first["rows"], "no rows rendered"
    for row in first["rows"]:
        assert row.startswith("| ") and row.endswith(" |")
    assert sum(len(row.split(" | ")) for row in first["rows"]) == first["cell_count"]


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form,role", HTML_DOCUMENTS)
def test_every_table_cell_is_the_documents_own_text(ticker, form, role):
    html = document(ticker, form, role)
    result = clean_text.clean(html)
    source = independent_text.Source(html)
    cells = [cell for table in result["tables"] for cell in table["cells"] if cell]
    missing = source.missing(cells)
    assert not missing, f"{ticker} {form} {role}: {missing[:3]}"


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form", ("10-K", "10-Q", "8-K"))
def test_the_dropped_table_count(ticker, form):
    role = "exhibit_99_1" if form == "8-K" else "primary_html"
    facts = (extract_numbers.extract(ticker, (form,))["facts"]
             if form in ("10-K", "10-Q") else [])
    result = clean_text.clean(document(ticker, form, role), facts=facts)
    record = expected(ticker)["cleaner"][form]
    assert len(result["tables"]) == record["tables"]
    assert result["dropped_tables"] == record["tables_already_in_xbrl"]


@pytest.mark.parametrize("ticker", TICKERS)
def test_no_earnings_release_table_is_dropped(ticker):
    """The non-GAAP reconciliation and the guidance table are the two tables
    whose numbers are nowhere in XBRL, and they are the reason the exhibit is
    fetched at all."""
    assert expected(ticker)["cleaner"]["8-K"]["tables_already_in_xbrl"] == 0


def test_a_table_of_tagged_numbers_is_dropped_and_one_with_a_stranger_is_not():
    facts = [{"number": 1000.0}, {"number": 2000.0}, {"number": 3000.0}, {"number": 4000.0}]
    values = clean_text.fact_values(facts)
    tagged = [["Revenue", "1,000", "2,000"], ["Cost", "3,000", "4,000"]]
    assert clean_text.table_is_in_xbrl(tagged, values)[0] is True
    stranger = [["Revenue", "1,000", "2,000"], ["Adjusted", "3,000", "9,999"]]
    assert clean_text.table_is_in_xbrl(stranger, values)[0] is False


def test_a_table_with_too_few_numbers_is_always_kept():
    values = clean_text.fact_values([{"number": 1000.0}])
    assert clean_text.table_is_in_xbrl([["Revenue", "1,000"]], values)[0] is False


def test_a_cell_is_read_as_a_number_only_when_it_is_one():
    assert clean_text.cell_number("1,234") == 1234.0
    assert clean_text.cell_number("(1,234)") == -1234.0
    assert clean_text.cell_number("$ 1,234.5") == 1234.5
    assert clean_text.cell_number("12.3%") == 12.3
    assert clean_text.cell_number("Revenue") is None
    assert clean_text.cell_number("2025 vs. 2024") is None
    assert clean_text.cell_number("—") is None
    assert clean_text.cell_number("") is None
