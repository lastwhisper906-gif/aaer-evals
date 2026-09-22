"""Four expected values, and none of them is anything this control produced.

The **schema** is `docs/CHECKLIST.md` §7, transcribed into `SCHEMA_BLOCK` below
by hand and then asserted to be a slice of that document, character for
character. Every field the control writes is asserted against it by name here,
not by handing the written file back to the checker that wrote it. The members
of `evidence` are *read off that block* rather than written out a second time:
two hand lists agree with each other and not with the document the day it moves,
and §7 gives `evidence` one member while this control carries two, so the one it
adds is named here beside the reason rather than mixed into a list.

The **cutoff** is `tests/fixtures/AAPL/manifest.json`, EDGAR's own record of when
the accession this run names was filed — 2025-10-31 for 0000320193-25-000079.
The test reads it out of that file with `json`, importing nothing from `src/`,
and the control has to agree with it. `CLAUDE.md` makes the cutoff the filing
date of the triggering report, so a run whose manifest says otherwise is a run
whose boundary has moved for itself.

The **ids that resolve to nothing** are planted: one naming another company's
accession, NVDA's 10-K, and one naming a paragraph of this company that no
committed file declares. Neither is in the index `src/quote_gate.py` builds from
the planted directory, which is what makes the expected result a drop.

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

import datetime as dt
import json
import re
from pathlib import Path

import pytest

from src import agent_inputs, control_single_agent, quote_gate
from src.control_single_agent import ControlError

REPO_ROOT = Path(__file__).resolve().parent.parent
CHECKLIST = REPO_ROOT / "docs" / "CHECKLIST.md"
INPUT_SPEC = REPO_ROOT / "docs" / "INPUT_SPEC.md"
HOW_WE_WORK = REPO_ROOT / "docs" / "HOW_WE_WORK.md"
SUPERVISOR_PROMPT = REPO_ROOT / ".claude" / "agents" / "supervisor-accounting.md"
FIXTURES = REPO_ROOT / "tests" / "fixtures"

# Apple's 10-K, and the date `tests/fixtures/AAPL/manifest.json` records it as
# filed on. Both are asserted against that file below before anything runs.
TICKER = "AAPL"
ACCESSION = "0000320193-25-000079"
FILED = "2025-10-31"

# Another company's filing, and a paragraph of this one that no file declares.
# Neither is in the index the planted directory offers, so both are drops.
OTHER_ACCESSION = "0001045810-25-000023"
NO_SUCH_PARAGRAPH = f"{ACCESSION}:notes:99"

# An earlier quarter of this company and a later one, both out of the same
# fixture record and asserted against it below. The earlier is what
# `input_prior_predictions.md` mints its ids from, so it has to stay allowed;
# the later is the cutoff rule read over the record.
PRIOR_ACCESSION = "0000320193-24-000123"
LATER_ACCESSION = "0000320193-26-000020"

MANIFEST_NAME = "input_manifest.json"

# What a control directory may not hold: a price file carrying the outcome
# window, and another company's notes. The first wears the `input_` prefix the
# old guard read as sufficient; the second wears no catalogue name at all.
OUTCOME_WINDOW_PRICES = "input_prices_outcome_window.json"
OTHER_COMPANY_NOTES = "NVDA_notes.md"

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


def schema_members(field: str) -> tuple[str, ...]:
    """The members §7 gives one of its list-of-objects fields, off the block.

    Read rather than transcribed a second time: a list written out here agrees
    with the list written out in `src/control_single_agent.py` and with nothing
    else, so the day the document gains a member the two go on agreeing with
    each other about a shape neither of them has any more.
    """
    found = re.search(rf'"{field}":\s*\[\s*\{{(.*?)\}}\s*\]',
                      SCHEMA_BLOCK, flags=re.DOTALL)
    assert found is not None, f"§7 shows no object under {field}"
    return tuple(re.findall(r'"([a-z_]+)":', found.group(1)))


def spec_input_names() -> tuple[str, ...]:
    """The `input_` files `docs/INPUT_SPEC.md` §6 lists, read off that list.

    The document, not the module's own comprehension over
    `agent_inputs.BUNDLE_CATALOGUE`. Two readings of one document can be
    compared; a reading compared with itself cannot.
    """
    text = INPUT_SPEC.read_text(encoding="utf-8")
    block = re.search(r"```\n(input_numbers\.json.*?)```", text, flags=re.DOTALL)
    assert block is not None, "§6 shows no file list"
    return tuple(re.findall(r"^(input_\S+)", block.group(1), flags=re.MULTILINE))


# §6's own line for the manifest, read out of the document so the test that
# says what it holds is quoting rather than remembering.
SPEC_MANIFEST_LINE = re.search(
    r"^input_manifest\.json.*?(?=^\S)",
    INPUT_SPEC.read_text(encoding="utf-8"),
    flags=re.MULTILINE | re.DOTALL).group(0)

# §7 shows `evidence` with `upstream_item_id` alone. This control has no
# upstream report — its upstream is the committed filing — so the id it writes
# names a paragraph, and a paragraph id is verified by quoting it. `quote` is
# named here, once, beside that reason.
QUOTE = "quote"
EVIDENCE_MEMBERS = schema_members("evidence") + (QUOTE,)

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

MANIFEST = {"ticker": TICKER, "accession": ACCESSION, "cutoff": FILED,
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


def test_the_evidence_members_are_the_schemas_own_plus_the_quote():
    """The one member this control adds to §7's, and nothing else.

    Both sides now come off the block above: the module derives its own tuple
    the same way, so a member added to §7 reaches the control instead of being
    outvoted by two copies of the old shape.
    """
    assert schema_members("evidence") == ("upstream_item_id",)
    assert control_single_agent.EVIDENCE_FIELDS == EVIDENCE_MEMBERS
    assert QUOTE not in schema_members("evidence")


def test_the_accession_and_cutoff_planted_here_are_the_ones_edgar_recorded():
    """The expected cutoff, read out of the fixture record by this file.

    `json` and a path, importing nothing from `src/`: the date the control has
    to agree with comes from the record of what EDGAR published, not from the
    module that checks it or from the manifest the run wrote about itself.
    """
    recorded = json.loads((FIXTURES / TICKER / "manifest.json").read_text(
        encoding="utf-8"))
    dates = {row["filing_date"] for row in recorded["documents"]
             if row["accession"] == ACCESSION}
    assert dates == {FILED}
    assert MANIFEST["cutoff"] == FILED
    # And the other company's accession is another company's, on its own record.
    other = json.loads((FIXTURES / "NVDA" / "manifest.json").read_text(
        encoding="utf-8"))
    assert OTHER_ACCESSION in {row["accession"] for row in other["documents"]}
    assert OTHER_ACCESSION not in {row["accession"] for row in recorded["documents"]}


def test_the_controls_are_done_when_every_citation_resolves():
    """What the explanation drops below are measured against."""
    assert ("control files, with every citation resolving"
            in HOW_WE_WORK.read_text(encoding="utf-8"))


def test_the_layer_guard_this_directory_guard_copies_refuses_a_link_too():
    """Where the symlink refusal below comes from: the committed layer guard.

    `src/agent_inputs.py` refuses anything outside what a layer may hold, and a
    link is one of the things it names by hand. The control's directory is not
    one that file builds, so the rule is asserted against its source here rather
    than inherited by calling it.
    """
    source = (REPO_ROOT / "src" / "agent_inputs.py").read_text(encoding="utf-8")
    assert "a link's ancestors are the bundle's" in source


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
            assert sorted(cited) == sorted(EVIDENCE_MEMBERS)


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


def test_the_explanation_planted_here_resolves_and_stands(tmp_path):
    """The positive control beside the two drops below.

    A gate that dropped every explanation would pass those two on air, so the
    one that resolves is asserted to survive into the written file first.
    """
    root, folder = plant(tmp_path)
    result = go(root, folder, "accounting_reliability", accounting_answer())
    assert [entry["id"] for entry in written(root, "accounting_reliability")
            ["explanations"]] == [NOTES_TWO]
    assert NOTES_TWO in quote_gate.quotable(folder, ACCESSION)
    assert not [row for row in result["dropped"] if "explanations" in row["item_id"]]


def test_an_explanation_naming_another_companys_accession_is_dropped_and_counted(tmp_path):
    """§7 step 6: both control files, with every citation resolving."""
    root, folder = plant(tmp_path)
    answer = accounting_answer()
    answer["explanations"] = [
        {"id": f"{OTHER_ACCESSION}:notes:1", "support": "sufficient",
         "realization_p": 0.4}]
    result = go(root, folder, "accounting_reliability", answer)
    assert written(root, "accounting_reliability")["explanations"] == []
    row = next(row for row in result["dropped"]
               if row["item_id"].endswith(f"{OTHER_ACCESSION}:notes:1"))
    assert row["item_id"] == (
        f"accounting_reliability:explanations:{OTHER_ACCESSION}:notes:1")
    assert "does not resolve to an upstream item" in row["reason"]
    assert row["report"] == "control_single_agent_accounting.json"


def test_an_explanation_naming_a_paragraph_that_exists_nowhere_is_dropped(tmp_path):
    root, folder = plant(tmp_path)
    answer = accounting_answer()
    answer["explanations"] = [
        {"id": NO_SUCH_PARAGRAPH, "support": "unknown", "realization_p": 0.5},
        {"id": NOTES_ONE, "support": "sufficient", "realization_p": 0.2}]
    result = go(root, folder, "accounting_reliability", answer)
    # The one that resolves stays; only the one that names nothing goes.
    assert [entry["id"] for entry in written(root, "accounting_reliability")
            ["explanations"]] == [NOTES_ONE]
    assert [row["item_id"] for row in result["dropped"]
            if "explanations" in row["item_id"]] == [
        f"accounting_reliability:explanations:{NO_SUCH_PARAGRAPH}"]


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


def test_a_price_file_carrying_the_outcome_window_is_refused(tmp_path):
    """The `input_` prefix is not a passport.

    The guard used to refuse only the names it recognised as the pipeline's, so
    a file nobody routed went through and was listed to the model under "you
    see these files and nothing else". `src/agent_inputs.py` refuses anything
    outside what a layer may hold, for the reason its own message gives, and
    this is the same rule at the control's directory.
    """
    root, folder = plant(tmp_path)
    (folder / OUTCOME_WINDOW_PRICES).write_text(
        '{"ticker": "AAPL", "close": [190.1, 193.4], "window": "reaction_day_60"}\n',
        encoding="utf-8")
    with pytest.raises(ControlError) as caught:
        go(root, folder, "accounting_reliability", accounting_answer())
    assert OUTCOME_WINDOW_PRICES in str(caught.value)
    assert not (root / "control_single_agent_accounting.json").exists()


def test_another_companys_notes_in_the_control_directory_are_refused(tmp_path):
    root, folder = plant(tmp_path)
    (folder / OTHER_COMPANY_NOTES).write_text(
        f"# Notes\n\n[{OTHER_ACCESSION}:notes:1]\nAnother company's prose.\n",
        encoding="utf-8")
    with pytest.raises(ControlError) as caught:
        go(root, folder, "accounting_reliability", accounting_answer())
    assert OTHER_COMPANY_NOTES in str(caught.value)


def test_the_files_the_control_may_hold_are_the_bundles_and_the_market_table(tmp_path):
    """The allowlist is §6's own list, read off §6 and not off the module.

    The first version of this test asserted the set against the comprehension
    the module builds it with, which is the module's answer restated: a prefix
    reading that swept in a file no layer sees would have moved this expected
    value along with it. §6's fenced list is the document, and it is what the
    control is measured against here.
    """
    _, folder = plant(tmp_path)
    listed = spec_input_names()
    assert "input_market.json" in listed and MANIFEST_NAME in listed
    # `input_controls.md` is the one bundle file §6's list does not print, and
    # `src/agent_inputs.py` says so where it adds it. Named here once, with its
    # source asserted, rather than taken on faith from the catalogue.
    assert "input_controls.md" not in listed
    assert "§6 names, plus `input_controls.md`" in (
        REPO_ROOT / "src" / "agent_inputs.py").read_text(encoding="utf-8")
    assert set(control_single_agent.CONTROL_SEES) == (
        set(listed) | {"input_controls.md"}) - {MANIFEST_NAME}
    assert "report_numbers.md" not in control_single_agent.CONTROL_SEES
    assert OUTCOME_WINDOW_PRICES not in control_single_agent.CONTROL_SEES
    assert control_single_agent.input_files(folder) == [
        "input_market.json", "input_notes.md", "input_trends.json"]


def test_the_manifest_is_the_runs_bookkeeping_and_no_layer_sees_it(tmp_path):
    """Why `input_manifest.json` is the one `input_` name left off the list.

    §6's own line for it — read here, not paraphrased — gives it the
    dropped-item counts and the served models. `src/quote_gate.py` writes the
    three layers' dropped rows there, and they are written before `controls`
    runs, so a control reading it reads the pipeline's own output: the thing the
    guard refuses a report for. No agent in `src/agent_inputs.py` sees it
    either, which is the second reading of the same fact.
    """
    assert "dropped-item" in SPEC_MANIFEST_LINE and "served models" in SPEC_MANIFEST_LINE
    assert [name for name, spec in agent_inputs.AGENTS.items()
            if MANIFEST_NAME in spec.sees] == []
    root, folder = plant(tmp_path)
    (folder / MANIFEST_NAME).write_text(
        json.dumps(MANIFEST | {"dropped_items": [
            {"report": "report_numbers.md", "item_id": f"{NOTES_ONE}",
             "reason": "the quote does not match"}],
            "served_models": {"numbers-reader": "claude-opus-4-20250514"}},
            indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with pytest.raises(ControlError) as caught:
        go(root, folder, "accounting_reliability", accounting_answer())
    assert MANIFEST_NAME in str(caught.value)
    assert not (root / "control_single_agent_accounting.json").exists()


def test_a_prior_predictions_file_still_carrying_a_probability_is_refused(tmp_path):
    """An allowed name whose contents are not allowed.

    `docs/INPUT_SPEC.md` §6 gives this file "prior flags and outcomes,
    probabilities removed" and `docs/HOW_WE_WORK.md` §8 forbids putting "a prior
    run's probability into any agent's input". `src/agent_inputs.py` refuses to
    place one that still carries one; the control's directory is not one that
    file builds, so the same reader is run here rather than the rule being
    assumed to have been applied upstream.
    """
    assert "probabilities removed" in INPUT_SPEC.read_text(encoding="utf-8")
    assert ("a prior run's probability into any agent's input"
            in HOW_WE_WORK.read_text(encoding="utf-8"))
    root, folder = plant(tmp_path)
    (folder / "input_prior_predictions.md").write_text(
        f"# AAPL prior predictions\n\n## {OTHER_ACCESSION} — prediction_accounting.json\n\n"
        f'[{OTHER_ACCESSION}:prior:prediction_accounting:1]\n'
        '{"finding": "flag", "p_up": 0.71, "confidence": 0.9}\n',
        encoding="utf-8")
    stub = Stub(accounting_answer())
    with pytest.raises(ControlError) as caught:
        control_single_agent.run("accounting_reliability", input_dir=folder,
                                 bundle_root=root, ask=stub)
    assert "probability" in str(caught.value)
    assert stub.prompts == []


def test_another_companys_prose_under_an_allowed_name_is_refused(tmp_path):
    """The hole a name-only allowlist leaves, and the one the record closes.

    `src/quote_gate.py` indexes every `[id]` line in the directory and scopes
    none of them by accession — it cannot, because
    `src/assemble_bundle.py`'s `prior_predictions` mints ids from a prior run's
    accession and those belong in the bundle. So another company's prose copied
    into a file wearing an allowed name would have made every id in it resolve:
    the explanation id, the evidence quote and `market_direction.basis` would
    all have landed in this company's control file with nothing dropped and
    nothing counted. The record is what separates the two — NVDA's accession is
    in NVDA's manifest and in no AAPL one.
    """
    root, folder = plant(tmp_path)
    (folder / "input_notes.md").write_text(
        f"# Notes\n\n[{OTHER_ACCESSION}:notes:1]\nAnother company's prose.\n",
        encoding="utf-8")
    answer = accounting_answer()
    answer["checklist"] = [
        {"key": "receivables_outrun_revenue", "finding": "flag", "confidence": 0.6,
         "evidence": evidence(f"{OTHER_ACCESSION}:notes:1",
                              "Another company's prose.")}]
    answer["explanations"] = [{"id": f"{OTHER_ACCESSION}:notes:1",
                               "support": "sufficient", "realization_p": 0.4}]
    answer["market_direction"] = {"p_up": 0.45,
                                  "basis": [f"{OTHER_ACCESSION}:notes:1"]}
    answer["top_signals"] = ["receivables_outrun_revenue"]
    stub = Stub(answer)
    with pytest.raises(ControlError) as caught:
        control_single_agent.run("accounting_reliability", input_dir=folder,
                                 bundle_root=root, ask=stub)
    assert OTHER_ACCESSION in str(caught.value)
    assert not (root / "control_single_agent_accounting.json").exists()


def test_the_accessions_the_record_allows_are_this_tickers_by_the_cutoff(tmp_path):
    """The set the check above is made of, against the fixture record.

    A prior quarter of this company is in it — that is what carries
    `input_prior_predictions.md`'s ids — and a later quarter is not, which is
    the cutoff rule read over the same record.
    """
    allowed = control_single_agent.recorded_accessions(
        TICKER, dt.date.fromisoformat(FILED))
    assert ACCESSION in allowed
    assert PRIOR_ACCESSION in allowed
    assert LATER_ACCESSION not in allowed
    assert OTHER_ACCESSION not in allowed


def test_the_allowlist_reads_the_name_and_a_symlink_carries_someone_elses_bytes(tmp_path):
    """An allowed name on a link into another run, refused before the call.

    The order is `src/agent_inputs.py`'s, and so is the reason: it tests the
    symlink "before the source is read, and before `exists()`", because both
    that and `read_bytes()` follow the link. `is_file()` follows one too, so an
    allowlist standing on it reads the name of a file whose bytes are another
    company's — the leak this guard exists to refuse, wearing a name it allows.
    """
    root, folder = plant(tmp_path)
    elsewhere = tmp_path / "NVDA-10-K"
    elsewhere.mkdir()
    theirs = elsewhere / "input_notes.md"
    theirs.write_text(
        f"# Notes\n\n[{OTHER_ACCESSION}:notes:1]\nAnother company's prose.\n",
        encoding="utf-8")
    (folder / "input_companyfacts.json").symlink_to(theirs)
    stub = Stub(accounting_answer())
    with pytest.raises(ControlError) as caught:
        control_single_agent.run("accounting_reliability", input_dir=folder,
                                 bundle_root=root, ask=stub)
    assert "input_companyfacts.json" in str(caught.value)
    assert stub.prompts == []
    assert not (root / "control_single_agent_accounting.json").exists()


def test_a_directory_under_an_allowed_name_is_refused(tmp_path):
    """`bundle_files` keeps what `is_file()` says yes to, and that drops a
    directory — so an allowlist built on it never sees one. Whatever is under
    it reaches the control's directory under no name the prompt lists."""
    root, folder = plant(tmp_path)
    nested = folder / "input_exhibits.md"
    nested.mkdir()
    (nested / "NVDA_notes.md").write_text("Another company's prose.\n",
                                          encoding="utf-8")
    with pytest.raises(ControlError) as caught:
        go(root, folder, "accounting_reliability", accounting_answer())
    assert "input_exhibits.md" in str(caught.value)


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


