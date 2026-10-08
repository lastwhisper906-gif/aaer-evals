"""The auditor's report, Item 9A and the 10-Q's Item 4 — the controls sections.

These are the highest-value text in the bundle for accounting reliability: a
material-weakness sentence or a critical audit matter is exactly what the
question is asking about, and it is worth nothing if it never reached the
input. So the test that matters most here is the boring one — thirty-six
sections, zero empties.

Paragraph counts are recounted through `tests/independent_text.py`, which finds
the headings with its own regexes and its own parser.
"""

from __future__ import annotations

import datetime as dt
import re

import pytest

from src import cutoff_guard, html_text, split_sections
from src.fetch_fixtures import TICKERS
from tests import independent_text
from tests.expected_values import value

# (form, section) → (heading, item-marker-alone or None, end, select-by-content)
SPEC = {
    "auditors_report": (
        "10-K",
        re.compile(r"^report of independent registered public accounting firm"),
        None,
        re.compile(r"^consolidated statements? of operations\b"
                   r"|^consolidated balance sheets?\b"
                   r"|^consolidated statements? of income\b"
                   r"|^consolidated and combined statements? of operations\b"
                   r"|^reports? of management\b"
                   r"|^statement of management.{0,3}s responsibility\b"
                   r"|^management.{0,3}s report on internal control\b"
                   # Dell titles its balance sheet `Consolidated Statements of
                   # Financial Position` and places it first after the report.
                   r"|^consolidated statements? of financial position\b"
                   r"|^item\s*8\b|^item\s*9\b"),
        re.compile(r"critical audit matter")),
    "item_9a": (
        "10-K",
        re.compile(r"^item\s*9a\s*[.:\-–—]?\s*controls and procedures"),
        (re.compile(r"^item\s*9a\s*[.:\-–—]?$"), re.compile(r"^controls and procedures")),
        re.compile(r"^item\s*9b\b|^item\s*10\b"),
        None),
    "item_4_controls": (
        "10-Q",
        re.compile(r"^item\s*4\s*[.:\-–—]?\s*controls and procedures"),
        (re.compile(r"^item\s*4\s*[.:\-–—]?$"), re.compile(r"^controls and procedures")),
        re.compile(r"^item\s*1\s*[.:\-–—]?\s*legal proceedings|^part ii\b"
                   r"|^item\s*1a\b|^cautionary note\b"),
        None),
}


def source_html(ticker: str, form: str) -> str:
    row = cutoff_guard.one_document(ticker, form, "primary_html")
    return cutoff_guard.load_document(row["full_path"], row["filing_date"])


