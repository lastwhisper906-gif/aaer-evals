"""The decide stage's Python half, judged against the checklist and the owner's decision.

**The owner's decisions are the expected values.** 2026-09-13: until a price
source answers, the comparers are off and the first predictions publish on
filings alone. 2026-09-23: the supervisors run when the market table is
"unavailable" -- comparer reports absent, `market_direction` written as
"insufficient", the reason "no price source" in the manifest. Each of those
words is asserted below as the owner wrote it.

**`docs/CHECKLIST.md` is the expected value for the rules files.** The key
counts are the numbers in §1's and §2's own headings, read out of the document
here with a pattern of this file's own; the schema is §7's block, found in the
document by this file rather than taken from the module that writes it.

The run directory, the reader input and every answer are planted here as text.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from src import agent_inputs, decide, prediction_schema, quote_gate
from src.agent_inputs import AgentInputError
from src.decide import DecideError

CHECKLIST = Path(__file__).resolve().parent.parent / "docs" / "CHECKLIST.md"
ACCESSION = "0001045810-26-000075"
MANIFEST = "input_manifest.json"

# One notes paragraph, as a committed reader input prints it.
NOTE = f"{ACCESSION}:notes:1"
NOTES = f"""# Notes

[{NOTE}]
Accounts receivable rose to $22.1 billion from $23.1 billion.
"""
QUOTE = "Accounts receivable rose to $22.1 billion"

# Two reader items over it: one quoted verbatim, one with a word changed.
KEPT = f"{NOTE}:receivables-moved"
FALLS = f"{NOTE}:receivables-invented"


def plant(tmp_path: Path, *, rules_version="pilot") -> Path:
    """A run directory after `read`: the manifest, both reader reports, one input."""
    run = tmp_path / "runs" / "NVDA" / ACCESSION
    run.mkdir(parents=True)
    (run / MANIFEST).write_text(json.dumps(
        {"ticker": "NVDA", "accession": ACCESSION, "rules_version": rules_version,
         "counts": {"paragraphs": 1}}, indent=2) + "\n", encoding="utf-8")
    for name in agent_inputs.READER_REPORTS:
        (run / name).write_text(f"# this is {name}\n", encoding="utf-8")
    reader = run / "agents" / "notes-text-reader"
    reader.mkdir(parents=True)
    (reader / "input_notes.md").write_text(NOTES, encoding="utf-8")
    return run


def manifest(run: Path) -> dict:
    return json.loads((run / MANIFEST).read_text(encoding="utf-8"))


def reader_entry(run: Path) -> dict:
    return {"report": "report_notes_text.md", "input": run / "agents" / "notes-text-reader",
            "items": [{"id": KEPT, "paragraph_id": NOTE, "quote": QUOTE},
                      {"id": FALLS, "paragraph_id": NOTE,
                       "quote": "Accounts receivable fell to $22.1 billion"}]}


def answer(**changes) -> dict:
    """A §7 accounting answer, citing one reader item that stands and one that falls."""
    body = {
        "question": "accounting_reliability",
        "rules_version": "pilot",
        "checklist": [
            {"key": "receivables_growth_outruns_revenue", "finding": "flag",
             "confidence": 0.6, "evidence": [{"upstream_item_id": KEPT}]},
            {"key": "bad_debt_reserve_thinning", "finding": "insufficient",
             "confidence": 0.2, "evidence": [{"upstream_item_id": FALLS}]},
        ],
        "events": [],
        "explanations": [],
        "market_direction": {"p_up": 0.4, "basis": [KEPT]},
        "tier": "watch",
        "top_signals": ["receivables_growth_outruns_revenue", "bad_debt_reserve_thinning"],
    }
    body.update(changes)
    return body


# --- the owner's words ---------------------------------------------------------

def test_the_owners_words_are_the_modules():
    assert decide.NO_PRICE_SOURCE == "no price source"
    assert decide.UNAVAILABLE == "unavailable"
    assert decide.ABSTAIN == {"p_up": "insufficient", "basis": []}


# --- the rules beside the reports ---------------------------------------------

def headed_counts() -> dict[str, int]:
    """§1's and §2's own counts, out of their headings."""
    text = CHECKLIST.read_text(encoding="utf-8")
    found = dict(re.findall(r"^## \d\. Input indicators — (\w[\w ]*\w) \((\d+)\)$",
                            text, flags=re.MULTILINE))
    return {"accounting_reliability": int(found["accounting reliability"]),
            "financial_pressure": int(found["financial pressure"])}


def test_the_keys_are_as_many_as_each_heading_says():
    counts = headed_counts()
    assert counts == {"accounting_reliability": 33, "financial_pressure": 17}
    keys = decide.checklist_keys()
    assert {question: len(names) for question, names in keys.items()} == counts
    # The first row of each section's first table, read off the document.
    assert keys["accounting_reliability"][0] == "estimate_change_favorable"
    assert keys["financial_pressure"][0] == "missed_own_outlook"


def test_a_table_that_disagrees_with_its_heading_is_refused():
    text = CHECKLIST.read_text(encoding="utf-8").replace(
        "## 2. Input indicators — financial pressure (17)",
        "## 2. Input indicators — financial pressure (18)")
    with pytest.raises(DecideError, match="disagree"):
        decide.checklist_keys(text)


def test_the_schema_file_is_section_seven_with_the_runs_version():
    schema = decide.rules_texts("pilot")[decide.SCHEMA_FILE]
    block = re.search(r"```json\n(.*?)\n```", schema, flags=re.DOTALL).group(1)
    as_the_document_prints_it = block.replace('"rules_version": "pilot",',
                                              '"rules_version": "0.1",')
    assert as_the_document_prints_it != block
    assert as_the_document_prints_it in CHECKLIST.read_text(encoding="utf-8")


def test_the_keys_file_carries_names_and_no_definitions():
    keys = decide.rules_texts("pilot")[decide.KEYS_FILE]
    assert "`estimate_change_favorable`" in keys
    # §1's other columns never travel: where it is read, who computes it, when it flags.
    assert "critical accounting estimates note" not in keys
    assert "Flags when" not in keys and "Python" not in keys


def test_both_rules_files_are_written_once(tmp_path):
    run = plant(tmp_path)
    written = decide.write_rules(run)
    assert [path.name for path in written] == list(agent_inputs.RULES_FILES)
    assert '"rules_version": "pilot",' in (run / decide.SCHEMA_FILE).read_text(encoding="utf-8")
    assert decide.write_rules(run) == written  # the same bytes again change nothing
    (run / decide.KEYS_FILE).write_text("other\n", encoding="utf-8")
    with pytest.raises(DecideError, match="append-only"):
        decide.write_rules(run)


def test_a_run_naming_no_rules_version_gets_no_schema(tmp_path):
    run = plant(tmp_path)
    body = manifest(run)
    del body["rules_version"]
    (run / MANIFEST).write_text(json.dumps(body) + "\n", encoding="utf-8")
    with pytest.raises(DecideError, match="rules_version"):
        decide.write_rules(run)


# --- no market table ---------------------------------------------------------

def test_the_manifest_says_the_market_table_is_unavailable_and_why(tmp_path):
    run = plant(tmp_path)
    decide.mark_market_unavailable(run)
    written = manifest(run)
    assert written["market_table"] == "unavailable"
    assert written["market_table_reason"] == "no price source"
    assert written["ticker"] == "NVDA" and written["counts"] == {"paragraphs": 1}
    assert agent_inputs.market_unavailable(run) == "no price source"
    decide.mark_market_unavailable(run)  # said again, the same way
    with pytest.raises(DecideError, match="written once"):
        decide.mark_market_unavailable(run, "the feed was down")


@pytest.mark.parametrize("present", ["input_market.json", "report_numbers_vs_market.md",
                                     "report_notes_vs_market.md"])
def test_a_run_that_has_a_market_cannot_say_it_has_none(tmp_path, present):
    run = plant(tmp_path)
    (run / present).write_text("{}\n", encoding="utf-8")
    with pytest.raises(DecideError, match="two things"):
        decide.mark_market_unavailable(run)
    assert "market_table" not in manifest(run)


def test_a_supervisor_runs_on_the_two_reader_reports_and_its_rules(tmp_path):
    """The owner's judge: the supervisors run when the market table is
    unavailable, with the comparer reports absent."""
    run = plant(tmp_path)
    decide.write_rules(run)
    decide.mark_market_unavailable(run)
    for agent in decide.QUESTIONS:
        built = agent_inputs.build(run, agent)
        assert sorted(built["files"]) == sorted(agent_inputs.READER_REPORTS
                                                + agent_inputs.RULES_FILES)
        assert sorted(built["absent"]) == sorted(agent_inputs.COMPARER_REPORTS)
    assert agent_inputs.isolation_violations(run) == []


def test_without_the_manifest_saying_so_a_supervisor_still_waits_for_the_comparers(tmp_path):
    run = plant(tmp_path)
    decide.write_rules(run)
    with pytest.raises(AgentInputError, match="report_numbers_vs_market.md"):
        agent_inputs.build(run, "supervisor-accounting")


@pytest.mark.parametrize("comparer", ["numbers-vs-market", "notes-vs-market"])
def test_no_comparer_is_built_when_there_is_no_market_table(tmp_path, comparer):
    run = plant(tmp_path)
    decide.mark_market_unavailable(run)
    with pytest.raises(AgentInputError, match="nothing to compare"):
        agent_inputs.build(run, comparer)
    assert not agent_inputs.session_root(run, comparer).exists()


def test_a_run_saying_no_market_and_holding_a_comparer_report_is_refused(tmp_path):
    run = plant(tmp_path)
    decide.write_rules(run)
    decide.mark_market_unavailable(run)
    (run / "report_notes_vs_market.md").write_text("# a comparer's\n", encoding="utf-8")
    with pytest.raises(AgentInputError, match="two things"):
        agent_inputs.build(run, "supervisor-pressure")


@pytest.mark.parametrize("said, reason", [("available", "no price source"),
                                          ("unavailable", ""), ("unavailable", None)])
def test_a_manifest_saying_anything_else_about_the_market_is_refused(tmp_path, said, reason):
    run = plant(tmp_path)
    body = manifest(run) | {"market_table": said, "market_table_reason": reason}
    (run / MANIFEST).write_text(json.dumps(body) + "\n", encoding="utf-8")
    with pytest.raises(AgentInputError, match="market table"):
        agent_inputs.market_unavailable(run)


# --- what of an answer stands ------------------------------------------------

def test_a_checked_answer_passes_through(tmp_path):
    run = plant(tmp_path)
    assert decide.check(run, "accounting_reliability", answer()) == answer()


@pytest.mark.parametrize("change, said", [
    ({"question": "financial_pressure"}, "never merged"),
    ({"rules_version": "0.1"}, "scored against its own rules version"),
    ({"tier": "fine"}, "tier"),
    ({"continuous": []}, "continuous"),
])
def test_an_answer_that_is_not_the_runs_or_not_section_seven_is_refused(tmp_path, change, said):
    run = plant(tmp_path)
    with pytest.raises(DecideError, match=said):
        decide.check(run, "accounting_reliability", answer(**change))


def gated(run: Path, body: dict) -> tuple[dict, dict | None]:
    """The run's two layers through the one gate, then the published prediction."""
    question = body["question"]
    result = quote_gate.gate(
        [reader_entry(run),
         {"report": decide.PREDICTION_FILES[question],
          "items": decide.gate_items(question, body),
          "cites": ["report_notes_text.md"]}], run)
    return decide.published(run, question, body, result["kept"][decide.PREDICTION_FILES[question]])


