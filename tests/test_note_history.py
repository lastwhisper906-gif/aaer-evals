"""The note history is a change log, and every line of it came from a filing.

Three things are checked over all twelve companies' real pairs of 10-Qs: an
entry's text is a contiguous substring of one of the two filings, an unchanged
paragraph produces no entry at all (that is what "never several periods of full
text" means in practice), and the three counts survive being recomputed by a
different pairing written here.

The match rule is checked on constructed sections rather than on the fixtures,
because none of the twelve renamed an extension tag between these two quarters
— the fallback exists for a case the fixture set does not contain, and a rule
with no test is a rule that will be wrong the first time it fires.
"""

from __future__ import annotations

import datetime as dt
import json
import re
from pathlib import Path

import pytest

from src import cutoff_guard, diff_periods, extract_notes, note_history
from src.fetch_fixtures import TICKERS
from tests import independent_text

FIXTURES = Path(__file__).resolve().parent / "fixtures"
# Written here rather than imported: the point is to mask the numbers with a
# regex `src/` does not own.
NUMBER = re.compile(r"[0-9][0-9,.]*")


def expected(ticker: str) -> dict:
    return json.loads((FIXTURES / ticker / "expected.json").read_text())


def sources(ticker: str) -> independent_text.Source:
    """Both filings' notes, stripped once by the second stripper."""
    parts = [section["html"] for section in
             extract_notes.extract(ticker, "10-Q")["sections"]]
    parts += [section["html"] for section in extract_notes.extract(
        ticker, "10-Q", role="prior_period_xbrl_instance")["sections"]]
    return independent_text.Source("\n".join(parts))


def flat_mask(text: str) -> str:
    return re.sub(r"\s+", " ", NUMBER.sub("#", text)).strip().lower()


# --- (b) every emitted paragraph is one of the two filings' own text --------

@pytest.mark.parametrize("ticker", TICKERS)
def test_every_entry_is_a_substring_of_one_of_the_two_filings(ticker):
    payload = note_history.history(ticker)
    source = sources(ticker)
    emitted = [entry["text"] for entry in payload["entries"]]
    emitted += [entry["previous_text"] for entry in payload["entries"]
                if entry["kind"] == "changed"]
    missing = source.missing(emitted)
    assert not missing, f"{ticker}: {missing[:1]}"


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_rendered_file_holds_nothing_but_entries_and_headings(ticker):
    """(b) again, on the file itself: every line is either the change log's own
    scaffolding or a paragraph out of one of the two filings."""
    payload = note_history.history(ticker)
    source = sources(ticker)
    identifiers = {entry["id"] for entry in payload["entries"]}
    assert len(identifiers) == len(payload["entries"]), f"{ticker}: an id is repeated"
    stray, seen = [], set()
    for line in note_history.render(payload).split("\n"):
        if not line.strip() or line.startswith(("#", "- ", "  (was")):
            continue
        if line.startswith("[") and line[1:-1] in identifiers:
            seen.add(line[1:-1])
            continue
        # A rendered table row is not a run of the filing's characters and
        # cannot be — its separators are this pipeline's — so the claim is made
        # of every cell instead. Nothing is skipped either way.
        if not all(source.contains(piece)
                   for piece in independent_text.quotable(line)):
            stray.append(line)
    assert not stray, f"{ticker}: {stray[:1]}"
    assert seen == identifiers, f"{ticker}: an entry reached the file with no id"


def key_paragraphs(ticker: str, role: str | None = None) -> dict[str, list[str]]:
    """Every key note's paragraphs, gathered by tag name."""
    sections = extract_notes.extract(
        ticker, "10-Q", **({"role": role} if role else {}))["sections"]
    out: dict[str, list[str]] = {}
    for section in sections:
        if note_history.key_note(section["name"]):
            out.setdefault(section["name"], []).extend(
                note_history._paragraphs(section))
    return out


def test_apples_unchanged_litigation_paragraph_is_not_in_the_history():
    """Apple says the same thing about ordinary-course legal proceedings both
    quarters. A change log that repeated it would be two periods of full text,
    which is the one thing the spec forbids here. (The paragraph is still
    carried whole into `input_notes.md` — that is `diff_periods`' job, and its
    always-verbatim list is why contingencies survive there.)"""
    payload = note_history.history("AAPL")
    opening = ("The Company is subject to various legal proceedings and claims "
               "that have arisen in the ordinary course of business")
    prior = key_paragraphs("AAPL", "prior_period_xbrl_instance")
    carried = [text for text in
               prior["us-gaap:CommitmentsAndContingenciesDisclosureTextBlock"]
               if text.startswith(opening)]
    assert carried, "the named paragraph is no longer in the prior filing"
    assert not [entry for entry in payload["entries"]
                if entry["text"].startswith(opening)]


