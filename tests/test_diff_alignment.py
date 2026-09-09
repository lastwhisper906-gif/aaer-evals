"""Pair first, then compare: three filings where nothing was disclosed anew.

`docs/INPUT_SPEC.md` §2 Alignment asks for three things in one order — pair a
section against its prior-period counterpart by tag name, falling back to title
similarity; match one paragraph list against the other as a multiset; score each
paragraph for boilerplate before it counts as a change — and states what they
buy: a reordered or retitled section yields zero changes.

The three fixtures below are built here, in the test, so a reader can see why
zero is the right answer without opening anything else:

* **reordered** — the same two notes and the same paragraphs, printed in
  another order. Every paragraph on one side is on the other, once each, and
  the test says so before it asserts the count.
* **retitled** — the company renumbered a note and changed the extension tag
  with it. The paragraphs are last quarter's, word for word.
* **a table of a hundred identical cells** — both quarters print the same
  hundred em dashes. Matching them against the *first* prior cell instead of
  one for one is the mistake this repository already made and wrote down
  (`lessons.md`, 2026-09-07): ninety-nine of them looked removed.

Zero is only worth asserting if something could have moved it, so every fixture
carries a positive control: one sentence added, one tag renamed past the floor,
one cell replaced by a sentence — each of which must move the count by exactly
the amount written out beside it.
"""

from __future__ import annotations

import pytest

from src import cutoff_guard, diff_periods, note_history

# Two notes as a filer prints them: a heading, prose, and rendered table rows.
INVENTORIES_TAG = "esterline:InventoriesTextBlock"
INVENTORIES = [
    "Inventories are stated at the lower of cost and net realizable value.",
    "| Inventories | June 30, 2025 | December 31, 2024 |",
    "| Raw materials | 1,204 | 1,180 |",
    "Inventory reserves are recorded for excess and obsolete inventory, based "
    "on historical usage and expected demand.",
]
REVENUE_TAG = "us-gaap:RevenueFromContractWithCustomerTextBlock"
REVENUE = [
    "Revenue is recognized when control of the promised goods transfers to the "
    "customer, in an amount that reflects the consideration expected.",
    "| Americas | 4,120 | 3,980 |",
    "Contract balances consist of receivables, contract assets and contract "
    "liabilities.",
]

# An em dash is what a filer prints in a cell with nothing in it, so a hundred
# of them in one table is an ordinary table and not a contrived one.
CELL = "—"
FAIR_VALUE_TAG = "us-gaap:FairValueDisclosuresTextBlock"


def section(name: str, title: str, paragraphs: list[str]) -> dict:
    return {"name": name, "title": title, "paragraphs": list(paragraphs)}


def texts(sections: list[dict]) -> list[str]:
    return [text for entry in sections for text in entry["paragraphs"]]


# --- fixture one: the same filing, reordered -------------------------------

def reordered() -> tuple[list[dict], list[dict]]:
    """The two notes swap places, and the inventories paragraphs are permuted."""
    prior = [section(INVENTORIES_TAG, "Note 4 — Inventories", INVENTORIES),
             section(REVENUE_TAG, "Note 5 — Revenue", REVENUE)]
    current = [section(REVENUE_TAG, "Note 5 — Revenue", REVENUE),
               section(INVENTORIES_TAG, "Note 4 — Inventories",
                       [INVENTORIES[2], INVENTORIES[0], INVENTORIES[3],
                        INVENTORIES[1]])]
    return current, prior


def test_a_reordered_filing_has_no_changes_in_it():
    current, prior = reordered()
    # Why zero: the two sides hold the same paragraphs, once each. Order is the
    # only difference, and a multiset has none.
    assert sorted(texts(current)) == sorted(texts(prior))
    assert texts(current) != texts(prior)

    result = diff_periods.changes(current, prior)
    assert result["count"] == 0
    assert result["entries"] == []
    # Nothing was excused as boilerplate either: there was nothing left over.
    assert result["boilerplate"] == []
    # Both sections paired on their own tag, so section order decided nothing.
    assert result["match_rules"]["tag_name"] == 2


def test_a_sentence_added_to_a_reordered_filing_is_the_one_change():
    """The positive control. Reordering hides nothing that was written."""
    current, prior = reordered()
    added = ("The Company recorded a charge of $18 million for excess "
             "inventory in the quarter.")
    current[1]["paragraphs"].append(added)

    result = diff_periods.changes(current, prior)
    assert result["count"] == 1
    assert result["entries"][0]["kind"] == "added"
    assert result["entries"][0]["text"] == added
    assert result["entries"][0]["note"] == INVENTORIES_TAG


# --- fixture two: the same filing, retitled --------------------------------

