"""The note history is a change log, and every line of it came from a filing.

Three things are checked over all twelve companies' real pairs of 10-Qs: an
entry's text is a contiguous substring of one of the two filings, an unchanged
paragraph produces no entry at all (that is what "never several periods of full
text" means in practice), and how much moved per note survives being recomputed
by a different pairing written here.

The match rule is checked on constructed sections rather than on the fixtures,
because none of the twelve renamed an extension tag between these two quarters
— the fallback exists for a case the fixture set does not contain, and a rule
with no test is a rule that will be wrong the first time it fires.
"""

from __future__ import annotations

import datetime as dt
import re

import pytest

from src import cutoff_guard, diff_periods, extract_notes, note_history
from src.fetch_fixtures import TICKERS
from tests import independent_text
from tests.expected_values import value

# Written here rather than imported: the point is to mask the numbers with a
# regex `src/` does not own.
NUMBER = re.compile(r"[0-9][0-9,.]*")


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
    # A changed entry prints two paragraphs from two filings and so carries two
    # ids, one per filing. Every other kind carries one.
    changed = [entry for entry in payload["entries"] if entry["kind"] == "changed"]
    identifiers = {entry["id"] for entry in payload["entries"]}
    identifiers |= {entry["previous_id"] for entry in changed}
    assert len(identifiers) == len(payload["entries"]) + len(changed), \
        f"{ticker}: an id is repeated"
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


def key_sections(ticker: str, role: str | None = None) -> list[dict]:
    """The sections this parser calls key notes, in one of the two 10-Qs."""
    sections = extract_notes.extract(
        ticker, "10-Q", **({"role": role} if role else {}))["sections"]
    return [section for section in sections if note_history.key_note(section["name"])]


def key_paragraphs(ticker: str, role: str | None = None) -> dict[str, list[str]]:
    """Every key note's paragraphs, gathered by tag name."""
    out: dict[str, list[str]] = {}
    for section in key_sections(ticker, role):
        out.setdefault(section["name"], []).extend(note_history._paragraphs(section))
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


# --- (e) the recorded values ------------------------------------------------

# `KEY_NOTES["debt"]` matches the bare substring `debt`, so a note about debt
# securities the company *holds* is paired as the note about the debt it *owes*:
# `us-gaap:DebtSecuritiesAvailableForSale…` and `us-gaap:InvestmentsInDebtAnd
# MarketableEquitySecurities…`. Both are the investments note, and
# `docs/INPUT_SPEC.md` §5 asks for the note about what the company owes. Four of
# the twelve carry one or both.
#
# This stood on record for NVIDIA alone while the expected value was a *count*.
# CSCO, PANW and CIEN miss by exactly the same rule and their counts agreed with
# the parser anyway, because the tags read off the instance and the tags the
# parser paired differed by compensating amounts — 3 in and 3 out of CSCO's 13. A
# count cannot see a wrong pairing. The recorded value is the tag list now, so it
# can, and the defect is on record for the four companies it actually reaches.
# Strict, so narrowing the pattern turns these red and the marks come off.
BROAD_DEBT_MATCH = {
    "CSCO": "DebtSecuritiesAvailableForSaleUnrealizedLossPositionFairValueTable and "
            "InvestmentsInDebtAndMarketableEquitySecurities…; 11 read, 13 paired",
    "PANW": "DebtSecuritiesAvailableForSaleTable and InvestmentsInDebtAndMarketable"
            "EquitySecurities…; 6 read, 8 paired",
    "CIEN": "InvestmentsInDebtAndMarketableEquitySecurities…; 8 read, 9 paired",
    "NVDA": "DebtSecuritiesAvailableForSaleTable and InvestmentsInDebtAndMarketable"
            "EquitySecurities…; 4 read, 6 paired",
}


def key_tags(ticker: str, role: str | None = None) -> list[str]:
    """The names of those sections, which is what the instance can source."""
    return sorted(section["name"] for section in key_sections(ticker, role))


@pytest.mark.parametrize("ticker", [
    pytest.param(ticker, marks=pytest.mark.xfail(
        strict=True, reason=f"{ticker}: {BROAD_DEBT_MATCH[ticker]}"))
    if ticker in BROAD_DEBT_MATCH else ticker
    for ticker in TICKERS])
