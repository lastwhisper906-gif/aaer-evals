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

# Form 8-K numbered its items 1 to 12 until the SEC's amended form took effect
# on 2004-08-23 (Release 33-8400), and EDGAR's index keeps an older row's items
# in that numbering. NAPCO's index is the one here that reaches back past the
# change: 19 8-K rows filed 1998-05-15 to 2004-08-10 carry '5,7', '2,7', '4,7'
# or '4' -- {'accession': '0000950123-04-009506', 'filing_date': '2004-08-10',
# 'form': '8-K', 'items': '5,7'} is the last of them in
# tests/fixtures/NSSC/submissions.json -- and its next 8-K,
# 0000950123-04-011016 filed 2004-09-15, carries '2.02,9.01'. Every other
# company's index holds no 8-K filed before the change.
#
# The code-shape test below reads every code in the numbering since the change,
# as it was written, and NAPCO's old rows are not in it, so its case is a
# strict expected failure. It is not a parser defect: the parser splits each of
# these rows as the index writes it. What disagrees is the shape the test holds
# them to, and whether that shape should read the earlier numbering is left as
# needs judgment, with the rule as written as the default; a change to the rule
# or to the index turns the mark red. A strict mark covers the whole case, and
# the parser returns the newest row first, so NAPCO's later rows are read before
# its first old row fails the case and the 18 older ones are never reached; the
# test after it asserts, unmarked, everything the mark would hide.
NEW_NUMBERING_FROM = "2004-08-23"
OLD_NUMBERING = {
    "NSSC": "19 8-K rows filed 1998-05-15 to 2004-08-10 carry their items in Form "
            "8-K's numbering before 2004-08-23, a bare number: '5,7' on "
            "0000950123-04-009506, '4,7' on 0000950123-03-014035, '4' on "
            "0000950123-02-006856, and '2,7' on 0000950123-00-007499 and its 8-K/A",
}
# Each of those rows, as tests/fixtures/NSSC/submissions.json writes its
# accession, its items and its filing date.
ROWS_IN_THE_OLD_NUMBERING = {
    "NSSC": {
        "0000950123-98-005157": "5,7",  # 1998-05-15
        "0000950123-98-005484": "5,7",  # 1998-05-29
        "0000950123-00-007499": "2,7",  # 2000-08-11
        "0000950123-00-008897": "2,7",  # 2000-09-27, 8-K/A
        "0000950123-01-002241": "5,7",  # 2001-03-13
        "0000950123-02-006856": "4",  # 2002-07-10
        "0000950123-03-011361": "5,7",  # 2003-10-14
        "0000950123-03-011419": "5,7",  # 2003-10-16
        "0000950123-03-014035": "4,7",  # 2003-12-22
        "0000950123-03-014218": "5,7",  # 2003-12-29
        "0000950123-04-000206": "5,7",  # 2004-01-09
        "0000950123-04-001403": "5,7",  # 2004-02-09
        "0000950123-04-001895": "5,7",  # 2004-02-17
        "0000950123-04-002204": "5,7",  # 2004-02-23
        "0000950123-04-003956": "5,7",  # 2004-03-30
        "0000950123-04-005875": "5,7",  # 2004-05-06
        "0000950123-04-006950": "5,7",  # 2004-05-28
        "0000950123-04-007011": "5,7",  # 2004-06-02
        "0000950123-04-009506": "5,7",  # 2004-08-10
    },
}


def exhibit_html(ticker: str) -> str:
    row = cutoff_guard.one_document(ticker, "8-K", "exhibit_99_1")
    return cutoff_guard.load_document(row["full_path"], row["filing_date"])


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_stored_8k_carries_item_2_02(ticker):
    """The fixture selection and the parser have to agree on what a code is."""
    row = cutoff_guard.one_document(ticker, "8-K", "primary_html")
    assert "2.02" in parse_8k.item_codes(row["items"])


@pytest.mark.parametrize("ticker", [
    pytest.param(ticker, marks=pytest.mark.xfail(
        strict=True, reason=f"{ticker}: {OLD_NUMBERING[ticker]}"))
    if ticker in OLD_NUMBERING else ticker
    for ticker in TICKERS])
