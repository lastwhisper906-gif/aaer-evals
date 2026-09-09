"""Pair first, then compare: four filings where nothing was disclosed anew.

`docs/INPUT_SPEC.md` §2 Alignment asks for three things in one order — pair a
section against its prior-period counterpart by tag name, falling back to title
similarity; match one paragraph list against the other as a multiset; score each
paragraph for boilerplate before it counts as a change — and states what they
buy: a reordered or retitled section yields zero changes.

The three the item names are built here, in the test, so a reader can see why
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

A fourth fixture holds the rule *order* to the one the spec states: a heading
reworded to what the heading below it said last quarter must not take the
section that the note below it is tagged as. Every tag pair is made before the
first title pair, or two notes are compared against the wrong note each.

Zero is only worth asserting if something could have moved it, so every fixture
carries a positive control: one sentence added, one tag renamed past the floor,
one cell replaced by a sentence, one deliberate mis-pairing — each of which must
move the count by exactly the amount written out beside it.
"""

from __future__ import annotations

import re

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


# --- fixture four: a heading that reads like the note below it -------------

ACCRUED_TAG = "esterline:AccruedLiabilitiesTextBlock"
RENAMED_ACCRUED_TAG = "esterline:AccruedExpensesTextBlock"
ACCRUED = [
    "Accrued liabilities consist of payroll, warranty and customer rebates.",
    "| Accrued payroll | 312 | 298 |",
]
OTHER_LIABILITIES_TAG = "us-gaap:OtherLiabilitiesDisclosureTextBlock"
OTHER_LIABILITIES = [
    "Other liabilities include the long-term portion of deferred compensation.",
    "| Deferred compensation | 96 | 91 |",
]


def reworded_heading() -> tuple[list[dict], list[dict]]:
    """One heading is reworded to what the heading below it said last quarter.

    The company folded "and other" into the first note's heading and renamed
    the extension tag with it. The second note carries the same `us-gaap` tag
    in both filings and shortened its own heading. Neither note's paragraphs
    changed.
    """
    prior = [section(ACCRUED_TAG, "Note 6 — Accrued Liabilities", ACCRUED),
             section(OTHER_LIABILITIES_TAG,
                     "Note 7 — Accrued and Other Liabilities", OTHER_LIABILITIES)]
    current = [section(RENAMED_ACCRUED_TAG,
                       "Note 6 — Accrued and Other Liabilities", ACCRUED),
               section(OTHER_LIABILITIES_TAG, "Note 7 — Other Liabilities",
                       OTHER_LIABILITIES)]
    return current, prior


def test_every_tag_pair_is_made_before_the_first_title_pair():
    """The rules run one whole rule at a time, in the order the spec states.

    The reworded heading resembles the note *below* it more than the note it
    belongs to. A single pass in section order would hand it the `us-gaap`
    section, and the section actually filed under that tag — its own
    counterpart taken — would fall to the fallback and take what was left. Both
    notes would then be compared against the wrong note.
    """
    current, prior = reworded_heading()
    reworded = diff_periods.title_of(current[0])
    assert diff_periods.similarity(reworded, diff_periods.title_of(prior[1])) > \
        diff_periods.similarity(reworded, diff_periods.title_of(prior[0]))
    # Why zero: both notes' paragraphs are last quarter's, word for word.
    assert texts(current) == texts(prior)

    pairs = diff_periods.pair_sections(current, prior)
    # The tag is the same string in both filings, so it pairs first...
    assert (pairs[1]["matched_by"], pairs[1]["prior"]["name"]) == \
        ("tag_name", OTHER_LIABILITIES_TAG)
    # ...and the reworded heading pairs with what is left, which is its own.
    assert (pairs[0]["matched_by"], pairs[0]["prior"]["name"]) == \
        ("title_similarity", ACCRUED_TAG)

    result = diff_periods.changes(current, prior)
    assert result["count"] == 0
    assert result["boilerplate"] == []


