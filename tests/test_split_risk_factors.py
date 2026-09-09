"""Item 1A, cut at the right heading, and only its diff carried forward.

Two claims are held to something outside the splitter, and they are the two
this section can get wrong.

**Where the section starts and stops.** Recorded per company as the heading the
section opens at and the heading it ends before — two lines a reader can find in
the document — read off all twelve 10-Ks through `tests/independent_text.py`
and nothing from `src/`. A count cannot make this claim: a splitter that took
the table-of-contents entry would return three lines of index and still have a
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


def one_line(text: str, offset: int) -> str:
    """The first line with anything on it at or after `offset`, flattened.

    `normalized_spacing`, not `normalized`: the twelve write their headings in
    three different casings and the recorded line is the filing's own.
    """
    for start, end in html_text.lines(text):
        line = html_text.normalized_spacing(text[start:end].replace("​", ""))
        if start >= offset and line:
            return line
    return ""


# --- where the section starts and stops ------------------------------------


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_section_begins_and_ends_at_the_headings_the_filing_carries(ticker):
    text = stripped(ticker, "10-K")
    start, stop, _, _ = split_sections.bounds(text, "10-K", "risk_factors")
    assert one_line(text, start) == value(ticker, "risk_factors.10-K.opens_at")
    assert one_line(text, stop) == value(ticker, "risk_factors.10-K.ends_before")


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_table_of_contents_entry_is_not_the_one_selected(ticker):
    """The trap, made explicit: the index names Item 1A before the section does."""
    text = stripped(ticker, "10-K")
    spec = split_sections.SECTIONS[("10-K", "risk_factors")]
    candidates = split_sections.headings(text, spec)
    start, stop, _, rule = split_sections.bounds(text, "10-K", "risk_factors")
    assert rule == "last candidate"
    assert start == candidates[-1][0]
    if len(candidates) == 1:
        return

    # What the first match would have produced: the same end rule, applied from
    # the table-of-contents entry, which stops at the index's own Item 1B line.
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
    if ticker == "ESE" and form == "10-Q":
        pytest.skip("ESE's 10-Q carries no Item 1A; its own test says so")
    payload = section(ticker, form)
    assert payload["paragraphs"], f"{ticker} {form} risk factors came out empty"
    assert payload["text"].strip()


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form", ("10-K", "10-Q"))
def test_every_paragraph_is_the_filings_own_text(ticker, form):
    if ticker == "ESE" and form == "10-Q":
        pytest.skip("ESE's 10-Q carries no Item 1A; its own test says so")
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
    if ticker == "ESE" and form == "10-Q":
        pytest.skip("ESE's 10-Q carries no Item 1A; its own test says so")
    foreign = foreign_headings(form)
    for index, paragraph in enumerate(section(ticker, form)["paragraphs"][1:], start=2):
        flat = html_text.normalized(paragraph)
        hit = next((p.pattern for p in foreign if p.search(flat)), None)
        assert hit is None, f"{ticker} {form} risk factors [{index}] matches {hit!r}"


def test_esterlines_quarterly_report_carries_no_item_1a_and_says_so():
    """Read from the filing: `10-Q/ese-20260630x10q.htm` runs Part II Item 1
    Legal Proceedings straight into Item 2 Unregistered Sales. There is no
    Item 1A heading anywhere in it — the table of contents does not list one
    either — because Form 10-Q lets a filer leave the item out when it has
    nothing to add to the 10-K's risk factors.

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


def entries(prefix: str, paragraphs: list[str]) -> list[dict]:
    return [{"id": f"{prefix}:risk_factors:{index}", "text": text,
             "note": "risk_factors"}
            for index, text in enumerate(paragraphs, start=1)]


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
