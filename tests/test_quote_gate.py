"""Three alterations planted on purpose, and the count they leave in the manifest.

The committed input, the report items and the manifest here are all written by
this file. Nothing is read back out of the gate to decide what the gate should
have said: the quotes that stand are substrings of prose and of computed rows
written a few lines above them, and the three items that fall are that same
prose with one character changed, that same prose with one line wrap joined,
and a citation naming an id no report carries.

The count alone would pass a gate that dropped everything, so every test that
asserts a count asserts which items survived beside it.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src import assemble_bundle, quote_gate
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

TRENDS_INPUT = {
    "ticker": "AAPL",
    "quarters": [
        {"label": "Q-0", "filled": True,
         "ratios": {"days_sales_outstanding": {"days": 91, "value": 51.7}}},
    ],
}

NUMBERS_INPUT = {
    "ticker": "AAPL",
    "facts": [
        {"id": f"{ACCESSION}:receivables_net_current",
         "tag": "AccountsReceivableNetCurrent", "unit": "usd", "value": 29508000000},
    ],
}

# A manifest as `src/assemble_bundle.py` leaves it: counts for the two note
# paragraphs above, and nothing said about drops yet.
MANIFEST_BEFORE = {
    "ticker": "AAPL",
    "accession": ACCESSION,
    "cutoff": "2025-10-31",
    "counts": {"paragraphs": 2, "exclusions": 0},
}

TREND_CELL = "input_trends.json#/quarters/0/ratios/days_sales_outstanding"


def plant(tmp_path: Path) -> Path:
    """One run directory: two readers' committed inputs, and the manifest above."""
    root = tmp_path / "AAPL-10-K"
    for agent in ("notes_reader", "numbers_reader"):
        (root / agent).mkdir(parents=True)
    (root / "notes_reader" / "input_notes.md").write_text(NOTES, encoding="utf-8")
    for name, payload in (("input_trends.json", TRENDS_INPUT),
                          ("input_numbers.json", NUMBERS_INPUT)):
        (root / "numbers_reader" / name).write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (root / MANIFEST).write_text(
        json.dumps(MANIFEST_BEFORE, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return root


def notes_items() -> list[dict]:
    """Four items against the notes above: two verbatim, two altered on purpose."""
    return [
        {"id": "receivables_rose", "paragraph_id": f"{ACCESSION}:notes:1",
         "quote": "Accounts receivable, net of allowances, rose to $29,508 million"},
        # planted: the em dash of the filing written as a hyphen.
        {"id": "receivables_record_quarter", "paragraph_id": f"{ACCESSION}:notes:1",
         "quote": "rose to $29,508 million - the"},
        # planted: the line wrap of the filing joined into a single space.
        {"id": "receivables_largest_increase", "paragraph_id": f"{ACCESSION}:notes:1",
         "quote": "million — the largest quarterly increase"},
        {"id": "allowance_thinning", "paragraph_id": f"{ACCESSION}:notes:2",
         "quote": "The allowance for credit losses was reduced"},
    ]


def numbers_items() -> list[dict]:
    """Two computed rows, quoted as they print: a trend cell and a numeric fact."""
    return [
        {"id": "days_sales_outstanding_high", "paragraph_id": TREND_CELL,
         "quote": '"value": 51.7'},
        {"id": "receivables_on_the_balance_sheet",
         "paragraph_id": f"{ACCESSION}:receivables_net_current",
         "quote": '"value": 29508000000'},
    ]


def comparer_items() -> list[dict]:
    return [
        {"id": "receivables_priced_in", "upstream_item_id": "receivables_rose",
         "label": "priced_in"},
        # planted: a citation naming an id no reader report carries.
        {"id": "allowance_not_priced", "upstream_item_id": "allowance_reduced_early",
         "label": "not_priced"},
    ]


def three_layers(root: Path) -> list[dict]:
    return [
        {"report": "report_notes_text.md", "items": notes_items(),
         "input": root / "notes_reader"},
        {"report": "report_numbers.md", "items": numbers_items(),
         "input": root / "numbers_reader"},
        {"report": "report_numbers_vs_market.md", "items": comparer_items(),
         "cites": ["report_notes_text.md", "report_numbers.md"]},
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
        "receivables_record_quarter", "receivables_largest_increase",
        "allowance_not_priced"]
    assert kept_ids(result) == [
        "allowance_thinning", "days_sales_outstanding_high",
        "receivables_on_the_balance_sheet", "receivables_priced_in", "receivables_rose"]


def test_the_drop_count_reaches_the_manifest(tmp_path):
    root = plant(tmp_path)
    quote_gate.gate(three_layers(root), root)
    manifest = manifest_of(root)
    assert manifest["counts"]["dropped_items"] == 3
    assert len(manifest["dropped_items"]) == 3
    assert [row["item_id"] for row in manifest["dropped_items"]] == [
        "receivables_record_quarter", "receivables_largest_increase",
        "allowance_not_priced"]


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
    assert "does not string-match" in reason_for(result, "receivables_record_quarter")
    assert "does not string-match" in reason_for(result, "receivables_largest_increase")
    assert "does not resolve" in reason_for(result, "allowance_not_priced")


def test_gating_twice_writes_the_same_count(tmp_path):
    root = plant(tmp_path)
    quote_gate.gate(three_layers(root), root)
    quote_gate.gate(three_layers(root), root)
    assert manifest_of(root)["counts"]["dropped_items"] == 3


# --- string-match means string-match -----------------------------------------

def test_the_whole_paragraph_is_quotable(tmp_path):
    root = plant(tmp_path)
    item = {"id": "receivables_rose", "paragraph_id": f"{ACCESSION}:notes:1",
            "quote": "Accounts receivable, net of allowances, rose to $29,508 million — the\n"
                     "largest quarterly increase this company has on record."}
    assert kept_ids(gate_one(root, item)) == ["receivables_rose"]


def test_an_ellipsis_standing_in_for_words_does_not_match(tmp_path):
    root = plant(tmp_path)
    item = {"id": "receivables_rose", "paragraph_id": f"{ACCESSION}:notes:1",
            "quote": "Accounts receivable … rose to $29,508 million"}
    assert kept_ids(gate_one(root, item)) == []


def test_a_changed_case_does_not_match(tmp_path):
    root = plant(tmp_path)
    item = {"id": "receivables_rose", "paragraph_id": f"{ACCESSION}:notes:1",
            "quote": "accounts receivable, net of allowances"}
    assert kept_ids(gate_one(root, item)) == []


def test_an_empty_quote_is_dropped_rather_than_matching_everything(tmp_path):
    root = plant(tmp_path)
    item = {"id": "receivables_rose", "paragraph_id": f"{ACCESSION}:notes:1", "quote": ""}
    result = gate_one(root, item)
    assert kept_ids(result) == []
    assert "empty quote" in reason_for(result, "receivables_rose")


def test_a_quote_belonging_to_another_paragraph_is_dropped(tmp_path):
    root = plant(tmp_path)
    item = {"id": "allowance_thinning", "paragraph_id": f"{ACCESSION}:notes:2",
            "quote": "Accounts receivable, net of allowances"}
    assert kept_ids(gate_one(root, item)) == []


def test_a_paragraph_id_that_names_nothing_is_dropped(tmp_path):
    root = plant(tmp_path)
    item = {"id": "receivables_rose", "paragraph_id": f"{ACCESSION}:notes:9",
            "quote": "Accounts receivable, net of allowances"}
    result = gate_one(root, item)
    assert kept_ids(result) == []
    assert "not in this reader's committed input" in reason_for(result, "receivables_rose")


def test_an_item_with_no_id_is_dropped(tmp_path):
    root = plant(tmp_path)
    item = {"paragraph_id": f"{ACCESSION}:notes:2",
            "quote": "The allowance for credit losses was reduced"}
    result = gate_one(root, item)
    assert kept_ids(result) == []
    assert result["dropped"] == [{"report": "report_notes_text.md", "item_id": None,
                                  "reason": "the item carries no id, so nothing "
                                            "downstream could cite it"}]


# --- computed rows -----------------------------------------------------------

def test_a_trend_cell_is_quotable_as_the_row_it_prints(tmp_path):
    root = plant(tmp_path)
    assert quote_gate.committed_text(root / "numbers_reader", TREND_CELL) == \
        '{"days": 91, "value": 51.7}'


def test_a_pointer_into_a_row_that_is_not_there_names_nothing(tmp_path):
    root = plant(tmp_path)
    for pointer in ("input_trends.json#/quarters/1/ratios/days_sales_outstanding",
                    "input_trends.json#/quarters/0/ratios/gross_margin",
                    "input_market.json#/rows/0",
                    "input_trends.json#quarters"):
        assert quote_gate.committed_text(root / "numbers_reader", pointer) is None


def test_a_numeric_fact_is_quotable_by_the_id_it_already_carries(tmp_path):
    root = plant(tmp_path)
    item = {"id": "receivables_on_the_balance_sheet",
            "paragraph_id": f"{ACCESSION}:receivables_net_current",
            "quote": '"tag": "AccountsReceivableNetCurrent"'}
    assert kept_ids(gate_one(root, item, "numbers_reader")) == \
        ["receivables_on_the_balance_sheet"]


# --- citations ---------------------------------------------------------------

def test_an_item_that_cites_nothing_is_dropped(tmp_path):
    root = plant(tmp_path)
    result = quote_gate.gate([
        {"report": "report_notes_text.md", "items": notes_items(),
         "input": root / "notes_reader"},
        {"report": "report_notes_vs_market.md", "cites": ["report_notes_text.md"],
         "items": [{"id": "receivables_priced_in", "label": "priced_in"}]},
    ], root)
    assert kept_ids(result) == ["allowance_thinning", "receivables_rose"]
    assert "cites no upstream item" in reason_for(result, "receivables_priced_in")


def test_an_item_the_reader_layer_dropped_cannot_be_cited(tmp_path):
    root = plant(tmp_path)
    result = quote_gate.gate([
        {"report": "report_notes_text.md", "items": notes_items(),
         "input": root / "notes_reader"},
        {"report": "report_notes_vs_market.md", "cites": ["report_notes_text.md"],
         "items": [{"id": "record_quarter_priced_in",
                    "upstream_item_id": "receivables_record_quarter"}]},
    ], root)
    assert "record_quarter_priced_in" not in kept_ids(result)
    assert manifest_of(root)["counts"]["dropped_items"] == 3


def test_a_supervisor_item_needs_every_one_of_its_evidence_ids_to_resolve(tmp_path):
    root = plant(tmp_path)
    result = quote_gate.gate([
        {"report": "report_notes_text.md", "items": notes_items(),
         "input": root / "notes_reader"},
        {"report": "prediction_accounting.json", "cites": ["report_notes_text.md"],
         "items": [
             {"id": "receivables_outrun_revenue",
              "evidence": [{"upstream_item_id": "receivables_rose"},
                           {"upstream_item_id": "allowance_thinning"}]},
             {"id": "estimate_change_favorable",
              "evidence": [{"upstream_item_id": "receivables_rose"},
                           {"upstream_item_id": "estimate_relaxed"}]},
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
         "items": [{"id": "market_direction", "basis": ["receivables_rose",
                                                        "allowance_reduced_early"]}]},
    ], root)
    assert kept_ids(result) == ["allowance_thinning", "receivables_rose"]


# --- against a real committed input ------------------------------------------

def test_the_index_covers_a_real_assembled_bundle(tmp_path):
    """Planted prose is prose written to be matched. A filing is not.

    The claim here is not a value, which is why no number is asserted: it is
    that the index reaches a real bundle's note paragraphs at all, that a slice
    taken verbatim out of the longest of them stands, and that the same slice
    with one space added does not.
    """
    bundle = tmp_path / "bundle"
    assemble_bundle.write(assemble_bundle.build("AAPL", "10-Q"), bundle)
    index = quote_gate.quotable(bundle)
    identifier, text = max(((one, body) for one, body in index.items()
                            if ":notes:" in one), key=lambda pair: len(pair[1]))
    verbatim = text[:120]
    spaced = verbatim[:60] + " " + verbatim[60:]
    assert quote_gate.quote_drop_reason(
        {"id": "probe", "paragraph_id": identifier, "quote": verbatim}, bundle, index) is None
    assert quote_gate.quote_drop_reason(
        {"id": "probe", "paragraph_id": identifier, "quote": spaced}, bundle, index) \
        is not None


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
        quote_gate.quotable(root / "notes_reader")


def test_a_report_that_names_neither_an_input_nor_what_it_cites_is_refused(tmp_path):
    root = plant(tmp_path)
    with pytest.raises(QuoteGateError):
        quote_gate.gate([{"report": "report_notes_text.md", "items": notes_items()}], root)


def test_a_report_citing_one_that_has_not_been_gated_yet_is_refused(tmp_path):
    root = plant(tmp_path)
    with pytest.raises(QuoteGateError):
        quote_gate.gate([{"report": "report_notes_vs_market.md",
                          "items": comparer_items(),
                          "cites": ["report_notes_text.md"]}], root)


def test_a_manifest_that_is_not_there_is_refused(tmp_path):
    root = plant(tmp_path)
    (root / MANIFEST).unlink()
    with pytest.raises(CutoffGuardError):
        quote_gate.gate(three_layers(root), root)