@pytest.mark.parametrize("ticker", TICKERS)
def test_only_the_six_key_notes_are_in_the_history(ticker):
    payload = note_history.history(ticker)
    assert payload["entries"], f"{ticker}: nothing at all"
    for entry in payload["entries"]:
        assert entry["key_note"] in note_history.KEY_NOTES, entry["note"]


# --- (c) every entry says which rule matched its note -----------------------

@pytest.mark.parametrize("ticker", TICKERS)
def test_every_entry_is_labelled_with_a_match_rule(ticker):
    payload = note_history.history(ticker)
    for entry in payload["entries"]:
        assert entry["matched_by"] in note_history.MATCH_RULES, entry
        if entry["matched_by"] == "tag_name":
            assert entry["match_score"] == 1.0
        elif entry["matched_by"] == "title_similarity":
            assert entry["match_score"] >= note_history.TITLE_SIMILARITY_FLOOR
        else:
            # Nothing to match against, so no score to record.
            assert entry["match_score"] == 0.0


def test_the_unmatched_labels_name_the_direction():
    """QCOM's short-term debt schedule is new this quarter; Generac dropped a
    note it had last quarter. Both are changes a reader wants; neither is a
    match, and the label says which way it went."""
    new_note = note_history.history("QCOM")
    appeared = {entry["note"] for entry in new_note["entries"]
                if entry["matched_by"] == note_history.NO_PRIOR_NOTE}
    assert "us-gaap:ScheduleOfShortTermDebtTextBlock" in appeared
    for entry in new_note["entries"]:
        if entry["matched_by"] == note_history.NO_PRIOR_NOTE:
            assert entry["kind"] == "added"

    gone = note_history.history("GNRC")
    vanished = [entry for entry in gone["entries"]
                if entry["matched_by"] == note_history.NO_CURRENT_NOTE]
    assert vanished, "GNRC no longer drops a key note"
    for entry in vanished:
        assert entry["kind"] == "removed"


# --- (d) the constructed rename ---------------------------------------------

def section(name: str, title: str, body: str) -> dict:
    return {"name": name, "text": f"{title}\n\n{body}\n", "html": ""}


def test_a_renamed_extension_tag_matches_on_its_title_and_says_so():
    """The case the fixture set does not contain: the company retires
    `panw:SeventhNoteDebt…` for `panw:EighthNoteDebt…` and keeps the heading."""
    body = "The Company had $500.0 million of notes payable outstanding."
    current = [section("pnw:EighthNoteDebtTextBlock", "Note 8 — Debt", body)]
    prior = [section("pnw:SeventhNoteDebtTextBlock", "Note 7 — Debt", body)]

    pairs = note_history.match_notes(current, prior)
    assert len(pairs) == 1
    assert pairs[0]["matched_by"] == "title_similarity"
    assert pairs[0]["score"] >= note_history.TITLE_SIMILARITY_FLOOR
    assert pairs[0]["prior"] is prior[0]


def test_the_title_fallback_does_not_pair_two_unrelated_notes():
    current = [section("pnw:EighthNoteDebtTextBlock", "Note 8 — Debt", "a")]
    prior = [section("pnw:SecondNoteRevenueTextBlock",
                     "Note 2 — Revenue from Contracts with Customers", "b")]
    pairs = note_history.match_notes(current, prior)
    assert pairs[0]["matched_by"] == note_history.NO_PRIOR_NOTE
    assert pairs[1]["matched_by"] == note_history.NO_CURRENT_NOTE


def test_the_tag_name_is_tried_before_the_title():
    """Same tag, rewritten heading: still a tag-name match, score 1.0."""
    current = [section("us-gaap:DebtDisclosureTextBlock", "Note 8 — Borrowings", "a")]
    prior = [section("us-gaap:DebtDisclosureTextBlock", "Note 4 — Debt", "b")]
    pairs = note_history.match_notes(current, prior)
    assert pairs[0]["matched_by"] == "tag_name"
    assert pairs[0]["score"] == 1.0


