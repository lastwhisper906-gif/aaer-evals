"""Three alterations planted on purpose, and the count they leave in the manifest.

The committed input, the report items and the manifest here are all written by
this file, as text. Nothing is read back out of the gate to decide what the gate
should have said: the quotes that stand are slices of prose and of JSON rows
written a few lines above them, and the three items that fall are that same
prose with one character changed, that same prose with its line wrap trimmed to
a space, and a citation naming an id no report carries.

The JSON inputs are planted as characters rather than dumped from a dict,
because that is the whole question a computed row asks. A row quoted "as
printed" is quoted out of the file the reader was handed -- two-space indent,
one key to a line, the writer's own key order -- and a gate that re-renders the
row instead would accept `{"days": 91, "value": 51.7}`, which is in no committed
input, and refuse the same numbers copied off the reader's screen. So the
expected row text below is a slice of the planted file, and the test says so
before it uses it.

The count alone would pass a gate that dropped everything, so every test that
asserts a count asserts which items survived beside it.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src import assemble_bundle, cutoff_guard, quote_gate, trends
from src.cutoff_guard import CutoffGuardError
from src.quote_gate import QuoteGateError

MANIFEST = "input_manifest.json"
ACCESSION = "0000320193-25-000073"

# The em dash and the line wrap are the two features under test. Both are the
# ordinary shape of filing prose, and both are what a model silently tidies.
NOTES = f"""# Notes

[{ACCESSION}:notes:1]
Accounts receivable, net of allowances, rose to $29,508 million — the
largest quarterly increase this company has on record.

