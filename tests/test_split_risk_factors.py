"""Item 1A, cut at the right heading, and only its diff carried forward.

Two claims are held to something outside the splitter, and they are the two
this section can get wrong. A third group of tests holds no claim of this
item's: it records, against the filings, what the shared cleaner does when it
is handed a section instead of a document. Both of those are adverse and
neither is this item's to move, so they are written down rather than left to be
rediscovered — see the note under *the cleaner, handed a section rather than a
document*.

**Where the section starts and stops.** Recorded per company as the heading the
section opens at and the heading it ends before — two lines a reader can find in
the document — read off all twelve 10-Ks *and* all twelve 10-Qs through
`tests/independent_text.py` and nothing from `src/`. Both forms, because the
10-Q is the form the diff actually runs on: every 10-K here is carried whole for
want of a prior year, so a 10-K-only record would hold the boundary on the one
form whose boundary the reader never sees moved. Esterline's 10-Q carries no
Item 1A at all, and that absence is recorded as `null` rather than skipped, so
the claim is twelve of twelve on both forms with no test that quietly does
nothing. A count cannot make this claim: a splitter that took the
table-of-contents entry would return three lines of index and still have a
paragraph total to agree with, and `docs/INPUT_SPEC.md` §1 carries Item 1A as a
diff, where a boundary that slipped does not show up as an empty section — it
shows up as a page of risk factors the prior period does not have.

**That a reordered section is no change.** `docs/INPUT_SPEC.md` §2 asks for it
in as many words: *a reordered or retitled section yields zero changes*. The
fixture in `tests/fixtures/reordered_risk_factors/` is one document and a copy
of it whose eight risk factors are in a different order, and the copy is a
permutation of the original's own bytes — which this file proves before it asks
the splitter anything, by splitting both documents on their delimiters and
comparing the blocks. Zero is then the expected value by construction: a
multiset has the same members however it is ordered, so nothing was added and
nothing removed. A test that only asserted zero would pass on a diff that
always says zero, so the same pair is edited in one word here and the diff has
to report that one and no other.
"""

from __future__ import annotations

import datetime as dt
import functools
import re

import pytest

from src import clean_text, cutoff_guard, html_text, split_sections
from src.fetch_fixtures import TICKERS
from tests import independent_text
from tests.expected_values import value

FIXTURE = cutoff_guard.FIXTURES / "reordered_risk_factors"
DELIMITER = "<!-- risk factor -->"
# The first line of the section that follows the eight blocks. Splitting there
# keeps the trailing document out of the last block.
AFTER_THE_BLOCKS = "<div><b>Item 1B."
PARAGRAPH_ID = re.compile(r"^\[([\w.\-]+:risk_factors:\d+)\]$", re.MULTILINE)
# A page tail as the filings print it: a bare number, or one between dashes.
PAGE_TAIL = re.compile(r"[-–—]?\s*\d{1,3}\s*[-–—]?")


@functools.lru_cache(maxsize=None)
def source_html(ticker: str, form: str) -> str:
    row = cutoff_guard.one_document(ticker, form, "primary_html")
    return cutoff_guard.load_document(row["full_path"], row["filing_date"])


@functools.lru_cache(maxsize=None)
def stripped(ticker: str, form: str) -> str:
    return html_text.strip_tags(source_html(ticker, form))


@functools.lru_cache(maxsize=None)
def section(ticker: str, form: str) -> dict:
    return split_sections.extract(ticker, form, "risk_factors")


@functools.lru_cache(maxsize=None)
def diffed(ticker: str, form: str) -> dict:
    return split_sections.risk_factors(ticker, form)


def written_lines(text: str, offset: int):
    """Every line with anything on it from `offset`, flattened, as (start, line).

    `normalized_spacing`, not `normalized`: the twelve write their headings in
    three different casings and the recorded line is the filing's own.
    """
    for start, end in html_text.lines(text):
        line = html_text.normalized_spacing(text[start:end].replace("​", ""))
        if start >= offset and line:
            yield start, line