def test_an_entry_citing_a_dropped_reader_item_is_dropped_and_counted(tmp_path):
    run = plant(tmp_path)
    prediction, override = gated(run, answer())
    assert [entry["key"] for entry in prediction["checklist"]] == [
        "receivables_growth_outruns_revenue"]
    assert prediction["top_signals"] == ["receivables_growth_outruns_revenue"]
    # A market is on record in this run, so the supervisor's direction stands.
    assert override is None
    assert prediction["market_direction"] == {"p_up": 0.4, "basis": [KEPT]}
    dropped = [row["item_id"] for row in manifest(run)["dropped_items"]]
    assert dropped == [FALLS, "accounting_reliability:checklist:bad_debt_reserve_thinning"]
    assert manifest(run)["counts"]["dropped_items"] == 2


def test_with_no_market_table_the_direction_is_written_insufficient(tmp_path):
    """The owner's words: market_direction written as "insufficient", and the
    reason "no price source" in the manifest."""
    run = plant(tmp_path)
    decide.mark_market_unavailable(run)
    prediction, override = gated(run, answer())
    assert prediction["market_direction"] == {"p_up": "insufficient", "basis": []}
    assert override == {"prediction": "prediction_accounting.json",
                        "reason": "no price source",
                        "supervisor_said": {"p_up": 0.4, "basis": [KEPT]}}
    decide.record(run, [override])
    assert manifest(run)["market_direction_written_insufficient"] == [override]
    assert manifest(run)["market_table_reason"] == "no price source"


