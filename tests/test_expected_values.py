"""The expected values name their sources, and the drift baseline stays apart.

The parsers arrived with one file per company called `expected.json`, holding
both an answer key and a drift baseline, and the answer key had been produced by
running the parsers it judged. That is the hole this checks stays closed.

Two files now, for two different jobs. `expected_values.json` holds expectations
and every one carries a one-line note saying where it came from; a bare number
cannot be written into it, because the shape has no room for one, and a note that
names no source this project has — or cites a file that is not there — cannot be
read back out either. `expected.json` holds the extraction-drift baseline
`src/extraction_checks.py` reads, which is the pipeline's own output on purpose:
"has this moved?" is a question you ask of a previous run. Nothing in it is an
expected value, so nothing here may reach into it for a correctness assertion —
and the two files disagree wherever a parser defect is on record, which is the
clearest possible statement that one of them is not an answer key.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src import extraction_checks
from src.fetch_fixtures import TICKERS
from tests import expected_values

FIXTURES = Path(__file__).resolve().parent / "fixtures"
FORMS = ("10-K", "10-Q")
BASELINE_COUNTS = {"controls", "eight_k", "mdna", "note_history", "notes", "paragraphs"}


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
        wrong = expected_values.unsourced(str(entry["from"]))
        assert not wrong, f"{ticker} {key}: {wrong}"
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


# Counts of what survived a parser's own rules — the drop rules, the similarity
# floor, the table-matching rule — so re-deriving one means restating the rule it
# judges. Naming them here is what stops the next reader putting one back by hand.
UNSOURCEABLE = (
    "bundle.10-K.paragraphs", "bundle.10-K.notes", "bundle.10-K.mdna",
    "bundle.10-K.note_history", "bundle.10-K.controls",
    "bundle.10-Q.paragraphs", "bundle.10-Q.notes", "bundle.10-Q.mdna",
    "bundle.10-Q.note_history", "bundle.10-Q.controls",
    "cleaner.10-K.tables_already_in_xbrl", "cleaner.10-Q.tables_already_in_xbrl",
    "earnings_release.8-K.exhibit_99_1_paragraphs",
    "note_history.10-Q.added", "note_history.10-Q.removed", "note_history.10-Q.changed",
    "prior_period_diff.10-Q.carried_verbatim", "prior_period_diff.10-Q.collapsed",
)

# Not deleted — re-sourced into a shape that can fail. A count of key notes
# agreed with the parser in all twelve while naming a different set of tags in
# five of them, because a count cannot see a wrong pairing. The tag lists can,
# and both counts are derived from them in `tests/test_note_history.py`.
COUNTED_THE_PARSERS_WAY = ("note_history.10-Q.key_notes", "note_history.10-Q.match_rules")
THE_TAG_LISTS_INSTEAD = ("note_history.10-Q.key_note_tags",
                         "note_history.10-Q.prior_key_note_tags")


@pytest.mark.parametrize("ticker", TICKERS)
def test_a_deleted_expectation_is_absent_rather_than_softened(ticker):
    """The values this project could not source are gone, not widened."""
    entries = expected_values.entries(ticker)
    for key in UNSOURCEABLE + COUNTED_THE_PARSERS_WAY:
        assert key not in entries, f"{ticker}: {key} is back"
        with pytest.raises(KeyError):
            expected_values.value(ticker, key)
    for key in THE_TAG_LISTS_INSTEAD:
        assert expected_values.value(ticker, key)


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_drift_baseline_holds_nothing_but_bundle_counts(ticker):
    """`expected.json` is not an answer key and may not be read as one.

    It is the pipeline's own output, and the ±20% band is the only question it
    answers. What keeps it from being mistaken for an expectation is that it
    carries no provenance and nothing here compares it to a filing.
    """
    recorded = baseline(ticker)
    assert set(recorded) == {"_what_this_is", "bundle"}
    assert recorded["_what_this_is"].strip()
    assert set(recorded["bundle"]) == set(FORMS)
    for form in FORMS:
        assert set(recorded["bundle"][form]) == BASELINE_COUNTS
        # Read off the gate rather than restated: `check_counts` skips a count it
        # has no reference for, so a reference deleted from here is a gate that
        # silently stops checking. Five of the six went that way once.
        assert set(recorded["bundle"][form]) >= set(extraction_checks.COUNTED)


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form", FORMS)
def test_the_baseline_is_never_below_the_eight_k_the_exhibit_was_read_to_hold(
        ticker, form):
    """The two files hold the same 8-K count from two directions, and the gap
    between them is a parser defect, not noise.

    `expected_values.json` says how many paragraphs the exhibit *should* put in
    the bundle: blocks the exhibit was read block by block to hold, less the page
    furniture and safe-harbour boilerplate `docs/INPUT_SPEC.md` says to strip,
    plus the tables. `expected.json` says how many the pipeline actually put
    there. The cleaner under-drops, so the baseline is the higher of the two and
    never the lower — a baseline below the hand count would mean paragraphs going
    missing, which is the failure nobody would see in a ±20% band.
    """
    recorded = baseline(ticker)["bundle"][form]["eight_k"]
    by_hand = expected_values.value(ticker, f"bundle.{form}.eight_k")
    assert recorded >= by_hand, f"{ticker} {form}: the bundle lost 8-K paragraphs"


def test_the_reader_refuses_a_value_that_names_no_source(tmp_path):
    """The guarantee, exercised rather than asserted about: a number written
    without a note cannot be read back out, whatever it is worth — and neither
    can one whose note is prose, cites a line number, or names a file that is
    not there. "Non-empty" was the check that let a relabelled number through.
    """
    folder = tmp_path / "NOPE"
    folder.mkdir()
    (folder / "expected_values.json").write_text(json.dumps({
        "sourced.10-K.count": {"value": 3, "from": "the filing, read by eye"},
        "anchored.10-K.count": {
            "value": 3, "from": "already judged: tests/expected_values.py::unsourced"},
        "bare.10-K.count": 3,
        "blank.10-K.count": {"value": 3, "from": "   "},
        "extra.10-K.count": {"value": 3, "from": "somewhere", "note": "and more"},
        "prose.10-K.count": {"value": 3, "from": "somewhere, honestly"},
        "line.10-K.count": {"value": 3, "from": "read by eye at tests/test_parse_8k.py:119"},
        "absent.10-K.count": {"value": 3, "from": "read by eye in tests/no_such_file.py"},
        "anchorless.10-K.count": {
            "value": 3, "from": "read by eye in tests/expected_values.py::no_such_name"},
    }), encoding="utf-8")

    original = expected_values.FIXTURES
    expected_values.FIXTURES = tmp_path
    expected_values.entries.cache_clear()
    try:
        assert expected_values.value("NOPE", "sourced.10-K.count") == 3
        assert expected_values.value("NOPE", "anchored.10-K.count") == 3
        for key in ("bare.10-K.count", "blank.10-K.count", "extra.10-K.count",
                    "prose.10-K.count", "line.10-K.count", "absent.10-K.count",
                    "anchorless.10-K.count"):
            with pytest.raises(ValueError):
                expected_values.value("NOPE", key)
        with pytest.raises(KeyError):
            expected_values.value("NOPE", "missing.10-K.count")
    finally:
        expected_values.FIXTURES = original
        expected_values.entries.cache_clear()