def one_line(text: str, offset: int) -> str:
    """The first line with anything on it at or after `offset`."""
    return next((line for _, line in written_lines(text, offset)), "")


def what_follows(text: str, offset: int) -> str:
    """The first line after this heading that is not the section's own title.

    CSCO and four others put the item marker and the title in adjacent cells, so
    `Risk Factors` can be a line of its own between the heading and whatever
    comes next. What comes next is the discriminator: under a table-of-contents
    entry it is the page number, and under the section it is the section.
    """
    return next((line for start, line in written_lines(text, offset)
                 if start > offset and html_text.normalized(line) != "risk factors"),
                "")


def skip_where_the_filing_omits_the_item(ticker: str, form: str) -> None:
    """The one filing in the set with no Item 1A. Its own test holds that fact."""
    if ticker == "ESE" and form == "10-Q":
        pytest.skip("ESE's 10-Q carries no Item 1A; its own test says so")


# --- where the section starts and stops ------------------------------------


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form", ("10-K", "10-Q"))
def test_the_section_begins_and_ends_at_the_headings_the_filing_carries(ticker, form):
    """Both recorded lines, against both forms, for all twelve companies.

    A recorded `null` is the reading that there is no such heading in the
    document, and it is asserted rather than skipped: the splitter has to raise
    where the filing carries no Item 1A, because a section quietly returning
    nothing is the failure `SectionNotFound` exists to prevent.
    """
    opens_at = value(ticker, f"risk_factors.{form}.opens_at")
    ends_before = value(ticker, f"risk_factors.{form}.ends_before")
    text = stripped(ticker, form)

    if opens_at is None:
        assert ends_before is None
        with pytest.raises(split_sections.SectionNotFound):
            split_sections.bounds(text, form, "risk_factors")
        return

    start, stop, _, _ = split_sections.bounds(text, form, "risk_factors")
    assert one_line(text, start) == opens_at
    assert one_line(text, stop) == ends_before


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form", ("10-K", "10-Q"))
def test_the_table_of_contents_entry_is_not_the_one_selected(ticker, form):
    """The trap, made explicit: the index names Item 1A before the section does.

    Held on what *follows* each candidate rather than on the candidate's own
    words, because for CARR, CIEN and TTMI the index line and the body heading
    are the same string to the byte — so a recorded heading text cannot tell
    them apart, and a test that compared only that would pass on the wrong one.
    An index entry is followed by its page number; the section is followed by
    the section.
    """
    skip_where_the_filing_omits_the_item(ticker, form)
    text = stripped(ticker, form)
    spec = split_sections.SECTIONS[(form, "risk_factors")]
    candidates = split_sections.headings(text, spec)
    start, stop, _, rule = split_sections.bounds(text, form, "risk_factors")
    assert rule == "last candidate"
    assert start == candidates[-1][0]
    if len(candidates) == 1:
        return

    assert PAGE_TAIL.fullmatch(what_follows(text, candidates[0][0])), \
        "the first candidate should be the index entry, with its page number under it"
    assert not PAGE_TAIL.fullmatch(what_follows(text, start)), \
        "the selected heading should be followed by the section, not by a page number"

    # A quarterly Item 1A can be one sentence saying nothing changed, so the
    # length of what the index entry would have returned says nothing there. On
    # the annual it does: what the first match would have produced is the same
    # end rule applied from the index entry, stopping at the index's Item 1B.
    if form == "10-K":
        ends = [re.compile(pattern) for pattern in spec["end"]]
        from_index = candidates[0][0]
        index_stop = next(
            (line_start for line_start, line_end in html_text.lines(text)
             if line_start > from_index
             and any(end.search(html_text.normalized(text[line_start:line_end]))
                     for end in ends)),
            len(text))
        assert index_stop - from_index < (stop - start) / 10, \
            "the first match should be a line or two of index, not a section"


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form", ("10-K", "10-Q"))
def test_the_section_is_never_empty_where_the_filing_carries_it(ticker, form):
    skip_where_the_filing_omits_the_item(ticker, form)
    payload = section(ticker, form)
    assert payload["paragraphs"], f"{ticker} {form} risk factors came out empty"
    assert payload["text"].strip()


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form", ("10-K", "10-Q"))
def test_every_paragraph_is_the_filings_own_text(ticker, form):
    skip_where_the_filing_omits_the_item(ticker, form)
    payload = section(ticker, form)
    canonical = stripped(ticker, form)
    for paragraph in payload["paragraphs"]:
        assert paragraph in canonical
    missing = independent_text.Source(source_html(ticker, form)).missing(
        payload["paragraphs"])
    assert not missing, f"{ticker} {form}: {missing[:1]}"


