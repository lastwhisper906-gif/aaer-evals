"""Two expected values, and neither of them is anything this control produced.

The **schema** is `docs/CHECKLIST.md` §7, transcribed into `SCHEMA_BLOCK` below
by hand and then asserted to be a slice of that document, character for
character. Every field the control writes is asserted against it by name here,
not by handing the written file back to the checker that wrote it.

The **quotes** are slices of an input directory this file plants as characters,
and the judge that says they match is `src/quote_gate.py`, run over the file the
control wrote. A quote gate that dropped nothing because it can drop nothing
would pass that test on air, so the same gate is run over the altered quote on
its own and asserted to drop it -- the positive control beside the silence.

The altered quote is the ordinary shape of the failure: the filing's em dash
written as a hyphen. `src/quote_gate.py` normalizes nothing, so that is one
character of difference and the item goes.

The model is not called. `ask` here is a stub returning a payload written out in
this file, which is what makes the schema and the gate the only things under
test: the control's job is the prompt, the pin, the schema and the gate, and the
one call belongs to whoever runs the stage.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from src import agent_inputs, control_single_agent, quote_gate
from src.control_single_agent import ControlError

REPO_ROOT = Path(__file__).resolve().parent.parent
CHECKLIST = REPO_ROOT / "docs" / "CHECKLIST.md"
INPUT_SPEC = REPO_ROOT / "docs" / "INPUT_SPEC.md"
SUPERVISOR_PROMPT = REPO_ROOT / ".claude" / "agents" / "supervisor-accounting.md"

ACCESSION = "0000320193-25-000073"

# `docs/CHECKLIST.md` §7, "The two predictions", copied out by hand. The first
# test asserts this is still a slice of that file, so the fields asserted below
# are the document's and not this file's memory of it.
SCHEMA_BLOCK = '''{ "question": "accounting_reliability" | "financial_pressure",
  "rules_version": "0.1",
  "checklist": [ {"key": "", "finding": "", "confidence": 0,
                  "evidence": [{"upstream_item_id": ""}]} ],
  "continuous": [ {"key": "", "point": 0, "direction": "", "low": 0, "high": 0} ],
  "events": [ {"key": "", "p_within_horizon": 0} ],
  "explanations": [ {"id": "", "support": "sufficient|insufficient|unknown",
                     "realization_p": 0} ],
  "market_direction": {"p_up": 0, "basis": []},
  "tier": "elevated" | "watch" | "clear",
  "top_signals": [] }'''

# Every top-level field of that block, read off it one line at a time.
SCHEMA_FIELDS = ("question", "rules_version", "checklist", "continuous", "events",
                 "explanations", "market_direction", "tier", "top_signals")

# The model family `.claude/agents/supervisor-accounting.md` and
# `.claude/agents/supervisor-pressure.md` both name on their `model:` line.
SUPERVISOR_MODEL = "fable"
SERVED = "claude-fable-20260401"

# --- the input directory this file plants ------------------------------------
#
# Prose with the two features that separate a verbatim quote from a tidied one:
# an em dash, and a line wrap inside a sentence.

NOTES = f"""# Notes

[{ACCESSION}:notes:1]
Accounts receivable, net of allowances, rose to $29,508 million — the
largest quarterly increase this company has on record.

