"""The expected values name their sources, and the drift baseline stays apart.

The parsers arrived with one file per company called `expected.json`, holding
both an answer key and a drift baseline, and the answer key had been produced by
running the parsers it judged. That is the hole this checks stays closed.

Two files now, for two different jobs. `expected_values.json` holds expectations
and every one carries a one-line note saying where it came from; a bare number
cannot be written into it, because the shape has no room for one and
`tests/expected_values.py` refuses to return a value without a source.
`expected.json` holds the extraction-drift baseline `src/extraction_checks.py`
reads, which is the pipeline's own output on purpose — "has this moved?" is a
question you ask of a previous run. Nothing in it is an expected value, so
nothing here may reach into it for a correctness assertion.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.fetch_fixtures import TICKERS
from tests import expected_values

FIXTURES = Path(__file__).resolve().parent / "fixtures"
FORMS = ("10-K", "10-Q")


def baseline(ticker: str) -> dict:
    return json.loads((FIXTURES / ticker / "expected.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("ticker", TICKERS)
def test_every_expected_value_names_where_it_came_from(ticker):
    """Flat, and one shape at every leaf: `{value, from}` with a note in it.

    Flatness is the point. There is no depth at which a bare number can hide, so
    the check is one loop and it cannot miss a branch.
    """
    entries = expected_values.entries(ticker)
    assert entries, f"{ticker}: no expected values at all"
    for key, entry in entries.items():
        assert isinstance(entry, dict), f"{ticker} {key}: not an object"
        assert set(entry) == {"value", "from"}, \
            f"{ticker} {key}: members are {sorted(entry)}"
        assert str(entry["from"]).strip(), f"{ticker} {key}: the source note is empty"
        # The reader is the only way in, so it is what the shape is checked
        # through: a file this passes is a file every test can read.
        assert expected_values.value(ticker, key) == entry["value"]
        assert expected_values.source(ticker, key) == entry["from"]


def test_the_twelve_companies_expect_the_same_things():
    """A company cannot quietly lose an expectation. One key set, twelve files."""
    first, *rest = TICKERS
    keys = set(expected_values.entries(first))
    for ticker in rest:
        assert set(expected_values.entries(ticker)) == keys, \
            f"{ticker} differs from {first}: " \
            f"{sorted(keys ^ set(expected_values.entries(ticker)))}"


@pytest.mark.parametrize("ticker", TICKERS)
def test_a_deleted_expectation_is_absent_rather_than_softened(ticker):
    """The values this project could not source are gone, not widened.

    Each of these was a count of what survived a parser's own rules — the drop
    rules, the similarity floor, the table-matching rule — so re-deriving one
    means restating the rule it judges. Naming them here is what stops the next
    reader from putting one back by hand.
    """
    gone = [
        "bundle.10-K.paragraphs", "bundle.10-K.notes", "bundle.10-K.mdna",
        "bundle.10-K.note_history", "bundle.10-K.controls",
        "bundle.10-Q.paragraphs", "bundle.10-Q.notes", "bundle.10-Q.mdna",
        "bundle.10-Q.note_history", "bundle.10-Q.controls",
        "cleaner.10-K.tables_already_in_xbrl", "cleaner.10-Q.tables_already_in_xbrl",
        "earnings_release.8-K.exhibit_99_1_paragraphs",
        "note_history.10-Q.added", "note_history.10-Q.removed",
        "note_history.10-Q.changed",
        "prior_period_diff.10-Q.carried_verbatim", "prior_period_diff.10-Q.collapsed",
    ]
    entries = expected_values.entries(ticker)
    assert not [key for key in gone if key in entries]
    for key in gone:
        with pytest.raises(KeyError):
            expected_values.value(ticker, key)


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_drift_baseline_holds_nothing_but_the_baseline(ticker):
    """`expected.json` is not an answer key and may not be read as one.

    It is the pipeline's own output, so anything left in it is something a
    correctness test could reach for and certify the parsers with. Only the
    counts the drift band still has a source for stay.
    """
    recorded = baseline(ticker)
    assert set(recorded) == {"_what_this_is", "bundle"}
    assert recorded["_what_this_is"].strip()
    assert set(recorded["bundle"]) == set(FORMS)
    for form in FORMS:
        assert set(recorded["bundle"][form]) == {"eight_k"}


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form", FORMS)
def test_the_drift_baseline_mirrors_the_value_that_carries_the_provenance(ticker, form):
    """One number, written twice because two readers need it in two places. The
    copy `src/extraction_checks.py` reads has to stay in step with the copy that
    says where it came from."""
    assert baseline(ticker)["bundle"][form]["eight_k"] == \
        expected_values.value(ticker, f"bundle.{form}.eight_k")


def test_the_reader_refuses_a_value_that_names_no_source(tmp_path):
    """The guarantee, exercised rather than asserted about: a number written
    without a note cannot be read back out, whatever it is worth."""
    folder = tmp_path / "NOPE"
    folder.mkdir()
    (folder / "expected_values.json").write_text(json.dumps({
        "sourced.10-K.count": {"value": 3, "from": "the filing, read by eye"},
        "bare.10-K.count": 3,
        "blank.10-K.count": {"value": 3, "from": "   "},
        "extra.10-K.count": {"value": 3, "from": "somewhere", "note": "and more"},
    }), encoding="utf-8")

    original = expected_values.FIXTURES
    expected_values.FIXTURES = tmp_path
    expected_values.entries.cache_clear()
    try:
        assert expected_values.value("NOPE", "sourced.10-K.count") == 3
        for key in ("bare.10-K.count", "blank.10-K.count", "extra.10-K.count"):
            with pytest.raises(ValueError):
                expected_values.value("NOPE", key)
        with pytest.raises(KeyError):
            expected_values.value("NOPE", "absent.10-K.count")
    finally:
        expected_values.FIXTURES = original
        expected_values.entries.cache_clear()
