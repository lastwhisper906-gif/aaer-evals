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

import hashlib
import json
import os
import re
import shutil
from pathlib import Path

import pytest

from src import (agent_inputs, assemble_bundle, control_single_agent,
                 cutoff_guard, quote_gate)
from src.control_single_agent import ControlError
from src.fetch_fixtures import TICKERS

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

# The five files `plant` did not write, each a shape the assembler produces:
# two of them carry the undated prose that the first version of the paragraph
# rule refused all twenty-four bundles for, and they are written here so the
# fixture holds it too.
NOTES_HISTORY = "# Note change history\n\nNo note change history on record.\n"
MDNA = f"""# Management's discussion and analysis

[{ACCESSION}:mdna:1]
Gross margin was 46.5% of net sales, against 46.3% a year ago.
"""
CONTROLS = f"""# Controls and procedures

[{ACCESSION}:controls:1]
Disclosure controls and procedures were effective as of the end of the period.
"""
EIGHT_K = "# Current reports\n\nNo 8-K filed at or before this cutoff is on record.\n"
PRIOR_PREDICTIONS = "# Prior predictions\n\nNone on record.\n"

NUMBERS = json.dumps({
    "ticker": "AAPL",
    "cutoff": "2025-08-01",
    "documents": [{"accession": ACCESSION, "filing_date": "2025-08-01",
                   "form": "10-Q", "path": "10-Q/aapl_htm.xml",
                   "role": "xbrl_instance"}],
    "facts": [
        {"id": f"{ACCESSION}:f-1", "source_accession": ACCESSION,
         "filing_date": "2025-08-01", "form": "10-Q", "tag": "AccountsReceivableNetCurrent",
         "prefix": "us-gaap", "namespace": "http://fasb.org/us-gaap/2025",
         "unit": "iso4217:USD", "decimals": "-6", "nil": False,
         "value": "29508000000", "number": 29508000000.0,
         "context_ref": "c-1", "context": {"instant": "2025-06-28", "segment": []}},
        {"id": f"{ACCESSION}:f-2", "source_accession": ACCESSION,
         "filing_date": "2025-08-01", "form": "10-Q", "tag": "AllowanceForDoubtfulAccountsReceivableCurrent",
         "prefix": "us-gaap", "namespace": "http://fasb.org/us-gaap/2025",
         "unit": "iso4217:USD", "decimals": "-6", "nil": False,
         "value": "550000000", "number": 550000000.0,
         "context_ref": "c-1", "context": {"instant": "2025-06-28", "segment": []}},
    ],
}, indent=2, sort_keys=True) + "\n"

# `input_trends.json` as `src/trends.py` commits it: two-space indent, sorted
# keys, one key to a line. The `cutoff` is the file's own account of the
# boundary it was built at, and it is the manifest's — a real trend table
# carries it, and this fixture did not, so nothing here could have noticed that
# the two can disagree.
TRENDS = """{
  "cutoff": "2025-08-01",
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

# `filing_date` is the triggering report's own, and `src/assemble_bundle.py`
# writes it into every bundle beside `cutoff`. The two are one date --
# `src/extraction_checks.py`: "the cutoff is the triggering report's own filing
# date" -- and a planted manifest naming one without the other would be planting
# a run this repository does not assemble.
#
# Every date and form below is read off the committed record,
# `tests/fixtures/AAPL/submissions.json`, and `test_the_planted_manifest_is_the
# _record` reads them back out of that file rather than trusting this block:
# accession 0000320193-25-000073 is a 10-Q filed 2025-08-01, and the quarter
# before it is 0000320193-25-000057, filed 2025-05-02. The manifest used to pair
# this accession with 2025-10-31, which is the *10-K's* filing date -- a run
# whose own record put its triggering report three months after the document it
# names, and which every check here passed because none of them read a document.
PRIOR_ACCESSION = "0000320193-25-000057"
MANIFEST = {"ticker": "AAPL", "accession": ACCESSION, "form": "10-Q",
            "cutoff": "2025-08-01", "filing_date": "2025-08-01",
            "documents": [
                {"form": "10-Q", "role": "primary_html", "accession": ACCESSION,
                 "filing_date": "2025-08-01"},
                {"form": "10-Q", "role": "xbrl_instance", "accession": ACCESSION,
                 "filing_date": "2025-08-01"},
                {"form": "10-Q", "role": "prior_period",
                 "accession": PRIOR_ACCESSION, "filing_date": "2025-05-02"},
            ],
            "rules_version": "0.1", "counts": {"paragraphs": 2, "exclusions": 0}}

# Another company's accession, and a paragraph number the planted notes stop
# short of: `plant` writes two, numbered 1 and 2. Nothing in the committed input
# declares this id, which the gate's own index is asserted to agree about below.
OTHER_ACCESSION = "0000789019-25-000104"
STRAY_EXPLANATION = f"{OTHER_ACCESSION}:notes:7"

# Two files no layer routes, which is why neither name is in the catalogue: a
# price file carrying the sixty-day window the run is scored on, and another
# company's notes.
OUTCOME_PRICES = """{
  "ticker": "AAPL",
  "abnormal_return_60d": 0.184,
  "reaction_day": "2025-10-31"
}
"""
OTHER_NOTES = f"""# Notes