def test_a_direction_resting_on_a_dropped_item_abstains(tmp_path):
    run = plant(tmp_path)
    prediction, _ = gated(run, answer(market_direction={"p_up": 0.7, "basis": [FALLS]}))
    assert prediction["market_direction"] == {"p_up": "insufficient", "basis": []}


def test_the_published_prediction_is_still_section_seven(tmp_path):
    run = plant(tmp_path)
    decide.mark_market_unavailable(run)
    prediction, _ = gated(run, answer())
    assert decide.check(run, "accounting_reliability", prediction) == prediction


def test_the_prediction_is_written_once_into_the_run_directory(tmp_path):
    run = plant(tmp_path)
    prediction, _ = gated(run, answer())
    path = decide.write_prediction(run, "accounting_reliability", prediction)
    assert path == run / "prediction_accounting.json"
    assert json.loads(path.read_text(encoding="utf-8")) == prediction
    assert decide.write_prediction(run, "accounting_reliability", prediction) == path
    with pytest.raises(DecideError, match="written once"):
        decide.write_prediction(run, "accounting_reliability", prediction | {"tier": "clear"})


def test_the_schema_block_moved_and_the_control_shows_the_same_one():
    """One §7 block for both callers, still a slice of the document."""
    from src import control_single_agent
    assert control_single_agent.SCHEMA == prediction_schema.BLOCK
    assert prediction_schema.BLOCK in CHECKLIST.read_text(encoding="utf-8")
