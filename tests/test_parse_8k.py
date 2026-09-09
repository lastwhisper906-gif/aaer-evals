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

import pytest

from src import cutoff_guard, parse_8k
from src.fetch_fixtures import TICKERS
from tests import independent_text
from tests.expected_values import value

CODE = re.compile(r"^\d+\.\d{2}$")
BAR = chr(124)


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
    assert len(filings) == \
        value(ticker, "earnings_release.8-K.eight_k_filings_in_the_index")
    for filing in filings:
        assert filing["items"], f"{ticker} {filing['accession']}: no item codes"
        for code in filing["items"]:
            assert CODE.match(code), f"{ticker} {filing['accession']}: {code!r}"


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_index_is_a_recount_of_the_stored_file(ticker):
    """Read the index with `json` and count the 8-Ks by hand."""
    row = cutoff_guard.one_document(ticker, "submissions", "submissions_index")
    raw = json.loads(cutoff_guard.load_document(row["full_path"], row["filing_date"]))
    # `8-K/A` is an 8-K. Selecting the string exactly is what kept every
    # amendment out of the list this recount is checking.
    by_hand = [row for row in raw["filings"] if row["form"] in ("8-K", "8-K/A")]
    assert len(by_hand) == \
        value(ticker, "earnings_release.8-K.eight_k_filings_in_the_index")
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
def test_the_release_table_count_and_item_codes(ticker):
    """The release arrives cleaned, one entry per prose paragraph and one per
    table holding all of its rows — the same stream the notes and the MD&A
    arrive in. It used to be rendered uncleaned while the manifest recorded the
    drops of a *second* cleaning of the same document, so 43 paragraphs across
    the fixture set were published as verbatim and recorded as excluded at once.
    """
    payload = parse_8k.extract(ticker)
    stream = payload["item_2_02"]["paragraphs"]
    tables = [entry for entry in stream if entry.startswith(BAR)]
    assert len(tables) == value(ticker, "earnings_release.8-K.exhibit_99_1_tables")
    assert payload["held_items"] == value(ticker, "earnings_release.8-K.held_items")


# Nine of the twelve exhibits carry page furniture or a safe-harbour disclaimer
# the cleaner leaves in. This is not a disagreement about where the line falls:
# each of these was read off the exhibit block by block, against the rule
# `docs/INPUT_SPEC.md:175` states — strip page numbers and boilerplate
# forward-looking disclaimers — and the blocks the cleaner keeps are bare page
# numerals sitting alone in footer divs, and safe-harbour paragraphs that say so
# in their first sentence. Two rules in `src/clean_text.py` are behind all nine:
#
#   `page_numbers` only drops a numeral in a run of increasing numerals at least
#   `PAGE_RUN_MIN_GAP` visible blocks apart, so a release whose footers cluster
#   near its tables keeps every one of them.
#
#   `drop_reason` requires `_FORWARD_LOOKING` *and* `_SAFE_HARBOUR` to match the
#   same block, so a disclaimer that writes "undertakes no duty" for "undertake
#   no duty", or "cause actual results to differ" for "actual results may
#   differ", or that a page break has split in two, is carried into the input.
#
# The expected values stand as the exhibits read. These are strict xfails, so the
# day either rule is fixed this file goes red and the marks come off — which is
# the point of recording them here rather than rounding the numbers to fit.
UNDER_DROPPED = {
    "CSCO": "16 bare page numerals (1-16) in footer divs are carried; 17 read, 1 dropped",
    "PANW": "5 bare page numerals and all 3 forward-looking blocks are carried; "
            "8 read, 0 dropped",
    "CARR": "18 bare page numerals (1-18) are carried; 20 read, 2 dropped",
    "LFUS": "both paragraphs of the Safe Harbor section are carried and its heading "
            "is dropped instead; 13 read, 12 dropped",
    "GNRC": "10 of 12 bare page numerals and 3 of 4 forward-looking blocks are "
            "carried; 16 read, 2 dropped",
    "CIEN": "4 of 10 bare page numerals and 2 of 3 safe-harbour blocks are carried; "
            "13 read, 7 dropped",
    "ESE": "the second safe-harbour paragraph writes 'undertakes no duty' and "
           "'actual results in the future may differ'; 2 read, 1 dropped",
    "TTMI": "the safe-harbour paragraph writes 'actual events or results may differ' "
            "and 'does not undertake to update'; 1 read, 0 dropped",
    "NVDA": "a page break splits the forward-looking paragraph and only the half "
            "carrying 'within the meaning of' is dropped; 2 read, 1 dropped",
}