[{ACCESSION}:notes:2]
The allowance for credit losses was reduced during the period.
"""

# `input_trends.json` as `src/trends.py` commits it: two-space indent, sorted
# keys, one key to a line.
TRENDS = """{
  "quarters": [
    {
      "filled": true,
      "label": "Q-0",
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

# The market table declares no ids, so nothing in it is quotable. It is planted
# because the control is handed it and the prompt has to list it.
MARKET = """{
  "ticker": "AAPL",
  "rows": []
}
"""

MANIFEST = {"ticker": "AAPL", "accession": ACCESSION, "cutoff": "2025-10-31",
            "rules_version": "0.1", "counts": {"paragraphs": 2, "exclusions": 0}}

NOTES_ONE = f"{ACCESSION}:notes:1"
NOTES_TWO = f"{ACCESSION}:notes:2"
TREND_CELL = f"{ACCESSION}:trends:days_sales_outstanding:Q-0"

RECEIVABLES_QUOTE = "Accounts receivable, net of allowances, rose to $29,508 million"
ALLOWANCE_QUOTE = "The allowance for credit losses was reduced"
TREND_QUOTE = '"days": 91,\n          "value": 51.7'
# The same sentence with the filing's em dash written as a hyphen.
ALTERED_QUOTE = "rose to $29,508 million - the"


def plant(tmp_path: Path) -> tuple[Path, Path]:
    """The run directory, and the directory the control is handed."""
    root = tmp_path / "AAPL-10-K"
    folder = tmp_path / "single-agent"
    root.mkdir()
    folder.mkdir()
    (folder / "input_notes.md").write_text(NOTES, encoding="utf-8")
    (folder / "input_trends.json").write_text(TRENDS, encoding="utf-8")
    (folder / "input_market.json").write_text(MARKET, encoding="utf-8")
    (root / "input_manifest.json").write_text(
        json.dumps(MANIFEST, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return root, folder


# --- what the stub model answers ---------------------------------------------

def evidence(paragraph_id: str, quote: str) -> list[dict]:
    return [{"upstream_item_id": paragraph_id, "quote": quote}]


def accounting_answer() -> dict:
    """Four checklist entries, three quoted verbatim and one with the dash changed."""
    return {
        "question": "accounting_reliability",
        "rules_version": "0.1",
        "checklist": [
            {"key": "receivables_outrun_revenue", "finding": "flag",
             "confidence": 0.6, "evidence": evidence(NOTES_ONE, RECEIVABLES_QUOTE)},
            {"key": "bad_debt_reserve_thinning", "finding": "flag",
             "confidence": 0.4, "evidence": evidence(NOTES_TWO, ALLOWANCE_QUOTE)},
            {"key": "accruals_high", "finding": "no_flag",
             "confidence": 0.2, "evidence": evidence(TREND_CELL, TREND_QUOTE)},
            {"key": "estimate_change_favorable", "finding": "flag",
             "confidence": 0.5, "evidence": evidence(NOTES_ONE, ALTERED_QUOTE)},
        ],
        "events": [{"key": "late_filing", "p_within_horizon": 0.1}],
        "explanations": [{"id": f"{ACCESSION}:notes:2", "support": "insufficient",
                          "realization_p": 0.3}],
        "market_direction": {"p_up": 0.45, "basis": [NOTES_ONE]},
        "tier": "watch",
        "top_signals": ["receivables_outrun_revenue", "estimate_change_favorable"],
    }


def pressure_answer() -> dict:
    """The same shape with `continuous`, which is financial pressure's alone."""
    return {
        "question": "financial_pressure",
        "rules_version": "0.1",
        "checklist": [
            {"key": "gross_margin_falling", "finding": "flag", "confidence": 0.55,
             "evidence": evidence(TREND_CELL, TREND_QUOTE)},
        ],
        "continuous": [
            {"key": "revenue_growth_year_over_year", "point": -0.03,
             "direction": "down", "low": -0.08, "high": 0.01},
            {"key": "operating_margin", "point": 0.24, "direction": "down",
             "low": 0.21, "high": 0.27},
            {"key": "operating_cash_flow", "point": 26400000000.0,
             "direction": "down", "low": 22000000000.0, "high": 30000000000.0},
        ],
        "events": [{"key": "guidance_cut", "p_within_horizon": 0.2}],
        "explanations": [],
        "market_direction": {"p_up": "insufficient", "basis": []},
        "tier": "clear",
        "top_signals": ["gross_margin_falling"],
    }


class Stub:
    """One model call per question, and a record of what it was handed."""

    def __init__(self, answer: dict, served: str = SERVED):
        self.answer, self.served = answer, served
        self.prompts: list[str] = []
        self.models: list[str] = []

    def __call__(self, prompt: str, *, model: str) -> dict:
        self.prompts.append(prompt)
        self.models.append(model)
        return {"served_model": self.served, "text": json.dumps(self.answer)}


def go(root: Path, folder: Path, question: str, answer: dict, **kwargs) -> dict:
    """One control run, and everything it hands back."""
    return control_single_agent.run(question, input_dir=folder, bundle_root=root,
                                    ask=Stub(answer, **kwargs))


def written(root: Path, question: str) -> dict:
    name = control_single_agent.CONTROL_FILES[question]
    return json.loads((root / name).read_text(encoding="utf-8"))


# --- the expected values, before anything is run -----------------------------

def test_the_schema_asserted_here_is_the_one_the_checklist_gives():
    assert SCHEMA_BLOCK in CHECKLIST.read_text(encoding="utf-8")
    assert control_single_agent.SCHEMA == SCHEMA_BLOCK


def test_the_fields_asserted_here_are_every_field_that_schema_has():
    """Read back off the block rather than agreed with by a second hand list.

    Two lists written out by the same hand agree about a field both of them
    forgot; this scans the block for the keys at its own top level -- the ones
    opening the document or sitting at one indent -- so a field this file never
    heard of turns it red.
    """
    found = re.findall(r'^(?:\{ |  )"([a-z_]+)":', SCHEMA_BLOCK, flags=re.MULTILINE)
    assert found == list(SCHEMA_FIELDS)
    assert sorted(SCHEMA_FIELDS) == sorted(
        control_single_agent.FIELDS + (control_single_agent.CONTINUOUS,))


def test_the_quotes_planted_here_are_slices_of_the_input_planted_here():
    assert RECEIVABLES_QUOTE in NOTES
    assert ALLOWANCE_QUOTE in NOTES
    assert TREND_QUOTE in TRENDS
    # The one alteration: the em dash written as a hyphen, in no committed file.
    assert ALTERED_QUOTE not in NOTES


def test_the_control_borrows_the_model_the_supervisor_prompts_name():
    assert f"model: {SUPERVISOR_MODEL}" in SUPERVISOR_PROMPT.read_text(encoding="utf-8")
    assert control_single_agent.supervisor_model() == SUPERVISOR_MODEL


def test_the_two_control_files_are_the_two_the_input_spec_names():
    spec = INPUT_SPEC.read_text(encoding="utf-8")
    for name in control_single_agent.CONTROL_FILES.values():
        assert name in spec
        assert name in agent_inputs.BUNDLE_CATALOGUE


def test_supervisors_naming_two_models_leave_no_model_to_borrow(tmp_path):
    for name, model in (("supervisor-accounting.md", "fable"),
                        ("supervisor-pressure.md", "opus")):
        (tmp_path / name).write_text(f"---\nname: x\nmodel: {model}\n---\n",
                                     encoding="utf-8")
    with pytest.raises(ControlError) as caught:
        control_single_agent.supervisor_model(tmp_path)
    assert "different models" in str(caught.value)


# --- the file the control writes, field by field -----------------------------

def test_the_accounting_file_carries_every_field_of_the_schema_and_no_other(tmp_path):
    root, folder = plant(tmp_path)
    go(root, folder, "accounting_reliability", accounting_answer())
    payload = written(root, "accounting_reliability")
    # `continuous` is financial pressure only, so it is the one field of the
    # schema this question's file does not carry.
    assert sorted(payload) == sorted(set(SCHEMA_FIELDS) - {"continuous"})
    assert payload["question"] == "accounting_reliability"
    assert payload["rules_version"] == MANIFEST["rules_version"]
    assert payload["tier"] in ("elevated", "watch", "clear")
    assert payload["top_signals"] == ["receivables_outrun_revenue"]
    assert len(payload["top_signals"]) <= control_single_agent.TOP_SIGNALS_MAX


def test_every_checklist_entry_carries_the_schemas_four_members(tmp_path):
    root, folder = plant(tmp_path)
    go(root, folder, "accounting_reliability", accounting_answer())
    entries = written(root, "accounting_reliability")["checklist"]
    assert [entry["key"] for entry in entries] == [
        "receivables_outrun_revenue", "bad_debt_reserve_thinning", "accruals_high"]
    for entry in entries:
        assert sorted(entry) == ["confidence", "evidence", "finding", "key"]
        assert entry["finding"] in ("flag", "no_flag", "insufficient")
        assert 0 <= entry["confidence"] <= 1
        for cited in entry["evidence"]:
            assert sorted(cited) == ["quote", "upstream_item_id"]


def test_the_events_and_explanations_carry_the_members_the_schema_gives_them(tmp_path):
    root, folder = plant(tmp_path)
    go(root, folder, "accounting_reliability", accounting_answer())
    payload = written(root, "accounting_reliability")
    for entry in payload["events"]:
        assert sorted(entry) == ["key", "p_within_horizon"]
        assert 0 <= entry["p_within_horizon"] <= 1
    for entry in payload["explanations"]:
        assert sorted(entry) == ["id", "realization_p", "support"]
        assert entry["support"] in ("sufficient", "insufficient", "unknown")
        assert 0 <= entry["realization_p"] <= 1
    assert sorted(payload["market_direction"]) == ["basis", "p_up"]
    assert 0 <= payload["market_direction"]["p_up"] <= 1


def test_continuous_is_financial_pressure_and_only_financial_pressure(tmp_path):
    root, folder = plant(tmp_path)
    go(root, folder, "financial_pressure", pressure_answer())
    payload = written(root, "financial_pressure")
    assert sorted(payload) == sorted(SCHEMA_FIELDS)
    for entry in payload["continuous"]:
        assert sorted(entry) == ["direction", "high", "key", "low", "point"]
        assert entry["low"] <= entry["point"] <= entry["high"]
        assert entry["direction"]
    with pytest.raises(ControlError):
        control_single_agent.check_schema(
            pressure_answer() | {"question": "accounting_reliability"},
            "accounting_reliability", rules_version="0.1")


def test_p_up_may_be_insufficient_and_is_recorded_as_it_stands(tmp_path):
    root, folder = plant(tmp_path)
    result = go(root, folder, "financial_pressure", pressure_answer())
    assert written(root, "financial_pressure")["market_direction"] == {
        "p_up": "insufficient", "basis": []}
    assert result["dropped"] == []


def test_one_question_is_one_call_on_the_model_the_supervisor_names(tmp_path):
    root, folder = plant(tmp_path)
    stub = Stub(accounting_answer())
    control_single_agent.run("accounting_reliability", input_dir=folder,
                             bundle_root=root, ask=stub)
    assert stub.models == [SUPERVISOR_MODEL]
    assert len(stub.prompts) == 1


# --- the quote gate, over the control's own output ---------------------------

def gate_the_written_file(root: Path, folder: Path, question: str) -> tuple[list, dict]:
    """`src/quote_gate.py` over the evidence of the file the control wrote.

    The reader items are built here, out of the written file, so nothing in
    `src/` decides what the gate is shown.
    """
    payload = written(root, question)
    items = [{"id": f"{entry['key']}:{position}",
              "paragraph_id": cited["upstream_item_id"], "quote": cited["quote"]}
             for entry in payload["checklist"]
             for position, cited in enumerate(entry["evidence"], start=1)]
    return items, quote_gate.gate(
        [{"report": control_single_agent.CONTROL_FILES[question], "items": items,
          "input": folder}], root)


def test_the_quote_gate_keeps_every_item_of_the_file_the_control_wrote(tmp_path):
    root, folder = plant(tmp_path)
    go(root, folder, "accounting_reliability", accounting_answer())
    items, result = gate_the_written_file(root, folder, "accounting_reliability")
    # Counted here rather than read back: a gate shown nothing drops nothing.
    assert len(items) == 3
    assert result["dropped"] == []
    assert sorted(item["id"] for item in
                  result["kept"]["control_single_agent_accounting.json"]) == [
        "accruals_high:1", "bad_debt_reserve_thinning:1",
        "receivables_outrun_revenue:1"]


def test_the_gate_run_here_is_able_to_drop_the_altered_quote(tmp_path):
    """The positive control beside the silence above."""
    root, folder = plant(tmp_path)
    result = quote_gate.gate([{
        "report": "control_single_agent_accounting.json",
        "items": [{"id": "estimate_change_favorable:1", "paragraph_id": NOTES_ONE,
                   "quote": ALTERED_QUOTE}],
        "input": folder}], root)
    assert [row["item_id"] for row in result["dropped"]] == ["estimate_change_favorable:1"]
    assert "does not string-match" in result["dropped"][0]["reason"]


def test_every_basis_id_resolves_in_the_committed_input(tmp_path):
    root, folder = plant(tmp_path)
    go(root, folder, "accounting_reliability", accounting_answer())
    basis = written(root, "accounting_reliability")["market_direction"]["basis"]
    assert basis == [NOTES_ONE]
    index = quote_gate.quotable(folder, ACCESSION)
    assert all(one in index for one in basis)


def test_the_altered_quote_is_dropped_whole_and_counted(tmp_path):
    root, folder = plant(tmp_path)
    result = go(root, folder, "accounting_reliability", accounting_answer())
    assert [row["item_id"] for row in result["dropped"]] == [
        "accounting_reliability:checklist:estimate_change_favorable"]
    assert "does not string-match" in result["dropped"][0]["reason"]
    assert result["dropped"][0]["report"] == "control_single_agent_accounting.json"
    payload = written(root, "accounting_reliability")
    assert "estimate_change_favorable" not in [e["key"] for e in payload["checklist"]]
    # The top signal that named it goes with it.
    assert "estimate_change_favorable" not in payload["top_signals"]


def test_a_basis_that_resolves_to_nothing_becomes_the_schemas_own_abstention(tmp_path):
    root, folder = plant(tmp_path)
    answer = accounting_answer()
    answer["market_direction"] = {"p_up": 0.7, "basis": [f"{ACCESSION}:notes:99"]}
    result = go(root, folder, "accounting_reliability", answer)
    assert written(root, "accounting_reliability")["market_direction"] == {
        "p_up": "insufficient", "basis": []}
    assert "accounting_reliability:market_direction" in [
        row["item_id"] for row in result["dropped"]]


def test_an_insufficient_p_up_still_resolves_the_basis_it_carries(tmp_path):
    """The abstention excuses an empty basis, not an unresolvable one.

    Both supervisor prompts put it unconditionally -- "Python checks that each
    one resolves, and an unresolvable one is dropped and counted" -- so an
    `"insufficient"` p_up carrying ids that name nothing is a drop like any
    other, and what is written is the abstention with the basis emptied.
    """
    root, folder = plant(tmp_path)
    answer = accounting_answer()
    answer["market_direction"] = {"p_up": "insufficient",
                                  "basis": [f"{ACCESSION}:notes:99"]}
    result = go(root, folder, "accounting_reliability", answer)
    assert written(root, "accounting_reliability")["market_direction"] == {
        "p_up": "insufficient", "basis": []}
    assert "accounting_reliability:market_direction" in [
        row["item_id"] for row in result["dropped"]]


def test_an_evidence_entry_with_no_quote_is_refused(tmp_path):
    """§7 shows `evidence` with `upstream_item_id` alone; this control has no
    upstream report, so its id names a paragraph and the quote is the only
    thing Python can verify it by."""
    root, folder = plant(tmp_path)
    answer = accounting_answer()
    answer["checklist"][0]["evidence"] = [{"upstream_item_id": NOTES_ONE}]
    with pytest.raises(ControlError) as caught:
        go(root, folder, "accounting_reliability", answer)
    assert "quote" in str(caught.value)


def test_a_checklist_entry_resting_on_nothing_is_dropped(tmp_path):
    root, folder = plant(tmp_path)
    answer = accounting_answer()
    answer["checklist"][0]["evidence"] = []
    result = go(root, folder, "accounting_reliability", answer)
    reason = next(row["reason"] for row in result["dropped"] if row["item_id"]
                  == "accounting_reliability:checklist:receivables_outrun_revenue")
    assert "cites no upstream item" in reason


# --- what the control refuses ------------------------------------------------

def test_a_directory_holding_the_pipelines_own_output_is_refused(tmp_path):
    root, folder = plant(tmp_path)
    (folder / "report_numbers.md").write_text("# the numbers reader\n", encoding="utf-8")
    with pytest.raises(ControlError) as caught:
        go(root, folder, "accounting_reliability", accounting_answer())
    assert "report_numbers.md" in str(caught.value)


def test_an_empty_directory_is_refused(tmp_path):
    root, _ = plant(tmp_path)
    empty = tmp_path / "nothing"
    empty.mkdir()
    with pytest.raises(ControlError):
        go(root, empty, "accounting_reliability", accounting_answer())


def test_a_second_call_never_writes_over_the_first(tmp_path):
    root, folder = plant(tmp_path)
    go(root, folder, "accounting_reliability", accounting_answer())
    before = (root / "control_single_agent_accounting.json").read_text(encoding="utf-8")
    # The same answer again is the same bytes, and that is not a change.
    go(root, folder, "accounting_reliability", accounting_answer())
    answer = accounting_answer()
    answer["tier"] = "elevated"
    with pytest.raises(ControlError) as caught:
        go(root, folder, "accounting_reliability", answer)
    assert "append-only" in str(caught.value)
    assert (root / "control_single_agent_accounting.json").read_text(
        encoding="utf-8") == before


def test_the_control_file_is_never_written_through_a_link_out_of_the_run(tmp_path):
    root, folder = plant(tmp_path)
    elsewhere = tmp_path / "elsewhere.json"
    elsewhere.write_text("{}\n", encoding="utf-8")
    (root / "control_single_agent_accounting.json").symlink_to(elsewhere)
    with pytest.raises(ControlError) as caught:
        go(root, folder, "accounting_reliability", accounting_answer())
    assert "never through a link" in str(caught.value)
    assert elsewhere.read_text(encoding="utf-8") == "{}\n"


def test_a_served_model_from_another_family_is_refused(tmp_path):
    root, folder = plant(tmp_path)
    with pytest.raises(ControlError) as caught:
        go(root, folder, "accounting_reliability", accounting_answer(),
           served="claude-opus-20260401")
    assert "recorded as a failure" in str(caught.value)
    assert not (root / "control_single_agent_accounting.json").exists()


def test_the_model_does_not_name_the_rules_version(tmp_path):
    root, folder = plant(tmp_path)
    answer = accounting_answer()
    answer["rules_version"] = "0.2"
    with pytest.raises(ControlError) as caught:
        go(root, folder, "accounting_reliability", answer)
    assert "scored against its own rules version" in str(caught.value)


def test_a_run_with_no_rules_version_carries_the_null_the_manifest_carries(tmp_path):
    """`src/assemble_bundle.py` writes `rules_version: null` until `rules/v0.1`
    exists, so that is what a prediction from such a run carries."""
    root, folder = plant(tmp_path)
    (root / "input_manifest.json").write_text(
        json.dumps(MANIFEST | {"rules_version": None}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    answer = accounting_answer()
    answer["rules_version"] = None
    go(root, folder, "accounting_reliability", answer)
    assert written(root, "accounting_reliability")["rules_version"] is None


def test_an_answer_that_is_not_json_is_refused(tmp_path):
    root, folder = plant(tmp_path)

    def ask(prompt, *, model):
        return {"served_model": SERVED, "text": "I could not decide."}

    with pytest.raises(ControlError) as caught:
        control_single_agent.run("accounting_reliability", input_dir=folder,
                                 bundle_root=root, ask=ask)
    assert "not JSON" in str(caught.value)


def test_an_answer_to_the_other_question_is_refused(tmp_path):
    root, folder = plant(tmp_path)
    with pytest.raises(ControlError) as caught:
        go(root, folder, "accounting_reliability", pressure_answer())
    assert "never merged" in str(caught.value)


@pytest.mark.parametrize("field,value", [
    ("tier", "somewhat elevated"),
    ("top_signals", ["receivables_outrun_revenue", "no_such_indicator"]),
    ("events", [{"key": "late_filing", "p_within_horizon": 1.4}]),
    ("explanations", [{"id": "x", "support": "probably", "realization_p": 0.2}]),
    ("market_direction", {"p_up": 0.4}),
])
def test_a_field_outside_the_schema_is_refused(field, value):
    answer = accounting_answer() | {field: value}
    with pytest.raises(ControlError):
        control_single_agent.check_schema(answer, "accounting_reliability",
                                          rules_version="0.1")


@pytest.mark.parametrize("finding", ["flagged", "yes", "", None])
def test_a_finding_outside_the_three_the_checklist_allows_is_refused(finding):
    answer = accounting_answer()
    answer["checklist"][0]["finding"] = finding
    with pytest.raises(ControlError):
        control_single_agent.check_schema(answer, "accounting_reliability",
                                          rules_version="0.1")


@pytest.mark.parametrize("confidence", [-0.1, 1.1, "high", True, None])
def test_a_confidence_that_is_not_a_probability_is_refused(confidence):
    answer = accounting_answer()
    answer["checklist"][0]["confidence"] = confidence
    with pytest.raises(ControlError):
        control_single_agent.check_schema(answer, "accounting_reliability",
                                          rules_version="0.1")


def test_more_than_five_top_signals_is_refused():
    answer = accounting_answer()
    answer["checklist"] = [
        {"key": f"indicator_{name}", "finding": "flag", "confidence": 0.5,
         "evidence": evidence(NOTES_ONE, RECEIVABLES_QUOTE)}
        for name in ("one", "two", "three", "four", "five", "six")]
    answer["top_signals"] = [entry["key"] for entry in answer["checklist"]]
    with pytest.raises(ControlError) as caught:
        control_single_agent.check_schema(answer, "accounting_reliability",
                                          rules_version="0.1")
    assert "at most 5" in str(caught.value)


def test_one_indicator_one_key():
    answer = accounting_answer()
    answer["checklist"][1]["key"] = answer["checklist"][0]["key"]
    with pytest.raises(ControlError) as caught:
        control_single_agent.check_schema(answer, "accounting_reliability",
                                          rules_version="0.1")
    assert "more than once" in str(caught.value)


def test_a_continuous_point_outside_its_own_range_is_refused():
    answer = pressure_answer()
    answer["continuous"][0]["point"] = 0.5
    with pytest.raises(ControlError) as caught:
        control_single_agent.check_schema(answer, "financial_pressure",
                                          rules_version="0.1")
    assert "outside its own range" in str(caught.value)


def test_financial_pressure_with_no_continuous_values_is_refused():
    answer = pressure_answer()
    answer["continuous"] = []
    with pytest.raises(ControlError):
        control_single_agent.check_schema(answer, "financial_pressure",
                                          rules_version="0.1")


# --- the prompt, and the command line ----------------------------------------

def test_the_prompt_carries_the_schema_the_question_and_the_files(tmp_path):
    root, folder = plant(tmp_path)
    stub = Stub(accounting_answer())
    control_single_agent.run("accounting_reliability", input_dir=folder,
                             bundle_root=root, ask=stub)
    text = stub.prompts[0]
    assert SCHEMA_BLOCK in text
    assert "You answer one question: **accounting reliability**." in text
    assert "**financial pressure**" not in text
    for name in ("input_market.json", "input_notes.md", "input_trends.json"):
        assert f"- {name}" in text


def test_the_command_line_prints_the_call_it_would_make(tmp_path, capsys):
    _, folder = plant(tmp_path)
    code = control_single_agent.main(
        ["--question", "financial_pressure", "--input", str(folder)])
    printed = capsys.readouterr().out
    assert code == 0
    assert f"model: {SUPERVISOR_MODEL}" in printed
    assert "writes: control_single_agent_pressure.json" in printed
    assert SCHEMA_BLOCK in printed


def test_the_command_line_refuses_a_directory_it_cannot_read(tmp_path, capsys):
    code = control_single_agent.main(
        ["--question", "financial_pressure", "--input", str(tmp_path / "nowhere")])
    assert code == control_single_agent.BAD_INPUT
    assert "not a control" in capsys.readouterr().err
