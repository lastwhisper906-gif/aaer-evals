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
# The six roles per company the dispatch counted as "all 72 fixture documents".
DISPATCHED_ROLES = (("10-K", "primary_html"), ("10-K", "xbrl_instance"),
                    ("10-Q", "primary_html"), ("10-Q", "xbrl_instance"),
                    ("8-K", "primary_html"), ("8-K", "exhibit_99_1"))
# Item 7 appended the prior-period 10-Q to every company, so the property is
# checked over those as well. The claim only ever grows.
HTML_DOCUMENTS = (("10-K", "primary_html"), ("10-Q", "primary_html"),
                  ("10-Q", "prior_period"),
                  ("8-K", "primary_html"), ("8-K", "exhibit_99_1"))
INSTANCES = (("10-K", "xbrl_instance"), ("10-Q", "xbrl_instance"),
             ("10-Q", "prior_period_xbrl_instance"))


def expected(ticker: str) -> dict:
    return json.loads((FIXTURES / ticker / "expected.json").read_text())


def document(ticker: str, form: str, role: str) -> str:
    row = cutoff_guard.one_document(ticker, form, role)
    return cutoff_guard.load_document(row["full_path"], row["filing_date"])


def test_the_fixture_set_holds_seventy_two_documents():
    """The number the containment property is claimed over."""
    documents = [row for ticker in TICKERS
                 for row in cutoff_guard.documents(ticker)
                 if (row["form"], row["role"]) in DISPATCHED_ROLES]
    assert len(documents) == 72


def test_the_prior_period_documents_are_extra_and_are_covered_too():
    """Item 7 appends two documents per company. They are checked as well, so
    the property now holds over more than the seventy-two, never fewer."""
    extra = [row for ticker in TICKERS for row in cutoff_guard.documents(ticker)
             if row["role"].startswith("prior_period")]
    assert len(extra) == 24
    covered = {role for _, role in HTML_DOCUMENTS + INSTANCES}
    assert {"prior_period", "prior_period_xbrl_instance"} <= covered


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
    sections = extract_notes.extract(ticker, form, role=role)["sections"]
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


# --- the keep direction ------------------------------------------------------
#
# Everything above this line asks whether the furniture went. These ask whether
# anything else went with it, which is the half cycle 19 did not have and the
# half that protects "every quote exists in those inputs": a paragraph the
# cleaner deletes can never be quoted, and no downstream check can notice.

def _table_cell_texts(html: str) -> set[str]:
    """Every cell of every table in the document, flattened for comparison."""
    return {html_text.normalized(cell)
            for table in html_text.tables(html)
            for row in table for cell in row if html_text.normalized(cell)}


def _visible(text: str) -> str:
    """The text with zero-width characters treated as the whitespace they are."""
    return re.sub(r"[\s​‌‍⁠﻿]+", " ", text).strip()


def _dropped_cells(html: str) -> list[dict]:
    """Dropped paragraphs the same document also prints inside a table."""
    result = clean_text.clean(html)
    cells = _table_cell_texts(html)
    return [drop for drop in result["dropped"]
            if _visible(drop["text"]) and html_text.normalized(drop["text"]) in cells]


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form,role", HTML_DOCUMENTS)
def test_no_dropped_paragraph_is_a_cell_of_a_table_in_the_same_document(
        ticker, form, role):
    """The row labels are the words the numbers belong to.

    Apple's operating-lease maturity table names its rows `2026 2027 2028 2029
    2030` and Carrier's segment table numbers its footnotes `81 84 87`; both
    used to leave as page numbers while their amounts stayed. A paragraph the
    document itself prints as a table cell is data, whatever shape it has.
    """
    bad = _dropped_cells(document(ticker, form, role))
    assert not bad, f"{ticker} {form} {role}: {bad[:3]}"


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form,role", INSTANCES)
def test_no_dropped_note_paragraph_is_a_cell_of_a_table_in_the_same_note(
        ticker, form, role):
    """The other 36 of the 96: the note bodies inside the XBRL instances."""
    for section in extract_notes.extract(ticker, form, role=role)["sections"]:
        bad = _dropped_cells(section["html"])
        assert not bad, f"{ticker} {form} {section['name']}: {bad[:3]}"


_APPLE_FOOTER = re.compile(
    r"Apple Inc\.\s*\|\s*(?:2025 Form 10-K|Q[1-4] 2026 Form 10-Q)\s*\|\s*\d+")


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form,role", HTML_DOCUMENTS)
def test_the_only_running_header_in_the_fixture_set_is_apples_page_footer(
        ticker, form, role):
    """Eleven of the twelve print no repeating header the stripper can see.

    Cycle 19 deleted 384 distinct texts under this reason and only Apple's 26
    were furniture; the rest were debt-schedule row labels, roll-forward rows
    and period column headings. The rule is not "a shape that repeats" any
    more, so this asserts the outcome directly, against the one filer that has
    a page footer with words in it.
    """
    html = document(ticker, form, role)
    headers = _dropped_texts(clean_text.clean(html), "running_header")
    if ticker != "AAPL":
        assert headers == [], f"{ticker} {form} {role}: {headers[:3]}"
        return
    # Every one Apple's own text prints, and never one it does not.
    printed = set(_APPLE_FOOTER.findall(independent_text.strip(html)))
    for header in headers:
        assert _APPLE_FOOTER.fullmatch(header), header
        assert independent_text.flat(header) in {independent_text.flat(p)
                                                 for p in printed}