def test_a_cutoff_that_is_not_the_filing_date_on_record_is_refused(tmp_path):
    """`CLAUDE.md`: the cutoff is the filing date of the triggering report.

    Nothing in this module read the key at all, so a run carrying a cutoff of
    1999 — or of 2026, which is the direction that sweeps documents in — was
    answered, gated and written out. The date it is held against is EDGAR's
    record of the accession the manifest itself names, not the manifest's own
    second opinion about it.
    """
    root, folder = plant(tmp_path)
    (root / "input_manifest.json").write_text(
        json.dumps(MANIFEST | {"cutoff": "1999-01-01"}, indent=2, sort_keys=True)
        + "\n", encoding="utf-8")
    stub = Stub(accounting_answer())
    with pytest.raises(ControlError) as caught:
        control_single_agent.run("accounting_reliability", input_dir=folder,
                                 bundle_root=root, ask=stub)
    assert "1999-01-01" in str(caught.value) and FILED in str(caught.value)
    # Refused before the call: a run outside its own cutoff never reaches a model.
    assert stub.prompts == []
    assert not (root / "control_single_agent_accounting.json").exists()


def test_a_manifest_with_no_cutoff_at_all_is_refused(tmp_path):
    """An absent date is not an early date — `src/cutoff_guard.py` says so."""
    root, folder = plant(tmp_path)
    without = {key: value for key, value in MANIFEST.items() if key != "cutoff"}
    (root / "input_manifest.json").write_text(
        json.dumps(without, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with pytest.raises(ControlError) as caught:
        go(root, folder, "accounting_reliability", accounting_answer())
    assert "cutoff" in str(caught.value)


def test_a_manifest_naming_an_accession_nobody_recorded_is_refused(tmp_path):
    """Fail-closed: an unrecorded accession has no filing date to be held to."""
    root, folder = plant(tmp_path)
    (root / "input_manifest.json").write_text(
        json.dumps(MANIFEST | {"accession": "0000320193-25-000073"},
                   indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with pytest.raises(ControlError) as caught:
        go(root, folder, "accounting_reliability", accounting_answer())
    assert "0000320193-25-000073" in str(caught.value)


def plant_record(tmp_path: Path, rows: list[dict]) -> Path:
    """A fixture root holding one company's record, for the two branches the
    committed twelve cannot show: a manifest with no ticker, and an accession
    recorded twice under two filing dates."""
    ticker_dir = tmp_path / "record" / TICKER
    ticker_dir.mkdir(parents=True)
    (ticker_dir / "manifest.json").write_text(
        json.dumps({"ticker": TICKER, "as_of": FILED, "documents": rows},
                   indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return tmp_path / "record"


def test_the_cutoff_check_returns_the_date_the_record_carries(tmp_path):
    root = plant_record(tmp_path, [
        {"form": "10-K", "role": "primary_html", "accession": ACCESSION,
         "filing_date": FILED, "path": "10-K/primary.htm"}])
    assert control_single_agent.cutoff_on_record(
        MANIFEST, fixtures_root=root) == dt.date.fromisoformat(FILED)


def test_a_manifest_with_no_ticker_cannot_have_its_accession_looked_up(tmp_path):
    root = plant_record(tmp_path, [])
    without = {key: value for key, value in MANIFEST.items() if key != "ticker"}
    with pytest.raises(ControlError) as caught:
        control_single_agent.cutoff_on_record(without, fixtures_root=root)
    assert "names no ticker" in str(caught.value)


def test_one_accession_recorded_under_two_filing_dates_is_refused(tmp_path):
    """A cutoff cannot be held to two dates, so it is held to neither."""
    root = plant_record(tmp_path, [
        {"form": "10-K", "role": "primary_html", "accession": ACCESSION,
         "filing_date": FILED, "path": "10-K/primary.htm"},
        {"form": "10-K", "role": "exhibit_21", "accession": ACCESSION,
         "filing_date": "2025-11-04", "path": "10-K/exhibit21.htm"}])
    with pytest.raises(ControlError) as caught:
        control_single_agent.cutoff_on_record(MANIFEST, fixtures_root=root)
    assert "one accession is one filing" in str(caught.value)
    assert FILED in str(caught.value) and "2025-11-04" in str(caught.value)


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