[{OTHER_ACCESSION}:notes:1]
Deferred revenue rose during the period.
"""

# `docs/INPUT_SPEC.md` §6's file list, the `input_` half of it, copied out by
# hand -- plus `input_controls.md`, the one input name §6's list does not carry
# and `src/agent_inputs.py` adds to the catalogue in those words.
# `docs/CHECKLIST.md` §8: "handed the whole bundle plus the market table".
# `input_manifest.json` is not here: it is the run's bookkeeping, the control
# reads it from the run directory, and it carries the text of the paragraphs
# the pipeline kept out of a reader's input.
CONTROL_MAY_SEE = (
    "input_numbers.json", "input_companyfacts.json", "input_trends.json",
    "input_notes.md", "input_notes_history.md", "input_mdna.md",
    "input_exhibits.md", "input_risk_factors.md", "input_8k.md",
    "input_prior_predictions.md", "input_market.json", "input_controls.md")

NOTES_ONE = f"{ACCESSION}:notes:1"
NOTES_TWO = f"{ACCESSION}:notes:2"
TREND_CELL = f"{ACCESSION}:trends:days_sales_outstanding:Q-0"

RECEIVABLES_QUOTE = "Accounts receivable, net of allowances, rose to $29,508 million"
ALLOWANCE_QUOTE = "The allowance for credit losses was reduced"
TREND_QUOTE = '"days": 91,\n          "value": 51.7'
# The same sentence with the filing's em dash written as a hyphen.
ALTERED_QUOTE = "rose to $29,508 million - the"


def plant(tmp_path: Path) -> tuple[Path, Path]:
    """The run directory, and the directory the control is handed.

    The bundle is written into the run and copied into the control's directory,
    which is the shape `src/agent_inputs.py` builds -- the run holds every
    `input_` file `docs/INPUT_SPEC.md` §6 names, and an agent's directory holds
    the copies it was routed. Planting them only in the agent's directory made a
    run in which nothing the control read had a copy to be checked against.
    """
    root = tmp_path / "AAPL-10-K"
    folder = tmp_path / "single-agent"
    root.mkdir()
    folder.mkdir()
    planted = (("input_notes.md", NOTES), ("input_trends.json", TRENDS),
               ("input_numbers.json", NUMBERS), ("input_market.json", MARKET),
               ("input_notes_history.md", NOTES_HISTORY), ("input_mdna.md", MDNA),
               ("input_controls.md", CONTROLS), ("input_8k.md", EIGHT_K),
               ("input_prior_predictions.md", PRIOR_PREDICTIONS))
    for name, text in planted:
        (root / name).write_text(text, encoding="utf-8")
        (folder / name).write_text(text, encoding="utf-8")
    # `docs/INPUT_SPEC.md` §6's manifest accounts for what the build wrote: a
    # hash and a byte count per file, and one row per `[id]` block with the file
    # it landed in. Both are computed here, by this test, from the planted text
    # -- `hashlib` and a bracket scan, nothing imported from `src/`. They used
    # to be absent, and the control read the text with nothing saying it was the
    # text the build wrote.
    manifest = dict(
        MANIFEST,
        files={name: {"sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                      "bytes": len(text.encode("utf-8"))}
               for name, text in planted},
        paragraphs=[{"id": line.strip()[1:-1], "file": name, "kind": "planted"}
                    for name, text in planted if name.endswith(".md")
                    for line in text.split("\n")
                    if line.strip().startswith("[") and line.strip().endswith("]")])
    (root / "input_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return root, folder


def replant(root: Path, folder: Path, name: str, text: str) -> None:
    """Rewrite one planted file in both copies **and** in the manifest.

    The manifest's `files` hash and `paragraphs` rows are what say the handed
    text is the text the build wrote, so a tamper that leaves them alone is
    refused by that check and never reaches the rule under test. Every test
    below whose subject is a later date, an unrecorded filing or a period past
    the cutoff uses this, so the refusal it asserts is its own rule's.
    """
    for where in (root, folder):
        (where / name).write_text(text, encoding="utf-8")
    path = root / "input_manifest.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    manifest["files"][name] = {
        "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "bytes": len(text.encode("utf-8"))}
    if name.endswith(".md"):
        manifest["paragraphs"] = [row for row in manifest["paragraphs"]
                                  if row["file"] != name] + [
            {"id": line.strip()[1:-1], "file": name, "kind": "planted"}
            for line in text.split("\n")
            if line.strip().startswith("[") and line.strip().endswith("]")]
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8")


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


def explaining_answer() -> dict:
    """The accounting answer with three explanations: two that resolve, one that
    resolves to nothing at all."""
    answer = accounting_answer()
    answer["explanations"] = [
        {"id": NOTES_TWO, "support": "insufficient", "realization_p": 0.3},
        {"id": TREND_CELL, "support": "sufficient", "realization_p": 0.6},
        {"id": STRAY_EXPLANATION, "support": "sufficient", "realization_p": 0.9},
    ]
    return answer


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


def test_a_directory_holding_part_of_the_bundle_is_refused(tmp_path):
    """§8 hands this control the whole bundle plus the market table.

    An allowlist says what may be handed and this said nothing about what must
    be: handed one price file and nothing else, every check passed, the model
    was called, and a tier was written for the accounting question off a table
    holding no filing at all. A baseline scored on a fragment is a baseline the
    layers beat for free, which is the one thing the scorecard exists to rule on.
    """
    root, folder = plant(tmp_path)
    for name in ("input_notes.md", "input_mdna.md"):
        (folder / name).unlink()
    stub = Stub(accounting_answer())
    with pytest.raises(ControlError) as caught:
        control_single_agent.run("accounting_reliability", input_dir=folder,
                                 bundle_root=root, ask=stub)
    assert "input_mdna.md, input_notes.md" in str(caught.value)   # sorted
    assert "a baseline the layers beat for free" in str(caught.value)
    assert stub.prompts == []


def test_the_three_names_no_builder_writes_yet_are_not_required(tmp_path):
    """Absent and recorded, the way `src/agent_inputs.py` treats them."""
    for name in agent_inputs.NOT_BUILT_YET:
        assert name in control_single_agent.CONTROL_SEES
        assert name not in control_single_agent.CONTROL_NEEDS
    root, folder = plant(tmp_path)
    go(root, folder, "accounting_reliability", accounting_answer())
    assert written(root, "accounting_reliability")["tier"]


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
    _replant_manifest(root, _planted_manifest(root) | {"rules_version": None})
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


# --- every explanation id resolves, or the entry goes ------------------------

def test_the_stray_explanation_id_is_in_none_of_the_committed_input(tmp_path):
    """The planted value, said by the gate's index rather than by this file."""
    _, folder = plant(tmp_path)
    index = quote_gate.quotable(folder, ACCESSION)
    assert STRAY_EXPLANATION not in index
    assert OTHER_ACCESSION not in "".join(index)
    # The two beside it are, so a gate that resolved nothing would not pass here.
    assert NOTES_TWO in index
    assert TREND_CELL in index


def test_an_explanation_id_that_resolves_to_nothing_is_dropped_and_counted(tmp_path):
    """`docs/HOW_WE_WORK.md` finishes the controls at "both control files, with
    every citation resolving"; an `explanations` id is a citation."""
    root, folder = plant(tmp_path)
    result = go(root, folder, "accounting_reliability", explaining_answer())
    written_ids = [entry["id"] for entry in
                   written(root, "accounting_reliability")["explanations"]]
    # By name, so a gate that dropped all three fails here too.
    assert written_ids == [NOTES_TWO, TREND_CELL]
    dropped = {row["item_id"]: row["reason"] for row in result["dropped"]}
    assert f"accounting_reliability:explanations:{STRAY_EXPLANATION}" in dropped
    assert "does not resolve" in dropped[
        f"accounting_reliability:explanations:{STRAY_EXPLANATION}"]
    assert all(row["report"] == "control_single_agent_accounting.json"
               for row in result["dropped"])


def test_an_explanation_whose_id_resolves_is_written_as_it_stands(tmp_path):
    root, folder = plant(tmp_path)
    go(root, folder, "accounting_reliability", accounting_answer())
    assert written(root, "accounting_reliability")["explanations"] == [
        {"id": NOTES_TWO, "support": "insufficient", "realization_p": 0.3}]


# --- the input guard is an allowlist -----------------------------------------

def test_the_allowlist_is_the_input_half_of_the_committed_bundle():
    spec = INPUT_SPEC.read_text(encoding="utf-8")
    for name in CONTROL_MAY_SEE:
        assert name.startswith("input_")
        assert name in agent_inputs.BUNDLE_CATALOGUE
        # `input_controls.md` is the one §6's list does not name.
        assert name in spec or name == "input_controls.md"
    assert sorted(CONTROL_MAY_SEE) == sorted(control_single_agent.CONTROL_SEES)
    for name in ("report_numbers.md", "prediction_accounting.json",
                 "explanations.json", "baselines.json",
                 "control_single_agent_accounting.json",
                 # The run's own bookkeeping, refused by name like any report.
                 "input_manifest.json"):
        assert name in agent_inputs.BUNDLE_CATALOGUE
        assert name not in control_single_agent.CONTROL_SEES


