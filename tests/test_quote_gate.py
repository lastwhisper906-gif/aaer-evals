"""Three alterations planted on purpose, and the count they leave in the manifest.

The committed input, the report items and the manifest here are all written by
this file, as text. Nothing is read back out of the gate to decide what the gate
should have said: the quotes that stand are slices of prose and of JSON rows
written a few lines above them, and the three items that fall are that same
prose with one character changed, that same prose with its line wrap trimmed
out, and a citation naming an id no report carries. The wrap used to be trimmed
to a space; since the owner's decision of 2026-09-23 the gate reads every
whitespace character as a space, so that one now stands, and the test that
says so is in the fold's section at the end.

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
import sys
import unicodedata
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
        {"id": "receivables_rose", "paragraph_id": f"{ACCESSION}:notes:1",
         "quote": "Accounts receivable, net of allowances, rose to $29,508 million"},
        # planted: the em dash of the filing written as a hyphen.
        {"id": "receivables_record_quarter", "paragraph_id": f"{ACCESSION}:notes:1",
         "quote": "rose to $29,508 million - the"},
        # planted: the line wrap of the filing trimmed out, two words run together.
        {"id": "receivables_largest_increase", "paragraph_id": f"{ACCESSION}:notes:1",
         "quote": "million — thelargest quarterly increase"},
        {"id": "allowance_thinning", "paragraph_id": f"{ACCESSION}:notes:2",
         "quote": "The allowance for credit losses was reduced"},
    ]


def numbers_items() -> list[dict]:
    """Two computed rows, quoted out of the files that print them."""
    return [
        {"id": "days_sales_outstanding_high", "paragraph_id": TREND_CELL,
         "quote": '"days": 91,\n          "value": 51.7'},
        {"id": "receivables_on_the_balance_sheet", "paragraph_id": FACT_ROW_ID,
         "quote": '"tag": "AccountsReceivableNetCurrent"'},
    ]


def notes_comparer_items() -> list[dict]:
    return [
        {"id": "receivables_priced_in", "upstream_item_id": "receivables_rose",
         "label": "priced_in"},
        # planted: a citation naming an id no reader report carries.
        {"id": "allowance_not_priced", "upstream_item_id": "allowance_reduced_early",
         "label": "not_priced"},
    ]


def numbers_comparer_items() -> list[dict]:
    return [{"id": "days_sales_outstanding_priced_in", "label": "priced_in",
             "upstream_item_id": "days_sales_outstanding_high"}]


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
        "receivables_record_quarter", "receivables_largest_increase",
        "allowance_not_priced"]
    assert kept_ids(result) == [
        "allowance_thinning", "days_sales_outstanding_high",
        "days_sales_outstanding_priced_in", "receivables_on_the_balance_sheet",
        "receivables_priced_in", "receivables_rose"]


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
    item = {"id": "days_sales_outstanding_high", "paragraph_id": TREND_CELL,
            "quote": one_line}
    result = gate_one(root, item, "numbers_reader")
    assert kept_ids(result) == []
    assert "does not string-match" in reason_for(result, "days_sales_outstanding_high")


def test_a_row_with_its_keys_reordered_does_not_match(tmp_path):
    root = plant(tmp_path)
    reordered = '"tag": "AccountsReceivableNetCurrent", "unit": "usd"'
    assert reordered not in NUMBERS
    item = {"id": "receivables_on_the_balance_sheet", "paragraph_id": FACT_ROW_ID,
            "quote": reordered}
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
    item = {"id": "market_moved", "paragraph_id": "input_market.json#/rows/0",
            "quote": '"abnormal_return": 0.031'}
    assert kept_ids(gate_one(root, item, "numbers_reader")) == []


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


# --- one id names one item ---------------------------------------------------

def test_two_items_in_one_report_sharing_an_id_are_both_dropped(tmp_path):
    """Otherwise a failed item stays citable under its twin's name.

    One of these two quotes matches and one is the planted hyphen. Keeping the
    good one would leave `twin` resolving downstream, which is the dropped
    item's id passed through by another name.
    """
    root = plant(tmp_path)
    result = quote_gate.gate([
        {"report": "report_notes_text.md", "input": root / "notes_reader", "items": [
            {"id": "twin", "paragraph_id": f"{ACCESSION}:notes:1",
             "quote": "Accounts receivable, net of allowances"},
            {"id": "twin", "paragraph_id": f"{ACCESSION}:notes:1",
             "quote": "rose to $29,508 million - the"},
        ]},
        {"report": "report_notes_vs_market.md", "cites": ["report_notes_text.md"],
         "items": [{"id": "twin_priced_in", "upstream_item_id": "twin"}]},
    ], root)
    assert kept_ids(result) == []
    assert "more than one item in this run" in reason_for(result, "twin")
    assert manifest_of(root)["counts"]["dropped_items"] == 3


def test_two_reports_sharing_an_item_id_lose_it_in_both(tmp_path):
    root = plant(tmp_path)
    result = quote_gate.gate([
        {"report": "report_notes_text.md", "input": root / "notes_reader",
         "items": [{"id": "shared", "paragraph_id": f"{ACCESSION}:notes:1",
                    "quote": "Accounts receivable, net of allowances"}]},
        {"report": "report_numbers.md", "input": root / "numbers_reader",
         "items": [{"id": "shared", "paragraph_id": FACT_ROW_ID,
                    "quote": '"tag": "AccountsReceivableNetCurrent"'}]},
        {"report": "report_notes_vs_market.md", "cites": ["report_notes_text.md"],
         "items": [{"id": "shared_priced_in", "upstream_item_id": "shared"}]},
    ], root)
    assert kept_ids(result) == []
    assert manifest_of(root)["counts"]["dropped_items"] == 3


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



# --- the one fold: whitespace is a space -------------------------------------
#
# The owner's decision of 2026-09-23: before a quote is matched, the
# non-breaking space and every other Unicode whitespace character is read as an
# ordinary space, on the quote and on the committed input alike, one character
# for one, and every quote that stood only through that is counted in the
# manifest. Nothing else is folded.

NBSP = "\u00a0"

# Unicode's White_Space property, copied by hand out of the Unicode Character
# Database's PropList.txt: twenty-five code points, U+0020 among them.
WHITE_SPACE = ([chr(code) for code in range(0x0009, 0x000D + 1)]
               + ["\u0020", "\u0085", "\u00a0", "\u1680"]
               + [chr(code) for code in range(0x2000, 0x200A + 1)]
               + ["\u2028", "\u2029", "\u202f", "\u205f", "\u3000"])


def test_the_fold_is_unicodes_own_whitespace():
    """The module writes its list out; the expected value is PropList.txt's."""
    assert len(WHITE_SPACE) == len(set(WHITE_SPACE)) == 25
    assert len(quote_gate.WHITESPACE) == len(set(quote_gate.WHITESPACE)) == 24
    assert set(quote_gate.WHITESPACE) == set(WHITE_SPACE) - {" "}


