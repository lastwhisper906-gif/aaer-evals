"""8-K item codes from the index, and the earnings release from the exhibit.

The fixture 8-K for each company was chosen because it carries item 2.02, so
none of the twelve happens to carry a 1.01, 4.01, 4.02 or 5.02 — the items
whose bodies go in verbatim. That path is therefore tested on a constructed
8-K body rather than on a fixture, and the absence is stated here rather than
left for a reader to notice: today no company in the fixture set has filed a
non-reliance or auditor-change 8-K within the stored window.
"""

from __future__ import annotations

import datetime as dt
import json
import re
from pathlib import Path

import pytest

from src import cutoff_guard, parse_8k
from src.fetch_fixtures import TICKERS
from tests import independent_text

FIXTURES = Path(__file__).resolve().parent / "fixtures"
CODE = re.compile(r"^\d+\.\d{2}$")


def expected(ticker: str) -> dict:
    return json.loads((FIXTURES / ticker / "expected.json").read_text())


def exhibit_html(ticker: str) -> str:
    row = cutoff_guard.one_document(ticker, "8-K", "exhibit_99_1")
    return cutoff_guard.load_document(row["full_path"], row["filing_date"])


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_stored_8k_carries_item_2_02(ticker):
    """The fixture selection and the parser have to agree on what a code is."""
    row = cutoff_guard.one_document(ticker, "8-K", "primary_html")
    assert "2.02" in parse_8k.item_codes(row["items"])


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_index_reports_8ks_and_every_code_is_a_code(ticker):
    filings = parse_8k.eight_k_filings(parse_8k.submissions(ticker))
    assert filings, f"{ticker}: no 8-K in the stored submissions index"
    assert len(filings) == expected(ticker)["earnings_release"]["8-K"]["eight_k_filings_in_the_index"]
    for filing in filings:
        assert filing["items"], f"{ticker} {filing['accession']}: no item codes"
        for code in filing["items"]:
            assert CODE.match(code), f"{ticker} {filing['accession']}: {code!r}"


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_index_is_a_recount_of_the_stored_file(ticker):
    """Read the index with `json` and count the 8-Ks by hand."""
    row = cutoff_guard.one_document(ticker, "submissions", "submissions_index")
    raw = json.loads(cutoff_guard.load_document(row["full_path"], row["filing_date"]))
    by_hand = [row for row in raw["filings"] if row["form"] == "8-K"]
    assert len(by_hand) == \
        expected(ticker)["earnings_release"]["8-K"]["eight_k_filings_in_the_index"]
    assert {row["accession"] for row in by_hand} == \
        {row["accession"] for row in parse_8k.eight_k_filings(raw)}


@pytest.mark.parametrize("ticker", TICKERS)
def test_a_run_with_an_earlier_cutoff_does_not_learn_of_later_filings(ticker):
    """The index file is read without the date gate, because a catalogue of
    filings is not a filing. The cutoff moves to the rows instead, and this is
    the test that says the rows are actually filtered."""
    index = parse_8k.submissions(ticker)
    everything = parse_8k.eight_k_filings(index)
    edge = everything[-1]["filing_date"]
    kept = parse_8k.eight_k_filings(index, edge)
    assert kept, f"{ticker}: the oldest 8-K should survive its own date"
    assert all(row["filing_date"] <= edge for row in kept)
    assert len(kept) < len(everything) or len(everything) == 1
    day_before = (dt.date.fromisoformat(edge) - dt.timedelta(days=1)).isoformat()
    assert parse_8k.eight_k_filings(index, day_before) == []


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_stored_index_holds_nothing_filed_after_the_cutoff(ticker):
    row = cutoff_guard.one_document(ticker, "submissions", "submissions_index")
    raw = json.loads(cutoff_guard.load_document(row["full_path"], row["filing_date"]))
    assert raw["filings"]
    for filing in raw["filings"]:
        assert filing["filing_date"] <= raw["as_of"], \
            f"{ticker}: {filing['accession']} filed {filing['filing_date']}"


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_release_paragraph_and_table_counts(ticker):
    payload = parse_8k.extract(ticker)
    record = expected(ticker)["earnings_release"]["8-K"]
    assert len(payload["item_2_02"]["paragraphs"]) == record["exhibit_99_1_paragraphs"]
    assert len(payload["item_2_02"]["tables"]) == record["exhibit_99_1_tables"]
    assert payload["held_items"] == record["held_items"]


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_expected_counts_survive_an_independent_recount(ticker):
    """Strip the exhibit with the other parser and count; count `<table` by hand."""
    html = exhibit_html(ticker)
    record = expected(ticker)["earnings_release"]["8-K"]
    assert len(independent_text.block_paragraphs(html)) == record["exhibit_99_1_paragraphs"]
    assert len(re.findall(r"<table[\s>]", html, re.IGNORECASE)) == record["exhibit_99_1_tables"]