def foreign_headings(form: str) -> list[re.Pattern]:
    """Every item heading the splitter knows except this section's own."""
    spec = split_sections.SECTIONS[(form, "risk_factors")]
    own = set(spec["start"]) | {spec["marker"][0]}
    items = set()
    for other in split_sections.SECTIONS.values():
        patterns = list(other["start"]) + list(other["end"])
        if other.get("marker"):
            patterns.append(other["marker"][0])
        items |= {pattern for pattern in patterns if pattern.startswith(r"^item\s*")}
    return [re.compile(pattern) for pattern in sorted(items - own)]


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form", ("10-K", "10-Q"))
def test_no_paragraph_after_the_first_is_another_sections_heading(ticker, form):
    skip_where_the_filing_omits_the_item(ticker, form)
    foreign = foreign_headings(form)
    for index, paragraph in enumerate(section(ticker, form)["paragraphs"][1:], start=2):
        flat = html_text.normalized(paragraph)
        hit = next((p.pattern for p in foreign if p.search(flat)), None)
        assert hit is None, f"{ticker} {form} risk factors [{index}] matches {hit!r}"


def test_esterlines_quarterly_report_carries_no_item_1a_and_says_so():
    """Read from the filing: in `10-Q/ese-20260630x10q.htm` the line `PART II.
    OTHER INFORMATION` is followed directly by `ITEM 2. UNREGISTERED SALES OF
    EQUITY SECURITIES AND USE OF PROCEEDS`, with no Item 1 and no Item 1A
    between them. There is no Item 1A heading anywhere in the document — the
    table of contents does not list one either — because Form 10-Q lets a filer
    leave the item out when it has nothing to add to the 10-K's risk factors.

    That is not a section that did not change, and the difference matters: the
    first reads as an absence to go and check, the second as a quarter of
    stability. So the payload records the absence, the file states it, and the
    zero beside it is never the only thing a reader sees."""
    payload = diffed("ESE", "10-Q")
    assert payload["present"] is False
    assert "no heading matched" in payload["absent"]
    rendered = split_sections.render_risk_factors(payload)
    assert "carries no Item 1A" in rendered
    assert "is not a section that did not change" in rendered
    with pytest.raises(split_sections.SectionNotFound):
        split_sections.extract("ESE", "10-Q", "risk_factors")


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_annual_report_has_no_prior_on_record_and_the_file_says_which(ticker):
    """`docs/INPUT_SPEC.md` §2 reads the first filing whole, and the fixture set
    holds one 10-K per company, so there is no prior-year Item 1A to diff
    against. The file has to say that rather than print a section under a
    heading that claims it is a diff."""
    payload = diffed(ticker, "10-K")
    assert payload["has_prior_period"] is False
    assert payload["carried_whole"] is True
    assert payload["prior_accession"] is None
    assert "carried whole" in split_sections.render_risk_factors(payload)


# --- the diff, and only the diff --------------------------------------------