def test_the_index_reports_8ks_and_every_code_is_a_code(ticker):
    filings = parse_8k.eight_k_filings(parse_8k.submissions(ticker))
    assert filings, f"{ticker}: no 8-K in the stored submissions index"
    assert len(filings) == \
        value(ticker, "earnings_release.8-K.eight_k_filings_in_the_index")
    for filing in filings:
        assert filing["items"], f"{ticker} {filing['accession']}: no item codes"
        for code in filing["items"]:
            assert CODE.match(code), f"{ticker} {filing['accession']}: {code!r}"


@pytest.mark.parametrize("ticker", sorted(ROWS_IN_THE_OLD_NUMBERING))
def test_an_index_reaching_past_the_renumbering_reads_the_new_codes_after_it(ticker):
    """What the mark above would hide in NAPCO's case, asserted unmarked: the
    count of 8-Ks, an item on every row, every code of every row filed from
    2004-08-23 on in the numbering since, and before that date exactly the rows
    read off the index, each with the items it carries."""
    filings = parse_8k.eight_k_filings(parse_8k.submissions(ticker))
    assert len(filings) == \
        value(ticker, "earnings_release.8-K.eight_k_filings_in_the_index")
    for filing in filings:
        assert filing["items"], f"{ticker} {filing['accession']}: no item codes"
        if filing["filing_date"] >= NEW_NUMBERING_FROM:
            for code in filing["items"]:
                assert CODE.match(code), f"{ticker} {filing['accession']}: {code!r}"
    earlier = {filing["accession"]: ",".join(filing["items"]) for filing in filings
               if filing["filing_date"] < NEW_NUMBERING_FROM}
    assert earlier == ROWS_IN_THE_OLD_NUMBERING[ticker]


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
# `docs/INPUT_SPEC.md` §2 item 1 states — strip page numbers and boilerplate
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
# The expected values stand as the exhibits read. These are strict xfails, so a
# fixed rule turns them red and the marks come off — which is the point of
# recording them rather than rounding the numbers to fit. PANW, GNRC and CIEN miss
# on both rules at once, so fixing one of the two leaves those three still
# xfailing; the count in each reason says how far each has to move.
#
# The mark covers one assertion and no more. `carried + dropped == the blocks the
# exhibit holds` is true of all twelve however badly the cleaner draws the line,
# so it is a live test above and no company's is skipped: a strict xfail is
# satisfied by any failure, and an assertion sharing a test with a known-failing
# one is an assertion nobody evaluates.
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
    # The eight added on 2026-10-07, read the same way; POWL's one safe-harbour
    # paragraph is dropped and its pages carry no numerals, so it is not here.
    "DELL": "9 of 16 bare page numerals and 5 of the 6 blocks of the 'Special Note "
            "on Forward-Looking Statements' are carried; 22 read, 8 dropped",
    "WDC": "13 of 14 bare page numerals and the disclaimer's heading are carried; "
           "16 read, 2 dropped",
    "ANET": "3 of 8 bare page numerals and both blocks of the disclaimer are carried; "
            "10 read, 5 dropped",
    "FTNT": "the disclaimer's heading and its opening paragraph are carried, and a "
            "one-sentence pointer inside the guidance is dropped instead; "
            "3 read, 2 dropped",
    "JCI": "all 20 bare page numerals and the disclaimer's heading are carried; "
           "22 read, 1 dropped",
    "FELE": "the heading and the page-broken second half of the safe-harbour "
            "paragraph are carried; 3 read, 1 dropped",
    "FN": "the disclaimer's heading is carried; 2 read, 1 dropped",
    # The next eight, added the same day under the continued rule, read the
    # same way. Every one of them is here: five print no page numerals, and the
    # cleaner keeps part of their disclaimer -- its heading, its second
    # paragraph or its page-broken second half; Motorola, Broadcom and Sandisk
    # print runs of numerals too, and the cleaner keeps most or all of them.
    "MSI": "17 of 19 bare page numerals, the disclaimer's heading and its page-broken "
           "continuation are carried; 22 read, 3 dropped",
    "LITE": "the disclaimer's heading is carried; 2 read, 1 dropped",
    "FLEX": "the disclaimer's heading and its second paragraph are carried; "
            "3 read, 1 dropped",
    "AVGO": "all 5 bare page numerals and 4 of the 5 blocks of the cautionary note "
            "are carried; 10 read, 1 dropped",
    "SMCI": "the disclaimer's heading is carried; 2 read, 1 dropped",
    "SNDK": "12 of 13 bare page numerals and the disclaimer's heading are carried; "
            "15 read, 2 dropped",
    "FFIV": "the disclaimer's heading and its page-broken second half are carried; "
            "3 read, 1 dropped",
    "LOGI": "the page-broken second half of the disclaimer is carried; "
            "2 read, 1 dropped",
    # The third eight, added the same day under the rule read as current
    # filers, read the same way. Every one of them is here too: the cleaner
    # keeps part of each disclaimer, and UI, AMD and OMCL print bare page
    # numerals it keeps. NSSC's disclaimer is carried whole, and the 13 blocks
    # the cleaner does drop from its release are its blocks of a lone
    # zero-width space, none of the 43 read (INVISIBLE_BLOCKS below), so the
    # test counts 13 drops against the 2 the exhibit says are droppable.
    "LII": "the heading 'FORWARD-LOOKING STATEMENTS & NON-GAAP FINANCIAL MEASURES' "
           "and the paragraph 'For information concerning these and other risks and "
           "uncertainties' are carried; 3 read, 1 dropped",
    "AMSC": "the heading 'Forward-Looking Statements' is carried; 2 read, 1 dropped",
    "UI": "the safe-harbour paragraphs 'Forward-looking statements are subject to "
          "certain risks and uncertainties' and 'Given these uncertainties, you should "
          "not place undue reliance' and the bare page numeral '1' are carried; "
          "5 read, 2 dropped",
    "NSSC": "the heading 'Safe Harbor Statement' and its one paragraph 'This press "
            "release contains forward-looking statements that are based on current "
            "expectations' are carried, and the 13 blocks dropped are its blocks of a "
            "lone zero-width space, none of them read; 2 read, 13 dropped, neither of "
            "the 2 among them",
    "CLS": "the heading 'Cautionary Note Regarding Forward-looking Statements' and six "
           "of its seven paragraphs, its page-broken continuation 'alignment of our "
           "capacity with our business demands' among them, are carried; "
           "8 read, 1 dropped",
    "AMD": "10 of 12 bare page numerals, the outlook disclaimer 'The following "
           "statements are forward-looking and actual results could differ materially' "
           "and the heading 'Cautionary Statement' are carried; 15 read, 3 dropped",
    "OMCL": "5 of 13 bare page numerals, the heading 'Forward-Looking Statements' and "
            "the paragraphs 'Such statements include, but are not limited to' and "
            "'Actual results and other events may differ significantly' are carried; "
            "18 read, 10 dropped",
    "NTAP": "the second paragraph 'Actual results may differ materially from these "
            "statements' is carried; 3 read, 2 dropped",
}

