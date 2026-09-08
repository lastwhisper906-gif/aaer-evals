"""Every TextBlock, and nothing invented on the way out.

Two counts again: the extractor's, and one taken straight off the instance with
ElementTree and the input spec's rule. Then the containment property, checked
against the naive stripper in `tests/independent_text.py` rather than against
the one the extractor used.
"""

from __future__ import annotations

import datetime as dt
import gzip
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from src import cutoff_guard, extract_notes, html_text
from src.fetch_fixtures import TICKERS
from tests import independent_text

FIXTURES = Path(__file__).resolve().parent / "fixtures"
FORMS = ("10-K", "10-Q")
ENTITY = re.compile(r"&(amp|lt|gt|quot|nbsp|#[0-9]+);")
HEADING = re.compile(r"^## ", re.MULTILINE)


def expected(ticker: str) -> dict:
    return json.loads((FIXTURES / ticker / "expected.json").read_text())


def _raw(path: Path) -> bytes:
    data = path.read_bytes()
    return gzip.decompress(data) if data[:2] == b"\x1f\x8b" else data


def _count_by_hand(path: Path) -> int:
    root = ET.fromstring(_raw(path))
    return sum(1 for element in root.iter()
               if element.tag.split("}")[-1].endswith("TextBlock"))


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form", FORMS)
def test_the_expected_count_is_what_the_instance_contains(ticker, form):
    row = cutoff_guard.one_document(ticker, form, "xbrl_instance")
    assert _count_by_hand(row["full_path"]) == expected(ticker)["notes"][form]["textblock_count"]


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form", FORMS)
def test_one_heading_per_textblock(ticker, form):
    payload = extract_notes.extract(ticker, form)
    document = extract_notes.render(payload)
    count = expected(ticker)["notes"][form]["textblock_count"]
    assert len(payload["sections"]) == count
    assert len(HEADING.findall(document)) == count


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form", FORMS)
def test_no_html_entity_survives(ticker, form):
    document = extract_notes.render(extract_notes.extract(ticker, form))
    leftovers = ENTITY.findall(document)
    assert not leftovers, f"{ticker} {form}: {sorted(set(leftovers))}"


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form", FORMS)
def test_every_section_is_the_filings_own_text(ticker, form):
    """Both directions of the containment property, per section.

    The first assertion is exact against the canonical stripper. The second
    re-derives the text with the naive stripper in tests/ and asserts the
    section is a contiguous run of *that*, which is what catches a canonical
    stripper that invented or dropped characters of its own.
    """
    for section in extract_notes.extract(ticker, form)["sections"]:
        assert section["text"] in html_text.strip_tags(section["html"])
        assert independent_text.contains(section["html"], section["text"]), \
            f"{ticker} {form} {section['name']}: not a contiguous run of the source"


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_selection_is_not_a_standard_tag_list(ticker):
    """A fixed list of standard tags would miss every one of these."""
    payload = extract_notes.extract(ticker, "10-K")
    extensions = [section for section in payload["sections"] if section["extension"]]
    assert len(extensions) == expected(ticker)["notes"]["10-K"]["extension_tag_count"]
    for section in extensions:
        assert not section["namespace"].startswith("http://fasb.org/us-gaap/")
        assert section["name"].startswith(f"{section['prefix']}:")


def test_at_least_one_company_carries_a_note_on_its_own_extension_namespace():
    """AAPL's disaggregated-net-sales table is tagged aapl:, not us-gaap:."""
    payload = extract_notes.extract("AAPL", "10-K")
    names = {section["name"]: section for section in payload["sections"]}
    section = names["aapl:DisaggregatedNetSalesAndPortionOfNetSalesThatWasPreviouslyDeferredTableTextBlock"]
    assert section["extension"] is True
    assert section["namespace"] == "http://www.apple.com/20250927"


@pytest.mark.parametrize("ticker", TICKERS)
def test_note_ids_are_dense_and_unique(ticker):
    sections = extract_notes.extract(ticker, "10-K")["sections"]
    accession = extract_notes.extract(ticker, "10-K")["accession"]
    # `note_section`, not `notes`: `…:notes:n` is the nth paragraph of
    # `input_notes.md` and this is the nth TextBlock of the instance.
    assert [section["id"] for section in sections] == \
        [f"{accession}:note_section:{i}" for i in range(1, len(sections) + 1)]


def test_the_extractor_goes_through_the_cutoff_gate():
    with pytest.raises(cutoff_guard.CutoffViolationError):
        extract_notes.extract("AAPL", "10-K", cutoff=dt.date(2020, 1, 1))