def retitled() -> tuple[list[dict], list[dict]]:
    """The inventories note is renumbered and its extension tag changes with it.

    Filers renumber notes every time one is added above them, and an extension
    tag carrying the old number goes with the number. The text is untouched.
    """
    prior = [section(INVENTORIES_TAG, "Note 4 — Inventories", INVENTORIES),
             section(REVENUE_TAG, "Note 5 — Revenue", REVENUE)]
    current = [section("esterline:InventoryNoteTextBlock",
                       "Note 5 — Inventories", INVENTORIES),
               section(REVENUE_TAG, "Note 6 — Revenue", REVENUE)]
    return current, prior


def test_a_retitled_section_has_no_changes_in_it():
    current, prior = retitled()
    # Why zero: the paragraphs are the prior filing's, word for word. What
    # changed is the tag and the heading, and a heading is not a paragraph.
    assert current[0]["paragraphs"] == prior[0]["paragraphs"]
    assert current[0]["name"] != prior[0]["name"]
    assert current[0]["title"] != prior[0]["title"]

    result = diff_periods.changes(current, prior)
    assert result["count"] == 0
    assert result["boilerplate"] == []
    # The tag it was filed under is gone, so the title is what paired it, and
    # the score that paired it clears the floor already on record.
    assert result["match_rules"] == {"tag_name": 1, "title_similarity": 1,
                                     "no_prior_section": 0, "no_current_section": 0}
    pairs = diff_periods.pair_sections(current, prior)
    assert pairs[0]["matched_by"] == "title_similarity"
    assert pairs[0]["score"] >= diff_periods.TITLE_SIMILARITY_FLOOR
    assert pairs[0]["prior"]["name"] == INVENTORIES_TAG


def test_a_section_with_no_counterpart_is_every_paragraph_of_both():
    """The positive control: a title similar to nothing pairs with nothing.

    A note that appeared and a note that went away are changes, and the count
    says so — four paragraphs added under the new heading, the same four
    removed with the old one, and none of the eight is furniture.
    """
    current, prior = retitled()
    current[0]["title"] = "Note 5 — Business Combinations"

    similarity = diff_periods.similarity(
        diff_periods.title_of(current[0]), diff_periods.title_of(prior[0]))
    assert similarity < diff_periods.TITLE_SIMILARITY_FLOOR

    result = diff_periods.changes(current, prior)
    assert result["count"] == 4 + 4
    assert result["boilerplate"] == []
    assert [entry["kind"] for entry in result["entries"]] == \
        ["added"] * 4 + ["removed"] * 4


# --- fixture three: a table of a hundred identical cells -------------------

def table_of_identical_cells() -> tuple[list[dict], list[dict]]:
    """Both quarters print the same hundred empty cells.

    Two things around the hundred are furniture and not disclosure: the column
    head, whose date moves by a year every year on its own, and the currency
    symbol, which the prior quarter's markup put in a cell of its own and this
    quarter's folds into the amount.
    """
    prior = [section(FAIR_VALUE_TAG, "Note 8 — Fair Value Measurements",
                     ["| (In millions) | Three Months Ended June 30, 2024 |", "$"]
                     + [CELL] * 100)]
    current = [section(FAIR_VALUE_TAG, "Note 8 — Fair Value Measurements",
                       ["| (In millions) | Three Months Ended June 30, 2025 |"]
                       + [CELL] * 100)]
    return current, prior


def test_a_hundred_identical_cells_pair_one_for_one():
    """The multiset, on its own: a hundred cells against a hundred cells.

    The index lookup this replaces kept one index per distinct text, so all one
    hundred matched cell one and ninety-nine were left looking removed.
    """
    matched = diff_periods.match_paragraphs([CELL] * 100, [CELL] * 100)
    assert len(matched["matched"]) == 100
    assert matched["added"] == []
    assert matched["removed"] == []
    # Cell one is used once, by cell one. Every cell has its own counterpart.
    assert [prior for _, prior in matched["matched"]] == list(range(100))


def test_a_table_of_a_hundred_identical_cells_has_no_changes_in_it():
    current, prior = table_of_identical_cells()
    # Why zero: a hundred identical cells on each side, pairing one for one,
    # and the three paragraphs left over hold no word between them.
    assert texts(current).count(CELL) == 100
    assert texts(prior).count(CELL) == 100

    result = diff_periods.changes(current, prior)
    assert result["count"] == 0
    assert result["entries"] == []
    assert [entry["text"] for entry in result["boilerplate"]] == [
        "| (In millions) | Three Months Ended June 30, 2025 |",
        "| (In millions) | Three Months Ended June 30, 2024 |",
        "$"]
    assert all(entry["boilerplate_score"] == 1.0 for entry in result["boilerplate"])