[{ACCESSION}:notes:2]
The allowance for credit losses was reduced during the period.
"""

# `input_trends.json` as `src/trends.py` commits it: two-space indent, sorted
# keys, one trailing newline.
TRENDS = """{
  "quarters": [
    {
      "filled": true,
      "label": "quarters-back-0",
      "ratios": {
        "days_sales_outstanding": {
          "days": 91,
          "value": 51.7
        }
      }
    }
  ],
  "ticker": "AAPL"
}
"""

# `input_numbers.json` as `src/assemble_bundle.py` commits it: the same indent,
# and the extractor's field order rather than a sorted one.
NUMBERS = """{
  "ticker": "AAPL",
  "facts": [
    {
      "id": "0000320193-25-000073:receivables_net_current",
      "tag": "AccountsReceivableNetCurrent",
      "prefix": "us-gaap",
      "unit": "usd",
      "value": "29508000000"
    }
  ]
}
"""

# A manifest as `src/assemble_bundle.py` leaves it: counts for the two note
# paragraphs above, and nothing said about drops yet.
MANIFEST_BEFORE = {
    "ticker": "AAPL",
    "accession": ACCESSION,
    "cutoff": "2025-10-31",
    "counts": {"paragraphs": 2, "exclusions": 0},
}

TREND_CELL = f"{ACCESSION}:trends:days_sales_outstanding:quarters-back-0"
FACT_ROW_ID = f"{ACCESSION}:receivables_net_current"

# The two rows above as the two files print them, copied out of the text.
TREND_ROW = ('{\n'
             '          "days": 91,\n'
             '          "value": 51.7\n'
             '        }')
FACT_ROW = ('{\n'
            '      "id": "0000320193-25-000073:receivables_net_current",\n'
            '      "tag": "AccountsReceivableNetCurrent",\n'
            '      "prefix": "us-gaap",\n'
            '      "unit": "usd",\n'
            '      "value": "29508000000"\n'
            '    }')


def plant(tmp_path: Path) -> Path:
    """One run directory: two readers' committed inputs, and the manifest above."""
    root = tmp_path / "AAPL-10-K"
    for agent in ("notes_reader", "numbers_reader"):
        (root / agent).mkdir(parents=True)
    (root / "notes_reader" / "input_notes.md").write_text(NOTES, encoding="utf-8")
    for name, text in (("input_trends.json", TRENDS), ("input_numbers.json", NUMBERS)):
        (root / "numbers_reader" / name).write_text(text, encoding="utf-8")
    (root / MANIFEST).write_text(
        json.dumps(MANIFEST_BEFORE, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return root


def notes_items() -> list[dict]:
    """Four items against the notes above: two verbatim, two altered on purpose."""
    return [
        {"id": "revenue_recognition_receivables_rising",
         "paragraph_id": f"{ACCESSION}:notes:1",
         "quote": "Accounts receivable, net of allowances, rose to $29,508 million"},
        # planted: the em dash of the filing written as a hyphen.
        {"id": "revenue_recognition_receivables_record_increase",
         "paragraph_id": f"{ACCESSION}:notes:1",
         "quote": "rose to $29,508 million - the"},
        # planted: the line wrap of the filing trimmed to a single space.
        {"id": "revenue_recognition_receivables_largest_increase",
         "paragraph_id": f"{ACCESSION}:notes:1",
         "quote": "million — the largest quarterly increase"},
        {"id": "estimates_and_discretion_allowance_reduced",
         "paragraph_id": f"{ACCESSION}:notes:2",
         "quote": "The allowance for credit losses was reduced"},
    ]


def numbers_items() -> list[dict]:
    """Two computed rows, quoted out of the files that print them."""
    return [
        {"id": "revenue_recognition_days_sales_outstanding_high",
         "paragraph_id": TREND_CELL,
         "quote": '"days": 91,\n          "value": 51.7'},
        {"id": "revenue_recognition_receivables_on_the_balance_sheet",
         "paragraph_id": FACT_ROW_ID,
         "quote": '"tag": "AccountsReceivableNetCurrent"'},
    ]


def notes_comparer_items() -> list[dict]:
    return [
        {"id": "revenue_recognition_receivables_rising_versus_market",
         "upstream_item_id": "revenue_recognition_receivables_rising",
         "label": "priced_in"},
        # planted: a citation naming an id no reader report carries.
        {"id": "estimates_and_discretion_allowance_reduced_early_versus_market",
         "upstream_item_id": "estimates_and_discretion_allowance_reduced_early",
         "label": "not_priced"},
    ]


def numbers_comparer_items() -> list[dict]:
    return [{"id": "revenue_recognition_days_sales_outstanding_high_versus_market",
             "upstream_item_id": "revenue_recognition_days_sales_outstanding_high",
             "label": "priced_in"}]


def three_layers(root: Path) -> list[dict]:
    """Two readers and the two comparers over them, each labelling its own report.

    `docs/INPUT_SPEC.md`: a comparer holds both reader reports and "labels only
    the items of its own report — numbers versus market labels
    `report_numbers.md`, notes versus market labels `report_notes_text.md`.
    Labelling an item from the other report is a broken run." So neither
    comparer here cites across, and a specimen where one did would be a
    specimen of a broken run.
    """
    return [
        {"report": "report_notes_text.md", "items": notes_items(),
         "input": root / "notes_reader"},
        {"report": "report_numbers.md", "items": numbers_items(),
         "input": root / "numbers_reader"},
        {"report": "report_notes_vs_market.md", "items": notes_comparer_items(),
         "cites": ["report_notes_text.md"]},
        {"report": "report_numbers_vs_market.md", "items": numbers_comparer_items(),
         "cites": ["report_numbers.md"]},
    ]


def kept_ids(result: dict) -> list[str]:
    return sorted(item["id"] for items in result["kept"].values() for item in items)


def reason_for(result: dict, identifier: str) -> str:
    return next(row["reason"] for row in result["dropped"] if row["item_id"] == identifier)


def manifest_of(root: Path) -> dict:
    return json.loads((root / MANIFEST).read_text(encoding="utf-8"))


def gate_one(root: Path, item: dict, agent: str = "notes_reader") -> dict:
    """One reader item on its own, against one committed input."""
    return quote_gate.gate(
        [{"report": "report_notes_text.md", "items": [item], "input": root / agent}], root)


# --- the three planted items -------------------------------------------------

def test_each_planted_item_is_dropped_and_the_rest_survive(tmp_path):
    root = plant(tmp_path)
    result = quote_gate.gate(three_layers(root), root)
    assert [row["item_id"] for row in result["dropped"]] == [
        "revenue_recognition_receivables_record_increase",
        "revenue_recognition_receivables_largest_increase",
        "estimates_and_discretion_allowance_reduced_early_versus_market"]
    assert kept_ids(result) == [
        "estimates_and_discretion_allowance_reduced",
        "revenue_recognition_days_sales_outstanding_high",
        "revenue_recognition_days_sales_outstanding_high_versus_market",
        "revenue_recognition_receivables_on_the_balance_sheet",
        "revenue_recognition_receivables_rising",
        "revenue_recognition_receivables_rising_versus_market"]


def test_the_drop_count_reaches_the_manifest(tmp_path):
    root = plant(tmp_path)
    quote_gate.gate(three_layers(root), root)
    manifest = manifest_of(root)
    assert manifest["counts"]["dropped_items"] == 3
    assert len(manifest["dropped_items"]) == 3
    assert [row["item_id"] for row in manifest["dropped_items"]] == [
        "revenue_recognition_receivables_record_increase",
        "revenue_recognition_receivables_largest_increase",
        "estimates_and_discretion_allowance_reduced_early_versus_market"]


def test_the_manifest_keeps_everything_it_already_said(tmp_path):
    root = plant(tmp_path)
    quote_gate.gate(three_layers(root), root)
    manifest = manifest_of(root)
    assert manifest["ticker"] == "AAPL"
    assert manifest["accession"] == ACCESSION
    assert manifest["cutoff"] == "2025-10-31"
    assert manifest["counts"]["paragraphs"] == 2
    assert manifest["counts"]["exclusions"] == 0


def test_each_planted_item_is_dropped_for_its_own_reason(tmp_path):
    root = plant(tmp_path)
    result = quote_gate.gate(three_layers(root), root)
    assert "does not string-match" in reason_for(
        result, "revenue_recognition_receivables_record_increase")
    assert "does not string-match" in reason_for(
        result, "revenue_recognition_receivables_largest_increase")
    assert "does not resolve" in reason_for(
        result, "estimates_and_discretion_allowance_reduced_early_versus_market")


def test_gating_twice_writes_the_same_count(tmp_path):
    root = plant(tmp_path)
    quote_gate.gate(three_layers(root), root)
    quote_gate.gate(three_layers(root), root)
    assert manifest_of(root)["counts"]["dropped_items"] == 3


# --- string-match means string-match -----------------------------------------

def test_the_whole_paragraph_is_quotable(tmp_path):
    root = plant(tmp_path)
    item = {"id": "revenue_recognition_receivables_rising",
            "paragraph_id": f"{ACCESSION}:notes:1",
            "quote": "Accounts receivable, net of allowances, rose to $29,508 million — the\n"
                     "largest quarterly increase this company has on record."}
    assert kept_ids(gate_one(root, item)) == ["revenue_recognition_receivables_rising"]


def test_an_ellipsis_standing_in_for_words_does_not_match(tmp_path):
    root = plant(tmp_path)
    item = {"id": "revenue_recognition_receivables_rising",
            "paragraph_id": f"{ACCESSION}:notes:1",
            "quote": "Accounts receivable … rose to $29,508 million"}
    assert kept_ids(gate_one(root, item)) == []


def test_a_changed_case_does_not_match(tmp_path):
    root = plant(tmp_path)
    item = {"id": "revenue_recognition_receivables_rising",
            "paragraph_id": f"{ACCESSION}:notes:1",
            "quote": "accounts receivable, net of allowances"}
    assert kept_ids(gate_one(root, item)) == []


def test_an_empty_quote_is_dropped_rather_than_matching_everything(tmp_path):
    root = plant(tmp_path)
    item = {"id": "revenue_recognition_receivables_rising",
            "paragraph_id": f"{ACCESSION}:notes:1", "quote": ""}
    result = gate_one(root, item)
    assert kept_ids(result) == []
    assert "empty quote" in reason_for(result, "revenue_recognition_receivables_rising")


def test_a_quote_belonging_to_another_paragraph_is_dropped(tmp_path):
    root = plant(tmp_path)
    item = {"id": "estimates_and_discretion_allowance_reduced",
            "paragraph_id": f"{ACCESSION}:notes:2",
            "quote": "Accounts receivable, net of allowances"}
    assert kept_ids(gate_one(root, item)) == []


def test_a_paragraph_id_that_names_nothing_is_dropped(tmp_path):
    root = plant(tmp_path)
    item = {"id": "revenue_recognition_receivables_rising",
            "paragraph_id": f"{ACCESSION}:notes:9",
            "quote": "Accounts receivable, net of allowances"}
    result = gate_one(root, item)
    assert kept_ids(result) == []
    assert "not in this reader's committed input" in reason_for(
        result, "revenue_recognition_receivables_rising")


def test_an_item_with_no_id_is_dropped(tmp_path):
    root = plant(tmp_path)
    item = {"paragraph_id": f"{ACCESSION}:notes:2",
            "quote": "The allowance for credit losses was reduced"}
    result = gate_one(root, item)
    assert kept_ids(result) == []
    assert result["dropped"] == [{"report": "report_notes_text.md", "item_id": None,
                                  "reason": "the item carries no id, so nothing "
                                            "downstream could cite it"}]


# --- computed rows are quoted out of the committed file ----------------------

def test_the_planted_inputs_wear_the_layout_the_pipeline_commits():
    """The fixtures above are the two writers' own output, not a convenience.

    The claim a computed row makes is about characters, so a fixture written in
    some other layout would be testing a file no reader is ever handed.
    """
    assert TRENDS == trends.render(json.loads(TRENDS))
    assert NUMBERS == json.dumps(json.loads(NUMBERS), indent=2, sort_keys=False) + "\n"


def test_a_trend_cell_is_quotable_as_the_row_the_file_prints(tmp_path):
    root = plant(tmp_path)
    assert TREND_ROW in TRENDS
    assert quote_gate.quotable(root / "numbers_reader", ACCESSION)[TREND_CELL] == TREND_ROW


def test_a_numeric_fact_is_quotable_by_the_id_it_already_carries(tmp_path):
    root = plant(tmp_path)
    assert FACT_ROW in NUMBERS
    assert quote_gate.quotable(root / "numbers_reader", ACCESSION)[FACT_ROW_ID] == FACT_ROW


def test_a_row_re_rendered_onto_one_line_does_not_match(tmp_path):
    """The alteration a normalizing gate cannot see, and the one it invents.

    `{"days": 91, "value": 51.7}` is the row with its indent and its line breaks
    taken out. It is in no committed input, so it is not a quote of anything.
    """
    root = plant(tmp_path)
    one_line = '{"days": 91, "value": 51.7}'
    assert one_line not in TRENDS
    item = {"id": "revenue_recognition_days_sales_outstanding_high",
            "paragraph_id": TREND_CELL, "quote": one_line}
    result = gate_one(root, item, "numbers_reader")
    assert kept_ids(result) == []
    assert "does not string-match" in reason_for(
        result, "revenue_recognition_days_sales_outstanding_high")


def test_a_row_with_its_keys_reordered_does_not_match(tmp_path):
    root = plant(tmp_path)
    reordered = '"tag": "AccountsReceivableNetCurrent", "unit": "usd"'
    assert reordered not in NUMBERS
    item = {"id": "revenue_recognition_receivables_on_the_balance_sheet",
            "paragraph_id": FACT_ROW_ID, "quote": reordered}
    assert kept_ids(gate_one(root, item, "numbers_reader")) == []


def test_a_computed_row_that_is_not_in_the_input_names_nothing(tmp_path):
    root = plant(tmp_path)
    index = quote_gate.quotable(root / "numbers_reader", ACCESSION)
    for absent in (f"{ACCESSION}:trends:days_sales_outstanding:quarters-back-1",
                   f"{ACCESSION}:trends:gross_margin:quarters-back-0",
                   f"{ACCESSION}:articulation:receivables:quarters-back-0",
                   f"{ACCESSION}:receivables_net_prior"):
        assert absent not in index


def test_a_file_that_is_not_this_readers_input_offers_nothing_to_quote(tmp_path):
    """The market table and the manifest are not evidence, whatever sits beside them.

    `input_market.json` never reaches a reader and `input_manifest.json` carries
    the text of paragraphs the pipeline took *out* of the reader's input. A gate
    that let a paragraph id reach into an arbitrary file would certify a quote
    of either.
    """
    root = plant(tmp_path)
    reader = root / "numbers_reader"
    market = '{\n  "rows": [\n    {\n      "abnormal_return": 0.031\n    }\n  ]\n}\n'
    (reader / "input_market.json").write_text(market, encoding="utf-8")
    (reader / MANIFEST).write_text(
        (root / MANIFEST).read_text(encoding="utf-8"), encoding="utf-8")
    assert sorted(quote_gate.quotable(reader, ACCESSION)) == [FACT_ROW_ID, TREND_CELL]
    item = {"id": "results_against_expectations_market_moved",
            "paragraph_id": "input_market.json#/rows/0",
            "quote": '"abnormal_return": 0.031'}
    assert kept_ids(gate_one(root, item, "numbers_reader")) == []


# --- citations ---------------------------------------------------------------

def test_an_item_that_cites_nothing_is_dropped(tmp_path):
    root = plant(tmp_path)
    result = quote_gate.gate([
        {"report": "report_notes_text.md", "items": notes_items(),
         "input": root / "notes_reader"},
        {"report": "report_notes_vs_market.md", "cites": ["report_notes_text.md"],
         "items": [{"id": "revenue_recognition_receivables_rising_versus_market",
                    "label": "priced_in"}]},
    ], root)
    assert kept_ids(result) == ["estimates_and_discretion_allowance_reduced",
                                "revenue_recognition_receivables_rising"]
    assert "cites no upstream item" in reason_for(
        result, "revenue_recognition_receivables_rising_versus_market")


def test_an_item_the_reader_layer_dropped_cannot_be_cited(tmp_path):
    root = plant(tmp_path)
    result = quote_gate.gate([
        {"report": "report_notes_text.md", "items": notes_items(),
         "input": root / "notes_reader"},
        {"report": "report_notes_vs_market.md", "cites": ["report_notes_text.md"],
         "items": [{"id": "revenue_recognition_receivables_record_increase_versus_market",
                    "upstream_item_id": "revenue_recognition_receivables_record_increase"}]},
    ], root)
    assert "revenue_recognition_receivables_record_increase_versus_market" not in kept_ids(result)
    assert manifest_of(root)["counts"]["dropped_items"] == 3


def test_a_supervisor_item_needs_every_one_of_its_evidence_ids_to_resolve(tmp_path):
    root = plant(tmp_path)
    result = quote_gate.gate([
        {"report": "report_notes_text.md", "items": notes_items(),
         "input": root / "notes_reader"},
        {"report": "prediction_accounting.json", "cites": ["report_notes_text.md"],
         "items": [
             {"id": "receivables_outrun_revenue",
              "evidence": [{"upstream_item_id": "revenue_recognition_receivables_rising"},
                           {"upstream_item_id": "estimates_and_discretion_allowance_reduced"}]},
             {"id": "estimate_change_favorable",
              "evidence": [{"upstream_item_id": "revenue_recognition_receivables_rising"},
                           {"upstream_item_id": "estimates_and_discretion_estimate_relaxed"}]},
         ]},
    ], root)
    assert "receivables_outrun_revenue" in kept_ids(result)
    assert "estimate_change_favorable" not in kept_ids(result)


def test_a_market_direction_basis_resolves_the_same_way(tmp_path):
    root = plant(tmp_path)
    result = quote_gate.gate([
        {"report": "report_notes_text.md", "items": notes_items(),
         "input": root / "notes_reader"},
        {"report": "prediction_pressure.json", "cites": ["report_notes_text.md"],
         "items": [{"id": "market_direction",
                    "basis": ["revenue_recognition_receivables_rising",
                              "estimates_and_discretion_allowance_reduced_early"]}]},
    ], root)
    assert kept_ids(result) == ["estimates_and_discretion_allowance_reduced",
                                "revenue_recognition_receivables_rising"]


# --- one id names one item ---------------------------------------------------

def test_two_items_in_one_report_sharing_an_id_are_both_dropped(tmp_path):
    """Otherwise a failed item stays citable under its twin's name.

    One of these two quotes matches and one is the planted hyphen. Keeping the
    good one would leave the shared id resolving downstream, which is the
    dropped item's id passed through by another name.
    """
    root = plant(tmp_path)
    result = quote_gate.gate([
        {"report": "report_notes_text.md", "input": root / "notes_reader", "items": [
            {"id": "revenue_recognition_receivables_rising",
             "paragraph_id": f"{ACCESSION}:notes:1",
             "quote": "Accounts receivable, net of allowances"},
            {"id": "revenue_recognition_receivables_rising",
             "paragraph_id": f"{ACCESSION}:notes:1",
             "quote": "rose to $29,508 million - the"},
        ]},
        {"report": "report_notes_vs_market.md", "cites": ["report_notes_text.md"],
         "items": [{"id": "revenue_recognition_receivables_rising_versus_market",
                    "upstream_item_id": "revenue_recognition_receivables_rising"}]},
    ], root)
    assert kept_ids(result) == []
    assert "more than one item in this run" in reason_for(
        result, "revenue_recognition_receivables_rising")
    assert manifest_of(root)["counts"]["dropped_items"] == 3


def test_two_reports_sharing_an_item_id_lose_it_in_both(tmp_path):
    root = plant(tmp_path)
    result = quote_gate.gate([
        {"report": "report_notes_text.md", "input": root / "notes_reader",
         "items": [{"id": "revenue_recognition_receivables_rising",
                    "paragraph_id": f"{ACCESSION}:notes:1",
                    "quote": "Accounts receivable, net of allowances"}]},
        {"report": "report_numbers.md", "input": root / "numbers_reader",
         "items": [{"id": "revenue_recognition_receivables_rising",
                    "paragraph_id": FACT_ROW_ID,
                    "quote": '"tag": "AccountsReceivableNetCurrent"'}]},
        {"report": "report_notes_vs_market.md", "cites": ["report_notes_text.md"],
         "items": [{"id": "revenue_recognition_receivables_rising_versus_market",
                    "upstream_item_id": "revenue_recognition_receivables_rising"}]},
    ], root)
    assert kept_ids(result) == []
    assert manifest_of(root)["counts"]["dropped_items"] == 3


# --- a reader or comparer item's id says what the item looks at --------------
#
# The owner's decision, 2026-09-23, verbatim: "t1~t40 대신 쓸 쉬운 이름
# revenue_recognition 같이 항목을 무엇을 보는지가 이름에 그대로 드러나게" -- in
# English, item names say what they look at. The rule as the owner stated it: a
# reader or comparer item id is lowercase snake_case, letters and underscores
# only, no digits; it starts with its area and then says what it looks at; the
# location stays in `paragraph_id`, and a period or a date never goes in the id.
# Every id below is planted from that text, and none is read back out of the
# gate. Every item below quotes its paragraph verbatim, so the id is the only
# thing that can drop it.

REPO_ROOT = Path(__file__).resolve().parent.parent
AREAS_FILE = REPO_ROOT / "rules" / "pilot" / "areas.json"
CHECKLIST = REPO_ROOT / "docs" / "CHECKLIST.md"
PROMPTS = REPO_ROOT / ".claude" / "agents"

# The `###` headings under `docs/CHECKLIST.md` §1 and §2, read off the file by
# hand, each beside the slug it becomes: lowercase, commas dropped, a space
# written as an underscore.
AREAS_BY_HAND = {
    "estimates_and_discretion": "Estimates and discretion",
    "revenue_recognition": "Revenue recognition",
    "earnings_quality": "Earnings quality",
    "articulation_and_the_filed_history": "Articulation and the filed history",
    "controls_audit_and_filings": "Controls, audit and filings",
    "related_parties_contingencies_and_subsequent_events":
        "Related parties, contingencies and subsequent events",
    "structure_and_disclosure_changes": "Structure and disclosure changes",
    "across_documents": "Across documents",
    "results_against_expectations": "Results against expectations",
    "liquidity_and_capital": "Liquidity and capital",
    "narrative_signs_of_operating_pressure": "Narrative signs of operating pressure",
}

# The owner's first example, and a comparer item named after it by the
# convention the two comparer prompts give.
EXAMPLE = "revenue_recognition_extended_payment_terms"
EXAMPLE_VERSUS_MARKET = "revenue_recognition_extended_payment_terms_versus_market"
QUOTED = "Accounts receivable, net of allowances"

NOT_A_NAME = "is not a plain name"
NO_AREA = "does not start with an area"


def reader_item(identifier) -> dict:
    """A notes-reader item whose quote matches, so only its id is on trial."""
    return {"id": identifier, "paragraph_id": f"{ACCESSION}:notes:1", "quote": QUOTED}


def test_the_area_list_is_the_eleven_checklist_headings():
    assert len(AREAS_BY_HAND) == 11
    assert json.loads(AREAS_FILE.read_text(encoding="utf-8")) == AREAS_BY_HAND


def test_the_area_list_still_matches_the_checklist_it_was_read_from():
    """The file and the document are one list written twice, so this reads both."""
    text = CHECKLIST.read_text(encoding="utf-8")
    section = text[text.index("\n## 1. "):text.index("\n## 3. ")]
    headings = [line[len("### "):] for line in section.splitlines()
                if line.startswith("### ")]
    assert headings == list(json.loads(AREAS_FILE.read_text(encoding="utf-8")).values())


def test_the_owners_example_name_stands(tmp_path):
    root = plant(tmp_path)
    result = gate_one(root, reader_item(EXAMPLE))
    assert kept_ids(result) == [EXAMPLE]
    assert result["dropped"] == []


@pytest.mark.parametrize("identifier, why", [
    ("T01", NOT_A_NAME),                                     # the numbering it replaces
    # the first numbers item of the second pipeline check (PR #73), as committed
    ("0001045810-26-000075:trends:days_sales_outstanding:2026-04-27..2026-07-26",
     NOT_A_NAME),
    ("revenue_recognition_q3_2026", NOT_A_NAME),             # a period in the id
    ("Revenue_Recognition_x", NOT_A_NAME),                   # capitals
    ("revenue-recognition-extended-payment-terms", NOT_A_NAME),
    ("revenue_recognition__extended_payment_terms", NOT_A_NAME),
    ("revenue_recognition_extended_payment_terms_", NOT_A_NAME),
    (" revenue_recognition_extended_payment_terms", NOT_A_NAME),
    ("revenue_recognition_extended_payment_terms\n", NOT_A_NAME),
    ("revenue_recognition_échéance", NOT_A_NAME),            # a slug is ASCII
    ("payment_terms_extended", NO_AREA),                     # no area
    ("revenue_recognition", NO_AREA),                        # an area, and nothing after it
    ("revenue_recognitions_extended_payment_terms", NO_AREA),
])
def test_an_id_that_is_not_a_descriptive_name_is_dropped_and_recorded(tmp_path, identifier, why):
    root = plant(tmp_path)
    result = gate_one(root, reader_item(identifier))
    assert kept_ids(result) == []
    reason = reason_for(result, identifier)
    assert why in reason
    manifest = manifest_of(root)
    assert manifest["counts"]["dropped_items"] == 1
    assert manifest["dropped_items"] == [
        {"report": "report_notes_text.md", "item_id": identifier, "reason": reason}]


@pytest.mark.parametrize("identifier", ["receivables_days_sales_outstanding_rising",
                                        "inventory_purchase_obligations_in_excess"])
def test_the_owners_two_account_led_examples_are_refused_under_the_heading_list(
        tmp_path, identifier):
    """Stated rather than hidden. Two of the owner's three examples lead with an
    account, and `receivables` and `inventory` are not `###` headings of §1 or
    §2. The heading list is the rule in force; adding account-level areas is the
    open row in `docs/needs_judgment.md`, and from the rules version that adds
    them this test changes with it."""
    root = plant(tmp_path)
    result = gate_one(root, reader_item(identifier))
    assert kept_ids(result) == []
    assert NO_AREA in reason_for(result, identifier)


def test_each_of_the_four_reports_is_held_to_the_rule(tmp_path):
    root = plant(tmp_path)
    layers = three_layers(root)
    planted = {
        "report_notes_text.md": {"id": "T01", "paragraph_id": f"{ACCESSION}:notes:2",
                                 "quote": "The allowance for credit losses"},
        "report_numbers.md": {"id": "T02", "paragraph_id": FACT_ROW_ID,
                              "quote": '"unit": "usd"'},
        "report_notes_vs_market.md": {
            "id": "T03", "label": "not_priced",
            "upstream_item_id": "estimates_and_discretion_allowance_reduced"},
        "report_numbers_vs_market.md": {
            "id": "T04", "label": "not_priced",
            "upstream_item_id": "revenue_recognition_days_sales_outstanding_high"},
    }
    for entry in layers:
        entry["items"].append(planted[entry["report"]])
    result = quote_gate.gate(layers, root)
    assert [row["item_id"] for row in result["dropped"]
            if NOT_A_NAME in row["reason"]] == ["T01", "T02", "T03", "T04"]
    assert kept_ids(result) == [
        "estimates_and_discretion_allowance_reduced",
        "revenue_recognition_days_sales_outstanding_high",
        "revenue_recognition_days_sales_outstanding_high_versus_market",
        "revenue_recognition_receivables_on_the_balance_sheet",
        "revenue_recognition_receivables_rising",
        "revenue_recognition_receivables_rising_versus_market"]
    assert manifest_of(root)["counts"]["dropped_items"] == 7


def test_a_comparer_item_named_after_the_reader_item_it_labels_stands(tmp_path):
    root = plant(tmp_path)
    result = quote_gate.gate([
        {"report": "report_notes_text.md", "input": root / "notes_reader",
         "items": [reader_item(EXAMPLE)]},
        {"report": "report_notes_vs_market.md", "cites": ["report_notes_text.md"],
         "items": [{"id": EXAMPLE_VERSUS_MARKET, "upstream_item_id": EXAMPLE,
                    "label": "not_priced"}]},
    ], root)
    assert kept_ids(result) == [EXAMPLE, EXAMPLE_VERSUS_MARKET]
    assert result["dropped"] == []


@pytest.mark.parametrize("identifier, why", [
    ("T05", NOT_A_NAME),
    ("revenue_recognition_extended_payment_terms_q3", NOT_A_NAME),
    ("priced_in_extended_payment_terms", NO_AREA),
])
def test_a_comparer_id_is_held_to_the_same_shape(tmp_path, identifier, why):
    root = plant(tmp_path)
    result = quote_gate.gate([
        {"report": "report_notes_text.md", "input": root / "notes_reader",
         "items": [reader_item(EXAMPLE)]},
        {"report": "report_notes_vs_market.md", "cites": ["report_notes_text.md"],
         "items": [{"id": identifier, "upstream_item_id": EXAMPLE, "label": "not_priced"}]},
    ], root)
    assert kept_ids(result) == [EXAMPLE]
    assert why in reason_for(result, identifier)
    assert manifest_of(root)["dropped_items"][0]["report"] == "report_notes_vs_market.md"


def test_a_comparer_item_wearing_the_reader_id_it_cites_is_refused(tmp_path):
    """A comparer item's id is its own name. Wearing the reader's makes one id
    name two items, and both go, each with the reason written down."""
    root = plant(tmp_path)
    result = quote_gate.gate([
        {"report": "report_notes_text.md", "input": root / "notes_reader",
         "items": [reader_item(EXAMPLE)]},
        {"report": "report_notes_vs_market.md", "cites": ["report_notes_text.md"],
         "items": [{"id": EXAMPLE, "upstream_item_id": EXAMPLE, "label": "not_priced"}]},
    ], root)
    assert kept_ids(result) == []
    rows = manifest_of(root)["dropped_items"]
    assert [(row["report"], row["item_id"]) for row in rows] == [
        ("report_notes_text.md", EXAMPLE), ("report_notes_vs_market.md", EXAMPLE)]
    assert all("more than one item in this run" in row["reason"] for row in rows)


def test_one_name_in_two_reader_reports_is_refused_in_each_with_its_reason(tmp_path):
    root = plant(tmp_path)
    result = quote_gate.gate([
        {"report": "report_notes_text.md", "input": root / "notes_reader",
         "items": [reader_item(EXAMPLE)]},
        {"report": "report_numbers.md", "input": root / "numbers_reader",
         "items": [{"id": EXAMPLE, "paragraph_id": FACT_ROW_ID,
                    "quote": '"tag": "AccountsReceivableNetCurrent"'}]},
    ], root)
    assert kept_ids(result) == []
    rows = manifest_of(root)["dropped_items"]
    assert [(row["report"], row["item_id"]) for row in rows] == [
        ("report_notes_text.md", EXAMPLE), ("report_numbers.md", EXAMPLE)]
    assert all("more than one item in this run" in row["reason"] for row in rows)
    assert manifest_of(root)["counts"]["dropped_items"] == 2


def test_a_supervisors_checklist_keys_are_not_held_to_the_item_id_shape(tmp_path):
    """The rule is the readers' and the comparers'. A supervisor's entries are
    named by the checklist keys, which stay as they are."""
    root = plant(tmp_path)
    result = quote_gate.gate([
        {"report": "report_notes_text.md", "input": root / "notes_reader",
         "items": [reader_item(EXAMPLE)]},
        {"report": "prediction_accounting.json", "cites": ["report_notes_text.md"],
         "items": [{"id": "receivables_outrun_revenue",
                    "evidence": [{"upstream_item_id": EXAMPLE}]},
                   {"id": "market_direction", "basis": [EXAMPLE]}]},
    ], root)
    assert kept_ids(result) == ["market_direction", "receivables_outrun_revenue", EXAMPLE]


def test_a_report_handed_under_a_path_is_held_to_the_rule_by_its_file_name(tmp_path):
    root = plant(tmp_path)
    result = quote_gate.gate([
        {"report": "agents/notes-text-reader/report_notes_text.md",
         "input": root / "notes_reader", "items": [reader_item("T01"), reader_item(EXAMPLE)]},
    ], root)
    assert kept_ids(result) == [EXAMPLE]
    assert NOT_A_NAME in reason_for(result, "T01")


@pytest.mark.parametrize("report, side", [
    ("report_notes.md", "input"),                     # a name the layer table does not give
    ("report_numbers_vs_market.md", "input"),         # a comparer's report quoting an input
    ("report_notes_text.md", "cites"),                # a reader's report citing
    ("prediction_accounting.json", "input"),          # a supervisor's output quoting an input
    ("control_single_agent_accounting.json", "cites"),
])
def test_a_report_the_layer_table_does_not_place_that_way_is_refused(tmp_path, report, side):
    """The rule reaches a report by its name, so a name has to mean one layer."""
    root = plant(tmp_path)
    entry = {"report": report, "items": [reader_item("T01")]}
    entry.update({"input": root / "notes_reader"} if side == "input" else {"cites": []})
    with pytest.raises(QuoteGateError):
        quote_gate.gate([entry], root)


@pytest.mark.parametrize("text", [
    None,                                                  # not there
    "the eleven headings",                                 # not JSON
    '["revenue_recognition"]',                             # not an object
    "{}",                                                  # no area at all
    '{"revenue_recognition_2": "Revenue recognition"}',   # a slug that is not a name
    '{"revenue_recognition": ""}',                         # no heading beside it
    '{"revenue_recognition": 5}',
    '{"revenue_recognition": "A", "revenue_recognition": "B"}',
])
def test_an_area_list_that_cannot_be_read_stops_the_gate(tmp_path, monkeypatch, text):
    root = plant(tmp_path)
    areas = tmp_path / "areas.json"
    if text is not None:
        areas.write_text(text, encoding="utf-8")
    monkeypatch.setattr(quote_gate, "AREAS", areas)
    with pytest.raises(QuoteGateError):
        quote_gate.gate(three_layers(root), root)


@pytest.mark.parametrize("reader", ["numbers-reader", "notes-text-reader"])
def test_each_reader_prompt_names_every_area_as_the_gate_reads_it(reader):
    """The readers run in sessions that cannot reach `rules/`, so the list is in
    the prompt as well, and this is what keeps the two copies one list."""
    prompt = (PROMPTS / f"{reader}.md").read_text(encoding="utf-8")
    for area in json.loads(AREAS_FILE.read_text(encoding="utf-8")):
        assert f"`{area}`" in prompt
    assert f"`{EXAMPLE}`" in prompt


@pytest.mark.parametrize("comparer", ["numbers-vs-market", "notes-vs-market"])
def test_each_comparer_prompt_gives_the_versus_market_convention(comparer):
    prompt = (PROMPTS / f"{comparer}.md").read_text(encoding="utf-8")
    assert "`_versus_market`" in prompt
    assert f"`{EXAMPLE_VERSUS_MARKET}`" in prompt


# --- against a real committed input ------------------------------------------

@pytest.fixture(scope="module")
def real_bundle(tmp_path_factory):
    """One real AAPL 10-Q bundle, assembled once for the tests that want one."""
    out = tmp_path_factory.mktemp("bundle")
    built = assemble_bundle.build("AAPL", "10-Q")
    assemble_bundle.write(built, out)
    return out, built["manifest"]["accession"]


def test_the_index_covers_a_real_assembled_bundle(real_bundle):
    """Planted prose is prose written to be matched. A filing is not.

    The claim here is not a value, which is why no number is asserted: it is
    that the index reaches a real bundle's note paragraphs at all, that a slice
    taken verbatim out of the longest of them stands, and that the same slice
    with one space added does not.
    """
    bundle, accession = real_bundle
    index = quote_gate.quotable(bundle, accession)
    identifier, text = max(((one, body) for one, body in index.items()
                            if ":notes:" in one), key=lambda pair: len(pair[1]))
    verbatim = text[:120]
    spaced = verbatim[:60] + " " + verbatim[60:]
    assert quote_gate.quote_drop_reason(
        {"id": "probe", "paragraph_id": identifier, "quote": verbatim}, index) is None
    assert quote_gate.quote_drop_reason(
        {"id": "probe", "paragraph_id": identifier, "quote": spaced}, index) is not None


def test_a_real_bundles_computed_rows_are_slices_of_the_files_that_hold_them(real_bundle):
    """Every row the index offers is characters a reader could copy off its screen."""
    bundle, accession = real_bundle
    index = quote_gate.quotable(bundle, accession)

    committed = cutoff_guard.load_bundle_file(bundle, "input_trends.json")
    cells = [one for one in index if one.startswith(f"{accession}:trends:")]
    assert cells
    for one in cells:
        assert index[one] in committed

    committed = cutoff_guard.load_bundle_file(bundle, "input_numbers.json")
    facts = [fact["id"] for fact in json.loads(committed)["facts"]]
    assert facts
    for one in facts:
        assert index[one] in committed


def test_a_real_bundles_fact_row_is_quoted_out_of_the_file(real_bundle):
    """The row a reader can copy stands; the row a gate would re-render does not."""
    bundle, accession = real_bundle
    index = quote_gate.quotable(bundle, accession)
    committed = cutoff_guard.load_bundle_file(bundle, "input_numbers.json")
    identifier = json.loads(committed)["facts"][0]["id"]

    verbatim = index[identifier][:120]
    assert verbatim in committed
    assert quote_gate.quote_drop_reason(
        {"id": "probe", "paragraph_id": identifier, "quote": verbatim}, index) is None

    one_line = json.dumps(json.loads(index[identifier]), sort_keys=True)
    assert one_line not in committed
    assert quote_gate.quote_drop_reason(
        {"id": "probe", "paragraph_id": identifier, "quote": one_line}, index) is not None


# --- the gate fails closed ---------------------------------------------------

def test_a_committed_input_that_is_not_on_disk_is_refused(tmp_path):
    root = plant(tmp_path)
    with pytest.raises(QuoteGateError):
        quote_gate.gate([{"report": "report_notes_text.md", "items": notes_items(),
                          "input": root / "nowhere"}], root)


def test_one_paragraph_id_naming_two_paragraphs_is_refused(tmp_path):
    root = plant(tmp_path)
    (root / "notes_reader" / "input_mdna.md").write_text(
        f"# Management's discussion\n\n[{ACCESSION}:notes:1]\nSomething else entirely.\n",
        encoding="utf-8")
    with pytest.raises(QuoteGateError):
        quote_gate.quotable(root / "notes_reader", ACCESSION)


def test_a_report_that_names_neither_an_input_nor_what_it_cites_is_refused(tmp_path):
    root = plant(tmp_path)
    with pytest.raises(QuoteGateError):
        quote_gate.gate([{"report": "report_notes_text.md", "items": notes_items()}], root)


def test_a_report_citing_one_that_has_not_been_gated_yet_is_refused(tmp_path):
    root = plant(tmp_path)
    with pytest.raises(QuoteGateError):
        quote_gate.gate([{"report": "report_notes_vs_market.md",
                          "items": notes_comparer_items(),
                          "cites": ["report_notes_text.md"]}], root)


def test_a_manifest_that_is_not_there_is_refused(tmp_path):
    root = plant(tmp_path)
    (root / MANIFEST).unlink()
    with pytest.raises(CutoffGuardError):
        quote_gate.gate(three_layers(root), root)


def test_a_manifest_naming_no_accession_is_refused(tmp_path):
    root = plant(tmp_path)
    (root / MANIFEST).write_text(json.dumps({"ticker": "AAPL"}) + "\n", encoding="utf-8")
    with pytest.raises(QuoteGateError):
        quote_gate.gate(three_layers(root), root)