def test_the_six_key_notes_are_the_input_specs_six():
    assert set(note_history.KEY_NOTES) == {
        "revenue_recognition_policy", "critical_accounting_estimates",
        "contingencies", "debt", "related_parties", "subsequent_events"}
    assert note_history.key_note("us-gaap:DebtDisclosureTextBlock") == "debt"
    assert note_history.key_note("us-gaap:SubsequentEventsTextBlock") == "subsequent_events"
    assert note_history.key_note(
        "us-gaap:CommitmentsAndContingenciesDisclosureTextBlock") == "contingencies"
    assert note_history.key_note("us-gaap:IncomeTaxDisclosureTextBlock") is None


# --- (e) the recorded counts ------------------------------------------------

@pytest.mark.parametrize("ticker", TICKERS)
def test_the_added_removed_and_changed_counts(ticker):
    payload = note_history.history(ticker)
    record = expected(ticker)["note_history"]["10-Q"]
    assert payload["counts"]["added"] == record["added"]
    assert payload["counts"]["removed"] == record["removed"]
    assert payload["counts"]["changed"] == record["changed"]
    assert payload["key_notes"] == record["key_notes"]
    assert payload["prior_accession"] == record["prior_accession"]
    assert {rule: count for rule, count in payload["match_rules"].items() if count} \
        == record["match_rules"]


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_counts_survive_an_independent_recount(ticker):
    """Pair the two periods by tag name here, mask the numbers with the regex
    written above, and count per note what each side does not have.

    A paragraph the other side lacks is either `added` or `changed`, and the
    recount cannot tell which without restating the similarity rule — so it
    pins the two sums, note by note, and `expected.json` pins the split. That
    is the honest limit of an independent count of this layer: it cannot be
    fooled about how much moved, only about how the movement was labelled."""
    payload = note_history.history(ticker)
    current = key_paragraphs(ticker)
    prior = key_paragraphs(ticker, "prior_period_xbrl_instance")

    by_note: dict[str, dict[str, int]] = {}
    for entry in payload["entries"]:
        kinds = by_note.setdefault(entry["note"], {"added": 0, "removed": 0, "changed": 0})
        kinds[entry["kind"]] += 1

    shared_total = 0
    for tag in set(current) | set(prior):
        pool = [flat_mask(text) for text in prior.get(tag, [])]
        only_current = 0
        for masked in (flat_mask(text) for text in current.get(tag, [])):
            if masked in pool:
                pool.remove(masked)
                shared_total += 1
            else:
                only_current += 1
        kinds = by_note.get(tag, {"added": 0, "removed": 0, "changed": 0})
        assert only_current == kinds["added"] + kinds["changed"], f"{ticker} {tag}"
        assert len(pool) == kinds["removed"] + kinds["changed"], f"{ticker} {tag}"

    assert shared_total, f"{ticker}: nothing was carried unchanged at all"
    for kind in ("added", "removed", "changed"):
        assert sum(kinds[kind] for kinds in by_note.values()) == payload["counts"][kind]


@pytest.mark.parametrize("ticker", TICKERS)
def test_a_changed_entry_carries_the_paragraph_it_replaced(ticker):
    payload = note_history.history(ticker)
    changed = [entry for entry in payload["entries"] if entry["kind"] == "changed"]
    for entry in changed:
        assert entry["previous_text"]
        assert entry["previous_text"] != entry["text"]
        assert entry["score"] >= note_history.CHANGED_SIMILARITY_FLOOR
        assert entry["prior_period"] < entry["period"]


# --- the gate and the CLI ---------------------------------------------------

def test_the_history_goes_through_the_cutoff_gate():
    with pytest.raises(cutoff_guard.CutoffViolationError):
        note_history.history("AAPL", cutoff=dt.date(2020, 1, 1))


def test_the_command_writes_the_file(tmp_path):
    out = tmp_path / "input_notes_history.md"
    assert note_history.main(["--ticker", "aapl", "--out", str(out)]) == 0
    text = out.read_text(encoding="utf-8")
    assert text.startswith("# AAPL note change history — ")
    assert "matched_by: tag_name" in text


def test_the_always_verbatim_notes_are_carried_by_the_diff_layer_not_here():
    """The spec allows contingencies, related parties and subsequent events to
    be carried whole. They already are, by `diff_periods.ALWAYS_VERBATIM`;
    doing it twice would put full text in the file that must not have any."""
    assert {"contingencies_and_litigation", "subsequent_events", "related_parties"} \
        <= set(diff_periods.ALWAYS_VERBATIM)