def test_a_sentence_in_place_of_a_cell_is_the_one_change():
    """The positive control. A dash that became a sentence is a disclosure."""
    current, prior = table_of_identical_cells()
    said = ("The Company transferred $412 million of assets out of Level 3 "
            "during the quarter.")
    current[0]["paragraphs"][-1] = said

    result = diff_periods.changes(current, prior)
    assert result["count"] == 1
    assert result["entries"][0]["kind"] == "added"
    assert result["entries"][0]["text"] == said
    # The dash it displaced is left over on the prior side and is furniture, so
    # the sentence is the only change: the two column heads, the currency
    # symbol and that one dash are the four the score took out.
    assert len(result["boilerplate"]) == 4


# --- the two rules the count turns on --------------------------------------

def test_a_paragraph_is_furniture_or_it_makes_a_claim():
    """The score is the share of tokens that are furniture, counted by hand."""
    # `| $ | — | 54,252 |` is seven tokens — |, $, |, —, |, 54,252, | — and not
    # one of them holds a letter. Seven of seven: 1.0.
    assert diff_periods.boilerplate_score("| $ | — | 54,252 |") == 1.0
    # Six tokens: `three`, `months`, `ended` and `june` are stock period words,
    # `30,` and `2025` hold no letter. Six of six: 1.0.
    assert diff_periods.boilerplate_score("Three Months Ended June 30, 2025") == 1.0
    # Seven tokens. `the` is a stock word and `$2.4` holds no letter; `billion.`
    # is `billion` once the full stop is off it. `company`, `acquired`,
    # `alphawave` and `for` are none of those. Three of seven.
    assert diff_periods.boilerplate_score(
        "The Company acquired Alphawave for $2.4 billion.") == 3 / 7
    assert not diff_periods.is_boilerplate(
        "The Company acquired Alphawave for $2.4 billion.")
    # A row label naming an account is not furniture. A line item printed for
    # the first time is a change, and this score must not be what hides it.
    assert diff_periods.boilerplate_score("Total") == 1.0
    assert diff_periods.boilerplate_score("Total goodwill impairment") == 1 / 3


def test_the_title_floor_is_the_floor_already_on_record():
    """`src/note_history.py` pairs notes the same way and records the floor.
    The same rule written in two files is two rules until something reads both.
    """
    assert diff_periods.TITLE_SIMILARITY_FLOOR == note_history.TITLE_SIMILARITY_FLOOR
    assert diff_periods.similarity("note 4 — inventories", "note 5 — inventories") == \
        note_history.similarity("note 4 — inventories", "note 5 — inventories")


def test_a_paragraph_that_moved_to_another_section_is_a_change_in_both():
    """Pairing is what decides where a paragraph is looked for. Boilerplate
    that moved from one note to another is added where it lands and removed
    where it was, exactly as `diff_stream` carries it verbatim in both."""
    moved = "This note should be read with the consolidated financial statements."
    current = [section(INVENTORIES_TAG, "Note 4 — Inventories",
                       INVENTORIES + [moved]),
               section(REVENUE_TAG, "Note 5 — Revenue", REVENUE)]
    prior = [section(INVENTORIES_TAG, "Note 4 — Inventories", INVENTORIES),
             section(REVENUE_TAG, "Note 5 — Revenue", REVENUE + [moved])]

    result = diff_periods.changes(current, prior)
    assert result["count"] == 2
    assert {(entry["kind"], entry["note"]) for entry in result["entries"]} == \
        {("added", INVENTORIES_TAG), ("removed", REVENUE_TAG)}


# --- the layer as the pipeline runs it -------------------------------------

@pytest.mark.parametrize("ticker", ["QCOM"])
def test_the_change_count_is_read_off_a_real_pair_of_filings(ticker):
    """The alignment is wired into the diff, not standing beside it.

    No expected number here: the count belongs to two filings nothing in this
    repository has counted by hand. What is asserted is that it is a count of
    the entries under it, that every entry names a section of one of the two
    periods, and that nothing landed in both the count and the boilerplate.
    """
    payload = diff_periods.extract(ticker)
    result = payload["changes"]
    assert result["count"] == len(result["entries"])
    assert sum(result["match_rules"].values()) == result["sections"]

    sections = {entry["note"] for entry in payload["notes"] + payload["mdna"]}
    prior_sections = {entry["note"] for entry in diff_periods._note_paragraphs(
        ticker, "10-Q", "prior_period_xbrl_instance", cutoff=payload["cutoff"],
        fixtures_root=cutoff_guard.FIXTURES)}
    for entry in result["entries"] + result["boilerplate"]:
        assert entry["note"] in sections | prior_sections
        assert entry["kind"] in ("added", "removed")
    for entry in result["entries"]:
        assert entry["boilerplate_score"] < 1.0
    for entry in result["boilerplate"]:
        assert entry["boilerplate_score"] == 1.0
