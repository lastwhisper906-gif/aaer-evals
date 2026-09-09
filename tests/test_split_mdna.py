"""MD&A, cut at the right heading — and recounted through a different parser.

The recount here is not a call into `src/`. `tests/independent_text.py` builds
the block text with `html.parser`, this module finds the headings with its own
regexes, and the paragraph count that comes out is what `expected.json` is held
to. Twenty-four sections, twenty-four agreements, or the number is wrong.
"""

from __future__ import annotations

import datetime as dt
import json
import re
from pathlib import Path

import pytest

from src import cutoff_guard, html_text, split_sections
from src.fetch_fixtures import TICKERS
from tests import independent_text

FIXTURES = Path(__file__).resolve().parent / "fixtures"
FORMS = ("10-K", "10-Q")

TITLE = r"management.{0,3}s discussion and analysis"
# (heading, item-marker-alone, section end) per form, written out here rather
# than imported, so a change to src/split_sections.py cannot move both sides.
SPEC = {
    "10-K": (re.compile(rf"^item\s*7\s*[.:\-–—]?\s*{TITLE}"),
             re.compile(r"^item\s*7\s*[.:\-–—]?$"),
             re.compile(r"^item\s*7a\b|^item\s*8\b")),
    "10-Q": (re.compile(rf"^item\s*2\s*[.:\-–—]?\s*{TITLE}"),
             re.compile(r"^item\s*2\s*[.:\-–—]?$"),
             re.compile(r"^item\s*3\b|^item\s*4\b")),
}
TITLE_START = re.compile(rf"^{TITLE}")


def expected(ticker: str) -> dict:
    return json.loads((FIXTURES / ticker / "expected.json").read_text())


def source_html(ticker: str, form: str) -> str:
    row = cutoff_guard.one_document(ticker, form, "primary_html")
    return cutoff_guard.load_document(row["full_path"], row["filing_date"])


def _flat(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def recount(html: str, form: str) -> list[str]:
    """Strip tags, take the LAST Item 7 heading, stop at the first Item 7A or
    Item 8 heading, split on blank lines. No import from src."""
    text = independent_text.block_text(html)
    heading, marker, end = SPEC[form]
    rows = [(match.start(), _flat(match.group()))
            for match in re.finditer(r"^.*$", text, re.MULTILINE)]
    rows = [(offset, flat) for offset, flat in rows if flat]

    candidates = []
    for index, (offset, flat) in enumerate(rows):
        following = rows[index + 1][1] if index + 1 < len(rows) else ""
        if heading.search(flat) or (marker.search(flat) and TITLE_START.search(following)):
            candidates.append(offset)
    assert candidates, "no Item 7 heading found by the recount"

    start = candidates[-1]
    stop = next((offset for offset, flat in rows
                 if offset > start and end.search(flat)), len(text))
    return [chunk.strip() for chunk in text[start:stop].strip().split("\n\n")
            if chunk.strip()]


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form", FORMS)
def test_the_expected_paragraph_count_survives_an_independent_recount(ticker, form):
    assert len(recount(source_html(ticker, form), form)) == \
        expected(ticker)["mdna"][form]["paragraphs"]


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form", FORMS)
def test_the_splitter_finds_exactly_that_many_paragraphs(ticker, form):
    payload = split_sections.extract(ticker, form, "mdna")
    assert len(payload["paragraphs"]) == expected(ticker)["mdna"][form]["paragraphs"]


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form", FORMS)
def test_paragraph_ids_are_unique_and_dense(ticker, form):
    payload = split_sections.extract(ticker, form, "mdna")
    accession = payload["accession"]
    # One id per paragraph that survives the cleaner, because that is the list
    # the bundle publishes. Minted over the raw `paragraphs` the same string
    # named a different paragraph here than in the bundle.
    count = len(payload["carried"])
    assert count <= len(payload["paragraphs"])
    assert set(payload["paragraph_ids"]) == \
        {f"{accession}:mdna:{index}" for index in range(1, count + 1)}
    assert len(set(payload["paragraph_ids"])) == count


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_section_stops_before_item_7a_and_item_8(ticker):
    """A heading is a line. A sentence that mentions Item 8 is not one — STX's
    last MD&A paragraph says 'see "Item 8. Financial Statements"' and that is
    text, not a boundary."""
    payload = split_sections.extract(ticker, "10-K", "mdna")
    text = payload["text"]
    heads = [html_text.normalized(text[start:end]) for start, end in html_text.lines(text)]
    assert not [head for head in heads if re.match(r"^item\s*7a\b", head)]
    assert not [head for head in heads if re.match(r"^item\s*8\b", head)]
    assert sum(1 for head in heads if re.match(r"^item\s*7\s*[.:\-–—]?", head)) == 1


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form", FORMS)
def test_every_paragraph_is_the_filings_own_text(ticker, form):
    html = source_html(ticker, form)
    payload = split_sections.extract(ticker, form, "mdna")
    canonical = html_text.strip_tags(html)
    for paragraph in payload["paragraphs"]:
        assert paragraph in canonical
    missing = independent_text.Source(html).missing(payload["paragraphs"])
    assert not missing, f"{ticker} {form}: {missing[:1]}"


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form", FORMS)
def test_the_table_of_contents_entry_is_not_the_one_selected(ticker, form):
    """The trap, made explicit: where there are two candidates, taking the
    first one gives the index, and the index is three lines long."""
    html = source_html(ticker, form)
    text = html_text.strip_tags(html)
    spec = split_sections.SECTIONS[(form, "mdna")]
    candidates = split_sections.headings(text, spec)
    assert len(candidates) == expected(ticker)["mdna"][form]["heading_candidates"]

    start, stop, _, rule = split_sections.bounds(text, form, "mdna")
    assert rule == "last candidate"
    assert start == candidates[-1][0]
    if len(candidates) == 1:
        return

    # What the first match would have produced: the same end rule, applied from
    # the table-of-contents entry. It stops at the table of contents' own next
    # entry, so it is the index — a handful of lines, not the section.
    ends = [re.compile(pattern) for pattern in spec["end"]]
    from_index = candidates[0][0]
    index_stop = next(
        (line_start for line_start, line_end in html_text.lines(text)
         if line_start > from_index
         and any(end.search(html_text.normalized(text[line_start:line_end]))
                 for end in ends)),
        len(text))
    assert index_stop - from_index < (stop - start) / 10, \
        "the first match should be three lines of index, not a section"


def test_a_missing_section_raises_rather_than_returning_nothing():
    with pytest.raises(split_sections.SectionNotFound):
        split_sections.split("<html><body><p>nothing here</p></body></html>",
                             "10-K", "mdna")


def test_the_splitter_goes_through_the_cutoff_gate():
    with pytest.raises(cutoff_guard.CutoffViolationError):
        split_sections.extract("AAPL", "10-K", "mdna", cutoff=dt.date(2020, 1, 1))