def test_a_file_no_layer_routes_is_refused_and_named(tmp_path):
    """The price file carries the window the run is scored on and the notes are
    another company's, and neither is a name the pipeline would have written."""
    root, folder = plant(tmp_path)
    for name in ("prices_after_the_filing.json", "MSFT_notes.md"):
        assert name not in agent_inputs.BUNDLE_CATALOGUE
    (folder / "prices_after_the_filing.json").write_text(OUTCOME_PRICES,
                                                         encoding="utf-8")
    (folder / "MSFT_notes.md").write_text(OTHER_NOTES, encoding="utf-8")
    stub = Stub(accounting_answer())
    with pytest.raises(ControlError) as caught:
        control_single_agent.run("accounting_reliability", input_dir=folder,
                                 bundle_root=root, ask=stub)
    assert "MSFT_notes.md" in str(caught.value)
    assert "prices_after_the_filing.json" in str(caught.value)
    assert stub.prompts == []
    assert not (root / "control_single_agent_accounting.json").exists()


def test_the_prompt_lists_the_files_and_the_directory_holds_nothing_else(tmp_path):
    root, folder = plant(tmp_path)
    stub = Stub(accounting_answer())
    control_single_agent.run("accounting_reliability", input_dir=folder,
                             bundle_root=root, ask=stub)
    listed = [line[2:] for line in stub.prompts[0].split("\n")
              if line.startswith("- input_")]
    assert listed == sorted(path.name for path in folder.iterdir())
    assert all(name in control_single_agent.CONTROL_SEES for name in listed)


# --- the guard is an allowlist over what the directory holds ------------------

def test_a_symlink_under_an_allowed_name_is_refused(tmp_path):
    """A link answers `is_file()` and reads as whatever it points at.

    Planted as the refute lens planted it: another company's notes, outside the
    directory, wearing a name the control may hold. Before the guard walked the
    entries, `quotable` followed the link, indexed that company's paragraph ids,
    and an explanation citing one of them was written out as resolved.
    """
    root, folder = plant(tmp_path)
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    other = elsewhere / "MSFT_notes.md"
    other.write_text(OTHER_NOTES, encoding="utf-8")
    link = folder / "input_notes.md"
    link.unlink()
    link.symlink_to(other)
    stub = Stub(accounting_answer())
    with pytest.raises(ControlError) as caught:
        control_single_agent.run("accounting_reliability", input_dir=folder,
                                 bundle_root=root, ask=stub)
    assert "input_notes.md" in str(caught.value)
    assert str(other) in str(caught.value)
    assert stub.prompts == []
    assert not (root / "control_single_agent_accounting.json").exists()


def test_a_directory_holding_the_outcome_window_is_refused(tmp_path):
    """A name the allowlist does not carry is refused whatever kind of thing it is.

    `cutoff_guard.bundle_files` keeps what `is_file()` says is a file, so a
    subdirectory was neither listed to the model nor refused: the outcome window
    sat in the directory under "you see these files and nothing else".
    """
    root, folder = plant(tmp_path)
    outcome = folder / "outcome"
    outcome.mkdir()
    (outcome / "prices_after_the_filing.json").write_text(OUTCOME_PRICES,
                                                          encoding="utf-8")
    stub = Stub(accounting_answer())
    with pytest.raises(ControlError) as caught:
        control_single_agent.run("accounting_reliability", input_dir=folder,
                                 bundle_root=root, ask=stub)
    assert "outcome" in str(caught.value)
    assert stub.prompts == []
    assert not (root / "control_single_agent_accounting.json").exists()


def test_the_boundary_call_cannot_be_reached_and_reports_the_escape_anyway(
        tmp_path):
    """`agent_inputs.escapes` is asked, and two earlier rules always answer.

    Switching the call off turned nothing red, and this says why rather than
    deleting it. Everything that escapes the handed directory is refused before
    the call: a link under a name no layer routes goes by name, a link under an
    allowed name goes by the symlink rule, and an allowed name that is a
    directory goes by the kind rule. So what is asserted here is what can be —
    that the helper does report the escape, and that `input_files` refuses such
    a directory whichever rule speaks. The third reading's deletion of a rule
    reasoned unreachable is why this one stays.
    """
    root, folder = plant(tmp_path)
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "input_notes.md").write_text(OTHER_NOTES, encoding="utf-8")
    (folder / "reaches_out").symlink_to(outside)
    assert agent_inputs.escapes(folder)          # the helper's own report
    with pytest.raises(ControlError) as caught:  # and the directory is refused
        control_single_agent.input_files(folder)
    assert "reaches_out" in str(caught.value)

    # under an allowed name, the symlink rule is the one that answers
    (folder / "reaches_out").unlink()
    (folder / "input_notes.md").unlink()
    (folder / "input_notes.md").symlink_to(outside / "input_notes.md")
    assert agent_inputs.escapes(folder)
    with pytest.raises(ControlError, match="is a symlink to"):
        control_single_agent.input_files(folder)


def test_an_allowed_name_that_is_not_a_file_is_refused(tmp_path):
    """The prompt calls every listed name a file, so it has to be one."""
    root, folder = plant(tmp_path)
    (folder / "input_notes.md").unlink()
    (folder / "input_notes.md").mkdir()
    stub = Stub(accounting_answer())
    with pytest.raises(ControlError) as caught:
        control_single_agent.run("accounting_reliability", input_dir=folder,
                                 bundle_root=root, ask=stub)
    # This rule's own sentence. The file name alone was also satisfied by the
    # handed-hardlink rule below, which counts links and finds two or more on
    # any directory -- so switching this rule off left the run refused and the
    # reason wrong, reported as "one name of 2 for the same bytes" about a
    # directory, with nothing in the suite red.
    assert "carries a name this control may hold and is not a file" in str(caught.value)
    assert stub.prompts == []


def test_a_plain_copy_of_another_companys_notes_is_refused(tmp_path):
    """No link anywhere: the right name written over other bytes.

    The second lens wrote MSFT's notes into `input_notes.md` directly. Every
    name check, kind check and boundary check passed it, the model was handed
    it under "you see these files and nothing else", and the explanation citing
    MSFT's paragraph was written out as resolved.
    """
    root, folder = plant(tmp_path)
    (folder / "input_notes.md").write_text(OTHER_NOTES, encoding="utf-8")
    stub = Stub(accounting_answer())
    with pytest.raises(ControlError) as caught:
        control_single_agent.run("accounting_reliability", input_dir=folder,
                                 bundle_root=root, ask=stub)
    # The byte-compare's own sentence, not the file name. Asserting the name
    # alone let the manifest's sha256 refusal stand in for this rule, and
    # switching the byte-compare off turned nothing in the suite red.
    assert "is not the run's own input_notes.md" in str(caught.value)
    assert stub.prompts == []
    assert not (root / "control_single_agent_accounting.json").exists()