def test_every_space_separator_unicodedata_knows_is_folded():
    """A second source for part of the same list: category Zs, off `unicodedata`."""
    separators = {chr(code) for code in range(sys.maxunicode + 1)
                  if unicodedata.category(chr(code)) == "Zs"}
    assert NBSP in separators
    assert separators - {" "} <= set(quote_gate.WHITESPACE)


# --- the seven quotes the second pipeline check dropped ----------------------
#
# The second pipeline check (PR #73) read NVDA's 10-Q 0001045810-26-000075 and
# dropped seven of the notes reader's forty items, each quote differing from its
# committed paragraph only where the paragraph holds U+00A0 and the reader wrote
# U+0020. Four of those seven paragraphs are below, copied by hand out of
# `runs/NVDA/0001045810-26-000075/agents/notes-text-reader/input_notes.md` on the
# branch `runs/pipeline-check-2`, which is not merged, so the source is read with
# `git show origin/runs/pipeline-check-2:<that path>`. Each U+00A0 is written as
# an escape so it can be seen; each quote is the reader's own, copied out of
# `report_notes_text.md` beside it, where every space is U+0020. The item ids
# are written here: the reader numbered its items, and a numbered id is a
# letter-number code.

NVDA = "0001045810-26-000075"
NVDA_PARAGRAPHS = {
    f"{NVDA}:notes:61": (
        "(1)\u00a0\u00a0\u00a0\u00a0Included customer advances and unearned revenue "
        "primarily related to hardware and software support, and license and "
        "development arrangements. The balance as of July\u00a026, 2026, and "
        "January\u00a025, 2026, included $2.8 billion and $160 million of customer "
        "advances, respectively."),
    f"{NVDA}:notes:90": (
        "In June 2026, we issued an aggregate of $25.0\u00a0billion of senior "
        "unsecured notes across seven tranches for general corporate purposes."),
    f"{NVDA}:notes:93": (
        "As of July\u00a026, 2026, we complied with the required covenants under the "
        "outstanding notes."),
    f"{NVDA}:notes:99": (
        "Supply and capacity \u2013 We have partnered with our extensive network to "
        "secure the necessary supply and critical components needed to meet demand "
        "for the next several years, increasing supply commitments from $119 billion "
        "last quarter to $279 billion as of July\u00a026, 2026. These supply "
        "commitments are for our data center infrastructure systems, primarily "
        "memory and manufacturing facilities, to produce our products for long-term "
        "demand across current and future product architectures. We enter into "
        "agreements with our suppliers that allow them to procure inventory based "
        "upon our defined criteria, and in certain instances, these agreements may "
        "be cancelable, rescheduled, or adjustable for our business needs prior to "
        "placing firm orders. Changes to these agreements may result in additional "
        "costs."),
}