# What a reader can see, written here rather than read from the cleaner: a
# character that is neither whitespace nor one of the zero-width characters a
# filer pads a paragraph with. Every release's note counts "blocks with visible
# text"; `independent_text.flat` keeps a block that holds anything but
# whitespace, and the two part only on a block of nothing but a zero-width
# character, which is not whitespace to Python.
INVISIBLE = "\u200b\u200c\u200d\u2060\ufeff"


def visible(text: str) -> bool:
    """Does the text hold a character a reader would see?"""
    return any(not (character.isspace() or character in INVISIBLE) for character in text)


def drops_of_text(payload: dict) -> list[dict]:
    """The release's drops a reader could have read: the paragraphs it lost."""
    return [drop for drop in payload["item_2_02"]["dropped"] if visible(drop["text"])]


# NAPCO's release separates its sections with 13 paragraphs that hold a lone
# zero-width space, U+200B, and nothing else -- the 6th, 8th, 11th, 20th, 24th,
# 28th, 32nd, 33rd, 34th, 38th, 43rd, 48th and 49th of the 56 blocks `flat`
# leaves non-empty outside the tables of 8-K/nssc-20260820xex99d1.htm, the first
# between 'Fourth Quarter 2026 Financial Results as Compared to Fourth Quarter
# 2025' and 'Full Year 2026 Financial Results as Compared to Full Year 2025'.
# `flat` keeps each of them, and the cleaner splits each as a paragraph and drops
# it as `empty`. A reader sees 43 blocks there, which is what NAPCO's note
# records, as every release's note counts blocks with visible text; the other
# thirty-five releases hold no such block and count the same either way.
#
# The three tests below that count every block `flat` keeps and every drop the
# cleaner lists, and hold every drop to the two reasons, read as they were
# written, so NAPCO's case of each is a strict expected failure: 43 carried and
# 13 dropped make 56 against the 43 read, the recount splits 56, and `empty` is
# neither of the two reasons. Whether a block of nothing but invisible
# characters is a block of a release, and its drop a third reason, is left as
# needs judgment (`docs/needs_judgment.md`), the tests as written being the
# default. What the marks hide is asserted, unmarked, by the two tests after
# them: the sum and the recount by what a reader sees, the table count, the two
# reasons over every drop with visible text, and `empty` over the 13. Strict, so
# a cleaner that no longer lists these blocks among its drops turns the first
# and the third red, and a recount that no longer keeps them the second.
INVISIBLE_BLOCKS = {
    "NSSC": "13 of the 56 blocks outside its tables are a lone zero-width space "
            "(U+200B), the first between 'Fourth Quarter 2026 Financial Results as "
            "Compared to Fourth Quarter 2025' and 'Full Year 2026 Financial Results as "
            "Compared to Full Year 2025', and the cleaner drops each as 'empty'; "
            "43 read, 56 split",
}