def test_qualcomms_page_tails_run_to_the_last_page_of_the_item():
    """38 through 46. Page 46 holds nine paragraphs before Item 7 ends, which
    is why the run rule counts the gap in paragraphs rather than requiring a
    whole page of them."""
    pages = _dropped_texts(_mdna("QCOM"), "page_number")
    assert sorted(set(pages), key=int) == [str(n) for n in range(38, 47)]


def test_palo_altos_ascending_year_columns_are_not_a_page_run():
    """`2023 2024 2025` climbs, a page apart, flanked by prose, six times over
    in Palo Alto's MD&A. Qualcomm's columns descend, so cycle 19's control test
    passed while this one would have failed."""
    result = _mdna("PANW")
    assert _dropped_texts(result, "page_number") == []
    kept = {html_text.normalized(p) for p in result["paragraphs"]}
    assert {"2023", "2024", "2025"} <= kept


ROW_LABELS_THAT_MUST_SURVIVE = (
    # (ticker, form, role, text) — every one named in the cycle-20 review as
    # content the cleaner deleted, read back out of the filing it came from.
    ("AAPL", "10-K", "primary_html", "2026"),
    ("AAPL", "10-K", "primary_html", "2030"),
    ("TTMI", "10-K", "primary_html", "2027"),
    ("TTMI", "10-K", "primary_html", "2030"),
    ("CARR", "10-K", "primary_html", "81"),
    ("CARR", "10-K", "primary_html", "87"),
    ("ESE", "10-Q", "primary_html", "308"),
    ("ESE", "10-Q", "primary_html", "310"),
    ("STX", "10-K", "primary_html", "Balance at June 27, 2025"),
    ("CARR", "10-K", "primary_html", "(2) See Note 20 - Divestitures for additional information."),
    ("QCOM", "10-Q", "primary_html", "+ $101 million increase in share-based compensation expense"),
)


@pytest.mark.parametrize("ticker,form,role,text", ROW_LABELS_THAT_MUST_SURVIVE)
def test_the_row_labels_the_cleaner_used_to_delete_are_in_the_input(
        ticker, form, role, text):
    result = clean_text.clean(document(ticker, form, role))
    dropped = [d for d in result["dropped"]
               if html_text.normalized(d["text"]) == html_text.normalized(text)]
    assert not dropped, f"{ticker} {form} dropped {text!r} as {dropped[0]['reason']}"
    assert any(html_text.normalized(p) == html_text.normalized(text)
               for p in result["paragraphs"]), f"{ticker} {form} has no {text!r}"


def test_a_running_header_is_a_line_whose_page_number_climbs():
    """The shape test alone matched eight Qualcomm MD&A bullets and a Carrier
    footnote. What a page footer has and a repeated row label does not is one
    digit group that counts up through the document."""
    footers = ["Acme Inc. | 2025 Form 10-K | 12",
               "Acme Inc. | 2025 Form 10-K | 13",
               "Acme Inc. | 2025 Form 10-K | 14"]
    assert clean_text.running_headers(footers) == {"acme inc. | # form #-k | #"}
    bullets = ["+ $101 million increase in share-based compensation expense",
               "+ $269 million increase in share-based compensation expense",
               "+ $62 million increase in share-based compensation expense"]
    assert clean_text.running_headers(bullets) == set()
    two_groups = ["Balance at June 30, 2023", "Balance at June 28, 2024",
                  "Balance at June 27, 2025"]
    assert clean_text.running_headers(two_groups) == set()


def test_a_row_label_next_to_its_own_numbers_is_never_furniture():
    paragraphs = ["Balance at June 30, 2023", "207", "—", "7,373"]
    assert clean_text.beside_a_number(paragraphs, 0) is True
    assert clean_text.beside_prose(paragraphs, 0) is True
    prose = ["Rest of Asia Pacific net sales increased during 2025.",
             "Apple Inc. | 2025 Form 10-K | 22", "Products and Services"]
    assert clean_text.beside_a_number(prose, 1) is False


def test_a_bare_number_between_two_cells_is_not_a_page_tail():
    """Qualcomm's MD&A: `55` then `%` is a table, `46` then a heading is a page."""
    assert clean_text.beside_prose(["1,469", "55", "%"], 1) is False
    assert clean_text.beside_prose(["…text…", "46", "Recent Accounting"], 1) is True