def entries(prefix: str, paragraphs: list[str]) -> list[dict]:
    """Paragraphs in the shape `risk_factor_diff` takes them from a filing."""
    return [{"id": f"{prefix}:risk_factors:{index}", "text": text,
             "note": "risk_factors"}
            for index, text in enumerate(paragraphs, start=1)]


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_file_carries_the_changed_paragraphs_and_no_others(ticker):
    """Every id in `input_risk_factors.md` is a paragraph the diff reported.

    Compared as ids rather than as substrings, because an unchanged one-line
    paragraph can be a run of characters inside a changed one and a containment
    check would forgive exactly the failure this is looking for."""
    if ticker == "ESE":
        pytest.skip("ESE's 10-Q carries no Item 1A; its own test says so")
    payload = diffed(ticker, "10-Q")
    rendered = split_sections.render_risk_factors(payload)
    reported = [entry["id"] for entry in payload["changed"] + payload["removed"]]
    assert PARAGRAPH_ID.findall(rendered) == reported
    for entry in payload["changed"] + payload["removed"]:
        assert entry["text"] in rendered
    assert payload["unchanged"] == payload["paragraphs"] - len(payload["changed"])


def test_qualcomms_quarterly_risk_factors_repeat_and_none_of_them_is_carried():
    """The case the rule exists for. Qualcomm files its whole Item 1A again
    each quarter, so the prior-period diff has nothing to report, and the file
    is four lines rather than the section. Twenty of those paragraphs name
    litigation, an investigation or a credit facility — the topics
    `docs/INPUT_SPEC.md` §2 item 6 keeps out of the diff *in a note* — and none
    of them is carried, which is the decision `src/split_sections.py` records:
    in Item 1A the finding is the change, not the repetition."""
    payload = diffed("QCOM", "10-Q")
    assert payload["changes"] == 0
    assert payload["unchanged"] == payload["paragraphs"] > 0
    rendered = split_sections.render_risk_factors(payload)
    assert PARAGRAPH_ID.findall(rendered) == []
    for paragraph in section("QCOM", "10-Q")["carried"]:
        assert paragraph not in rendered


def test_a_prior_period_that_carried_no_item_1a_is_named_where_it_matters():
    """The third outcome of `risk_factors`, which no fixture pair produces.

    A 10-Q may omit Item 1A — Esterline's does — so a company can file one
    quarter without the item and the next quarter with it. Every paragraph is
    then new, and that is a true statement only if the reader is told what it is
    new *against*: against a section that was not there, not against a section
    that said something else. No pair in the fixture set runs that way round, so
    the outcome is put together here from a real section and the empty prior
    that `risk_factors` passes on when the prior filing raises `SectionNotFound`.
    """
    carried = section("TTMI", "10-Q")["carried"]
    found = split_sections.risk_factor_diff(entries("now", carried), [])
    assert len(found["changed"]) == found["paragraphs"] == len(carried) > 0
    assert found["removed"] == [] and found["unchanged"] == 0

    payload = diffed("TTMI", "10-Q") | found | {
        "prior_absent": "10-Q risk_factors: no heading matched"}
    rendered = split_sections.render_risk_factors(payload)
    assert "That prior filing carried no Item 1A" in rendered
    assert "new against a section that was not there" in rendered


# --- the cleaner, handed a section rather than a document -------------------
#
# `_risk_factor_paragraphs` hands `src/clean_text.py` the section's blocks, the
# way `extract` has always handed it the MD&A's. Two of the cleaner's rules read
# the document *around* a paragraph, and a section is not that document, so both
# behave differently here than they do over a whole filing. Neither is this
# item's to move: the call is the MD&A splitter's, the rules are the cleaner's,
# and changing either changes `mdna.*.paragraphs`, an expected value already
# recorded against these filings. `input_mdna.md` carries both today. They are
# asserted here so that the record is in the suite rather than in a review
# comment — and so that whoever fixes the cleaner is shown these two tests.


