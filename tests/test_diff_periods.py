"""What the diff layer is allowed to do: carry a paragraph, or replace it.

There is no third outcome, and the test that says so is parameterised over all
twelve companies' real pairs of 10-Qs. The behaviour the rule turns on — a
paragraph collapses only when the same note in the previous report holds the
same text, word for word and digit for digit — is asserted on named paragraphs
from named filings, because that distinction is the whole layer.
"""

from __future__ import annotations

import collections
import datetime as dt
import json
import re
from pathlib import Path

import pytest

from src import assemble_bundle, cutoff_guard, diff_periods, extract_notes
from src.fetch_fixtures import TICKERS
from tests import independent_text

FIXTURES = Path(__file__).resolve().parent / "fixtures"
PLACEHOLDER = re.compile(r"^\[same as prior period, unchanged from (\S+)\]$")


def expected(ticker: str) -> dict:
    return json.loads((FIXTURES / ticker / "expected.json").read_text())


def current_sources(ticker: str, cutoff) -> independent_text.Source:
    """Everything the current 10-Q says: its HTML, and the HTML inside its notes."""
    row = cutoff_guard.one_document(ticker, "10-Q", "primary_html")
    parts = [cutoff_guard.load_document(row["full_path"], cutoff)]
    parts += [section["html"] for section in
              extract_notes.extract(ticker, "10-Q", cutoff=cutoff)["sections"]]
    return independent_text.Source("\n".join(parts))


def prior_sources(ticker: str, cutoff) -> independent_text.Source:
    """Everything the previous 10-Q said. A collapsed paragraph must be in here."""
    row = cutoff_guard.documents(ticker, form="10-Q", role="prior_period")[0]
    parts = [cutoff_guard.load_document(row["full_path"], cutoff)]
    parts += [section["html"] for section in extract_notes.extract(
        ticker, "10-Q", role="prior_period_xbrl_instance", cutoff=cutoff)["sections"]]
    return independent_text.Source("\n".join(parts))


# --- the fetcher's half of the item ----------------------------------------

@pytest.mark.parametrize("ticker", TICKERS)
def test_every_company_has_a_prior_period_10q_on_record(ticker):
    rows = cutoff_guard.documents(ticker, form="10-Q", role="prior_period")
    assert len(rows) == 1, f"{ticker}: {len(rows)} prior-period 10-Q documents"
    row = rows[0]
    assert row["sha256"] and len(row["sha256"]) == 64
    assert row["full_path"].exists()
    current = cutoff_guard.one_document(ticker, "10-Q", "primary_html")
    assert row["filing_date"] < current["filing_date"]
    assert row["filing_date"] <= row["as_of"]


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_prior_periods_instance_is_on_record_too(ticker):
    rows = cutoff_guard.documents(ticker, form="10-Q",
                                  role="prior_period_xbrl_instance")
    assert len(rows) == 1
    assert rows[0]["accession"] == \
        cutoff_guard.documents(ticker, form="10-Q", role="prior_period")[0]["accession"]


# --- the diff itself -------------------------------------------------------

@pytest.mark.parametrize("ticker", TICKERS)
def test_every_output_paragraph_is_the_filing_or_the_placeholder(ticker):
    """No third kind."""
    payload = diff_periods.extract(ticker)
    source = current_sources(ticker, payload["cutoff"])
    carried = [entry["text"] for entry in payload["notes"] + payload["mdna"]
               if entry["kind"] == "verbatim"]
    missing = source.missing(carried)
    assert not missing, f"{ticker}: {missing[:1]}"
    named = []
    for entry in payload["notes"] + payload["mdna"]:
        if entry["kind"] == "collapsed":
            match = PLACEHOLDER.match(entry["line"])
            assert match is not None, entry["line"]
            # The line names the paragraph it stands for, in the previous
            # report. A count would not tell a reader which one.
            assert match.group(1).startswith(payload["prior_accession"])
            named.append(match.group(1))
        else:
            assert entry["kind"] == "verbatim"
    assert len(named) == len(set(named)), "two placeholders name one paragraph"


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_collapsed_and_carried_counts(ticker):
    payload = diff_periods.extract(ticker)
    record = expected(ticker)["prior_period_diff"]["10-Q"]
    assert payload["collapsed"] == record["collapsed"]
    assert payload["carried"] == record["carried_verbatim"]
    assert payload["prior_accession"] == record["prior_accession"]