@pytest.mark.parametrize("ticker", TICKERS)
def test_every_release_paragraph_is_the_exhibits_own_text(ticker):
    payload = parse_8k.extract(ticker)
    missing = independent_text.Source(exhibit_html(ticker)).missing(
        payload["item_2_02"]["paragraphs"])
    assert not missing, f"{ticker}: {missing[:1]}"


@pytest.mark.parametrize("ticker", TICKERS)
def test_every_table_cell_is_the_exhibits_own_text(ticker):
    """A rendered row flattens whitespace, so the guarantee is asserted at the
    cell — which is where the numbers a reader would quote actually live."""
    payload = parse_8k.extract(ticker)
    source = independent_text.Source(exhibit_html(ticker))
    cells = [cell for table in payload["item_2_02"]["tables"]
             for row in table for cell in row if cell]
    assert cells
    missing = source.missing(cells)
    assert not missing, f"{ticker}: {missing[:3]}"


@pytest.mark.parametrize("ticker", TICKERS)
def test_release_paragraph_ids_are_dense(ticker):
    payload = parse_8k.extract(ticker)
    count = len(payload["item_2_02"]["paragraphs"])
    assert set(payload["item_2_02"]["paragraph_ids"]) == \
        {f"{payload['accession']}:8k_2_02:{index}" for index in range(1, count + 1)}


def test_an_item_string_is_split_into_codes_and_nothing_else():
    assert parse_8k.item_codes("2.02,9.01") == ["2.02", "9.01"]
    assert parse_8k.item_codes("2.02, 7.01, 9.01") == ["2.02", "7.01", "9.01"]
    assert parse_8k.item_codes("") == []
    assert parse_8k.item_codes(None) == []


CONSTRUCTED_8K = """
<html><body>
<p>UNITED STATES SECURITIES AND EXCHANGE COMMISSION</p>
<p>Item 4.02 Non-Reliance on Previously Issued Financial Statements.</p>
<p>On March 3, 2026, the Audit Committee concluded that the previously issued
financial statements for the year ended December 31, 2025 should no longer be
relied upon.</p>
<p>The Company intends to restate those financial statements.</p>
<p>Item 5.02 Departure of Directors or Certain Officers.</p>
<p>On March 4, 2026, the Chief Financial Officer resigned.</p>
<p>Item 9.01 Financial Statements and Exhibits.</p>
<p>(d) Exhibits.</p>
<p>SIGNATURES</p>
<p>Pursuant to the requirements of the Securities Exchange Act of 1934.</p>
</body></html>
"""


def test_a_non_reliance_body_is_carried_whole():
    items = parse_8k.body_items(CONSTRUCTED_8K)
    assert sorted(items) == ["4.02", "5.02", "9.01"]
    assert "should no longer be\nrelied upon" in items["4.02"]["text"]
    assert "intends to restate" in items["4.02"]["text"]
    # The next item's heading ends the previous item.
    assert "Chief Financial Officer" not in items["4.02"]["text"]
    # Signatures end the last item.
    assert "Securities Exchange Act of 1934" not in items["9.01"]["text"]


def test_only_the_four_named_items_go_in_verbatim(tmp_path):
    """9.01 is in the body and is not carried; 4.02 and 5.02 are."""
    items = parse_8k.body_items(CONSTRUCTED_8K)
    carried = [code for code in parse_8k.VERBATIM_ITEMS if code in items]
    assert carried == ["4.02", "5.02"]
    assert "9.01" not in parse_8k.VERBATIM_ITEMS


@pytest.mark.parametrize("ticker", TICKERS)
def test_no_fixture_8k_carries_a_verbatim_item(ticker):
    """Stated as a test so the day one does, this fails and is looked at."""
    payload = parse_8k.extract(ticker)
    assert payload["verbatim_items"] == {}, \
        f"{ticker} now files {sorted(payload['verbatim_items'])} — check the rendering"


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_rendered_file_carries_every_8k_and_its_codes(ticker):
    payload = parse_8k.extract(ticker)
    document = parse_8k.render(payload)
    for filing in payload["filings"]:
        assert filing["accession"] in document
    assert document.count("[") >= len(payload["item_2_02"]["paragraph_ids"])


def test_the_parser_goes_through_the_cutoff_gate():
    with pytest.raises(cutoff_guard.CutoffViolationError):
        parse_8k.extract("AAPL", cutoff=dt.date(2020, 1, 1))