def test_a_hardlink_under_an_allowed_name_is_refused(tmp_path):
    """A hardlink resolves inside the directory and answers to the name."""
    root, folder = plant(tmp_path)
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    other = elsewhere / "MSFT_notes.md"
    other.write_text(OTHER_NOTES, encoding="utf-8")
    handed = folder / "input_notes.md"
    handed.unlink()
    handed.hardlink_to(other)
    assert not handed.is_symlink()
    stub = Stub(accounting_answer())
    with pytest.raises(ControlError) as caught:
        control_single_agent.run("accounting_reliability", input_dir=folder,
                                 bundle_root=root, ask=stub)
    assert "one name of 2" in str(caught.value)
    assert stub.prompts == []


def test_an_input_directory_that_is_itself_a_link_is_refused(tmp_path):
    """`agent_inputs.escapes` resolves the root with everything under it, so a
    linked directory is judged against its own target and nothing escapes."""
    root, folder = plant(tmp_path)
    elsewhere = tmp_path / "another-run"
    elsewhere.mkdir()
    for name in control_single_agent.CONTROL_NEEDS:
        (elsewhere / name).write_text(
            OTHER_NOTES if name == "input_notes.md"
            else (folder / name).read_text(encoding="utf-8"), encoding="utf-8")
    link = tmp_path / "handed-to-the-control"
    link.symlink_to(elsewhere, target_is_directory=True)
    assert control_single_agent.agent_inputs.escapes(link) == []
    stub = Stub(accounting_answer())
    with pytest.raises(ControlError) as caught:
        control_single_agent.run("accounting_reliability", input_dir=link,
                                 bundle_root=root, ask=stub)
    assert str(elsewhere) in str(caught.value)
    assert stub.prompts == []


def test_a_file_the_run_does_not_hold_is_refused(tmp_path):
    """An allowed name, real bytes, and no copy in the run to be checked against."""
    root, folder = plant(tmp_path)
    name = "input_risk_factors.md"
    (folder / name).write_text(NOTES, encoding="utf-8")
    assert name in control_single_agent.CONTROL_SEES
    # and not in `CONTROL_NEEDS`, so the missing-name rule has nothing to say:
    # it is a name the control may hold and this run did not assemble.
    assert name not in control_single_agent.CONTROL_NEEDS
    assert not (root / name).exists()
    stub = Stub(accounting_answer())
    with pytest.raises(ControlError) as caught:
        control_single_agent.run("accounting_reliability", input_dir=folder,
                                 bundle_root=root, ask=stub)
    assert f"{name} is in the directory handed to the control" in str(caught.value)
    assert stub.prompts == []


def test_a_file_rewritten_during_the_call_is_refused_before_it_is_quoted(tmp_path):
    """A directory checked before the call and read after it is two directories.

    `verify` rebuilds the quote index from the handed directory as it stands
    when the answer comes back, and in this repository's own model of a call the
    writer can be the model: every layer runs as a session with `Write` rooted
    at its own directory. An `ask` that rewrites `input_notes.md` while it
    answers had the other company's paragraph ids resolving, with no drop row --
    the same leak as a planted copy, one step later.
    """
    root, folder = plant(tmp_path)

    class Rewrites(Stub):
        def __call__(self, prompt: str, *, model: str) -> dict:
            (folder / "input_notes.md").write_text(OTHER_NOTES, encoding="utf-8")
            return super().__call__(prompt, model=model)

    stub = Rewrites(accounting_answer())
    with pytest.raises(ControlError) as caught:
        control_single_agent.run("accounting_reliability", input_dir=folder,
                                 bundle_root=root, ask=stub)
    assert "is not the run's own input_notes.md" in str(caught.value)
    assert stub.prompts != []          # the call did happen
    assert not (root / "control_single_agent_accounting.json").exists()


def test_a_linked_copy_in_the_run_is_refused_as_the_thing_to_check_against(tmp_path):
    """`is_file()` and `read_bytes()` both follow a link, so a linked run copy
    would make the comparison agree with whatever it points at."""
    root, folder = plant(tmp_path)
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    other = elsewhere / "MSFT_notes.md"
    other.write_text(OTHER_NOTES, encoding="utf-8")
    (root / "input_notes.md").unlink()
    (root / "input_notes.md").symlink_to(other)
    (folder / "input_notes.md").write_text(OTHER_NOTES, encoding="utf-8")
    stub = Stub(accounting_answer())
    with pytest.raises(ControlError) as caught:
        control_single_agent.run("accounting_reliability", input_dir=folder,
                                 bundle_root=root, ask=stub)
    assert str(other) in str(caught.value)
    assert stub.prompts == []


def test_the_evidence_fields_are_the_checklist_documents_own(tmp_path):
    """Read out of `docs/CHECKLIST.md` §7 by this test, not out of the module.

    The module parses the same object out of the schema it shows the model, and
    the suite asserts that schema is a slice of the document. Both sides used to
    be hand-written lists that agreed with each other and would have gone on
    agreeing if §7 moved.
    """
    document = CHECKLIST.read_text(encoding="utf-8")
    assert SCHEMA_BLOCK in document
    evidence = SCHEMA_BLOCK.split('"evidence": [', 1)[1].split("]", 1)[0]
    named = tuple(re.findall(r'"([^"]+)"\s*:', evidence))
    assert named == ("upstream_item_id",)
    assert control_single_agent.EVIDENCE_FIELDS == named + ("quote",)
    assert control_single_agent.QUOTE_FIELD == "quote"


# --- the cutoff the run was assembled under ----------------------------------

def test_the_planted_manifest_is_the_record(tmp_path):
    """Every date in `MANIFEST` read back out of the committed submissions index."""
    rows = json.loads(
        (REPO_ROOT / "tests" / "fixtures" / "AAPL" / "submissions.json")
        .read_text(encoding="utf-8"))["filings"]
    by_accession = {row["accession"]: row for row in rows}
    assert by_accession[ACCESSION]["form"] == MANIFEST["form"] == "10-Q"
    assert by_accession[ACCESSION]["filing_date"] == MANIFEST["filing_date"]
    assert by_accession[PRIOR_ACCESSION]["filing_date"] == "2025-05-02"
    for row in MANIFEST["documents"]:
        recorded = by_accession[row["accession"]]
        assert row["filing_date"] == recorded["filing_date"]
        assert row["form"] == recorded["form"]
        assert row["filing_date"] <= MANIFEST["cutoff"]