@pytest.mark.parametrize("ticker", TICKERS)
def test_nothing_collapses_that_is_not_word_for_word_in_the_prior_filing(ticker):
    """What the placeholder promises, checked against the previous filing's own
    bytes through the second stripper — not through the note stream that
    produced the decision."""
    payload = diff_periods.extract(ticker)
    source = prior_sources(ticker, payload["cutoff"])
    misses = []
    for entry in payload["notes"] + payload["mdna"]:
        if entry["kind"] != "collapsed":
            continue
        for piece in independent_text.quotable(entry["text"]):
            if not source.contains(piece):
                misses.append(piece)
    assert not misses, f"{ticker}: {misses[:2]}"


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_counts_survive_an_independent_recount(ticker):
    """Pair the two periods again, with a counter written in this file."""
    payload = diff_periods.extract(ticker)
    prior = diff_periods._note_paragraphs(
        ticker, "10-Q", "prior_period_xbrl_instance",
        cutoff=payload["cutoff"], fixtures_root=cutoff_guard.FIXTURES)
    # A counter, not a set: one paragraph of the previous report stands for one
    # paragraph of this one, so a row printed twice this quarter and once last
    # quarter collapses once. A set cannot count that and cycle 19 used one.
    left = collections.Counter((entry["note"], entry["text"]) for entry in prior)
    collapsed = 0
    for entry in payload["notes"]:
        if entry["verbatim_topic"] is not None:
            continue
        key = (entry["note"], entry["text"])
        if left[key]:
            left[key] -= 1
            collapsed += 1
    assert collapsed == sum(1 for entry in payload["notes"]
                            if entry["kind"] == "collapsed")


def test_a_paragraph_that_differs_only_in_a_number_is_carried_verbatim():
    """Qualcomm's Level 1 footnote is '(1) …' one quarter and '(2) …' the next.
    Cycle 19 masked both to '(#) …' and replaced the second with a placeholder.
    The marker moved, so the paragraph changed, and `docs/INPUT_SPEC.md` §2.3
    carries a changed paragraph verbatim."""
    payload = diff_periods.extract("QCOM")
    sentence = ("Other investments and other liabilities included in Level 1 are "
                "comprised of our deferred compensation plan assets and liabilities.")
    hits = [entry for entry in payload["notes"] if sentence in entry["text"]]
    assert hits, "the named paragraph is no longer in the filing"
    assert hits[0]["text"].startswith("(2)")
    assert hits[0]["kind"] == "verbatim"


def test_a_paragraph_that_is_word_for_word_the_same_is_collapsed():
    """Qualcomm's Alphawave note says the same sentence about pro forma results
    in both quarters, and the placeholder names the paragraph it repeats."""
    payload = diff_periods.extract("QCOM")
    sentence = ("Pro forma results of operations have not been presented because "
                "the effects of this acquisition were not material")
    hits = [entry for entry in payload["notes"] if sentence in entry["text"]]
    assert hits, "the named paragraph is no longer in the filing"
    assert hits[0]["kind"] == "collapsed"
    assert hits[0]["line"] == \
        f"[same as prior period, unchanged from {hits[0]['prior_id']}]"
    assert hits[0]["prior_id"].startswith(payload["prior_accession"])


def test_a_paragraph_that_differs_in_a_word_is_carried_verbatim():
    """Apple's earnings-per-share lead-in reads 'three- and nine-month periods'
    this quarter and 'three- and six-month periods' last quarter. Masking the
    numbers does not make 'nine' into 'six', so it is carried."""
    payload = diff_periods.extract("AAPL")
    # The sentence opens the earnings-per-share note under its own heading, so
    # the paragraph it belongs to is `Earnings Per Share\nThe following table…`.
    hits = [entry for entry in payload["notes"]
            if "The following table shows the computation of basic and diluted "
               "earnings per share" in entry["text"]]
    assert hits, "the named paragraph is no longer in the filing"
    assert "three- and nine-month periods" in hits[0]["text"]
    assert hits[0]["kind"] == "verbatim"
    assert hits[0]["reason"] == "new or changed"


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_always_verbatim_notes_are_never_collapsed(ticker):
    """Contingencies, subsequent events, related parties, debt and covenants,
    accounting changes: an unchanged paragraph there is itself the finding."""
    payload = diff_periods.extract(ticker)
    protected = [entry for entry in payload["notes"] if entry["verbatim_topic"]]
    assert protected, f"{ticker}: no note matched the always-verbatim list"
    for entry in protected:
        assert entry["kind"] == "verbatim", f"{ticker} {entry['note']} was collapsed"
        assert entry["reason"].startswith("always verbatim") or \
            entry["reason"] == "new or changed"


@pytest.mark.parametrize("ticker", TICKERS)
def test_at_least_one_protected_note_would_otherwise_have_collapsed(ticker):
    """Otherwise the rule is untested: it has to actually rescue something."""
    payload = diff_periods.extract(ticker)
    prior = {(entry["note"], entry["text"]) for entry in diff_periods._note_paragraphs(
        ticker, "10-Q", "prior_period_xbrl_instance",
        cutoff=payload["cutoff"], fixtures_root=cutoff_guard.FIXTURES)}
    rescued = [entry for entry in payload["notes"] if entry["verbatim_topic"]
               and (entry["note"], entry["text"]) in prior]
    assert rescued, f"{ticker}: the always-verbatim list changed nothing"


