"""What the diff layer is allowed to do: carry a paragraph, or replace it.

There is no third outcome, and the test that says so is parameterised over all
twelve companies' real pairs of 10-Qs. The two behaviours the rule turns on —
a paragraph that differs only in its numbers collapses, a paragraph that
differs in a word does not — are asserted on named paragraphs from named
filings, because that distinction is the whole layer.
"""

from __future__ import annotations

import datetime as dt
import json
import re
from pathlib import Path

import pytest

from src import cutoff_guard, diff_periods, extract_notes
from src.fetch_fixtures import TICKERS
from tests import independent_text

FIXTURES = Path(__file__).resolve().parent / "fixtures"
PLACEHOLDER = re.compile(r"^\[same as prior period, (\d+) periods running\]$")


def expected(ticker: str) -> dict:
    return json.loads((FIXTURES / ticker / "expected.json").read_text())


def current_sources(ticker: str, cutoff) -> independent_text.Source:
    """Everything the current 10-Q says: its HTML, and the HTML inside its notes."""
    row = cutoff_guard.one_document(ticker, "10-Q", "primary_html")
    parts = [cutoff_guard.load_document(row["full_path"], cutoff)]
    parts += [section["html"] for section in
              extract_notes.extract(ticker, "10-Q", cutoff=cutoff)["sections"]]
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
    for entry in payload["notes"] + payload["mdna"]:
        if entry["kind"] == "collapsed":
            match = PLACEHOLDER.match(entry["line"])
            assert match is not None, entry["line"]
            assert int(match.group(1)) >= 2
        else:
            assert entry["kind"] == "verbatim"


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_collapsed_and_carried_counts(ticker):
    payload = diff_periods.extract(ticker)
    record = expected(ticker)["prior_period_diff"]["10-Q"]
    assert payload["collapsed"] == record["collapsed"]
    assert payload["carried"] == record["carried_verbatim"]
    assert payload["prior_accession"] == record["prior_accession"]


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_counts_survive_an_independent_recount(ticker):
    """Mask the numbers with a different regex, pair the two periods by hand."""
    payload = diff_periods.extract(ticker)
    prior = diff_periods._note_paragraphs(
        ticker, "10-Q", "prior_period_xbrl_instance",
        cutoff=payload["cutoff"], fixtures_root=cutoff_guard.FIXTURES)
    seen = {re.sub(r"\s+", " ", re.sub(r"[0-9][0-9,.]*", "#", entry["text"])).strip().lower()
            for entry in prior}
    collapsed = 0
    for entry in payload["notes"]:
        if entry["verbatim_topic"] is not None:
            continue
        flat = re.sub(r"\s+", " ", re.sub(r"[0-9][0-9,.]*", "#", entry["text"])).strip().lower()
        collapsed += flat in seen
    assert collapsed == sum(1 for entry in payload["notes"]
                            if entry["kind"] == "collapsed")


def test_a_paragraph_that_differs_only_in_a_number_is_collapsed():
    """Qualcomm's Level 1 footnote is '(1) …' one quarter and '(2) …' the next.
    Same sentence, different number: collapsed."""
    payload = diff_periods.extract("QCOM")
    sentence = ("Other investments and other liabilities included in Level 1 are "
                "comprised of our deferred compensation plan assets and liabilities.")
    hits = [entry for entry in payload["notes"] if sentence in entry["text"]]
    assert hits, "the named paragraph is no longer in the filing"
    assert hits[0]["text"].startswith("(2)")
    assert hits[0]["kind"] == "collapsed"
    assert hits[0]["line"] == "[same as prior period, 2 periods running]"


def test_a_paragraph_that_differs_in_a_word_is_carried_verbatim():
    """Apple's earnings-per-share lead-in reads 'three- and nine-month periods'
    this quarter and 'three- and six-month periods' last quarter. Masking the
    numbers does not make 'nine' into 'six', so it is carried."""
    payload = diff_periods.extract("AAPL")
    hits = [entry for entry in payload["notes"]
            if entry["text"].startswith("The following table shows the computation of "
                                        "basic and diluted earnings per share")]
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
    prior = {diff_periods.mask(entry["text"]) for entry in diff_periods._note_paragraphs(
        ticker, "10-Q", "prior_period_xbrl_instance",
        cutoff=payload["cutoff"], fixtures_root=cutoff_guard.FIXTURES)}
    rescued = [entry for entry in payload["notes"]
               if entry["verbatim_topic"] and diff_periods.mask(entry["text"]) in prior]
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


def test_masking_takes_out_numbers_and_nothing_else():
    assert diff_periods.mask("Revenue was $1,234.5 million") == "revenue was $# million"
    assert diff_periods.mask("Revenue was $9,999.9 million") == "revenue was $# million"
    assert diff_periods.mask("three- and nine-month") != diff_periods.mask("three- and six-month")


def test_the_first_period_carries_everything():
    """With nothing to compare against, nothing collapses."""
    entries = [{"id": "a:notes:1", "text": "unchanged text", "note": "n",
                "verbatim_topic": None}]
    assert diff_periods.diff_stream(entries, [])[0]["kind"] == "verbatim"
    assert diff_periods.diff_stream(entries, ["unchanged text"])[0]["kind"] == "collapsed"


def test_the_differ_goes_through_the_cutoff_gate():
    with pytest.raises(cutoff_guard.CutoffViolationError):
        diff_periods.extract("AAPL", cutoff=dt.date(2020, 1, 1))