def test_what_the_wrong_pairing_would_have_cost():
    """The positive control for the pass order: the count these two notes carry
    when they are compared against each other. Two paragraphs added, two
    removed, and no furniture among the four."""
    current, prior = reworded_heading()

    mispaired = diff_periods.changes([current[0]], [prior[1]])
    assert mispaired["count"] == 2 + 2
    assert mispaired["boilerplate"] == []
    assert [entry["matched_by"] for entry in mispaired["entries"]] == \
        ["title_similarity"] * 4


def test_the_pairing_does_not_depend_on_the_order_the_sections_are_in():
    """A filing printed in another order is the same filing — of the pairing as
    much as of the paragraphs. The fallback takes its best score first and not
    its earliest section, so reversing both sides forms the same two pairs."""
    current, prior = reworded_heading()

    def made(pairs: list[dict]) -> set[tuple[str, str, str]]:
        return {(pair["current"]["name"], pair["prior"]["name"],
                 pair["matched_by"]) for pair in pairs}

    forward = made(diff_periods.pair_sections(current, prior))
    assert forward == {(RENAMED_ACCRUED_TAG, ACCRUED_TAG, "title_similarity"),
                       (OTHER_LIABILITIES_TAG, OTHER_LIABILITIES_TAG, "tag_name")}
    assert made(diff_periods.pair_sections(current[::-1], prior[::-1])) == forward
    assert diff_periods.changes(current[::-1], prior[::-1])["count"] == 0


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

# What `render` writes above every paragraph: the entry's id, alone in
# brackets. The collapsed placeholder is bracketed too and holds spaces, which
# is what tells the two apart.
ID_LINE = re.compile(r"^\[\S+:(?:notes|mdna):\d+\]$")


def test_the_flat_stream_regroups_into_the_sections_it_came_out_of():
    """`notes` and `extract` carry one flat list whose entries name their note.

    Alignment pairs sections, so it needs them back: in the filing's own order,
    and one section per note however far apart that note's paragraphs sit.
    """
    entries = [{"note": INVENTORIES_TAG, "text": INVENTORIES[0]},
               {"note": REVENUE_TAG, "text": REVENUE[0]},
               {"note": INVENTORIES_TAG, "text": INVENTORIES[1]}]

    assert diff_periods.sections_of(entries) == [
        {"name": INVENTORIES_TAG, "paragraphs": [INVENTORIES[0], INVENTORIES[1]]},
        {"name": REVENUE_TAG, "paragraphs": [REVENUE[0]]}]


def test_the_command_says_how_much_moved(tmp_path, capsys):
    """The summary line is where the change count is read out loud.

    Two of its four numbers are recounted here from the two files the same run
    wrote: an entry is an id line, and a collapsed entry is the one the
    placeholder follows. The change count is not one of them — no one has
    counted these two filings by hand — so what is asserted of it is that the
    line reports the payload's own count and not some other number.
    """
    notes_file, mdna_file = tmp_path / "input_notes.md", tmp_path / "input_mdna.md"
    assert diff_periods.main(["--ticker", "qcom", "--out-notes", str(notes_file),
                              "--out-mdna", str(mdna_file)]) == 0
    line = capsys.readouterr().out.strip()

    written = (notes_file.read_text(encoding="utf-8").splitlines()
               + mdna_file.read_text(encoding="utf-8").splitlines())
    ids = [index for index, text in enumerate(written) if ID_LINE.match(text)]
    collapsed = sum(1 for index in ids
                    if diff_periods.is_collapsed_line(written[index + 1]))
    assert line.startswith(f"diff_periods: QCOM {collapsed} collapsed, "
                           f"{len(ids) - collapsed} carried verbatim, ")

    payload = diff_periods.extract("QCOM")
    assert line.endswith(f"{payload['changes']['count']} changes over "
                         f"{payload['changes']['sections']} paired sections")


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