def test_a_document_filed_after_the_cutoff_is_refused(tmp_path):
    """The row the manifest itself carries, dated after the boundary it names.

    The date planted is the *next* quarter's own filing date from the committed
    index — the document a bundle triggered by this 10-Q could not have read.
    Two keys agreeing said nothing about it, and the control answered.
    """
    root, folder = plant(tmp_path)
    rows = json.loads(
        (REPO_ROOT / "tests" / "fixtures" / "AAPL" / "submissions.json")
        .read_text(encoding="utf-8"))["filings"]
    later = [row for row in rows
             if row["form"] == "10-Q" and row["filing_date"] > MANIFEST["cutoff"]]
    after = min(row["filing_date"] for row in later)
    ahead = min(row for row in later if row["filing_date"] == after)
    planted = dict(MANIFEST)
    planted["documents"] = MANIFEST["documents"] + [
        {"form": "10-Q", "role": "prior_period", "accession": ahead["accession"],
         "filing_date": ahead["filing_date"]}]
    _replant_manifest(root, planted)
    stub = Stub(accounting_answer())
    with pytest.raises(ControlError) as caught:
        control_single_agent.run("accounting_reliability", input_dir=folder,
                                 bundle_root=root, ask=stub)
    assert ahead["filing_date"] in str(caught.value)
    assert MANIFEST["cutoff"] in str(caught.value)
    assert stub.prompts == []
    assert not (root / "control_single_agent_accounting.json").exists()


def test_a_cutoff_moved_along_with_the_filing_date_is_refused(tmp_path):
    """Both keys moved together, and the record they claim to describe did not.

    `cutoff == filing_date` is satisfied by moving the pair, and every document
    row is then under the new boundary — including the next quarter, which this
    run could not have read. What cannot move with them is the row for the
    filing the manifest says it is about: the triggering report's own filing
    date is on the record, and the run is refused when the two disagree.
    """
    root, folder = plant(tmp_path)
    rows = json.loads(
        (REPO_ROOT / "tests" / "fixtures" / "AAPL" / "submissions.json")
        .read_text(encoding="utf-8"))["filings"]
    later = min((row["filing_date"] for row in rows
                 if row["form"] == "10-Q" and row["filing_date"] > MANIFEST["cutoff"]))
    ahead = min(row for row in rows if row["filing_date"] == later)
    planted = dict(MANIFEST, cutoff=later, filing_date=later)
    planted["documents"] = MANIFEST["documents"] + [
        {"form": ahead["form"], "role": "prior_period",
         "accession": ahead["accession"], "filing_date": ahead["filing_date"]}]
    _replant_manifest(root, planted)
    stub = Stub(accounting_answer())
    with pytest.raises(ControlError) as caught:
        control_single_agent.run("accounting_reliability", input_dir=folder,
                                 bundle_root=root, ask=stub)
    # the pair agreed with each other; the accession's own row is what refused
    assert ACCESSION in str(caught.value)
    assert MANIFEST["filing_date"] in str(caught.value)
    assert later in str(caught.value)
    assert stub.prompts == []
    assert not (root / "control_single_agent_accounting.json").exists()