@pytest.mark.parametrize("ticker", [
    pytest.param(ticker, marks=pytest.mark.xfail(
        strict=True, reason=f"{ticker}: {INVISIBLE_BLOCKS[ticker]}"))
    if ticker in INVISIBLE_BLOCKS else ticker
    for ticker in TICKERS])
def test_every_block_outside_a_table_is_carried_or_dropped(ticker):
    """The segmentation, pinned for all twelve with no parser number in it.

    A block of the exhibit is either in the release or in the drop list, so the
    two have to add up to the block count somebody counted off the exhibit — and
    that count is the recorded value, measured by `tests/independent_text` and
    re-derived below. This holds whether or not the cleaner draws the line in the
    right place, which is why it is here and not behind the mark: without it
    nothing at all would pin the carried paragraph count of nine of the twelve
    releases, and the parser could emit no prose for CSCO and stay green.
    """
    payload = parse_8k.extract(ticker)
    stream = payload["item_2_02"]["paragraphs"]
    tables = [entry for entry in stream if entry.startswith(BAR)]
    carried = len(stream) - len(tables)
    assert carried + len(payload["item_2_02"]["dropped"]) == \
        value(ticker, "earnings_release.8-K.exhibit_99_1_blocks_outside_tables")


@pytest.mark.parametrize("ticker", [
    pytest.param(ticker, marks=pytest.mark.xfail(
        strict=True, reason=f"{ticker}: {UNDER_DROPPED[ticker]}"))
    if ticker in UNDER_DROPPED else ticker
    for ticker in TICKERS])
def test_the_cleaner_drops_the_blocks_the_exhibit_says_are_droppable(ticker):
    """One assertion: the drop count each exhibit was read by eye to justify.

    The carried count is the subtraction of this from the block count, so it is
    not recorded separately — that would have made the recount below an identity
    instead of a check.
    """
    assert len(parse_8k.extract(ticker)["item_2_02"]["dropped"]) == \
        value(ticker, "earnings_release.8-K.exhibit_99_1_dropped")


TABLE_BLOCK = re.compile(r"<table\b.*?</table\s*>", re.DOTALL | re.IGNORECASE)
CELL = re.compile(r"<t[dh]\b.*?</t[dh]\s*>", re.DOTALL | re.IGNORECASE)


@pytest.mark.parametrize("ticker", [
    pytest.param(ticker, marks=pytest.mark.xfail(
        strict=True, reason=f"{ticker}: {INVISIBLE_BLOCKS[ticker]}"))
    if ticker in INVISIBLE_BLOCKS else ticker
    for ticker in TICKERS])
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
def test_a_drop_with_nothing_visible_in_it_is_an_empty_block_of_the_exhibit(ticker):
    """The drops NAPCO's marks are about, held on both sides, over every release.

    Whatever the cleaner drops with no visible character in it, it drops as
    `empty`; nothing it drops as `empty` holds a visible character, so that
    reason cannot carry away a word of a release; and there are as many of them
    as the exhibit holds blocks of nothing but invisible characters, by the
    split above -- NAPCO's 13, and none in the other thirty-five releases, whose
    cases of the segmentation sum and the recount above and of the reasons
    below pass as written; the drop count between them is UNDER_DROPPED's."""
    dropped = parse_8k.extract(ticker)["item_2_02"]["dropped"]
    unseen = [drop for drop in dropped if not visible(drop["text"])]
    assert all(drop["reason"] == "empty" for drop in unseen), f"{ticker}"
    assert not [drop for drop in dropped
                if drop["reason"] == "empty" and visible(drop["text"])], \
        f"{ticker}: a drop with visible text is called empty"
    outside_tables = TABLE_BLOCK.sub("\n<p></p>\n", exhibit_html(ticker))
    blank = [block for block in independent_text.block_paragraphs(outside_tables)
             if independent_text.flat(block) and not visible(block)]
    assert len(unseen) == len(blank), \
        f"{ticker}: {len(unseen)} dropped with nothing visible, {len(blank)} in the exhibit"