@pytest.mark.parametrize("ticker", [
    pytest.param(ticker, marks=pytest.mark.xfail(
        strict=True, reason=f"{ticker}: {UNDER_DROPPED[ticker]}"))
    if ticker in UNDER_DROPPED else ticker
    for ticker in TICKERS])
def test_the_cleaner_drops_the_blocks_the_exhibit_says_are_droppable(ticker):
    """Every block outside a table is carried or dropped, and each exhibit was
    read by eye to say which. So the carried count is the subtraction, not a
    number of its own — recording it separately would have made the independent
    recount below an identity instead of a check."""
    payload = parse_8k.extract(ticker)
    blocks = value(ticker, "earnings_release.8-K.exhibit_99_1_blocks_outside_tables")
    dropped = value(ticker, "earnings_release.8-K.exhibit_99_1_dropped")
    stream = payload["item_2_02"]["paragraphs"]
    tables = [entry for entry in stream if entry.startswith(BAR)]
    assert len(payload["item_2_02"]["dropped"]) == dropped
    assert len(stream) - len(tables) == blocks - dropped


TABLE_BLOCK = re.compile(r"<table\b.*?</table\s*>", re.DOTALL | re.IGNORECASE)
CELL = re.compile(r"<t[dh]\b.*?</t[dh]\s*>", re.DOTALL | re.IGNORECASE)


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_expected_counts_survive_an_independent_recount(ticker):
    """The recorded counts, re-derived from the exhibit by two measures that
    import nothing from `src/`.

    Prose: block-split the exhibit with `tests/independent_text.py` after
    deleting every `<table>` region, so a table cell cannot be counted as a
    paragraph. That block count is the recorded value, measured the same way and
    written down — not recomputed on both sides of the assertion. The split of
    those blocks into carried and dropped is pinned separately, by the drop
    enumeration somebody read off the exhibit one block at a time.

    Tables: a bare regex for `<table>` elements holding at least one cell with a
    character in it.
    """
    html = exhibit_html(ticker)

    outside_tables = TABLE_BLOCK.sub("\n<p></p>\n", html)
    blocks = [block for block in independent_text.block_paragraphs(outside_tables)
              if independent_text.flat(block)]
    assert len(blocks) == \
        value(ticker, "earnings_release.8-K.exhibit_99_1_blocks_outside_tables")

    tables = 0
    for block in TABLE_BLOCK.findall(html):
        if any(independent_text.flat(independent_text.strip(cell))
               for cell in CELL.findall(block)):
            tables += 1
    assert tables == value(ticker, "earnings_release.8-K.exhibit_99_1_tables")


@pytest.mark.parametrize("ticker", TICKERS)
def test_every_release_drop_is_a_page_number_or_forward_looking_boilerplate(ticker):
    """31 drops across the twelve exhibits, and every one of them is one of the
    two reasons an earnings release may lose a paragraph for.

    This is the direction that still holds: nothing the cleaner drops here is
    anything but page furniture or a safe-harbour paragraph, so no release
    content is being deleted. The other direction — that it drops *everything*
    those two reasons cover — is where nine of the twelve fail, and that is
    recorded above rather than here."""
    dropped = parse_8k.extract(ticker)["item_2_02"]["dropped"]
    reasons = {drop["reason"] for drop in dropped}
    assert reasons <= {"page_number", "forward_looking_boilerplate"}, f"{ticker}"


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
    cells = [cell.strip()
             for entry in payload["item_2_02"]["paragraphs"] if entry.startswith(BAR)
             for row in entry.split("\n") for cell in row.split(BAR) if cell.strip()]
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


