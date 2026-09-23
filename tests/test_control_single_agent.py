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

from src import agent_inputs, control_single_agent, prediction_schema, quote_gate
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


BUNDLE = {"input_notes.md": NOTES, "input_trends.json": TRENDS,
          "input_market.json": MARKET}


def plant(tmp_path: Path, root: Path | None = None) -> tuple[Path, Path]:
    """The run directory, and the directory the control is handed.

    The bundle is written into the run directory and *copied* into the
    control's, which is how `src/agent_inputs.py` places a layer's files and
    what the byte check below is measured against. A control directory that
    were not a copy of the run would be a directory nobody assembled.

    `root` is where the run directory sits, when a test needs it somewhere in
    particular; everything else plants it beside the control's directory.
    """
    root = tmp_path / "AAPL-10-K" if root is None else root
    folder = tmp_path / "single-agent"
    root.mkdir(parents=True)
    folder.mkdir()
    for name, text in BUNDLE.items():
        (root / name).write_text(text, encoding="utf-8")
        (folder / name).write_text(text, encoding="utf-8")
    (root / "input_manifest.json").write_text(
        json.dumps(MANIFEST, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return root, folder


def hand(folder: Path, root: Path, name: str, text: str) -> None:
    """One file the run assembled and the control was handed, both the same."""
    (root / name).write_text(text, encoding="utf-8")
    (folder / name).write_text(text, encoding="utf-8")


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
    # The fields the run settles, the fields the answer carries, and the one
    # the schema gives financial pressure alone: between them, every field.
    assert sorted(SCHEMA_FIELDS) == sorted(
        prediction_schema.RUN_KEYS + prediction_schema.PREDICTED_KEYS
        + (prediction_schema.CONTINUOUS,))


def test_the_evidence_members_are_the_schemas_own_plus_the_quote():
    """The one member this control adds to §7's, and nothing else.

    This side comes off the block above; the module's is
    `src/prediction_schema.py`'s own member with the quote beside it, and the
    shuffled control's tests hold that member against §7 by hand and parsed.
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
    assert len(payload["top_signals"]) <= prediction_schema.TOP_SIGNALS_MAX


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
#
# Every name the allowlist refuses is planted **in the run directory as well**,
# by `hand`, with the same bytes. That is what makes the allowlist the thing
# under test: the two checks after it -- the run has no file of that name, and
# the bytes are not the run's -- both raise naming the same file, so a test that
# planted the stray copy alone stayed green with the allowlist deleted and was
# reading another branch's message. Planted in both places there is nothing left
# to refuse it but the list, and `stub.prompts == []` says the model never saw
# the directory. `REFUSED_BY_THE_LIST` is that branch's own sentence, so a
# refusal arriving from anywhere else is not mistaken for this one.

REFUSED_BY_THE_LIST = "which this control may not see"


def refused(root: Path, folder: Path, answer: dict | None = None) -> str:
    """One run the directory has to stop, and the refusal it raised.

    The model is never called and no control file is written -- asserted here
    once rather than in every test below, because `run` settles the input
    before the call on purpose: "a refusal after the answer has come back is a
    refusal that has already paid for the look-ahead". That ordering is a claim
    this change makes and `stub.prompts == []` is the only thing that holds it:
    move `resolvable` below the call and every refusal below still raises, just
    after the model has read the directory. So a test carrying its own answer
    passes it here rather than raising on its own.
    """
    stub = Stub(accounting_answer() if answer is None else answer)
    with pytest.raises(ControlError) as caught:
        control_single_agent.run("accounting_reliability", input_dir=folder,
                                 bundle_root=root, ask=stub)
    assert stub.prompts == []
    assert not (root / "control_single_agent_accounting.json").exists()
    return str(caught.value)


def test_a_report_the_run_wrote_is_refused_even_though_the_run_wrote_it(tmp_path):
    """The pipeline's own output, in the run directory where it belongs.

    A reader report *is* in the run's directory -- that is where the read stage
    writes it -- so the control's copy of it is a true copy and the byte check
    has nothing to say. The control is a control beside the pipeline, not a
    reader of it, and the list is what says so.
    """
    root, folder = plant(tmp_path)
    hand(folder, root, "report_numbers.md", "# the numbers reader\n")
    message = refused(root, folder)
    assert "report_numbers.md" in message and REFUSED_BY_THE_LIST in message


def test_a_price_file_carrying_the_outcome_window_is_refused(tmp_path):
    """The `input_` prefix is not a passport.

    The guard used to refuse only the names it recognised as the pipeline's, so
    a file nobody routed went through and was listed to the model under "you
    see these files and nothing else". `src/agent_inputs.py` refuses anything
    outside what a layer may hold, for the reason its own message gives, and
    this is the same rule at the control's directory.
    """
    root, folder = plant(tmp_path)
    hand(folder, root, OUTCOME_WINDOW_PRICES,
         '{"ticker": "AAPL", "close": [190.1, 193.4], "window": "reaction_day_60"}\n')
    message = refused(root, folder)
    assert OUTCOME_WINDOW_PRICES in message and REFUSED_BY_THE_LIST in message


def test_another_companys_notes_in_the_control_directory_are_refused(tmp_path):
    root, folder = plant(tmp_path)
    hand(folder, root, OTHER_COMPANY_NOTES,
         f"# Notes\n\n[{OTHER_ACCESSION}:notes:1]\nAnother company's prose.\n")
    message = refused(root, folder)
    assert OTHER_COMPANY_NOTES in message and REFUSED_BY_THE_LIST in message


def test_the_files_the_control_may_hold_are_the_bundles_and_the_market_table(tmp_path):
    """The allowlist is §6's own list, read off §6 and not off the module.

    The first version of this test asserted the set against the comprehension
    the module builds it with, which is the module's answer restated: a prefix
    reading that swept in a file no layer sees would have moved this expected
    value along with it. §6's fenced list is the document, and it is what the
    control is measured against here.
    """
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
    root, folder = plant(tmp_path)
    assert control_single_agent.input_files(folder, root) == [
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
    # The run's own manifest, and the control handed a true copy of it: this is
    # the file the run keeps and `run` reads from `bundle_root`, so the copy is
    # byte for byte the run's and the list is the only thing that refuses it.
    hand(folder, root, MANIFEST_NAME,
         json.dumps(MANIFEST | {"dropped_items": [
             {"report": "report_numbers.md", "item_id": f"{NOTES_ONE}",
              "reason": "the quote does not match"}],
             "served_models": {"numbers-reader": "claude-opus-4-20250514"}},
             indent=2, sort_keys=True) + "\n")
    message = refused(root, folder)
    assert MANIFEST_NAME in message and REFUSED_BY_THE_LIST in message


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
    # In the run's own bundle as well as in the copy: the question is whether
    # the control reads what it was handed, not whether the copy was faithful.
    hand(folder, root, "input_prior_predictions.md",
         f"# AAPL prior predictions\n\n## {PRIOR_ACCESSION} — prediction_accounting.json\n\n"
         f'[{PRIOR_ACCESSION}:prior:prediction_accounting:1]\n'
         '{"finding": "flag", "p_up": 0.71, "confidence": 0.9}\n')
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
    # Assembled wrong, not copied wrong: the bytes match the run's own file,
    # so the byte check below has nothing to say and the record is the only
    # thing left that knows whose paragraphs these are.
    hand(folder, root, "input_notes.md",
         f"# Notes\n\n[{OTHER_ACCESSION}:notes:1]\nAnother company's prose.\n")
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
    assert OTHER_ACCESSION in refused(root, folder, answer)


def test_a_later_quarter_of_this_company_under_an_allowed_name_is_refused(tmp_path):
    """The other half of the record check, and the half no other test reaches.

    The test above plants another company's accession, which `recorded_accessions`
    refuses on the ticker alone -- so the cutoff it is handed could be any date
    and that test would still pass. This one plants the *next quarter of this
    company*: `tests/fixtures/AAPL/manifest.json` records it, and the only thing
    that keeps it out is the cutoff `run` passes down. Replace that argument with
    a date far in the future and this is the test that notices.

    It is `CLAUDE.md`'s cutoff rule read at the control's own directory --
    "document filing date <= filing date of the triggering report. Nothing later
    enters the input" -- and it is a different failure from the manifest's own
    cutoff being wrong: the manifest here is right, and the directory holds a
    paragraph the manifest does not cover.
    """
    root, folder = plant(tmp_path)
    # Appended rather than substituted: the run's own paragraphs stay indexed,
    # so what refuses the directory is the added id and nothing else about it.
    hand(folder, root, "input_notes.md",
         NOTES + f"\n[{LATER_ACCESSION}:notes:1]\nNext quarter's prose.\n")
    message = refused(root, folder)
    assert LATER_ACCESSION in message
    assert FILED in message


def test_a_manifest_naming_no_accession_is_refused_as_that_and_not_as_a_miss(tmp_path):
    """The guard `run` opens with, and the misreading that stands in for it.

    Delete it and the run still refuses -- `cutoff_on_record` looks the accession
    up, finds no row and raises -- but it raises "AAPL None is in no fixture
    manifest", which says EDGAR has no record of a filing when what happened is
    that the bundle named none. A manifest with no accession is a manifest, not
    a missing filing, and the two get fixed in different places. So this asserts
    the reason as well as the refusal.
    """
    root, folder = plant(tmp_path)
    without = {key: value for key, value in MANIFEST.items() if key != "accession"}
    (root / "input_manifest.json").write_text(
        json.dumps(without, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    message = refused(root, folder)
    assert "accession" in message
    assert "None" not in message


def test_a_foreign_trend_table_under_its_allowed_name_is_refused(tmp_path):
    """The case no id check can reach, and the reason the bytes are read.

    `src/quote_gate.py` mints a trend cell's id from the run's own accession
    rather than out of the file, so another company's table is indexed under
    *this* run's ids and its values string-match as verbatim quotes. `resolvable`
    sees nothing wrong — the ids are this run's — and the row would be kept,
    quoted and written. `src/agent_inputs.py` names the only check that reaches
    it: "a hardlink to another file resolves inside the root and answers to the
    right name."
    """
    root, folder = plant(tmp_path)
    theirs = TRENDS.replace('"value": 51.7', '"value": 88.2')
    assert theirs != TRENDS
    (folder / "input_trends.json").write_text(theirs, encoding="utf-8")
    # The id the model would quote is this run's, and the quote does match the
    # bytes in the directory — which is exactly why the name check passes it.
    assert TREND_CELL in quote_gate.quotable(folder, ACCESSION)
    assert '"value": 88.2' in (folder / "input_trends.json").read_text(
        encoding="utf-8")
    stub = Stub(accounting_answer())
    with pytest.raises(ControlError) as caught:
        control_single_agent.run("accounting_reliability", input_dir=folder,
                                 bundle_root=root, ask=stub)
    assert "input_trends.json" in str(caught.value)
    assert stub.prompts == []
    assert not (root / "control_single_agent_accounting.json").exists()


def test_a_market_table_that_is_not_the_runs_own_is_refused(tmp_path):
    """`input_market.json` declares no paragraph ids, so nothing else can tell.

    The outcome-window rows the earlier test plants wear a name the allowlist
    does not carry, which is the easy half. Under the allowed name the same
    rows pass every check that reads names, and the market table offers no id
    for `resolvable` to scope — so the run's own copy is the only thing that
    says whether this is the table `src/market.py` bounded at reaction day two.
    """
    root, folder = plant(tmp_path)
    assert quote_gate.quotable(folder, ACCESSION).keys() == {
        NOTES_ONE, NOTES_TWO, TREND_CELL}
    (folder / "input_market.json").write_text(
        '{\n  "ticker": "AAPL",\n  "rows": [\n'
        '    {"date": "2026-12-31", "window": "outcome_day_60", '
        '"abnormal_return": 0.061}\n  ]\n}\n', encoding="utf-8")
    with pytest.raises(ControlError) as caught:
        go(root, folder, "accounting_reliability", accounting_answer())
    assert "input_market.json" in str(caught.value)


def test_a_file_the_run_never_assembled_is_refused(tmp_path):
    """An allowed name the run has no copy of is a file nobody routed."""
    root, folder = plant(tmp_path)
    (folder / "input_mdna.md").write_text(
        f"# MD&A\n\n[{ACCESSION}:mdna:1]\nManagement's discussion.\n",
        encoding="utf-8")
    with pytest.raises(ControlError) as caught:
        go(root, folder, "accounting_reliability", accounting_answer())
    assert "input_mdna.md" in str(caught.value)


def test_the_prior_and_later_accessions_planted_here_are_the_records_own(tmp_path):
    """The second and third dates this file leans on, read the way the first is.

    `FILED` is read off the fixture record above with `json`; these two were
    asserted only through `recorded_accessions`, the function they judge, so
    the claim that they came off the record was not one this file made good.
    """
    recorded = json.loads((FIXTURES / TICKER / "manifest.json").read_text(
        encoding="utf-8"))
    filed = {row["accession"]: row["filing_date"] for row in recorded["documents"]}
    assert filed[PRIOR_ACCESSION] < FILED
    assert filed[LATER_ACCESSION] > FILED


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


def test_a_link_to_the_runs_own_file_is_refused_though_the_bytes_are_right(tmp_path):
    """The one case the symlink check is the only thing that reaches.

    A link into *another* run is refused whether this check exists or not: its
    target's bytes are not the run's, so the byte check two steps down says so,
    which is why the earlier form of this test stayed green with the symlink
    check deleted. The case left is the link that passes everything else — the
    run's own file, under its own name, same bytes. `is_file()` follows a link,
    so the allowlist sees a file; `read_bytes()` follows one too, so `_differs`
    sees the run's own bytes. What is refused is the link itself: the directory
    is committed as what the control saw, its ancestors are outside it, and a
    target that changes after the commit changes the record with it.

    The order is `src/agent_inputs.py`'s, and so is the reason: it tests the
    symlink "before the source is read, and before `exists()`", because both
    that and `read_bytes()` follow the link.
    """
    root, folder = plant(tmp_path)
    placed = folder / "input_notes.md"
    placed.unlink()
    placed.symlink_to(root / "input_notes.md")
    # Everything after this check passes: an allowed name, a file to `is_file()`,
    # and the run's own bytes.
    assert placed.is_file() and placed.read_text(encoding="utf-8") == NOTES
    assert not agent_inputs._differs(placed, root / "input_notes.md")
    message = refused(root, folder)
    assert "input_notes.md" in message
    assert "A control reads the directory it was handed" in message


def test_a_directory_under_an_allowed_name_is_refused(tmp_path):
    """`bundle_files` keeps what `is_file()` says yes to, and that drops a
    directory — so an allowlist built on it never sees one. Whatever is under
    it reaches the control's directory under no name the prompt lists.

    The name is one the run has a file of, because nothing else here judges
    this check: a directory named for a file the run never wrote is refused by
    the check below it, and `agent_inputs._differs` answers False the moment
    `placed.is_file()` is False — so with this check gone a directory reads as
    a faithful copy of the run's own file and is listed to the model as one.
    """
    root, folder = plant(tmp_path)
    nested = folder / "input_notes.md"
    nested.unlink()
    nested.mkdir()
    (nested / "NVDA_notes.md").write_text("Another company's prose.\n",
                                          encoding="utf-8")
    assert (root / "input_notes.md").is_file()
    assert not agent_inputs._differs(nested, root / "input_notes.md")
    message = refused(root, folder)
    assert "input_notes.md" in message and "which is a directory" in message


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


# --- where the control's file may land ---------------------------------------
#
# The expected value is read off two documents and one check that predates this
# control's rule. `docs/INPUT_SPEC.md` §6 lists the control files in the
# committed bundle under `runs/{ticker}/{accession}/` -- the run directory -- and
# says in the same breath that "each agent's input directory is committed as
# what it saw, and the directory is the isolation boundary";
# `docs/HOW_WE_WORK.md` §1.6 says it again. `src/agent_inputs.py` is that
# boundary as directories: `runs/{ticker}/{accession}/agents/{agent}/`. So a
# control file inside another run's `agents/` tree is written into what that
# tree records its agents as having seen, and the refusal is the expected
# result.

OTHER_RUN_TICKER = "NVDA"
OUTSIDE_THE_BOUNDARY = "per-agent input"


def another_run(tmp_path: Path, *, built: bool = True) -> Path:
    """A second company's run, with its numbers reader's input directory built.

    Built by `src/agent_inputs.py` itself rather than by `mkdir`, so the
    directory the control is pointed into is one the layer table made. The
    reader's files are placeholders: what is under test is where they sit.
    `built=False` is the same run before any agent's directory exists.
    """
    run = tmp_path / "runs" / OTHER_RUN_TICKER / OTHER_ACCESSION
    run.mkdir(parents=True)
    for name in agent_inputs.AGENTS["numbers-reader"].required():
        (run / name).write_text(f"# {OTHER_RUN_TICKER} {name}\n", encoding="utf-8")
    (run / MANIFEST_NAME).write_text(
        json.dumps({"ticker": OTHER_RUN_TICKER, "accession": OTHER_ACCESSION},
                   indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if built:
        agent_inputs.build(run, "numbers-reader")
    assert agent_inputs.isolation_violations(run) == []
    return run


@pytest.mark.parametrize("where", ["a reader's own directory",
                                   "the directory the six sit in",
                                   "a link into a reader's directory",
                                   "a reader's directory where the layout does not put it",
                                   "the directory the six sit in, before any is built"])
def test_a_run_directory_inside_another_runs_input_tree_is_refused(tmp_path, where):
    """This control writes into the run directory it is handed, so that is its output.

    Planted five ways: under the numbers reader's session root; under the
    `agents/` directory that holds the six and nothing else; at an ordinary
    path that is a link into the first, because a link's ancestors are wherever
    it points and the file follows the link; under a reader's directory sitting
    somewhere the layout does not put it, which `agent_directories` finds by its
    name "wherever it sits"; and under a run's `agents/` before any agent's
    directory is in it, which the layout says holds nothing but the six, ever.
    """
    other = another_run(tmp_path, built=not where.endswith("before any is built"))
    held = agent_inputs.session_root(other, "numbers-reader")
    if where.startswith("the directory the six sit in"):
        held = agent_inputs.agents_root(other)
    elif where == "a reader's directory where the layout does not put it":
        held = other / "readers" / "numbers-reader"
    planted, folder = plant(tmp_path, held / "AAPL-10-K")
    root = planted
    if where == "a link into a reader's directory":
        root = tmp_path / "AAPL-10-K"
        root.symlink_to(planted, target_is_directory=True)
    message = refused(root, folder)
    assert OUTSIDE_THE_BOUNDARY in message
    assert str(held.resolve()) in message
    assert sorted(other.rglob("control_single_agent_*")) == []


def test_a_run_directory_that_holds_its_own_input_tree_still_takes_its_file(tmp_path):
    """The positive side: the run directory is where §6 puts the control file.

    A run directory holds the bundle *and* its `agents/` directory, so the rule
    cannot be "no agent directory nearby" -- that would refuse every run the
    stage runner finishes. The file lands beside the bundle, and the boundary
    check `src/agent_inputs.py` already runs finds nothing wrong with the tree.
    """
    root, folder = plant(tmp_path)
    agent_inputs.session_root(root, "numbers-reader").mkdir(parents=True)
    go(root, folder, "accounting_reliability", accounting_answer())
    assert (root / "control_single_agent_accounting.json").is_file()
    assert agent_inputs.isolation_violations(root) == []


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


def test_a_cutoff_earlier_than_the_filing_date_on_record_is_refused(tmp_path):
    """`CLAUDE.md`: the cutoff is the filing date of the triggering report.

    Nothing in this module read the key at all, so a run carrying a cutoff of
    1999 was answered, gated and written out. The date it is held against is
    EDGAR's record of the accession the manifest itself names, not the
    manifest's own second opinion about it.
    """
    root, folder = plant(tmp_path)
    (root / "input_manifest.json").write_text(
        json.dumps(MANIFEST | {"cutoff": "1999-01-01"}, indent=2, sort_keys=True)
        + "\n", encoding="utf-8")
    # `refused` is what says the model was never called: a run outside its own
    # cutoff is stopped before the look-ahead has been paid for.
    message = refused(root, folder)
    assert "1999-01-01" in message and FILED in message


def test_a_cutoff_later_than_the_filing_date_on_record_is_refused(tmp_path):
    """The other direction, and the only one that lets a document in.

    The test above plants 1999, and a check written as "the cutoff may not be
    *before* the filing date" passes it — while the run that moved its boundary
    forward is the one `CLAUDE.md` is about: "document filing date ≤ filing date
    of the triggering report. Nothing later enters the input." The date planted
    here is the one EDGAR's record gives the next quarter's 10-Q, read out of
    `tests/fixtures/AAPL/manifest.json` with `json` alone — so this is not a
    date chosen to fail but the exact boundary that would sweep that filing in,
    and `recorded_accessions` above shows the same record admitting it once the
    cutoff reaches it.
    """
    recorded = json.loads((FIXTURES / TICKER / "manifest.json").read_text(
        encoding="utf-8"))
    later = {row["filing_date"] for row in recorded["documents"]
             if row["accession"] == LATER_ACCESSION}
    assert len(later) == 1
    moved = later.pop()
    assert moved > FILED
    assert LATER_ACCESSION in control_single_agent.recorded_accessions(
        TICKER, dt.date.fromisoformat(moved))

    root, folder = plant(tmp_path)
    (root / "input_manifest.json").write_text(
        json.dumps(MANIFEST | {"cutoff": moved}, indent=2, sort_keys=True)
        + "\n", encoding="utf-8")
    message = refused(root, folder)
    assert moved in message and FILED in message


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


def test_a_prediction_carrying_no_rules_version_is_refused_when_the_run_has_none(tmp_path):
    """§7 gives every prediction a `rules_version`, and a run whose manifest
    carries `null` does not make the field optional.

    The field is the run's, so it is checked here and not handed to the one
    checker. Read with `.get`, an answer with no such field would have been
    taken as carrying the run's null and written standing.
    """
    root, folder = plant(tmp_path)
    (root / "input_manifest.json").write_text(
        json.dumps(MANIFEST | {"rules_version": None}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    answer = accounting_answer()
    del answer["rules_version"]
    with pytest.raises(ControlError) as caught:
        go(root, folder, "accounting_reliability", answer)
    assert "carries no rules_version" in str(caught.value)
    assert not (root / "control_single_agent_accounting.json").exists()


def test_the_control_answers_through_the_one_checker(tmp_path, monkeypatch):
    """Called, not copied: the production path reaches the one §7 checker the
    shuffled control also calls, with this control's evidence shape -- §7's
    `upstream_item_id` and the quote beside it -- and with every field but the
    two the run settles.

    A copy of the check kept here beside a call nobody makes would pass every
    schema test in this file and this one would still fail.
    """
    calls = []
    real = prediction_schema.check

    def recording(answer, question, *, evidence):
        calls.append((question, evidence, sorted(answer)))
        return real(answer, question, evidence=evidence)

    monkeypatch.setattr(prediction_schema, "check", recording)
    root, folder = plant(tmp_path)
    go(root, folder, "financial_pressure", pressure_answer())
    assert calls == [("financial_pressure", EVIDENCE_MEMBERS,
                      sorted(set(SCHEMA_FIELDS) - {"question", "rules_version"}))]

    def refusing(answer, question, *, evidence):
        raise prediction_schema.SchemaError("the one checker refused this")

    monkeypatch.setattr(prediction_schema, "check", refusing)
    with pytest.raises(ControlError, match="the one checker refused this"):
        go(root, folder, "accounting_reliability", accounting_answer())
    assert not (root / "control_single_agent_accounting.json").exists()


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
    root, folder = plant(tmp_path)
    code = control_single_agent.main(
        ["--question", "financial_pressure", "--input", str(folder),
         "--bundle", str(root)])
    printed = capsys.readouterr().out
    assert code == 0
    assert f"model: {SUPERVISOR_MODEL}" in printed
    assert "writes: control_single_agent_pressure.json" in printed
    assert SCHEMA_BLOCK in printed


def test_the_command_line_refuses_a_directory_it_cannot_read(tmp_path, capsys):
    root, _ = plant(tmp_path)
    code = control_single_agent.main(
        ["--question", "financial_pressure", "--input", str(tmp_path / "nowhere"),
         "--bundle", str(root)])
    assert code == control_single_agent.BAD_INPUT
    assert "not a control" in capsys.readouterr().err