@pytest.mark.parametrize("ticker", [
    pytest.param(ticker, marks=pytest.mark.xfail(
        strict=True, reason=f"{ticker}: {INVISIBLE_BLOCKS[ticker]}"))
    if ticker in INVISIBLE_BLOCKS else ticker
    for ticker in TICKERS])
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


@pytest.mark.parametrize("ticker", sorted(INVISIBLE_BLOCKS))
def test_what_the_marks_on_a_release_with_invisible_blocks_hide_holds_for_what_is_seen(
        ticker):
    """What INVISIBLE_BLOCKS' three marks hide in NAPCO's case, asserted
    unmarked: the segmentation sum and the recount, by the blocks with visible
    text the note reads; the table count, the recount's second assertion, which
    its first stops before; and the two reasons over every drop a reader could
    have read. The drops with nothing visible in them are the test above's."""
    read = value(ticker, "earnings_release.8-K.exhibit_99_1_blocks_outside_tables")
    payload = parse_8k.extract(ticker)
    stream = payload["item_2_02"]["paragraphs"]
    carried = len([entry for entry in stream if not entry.startswith(BAR)])
    assert carried + len(drops_of_text(payload)) == read

    html = exhibit_html(ticker)
    outside_tables = TABLE_BLOCK.sub("\n<p></p>\n", html)
    blocks = [block for block in independent_text.block_paragraphs(outside_tables)
              if visible(block)]
    assert len(blocks) == read

    tables = 0
    for block in TABLE_BLOCK.findall(html):
        if any(independent_text.flat(independent_text.strip(cell))
               for cell in CELL.findall(block)):
            tables += 1
    assert tables == value(ticker, "earnings_release.8-K.exhibit_99_1_tables")

    reasons = {drop["reason"] for drop in drops_of_text(payload)}
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


# Read off the submissions index by hand. Fabrinet's stored 8-K, accession
# 0001408710-26-000026 filed 2026-08-17, is the one row of
# tests/fixtures/FN/submissions.json with that accession and carries items
# "1.01,2.02,2.03,5.02,9.01"; 1.01 (the credit-facility amendment and term loan)
# and 5.02 (the executive incentive plan) are two of the four items
# docs/INPUT_SPEC.md carries verbatim, 2.02 is the release, and 2.03 and 9.01 are
# not carried. No other company's stored 8-K carries a verbatim item: the twelve's
# rows all read "2.02,9.01" and POWL's "2.02,8.01,9.01". Of the third eight, read
# off each stored 8-K's submissions row the same way: AMSC's
# 0001437749-26-025921 reads "2.02,5.07,9.01", UI's 0001511737-26-000057
# "2.02,8.01,9.01", NSSC's 0001104659-26-100077 and AMD's 0000002488-26-000121
# "2.02,7.01,9.01", and LII's, CLS's, OMCL's and NTAP's "2.02,9.01"; a vote
# (5.07), Regulation FD (7.01) and other events (8.01) are not carried verbatim.
VERBATIM_ON_RECORD = {"FN": ["1.01", "5.02"]}


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_fixture_8ks_carry_the_verbatim_items_their_index_rows_name(ticker):
    """Stated as a test so the day a new one does, this fails and is looked at."""
    payload = parse_8k.extract(ticker)
    assert sorted(payload["verbatim_items"]) == VERBATIM_ON_RECORD.get(ticker, []), \
        f"{ticker} now files {sorted(payload['verbatim_items'])} — check the rendering"
    for code, item in payload["verbatim_items"].items():
        assert code in parse_8k.VERBATIM_ITEMS
        assert item["paragraphs"][0].startswith(f"Item {code}")


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