# (item id, paragraph id, the reader's quote, characters folded) -- the count is
# the U+00A0 inside the quoted span of the paragraph above, counted by eye.
NVDA_QUOTES = [
    (f"{NVDA}:notes:61:customer-advances", f"{NVDA}:notes:61",
     "The balance as of July 26, 2026, and January 25, 2026, included $2.8 billion "
     "and $160 million of customer advances, respectively.", 2),
    (f"{NVDA}:notes:90:senior-notes-issued", f"{NVDA}:notes:90",
     "In June 2026, we issued an aggregate of $25.0 billion of senior unsecured "
     "notes across seven tranches for general corporate purposes.", 1),
    (f"{NVDA}:notes:93:covenants-met", f"{NVDA}:notes:93",
     "As of July 26, 2026, we complied with the required covenants under the "
     "outstanding notes.", 1),
    (f"{NVDA}:notes:99:supply-commitments-up", f"{NVDA}:notes:99",
     "increasing supply commitments from $119 billion last quarter to $279 billion "
     "as of July 26, 2026", 1),
]


def plant_nvda(tmp_path: Path) -> Path:
    """A run directory holding the four NVDA paragraphs as the notes reader's input."""
    root = tmp_path / "NVDA-10-Q"
    (root / "notes_reader").mkdir(parents=True)
    notes = f"# NVDA notes — {NVDA}\n\n" + "\n".join(
        f"[{paragraph}]\n{text}\n" for paragraph, text in NVDA_PARAGRAPHS.items())
    (root / "notes_reader" / "input_notes.md").write_text(notes, encoding="utf-8")
    (root / MANIFEST).write_text(json.dumps(
        {"ticker": "NVDA", "accession": NVDA, "counts": {"paragraphs": 4}},
        indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return root


def gate_nvda(root: Path, items: list[dict]) -> dict:
    return quote_gate.gate([{"report": "report_notes_text.md", "items": items,
                             "input": root / "notes_reader"}], root)


def nvda_item(identifier: str, paragraph: str, quote: str) -> dict:
    return {"id": identifier, "paragraph_id": paragraph, "quote": quote}


def test_the_dropped_quotes_fail_as_written_and_differ_only_by_the_space():
    """The precondition, so the next test is about the fold and nothing else."""
    for _, paragraph, quote, _ in NVDA_QUOTES:
        text = NVDA_PARAGRAPHS[paragraph]
        assert NBSP not in quote
        assert quote not in text
        assert quote in text.replace(NBSP, " ")


def test_the_dropped_quotes_now_stand(tmp_path):
    root = plant_nvda(tmp_path)
    result = gate_nvda(root, [nvda_item(*row[:3]) for row in NVDA_QUOTES])
    assert result["dropped"] == []
    assert kept_ids(result) == sorted(row[0] for row in NVDA_QUOTES)


def test_the_dropped_quotes_are_each_counted_as_folded(tmp_path):
    root = plant_nvda(tmp_path)
    result = gate_nvda(root, [nvda_item(*row[:3]) for row in NVDA_QUOTES])
    expected = [{"report": "report_notes_text.md", "item_id": identifier,
                 "paragraph_id": paragraph, "characters": characters}
                for identifier, paragraph, _, characters in NVDA_QUOTES]
    manifest = manifest_of(root)
    assert manifest["normalized_quotes"] == expected
    assert manifest["counts"]["normalized_quotes"] == 4
    assert manifest["counts"]["dropped_items"] == 0
    assert result["normalized"] == expected


def test_a_changed_word_in_a_dropped_quote_still_falls(tmp_path):
    root = plant_nvda(tmp_path)
    identifier = f"{NVDA}:notes:90:senior-notes-issued"
    result = gate_nvda(root, [nvda_item(
        identifier, f"{NVDA}:notes:90",
        "In June 2026, we issued an aggregate of $25.0 million of senior unsecured")])
    assert kept_ids(result) == []
    assert "does not string-match" in reason_for(result, identifier)
    assert manifest_of(root)["normalized_quotes"] == []


def test_a_changed_dash_in_a_real_paragraph_still_falls(tmp_path):
    """The filing's en dash written as a hyphen, with the fold in force."""
    root = plant_nvda(tmp_path)
    identifier = f"{NVDA}:notes:99:supply-partners"
    paragraph = f"{NVDA}:notes:99"
    hyphen = "Supply and capacity - We have partnered with our extensive network"
    result = gate_nvda(root, [nvda_item(identifier, paragraph, hyphen)])
    assert kept_ids(result) == []
    assert "does not string-match" in reason_for(result, identifier)
    en_dash = hyphen.replace(" - ", " \u2013 ")
    assert kept_ids(gate_nvda(root, [nvda_item(identifier, paragraph, en_dash)])) == [
        identifier]


# --- what the fold reaches, and what it does not -----------------------------

SPACED = f"{ACCESSION}:notes:3"
SPACED_PARAGRAPH = (f"[{SPACED}]\n"
                    f"Revenue was $46.7{NBSP}billion, up 56%{NBSP}from a year ago.\n")
REVENUE_UP = f"{SPACED}:revenue-up"


def plant_spaced(tmp_path: Path) -> Path:
    root = plant(tmp_path)
    (root / "notes_reader" / "input_notes.md").write_text(
        NOTES + "\n" + SPACED_PARAGRAPH, encoding="utf-8")
    return root


def spaced_item(quote: str) -> dict:
    return {"id": REVENUE_UP, "paragraph_id": SPACED, "quote": quote}


def test_the_fold_runs_on_both_sides(tmp_path):
    """A U+00A0 in the quote where the input holds U+0020 stands too."""
    root = plant(tmp_path)
    item = {"id": "allowance_thinning", "paragraph_id": f"{ACCESSION}:notes:2",
            "quote": f"The allowance for{NBSP}credit losses"}
    assert kept_ids(gate_one(root, item)) == ["allowance_thinning"]


def test_the_filings_line_wrap_written_as_a_space_now_stands_and_is_counted(tmp_path):
    """The rule this decision reverses.

    Until 2026-09-23 this quote was one of the gate's planted drops: the
    filing's line break written as an ordinary space. A line break is Unicode
    whitespace, so it now stands, and the manifest says it stood only through
    the fold. The planted wrap in `notes_items` is now the wrap trimmed out.
    """
    root = plant(tmp_path)
    identifier = "receivables_largest_increase"
    result = gate_one(root, {"id": identifier, "paragraph_id": f"{ACCESSION}:notes:1",
                             "quote": "million — the largest quarterly increase"})
    assert kept_ids(result) == [identifier]
    assert manifest_of(root)["normalized_quotes"] == [
        {"report": "report_notes_text.md", "item_id": identifier,
         "paragraph_id": f"{ACCESSION}:notes:1", "characters": 1}]


def test_a_computed_row_is_folded_one_for_one_as_prose_is(tmp_path):
    """The fold reaches the JSON inputs, and no further than it reaches prose.

    The trend row's line break written as a space, with its ten-space indent
    kept, stands and is counted. The row re-rendered onto one line still falls:
    collapsing the indent changes the row's length, and the fold never does.
    """
    root = plant(tmp_path)
    identifier = "days_sales_outstanding_high"
    line_break_as_space = '"days": 91,' + " " * 11 + '"value": 51.7'
    assert line_break_as_space.replace(" " * 11, "\n" + " " * 10) in TREND_ROW
    result = gate_one(root, {"id": identifier, "paragraph_id": TREND_CELL,
                             "quote": line_break_as_space}, "numbers_reader")
    assert kept_ids(result) == [identifier]
    assert manifest_of(root)["normalized_quotes"] == [
        {"report": "report_notes_text.md", "item_id": identifier,
         "paragraph_id": TREND_CELL, "characters": 1}]

    root = plant(tmp_path / "again")
    one_line = '{"days": 91, "value": 51.7}'
    result = gate_one(root, {"id": identifier, "paragraph_id": TREND_CELL,
                             "quote": one_line}, "numbers_reader")
    assert kept_ids(result) == []
    assert manifest_of(root)["normalized_quotes"] == []


@pytest.mark.parametrize("quote", [
    "Revenue was $46.7  billion, up 56% from",     # a run is not collapsed
    "Revenue was $46.7billion, up 56% from",       # a space is not dropped
    "Revenue was $46.7 billion, up 56 % from",     # nor is one added
    "Revenue was $46.7 billion, up 56%\n\nfrom",   # one for one: two for one falls
])
def test_the_fold_is_one_character_for_one_and_nothing_else(tmp_path, quote):
    root = plant_spaced(tmp_path)
    result = gate_one(root, spaced_item(quote))
    assert kept_ids(result) == []
    assert manifest_of(root)["normalized_quotes"] == []


@pytest.mark.parametrize("written", ["\t", "\n", "\u2028", "\u202f", "\u3000"])
def test_any_whitespace_in_the_quote_reads_as_the_inputs_space(tmp_path, written):
    root = plant_spaced(tmp_path)
    quote = f"Revenue was $46.7{written}billion, up 56% from"
    assert kept_ids(gate_one(root, spaced_item(quote))) == [REVENUE_UP]


def test_every_quote_that_stood_only_through_the_fold_is_counted_in_the_manifest(
        tmp_path):
    root = plant_spaced(tmp_path)
    items = notes_items() + [spaced_item("Revenue was $46.7 billion, up 56% from")]
    result = quote_gate.gate(
        [{"report": "report_notes_text.md", "items": items,
          "input": root / "notes_reader"}], root)
    manifest = manifest_of(root)
    expected = [{"report": "report_notes_text.md", "item_id": REVENUE_UP,
                 "paragraph_id": SPACED, "characters": 2}]
    assert manifest["normalized_quotes"] == expected
    assert manifest["counts"]["normalized_quotes"] == 1
    assert result["normalized"] == expected
    # The drops beside it are the planted two, unchanged by the fold.
    assert [row["item_id"] for row in manifest["dropped_items"]] == [
        "receivables_record_quarter", "receivables_largest_increase"]


def test_a_run_with_nothing_folded_says_zero(tmp_path):
    root = plant(tmp_path)
    quote_gate.gate(three_layers(root), root)
    manifest = manifest_of(root)
    assert manifest["normalized_quotes"] == []
    assert manifest["counts"]["normalized_quotes"] == 0


@pytest.mark.parametrize("quote, text, expected", [
    ("a b", "a b", 0),
    ("a b", f"a{NBSP}b", 1),
    (f"a{NBSP}b", "a b", 1),
    ("a b c", f"a{NBSP}b\nc", 2),
    ("a b", "a\tb", 1),
    ("a b", "a\r\nb", None),
    ("ab", "a b", None),
    ("a b", "a c", None),
    ("a - b", "a \u2013 b", None),
])
def test_folded_characters_counts_the_characters_the_fold_changed(quote, text, expected):
    assert quote_gate.folded_characters(quote, text) == expected


@pytest.mark.parametrize("text", [
    f"a{NBSP}b{NBSP}c, and a b{NBSP}c",
    f"a b{NBSP}c, and a{NBSP}b{NBSP}c",
])
def test_a_quote_the_input_holds_twice_is_counted_where_it_needed_the_fewest(text):
    """The count is the quote's own, not the order the text happens to be in."""
    assert quote_gate.folded_characters("a b c", text) == 1


@pytest.mark.parametrize("character", [
    "\u001c",   # a file separator: `str.isspace` says yes, White_Space says no
    "\u200b",   # a zero-width space
    "\u180e",   # the Mongolian vowel separator, out of White_Space since 6.3
    "\ufeff",   # a zero-width no-break space
])
def test_a_character_outside_white_space_is_not_folded(character):
    assert quote_gate.folded(f"a{character}b") == f"a{character}b"
    assert quote_gate.folded_characters("a b", f"a{character}b") is None
    assert quote_gate.folded_characters(f"a{character}b", "a b") is None


@pytest.mark.parametrize("quote, text", [
    ("\u201cnet\u201d", '"net"'),    # curly quotation marks are not straight ones
    ("x\u00b2", "x2"),               # a superscript two is not a two
    ("\uff21", "A"),                 # a fullwidth letter is not a letter
    ("a\u2014b", "a-b"),             # an em dash is not a hyphen
])
def test_nothing_but_whitespace_is_folded(quote, text):
    assert quote_gate.folded_characters(quote, text) is None
    assert quote_gate.folded_characters(text, quote) is None