def _flat(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def recount(html: str, section: str) -> list[str]:
    """Find the section and split it on blank lines, without importing src."""
    _, heading, marker, end, select = SPEC[section]
    text = independent_text.block_text(html)
    rows = [(match.start(), _flat(match.group()))
            for match in re.finditer(r"^.*$", text, re.MULTILINE)]
    rows = [row for row in rows if row[1]]

    candidates = []
    for index, (offset, flat) in enumerate(rows):
        following = rows[index + 1][1] if index + 1 < len(rows) else ""
        if heading.search(flat) or (marker and marker[0].search(flat)
                                    and marker[1].search(following)):
            candidates.append(offset)
    assert candidates, f"{section}: the recount found no heading"

    def stop_after(start: int) -> int:
        return next((offset for offset, flat in rows
                     if offset > start and end.search(flat)), len(text))

    if select is not None:
        start = next(offset for offset in candidates
                     if select.search(_flat(text[offset:stop_after(offset)])))
    else:
        start = candidates[-1]
    body = text[start:stop_after(start)].strip()
    return [chunk.strip() for chunk in body.split("\n\n") if chunk.strip()]


# NAPCO's 10-K heads Item 9A 'ITEM 9A: CONTROL AND PROCEDURES', singular, on the
# one line of the document that names the item (10-K/nssc-20260630x10k.htm.gz);
# its table of contents names none. The recount's title above is written
# 'controls and procedures', as the splitter's is, so the recount finds no
# heading in that 10-K either, and NAPCO's case of the recount test is a strict
# expected failure (RECOUNT_FINDS_NO_HEADING below). The line, as the recount
# flattens it:
SINGULAR_ITEM_9A = {"NSSC": "item 9a: control and procedures"}
# A title of either number, read by the test below alone and never by the
# recount, to show what the recount's title, as written, misses.
EITHER_NUMBER = (re.compile(r"^item\s*9a\s*[.:\-–—]?\s*controls? and procedures"),
                 re.compile(r"^controls? and procedures"))


def item_9a_headings(text: str, heading: re.Pattern, title: re.Pattern) -> list[str]:
    """The lines the recount takes for an Item 9A heading under one title: a
    heading line, or the bare item marker whose next line is the title."""
    marker = SPEC["item_9a"][2][0]
    rows = [_flat(line) for line in text.split("\n")]
    rows = [row for row in rows if row]
    return [row for index, row in enumerate(rows)
            if heading.search(row) or (marker.search(row) and index + 1 < len(rows)
                                       and title.search(rows[index + 1]))]


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_only_item_9a_line_the_recounts_title_misses_is_written_singular(ticker):
    """Both sides of the recount's mark: where SINGULAR_ITEM_9A names the line,
    the recount's title finds no Item 9A heading and a title of either number
    finds that line alone; in every other 10-K the two find the same lines, so
    the number of the title decides no other company's count."""
    text = independent_text.block_text(source_html(ticker, "10-K"))
    _, heading, (_, title), _, _ = SPEC["item_9a"]
    written = item_9a_headings(text, heading, title)
    either = item_9a_headings(text, *EITHER_NUMBER)
    if ticker in SINGULAR_ITEM_9A:
        assert written == [], f"{ticker}: {written}"
        assert either == [SINGULAR_ITEM_9A[ticker]], f"{ticker}: {either}"
    else:
        assert either == written, f"{ticker}: {either} against {written}"


# NAPCO's 10-K writes 'ITEM 9A: CONTROL AND PROCEDURES', singular, on the one
# line of the document that names Item 9A; its table of contents names none.
# `src/split_sections.py` starts the item on 'controls and procedures', as a
# heading line or after a marker line, so it finds no candidate and raises
# SectionNotFound. The item is there, 29 blocks read one by one off the 10-K
# (its note in tests/fixtures/NSSC/expected_values.json names each) -- 'Evaluation
# of Disclosure Controls and Procedures', 'Management’s Report on Internal
# Control over Financial Reporting', 'Changes in Internal Control over Financial
# Reporting' and Deloitte's 'Opinion on Internal Control over Financial
# Reporting', signed '/s/ DELOITTE & TOUCHE LLP' -- and none of it reaches the
# bundle. Every test below that asks the splitter for the item carries the
# mark. Strict, so teaching the splitter the singular turns these red and the
# marks come off.
HEADING_NOT_FOUND = {
    ("NSSC", "item_9a"): "the 10-K's one Item 9A line is 'ITEM 9A: CONTROL AND "
                         "PROCEDURES', singular, and the splitter's title is 'controls "
                         "and procedures'; 29 read, no heading found",
}


def marked(ticker: str, section: str, *values, **named):
    """One case, carrying the strict mark where HEADING_NOT_FOUND names it."""
    marks = ([pytest.mark.xfail(
        strict=True, reason=f"{ticker} {section}: {HEADING_NOT_FOUND[(ticker, section)]}")]
        if (ticker, section) in HEADING_NOT_FOUND else [])
    return pytest.param(*values, marks=marks, **named)


# The cases in the order and with the ids the two stacked parametrisations gave
# them, section first: `auditors_report-AAPL` ... `item_9a-NTAP`.
SECTION_CASES = [marked(ticker, section, ticker, section, id=f"{section}-{ticker}")
                 for section in sorted(SPEC) for ticker in TICKERS]


@pytest.mark.parametrize("ticker,section", SECTION_CASES)
def test_the_section_is_never_empty(ticker, section):
    form = SPEC[section][0]
    payload = split_sections.extract(ticker, form, section)
    assert payload["paragraphs"], f"{ticker} {form} {section} came out empty"
    assert payload["text"].strip()


# The recount's title is written 'controls and procedures' (SPEC above), so it
# finds no heading in NAPCO's 10-K and stops at `assert candidates` before it
# counts anything. That case is a strict expected failure, beside the splitter's;
# the count it would have checked is asserted, unmarked, from the one line the
# 10-K prints, by the test after it. Strict, so a recount that reads the
# singular turns it red and the mark comes off.
RECOUNT_FINDS_NO_HEADING = {
    ("NSSC", "item_9a"): "the 10-K's one Item 9A line is 'ITEM 9A: CONTROL AND "
                         "PROCEDURES', singular, and the recount's title is 'controls "
                         "and procedures'; 29 read, no heading recounted",
}

# The cases in the order and with the ids the two stacked parametrisations gave
# them, section first: `auditors_report-AAPL` ... `item_9a-NTAP`.
RECOUNT_CASES = [
    pytest.param(ticker, section, id=f"{section}-{ticker}", marks=[pytest.mark.xfail(
        strict=True,
        reason=f"{ticker} {section}: {RECOUNT_FINDS_NO_HEADING[(ticker, section)]}")]
        if (ticker, section) in RECOUNT_FINDS_NO_HEADING else [])
    for section in sorted(SPEC) for ticker in TICKERS]


@pytest.mark.parametrize("ticker,section", RECOUNT_CASES)
def test_the_expected_paragraph_count_survives_an_independent_recount(ticker, section):
    form = SPEC[section][0]
    assert len(recount(source_html(ticker, form), section)) == \
        value(ticker, f"{section}.{form}.paragraphs")


@pytest.mark.parametrize("ticker", sorted(SINGULAR_ITEM_9A))
def test_an_item_9a_headed_in_the_singular_holds_its_count_from_the_line_it_prints(
        ticker):
    """What the recount's mark hides, asserted unmarked: the item split as the
    recount splits it -- the same block text, its blank lines and its end rule
    -- from the one Item 9A line the 10-K prints, which SINGULAR_ITEM_9A records,
    holds the count its note reads block by block."""
    _, _, _, end, _ = SPEC["item_9a"]
    text = independent_text.block_text(source_html(ticker, "10-K"))
    rows = [(match.start(), _flat(match.group()))
            for match in re.finditer(r"^.*$", text, re.MULTILINE)]
    rows = [row for row in rows if row[1]]
    starts = [offset for offset, flat in rows if flat == SINGULAR_ITEM_9A[ticker]]
    assert len(starts) == 1, f"{ticker}: {len(starts)} lines read the item's heading"
    stop = next((offset for offset, flat in rows
                 if offset > starts[0] and end.search(flat)), len(text))
    body = text[starts[0]:stop].strip()
    blocks = [chunk.strip() for chunk in body.split("\n\n") if chunk.strip()]
    assert len(blocks) == value(ticker, "item_9a.10-K.paragraphs")


# Dell's 10-K places its `CONSOLIDATED STATEMENTS OF FINANCIAL POSITION` first
# after the auditor's report, under that title. `src/split_sections.py`'s end
# rule knows `consolidated balance sheets` and `consolidated statements of
# income` and not that title, so the split runs through the whole statement of
# financial position and stops at the statement of income. The expected value
# stands as the report reads -- 27 blocks, from the heading to the page
# furniture before the statement title -- and the recount above, whose end rule
# names the title, agrees with it. Strict, so teaching the rule the title turns
# this red and the mark comes off.
OVERRUNS = {
    ("DELL", "auditors_report"): "the split runs through the statement of financial "
                                 "position to the statement of income; 27 read, 149 split",
}


@pytest.mark.parametrize("ticker,section", [
    pytest.param(ticker, section, marks=pytest.mark.xfail(
        strict=True, reason=f"{ticker} {section}: {OVERRUNS[(ticker, section)]}"))
    if (ticker, section) in OVERRUNS else marked(ticker, section, ticker, section)
    for ticker in TICKERS for section in sorted(SPEC)])
def test_the_splitter_finds_exactly_that_many_paragraphs(ticker, section):
    form = SPEC[section][0]
    payload = split_sections.extract(ticker, form, section)
    assert len(payload["paragraphs"]) == value(ticker, f"{section}.{form}.paragraphs")


@pytest.mark.parametrize("ticker,section", SECTION_CASES)
def test_paragraph_ids_are_unique_and_dense(ticker, section):
    form = SPEC[section][0]
    payload = split_sections.extract(ticker, form, section)
    count = len(payload["carried"])
    assert set(payload["paragraph_ids"]) == \
        {f"{payload['accession']}:{section}:{index}" for index in range(1, count + 1)}


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_report_carries_the_audit_firms_name(ticker):
    payload = split_sections.extract(ticker, "10-K", "auditors_report")
    firm = value(ticker, "auditors_report.10-K.audit_firm")
    # PANW signs "Ernst\xa0& Young LLP" and ESE signs in capitals, so the
    # comparison flattens whitespace and case. Nothing emitted is changed.
    assert html_text.normalized(firm) in html_text.normalized(payload["text"])


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_parser_finds_the_critical_audit_matters_the_report_states(ticker):
    payload = split_sections.extract(ticker, "10-K", "auditors_report")
    matters = value(ticker, "auditors_report.10-K.critical_audit_matters")
    stated = value(ticker, "auditors_report.10-K.the_report_states")
    assert payload["critical_audit_matters"]["count"] == matters
    assert payload["critical_audit_matters"]["stated"] == stated
    # The report says in its own words how many there are; the count has to
    # agree with that sentence, and `critical_audit_matters` raises if it does
    # not. Asserted here as well so the rule is visible, not just enforced.
    if stated == "one":
        assert matters == 1
    elif stated == "many":
        assert matters >= 2


def test_a_count_that_contradicts_the_report_is_an_error_not_a_guess():
    with pytest.raises(split_sections.CriticalAuditMatterCountUnclear):
        split_sections.critical_audit_matters(
            "Critical Audit Matters\n\nThe critical audit matters communicated below "
            "are matters arising from the current period audit.\n\n"
            "Goodwill\n\nWe identified goodwill as a critical audit matter.")


# Fortinet's 10-K for 2025 (Deloitte) heads the section `Critical Audit Matter`,
# describes one matter under one `Critical Audit Matter Description`, and then
# carries the firm's plural template: "The critical audit matters communicated
# below are matters arising from the current-period audit of the financial
# statements". The heading is the report's other statement of how many, and
# the count says which of the two the report means. Both sides of that rule:
# the same sentence under a plural heading is still the contradiction above.

def test_a_singular_heading_over_the_plural_template_sentence_states_one_matter():
    found = split_sections.critical_audit_matters(
        "Critical Audit Matter\n\nThe critical audit matters communicated below "
        "are matters arising from the current-period audit.\n\n"
        "Revenue\n\nCritical Audit Matter Description\n\nWe identified the "
        "evaluation of performance obligations as a critical audit matter.\n\n"
        "How the Critical Audit Matter Was Addressed in the Audit\n\nWe read "
        "the contracts.")
    assert found["count"] == 1
    assert found["stated"] == "one"
    assert found["heading"] == "one"


def test_the_plural_template_sentence_under_a_plural_heading_is_still_refused():
    with pytest.raises(split_sections.CriticalAuditMatterCountUnclear):
        split_sections.critical_audit_matters(
            "Critical Audit Matters\n\nThe critical audit matters communicated below "
            "are matters arising from the current-period audit.\n\n"
            "Revenue\n\nCritical Audit Matter Description\n\nWe identified the "
            "evaluation of performance obligations as a critical audit matter.\n\n"
            "How the Critical Audit Matter Was Addressed in the Audit\n\nWe read "
            "the contracts.")


def test_fortinets_report_is_read_as_one_matter_by_its_heading():
    """Read from the filing: the heading 'Critical Audit Matter', one 'Critical
    Audit Matter Description' for 'Revenue', and the plural template sentence
    between them."""
    payload = split_sections.extract("FTNT", "10-K", "auditors_report")
    assert payload["critical_audit_matters"] == {
        "count": 1, "stated": "one", "heading": "one",
        "matched_by": "addressed_headings"}


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_auditors_report_stops_before_the_financial_statements(ticker):
    payload = split_sections.extract(ticker, "10-K", "auditors_report")
    heads = [html_text.normalized(payload["text"][start:end])
             for start, end in html_text.lines(payload["text"])]
    assert not [head for head in heads if re.match(r"^item\s*8\b", head)]
    assert not [head for head in heads
                if re.match(r"^consolidated balance sheets?\b", head)]


@pytest.mark.parametrize("ticker", [marked(ticker, "item_9a", ticker) for ticker in TICKERS])
def test_item_9a_stops_before_item_9b(ticker):
    payload = split_sections.extract(ticker, "10-K", "item_9a")
    heads = [html_text.normalized(payload["text"][start:end])
             for start, end in html_text.lines(payload["text"])]
    assert not [head for head in heads if re.match(r"^item\s*9b\b", head)]


@pytest.mark.parametrize("ticker,section", SECTION_CASES)
def test_every_paragraph_is_the_filings_own_text(ticker, section):
    form = SPEC[section][0]
    html = source_html(ticker, form)
    payload = split_sections.extract(ticker, form, section)
    canonical = html_text.strip_tags(html)
    for paragraph in payload["paragraphs"]:
        assert paragraph in canonical
    missing = independent_text.Source(html).missing(payload["paragraphs"])
    assert not missing, f"{ticker} {section}: {missing[:1]}"


def test_the_last_candidate_would_be_the_internal_control_opinion():
    """Why the auditor's report is selected by content and not by position.

    AAPL's 10-K carries two reports under the identical heading. The last one
    is the opinion on internal control over financial reporting, and it says
    nothing about a critical audit matter — which is the whole reason the
    input spec asks for this section.
    """
    html = source_html("AAPL", "10-K")
    text = html_text.strip_tags(html)
    spec = split_sections.SECTIONS[("10-K", "auditors_report")]
    candidates = split_sections.headings(text, spec)
    assert len(candidates) > 1
    start, _, _, rule = split_sections.bounds(text, "10-K", "auditors_report")
    assert rule.startswith("first candidate")
    assert start == candidates[0][0] != candidates[-1][0]


def test_the_splitters_go_through_the_cutoff_gate():
    for form, section in (("10-K", "auditors_report"), ("10-K", "item_9a"),
                          ("10-Q", "item_4_controls")):
        with pytest.raises(cutoff_guard.CutoffViolationError):
            split_sections.extract("AAPL", form, section, cutoff=dt.date(2020, 1, 1))


# --- the boundary, which cycle 19 had no criterion for ----------------------
#
# The end-pattern list knew only item headings and financial-statement titles,
# so any unnumbered section between the target and the next item was absorbed:
# CARR's Item 4 ran 25 paragraphs of which 22 were forward-looking-statement
# bullets, and CSCO's auditor's report ran 46 of which 20 were "Reports of
# Management" — including the CEO's and the CFO's signatures, published as
# though the auditor had written them.
#
# Two headings are deliberately NOT foreign, and hand-reading says why: a 10-K
# carries the report on the financial statements and the report on internal
# control under the identical title (seven companies), and Item 9A is the item
# that carries management's ICFR report (eight companies). Neither is another
# item's heading and neither is a financial statement's.

STATEMENT_TITLES = (r"^consolidated statements? of operations\b",
                    r"^consolidated balance sheets?\b",
                    r"^consolidated statements? of income\b",
                    r"^consolidated and combined statements? of operations\b")


def foreign_headings(form: str, section: str) -> list[re.Pattern]:
    """Every item heading the splitter knows except this section's own."""
    spec = split_sections.SECTIONS[(form, section)]
    own = set(spec["start"])
    if spec.get("marker"):
        own.add(spec["marker"][0])
    items = set()
    for other in split_sections.SECTIONS.values():
        patterns = list(other["start"]) + list(other["end"])
        if other.get("marker"):
            patterns.append(other["marker"][0])
        items |= {p for p in patterns if p.startswith(r"^item\s*")}
    return [re.compile(p) for p in sorted(items - own) + list(STATEMENT_TITLES)]


@pytest.mark.parametrize("ticker,form,section", [
    # In the order and with the ids the two stacked parametrisations gave them,
    # the section first: `10-K-auditors_report-AAPL` ... `10-Q-item_4_controls-NTAP`.
    marked(ticker, section, ticker, form, section, id=f"{form}-{section}-{ticker}")
    for form, section in (("10-K", "auditors_report"),
                          ("10-K", "item_9a"),
                          ("10-Q", "item_4_controls"))
    for ticker in TICKERS])
def test_no_paragraph_after_the_first_is_another_sections_heading(ticker, form, section):
    payload = split_sections.extract(ticker, form, section)
    foreign = foreign_headings(form, section)
    for index, paragraph in enumerate(payload["paragraphs"][1:], start=2):
        flat = html_text.normalized(paragraph)
        hit = next((p.pattern for p in foreign if p.search(flat)), None)
        assert hit is None, f"{ticker} {form} {section} [{index}] matches {hit!r}"


def test_carriers_item_4_ends_at_the_no_change_statement():
    """Read from the filing: [1] the heading, [2] the Rule 13a-15 evaluation,
    [3] "There has been no change in our internal control over financial
    reporting during the three months ended June 30, 2026…". [4] opens
    "CAUTIONARY NOTE CONCERNING FACTORS THAT MAY AFFECT FUTURE RESULTS", which
    is Carrier's own unnumbered section and not part of Item 4."""
    payload = split_sections.extract("CARR", "10-Q", "item_4_controls")
    assert len(payload["paragraphs"]) == 3
    assert payload["paragraphs"][-1].startswith(
        "There has been no change in our internal control over financial reporting")


def test_ciscos_auditors_report_ends_before_reports_of_management():
    """Read from the filing: [21] `/s/ PricewaterhouseCoopers LLP`, [22] San
    Jose, [23] the date, [24] "We have served as the Company's auditor since
    1988." — the report's own last paragraph. [25] `54` and [26] `Table of
    Contents` are page furniture, and [27] opens "Reports of Management", which
    is management's section and carries the CEO's and the CFO's signatures."""
    payload = split_sections.extract("CSCO", "10-K", "auditors_report")
    assert len(payload["paragraphs"]) == 26
    assert payload["paragraphs"][23] == \
        "We have served as the Company\u2019s auditor since 1988."
    # The cleaner takes the two `Table of Contents` headers and keeps the page
    # numbers `53` and `54`: two candidates is below the page-run threshold, and
    # a section handed to the cleaner on its own does not show the run a whole
    # document does. That is the conservative direction R20-2 asked for, and it
    # is recorded here rather than tuned around.
    assert len(payload["carried"]) == 24
    assert payload["carried"][22] == payload["paragraphs"][23]
    assert payload["carried"][-1] == "54"
    joined = "\n".join(payload["paragraphs"])
    assert "CHARLES H. ROBBINS" not in joined
    assert "Statement of Management" not in joined
