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
import json
import re
from pathlib import Path

import pytest

from src import cutoff_guard, html_text, split_sections
from src.fetch_fixtures import TICKERS
from tests import independent_text

FIXTURES = Path(__file__).resolve().parent / "fixtures"

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


def expected(ticker: str) -> dict:
    return json.loads((FIXTURES / ticker / "expected.json").read_text())


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


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("section", sorted(SPEC))
def test_the_section_is_never_empty(ticker, section):
    form = SPEC[section][0]
    payload = split_sections.extract(ticker, form, section)
    assert payload["paragraphs"], f"{ticker} {form} {section} came out empty"
    assert payload["text"].strip()


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("section", sorted(SPEC))
def test_the_expected_paragraph_count_survives_an_independent_recount(ticker, section):
    form = SPEC[section][0]
    assert len(recount(source_html(ticker, form), section)) == \
        expected(ticker)[section][form]["paragraphs"]


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("section", sorted(SPEC))
def test_the_splitter_finds_exactly_that_many_paragraphs(ticker, section):
    form = SPEC[section][0]
    payload = split_sections.extract(ticker, form, section)
    assert len(payload["paragraphs"]) == expected(ticker)[section][form]["paragraphs"]


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("section", sorted(SPEC))
def test_paragraph_ids_are_unique_and_dense(ticker, section):
    form = SPEC[section][0]
    payload = split_sections.extract(ticker, form, section)
    count = len(payload["carried"])
    assert set(payload["paragraph_ids"]) == \
        {f"{payload['accession']}:{section}:{index}" for index in range(1, count + 1)}


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_report_carries_the_audit_firms_name(ticker):
    payload = split_sections.extract(ticker, "10-K", "auditors_report")
    firm = expected(ticker)["auditors_report"]["10-K"]["audit_firm"]
    # PANW signs "Ernst\xa0& Young LLP" and ESE signs in capitals, so the
    # comparison flattens whitespace and case. Nothing emitted is changed.
    assert html_text.normalized(firm) in html_text.normalized(payload["text"])


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_parser_finds_the_critical_audit_matters_the_report_states(ticker):
    payload = split_sections.extract(ticker, "10-K", "auditors_report")
    record = expected(ticker)["auditors_report"]["10-K"]
    assert payload["critical_audit_matters"]["count"] == record["critical_audit_matters"]
    assert payload["critical_audit_matters"]["stated"] == record["the_report_states"]
    # The report says in its own words how many there are; the count has to
    # agree with that sentence, and `critical_audit_matters` raises if it does
    # not. Asserted here as well so the rule is visible, not just enforced.
    if record["the_report_states"] == "one":
        assert record["critical_audit_matters"] == 1
    elif record["the_report_states"] == "many":
        assert record["critical_audit_matters"] >= 2


def test_a_count_that_contradicts_the_report_is_an_error_not_a_guess():
    with pytest.raises(split_sections.CriticalAuditMatterCountUnclear):
        split_sections.critical_audit_matters(
            "Critical Audit Matters\n\nThe critical audit matters communicated below "
            "are matters arising from the current period audit.\n\n"
            "Goodwill\n\nWe identified goodwill as a critical audit matter.")


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_auditors_report_stops_before_the_financial_statements(ticker):
    payload = split_sections.extract(ticker, "10-K", "auditors_report")
    heads = [html_text.normalized(payload["text"][start:end])
             for start, end in html_text.lines(payload["text"])]
    assert not [head for head in heads if re.match(r"^item\s*8\b", head)]
    assert not [head for head in heads
                if re.match(r"^consolidated balance sheets?\b", head)]


@pytest.mark.parametrize("ticker", TICKERS)
def test_item_9a_stops_before_item_9b(ticker):
    payload = split_sections.extract(ticker, "10-K", "item_9a")
    heads = [html_text.normalized(payload["text"][start:end])
             for start, end in html_text.lines(payload["text"])]
    assert not [head for head in heads if re.match(r"^item\s*9b\b", head)]


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("section", sorted(SPEC))
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


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form,section", (("10-K", "auditors_report"),
                                          ("10-K", "item_9a"),
                                          ("10-Q", "item_4_controls")))
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