def test_a_manifest_the_run_holds_only_as_a_link_is_refused(tmp_path):
    """The run's own record, read through a link to another run's.

    Every other file the control reads is compared against the run's copy, and
    this one *is* the run's copy — the cutoff, the accession and the rules
    version all come out of it. `is_file()` and `read_text()` both follow a
    link, so a linked manifest hands the control another run's boundary under
    this run's name, and nothing downstream can see the difference.
    """
    root, folder = plant(tmp_path)
    elsewhere = tmp_path / "another-run"
    elsewhere.mkdir()
    other = dict(MANIFEST, accession=OTHER_ACCESSION,
                 cutoff="2026-01-30", filing_date="2026-01-30")
    other["documents"] = [{"form": "10-Q", "role": "primary_html",
                           "accession": OTHER_ACCESSION,
                           "filing_date": "2026-01-30"}]
    (elsewhere / "input_manifest.json").write_text(
        json.dumps(other, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (root / "input_manifest.json").unlink()
    (root / "input_manifest.json").symlink_to(elsewhere / "input_manifest.json")

    stub = Stub(accounting_answer())
    with pytest.raises((ControlError, cutoff_guard.CutoffGuardError)) as caught:
        control_single_agent.run("accounting_reliability", input_dir=folder,
                                 bundle_root=root, ask=stub)
    assert "symlink" in str(caught.value)
    assert stub.prompts == []
    assert not (root / "control_single_agent_accounting.json").exists()


def _the_next_filing() -> tuple[str, str]:
    """The first filing the record holds after the planted run's cutoff."""
    rows = json.loads(
        (REPO_ROOT / "tests" / "fixtures" / "AAPL" / "submissions.json")
        .read_text(encoding="utf-8"))["filings"]
    later = sorted((row["filing_date"], row["accession"]) for row in rows
                   if row["filing_date"] > MANIFEST["cutoff"])
    assert later, "the record must hold a filing after the cutoff for this to bite"
    return later[0]


def test_a_paragraph_under_a_later_filings_accession_is_refused(tmp_path):
    """The manifest's list is the run's word; the text says where it came from.

    A paragraph appended to `input_notes.md` under the next filing's accession
    is in no `documents` row, so the gate over that list never sees it; it is in
    both copies, so the byte check agrees; and `src/quote_gate.py` indexes it as
    quotable like any other. It was handed to the model, and its quote verified
    and its citation resolved, while the run reported a clean cutoff. The id
    names the filing and the submissions index dates it.
    """
    root, folder = plant(tmp_path)
    filed, late = _the_next_filing()
    extra = f"\n[{late}:notes:9]\nInventories rose sharply during the quarter.\n"
    replant(root, folder, "input_notes.md", NOTES + extra)

    stub = Stub(accounting_answer())
    with pytest.raises(ControlError) as caught:
        control_single_agent.run("accounting_reliability", input_dir=folder,
                                 bundle_root=root, ask=stub)
    assert late in str(caught.value)
    assert filed in str(caught.value)
    assert MANIFEST["cutoff"] in str(caught.value)
    assert stub.prompts == []
    assert not (root / "control_single_agent_accounting.json").exists()


def test_a_paragraph_under_a_filing_nobody_recorded_is_refused(tmp_path):
    """Fail-closed: an accession EDGAR's own catalogue does not list has no date
    to check, so it is refused rather than read as early."""
    root, folder = plant(tmp_path)
    extra = f"\n[{OTHER_ACCESSION}:notes:9]\nDeferred revenue rose.\n"
    replant(root, folder, "input_notes.md", NOTES + extra)

    stub = Stub(accounting_answer())
    with pytest.raises(ControlError, match="in no row of"):
        control_single_agent.run("accounting_reliability", input_dir=folder,
                                 bundle_root=root, ask=stub)
    assert stub.prompts == []


def test_the_planted_manifest_names_the_cutoff_the_filing_date_gives_it():
    assert MANIFEST["cutoff"] == MANIFEST["filing_date"]


def test_the_control_runs_under_the_cutoff_the_manifest_names(tmp_path):
    root, folder = plant(tmp_path)
    result = go(root, folder, "accounting_reliability", accounting_answer())
    assert result["cutoff"] == MANIFEST["cutoff"]


def _planted_manifest(root: Path) -> dict:
    return json.loads((root / "input_manifest.json").read_text(encoding="utf-8"))


def _replant_manifest(root: Path, manifest: dict) -> None:
    (root / "input_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def test_a_manifest_whose_two_dates_disagree_is_refused_by_the_first_rule_too(
        tmp_path):
    """The two keys, compared before the record is read.

    `run_cutoff` compares `cutoff` with `filing_date` and then calls
    `extraction_checks.check_cutoff`, which dates every document row against
    EDGAR's index. The second gate is strictly stronger and answers first on
    anything planted here, which is why switching the comparison off turned
    nothing red. It is the cheaper of the two and it is what the manifest says
    about itself, so it is asserted where it speaks.
    """
    manifest = MANIFEST | {"cutoff": "2025-07-01"}
    with pytest.raises(ControlError) as caught:
        control_single_agent.run_cutoff(manifest)
    assert "names the cutoff 2025-07-01 and the triggering report's filing date" \
        in str(caught.value)
    assert "a boundary nobody set" in str(caught.value)


@pytest.mark.parametrize("manifest,says", [
    ({key: value for key, value in MANIFEST.items() if key != "cutoff"},
     "cutoff is missing"),
    ({key: value for key, value in MANIFEST.items() if key != "filing_date"},
     "filing_date is missing"),
    (MANIFEST | {"cutoff": "the fourth quarter"}, "not an ISO date"),
])
def test_a_manifest_with_no_readable_cutoff_is_refused_by_run_cutoff(
        tmp_path, manifest, says):
    """The same three shapes, straight at the function, so the refusal is its."""
    with pytest.raises(ControlError, match=says):
        control_single_agent.run_cutoff(manifest)


@pytest.mark.parametrize("manifest,says", [
    ({key: value for key, value in MANIFEST.items() if key != "cutoff"},
     "cutoff is missing"),
    ({key: value for key, value in MANIFEST.items() if key != "filing_date"},
     "filing_date is missing"),
    (MANIFEST | {"cutoff": "the fourth quarter"}, "not an ISO date"),
])
def test_a_manifest_with_no_readable_cutoff_is_refused(tmp_path, manifest, says):
    root, folder = plant(tmp_path)
    _replant_manifest(root, manifest)
    stub = Stub(accounting_answer())
    with pytest.raises(ControlError) as caught:
        control_single_agent.run("accounting_reliability", input_dir=folder,
                                 bundle_root=root, ask=stub)
    assert says in str(caught.value)
    assert stub.prompts == []
    assert not (root / "control_single_agent_accounting.json").exists()


def test_a_cutoff_years_before_the_filing_is_refused_rather_than_run(tmp_path):
    """`CLAUDE.md`: the cutoff is the filing date of the triggering report. A
    run that recorded 1999 for a 2025 filing set its boundary somewhere nobody
    decided, and the control is not the place to find that out afterwards."""
    root, folder = plant(tmp_path)
    _replant_manifest(root, MANIFEST | {"cutoff": "1999-12-31"})
    stub = Stub(accounting_answer())
    with pytest.raises(ControlError) as caught:
        control_single_agent.run("accounting_reliability", input_dir=folder,
                                 bundle_root=root, ask=stub)
    assert "1999-12-31" in str(caught.value)
    assert MANIFEST["filing_date"] in str(caught.value)
    assert stub.prompts == []
    assert not (root / "control_single_agent_accounting.json").exists()


# --- the guard's own two sides, and the text nothing dates -------------------

def test_the_run_directory_handed_to_itself_is_refused(tmp_path):
    """The whole guard is one directory compared against another.

    `the_runs_own_copies` compares each handed file with the run's own copy, and
    every other check here rests on that comparison holding. Handed the run
    directory as its own input directory, every comparison passed by identity:
    the pre-call and post-call byte checks were both no-ops, an `ask` that
    appended a paragraph under the next filing's accession wrote it into the one
    file both sides read, and the run reported the cutoff clean with no drop.

    `docs/HOW_WE_WORK.md` makes the per-run, per-agent input directory the
    isolation boundary. A boundary with one side is not one.
    """
    root, _ = plant(tmp_path)
    with pytest.raises(ControlError) as caught:
        control_single_agent.run("accounting_reliability", input_dir=root,
                                 bundle_root=root, ask=Stub(accounting_answer()))
    # `run()` never reaches the identity rule: the run directory holds
    # `input_manifest.json`, which no layer routes to a control, so the
    # allowlist refuses the directory by name one step earlier. That refusal is
    # the one this path actually makes, and the identity rule is asserted below
    # where it can speak.
    assert "input_manifest.json" in str(caught.value)
    assert "a file nobody routed" in str(caught.value)
    with pytest.raises(ControlError) as direct:
        control_single_agent.the_runs_own_copies(["input_notes.md"], root, root)
    assert "is the run directory" in str(direct.value)
    assert "a boundary with one side is not one" in str(direct.value)
    # and by the resolved path, not only by the spelling
    with pytest.raises(ControlError, match="is the run directory"):
        control_single_agent.the_runs_own_copies(
            ["input_notes.md"], root / ".", root)
    # and by inode, which is the one `resolve()` cannot do. `resolve()`
    # normalises `.`, `..` and links and leaves case alone, and this filesystem
    # is case-insensitive -- so one directory under two spellings compared
    # unequal, `st_nlink` was 1 on both names, and every rule below passed by
    # identity. The third reading's fix deleted the per-file `samefile` call as
    # unreachable; the fourth found this, which is the same case one level up.
    spelled = root.parent / root.name.lower()
    if spelled != root and spelled.is_dir():
        assert spelled.samefile(root)
        assert spelled.resolve() != root.resolve()
        with pytest.raises(ControlError, match="is the run directory"):
            control_single_agent.the_runs_own_copies(
                ["input_notes.md"], spelled, root)


def test_a_handed_file_that_is_a_link_to_the_runs_own_is_refused(tmp_path):
    """Two names for one file is one file, and the comparison reads it twice.

    The handed side was never checked for a link: `read_bytes` follows one, so a
    symlink pointing at the run's own copy compared equal to itself, and a
    rewrite during the call landed on both sides at once — the same hole as
    handing over the run directory, one file at a time.
    """
    root, folder = plant(tmp_path)
    name = "input_notes.md"
    (folder / name).unlink()
    (folder / name).symlink_to(root / name)
    with pytest.raises(ControlError) as caught:
        go(root, folder, "accounting_reliability", accounting_answer())
    assert "symlink" in str(caught.value)

    (folder / name).unlink()
    os.link(root / name, folder / name)
    with pytest.raises(ControlError) as caught:
        go(root, folder, "accounting_reliability", accounting_answer())
    # The run's own side speaks, because a hard link raises the link count on
    # both names and that rule is asked first. The `or` this assertion used to
    # carry was hiding which of the two sentences fires -- and the other branch
    # it allowed for, `samefile`, could never fire at all and is gone.
    assert "is one name of 2" in str(caught.value)
    assert str(root / name) in str(caught.value)


def test_a_run_copy_hard_linked_out_of_the_run_is_refused(tmp_path):
    """The reference side, closed the way `src/cutoff_guard.py` closes it.

    A hard link has no target to read and no link bit to test, so the run's copy
    and another directory's file are one file — and whoever holds the other name
    writes the bytes this compares against. The symlink on this side was already
    refused; the link with no arrow was not.
    """
    root, folder = plant(tmp_path)
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    name = "input_notes.md"
    os.link(root / name, elsewhere / name)
    with pytest.raises(ControlError) as caught:
        go(root, folder, "accounting_reliability", accounting_answer())
    assert "one name of" in str(caught.value)


def test_a_handed_file_that_is_a_symlink_is_refused_by_the_comparison_too(tmp_path):
    """The handed side's link rule, reached directly.

    Inside `run()` nothing gets here: `input_files` refuses every symlink in the
    handed directory by name before the comparison is reached, which is why
    switching this rule off turned nothing red. It is the comparison's own floor
    all the same -- `read_bytes` follows a link, so a link pointing at the run's
    copy compares equal to itself -- so it is asserted where it can speak, and
    the test above covers the path `run()` actually takes.
    """
    root, folder = plant(tmp_path)
    name = "input_notes.md"
    (folder / name).unlink()
    (folder / name).symlink_to(root / name)
    with pytest.raises(ControlError) as caught:
        control_single_agent.the_runs_own_copies([name], folder, root)
    assert "is a symlink to" in str(caught.value)


def test_a_manifest_whose_byte_count_disagrees_with_its_own_hash_is_refused(tmp_path):
    """A record that contradicts itself is not a record.

    No tamper reaches this: the same bytes give the same count, so a matching
    sha256 and a wrong `bytes` can only both be true if the manifest was written
    wrong. That is worth refusing and it had no judge, which is how the third
    reading found the field unasserted.
    """
    root, folder = plant(tmp_path)
    manifest = _planted_manifest(root)
    manifest["files"]["input_notes.md"]["bytes"] += 1
    _replant_manifest(root, manifest)
    with pytest.raises(ControlError) as caught:
        go(root, folder, "accounting_reliability", accounting_answer())
    assert "bytes and input_manifest.json records" in str(caught.value)


def test_a_context_the_filing_itself_dates_past_the_cutoff_stands(tmp_path):
    """The control on the test above, and the reason it is filing dates only.

    A filing filed on the first of the month may state a value measured on the
    fifth: NVIDIA's 10-Q filed 2026-08-26 carries an instant of 2026-08-31, and
    Apple's remaining-performance-obligation axis carries fiscal year-ends into
    2028. Those are disclosures, not documents, and refusing them refused
    thirteen of the twenty-four bundles this repository assembles.
    """
    root, folder = plant(tmp_path)
    payload = json.loads(NUMBERS)
    payload["facts"][0]["context"]["instant"] = "2027-01-15"
    replant(root, folder, "input_numbers.json",
            json.dumps(payload, indent=2, sort_keys=True) + "\n")
    go(root, folder, "accounting_reliability", accounting_answer())
    assert written(root, "accounting_reliability")["tier"]


@pytest.mark.parametrize("name", ["input_trends.json", "input_numbers.json"])
def test_a_computed_file_built_at_another_cutoff_is_refused(tmp_path, name):
    """The boundary a computed file says it read at, against the run's.

    `src/trends.py` publishes the cutoff it was handed, so the two can disagree
    only if the file and the run came from different boundaries -- and that is
    exactly the case worth refusing. The fixture carried the matching value from
    the day it was written, so nothing had ever planted a disagreement.
    """
    root, folder = plant(tmp_path)
    payload = json.loads(TRENDS if name == "input_trends.json" else NUMBERS)
    payload["cutoff"] = "2030-01-01"
    replant(root, folder, name,
            json.dumps(payload, indent=2, sort_keys=True) + "\n")
    with pytest.raises(ControlError) as caught:
        go(root, folder, "accounting_reliability", accounting_answer())
    assert f"{name} says it was built at cutoff '2030-01-01'" in str(caught.value)


def test_a_sentence_added_inside_a_block_is_refused(tmp_path):
    """The text the model reads and the record does not account for.

    The first rule here refused prose sitting under no `[id]` line, and refused
    all twenty-four bundles this repository assembles with it: the assembler
    writes undated prose of its own in three of the eight files. The judge was
    already in the directory. A sentence appended *inside* an existing block is
    in a block, quotable, cited and dated like its neighbours -- and it changes
    the file's sha256, which `docs/INPUT_SPEC.md` §6 records per file.
    """
    root, folder = plant(tmp_path)
    inside = NOTES.replace("The allowance for credit losses",
                           "Receivables will fall next quarter. The allowance for "
                           "credit losses")
    assert inside != NOTES
    for where in (root, folder):
        (where / "input_notes.md").write_text(inside, encoding="utf-8")
    with pytest.raises(ControlError) as caught:
        go(root, folder, "accounting_reliability", accounting_answer())
    assert "input_notes.md is not the file the build wrote" in str(caught.value)


def test_a_block_added_under_the_manifests_own_accession_is_refused(tmp_path):
    """The variant the accession gate cannot see, and the paragraph list can.

    `the_text_names_no_later_filing` dates an id's accession against the
    submissions index, so a block planted under the *manifest's own* accession
    dates as the triggering report and passes. Nothing in the record says the
    build wrote it — except `paragraphs`, one row per block with its file. Here
    the hash is re-recorded and the list is not, which is the half of the record
    that catches this one.
    """
    root, folder = plant(tmp_path)
    added = NOTES + f"\n[{ACCESSION}:notes:9]\nReceivables will fall next quarter.\n"
    for where in (root, folder):
        (where / "input_notes.md").write_text(added, encoding="utf-8")
    manifest = _planted_manifest(root)
    manifest["files"]["input_notes.md"] = {
        "sha256": hashlib.sha256(added.encode("utf-8")).hexdigest(),
        "bytes": len(added.encode("utf-8"))}
    _replant_manifest(root, manifest)
    with pytest.raises(ControlError) as caught:
        go(root, folder, "accounting_reliability", accounting_answer())
    assert f"added {ACCESSION}:notes:9" in str(caught.value)
    assert "the record does not know about" in str(caught.value)


def test_a_run_whose_manifest_hashes_nothing_is_refused(tmp_path):
    """An absent `files` is not an empty one: a manifest that accounts for no
    file leaves every sentence the model reads undated, so the control refuses
    the run rather than reading it."""
    root, folder = plant(tmp_path)
    _replant_manifest(root, {key: value for key, value in
                             _planted_manifest(root).items() if key != "files"})
    with pytest.raises(ControlError, match="records no file hashes"):
        go(root, folder, "accounting_reliability", accounting_answer())


def test_a_run_whose_manifest_lists_no_paragraphs_is_refused(tmp_path):
    root, folder = plant(tmp_path)
    _replant_manifest(root, {key: value for key, value in
                             _planted_manifest(root).items() if key != "paragraphs"})
    with pytest.raises(ControlError, match="records no paragraph list"):
        go(root, folder, "accounting_reliability", accounting_answer())


def test_a_handed_file_the_manifest_never_hashed_is_refused(tmp_path):
    """The allowlist says the name is one the control may see; `files` says the
    build wrote it. A file that passes the first and not the second is a file
    somebody put in the directory."""
    root, folder = plant(tmp_path)
    manifest = _planted_manifest(root)
    del manifest["files"]["input_notes.md"]
    _replant_manifest(root, manifest)
    with pytest.raises(ControlError) as caught:
        go(root, folder, "accounting_reliability", accounting_answer())
    assert "records no hash for it" in str(caught.value)


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form", ["10-K", "10-Q"])
def test_a_bundle_this_repository_assembles_is_read_rather_than_refused(
        tmp_path, ticker, form):
    """The judge the first version of the check above did not have.

    It refused every one of these -- twelve companies, both triggering forms --
    before the model call, and the only input it had ever been run against was
    the two-block `input_notes.md` this file plants. So the bundle the assembler
    writes is built here and handed to the four gates that run before the call,
    in the order `run()` runs them, and the assertion is that none of them
    speaks. A guard nothing real is ever passed through is a guard whose reach
    is unknown.
    """
    run = tmp_path / "run"
    manifest = assemble_bundle.assemble(ticker, form, run, prior_runs=tmp_path / "none")
    # `docs/CHECKLIST.md` §8 hands this control "the whole bundle plus the
    # market table", and `src/agent_inputs.py` refuses to assemble a comparer
    # directory unless the run holds one -- so every run that reaches a layer
    # has it. `src/assemble_bundle.py` does not write it and its manifest
    # therefore records no hash for it, which is exactly the case the first
    # version of the hash check refused. It is written here for that reason.
    (run / "input_market.json").write_text(MARKET, encoding="utf-8")
    handed = tmp_path / "single-agent"
    handed.mkdir()
    for name in control_single_agent.CONTROL_SEES:
        if (run / name).is_file():
            shutil.copy2(run / name, handed / name)
    assert (handed / "input_market.json").is_file()
    assert "input_market.json" not in manifest["files"]
    assert not (handed / "input_manifest.json").exists()
    cutoff = cutoff_guard.parse_date(manifest["cutoff"], "the manifest's cutoff")

    control_single_agent.the_runs_own_copies(
        control_single_agent.input_files(handed), handed, run)
    control_single_agent.the_files_are_the_ones_the_manifest_hashed(handed, manifest)
    control_single_agent.the_computed_files_name_no_later_period(handed, cutoff)
    control_single_agent.the_text_names_no_later_filing(
        quote_gate.quotable(handed, manifest["accession"]), cutoff, ticker)


@pytest.mark.parametrize("where,plant_it", [
    ("facts[0].filing_date", lambda p: p["facts"][0].update(filing_date="2027-01-15")),
    ("documents[0].filing_date",
     lambda p: p["documents"][0].update(filing_date="2027-05-05")),
])
def test_a_filing_date_the_numbers_file_prints_past_the_cutoff_is_refused(
        tmp_path, where, plant_it):
    """The larger computed file, and the only one whose rows carry their own date.

    A fact's id begins with the accession of the filing it was drawn from, so a
    fact planted under an in-cutoff accession is dated in-cutoff by
    `the_text_names_no_later_filing` however late its own `filing_date` reads.
    The trend table had this check and the numbers file did not, and the lens
    read a fact dated 2027-01-15 straight through to the model.

    Filing dates only. The first version of this walked every date the file
    prints, the way the trend table's does, and refused thirteen of the
    twenty-four real bundles on contexts the filings themselves state -- see
    `_dates_inside`. A context instant is the filing's subject, not a filing.
    """
    root, folder = plant(tmp_path)
    payload = json.loads(NUMBERS)
    plant_it(payload)
    replant(root, folder, "input_numbers.json",
            json.dumps(payload, indent=2, sort_keys=True) + "\n")
    with pytest.raises(ControlError) as caught:
        go(root, folder, "accounting_reliability", accounting_answer())
    assert f"input_numbers.json.{where}" in str(caught.value)
    assert "after the cutoff 2025-08-01" in str(caught.value)


def test_a_date_used_as_a_key_is_read_like_any_other(tmp_path):
    """A table keyed by period prints its dates on the left of the colon.

    `_iso_dates` recursed on a dict's values only, so a document keyed by date
    published every one of them unread — the same omission as checking two of
    the five places `src/trends.py` prints one, a level further down.
    """
    root, folder = plant(tmp_path)
    payload = json.loads(TRENDS)
    payload["by_period"] = {"2027-03-31": {"days_sales_outstanding": 41.2}}
    replant(root, folder, "input_trends.json",
            json.dumps(payload, indent=2, sort_keys=True) + "\n")
    with pytest.raises(ControlError) as caught:
        go(root, folder, "accounting_reliability", accounting_answer())
    assert "input_trends.json.by_period.2027-03-31 (key)" in str(caught.value)


def test_a_trend_row_reaching_past_the_cutoff_is_refused(tmp_path):
    """The ids the record cannot date, dated by their own periods.

    A trend cell's id is `{accession}:trends:{metric}:{period}`, and that
    accession is the manifest's own — so looking it up in the submissions index
    dates the manifest against the index, which the cutoff gate already does. It
    says nothing about the cell. The period is the part that carries a fact's
    own date, it is printed in the file the model reads, and a row ending after
    the triggering report is a fact from after the triggering report whatever
    its id says.
    """
    root, folder = plant(tmp_path)
    later = json.loads(TRENDS)
    later["quarters"][0]["end"] = "2025-09-30"      # after MANIFEST's 2025-08-01
    replant(root, folder, "input_trends.json",
            json.dumps(later, indent=2, sort_keys=True) + "\n")
    with pytest.raises(ControlError) as caught:
        go(root, folder, "accounting_reliability", accounting_answer())
    assert "after the cutoff 2025-08-01" in str(caught.value)
    assert "input_trends.json.quarters[0].end" in str(caught.value)


@pytest.mark.parametrize("field", ["start", "end", "target_end"])
def test_every_date_a_trend_row_prints_is_inside_the_cutoff(tmp_path, field):
    """All three, because a row names the period it measured and the period it
    was meant to measure, and either one past the boundary is a look-ahead the
    model reads."""
    root, folder = plant(tmp_path)
    later = json.loads(TRENDS)
    later["quarters"][0][field] = "2026-01-31"
    replant(root, folder, "input_trends.json",
            json.dumps(later, indent=2, sort_keys=True) + "\n")
    with pytest.raises(ControlError, match=re.escape(field)):
        go(root, folder, "accounting_reliability", accounting_answer())


def test_a_trend_row_inside_the_cutoff_stands(tmp_path):
    """The control on the two above."""
    root, folder = plant(tmp_path)
    inside = json.loads(TRENDS)
    inside["quarters"][0] |= {"start": "2025-04-01", "end": "2025-06-30",
                              "target_end": "2025-06-30"}
    replant(root, folder, "input_trends.json",
            json.dumps(inside, indent=2, sort_keys=True) + "\n")
    result = go(root, folder, "accounting_reliability", accounting_answer())
    assert written(root, "accounting_reliability")["tier"]
    # The one drop is the dash-changed quote this file plants in every run. The
    # trend cell still resolves: three dates added beside the ratios leave the
    # ratio's own printed lines where they were. Nothing was dropped for the
    # cutoff, which is the assertion.
    assert [row["item_id"] for row in result["dropped"]] == \
        ["accounting_reliability:checklist:estimate_change_favorable"]