def test_cienas_whole_item_1a_is_one_paragraph_the_cleaner_drops():
    """Adverse, and recorded rather than softened.

    Ciena's quarterly Item 1A is a single paragraph saying its risk factors have
    not materially changed, and that paragraph carries the safe-harbour sentence
    the cleaner drops. So both quarters clean down to the heading line alone and
    the diff compares a heading with a heading. The wording did change — the
    quarter under test cites the cautionary note `in Item 2 of Part I of this
    report` where the prior one cited it `in this report` — and the file reports
    no change, which is the inverse of what this section is for. A new risk
    factor written into that same paragraph would go the same way.
    """
    current = section("CIEN", "10-Q")
    assert len(current["paragraphs"]) == 2, "a heading and one body paragraph"
    assert current["carried"] == current["paragraphs"][:1], "only the heading survives"

    dropped = clean_text.clean_stream(blocks=current["blocks"])["dropped"]
    assert [entry["reason"] for entry in dropped] == ["forward_looking_boilerplate"]

    # The change the diff cannot see, read with html.parser and nothing from src/.
    bodies = []
    for role in ("primary_html", "prior_period"):
        row = cutoff_guard.one_document("CIEN", "10-Q", role)
        paragraphs = independent_text.block_paragraphs(
            cutoff_guard.load_document(row["full_path"], row["filing_date"]))
        opens = max(index for index, text in enumerate(paragraphs)
                    if html_text.normalized(text).startswith("item 1a"))
        bodies.append(html_text.normalized_spacing(paragraphs[opens + 1]))
    assert bodies[0] != bodies[1], "the two quarters word this paragraph the same"

    assert diffed("CIEN", "10-Q")["changes"] == 0


def test_a_bare_page_number_still_reaches_the_diff_as_if_it_were_a_risk_factor():
    """The same root cause, pointing the other way: noise reported as a change.

    The cleaner knows a page tail by the run it belongs to — three rising
    numbers, pages apart — and a section holds only the tail of each of its own
    pages, so the run is broken and the numbers stay. Seagate's Item 1A spans
    pages 34 to 56 of its 10-Q and prints the number at the foot of each, so
    `46`, `48`, `51` and `55` arrive under `## New or changed` and `47` under
    `## Removed since the prior period`, and the summary line counts them. This
    asserts the defect: fixing the cleaner should break this test, and whoever
    breaks it should read the note above it.
    """
    payload = diffed("STX", "10-Q")
    reported = [entry["text"] for entry in payload["changed"] + payload["removed"]]
    page_tails = [text for text in reported if PAGE_TAIL.fullmatch(text.strip())]
    assert page_tails, ("no page tail reaches the diff any more — if the cleaner "
                        "was fixed, delete this test and the note above it")


# --- the reordered fixture --------------------------------------------------


def blocks_of(name: str) -> list[str]:
    """The eight delimited risk factors of one constructed document, as text.

    Nothing from `src/` and no HTML parser: the claim being made is about the
    bytes on disk, so it is made on the bytes on disk.
    """
    text = (FIXTURE / name).read_text(encoding="utf-8")
    found = text.split(DELIMITER)[1:]
    found[-1] = found[-1][: found[-1].index(AFTER_THE_BLOCKS)]
    return found


def constructed(name: str) -> list[str]:
    """The paragraphs of the constructed document's Item 1A, as the bundle has them."""
    html = (FIXTURE / name).read_text(encoding="utf-8")
    cut = split_sections.split(html, "10-K", "risk_factors")
    return clean_text.clean_stream(blocks=cut["blocks"])["paragraphs"]


def diff_of(now: list[str], was: list[str]) -> dict:
    """The two constructed sections put through the filings' own diff."""
    return split_sections.risk_factor_diff(entries("now", now), entries("was", was))


def test_the_reordered_document_is_a_reorder_and_not_an_edit():
    """The expected value below is zero because of this, and only this."""
    as_filed = blocks_of("risk_factors_as_filed.htm")
    reordered = blocks_of("risk_factors_reordered.htm")
    assert len(as_filed) == len(reordered) == 8
    assert sorted(as_filed) == sorted(reordered), "a block was edited, not moved"
    assert as_filed != reordered, "the second document is in the same order"