# --- amendments and late filings --------------------------------------------
#
# `form == "8-K"` exactly, so no `8-K/A` reached the item-code list
# `docs/INPUT_SPEC.md:28` promises and no NT filing reached anything. Both come
# from the already-stored `submissions.json`; neither needs a fetch.

@pytest.mark.parametrize("ticker", TICKERS)
def test_an_amendment_is_in_the_list_and_says_it_is_one(ticker):
    raw = json.loads(cutoff_guard.load_index(cutoff_guard.one_document(
        ticker, "submissions", "submissions_index")["full_path"]))
    by_hand = {row["accession"] for row in raw["filings"] if row["form"] == "8-K/A"}
    listed = {row["accession"] for row in parse_8k.eight_k_filings(raw)
              if row["amendment"]}
    assert listed == by_hand, ticker
    for row in parse_8k.eight_k_filings(raw):
        assert row["amendment"] == (row["form"] == "8-K/A")


def test_ttmis_amendment_names_the_filing_it_amends():
    """TTMI filed its earnings release and an amendment of it on 2026-08-06.
    The index has no `amends` field; both carry report date 2026-08-05, and
    exactly one 8-K does, so the amendment can name it."""
    raw = json.loads(cutoff_guard.load_index(cutoff_guard.one_document(
        "TTMI", "submissions", "submissions_index")["full_path"]))
    rows = {row["accession"]: row for row in parse_8k.eight_k_filings(raw)}
    amendment = rows["0001193125-26-337923"]
    assert amendment["amendment"] is True
    assert amendment["items"] == ["2.02", "9.01"]
    assert amendment["amends"] == "0001193125-26-336163"
    assert rows["0001193125-26-336163"]["items"] == ["2.02", "9.01"]


def test_the_amendment_is_outside_ttmis_own_bundles_because_of_the_cutoff():
    """It was filed 2026-08-06 and TTMI's 10-Q on 2026-08-05, so neither the
    amendment nor the 8-K it amends may enter that bundle. The cutoff outranks
    the wish to see it: `CLAUDE.md` — nothing filed after the triggering report
    enters the input."""
    raw = json.loads(cutoff_guard.load_index(cutoff_guard.one_document(
        "TTMI", "submissions", "submissions_index")["full_path"]))
    listed = {row["accession"]
              for row in parse_8k.eight_k_filings(raw, "2026-08-05")}
    assert "0001193125-26-337923" not in listed
    assert "0001193125-26-336163" not in listed
    assert "0001193125-26-337923" in {
        row["accession"] for row in parse_8k.eight_k_filings(raw, "2026-08-06")}


def test_littelfuses_late_filing_notice_is_on_the_list():
    """`docs/CHECKLIST.md:67` names an NT 10-K a filing irregularity. LFUS filed
    one on 2025-02-27 for the year ended 2024-12-28."""
    raw = json.loads(cutoff_guard.load_index(cutoff_guard.one_document(
        "LFUS", "submissions", "submissions_index")["full_path"]))
    late = parse_8k.late_filings(raw)
    assert [row["accession"] for row in late] == ["0001140361-25-006294"]
    assert late[0]["form"] == "NT 10-K"
    assert late[0]["report_date"] == "2024-12-28"
    assert not parse_8k.late_filings(raw, "2025-02-26")


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_late_filing_list_is_a_recount_of_the_stored_file(ticker):
    raw = json.loads(cutoff_guard.load_index(cutoff_guard.one_document(
        ticker, "submissions", "submissions_index")["full_path"]))
    by_hand = [row for row in raw["filings"]
               if row["form"] in ("NT 10-K", "NT 10-Q", "NT 10-K/A", "NT 10-Q/A")]
    assert {row["accession"] for row in by_hand} == \
        {row["accession"] for row in parse_8k.late_filings(raw)}