def test_the_key_notes_are_the_tags_the_two_instances_hold(ticker):
    """Which notes are key notes, and what that makes the pairing.

    The expected value is the *list of tag names*, read off each instance with
    ElementTree and marked against the six topics `docs/INPUT_SPEC.md` §5 names.
    It was a count, and a count of the right size over the wrong set is a test
    that passes while the parser is wrong — which is what it was doing in five
    companies. The counts below are derived from the two lists rather than
    recorded, so there is one reading and one place to disagree with it.

    The added / removed / changed split is not here and is not recorded anywhere:
    where the line falls between "added" and "changed" is set by
    `CHANGED_SIMILARITY_FLOOR` over number-masked text — a tuning parameter, not a
    fact about the filings — so a reader would disagree with a *correct* parser at
    the margin, and nobody reads 43 changed pairs off a page. The recount below
    pins added+changed and removed+changed note by note instead, with no expected
    value at all.
    """
    current = value(ticker, "note_history.10-Q.key_note_tags")
    prior = value(ticker, "note_history.10-Q.prior_key_note_tags")
    assert key_tags(ticker) == current
    assert key_tags(ticker, "prior_period_xbrl_instance") == prior

    # Pair by tag name, which is all the two lists can say; the title fallback
    # fires for none of the twelve, because none renamed an extension tag.
    shared = [tag for tag in current if tag in prior]
    rules = {"tag_name": len(shared)}
    if len(current) > len(shared):
        rules[note_history.NO_PRIOR_NOTE] = len(current) - len(shared)
    if len(prior) > len(shared):
        rules[note_history.NO_CURRENT_NOTE] = len(prior) - len(shared)

    payload = note_history.history(ticker)
    assert payload["key_notes"] == len(current) + len(prior) - len(shared)
    assert {rule: count for rule, count in payload["match_rules"].items() if count} \
        == rules


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_history_names_the_prior_report_the_index_names(ticker):
    """Its own test, for all twelve. A strict xfail is satisfied by any failure,
    so while this assertion shared a test with the pairing above, NVIDIA's mark
    meant nobody ever evaluated it there."""
    assert note_history.history(ticker)["prior_accession"] == \
        value(ticker, "note_history.10-Q.prior_accession")


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_counts_survive_an_independent_recount(ticker):
    """Pair the two periods by tag name here, mask the numbers with the regex
    written above, and count per note what each side does not have.

    A paragraph the other side lacks is either `added` or `changed`, and the
    recount cannot tell which without restating the similarity rule — so it
    pins the two sums, note by note, and nothing pins the split, because
    nothing outside the parser can source it. That is the honest limit of an
    independent count of this layer: it cannot be fooled about how much moved,
    only about how the movement was labelled."""
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


# --- an id names the filing its text came from -------------------------------
#
# Every entry used to be minted from the current accession, so a `removed`
# paragraph — which is the *prior* filing's text, and is in the file precisely
# because it is not in the current one — was published under a current-period
# id. A reader checking that quote against the filing the id names would not
# find it. AAPL 7 removed and 8 changed, CSCO 24 and 76, NVDA 123 and 22.

@pytest.mark.parametrize("ticker", TICKERS)
def test_an_entrys_id_names_the_filing_its_text_came_from(ticker):
    payload = note_history.history(ticker)
    now, before = payload["accession"], payload["prior_accession"]
    assert now != before
    current = independent_text.Source("\n".join(
        section["html"] for section in extract_notes.extract(ticker, "10-Q")["sections"]))
    prior = independent_text.Source("\n".join(
        section["html"] for section in extract_notes.extract(
            ticker, "10-Q", role="prior_period_xbrl_instance")["sections"]))
    for entry in payload["entries"]:
        named = before if entry["kind"] == "removed" else now
        assert entry["id"].startswith(named), f"{ticker}: {entry['kind']} {entry['id']}"
        holder = prior if entry["kind"] == "removed" else current
        assert all(holder.contains(piece)
                   for piece in independent_text.quotable(entry["text"])), \
            f"{ticker}: {entry['id']} is not in the filing it names"


@pytest.mark.parametrize("ticker", TICKERS)
def test_a_changed_entry_carries_an_id_for_each_of_its_two_paragraphs(ticker):
    payload = note_history.history(ticker)
    changed = [entry for entry in payload["entries"] if entry["kind"] == "changed"]
    assert changed, f"{ticker}: nothing changed, so the rule is untested"
    rendered = note_history.render(payload)
    for entry in changed:
        assert entry["previous_id"].startswith(payload["prior_accession"])
        assert entry["previous_id"] != entry["id"]
        assert f"[{entry['previous_id']}]" in rendered