def test_a_reordered_risk_factor_section_is_no_change():
    as_filed = constructed("risk_factors_as_filed.htm")
    reordered = constructed("risk_factors_reordered.htm")
    assert sorted(as_filed) == sorted(reordered) and as_filed != reordered

    found = diff_of(reordered, as_filed)
    assert (found["changed"], found["removed"]) == ([], [])
    assert found["changes"] == 0
    assert found["unchanged"] == found["paragraphs"] == len(reordered)


def test_one_edited_word_in_that_same_pair_is_reported():
    """The control. A diff that always answered zero would pass the test above."""
    as_filed = constructed("risk_factors_as_filed.htm")
    reordered = constructed("risk_factors_reordered.htm")
    planted = [text.replace("a leverage covenant", "two leverage covenants")
               for text in reordered]
    assert planted != reordered, "the planted edit did not land"

    found = diff_of(planted, as_filed)
    assert len(found["changed"]) == len(found["removed"]) == 1
    assert found["changes"] == 2
    assert "two leverage covenants" in found["changed"][0]["text"]
    assert "a leverage covenant" in found["removed"][0]["text"]


def test_the_constructed_document_has_the_table_of_contents_trap_in_it():
    """Two candidates, and the section is the second. A fixture that resolved on
    one candidate would not be exercising the rule it is here to hold."""
    html = (FIXTURE / "risk_factors_as_filed.htm").read_text(encoding="utf-8")
    text = html_text.strip_tags(html)
    spec = split_sections.SECTIONS[("10-K", "risk_factors")]
    assert len(split_sections.headings(text, spec)) == 2
    start, stop, _, rule = split_sections.bounds(text, "10-K", "risk_factors")
    assert rule == "last candidate"
    assert one_line(text, start) == "Item 1A. Risk Factors"
    assert one_line(text, stop) == "Item 1B. Unresolved Staff Comments"


# --- the gate and the file name ---------------------------------------------


def test_the_splitter_goes_through_the_cutoff_gate():
    for form in ("10-K", "10-Q"):
        with pytest.raises(cutoff_guard.CutoffViolationError):
            split_sections.extract("AAPL", form, "risk_factors",
                                   cutoff=dt.date(2020, 1, 1))
        with pytest.raises(cutoff_guard.CutoffViolationError):
            split_sections.risk_factors("AAPL", form, cutoff=dt.date(2020, 1, 1))


def test_a_missing_section_raises_rather_than_returning_nothing():
    with pytest.raises(split_sections.SectionNotFound):
        split_sections.split("<html><body><p>nothing here</p></body></html>",
                             "10-K", "risk_factors")


def test_the_command_writes_the_bundles_risk_factors_file(tmp_path, capsys):
    out = tmp_path / split_sections.RISK_FACTORS_FILE
    assert split_sections.main(["--ticker", "qcom", "--form", "10-Q",
                                "--section", "risk_factors", "--out", str(out)]) == 0
    assert "0 changes" in capsys.readouterr().out
    assert out.read_text(encoding="utf-8").startswith("# QCOM 10-Q Item 1A risk factors")


def test_every_other_bundle_name_is_still_refused(tmp_path, capsys):
    """The carve-out is one name for one section, not an open door."""
    for section_name, name in (("mdna", "input_mdna.md"),
                               ("mdna", split_sections.RISK_FACTORS_FILE),
                               ("risk_factors", "input_notes.md")):
        out = tmp_path / name
        assert split_sections.main(["--ticker", "AAPL", "--form", "10-K",
                                    "--section", section_name,
                                    "--out", str(out)]) == split_sections.BAD_INPUT
        assert "is a bundle filename" in capsys.readouterr().err
        assert not out.exists()