def test_the_always_verbatim_list_is_the_input_specs_list():
    assert set(diff_periods.ALWAYS_VERBATIM) == {
        "contingencies_and_litigation", "subsequent_events", "related_parties",
        "debt_and_covenants", "accounting_changes_and_corrections"}
    assert diff_periods.always_verbatim(
        "us-gaap:CommitmentsAndContingenciesDisclosureTextBlock") == \
        "contingencies_and_litigation"
    assert diff_periods.always_verbatim("us-gaap:SubsequentEventsTextBlock") == \
        "subsequent_events"
    assert diff_periods.always_verbatim("us-gaap:DebtDisclosureTextBlock") == \
        "debt_and_covenants"
    assert diff_periods.always_verbatim("us-gaap:RevenueFromContractWithCustomerTextBlock") \
        is None


def test_a_note_about_debt_securities_is_not_a_note_about_debt():
    """`DebtSecuritiesAvailableForSale…` is an investments note. Read as one run
    of letters it contains 'debt' and pulled 410 of NVIDIA's 596 rescued
    paragraphs in with it, so the name is read as words and `debt` is anchored."""
    assert diff_periods.words_of("us-gaap:DebtDisclosureTextBlock") == \
        "us gaap debt disclosure text block"
    assert diff_periods.always_verbatim(
        "us-gaap:DebtSecuritiesAvailableForSaleTextBlock") is None
    payload = diff_periods.extract("QCOM")
    sentence = "Debt securities with no single maturity date included"
    hits = [entry for entry in payload["notes"] if sentence in entry["text"]]
    assert hits, "the named paragraph is no longer in the filing"
    assert hits[0]["verbatim_topic"] is None
    assert hits[0]["kind"] == "collapsed"


def test_a_topic_is_matched_on_the_paragraphs_own_words_too():
    """The topics are not only notes. Esterline's one contingencies paragraph in
    the whole input is in MD&A, which carries no tag to read."""
    assert diff_periods.always_verbatim(
        "mdna", "We are party to various legal proceedings arising in the "
                "ordinary course of business.") == "contingencies_and_litigation"
    assert diff_periods.always_verbatim(
        "mdna", "Revenues increased in every region.") is None


def test_esterlines_one_contingencies_paragraph_reaches_the_file():
    """It is in MD&A, not in a note, and it was a placeholder."""
    text = assemble_bundle.build("ESE", "10-Q")["texts"]["input_mdna.md"]
    assert text.count("As a normal incident of the business") == 1


def test_apples_three_pronouncement_paragraphs_reach_the_file():
    """Two of the three name the standard as `ASU No. 2024-03` and the third
    spells out `Accounting Standards Update`. All three are the same topic."""
    payload = diff_periods.extract("AAPL")
    hits = [entry for entry in payload["mdna"]
            if "FASB" in entry["text"] and "ASU" in entry["text"]]
    assert len(hits) == 3, [entry["id"] for entry in hits]
    for entry in hits:
        assert entry["verbatim_topic"] == "accounting_changes_and_corrections"
        assert entry["kind"] == "verbatim"


def test_masking_takes_out_numbers_and_nothing_else():
    assert diff_periods.mask("Revenue was $1,234.5 million") == "revenue was $# million"
    assert diff_periods.mask("Revenue was $9,999.9 million") == "revenue was $# million"
    assert diff_periods.mask("three- and nine-month") != diff_periods.mask("three- and six-month")


def test_the_first_period_carries_everything():
    """With nothing to compare against, nothing collapses."""
    entries = [{"id": "a:notes:1", "text": "unchanged text", "note": "n",
                "verbatim_topic": None}]
    prior = [{"id": "b:notes:1", "text": "unchanged text", "note": "n"}]
    assert diff_periods.diff_stream(entries, [])[0]["kind"] == "verbatim"
    assert diff_periods.diff_stream(entries, prior)[0]["kind"] == "collapsed"


def test_one_prior_paragraph_stands_for_one_current_paragraph():
    """A note that prints the same row twice this quarter and once last quarter
    collapses one and carries the other. A set cannot tell those apart."""
    current = [{"id": "a:notes:1", "text": "same row", "note": "n",
                "verbatim_topic": None},
               {"id": "a:notes:2", "text": "same row", "note": "n",
                "verbatim_topic": None}]
    prior = [{"id": "b:notes:1", "text": "same row", "note": "n"}]
    kinds = [entry["kind"] for entry in diff_periods.diff_stream(current, prior)]
    assert kinds == ["collapsed", "verbatim"]


def test_the_counterpart_has_to_be_in_the_same_note():
    """Boilerplate that moved from one note to another is new where it lands."""
    current = [{"id": "a:notes:1", "text": "shared boilerplate", "note": "note_one",
                "verbatim_topic": None}]
    prior = [{"id": "b:notes:1", "text": "shared boilerplate", "note": "note_two"}]
    assert diff_periods.diff_stream(current, prior)[0]["kind"] == "verbatim"


def test_the_differ_goes_through_the_cutoff_gate():
    with pytest.raises(cutoff_guard.CutoffViolationError):
        diff_periods.extract("AAPL", cutoff=dt.date(2020, 1, 1))
