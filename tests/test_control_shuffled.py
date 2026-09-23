"""The crossing is the control, so the crossing is what is asserted.

Where the expected values come from
-----------------------------------

**What is swapped** is `docs/CHECKLIST.md` §8, in its own words: "company A keeps
`report_numbers.md` and `report_numbers_vs_market.md`; `report_notes_text.md` and
`report_notes_vs_market.md` come from company B."
`test_the_checklist_still_says_which_side_each_report_is_on` reads that sentence
out of the document rather than trusting this paragraph, because the split
written in two files is two rules until something reads both.

**Which company is B** is the same section: "the next company in the twelve by
ticker, wrapping around". The twelve are `src/fetch_fixtures.TICKERS`; in ticker
order they begin AAPL, CARR, so AAPL's partner is CARR.

**The two file names** are `docs/INPUT_SPEC.md` §6, which lists
`control_shuffled_accounting.json` and `control_shuffled_pressure.json` in the
committed bundle, and the two scorecard rows are `docs/CHECKLIST.md` §8's
`shuffled_accounting` and `shuffled_pressure`.

**Which company each half came from** is `tests/fixtures/shuffled_report_pair/`,
eight report files written by hand. Nothing in this file was produced by running
`src/control_shuffled.py`: the reports were written before it was, the
predictions the stand-in supervisor returns are written out below, and the
crossing is asserted against the fixture text, never against what the runner
reported about itself.

**Which filing each half was written from** is `tests/fixtures/{ticker}/manifest.json`,
the record of what was fetched from EDGAR: AAPL's 10-K is accession
`0000320193-25-000079` filed 2025-10-31, CARR's is `0001783180-26-000008` filed
2026-02-05, and those two accessions are the ones the committed reports carry in
their item ids. The ninety-seven days between them are counted out below.

The crossing assertion carries its own control
----------------------------------------------

"The notes came from the other company" is only readable if the two companies'
notes reports are not the same text, so
`test_the_two_companies_reports_differ_file_by_file` asserts that first and the
crossing assertions have something to bite on. The sharp form of the crossing is
`test_the_notes_half_is_not_the_numbers_company_own_notes`: AAPL's own notes
report is in the fixture and sitting in the bundle, and the supervisor did not
get it.

A label is not a crossing, and neither is a round trip
------------------------------------------------------

Two directories that both hold AAPL's reports satisfy every label a caller could
pass, so `test_two_directories_of_one_companys_reports_are_refused` builds that
pair and asserts the refusal names AAPL -- the company found on both sides --
and not CARR, the company the label claimed.
"""

from __future__ import annotations

import datetime as dt
import json
import math
import re
import shutil
from pathlib import Path

import pytest

from src import agent_inputs, control_shuffled, cutoff_guard, prediction_schema
from src.control_shuffled import ControlError
from src.fetch_fixtures import TICKERS

REPO_ROOT = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures"
PAIR = FIXTURES / "shuffled_report_pair"

# Company A keeps the numbers side and is the company being scored; company B
# supplies the notes side. docs/CHECKLIST.md §8, applied to the twelve.
#
# Carrier is the numbers side and Apple the notes side, which is the way round
# the cutoff allows: the notes half was filed 2025-10-31 and the filing being
# scored 2026-02-05. The pair used to run the other way and was ungated only
# because a pair of report directories carries no manifest -- ninety-seven days
# of look-ahead, in the fixture every crossing test ran on.
NUMBERS_COMPANY = "CARR"
NOTES_COMPANY = "AAPL"

# The filing each company's committed reports were written from, read off
# tests/fixtures/{ticker}/manifest.json. Asserted against the manifests below
# rather than trusted here.
NUMBERS_ACCESSION = "0001783180-26-000008"
NOTES_ACCESSION = "0000320193-25-000079"
NUMBERS_FILED = "2026-02-05"
NOTES_FILED = "2025-10-31"

# One id the numbers company's own notes-text report carries -- the report the
# crossing takes away from the supervisor, so it is in none of the four reports
# it was handed -- and one the crossed set does hold, out of that company's
# numbers-versus-market report.
UNCROSSED_ITEM = "0001783180-26-000008:notes:inventory:1"
CROSSED_ITEM = "0001783180-26-000008:numbers_vs_market:1"
# And one out of the *other* half. Every citation in this file used to come from
# the numbers side, so indexing only that side passed every test -- in a control
# whose whole point is that the two halves are two companies'.
NOTES_HALF_ITEM = "0000320193-25-000079:notes:receivables:1"

# The pairing rule's own example, which is not the way this file's fixture pair
# runs: the rule hands a run scoring Apple the notes of a filing ninety-seven
# days later, and the cutoff refuses it. Read off the committed manifests below.
PAIRING_EXAMPLE = "AAPL"
PAIRING_PARTNER = "CARR"
PAIRING_EXAMPLE_FILED = "2025-10-31"
PAIRING_PARTNER_FILED = "2026-02-05"

# docs/INPUT_SPEC.md §6.
ACCOUNTING_FILE = "control_shuffled_accounting.json"
PRESSURE_FILE = "control_shuffled_pressure.json"

# What the pipeline's own supervisor would return, written here by hand so that
# nothing the runner writes is judged against something the runner produced. The
# shapes are docs/CHECKLIST.md §7; `continuous` is financial pressure only.
#
# The findings read `flag` and `no_flag` because those are the two §7 lists,
# beside `insufficient`. They used to read `yes` and `no`, which §7 lists
# nowhere and the control accepted, because the control checked the fields the
# citation gate reads and let every other field through untouched.
ACCOUNTING_ANSWER = {
    "checklist": [{"key": "receivables_growth_outruns_revenue", "finding": "flag",
                   "confidence": 0.6,
                   "evidence": [{"upstream_item_id": CROSSED_ITEM}]}],
    "events": [{"key": "restatement", "p_within_horizon": 0.1}],
    "explanations": [],
    # A number resting on an id the crossed set carries. It used to rest on an
    # empty basis, which stood only because this control skipped the field
    # whenever the basis was empty -- the fixture was holding the gate open.
    "market_direction": {"p_up": 0.4, "basis": [CROSSED_ITEM]},
    "tier": "watch",
    "top_signals": ["receivables_growth_outruns_revenue"],
}
PRESSURE_ANSWER = {
    "checklist": [{"key": "liquidity_headroom", "finding": "no_flag", "confidence": 0.3,
                   "evidence": [{"upstream_item_id": CROSSED_ITEM}]}],
    "continuous": [{"key": "revenue_next_quarter", "point": 100.0,
                    "direction": "down", "low": 90.0, "high": 110.0}],
    "events": [{"key": "covenant_breach", "p_within_horizon": 0.05}],
    "explanations": [],
    "market_direction": {"p_up": "insufficient", "basis": []},
    "tier": "clear",
    "top_signals": [],
}
ANSWERS = {"accounting_reliability": ACCOUNTING_ANSWER,
           "financial_pressure": PRESSURE_ANSWER}


class StandInSupervisor:
    """The one model call per question, and a record of what it was handed."""

    def __init__(self, answers: dict = ANSWERS):
        self.answers = answers
        self.calls: list[tuple[str, dict]] = []

    def __call__(self, question: str, reports: dict) -> dict:
        self.calls.append((question, dict(reports)))
        return dict(self.answers[question])

    def saw(self, question: str) -> dict:
        return next(reports for asked, reports in self.calls if asked == question)


def report_text(ticker: str, name: str) -> str:
    """One committed fixture report, as it was written by hand."""
    return (PAIR / ticker / name).read_text(encoding="utf-8")


def bundle(root: Path, ticker: str) -> Path:
    """A run directory holding one company's four reports, built for this test."""
    folder = root / ticker
    folder.mkdir(parents=True, exist_ok=True)
    for name in control_shuffled.REPORTS:
        (folder / name).write_text(report_text(ticker, name), encoding="utf-8")
    return folder


def annual(ticker: str) -> dict:
    """The 10-K row `tests/fixtures/{ticker}/manifest.json` records for a company."""
    return cutoff_guard.one_document(ticker, "10-K", "primary_html")


def scored_run(folder: Path, ticker: str) -> Path:
    """Make a bundle say which filing it is scoring, the way a run directory does.

    `src/assemble_bundle.py` writes the triggering report's own filing date into
    `input_manifest.json`, and the cutoff is that date in those words. Nothing
    here is invented: the accession and the date come out of the company's own
    committed manifest.
    """
    row = annual(ticker)
    (folder / control_shuffled.MANIFEST).write_text(
        json.dumps({"ticker": ticker, "form": "10-K", "accession": row["accession"],
                    "filing_date": row["filing_date"], "cutoff": row["filing_date"]},
                   indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return folder


def run_crossed(tmp_path, out, predictor):
    """The crossed run under test: Carrier's numbers side, Apple's notes side.

    Only the supervisor varies between the tests that call this, so it is the
    only thing they name.
    """
    return control_shuffled.run(
        NUMBERS_COMPANY, NOTES_COMPANY,
        numbers_bundle=bundle(tmp_path, NUMBERS_COMPANY),
        notes_bundle=bundle(tmp_path, NOTES_COMPANY),
        out=out, predictor=predictor)


@pytest.fixture
def out(tmp_path):
    """The empty run directory one crossed pair is written into."""
    folder = tmp_path / "out"
    folder.mkdir()
    return folder


@pytest.fixture
def crossed_run(tmp_path, out):
    """Both control files, written from the fixture pair by a stand-in supervisor."""
    supervisor = StandInSupervisor()
    return run_crossed(tmp_path, out, supervisor), supervisor, out


# --- the fixture pair is what it claims to be --------------------------------

def test_the_pair_holds_the_four_reports_for_each_company():
    for ticker in (NUMBERS_COMPANY, NOTES_COMPANY):
        assert sorted(path.name for path in (PAIR / ticker).iterdir()) == \
               sorted(control_shuffled.REPORTS)


def test_the_two_companies_reports_differ_file_by_file():
    """The control on every crossing assertion below.

    If the two companies wrote the same notes report, "the notes came from the
    other company" would be unreadable from the text and every assertion that
    reads it would pass for the wrong reason.
    """
    for name in control_shuffled.REPORTS:
        assert report_text(NUMBERS_COMPANY, name) != report_text(NOTES_COMPANY, name)


def test_each_report_names_its_own_company():
    for ticker in (NUMBERS_COMPANY, NOTES_COMPANY):
        other = NOTES_COMPANY if ticker == NUMBERS_COMPANY else NUMBERS_COMPANY
        for name in control_shuffled.REPORTS:
            text = report_text(ticker, name)
            assert text.startswith(f"# {ticker} ")
            assert other not in text


def test_each_report_carries_the_accession_the_manifest_records_for_that_company():
    """A half says which filing it came from, and the record agrees."""
    for ticker, accession in ((NUMBERS_COMPANY, NUMBERS_ACCESSION),
                              (NOTES_COMPANY, NOTES_ACCESSION)):
        assert annual(ticker)["accession"] == accession
        for name in control_shuffled.REPORTS:
            assert control_shuffled.named_accession(
                name, report_text(ticker, name)) == accession
            assert control_shuffled.named_company(
                name, report_text(ticker, name)) == ticker


def test_the_pairing_rules_own_example_is_ninety_seven_days_of_look_ahead():
    """Read off the two manifests, and counted out here rather than trusted.

    The rule pairs Apple with Carrier. 2025-10-31 to 2025-11-30 is 30 days, to
    2025-12-31 is 61, to 2026-01-31 is 92, and to 2026-02-05 is 97 -- so a run
    scoring Apple would be handed notes written from a filing ninety-seven days
    after the one being scored, which is what the gate refuses and why this
    file's fixture pair runs the other way round.
    """
    assert control_shuffled.partner(PAIRING_EXAMPLE) == PAIRING_PARTNER
    assert annual(PAIRING_EXAMPLE)["filing_date"] == PAIRING_EXAMPLE_FILED
    assert annual(PAIRING_PARTNER)["filing_date"] == PAIRING_PARTNER_FILED
    apart = (dt.date.fromisoformat(PAIRING_PARTNER_FILED)
             - dt.date.fromisoformat(PAIRING_EXAMPLE_FILED))
    assert apart.days == 97


def test_the_fixture_pair_is_the_way_round_the_cutoff_allows():
    """The notes half is not later than the filing being scored."""
    assert annual(NUMBERS_COMPANY)["filing_date"] == NUMBERS_FILED
    assert annual(NOTES_COMPANY)["filing_date"] == NOTES_FILED
    assert NOTES_FILED < NUMBERS_FILED


def test_seven_of_the_twelve_pairings_put_the_partner_after_the_filing_being_scored():
    """The adverse result, counted rather than described.

    The pairing rule is fixed and the cutoff is absolute, and on the twelve as
    they stand the two collide for seven companies. The seven are written out
    here from the twelve annual filing dates in the committed manifests, so the
    day the fixture set moves this test says which pairings moved with it.
    """
    late = tuple(ticker for ticker in control_shuffled.PAIRING_ORDER
                 if annual(control_shuffled.partner(ticker))["filing_date"] >
                 annual(ticker)["filing_date"])
    assert late == ("AAPL", "CSCO", "ESE", "GNRC", "LFUS", "PANW", "QCOM")


# --- which company is B ------------------------------------------------------

def test_the_partner_is_the_next_company_in_the_twelve_by_ticker():
    assert control_shuffled.PAIRING_ORDER == tuple(sorted(TICKERS))
    assert control_shuffled.partner(PAIRING_EXAMPLE) == PAIRING_PARTNER


def test_the_pairing_wraps_around_and_pairs_nobody_with_themselves():
    order = control_shuffled.PAIRING_ORDER
    assert control_shuffled.partner(order[-1]) == order[0]
    assert all(control_shuffled.partner(ticker) != ticker for ticker in order)
    # One cycle over all twelve, so every company is somebody's notes side.
    assert {control_shuffled.partner(ticker) for ticker in order} == set(order)


def test_a_company_outside_the_twelve_has_no_partner():
    with pytest.raises(ControlError):
        control_shuffled.partner("NOTATICKER")


# --- the split, read out of the document that states it ----------------------

def test_the_checklist_still_says_which_side_each_report_is_on():
    """The split written in two files is two rules until something reads both.

    Matched with the line wrapping collapsed, so the assertion is coupled to
    what the document says and not to where its lines happen to break.
    """
    checklist = " ".join(
        (REPO_ROOT / "docs" / "CHECKLIST.md").read_text(encoding="utf-8").split())
    assert ("company A keeps `report_numbers.md` and `report_numbers_vs_market.md`; "
            "`report_notes_text.md` and `report_notes_vs_market.md` come from "
            "company B") in checklist
    assert "the next company in the twelve by ticker, wrapping around" in checklist
    assert control_shuffled.NUMBERS_SIDE == ("report_numbers.md",
                                             "report_numbers_vs_market.md")
    assert control_shuffled.NOTES_SIDE == ("report_notes_text.md",
                                           "report_notes_vs_market.md")


# --- both files are written --------------------------------------------------

def test_both_control_files_are_written(crossed_run):
    _, _, out = crossed_run
    assert sorted(path.name for path in out.iterdir()) == \
           sorted((ACCOUNTING_FILE, PRESSURE_FILE))


def test_the_two_files_are_the_names_the_input_spec_lists(crossed_run):
    """The two names are §6's, read out of §6 rather than restated here."""
    spec = (REPO_ROOT / "docs" / "INPUT_SPEC.md").read_text(encoding="utf-8")
    for name in (ACCOUNTING_FILE, PRESSURE_FILE):
        assert f"\n{name}\n" in spec
    result, _, out = crossed_run
    assert result["files"]["accounting_reliability"] == out / ACCOUNTING_FILE
    assert result["files"]["financial_pressure"] == out / PRESSURE_FILE
    assert set(control_shuffled.CONTROL_FILES.values()) == \
           {ACCOUNTING_FILE, PRESSURE_FILE}


# --- the crossing itself -----------------------------------------------------

def test_the_numbers_half_came_from_one_company_and_the_notes_half_from_the_other(
        crossed_run):
    """What the supervisor was handed, not what the runner said about it."""
    _, supervisor, _ = crossed_run
    for question in control_shuffled.QUESTIONS:
        saw = supervisor.saw(question)
        for name in control_shuffled.NUMBERS_SIDE:
            assert saw[name] == report_text(NUMBERS_COMPANY, name)
        for name in control_shuffled.NOTES_SIDE:
            assert saw[name] == report_text(NOTES_COMPANY, name)


def test_the_notes_half_is_not_the_numbers_company_own_notes(crossed_run):
    """The sharp form: AAPL's own notes report was in the bundle and was not used."""
    _, supervisor, _ = crossed_run
    saw = supervisor.saw("accounting_reliability")
    for name in control_shuffled.NOTES_SIDE:
        assert saw[name] != report_text(NUMBERS_COMPANY, name)


def test_the_supervisor_is_handed_the_four_reports_and_nothing_else(crossed_run):
    _, supervisor, _ = crossed_run
    for _, saw in supervisor.calls:
        assert sorted(saw) == sorted(control_shuffled.REPORTS)


def test_each_question_gets_one_model_call_on_the_same_crossed_evidence(crossed_run):
    _, supervisor, _ = crossed_run
    assert [question for question, _ in supervisor.calls] == \
           list(control_shuffled.QUESTIONS)
    first, second = (saw for _, saw in supervisor.calls)
    assert first == second


# --- what the written file records -------------------------------------------

def written(out: Path, name: str) -> dict:
    return json.loads((out / name).read_text(encoding="utf-8"))


# `test_the_control_file_records_which_company_each_half_came_from` was here and
# is gone: it read back the two strings `run_crossed` passed in, so it stood
# whether the halves were crossed or not, and it passed under a mutation that let
# the labels overwrite what the reports say. What replaces it is below -- the run
# directory and the accession, read off the halves themselves -- and the
# refusals that judge the labels against the reports.


def test_the_control_file_records_which_run_each_half_came_from(crossed_run, tmp_path):
    """The part a label cannot forge.

    Everything above this reads back the two strings `run_crossed` passed in, so
    it stands whether the halves were crossed or not. The run directory and the
    accession are read off the halves themselves -- the directory the reports
    were opened from, and the accession their own item ids begin with -- so a
    control file written from one company's two halves cannot record two.
    """
    _, _, out = crossed_run
    for name in (ACCOUNTING_FILE, PRESSURE_FILE):
        control = written(out, name)["control"]
        assert control["numbers_run"] == str((tmp_path / NUMBERS_COMPANY).resolve())
        assert control["notes_run"] == str((tmp_path / NOTES_COMPANY).resolve())
        assert control["numbers_accession"] == NUMBERS_ACCESSION
        assert control["notes_accession"] == NOTES_ACCESSION
        # Nothing here carries a manifest, and the gate used to come off with
        # it. The numbers half declares its own filing all the same, and the
        # file records which of the two answered.
        assert control["scored_filing_date"] == NUMBERS_FILED
        assert control["scored_filing_date_from"] == control_shuffled.HALF_BASIS


def test_the_control_file_names_the_scorecard_row_it_is_scored_on(crossed_run):
    """A control is scored beside the pipeline's number and never merged into it."""
    _, _, out = crossed_run
    assert written(out, ACCOUNTING_FILE)["control"]["scorecard_row"] == \
           "shuffled_accounting"
    assert written(out, PRESSURE_FILE)["control"]["scorecard_row"] == \
           "shuffled_pressure"


def test_the_control_file_is_the_prediction_schema(crossed_run):
    _, _, out = crossed_run
    accounting = written(out, ACCOUNTING_FILE)
    pressure = written(out, PRESSURE_FILE)
    assert accounting["question"] == "accounting_reliability"
    assert pressure["question"] == "financial_pressure"
    for payload, answer in ((accounting, ACCOUNTING_ANSWER),
                            (pressure, PRESSURE_ANSWER)):
        assert payload["rules_version"] == control_shuffled.RULES_VERSION
        for key, value in answer.items():
            assert payload[key] == value
    # `continuous` is financial pressure only.
    assert "continuous" not in accounting
    assert pressure["continuous"] == PRESSURE_ANSWER["continuous"]


# --- what is refused ---------------------------------------------------------

def test_a_supervisor_given_one_companys_own_two_halves_is_refused(tmp_path, out):
    """Uncrossed is the real run. A control that is the real run measures nothing."""
    with pytest.raises(ControlError, match="real run"):
        control_shuffled.run(
            NUMBERS_COMPANY, NUMBERS_COMPANY,
            numbers_bundle=bundle(tmp_path, NUMBERS_COMPANY),
            notes_bundle=bundle(tmp_path / "second", NUMBERS_COMPANY),
            out=out, predictor=StandInSupervisor())
    assert list(out.iterdir()) == []


def test_one_bundle_used_for_both_halves_is_refused(tmp_path, out):
    """Named, because the same-company refusal fires on this input too.

    With a bare `pytest.raises(ControlError)` this test passed with the
    same-directory refusal deleted: the two halves are also one company's, so
    the later sentence caught it and the test could not tell the two rules
    apart. It names the sentence it is about.
    """
    only = bundle(tmp_path, NUMBERS_COMPANY)
    with pytest.raises(ControlError) as caught:
        control_shuffled.run(NUMBERS_COMPANY, NOTES_COMPANY,
                             numbers_bundle=only, notes_bundle=only,
                             out=out, predictor=StandInSupervisor())
    assert "both halves would come out of" in str(caught.value)
    assert list(out.iterdir()) == []


def test_a_missing_report_writes_no_control_file(tmp_path, out):
    """Fail closed: half a crossing is not a control with one file missing."""
    notes = bundle(tmp_path, NOTES_COMPANY)
    (notes / "report_notes_vs_market.md").unlink()
    supervisor = StandInSupervisor()
    with pytest.raises(ControlError, match="report_notes_vs_market.md"):
        control_shuffled.run(NUMBERS_COMPANY, NOTES_COMPANY,
                             numbers_bundle=bundle(tmp_path, NUMBERS_COMPANY),
                             notes_bundle=notes, out=out, predictor=supervisor)
    assert list(out.iterdir()) == []
    assert supervisor.calls == []


@pytest.mark.parametrize("missing", ["checklist", "market_direction", "tier"])
def test_an_answer_short_of_the_schema_is_refused(tmp_path, out, missing):
    short = {question: {key: value for key, value in answer.items() if key != missing}
             for question, answer in ANSWERS.items()}
    with pytest.raises(ControlError, match=missing):
        run_crossed(tmp_path, out, StandInSupervisor(short))
    assert list(out.iterdir()) == []


@pytest.mark.parametrize("short_question", list(ANSWERS))
def test_a_short_answer_to_either_question_writes_neither_file(tmp_path, out,
                                                               short_question):
    """Two rows of one scorecard. Half a crossed pair cannot be finished later:
    the directory it would land in is one where nothing may be rewritten."""
    answers = dict(ANSWERS)
    answers[short_question] = {key: value
                               for key, value in ANSWERS[short_question].items()
                               if key != "tier"}
    with pytest.raises(ControlError, match="tier"):
        run_crossed(tmp_path, out, StandInSupervisor(answers))
    assert list(out.iterdir()) == []


def test_continuous_on_the_accounting_question_is_refused(tmp_path, out):
    """`continuous` is financial pressure only (docs/CHECKLIST.md §7)."""
    answers = {"accounting_reliability": dict(ACCOUNTING_ANSWER,
                                              continuous=PRESSURE_ANSWER["continuous"]),
               "financial_pressure": PRESSURE_ANSWER}
    with pytest.raises(ControlError, match="continuous"):
        run_crossed(tmp_path, out, StandInSupervisor(answers))


@pytest.mark.parametrize("on_record", [ACCOUNTING_FILE, PRESSURE_FILE])
def test_a_control_file_already_on_record_is_not_rewritten(tmp_path, out, on_record):
    """A run directory is append-only. A correction is a new run, not an overwrite.

    Either file being on record stops the whole run, so neither half of an
    earlier crossing is left standing beside a fresh half of another.
    """
    already = '{"question": "something else"}\n'
    (out / on_record).write_text(already, encoding="utf-8")
    with pytest.raises(ControlError, match="already on record"):
        run_crossed(tmp_path, out, StandInSupervisor())
    assert [path.name for path in out.iterdir()] == [on_record]
    assert (out / on_record).read_text(encoding="utf-8") == already


def test_writing_the_same_control_twice_is_allowed(crossed_run, tmp_path):
    """Rewriting identical content changes nothing on record, so it is not a change."""
    _, _, out = crossed_run
    before = (out / ACCOUNTING_FILE).read_text(encoding="utf-8")
    run_crossed(tmp_path, out, StandInSupervisor())
    assert (out / ACCOUNTING_FILE).read_text(encoding="utf-8") == before


# --- the label is not the crossing -------------------------------------------

def test_two_directories_of_one_companys_reports_are_refused(tmp_path, out):
    """The real uncrossed run, wearing the label of the shuffled one.

    Two directories and two labels satisfy every check a label can carry, and
    what would land on disk is a control file recording AAPL and CARR over a
    supervisor that read AAPL's own numbers beside AAPL's own notes. The reports
    say whose they are, so the refusal names AAPL and not the label.
    """
    supervisor = StandInSupervisor()
    with pytest.raises(ControlError, match="real run") as refusal:
        control_shuffled.run(
            NUMBERS_COMPANY, NOTES_COMPANY,
            numbers_bundle=bundle(tmp_path / "first", NUMBERS_COMPANY),
            notes_bundle=bundle(tmp_path / "second", NUMBERS_COMPANY),
            out=out, predictor=supervisor)
    assert NUMBERS_COMPANY in str(refusal.value)
    assert NOTES_COMPANY not in str(refusal.value)
    assert list(out.iterdir()) == []
    assert supervisor.calls == []


def test_a_half_whose_label_disagrees_with_its_own_reports_is_refused(tmp_path, out):
    """The label is what the control file would carry, so the reports settle it."""
    supervisor = StandInSupervisor()
    with pytest.raises(ControlError, match="labelled"):
        control_shuffled.run(NOTES_COMPANY, NUMBERS_COMPANY,
                             numbers_bundle=bundle(tmp_path, NUMBERS_COMPANY),
                             notes_bundle=bundle(tmp_path, NOTES_COMPANY),
                             out=out, predictor=supervisor)
    assert list(out.iterdir()) == []
    assert supervisor.calls == []


@pytest.mark.parametrize("side", ["numbers", "notes"])
def test_a_ticker_outside_the_twelve_is_refused(tmp_path, out, side):
    """`partner` has always checked; the runner never asked it to."""
    labels = {"numbers": ("NOTATICKER", NOTES_COMPANY),
              "notes": (NUMBERS_COMPANY, "NOTATICKER")}[side]
    supervisor = StandInSupervisor()
    with pytest.raises(ControlError, match="not one of the twelve"):
        control_shuffled.run(*labels,
                             numbers_bundle=bundle(tmp_path, NUMBERS_COMPANY),
                             notes_bundle=bundle(tmp_path, NOTES_COMPANY),
                             out=out, predictor=supervisor)
    assert list(out.iterdir()) == []
    assert supervisor.calls == []


# --- the cutoff reaches the crossed set --------------------------------------

def test_a_partner_filed_after_the_filing_being_scored_is_refused(tmp_path, out):
    """CLAUDE.md: nothing filed after the triggering report enters the input.

    The pair is the one the pairing rule itself produces for Apple, and
    Carrier's annual report was filed ninety-seven days after the one being
    scored. The crossed four reports are not a bundle and carry no manifest, so
    this is the only place that gate can be applied.
    """
    numbers = scored_run(bundle(tmp_path, PAIRING_EXAMPLE), PAIRING_EXAMPLE)
    supervisor = StandInSupervisor()
    with pytest.raises(ControlError, match=PAIRING_PARTNER_FILED):
        control_shuffled.run(PAIRING_EXAMPLE, PAIRING_PARTNER,
                             numbers_bundle=numbers,
                             notes_bundle=bundle(tmp_path, PAIRING_PARTNER),
                             out=out, predictor=supervisor)
    assert list(out.iterdir()) == []
    assert supervisor.calls == []


def test_a_late_partner_is_refused_with_no_manifest_to_declare_the_filing(tmp_path, out):
    """The route that had no gate at all.

    A pair of report directories carries no manifest, and the cutoff check came
    off with it -- which is the route every crossing test in this file took, on
    a pairing ninety-seven days out. The numbers half's own accession is on
    record with a filing date, so the gate has its date without a manifest.
    """
    supervisor = StandInSupervisor()
    with pytest.raises(ControlError, match=PAIRING_PARTNER_FILED):
        control_shuffled.run(PAIRING_EXAMPLE, PAIRING_PARTNER,
                             numbers_bundle=bundle(tmp_path, PAIRING_EXAMPLE),
                             notes_bundle=bundle(tmp_path, PAIRING_PARTNER),
                             out=out, predictor=supervisor)
    assert list(out.iterdir()) == []
    assert supervisor.calls == []


def test_the_manifest_is_what_declares_the_filing_when_the_run_carries_one(tmp_path, out):
    """The other basis, and the file says which one answered.

    The same pair as the fixture run, with the numbers side made a run directory
    that declares the filing it is scoring. The date is the same date here --
    the manifest and the half's own accession are the same filing -- and what
    differs is which of the two the file says it read.
    """
    numbers = scored_run(bundle(tmp_path, NUMBERS_COMPANY), NUMBERS_COMPANY)
    control_shuffled.run(NUMBERS_COMPANY, NOTES_COMPANY, numbers_bundle=numbers,
                         notes_bundle=bundle(tmp_path, NOTES_COMPANY),
                         out=out, predictor=StandInSupervisor())
    assert sorted(path.name for path in out.iterdir()) == \
           sorted((ACCOUNTING_FILE, PRESSURE_FILE))
    control = written(out, ACCOUNTING_FILE)["control"]
    assert control["scored_filing_date"] == NUMBERS_FILED
    assert control["scored_filing_date_from"] == control_shuffled.MANIFEST_BASIS
    assert control["numbers_from"] == NUMBERS_COMPANY
    assert control["notes_from"] == NOTES_COMPANY


def test_a_manifest_naming_a_filing_its_own_reports_do_not_is_refused(tmp_path, out):
    """The date belongs to the filing the manifest *names*.

    A run directory whose manifest says one accession and whose reports were
    written from another has not said which filing it is, and the cutoff would
    be read off whichever of the two the module happened to look at. The module
    has both in hand, so it refuses instead.
    """
    numbers = bundle(tmp_path, NUMBERS_COMPANY)
    (numbers / control_shuffled.MANIFEST).write_text(
        json.dumps({"ticker": NOTES_COMPANY, "form": "10-K",
                    "accession": NOTES_ACCESSION, "filing_date": NOTES_FILED,
                    "cutoff": NOTES_FILED}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    supervisor = StandInSupervisor()
    with pytest.raises(ControlError) as refusal:
        control_shuffled.run(NUMBERS_COMPANY, NOTES_COMPANY, numbers_bundle=numbers,
                             notes_bundle=bundle(tmp_path, NOTES_COMPANY),
                             out=out, predictor=supervisor)
    assert NOTES_ACCESSION in str(refusal.value)
    assert NUMBERS_ACCESSION in str(refusal.value)
    assert list(out.iterdir()) == []
    assert supervisor.calls == []


def test_a_manifest_naming_no_accession_at_all_is_refused(tmp_path, out):
    """Fail-closed: a date with no filing beside it says nothing about which
    filing it is the date of."""
    numbers = bundle(tmp_path, NUMBERS_COMPANY)
    (numbers / control_shuffled.MANIFEST).write_text(
        json.dumps({"ticker": NUMBERS_COMPANY, "form": "10-K",
                    "filing_date": NUMBERS_FILED, "cutoff": NUMBERS_FILED},
                   indent=2, sort_keys=True) + "\n", encoding="utf-8")
    supervisor = StandInSupervisor()
    with pytest.raises(ControlError, match="names no accession"):
        control_shuffled.run(NUMBERS_COMPANY, NOTES_COMPANY, numbers_bundle=numbers,
                             notes_bundle=bundle(tmp_path, NOTES_COMPANY),
                             out=out, predictor=supervisor)
    assert list(out.iterdir()) == []
    assert supervisor.calls == []


@pytest.mark.parametrize("claimed", ["2025-06-30", "2026-08-01"])
def test_a_manifest_that_disagrees_with_the_record_is_refused(tmp_path, out, claimed):
    """One filing has one date, and the manifest holds it twice.

    The half was checked against the scored date in one direction only, so a
    manifest dated *earlier* than the record was refused and one dated later
    was not -- and later is the direction that loosens the boundary. Claiming
    2026-08-01 for a filing the record files 2026-02-05 admits a notes half
    from any day up to it. `src/assemble_bundle.py` writes `filing_date` out of
    the very record row this reads, so any difference is a run contradicting
    itself.
    """
    assert claimed != NUMBERS_FILED
    numbers = bundle(tmp_path, NUMBERS_COMPANY)
    (numbers / control_shuffled.MANIFEST).write_text(
        json.dumps({"ticker": NUMBERS_COMPANY, "form": "10-K",
                    "accession": NUMBERS_ACCESSION, "filing_date": claimed,
                    "cutoff": claimed}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    supervisor = StandInSupervisor()
    with pytest.raises(ControlError, match="one date") as refusal:
        control_shuffled.run(NUMBERS_COMPANY, NOTES_COMPANY, numbers_bundle=numbers,
                             notes_bundle=bundle(tmp_path, NOTES_COMPANY),
                             out=out, predictor=supervisor)
    assert NUMBERS_FILED in str(refusal.value)
    assert claimed in str(refusal.value)
    assert list(out.iterdir()) == []
    assert supervisor.calls == []


def test_two_companies_reports_on_one_side_are_refused(tmp_path, out):
    """One half is one company's.

    Nothing asked this one either. A side holding one company's numbers report
    beside another's is not a half of one run, and the accession the side is
    dated by would be whichever of the two the set happened to pop.
    """
    mixed = tmp_path / "mixed"
    mixed.mkdir()
    first, second = control_shuffled.NUMBERS_SIDE
    (mixed / first).write_text(report_text(NUMBERS_COMPANY, first), encoding="utf-8")
    (mixed / second).write_text(report_text(NOTES_COMPANY, second), encoding="utf-8")
    supervisor = StandInSupervisor()
    with pytest.raises(ControlError, match="more than one company") as refusal:
        control_shuffled.run(NUMBERS_COMPANY, NOTES_COMPANY, numbers_bundle=mixed,
                             notes_bundle=bundle(tmp_path, NOTES_COMPANY),
                             out=out, predictor=supervisor)
    assert NUMBERS_COMPANY in str(refusal.value)
    assert NOTES_COMPANY in str(refusal.value)
    assert list(out.iterdir()) == []
    assert supervisor.calls == []


def test_a_report_whose_item_ids_begin_with_no_accession_is_refused(tmp_path, out):
    """An empty accession names no filing.

    `filed` looks an accession up in the company's own manifest, and the rows
    there carrying no accession are the submissions index and the companyfacts
    record -- catalogues drawn from many filings, each dated by the newest
    filing in it. A half whose ids begin with nothing would be dated off one of
    those, months after the filing its reports were written from.
    """
    catalogues = [row for row in cutoff_guard.documents(NUMBERS_COMPANY)
                  if not row.get("accession")]
    assert catalogues, "the record holds rows with no accession: the two catalogues"

    numbers = bundle(tmp_path, NUMBERS_COMPANY)
    for name in control_shuffled.NUMBERS_SIDE:
        blanked = (numbers / name).read_text(encoding="utf-8").replace(
            NUMBERS_ACCESSION, "")
        (numbers / name).write_text(blanked, encoding="utf-8")
    supervisor = StandInSupervisor()
    with pytest.raises(ControlError, match="begins with no accession"):
        control_shuffled.run(NUMBERS_COMPANY, NOTES_COMPANY, numbers_bundle=numbers,
                             notes_bundle=bundle(tmp_path, NOTES_COMPANY),
                             out=out, predictor=supervisor)
    assert list(out.iterdir()) == []
    assert supervisor.calls == []


def test_the_four_reports_the_supervisor_sees_go_through_the_pair_check(tmp_path):
    """`crossed` is the function the module docstring calls what the supervisor
    sees, and it used to read the two halves and hand them straight back: the
    one route through here with no cutoff on it and no refusal of a company
    crossed with itself. Nothing outside the module calls it, which is the only
    reason that was never a live leak."""
    with pytest.raises(ControlError, match="real run"):
        control_shuffled.crossed(bundle(tmp_path / "first", NUMBERS_COMPANY),
                                 bundle(tmp_path / "second", NUMBERS_COMPANY))
    with pytest.raises(ControlError, match="Nothing filed after"):
        control_shuffled.crossed(bundle(tmp_path / "rule", PAIRING_EXAMPLE),
                                 bundle(tmp_path / "partner", PAIRING_PARTNER))
    reports = control_shuffled.crossed(bundle(tmp_path, NUMBERS_COMPANY),
                                       bundle(tmp_path, NOTES_COMPANY))
    assert sorted(reports) == sorted(control_shuffled.REPORTS)


# --- what the citations resolve against --------------------------------------

def test_the_planted_citations_are_what_this_file_says_they_are():
    """The control on the two assertions below, read out of the fixture text."""
    assert f"[{UNCROSSED_ITEM}]" in report_text(NUMBERS_COMPANY, "report_notes_text.md")
    crossed = {name: report_text(
        NUMBERS_COMPANY if name in control_shuffled.NUMBERS_SIDE else NOTES_COMPANY,
        name) for name in control_shuffled.REPORTS}
    declared = control_shuffled.declared_ids(crossed)
    assert UNCROSSED_ITEM not in declared
    assert CROSSED_ITEM in declared


def test_an_item_citing_the_notes_report_that_was_taken_away_is_dropped_and_counted(
        tmp_path, out):
    """The sharp form of the citation gate.

    A supervisor pattern-matching AAPL's own run would cite AAPL's own notes
    item, and that item is in none of the four reports it was handed. The entry
    goes whole, the top signal naming it goes with it, and the count says one.
    """
    answers = dict(ANSWERS)
    answers["accounting_reliability"] = dict(
        ACCOUNTING_ANSWER,
        checklist=ACCOUNTING_ANSWER["checklist"] + [
            {"key": "reserve_release_unexplained", "finding": "flag",
             "confidence": 0.7,
             "evidence": [{"upstream_item_id": UNCROSSED_ITEM}]}],
        top_signals=["receivables_growth_outruns_revenue",
                     "reserve_release_unexplained"])
    run_crossed(tmp_path, out, StandInSupervisor(answers))

    accounting = written(out, ACCOUNTING_FILE)
    assert [entry["key"] for entry in accounting["checklist"]] == \
           ["receivables_growth_outruns_revenue"]
    assert accounting["top_signals"] == ["receivables_growth_outruns_revenue"]
    assert accounting["control"]["counts"]["dropped_items"] == 1
    dropped = accounting["control"]["dropped_items"][0]
    assert dropped["item_id"] == \
           "accounting_reliability:checklist:reserve_release_unexplained"
    assert UNCROSSED_ITEM in dropped["reason"]
    # The other question cited nothing that failed, so nothing left it.
    assert written(out, PRESSURE_FILE)["control"]["counts"]["dropped_items"] == 0


def test_a_market_call_resting_on_nothing_in_the_crossed_set_degrades(tmp_path, out):
    """§7 requires the field, so it cannot go: it becomes the abstention §7 allows."""
    answers = dict(ANSWERS)
    answers["accounting_reliability"] = dict(
        ACCOUNTING_ANSWER, market_direction={"p_up": 0.7, "basis": [UNCROSSED_ITEM]})
    run_crossed(tmp_path, out, StandInSupervisor(answers))
    accounting = written(out, ACCOUNTING_FILE)
    assert accounting["market_direction"] == {"p_up": "insufficient", "basis": []}
    assert accounting["control"]["counts"]["dropped_items"] == 1
    assert accounting["control"]["dropped_items"][0]["item_id"] == \
           "accounting_reliability:market_direction"


def test_a_probability_resting_on_an_empty_basis_is_dropped_and_counted(tmp_path, out):
    """`docs/CHECKLIST.md` §7's abstention is `p_up: "insufficient"`, not a
    number with nothing under it. `src/control_single_agent.py` drops that in
    this same sentence, and one schema gets one gate: the field cannot be
    dropped, so it degrades to the abstention and the drop is counted.
    """
    answers = dict(ANSWERS)
    answers["accounting_reliability"] = dict(
        ACCOUNTING_ANSWER, market_direction={"p_up": 0.4, "basis": []})
    run_crossed(tmp_path, out, StandInSupervisor(answers))

    accounting = written(out, ACCOUNTING_FILE)
    assert accounting["market_direction"] == {"p_up": "insufficient", "basis": []}
    dropped = accounting["control"]["dropped_items"]
    assert [row["item_id"] for row in dropped] == \
        ["accounting_reliability:market_direction"]
    assert dropped[0]["reason"] == control_shuffled.CITES_NOTHING
    assert accounting["control"]["counts"]["dropped_items"] == 1


def test_the_abstention_itself_stands_on_an_empty_basis(crossed_run):
    """The one case §7 allows nothing to be resolved: `"insufficient"` resting
    on no basis is the abstention and not a failure, and it is not counted as a
    drop. `PRESSURE_ANSWER` is written that way, so this is the fixture pair's
    own second question."""
    _, _, out = crossed_run
    pressure = written(out, PRESSURE_FILE)
    assert pressure["market_direction"] == PRESSURE_ANSWER["market_direction"]
    assert pressure["market_direction"] == {"p_up": "insufficient", "basis": []}
    assert pressure["control"]["counts"]["dropped_items"] == 0


def test_an_item_citing_nothing_at_all_is_dropped_and_counted(tmp_path, out):
    """CLAUDE.md: a failed item is dropped and counted.

    An entry with no evidence carries neither a quote nor an upstream id, so it
    is a failed item. It used to stand here while the sibling control dropped
    it, which made the difference between the two controls the gate rather than
    the crossing. The sentence is `src/quote_gate.py`'s own, asserted against
    that module below rather than copied into this file twice.
    """
    answers = dict(ANSWERS)
    answers["financial_pressure"] = dict(
        PRESSURE_ANSWER,
        checklist=[{"key": "liquidity_headroom", "finding": "no_flag",
                    "confidence": 0.3, "evidence": []}],
        top_signals=["liquidity_headroom"])
    run_crossed(tmp_path, out, StandInSupervisor(answers))

    pressure = written(out, PRESSURE_FILE)
    assert pressure["checklist"] == []
    assert pressure["top_signals"] == []
    assert pressure["control"]["counts"]["dropped_items"] == 1
    dropped = pressure["control"]["dropped_items"][0]
    assert dropped["item_id"] == "financial_pressure:checklist:liquidity_headroom"
    assert dropped["reason"] == control_shuffled.CITES_NOTHING
    # The other question cited the crossed set, so nothing left it.
    assert written(out, ACCOUNTING_FILE)["control"]["counts"]["dropped_items"] == 0


@pytest.mark.parametrize("shape", [0.7, "up", [0.7], {"p_up": 0.7},
                                   {"p_up": 0.7, "basis": [], "extra": 1}])
def test_a_market_direction_that_is_not_the_schemas_shape_is_refused(
        tmp_path, out, shape):
    """A bare probability is not an abstention.

    The citation gate reads `basis`, so anything with no `basis` to read went
    through it untouched and was written standing with no drop counted. The
    sibling control refuses the shape in its schema check; so does this one.
    """
    answers = dict(ANSWERS)
    answers["accounting_reliability"] = dict(ACCOUNTING_ANSWER,
                                             market_direction=shape)
    supervisor = StandInSupervisor(answers)
    with pytest.raises(ControlError, match="market_direction"):
        run_crossed(tmp_path, out, supervisor)
    assert list(out.iterdir()) == []


def test_an_item_citing_the_notes_half_stands(tmp_path, out):
    """The crossed set is both halves.

    Every citation in this file came out of the numbers half, so indexing only
    that side passed all of them -- in a control whose point is that the two
    halves are two companies'. This cites the notes company's own notes report,
    which the supervisor was handed, and it must stand.
    """
    answers = dict(ANSWERS)
    answers["accounting_reliability"] = dict(
        ACCOUNTING_ANSWER,
        checklist=[{"key": "receivables_growth_outruns_revenue", "finding": "flag",
                    "confidence": 0.6,
                    "evidence": [{"upstream_item_id": NOTES_HALF_ITEM}]}])
    run_crossed(tmp_path, out, StandInSupervisor(answers))
    accounting = written(out, ACCOUNTING_FILE)
    assert accounting["checklist"] == answers["accounting_reliability"]["checklist"]
    assert accounting["control"]["counts"]["dropped_items"] == 0


def test_the_notes_half_item_is_in_the_committed_notes_report():
    """The id above, located in the fixture text rather than taken on trust."""
    text = report_text(NOTES_COMPANY, "report_notes_text.md")
    assert f"[{NOTES_HALF_ITEM}]" in text
    assert NOTES_HALF_ITEM.startswith(NOTES_ACCESSION)


def test_an_explanation_citing_outside_the_crossed_set_is_dropped_and_counted(
        tmp_path, out):
    """`docs/CHECKLIST.md` §7 assembles explanations from what the supervisors
    say about upstream items, so the id names one and resolves like one. It was
    read by nothing here: an explanation naming the notes report the crossing
    took away was written standing and uncounted, which is the same hole the
    sibling control's own ledger item closed."""
    answers = dict(ANSWERS)
    answers["accounting_reliability"] = dict(
        ACCOUNTING_ANSWER,
        explanations=[{"id": UNCROSSED_ITEM, "support": "sufficient",
                       "realization_p": 0.4}])
    run_crossed(tmp_path, out, StandInSupervisor(answers))
    accounting = written(out, ACCOUNTING_FILE)
    assert accounting["explanations"] == []
    dropped = accounting["control"]["dropped_items"]
    assert [row["item_id"] for row in dropped] == \
        [f"accounting_reliability:explanations:{UNCROSSED_ITEM}"]
    assert UNCROSSED_ITEM in dropped[0]["reason"]
    assert accounting["control"]["counts"]["dropped_items"] == 1


def test_an_explanation_citing_the_crossed_set_stands(tmp_path, out):
    """The control on the drop above, from the other half."""
    answers = dict(ANSWERS)
    standing = [{"id": NOTES_HALF_ITEM, "support": "sufficient",
                 "realization_p": 0.4}]
    answers["accounting_reliability"] = dict(ACCOUNTING_ANSWER,
                                             explanations=standing)
    run_crossed(tmp_path, out, StandInSupervisor(answers))
    accounting = written(out, ACCOUNTING_FILE)
    assert accounting["explanations"] == standing
    assert accounting["control"]["counts"]["dropped_items"] == 0


def test_the_sentence_for_citing_nothing_is_the_pipelines_own():
    """The two gates say one thing about one failure.

    Read out of `src/quote_gate.py` by calling it, not copied out of it: the
    sibling control drops an uncited item through `citation_drop_reason`, and
    this control's own constant has to be the sentence that function returns.
    """
    from src import quote_gate
    reason = quote_gate.citation_drop_reason({"id": "an item", "evidence": []}, set())
    assert reason == control_shuffled.CITES_NOTHING


def test_an_item_citing_the_crossed_set_stands(crossed_run):
    """The control on the drop tests: the answer that resolves is written whole."""
    _, _, out = crossed_run
    accounting = written(out, ACCOUNTING_FILE)
    assert accounting["checklist"] == ACCOUNTING_ANSWER["checklist"]
    assert accounting["control"]["counts"]["dropped_items"] == 0
    assert accounting["control"]["dropped_items"] == []


# --- the rest of §7, field by field ------------------------------------------
#
# The gate above reads citations, so every field with no citations in it went
# through untouched: `tier: "banana"`, `events: "lots"`, a bare-string evidence
# entry and two explanations under one id all reached the file standing, with
# `dropped_items: 0` beside them. `docs/CHECKLIST.md` §8 scores market direction
# by Brier and hit rate and events by Brier, so an unscorable value on record is
# a scorecard row that cannot be computed, found months later with nothing left
# to recover.


@pytest.mark.parametrize("p_up", ["up", "0.7", 1.7, -0.1, True, None])
def test_a_market_probability_that_is_not_one_is_refused(tmp_path, out, p_up):
    """§7 gives `p_up` a number in zero to one, or the word `insufficient`.

    `True` is in the list because Python calls it an `int` and `0 <= True <= 1`;
    a scorer reading it as a probability of one is reading an abstention nobody
    wrote.
    """
    answers = dict(ANSWERS)
    answers["accounting_reliability"] = dict(
        ACCOUNTING_ANSWER, market_direction={"p_up": p_up, "basis": [CROSSED_ITEM]})
    with pytest.raises(ControlError, match="p_up"):
        run_crossed(tmp_path, out, StandInSupervisor(answers))
    assert list(out.iterdir()) == []


@pytest.mark.parametrize("basis", [CROSSED_ITEM, [""], ["  "], [CROSSED_ITEM, 7],
                                   {"0": CROSSED_ITEM}])
def test_a_basis_that_is_not_a_list_of_names_is_refused(tmp_path, out, basis):
    """The gate resolves what is in `basis`, and an entry that is not a name
    resolves for nobody -- a bare string is fifty-odd single characters, none of
    which is an item id."""
    answers = dict(ANSWERS)
    answers["accounting_reliability"] = dict(
        ACCOUNTING_ANSWER, market_direction={"p_up": 0.4, "basis": basis})
    with pytest.raises(ControlError, match="basis"):
        run_crossed(tmp_path, out, StandInSupervisor(answers))
    assert list(out.iterdir()) == []


@pytest.mark.parametrize("tier", ["banana", "Elevated", "", None, 1])
def test_a_tier_outside_the_three_is_refused(tmp_path, out, tier):
    """The two-by-two thresholds in `docs/CHECKLIST.md` produce one of three
    words, and a fourth is a row the scorecard has no column for."""
    answers = dict(ANSWERS)
    answers["accounting_reliability"] = dict(ACCOUNTING_ANSWER, tier=tier)
    with pytest.raises(ControlError, match="tier"):
        run_crossed(tmp_path, out, StandInSupervisor(answers))
    assert list(out.iterdir()) == []


@pytest.mark.parametrize("finding", ["yes", "no", "flagged", "", None])
def test_a_checklist_finding_outside_the_three_is_refused(tmp_path, out, finding):
    """`flag`, `no_flag`, `insufficient` -- and the count of insufficient answers
    is reported beside the score, so a fourth word is a denominator nobody can
    reconstruct."""
    answers = dict(ANSWERS)
    answers["accounting_reliability"] = dict(
        ACCOUNTING_ANSWER,
        checklist=[dict(ACCOUNTING_ANSWER["checklist"][0], finding=finding)])
    with pytest.raises(ControlError, match="finding"):
        run_crossed(tmp_path, out, StandInSupervisor(answers))
    assert list(out.iterdir()) == []


@pytest.mark.parametrize("confidence", [1.4, -0.2, "high", None, True])
def test_a_confidence_that_is_not_a_probability_is_refused(tmp_path, out, confidence):
    answers = dict(ANSWERS)
    answers["accounting_reliability"] = dict(
        ACCOUNTING_ANSWER,
        checklist=[dict(ACCOUNTING_ANSWER["checklist"][0], confidence=confidence)])
    with pytest.raises(ControlError, match="confidence"):
        run_crossed(tmp_path, out, StandInSupervisor(answers))
    assert list(out.iterdir()) == []


@pytest.mark.parametrize("cited", [CROSSED_ITEM, [CROSSED_ITEM],
                                   {"upstream_item_id": CROSSED_ITEM, "quote": "x"},
                                   {"quote": CROSSED_ITEM}, {}])
def test_an_evidence_entry_that_is_not_the_schemas_shape_is_refused(
        tmp_path, out, cited):
    """This supervisor's upstream is four reports, so §7's evidence here is an
    `upstream_item_id` and nothing else. A bare string passed the gate, because
    the gate asks each entry for that field and a string answers nothing -- the
    item was dropped for citing nothing, silently turning a malformed entry into
    an uncited one."""
    answers = dict(ANSWERS)
    answers["accounting_reliability"] = dict(
        ACCOUNTING_ANSWER,
        checklist=[dict(ACCOUNTING_ANSWER["checklist"][0], evidence=[cited])])
    with pytest.raises(ControlError, match="evidence"):
        run_crossed(tmp_path, out, StandInSupervisor(answers))
    assert list(out.iterdir()) == []


@pytest.mark.parametrize("events", ["lots", {"restatement": 0.1}, 3])
def test_an_events_field_that_is_not_a_list_is_refused(tmp_path, out, events):
    answers = dict(ANSWERS)
    answers["accounting_reliability"] = dict(ACCOUNTING_ANSWER, events=events)
    with pytest.raises(ControlError, match="events"):
        run_crossed(tmp_path, out, StandInSupervisor(answers))
    assert list(out.iterdir()) == []


@pytest.mark.parametrize("chance", [1.4, -0.1, "likely", None])
def test_an_event_probability_that_is_not_one_is_refused(tmp_path, out, chance):
    """§8 scores events by Brier, and Brier of `"likely"` is not a number."""
    answers = dict(ANSWERS)
    answers["accounting_reliability"] = dict(
        ACCOUNTING_ANSWER,
        events=[{"key": "restatement", "p_within_horizon": chance}])
    with pytest.raises(ControlError, match="p_within_horizon"):
        run_crossed(tmp_path, out, StandInSupervisor(answers))
    assert list(out.iterdir()) == []


def test_two_checklist_entries_under_one_key_are_refused(tmp_path, out):
    """One indicator, one key. Two entries under one key is a set, and the
    scorer reading the first would score a coin flip about which came back."""
    entry = ACCOUNTING_ANSWER["checklist"][0]
    answers = dict(ANSWERS)
    answers["accounting_reliability"] = dict(
        ACCOUNTING_ANSWER, checklist=[entry, dict(entry, finding="no_flag")])
    with pytest.raises(ControlError, match="receivables_growth_outruns_revenue"):
        run_crossed(tmp_path, out, StandInSupervisor(answers))
    assert list(out.iterdir()) == []


def test_two_explanations_under_one_id_are_refused(tmp_path, out):
    """The explanations file is assembled by id, so two under one id is one of
    them silently discarded at assembly."""
    entry = {"id": CROSSED_ITEM, "support": "sufficient", "realization_p": 0.4}
    answers = dict(ANSWERS)
    answers["accounting_reliability"] = dict(
        ACCOUNTING_ANSWER, explanations=[entry, dict(entry, support="unknown")])
    with pytest.raises(ControlError, match="explanations"):
        run_crossed(tmp_path, out, StandInSupervisor(answers))
    assert list(out.iterdir()) == []


@pytest.mark.parametrize("support", ["maybe", "", None, "Sufficient"])
def test_an_explanation_support_outside_the_three_is_refused(tmp_path, out, support):
    answers = dict(ANSWERS)
    answers["accounting_reliability"] = dict(
        ACCOUNTING_ANSWER,
        explanations=[{"id": CROSSED_ITEM, "support": support,
                       "realization_p": 0.4}])
    with pytest.raises(ControlError, match="support"):
        run_crossed(tmp_path, out, StandInSupervisor(answers))
    assert list(out.iterdir()) == []


def test_a_continuous_point_outside_its_own_range_is_refused(tmp_path, out):
    """A point estimate outside the interval it came with is not a wide
    interval, it is two numbers that cannot both be the same prediction."""
    answers = dict(ANSWERS)
    answers["financial_pressure"] = dict(
        PRESSURE_ANSWER,
        continuous=[dict(PRESSURE_ANSWER["continuous"][0], point=200.0)])
    with pytest.raises(ControlError, match="outside its own range"):
        run_crossed(tmp_path, out, StandInSupervisor(answers))
    assert list(out.iterdir()) == []


def test_an_empty_continuous_is_refused(tmp_path, out):
    """Financial pressure predicts next quarter's three numbers; an empty list
    is the field present and the prediction absent."""
    answers = dict(ANSWERS)
    answers["financial_pressure"] = dict(PRESSURE_ANSWER, continuous=[])
    with pytest.raises(ControlError, match="continuous"):
        run_crossed(tmp_path, out, StandInSupervisor(answers))
    assert list(out.iterdir()) == []


def test_more_top_signals_than_the_schema_allows_are_refused(tmp_path, out):
    answers = dict(ANSWERS)
    answers["accounting_reliability"] = dict(
        ACCOUNTING_ANSWER,
        checklist=[dict(ACCOUNTING_ANSWER["checklist"][0], key=f"signal_{n}")
                   for n in range(6)],
        top_signals=[f"signal_{n}" for n in range(6)])
    with pytest.raises(ControlError, match="top_signals"):
        run_crossed(tmp_path, out, StandInSupervisor(answers))
    assert list(out.iterdir()) == []


def test_one_signal_repeated_is_refused(tmp_path, out):
    """Two entries of one key, not six.

    At six the length check fired first, so deleting the uniqueness rule left
    this test green — it was named for a rule it never reached. Two is under
    the ceiling, so only uniqueness can refuse it.
    """
    answers = dict(ANSWERS)
    answers["accounting_reliability"] = dict(
        ACCOUNTING_ANSWER,
        top_signals=["receivables_growth_outruns_revenue"] * 2)
    with pytest.raises(ControlError) as caught:
        run_crossed(tmp_path, out, StandInSupervisor(answers))
    assert "more than once" in str(caught.value)
    assert "receivables_growth_outruns_revenue" in str(caught.value)
    assert list(out.iterdir()) == []


def test_a_signal_naming_no_checklist_item_is_refused(tmp_path, out):
    """The distinction, and which side of it this falls on.

    A signal naming an entry that was *dropped* leaves with it and writes no
    second drop row: that drop is on record under the entry's own key, and
    counting it twice would say two items failed where one did. The test above
    asserts that.

    A signal naming an entry that never existed is not a failed item at all --
    it is the answer contradicting itself before any citation is resolved, and
    `src/control_single_agent.py` refuses the whole prediction for it. This
    control used to drop and count it instead, which made the two controls
    disagree about one schema: one schema gets one gate, and the difference
    between the controls is the crossing and nothing else.
    """
    answers = dict(ANSWERS)
    answers["accounting_reliability"] = dict(
        ACCOUNTING_ANSWER,
        top_signals=["receivables_growth_outruns_revenue", "margin_collapse"])
    with pytest.raises(ControlError) as caught:
        run_crossed(tmp_path, out, StandInSupervisor(answers))
    assert "margin_collapse" in str(caught.value)
    assert "names no entry" in str(caught.value)
    assert list(out.iterdir()) == []


# --- one §7 checker, called by both controls ---------------------------------
#
# `docs/CHECKLIST.md` §7 read by hand, and §1 for the one list §7 leaves blank.
# Not read off either control and not off `src/prediction_schema.py`: a list
# copied out of the code it judges agrees with it by construction. The block,
# as the document prints it:
#
#   { "question": "accounting_reliability" | "financial_pressure",
#     "rules_version": "0.1",
#     "checklist": [ {"key": "", "finding": "", "confidence": 0,
#                     "evidence": [{"upstream_item_id": ""}]} ],
#     "continuous": [ {"key": "", "point": 0, "direction": "", "low": 0, "high": 0} ],
#     "events": [ {"key": "", "p_within_horizon": 0} ],
#     "explanations": [ {"id": "", "support": "sufficient|insufficient|unknown",
#                        "realization_p": 0} ],
#     "market_direction": {"p_up": 0, "basis": []},
#     "tier": "elevated" | "watch" | "clear",
#     "top_signals": [] }
#
# Under it: "`continuous` is financial pressure only. `top_signals` holds at
# most five keys." and "`p_up` may be `"insufficient"` instead of a number".
# §1: "An LLM answer is always `flag` / `no_flag` / `insufficient`".
BY_HAND_FIELDS = ("question", "rules_version", "checklist", "continuous", "events",
                  "explanations", "market_direction", "tier", "top_signals")
BY_HAND_QUESTIONS = ("accounting_reliability", "financial_pressure")
BY_HAND_CHECKLIST = ("key", "finding", "confidence", "evidence")
BY_HAND_EVIDENCE = ("upstream_item_id",)
BY_HAND_CONTINUOUS = ("key", "point", "direction", "low", "high")
BY_HAND_EVENTS = ("key", "p_within_horizon")
BY_HAND_EXPLANATIONS = ("id", "support", "realization_p")
BY_HAND_MARKET = ("p_up", "basis")
BY_HAND_FINDINGS = ("flag", "no_flag", "insufficient")
BY_HAND_SUPPORT = ("sufficient", "insufficient", "unknown")
BY_HAND_TIERS = ("elevated", "watch", "clear")
BY_HAND_SIGNAL_CEILING = 5


def test_the_one_checker_holds_what_section_seven_says():
    """The values the checker holds, against §7 as a person reads it.

    This stood as two controls' constants asserted equal to each other, which
    is a test standing in for a function: both could be wrong the same way and
    agree. There is one copy now, and it is held against the document.
    """
    assert prediction_schema.QUESTIONS == BY_HAND_QUESTIONS
    # `question` and `rules_version` are the run's, `continuous` is one
    # question's, and the rest is what every answer carries: nine between them.
    assert prediction_schema.RUN_KEYS == ("question", "rules_version")
    assert prediction_schema.CONTINUOUS == "continuous"
    assert prediction_schema.CONTINUOUS_QUESTION == "financial_pressure"
    assert sorted(prediction_schema.RUN_KEYS + prediction_schema.PREDICTED_KEYS
                  + (prediction_schema.CONTINUOUS,)) == sorted(BY_HAND_FIELDS)
    assert prediction_schema.CHECKLIST_FIELDS == BY_HAND_CHECKLIST
    assert prediction_schema.EVIDENCE_FIELDS == BY_HAND_EVIDENCE
    assert prediction_schema.CONTINUOUS_FIELDS == BY_HAND_CONTINUOUS
    assert prediction_schema.EVENT_FIELDS == BY_HAND_EVENTS
    assert prediction_schema.EXPLANATION_FIELDS == BY_HAND_EXPLANATIONS
    assert prediction_schema.MARKET_FIELDS == BY_HAND_MARKET
    assert prediction_schema.FINDINGS == BY_HAND_FINDINGS
    assert prediction_schema.SUPPORT == BY_HAND_SUPPORT
    assert prediction_schema.TIERS == BY_HAND_TIERS
    assert prediction_schema.TOP_SIGNALS_MAX == BY_HAND_SIGNAL_CEILING
    assert prediction_schema.INSUFFICIENT == "insufficient"


def schema_refuses(answer, question="accounting_reliability",
                   evidence=BY_HAND_EVIDENCE) -> str | None:
    """The one checker's refusal of an answer, or None when it stands."""
    try:
        prediction_schema.check(answer, question, evidence=evidence)
    except prediction_schema.SchemaError as refused:
        return str(refused)
    return None


def test_the_one_checker_takes_every_value_section_seven_allows_and_nothing_beside():
    """Equal constants are not a gate; what the function does with them is.

    Every value §7 and §1 allow stands, one at a time, and the first value
    beside them is refused -- so a list the checker holds and then never
    consults, or consults against the wrong field, turns this red.
    """
    good = dict(ACCOUNTING_ANSWER)
    assert schema_refuses(good) is None, "the good answer is the baseline"
    assert schema_refuses(dict(PRESSURE_ANSWER), "financial_pressure") is None

    entry = good["checklist"][0]
    for finding in BY_HAND_FINDINGS:
        assert schema_refuses(dict(good, checklist=[dict(entry, finding=finding)])) \
            is None, finding
    assert "finding" in schema_refuses(dict(good, checklist=[dict(entry, finding="yes")]))

    for support in BY_HAND_SUPPORT:
        explained = [{"id": CROSSED_ITEM, "support": support, "realization_p": 0.4}]
        assert schema_refuses(dict(good, explanations=explained)) is None, support
    assert "support" in schema_refuses(dict(good, explanations=[
        {"id": CROSSED_ITEM, "support": "maybe", "realization_p": 0.4}]))

    for tier in BY_HAND_TIERS:
        assert schema_refuses(dict(good, tier=tier)) is None, tier
    assert "tier" in schema_refuses(dict(good, tier="alert"))

    def signalled(count: int) -> dict:
        keys = [f"signal_{n}" for n in range(count)]
        return dict(good, checklist=[dict(entry, key=key) for key in keys],
                    top_signals=keys)
    assert schema_refuses(signalled(BY_HAND_SIGNAL_CEILING)) is None
    assert f"at most {BY_HAND_SIGNAL_CEILING}" in \
        schema_refuses(signalled(BY_HAND_SIGNAL_CEILING + 1))

    assert schema_refuses(dict(good, market_direction={
        "p_up": "insufficient", "basis": []})) is None
    assert "p_up" in schema_refuses(dict(good, market_direction={
        "p_up": "unsure", "basis": []}))

    # "`continuous` is financial pressure only": asked of one question,
    # refused on the other.
    assert "has no continuous" in schema_refuses(
        {key: value for key, value in PRESSURE_ANSWER.items() if key != "continuous"},
        "financial_pressure")
    assert "carries continuous" in schema_refuses(
        dict(good, continuous=PRESSURE_ANSWER["continuous"]))

    # A field of every nested object, taken away, is named.
    for field, broken in (
            ("confidence", dict(good, checklist=[
                {k: v for k, v in entry.items() if k != "confidence"}])),
            ("p_within_horizon", dict(good, events=[{"key": "restatement"}])),
            ("realization_p", dict(good, explanations=[
                {"id": CROSSED_ITEM, "support": "unknown"}])),
            ("basis", dict(good, market_direction={"p_up": 0.4})),
            ("high", dict(PRESSURE_ANSWER, continuous=[
                {k: v for k, v in PRESSURE_ANSWER["continuous"][0].items()
                 if k != "high"}]))):
        question = "financial_pressure" if "continuous" in broken else \
            "accounting_reliability"
        said = schema_refuses(broken, question)
        assert said is not None and field in said, field


def test_evidence_is_the_one_field_the_caller_names():
    """The two controls differ on `evidence` and on nothing else, so it is the
    argument -- and the argument may add to §7's shape, never take from it.

    The single-agent control's upstream is the committed filing, so its ids
    name paragraphs and a quote travels with each; the shuffled control's
    upstream is four reports, and §7's own member is the whole of it.
    """
    plain = dict(ACCOUNTING_ANSWER)
    quoted = dict(plain, checklist=[dict(plain["checklist"][0], evidence=[
        {"upstream_item_id": CROSSED_ITEM, "quote": "a sentence"}])])
    with_quote = BY_HAND_EVIDENCE + ("quote",)

    assert schema_refuses(plain, evidence=BY_HAND_EVIDENCE) is None
    assert schema_refuses(quoted, evidence=with_quote) is None
    # Each shape is refused under the other's argument, naming the member.
    assert "quote" in schema_refuses(quoted, evidence=BY_HAND_EVIDENCE)
    assert "quote" in schema_refuses(plain, evidence=with_quote)
    # The member a caller adds is held to be a name like §7's own.
    blank = dict(plain, checklist=[dict(plain["checklist"][0], evidence=[
        {"upstream_item_id": CROSSED_ITEM, "quote": "  "}])])
    assert "evidence[1].quote" in schema_refuses(blank, evidence=with_quote)
    # An argument leaving out §7's own member is refused, whatever the answer.
    said = schema_refuses(quoted, evidence=("quote",))
    assert said is not None and "leaves out upstream_item_id" in said


def test_the_shuffled_control_answers_through_the_one_checker(tmp_path, out, monkeypatch):
    """Called, not copied: the production path reaches the one checker once per
    question, with §7's own evidence shape, and the file it writes is what that
    checker let through.

    A copy of the check kept here beside a call nobody makes would pass every
    schema test in this file and this one would still fail.
    """
    calls = []
    real = prediction_schema.check

    def recording(answer, question, *, evidence):
        calls.append((question, evidence, sorted(answer)))
        return real(answer, question, evidence=evidence)

    monkeypatch.setattr(prediction_schema, "check", recording)
    run_crossed(tmp_path, out, StandInSupervisor())
    assert calls == [
        ("accounting_reliability", BY_HAND_EVIDENCE,
         sorted(set(BY_HAND_FIELDS) - {"question", "rules_version", "continuous"})),
        ("financial_pressure", BY_HAND_EVIDENCE,
         sorted(set(BY_HAND_FIELDS) - {"question", "rules_version"})),
    ]


def test_a_refusal_from_the_one_checker_is_the_controls_refusal(tmp_path, out,
                                                                 monkeypatch):
    """Whatever the one checker refuses, this control refuses in its own error
    type and writes nothing -- the refusal is not lost on the way back."""
    def refusing(answer, question, *, evidence):
        raise prediction_schema.SchemaError("the one checker refused this")

    monkeypatch.setattr(prediction_schema, "check", refusing)
    with pytest.raises(ControlError, match="the one checker refused this"):
        run_crossed(tmp_path, out, StandInSupervisor())
    assert list(out.iterdir()) == []


def test_neither_control_writes_out_a_section_seven_list_of_its_own():
    """The lists are written once, in `src/prediction_schema.py`.

    Read off each control's source rather than asked of its attributes: a copy
    under a new name is still a copy, and the next one to drift.
    """
    import ast
    by_hand = {BY_HAND_CHECKLIST, BY_HAND_EVIDENCE, BY_HAND_CONTINUOUS,
               BY_HAND_EVENTS, BY_HAND_EXPLANATIONS, BY_HAND_MARKET,
               BY_HAND_FINDINGS, BY_HAND_SUPPORT, BY_HAND_TIERS}
    for name in ("control_single_agent.py", "control_shuffled.py"):
        tree = ast.parse((REPO_ROOT / "src" / name).read_text(encoding="utf-8"))
        written = {tuple(element.value for element in node.elts)
                   for node in ast.walk(tree)
                   if isinstance(node, (ast.Tuple, ast.List)) and node.elts
                   and all(isinstance(element, ast.Constant)
                           and isinstance(element.value, str)
                           for element in node.elts)}
        assert not written & by_hand, f"{name} writes out {sorted(written & by_hand)}"


def section_seven() -> dict:
    """§7's prediction schema, parsed out of `docs/CHECKLIST.md` as JSON.

    The block in the document is not JSON -- three fields give their values as
    `"a" | "b"` unions -- so each union is collapsed into the one `|`-joined
    string §7 already uses for `support`. Nothing else is rewritten, and a
    document whose §7 block stops being parseable fails here rather than
    quietly falling back to what the module says.
    """
    document = (REPO_ROOT / "docs" / "CHECKLIST.md").read_text(encoding="utf-8")
    heading = document.index("## 7. Output schemas")
    block = document.index("```json", heading) + len("```json")
    pseudo = document[block:document.index("```", block)]
    real = re.sub(r'"[^"\n]*"(?:\s*\|\s*"[^"\n]*")+',
                  lambda union: '"%s"' % "|".join(
                      found.strip('"') for found in re.findall(r'"[^"\n]*"', union.group(0))),
                  pseudo)
    return json.loads(real)


def test_the_section_seven_value_lists_are_the_documents_own():
    """The lists read off §7 itself, not off the other module.

    The tests above hold the one checker against §7 as a person reads it. This
    one parses the document instead, so the day §7 moves and the hand reading
    above is not updated, the two disagree here rather than both going quietly
    stale. Everything comes out of `docs/CHECKLIST.md`: the field sets out of
    §7's own block, the three closed value lists out of the strings inside it
    and out of §1's sentence, and the ceiling out of the prose under the block.
    """
    schema = section_seven()
    # The keys, in §7's order. `question` and `rules_version` are the module's
    # own to write and `continuous` is asked of one question only, so those
    # three are named here rather than counted in.
    assert tuple(name for name in schema
                 if name not in prediction_schema.RUN_KEYS + (prediction_schema.CONTINUOUS,)
                 ) == prediction_schema.PREDICTED_KEYS
    assert tuple(name for name in schema if name in prediction_schema.RUN_KEYS) == \
        prediction_schema.RUN_KEYS
    assert prediction_schema.CONTINUOUS in schema
    assert tuple(schema["question"].split("|")) == prediction_schema.QUESTIONS
    assert tuple(schema["question"].split("|")) == control_shuffled.QUESTIONS
    assert schema["rules_version"] == control_shuffled.RULES_VERSION

    # Every nested entry's closed field set, and the evidence inside the
    # checklist entry rather than beside it.
    assert tuple(schema["checklist"][0]) == prediction_schema.CHECKLIST_FIELDS
    assert tuple(schema["checklist"][0]["evidence"][0]) == \
        prediction_schema.EVIDENCE_FIELDS
    assert tuple(schema["continuous"][0]) == prediction_schema.CONTINUOUS_FIELDS
    assert tuple(schema["events"][0]) == prediction_schema.EVENT_FIELDS
    assert tuple(schema["explanations"][0]) == prediction_schema.EXPLANATION_FIELDS
    assert tuple(schema["market_direction"]) == prediction_schema.MARKET_FIELDS

    # The two closed lists §7 spells out inside the block, and the one it
    # leaves empty there: `"finding": ""` says nothing, so the findings are §1's
    # sentence, which is the only place the three are written down.
    assert tuple(schema["tier"].split("|")) == prediction_schema.TIERS
    assert tuple(schema["explanations"][0]["support"].split("|")) == \
        prediction_schema.SUPPORT
    collapsed = " ".join(
        (REPO_ROOT / "docs" / "CHECKLIST.md").read_text(encoding="utf-8").split())
    said = re.search(r"An LLM answer is always (.+?), plus a confidence", collapsed)
    assert said, "docs/CHECKLIST.md §1 no longer says what an LLM answer is"
    assert tuple(one.strip(" `") for one in said.group(1).split("/")) == \
        prediction_schema.FINDINGS

    # The ceiling and the abstention, out of the prose under the block.
    assert "`top_signals` holds at most five keys" in collapsed
    assert prediction_schema.TOP_SIGNALS_MAX == 5
    assert '`p_up` may be `"insufficient"` instead of a number' in collapsed
    assert prediction_schema.INSUFFICIENT == "insufficient"


# --- the refusals that had no judge ------------------------------------------
#
# Every one of these survived a fail-open mutation with the file green, and they
# sit on the cutoff and identity path this control is about. The pattern is one
# input each, built out of the committed fixture pair, and the sentence named.


def test_a_report_of_the_wrong_kind_under_the_right_name_is_refused(tmp_path, out):
    """"Verify the reports it crossed" is company, filing **and** kind.

    Only the *name* of a file said which of the four reports it held. A file
    called `report_notes_text.md` holding the numbers report crossed with
    everything else checking out — one company, one filing, both halves inside
    the cutoff — and the supervisor was handed one company's numbers twice under
    two names, which is not the crossing and is not the pipeline either.
    """
    notes = bundle(tmp_path, NOTES_COMPANY)
    (notes / "report_notes_text.md").write_text(
        report_text(NOTES_COMPANY, "report_numbers.md"), encoding="utf-8")
    with pytest.raises(ControlError) as caught:
        control_shuffled.run(NUMBERS_COMPANY, NOTES_COMPANY,
                             numbers_bundle=bundle(tmp_path, NUMBERS_COMPANY),
                             notes_bundle=notes, out=out,
                             predictor=StandInSupervisor())
    assert "report_notes_text.md" in str(caught.value)
    assert "notes-text reader" in str(caught.value)
    assert list(out.iterdir()) == []


def test_the_heading_this_file_expects_is_the_one_every_committed_report_carries():
    """The map read against the source rather than agreed with.

    `REPORT_HEADING` is written out by hand in `src/control_shuffled.py`, so it
    is checked against all twenty-four committed reports here — both companies
    of the pair, every report, first line. A map agreeing only with itself is
    the hand-written list on both sides this project has been burned by.
    """
    for ticker in (NUMBERS_COMPANY, NOTES_COMPANY):
        for name in control_shuffled.REPORTS:
            first = report_text(ticker, name).split("\n", 1)[0].strip()
            assert first == f"# {ticker} — {control_shuffled.REPORT_HEADING[name]}"
    assert sorted(control_shuffled.REPORT_HEADING) == sorted(control_shuffled.REPORTS)


def test_a_report_carrying_no_item_id_is_refused(tmp_path, out):
    """A half that names no filing cannot be dated, and an undatable half is the
    cutoff not applying to it."""
    notes = bundle(tmp_path, NOTES_COMPANY)
    stripped = "\n".join(
        line for line in report_text(NOTES_COMPANY, "report_notes_text.md").split("\n")
        if not (line.strip().startswith("[") and line.strip().endswith("]")))
    (notes / "report_notes_text.md").write_text(stripped, encoding="utf-8")
    with pytest.raises(ControlError) as caught:
        control_shuffled.run(NUMBERS_COMPANY, NOTES_COMPANY,
                             numbers_bundle=bundle(tmp_path, NUMBERS_COMPANY),
                             notes_bundle=notes, out=out,
                             predictor=StandInSupervisor())
    assert "carries no item id" in str(caught.value)
    assert list(out.iterdir()) == []


def test_a_report_with_no_heading_is_refused(tmp_path, out):
    """Nothing in it says whose half it is, and the label the caller passed is
    the caller's word — which is the thing the heading exists to check."""
    notes = bundle(tmp_path, NOTES_COMPANY)
    body = report_text(NOTES_COMPANY, "report_notes_text.md").split("\n", 1)[1]
    (notes / "report_notes_text.md").write_text(body, encoding="utf-8")
    with pytest.raises(ControlError) as caught:
        control_shuffled.run(NUMBERS_COMPANY, NOTES_COMPANY,
                             numbers_bundle=bundle(tmp_path, NUMBERS_COMPANY),
                             notes_bundle=notes, out=out,
                             predictor=StandInSupervisor())
    assert "does not open with a heading" in str(caught.value)
    assert list(out.iterdir()) == []


def test_a_heading_naming_a_thirteenth_company_is_refused(tmp_path, out):
    """The twelve are the whole population, and the heading is where a report
    says which of them it is about.

    `run` reads its two *labels* through `one_of_the_twelve` and that call has a
    judge below. The call inside `named_company` reads what the report itself
    says, and had none -- it is a bare call to a plain function, so neither of
    the mutation probe's two patterns could even enumerate it. A half headed
    `# ZZZZ` was placed by the caller's label while the heading it is checked
    against named a company with no reports on record, no pairing, and no
    scorecard row to be scored on.
    """
    notes = bundle(tmp_path, NOTES_COMPANY)
    first, rest = report_text(NOTES_COMPANY, "report_notes_text.md").split("\n", 1)
    (notes / "report_notes_text.md").write_text(
        first.replace(NOTES_COMPANY, "ZZZZ", 1) + "\n" + rest, encoding="utf-8")
    with pytest.raises(ControlError) as caught:
        control_shuffled.run(NUMBERS_COMPANY, NOTES_COMPANY,
                             numbers_bundle=bundle(tmp_path, NUMBERS_COMPANY),
                             notes_bundle=notes, out=out,
                             predictor=StandInSupervisor())
    assert "ZZZZ is not one of the twelve" in str(caught.value)
    for ticker in control_shuffled.PAIRING_ORDER:
        assert ticker in str(caught.value)
    assert list(out.iterdir()) == []


def test_a_heading_naming_its_company_in_lower_case_is_that_company(tmp_path, out):
    """The other half of the same call: the case of the heading is not a company.

    `one_of_the_twelve` upper-cases before it looks, so `# carr` is Carrier's
    report and the run goes through. Without a judge on the accepting side, the
    refusal above stands whether the upper-casing is there or not -- and with it
    gone every lower-case heading becomes a thirteenth company. What the control
    file records is the heading read through that call, not the label the caller
    passed, so the assertion is on `numbers_from` in the written file.
    """
    numbers = bundle(tmp_path, NUMBERS_COMPANY)
    for name in control_shuffled.NUMBERS_SIDE:
        first, rest = report_text(NUMBERS_COMPANY, name).split("\n", 1)
        (numbers / name).write_text(
            first.replace(NUMBERS_COMPANY, NUMBERS_COMPANY.lower(), 1) + "\n" + rest,
            encoding="utf-8")
    control_shuffled.run(NUMBERS_COMPANY, NOTES_COMPANY,
                         numbers_bundle=numbers,
                         notes_bundle=bundle(tmp_path, NOTES_COMPANY),
                         out=out, predictor=StandInSupervisor())
    for name in (ACCOUNTING_FILE, PRESSURE_FILE):
        assert written(out, name)["control"]["numbers_from"] == NUMBERS_COMPANY


def test_two_filings_on_one_side_are_refused(tmp_path, out):
    """One half is one run's. A side holding items from two filings is two runs
    spliced, and `named_accession` is the only thing that says so — deleting it
    left the file green."""
    notes = bundle(tmp_path, NOTES_COMPANY)
    text = report_text(NOTES_COMPANY, "report_notes_text.md")
    # The numbers company's own filing, spliced into the notes company's half:
    # two accessions in one report, which is two runs spliced.
    other = NUMBERS_ACCESSION
    (notes / "report_notes_text.md").write_text(
        text + f"\n[{other}:notes:receivables:9]\nA later paragraph.\n",
        encoding="utf-8")
    with pytest.raises(ControlError) as caught:
        control_shuffled.run(NUMBERS_COMPANY, NOTES_COMPANY,
                             numbers_bundle=bundle(tmp_path, NUMBERS_COMPANY),
                             notes_bundle=notes, out=out,
                             predictor=StandInSupervisor())
    assert "carries items from" in str(caught.value)
    assert other in str(caught.value)
    assert list(out.iterdir()) == []


def test_a_half_whose_accession_no_manifest_records_is_refused(tmp_path, out):
    """The load-bearing fail-closed direction of the whole gate.

    `filed` is what dates a half. Mutated to answer `1900-01-01` for an
    accession no manifest holds, the file stayed green: nothing asked what it
    does when the record has never heard of the filing, and an absent date is
    not an early date.

    The invented accession goes into **both** reports on the side. Putting it in
    one left the side holding two accessions, which `_half` refuses first — so
    the test was named for `filed` and never reached it, and the refusal it
    asserted was the neighbouring rule's. That is the same defect this commit
    fixed in two other tests, made once more while fixing them.
    """
    notes = bundle(tmp_path, NOTES_COMPANY)
    invented = "9999999999-99-999999"
    for name in control_shuffled.NOTES_SIDE:
        (notes / name).write_text(
            report_text(NOTES_COMPANY, name).replace(NOTES_ACCESSION, invented),
            encoding="utf-8")
    with pytest.raises(ControlError) as caught:
        control_shuffled.run(NUMBERS_COMPANY, NOTES_COMPANY,
                             numbers_bundle=bundle(tmp_path, NUMBERS_COMPANY),
                             notes_bundle=notes, out=out,
                             predictor=StandInSupervisor())
    assert "no manifest records" in str(caught.value)
    assert invented in str(caught.value)
    assert list(out.iterdir()) == []


def test_two_reports_on_one_side_naming_two_filings_are_refused(tmp_path, out):
    """One half is one run's, across its two files and not only inside each.

    `named_accession` refuses two filings inside one report and had a judge;
    `_half` refuses two filings across the side's two reports and had none —
    while it sits on the cutoff path. With it gone, a side whose notes-text
    report is Apple's and whose notes-versus-market report is Carrier's own
    filing being scored is accepted, the control file records only the first
    accession, and the second filing is dated against nothing at all. Which of
    the two leaks depends on the order of `NOTES_SIDE`, which is not a thing to
    rest a boundary on.
    """
    notes = bundle(tmp_path, NOTES_COMPANY)
    (notes / "report_notes_vs_market.md").write_text(
        report_text(NOTES_COMPANY, "report_notes_vs_market.md")
        .replace(NOTES_ACCESSION, NUMBERS_ACCESSION), encoding="utf-8")
    with pytest.raises(ControlError) as caught:
        control_shuffled.run(NUMBERS_COMPANY, NOTES_COMPANY,
                             numbers_bundle=bundle(tmp_path, NUMBERS_COMPANY),
                             notes_bundle=notes, out=out,
                             predictor=StandInSupervisor())
    said = str(caught.value)
    assert "more than one filing on one side" in said
    assert NUMBERS_ACCESSION in said and NOTES_ACCESSION in said
    assert list(out.iterdir()) == []


@pytest.mark.parametrize("damage", ["not json", "not an object", "no filing date"])
def test_a_manifest_that_says_nothing_readable_is_refused(tmp_path, out, damage):
    """A broken record is refused, because an absent date is not an early date.

    Each of the three refusals could be turned into `return None` with the file
    green — and `None` is the branch that skips both manifest cross-checks, the
    two rules that stop a run's own manifest from setting its own boundary. The
    fallback date is the numbers half's own record date, so this is not a live
    leak; it is the module's stated rule asserted by nothing.
    """
    numbers = bundle(tmp_path, NUMBERS_COMPANY)
    body = {"not json": "{not json at all",
            "not an object": "[]",
            "no filing date": json.dumps({"accession": NUMBERS_ACCESSION})}[damage]
    (numbers / "input_manifest.json").write_text(body, encoding="utf-8")
    with pytest.raises(ControlError) as caught:
        control_shuffled.run(NUMBERS_COMPANY, NOTES_COMPANY,
                             numbers_bundle=numbers,
                             notes_bundle=bundle(tmp_path, NOTES_COMPANY),
                             out=out, predictor=StandInSupervisor())
    assert "input_manifest.json" in str(caught.value)
    assert list(out.iterdir()) == []


def test_an_output_that_is_not_a_directory_is_refused(tmp_path):
    """A control file has a directory to land in, or the run does not start."""
    not_a_directory = tmp_path / "out.txt"
    not_a_directory.write_text("", encoding="utf-8")
    with pytest.raises(ControlError):
        control_shuffled.run(NUMBERS_COMPANY, NOTES_COMPANY,
                             numbers_bundle=bundle(tmp_path, NUMBERS_COMPANY),
                             notes_bundle=bundle(tmp_path, NOTES_COMPANY),
                             out=not_a_directory,
                             predictor=StandInSupervisor())


# --- where the control files may land, and what one run is -------------------
#
# The expected values are read off the documents and off a check that predates
# this control's rule, never off the control. `docs/INPUT_SPEC.md` §6 lists
# `control_shuffled_accounting.json` and `control_shuffled_pressure.json` in the
# committed bundle under `runs/{ticker}/{accession}/`, and says in the same
# paragraph that "each agent's input directory is committed as what it saw, and
# the directory is the isolation boundary"; `docs/HOW_WE_WORK.md` §1.6 says it
# again. `src/agent_inputs.py` is that boundary as directories, and its
# `isolation_violations` is what says a tree is broken -- asked here before and
# after, and asked once more with a control file put where the refusal kept one
# out, so the refusal is shown to have prevented something that check calls a
# break rather than something this file calls one.
#
# The run a directory is, is the manifest it committed: `src/assemble_bundle.py`
# writes the triggering report's accession into `input_manifest.json` and files
# the run under that accession. A copy of a run carries the same manifest at a
# different path, and a link carries it at a path that resolves to the first;
# the path said a copy was two runs and a link one.

OUTSIDE_THE_BOUNDARY = "per-agent input"
ONE_RUN = "one run"


def another_run(tmp_path: Path) -> Path:
    """A run beside the pair, with its accounting supervisor's directory built.

    Built by `src/agent_inputs.py` itself, so the directory the control is
    pointed into is one the layer table made and not one this file shaped.
    """
    other = bundle(tmp_path / "another", NOTES_COMPANY)
    agent_inputs.build(other, "supervisor-accounting")
    assert agent_inputs.isolation_violations(other) == []
    return other


@pytest.mark.parametrize("where", ["a supervisor's own directory",
                                   "the directory the six sit in",
                                   "a link into a supervisor's directory"])
def test_a_control_pointed_inside_another_runs_input_tree_is_refused(tmp_path, where):
    other = another_run(tmp_path)
    held = agent_inputs.session_root(other, "supervisor-accounting")
    if where == "the directory the six sit in":
        held = agent_inputs.agents_root(other)
    target = held
    if where == "a link into a supervisor's directory":
        target = tmp_path / "looks-like-a-run"
        target.symlink_to(held, target_is_directory=True)
    supervisor = StandInSupervisor()
    with pytest.raises(ControlError) as refusal:
        control_shuffled.run(NUMBERS_COMPANY, NOTES_COMPANY,
                             numbers_bundle=bundle(tmp_path, NUMBERS_COMPANY),
                             notes_bundle=bundle(tmp_path, NOTES_COMPANY),
                             out=target, predictor=supervisor)
    assert OUTSIDE_THE_BOUNDARY in str(refusal.value)
    assert str(held.resolve()) in str(refusal.value)
    assert supervisor.calls == []
    assert agent_inputs.isolation_violations(other) == []
    # What the refusal kept out, put there by hand: the boundary check that
    # predates this rule calls the tree broken.
    (held / ACCOUNTING_FILE).write_text("{}\n", encoding="utf-8")
    assert agent_inputs.isolation_violations(other) != []


def test_a_control_file_that_is_a_link_out_of_the_output_is_refused(tmp_path, out):
    """The directory can be right and the file still land somewhere else.

    `write_text` follows a link, and a link whose target does not exist yet is
    not a file, so the "already on record" check reads it as absent and the
    write creates the target -- here, inside another run's supervisor directory.
    The sibling control refuses a link at its file name in the same words.
    """
    other = another_run(tmp_path)
    inside = agent_inputs.session_root(other, "supervisor-accounting") / ACCOUNTING_FILE
    (out / ACCOUNTING_FILE).symlink_to(inside)
    supervisor = StandInSupervisor()
    with pytest.raises(ControlError, match="never through a link"):
        run_crossed(tmp_path, out, supervisor)
    assert not inside.exists()
    assert supervisor.calls == []
    assert agent_inputs.isolation_violations(other) == []


def test_an_output_that_is_another_run_is_refused(tmp_path):
    """The control files are the scored run's, so they land in the scored run.

    §6 lists them in the bundle of one run, and §8 makes that run company A's:
    the numbers side is the company being scored. Written into the partner's
    run, they sit under the two names §6 gives the partner's *own* shuffled
    control, and the partner's run can then never be given its own.
    """
    partner = scored_run(bundle(tmp_path / "partner-run", NOTES_COMPANY), NOTES_COMPANY)
    supervisor = StandInSupervisor()
    with pytest.raises(ControlError) as refusal:
        run_crossed(tmp_path, partner, supervisor)
    assert NOTES_ACCESSION in str(refusal.value)
    assert NUMBERS_ACCESSION in str(refusal.value)
    assert supervisor.calls == []
    assert sorted(partner.glob("control_*")) == []


def test_a_copy_of_the_scored_run_is_where_its_control_may_land(tmp_path):
    """The positive side of the rule above, and the reason it reads a manifest.

    A rule reading paths would refuse this: the output is not the directory the
    numbers half was read out of. It is the same run, by the manifest it
    carries, and the files land in it.
    """
    numbers = scored_run(bundle(tmp_path, NUMBERS_COMPANY), NUMBERS_COMPANY)
    copy = Path(shutil.copytree(numbers, tmp_path / "the-same-run-elsewhere"))
    control_shuffled.run(NUMBERS_COMPANY, NOTES_COMPANY, numbers_bundle=numbers,
                         notes_bundle=bundle(tmp_path, NOTES_COMPANY),
                         out=copy, predictor=StandInSupervisor())
    assert written(copy, ACCOUNTING_FILE)["control"]["numbers_accession"] == \
           NUMBERS_ACCESSION
    assert (copy / PRESSURE_FILE).is_file()


@pytest.mark.parametrize("how", ["a copy", "a link"])
def test_the_scored_run_again_is_one_run_whatever_path_it_sits_at(tmp_path, out, how):
    """A copy made two and a link made one; by the manifest both are one.

    The copy carries the partner's two notes reports in place of its own, so
    every other check on the pair passes -- two companies, two filings, the
    notes half filed before the scored one -- and the only thing wrong is that
    the notes half is, by the manifest it committed, the run being scored. The
    path said it was a second run, and the pair was crossed and written.
    """
    numbers = scored_run(bundle(tmp_path, NUMBERS_COMPANY), NUMBERS_COMPANY)
    again = tmp_path / "again"
    if how == "a copy":
        shutil.copytree(numbers, again)
        for name in control_shuffled.NOTES_SIDE:
            (again / name).write_text(report_text(NOTES_COMPANY, name), encoding="utf-8")
    else:
        again.symlink_to(numbers, target_is_directory=True)
    supervisor = StandInSupervisor()
    with pytest.raises(ControlError) as refusal:
        control_shuffled.run(NUMBERS_COMPANY, NOTES_COMPANY, numbers_bundle=numbers,
                             notes_bundle=again, out=out, predictor=supervisor)
    assert ONE_RUN in str(refusal.value)
    assert NUMBERS_ACCESSION in str(refusal.value)
    assert supervisor.calls == []
    assert list(out.iterdir()) == []


def test_a_notes_half_whose_manifest_names_another_filing_is_refused(tmp_path, out):
    """A half's run is its manifest, so the manifest has to be the half's own.

    The numbers side has refused this since the cutoff was bound; the notes side
    never read its manifest at all. Without it, the manifest a notes half
    carries could name any run, and "which run the half came from" would be
    whatever it said.
    """
    elsewhere = annual("NVDA")
    notes = bundle(tmp_path, NOTES_COMPANY)
    (notes / control_shuffled.MANIFEST).write_text(
        json.dumps({"ticker": "NVDA", "form": "10-K",
                    "accession": elsewhere["accession"],
                    "filing_date": elsewhere["filing_date"],
                    "cutoff": elsewhere["filing_date"]},
                   indent=2, sort_keys=True) + "\n", encoding="utf-8")
    supervisor = StandInSupervisor()
    with pytest.raises(ControlError) as refusal:
        control_shuffled.run(NUMBERS_COMPANY, NOTES_COMPANY,
                             numbers_bundle=bundle(tmp_path, NUMBERS_COMPANY),
                             notes_bundle=notes, out=out, predictor=supervisor)
    assert elsewhere["accession"] in str(refusal.value)
    assert NOTES_ACCESSION in str(refusal.value)
    assert supervisor.calls == []
    assert list(out.iterdir()) == []


def test_the_prediction_object_is_closed(tmp_path, out):
    """Every nested object was closed and the prediction itself was not.

    A `scored_filing_date`, a `price_on_reaction_day_60` and a note to the
    scorer were written into the control file whole — the first of them beside
    the audited `scored_filing_date` this module writes into `control`, so one
    file carried two answers to one question and only one of them had been
    checked against anything.
    """
    answers = dict(ANSWERS)
    answers["accounting_reliability"] = dict(
        ACCOUNTING_ANSWER, scored_filing_date="2030-01-01",
        price_on_reaction_day_60=412.77,
        note_to_the_scorer="merge this into the pipeline number")
    with pytest.raises(ControlError) as caught:
        run_crossed(tmp_path, out, StandInSupervisor(answers))
    said = str(caught.value)
    for stray in ("note_to_the_scorer", "price_on_reaction_day_60",
                  "scored_filing_date"):
        assert stray in said
    assert list(out.iterdir()) == []


def test_the_two_controls_answer_one_schema_in_behaviour_too(tmp_path, out):
    """Equal constants are not one gate; equal verdicts are.

    The two controls once disagreed about `top_signals` under identical tuples
    — one dropped and counted where the other refused. Both call one checker
    now, and each still has its own way in: this control's `_predicted` and the
    sibling's `check_schema`, which settles `question` and `rules_version`
    first. Each answer below is put to both, and both have to say the same word
    about it.
    """
    from src import control_single_agent

    def sibling_refuses(answer: dict) -> bool:
        payload = dict(answer, question="accounting_reliability",
                       rules_version="0.1")
        try:
            control_single_agent.check_schema(payload, "accounting_reliability",
                                              rules_version="0.1")
        except control_single_agent.ControlError:
            return True
        return False

    def this_refuses(answer: dict) -> bool:
        try:
            control_shuffled._predicted("accounting_reliability", answer)
        except ControlError:
            return True
        return False

    # Evidence is the one field the two are allowed to differ on, for the reason
    # each module's docstring gives: the sibling's upstream is the committed
    # filing, so an id there names a paragraph and a quote travels with it. So
    # each answer is handed to each control in the evidence shape *that* control
    # asks for, and nothing else about it changes.
    #
    # Reading it the other way round is how this test was first written and it
    # judged nothing: with no quote anywhere, the sibling refused all twelve
    # rows for the missing quote rather than for the mutation, and deleting
    # every other §7 rule from the sibling left this green.
    def quoted(answer: dict) -> dict:
        """The same answer with a quote beside each upstream id.

        Left alone if the entry is not the shape a quote goes in -- a battery
        row whose whole point is a malformed checklist must reach the sibling
        malformed, not repaired on the way.
        """
        entries = answer.get("checklist")
        if not isinstance(entries, list):
            return dict(answer)
        rebuilt = []
        for entry in entries:
            cites = entry.get("evidence") if isinstance(entry, dict) else None
            if not isinstance(cites, list):
                rebuilt.append(entry)
                continue
            rebuilt.append(dict(entry, evidence=[
                dict(cited, quote="a sentence") if isinstance(cited, dict) else cited
                for cited in cites]))
        return dict(answer, checklist=rebuilt)

    good = dict(ACCOUNTING_ANSWER)
    # The row that cannot be written while the evidence shapes are confused: a
    # well-formed answer, which both controls have to *accept*.
    assert not this_refuses(good), "the good answer is the baseline"
    assert not sibling_refuses(quoted(good)), "the good answer is the baseline"

    battery = {
        "a fourth finding": {"checklist": [dict(good["checklist"][0],
                                                finding="yes")]},
        "a checklist entry that is not an object": {"checklist": [good, "x"]},
        "a confidence outside its range": {
            "checklist": [dict(good["checklist"][0], confidence=1.4)]},
        "a tier the thresholds never produce": {"tier": "banana"},
        "events that are not a list": {"events": "lots"},
        "an event probability that is a word": {
            "events": [{"key": "restatement", "p_within_horizon": "likely"}]},
        "a market probability that is a word": {
            "market_direction": {"p_up": "up", "basis": [CROSSED_ITEM]}},
        "a market probability outside its range": {
            "market_direction": {"p_up": 1.7, "basis": [CROSSED_ITEM]}},
        "two explanations under one id": {
            "explanations": [{"id": CROSSED_ITEM, "support": "sufficient",
                              "realization_p": 0.4},
                             {"id": CROSSED_ITEM, "support": "unknown",
                              "realization_p": 0.1}]},
        "an explanation support outside the three": {
            "explanations": [{"id": CROSSED_ITEM, "support": "maybe",
                              "realization_p": 0.4}]},
        "one signal repeated": {
            "top_signals": ["receivables_growth_outruns_revenue"] * 2},
        "a signal naming no entry": {
            "top_signals": ["receivables_growth_outruns_revenue",
                            "margin_collapse"]},
        "six signals": {
            "checklist": [dict(good["checklist"][0], key=f"signal_{n}")
                          for n in range(6)],
            "top_signals": [f"signal_{n}" for n in range(6)]},
    }
    for what, change in battery.items():
        answer = dict(good, **change)
        mine = this_refuses(answer)
        theirs = sibling_refuses(quoted(answer))
        assert mine and theirs, f"{what}: this control {mine}, the sibling {theirs}"


# --- the nested entries of §7, and the record the cutoff is read off ----------
#
# Sixteen rules below this line survived a fail-open mutation with the file
# green: every `_fields` call on a nested entry, every `key` and `id` asked to
# be a name, the uniqueness of `continuous` and `events` keys, `realization_p`'s
# range, the rule that one accession is one filing on one day -- and `_text`'s
# own guard, which no test reached through any of its six call sites. Thirteen
# of them accept a malformed value onto the record rather than refusing it, and
# one of the sixteen is on the cutoff path. A seventeenth row of the same probe
# was green on the parent commit too, and is not counted here because it was the
# unreachable branch the reorder in `_predicted` opened up rather than a live
# rule nobody judged. The probe is the one used on the sibling: turn the rule
# off, run this file, require red -- and see the section below, because a table
# of twenty rules is not a sweep of sixty-six.
#
# The §7 rules named here and in the two sections below have since moved out of
# `_predicted` into `src/prediction_schema.py`, the one check both controls
# call. The tests still reach them the way a run does, through this control.


@pytest.mark.parametrize("question,field,entries", [
    ("accounting_reliability", "checklist",
     [dict(ACCOUNTING_ANSWER["checklist"][0], note="see above")]),
    ("accounting_reliability", "events",
     [dict(ACCOUNTING_ANSWER["events"][0], note="see above")]),
    ("accounting_reliability", "explanations",
     [{"id": CROSSED_ITEM, "support": "sufficient", "realization_p": 0.4,
       "note": "see above"}]),
    ("financial_pressure", "continuous",
     [dict(PRESSURE_ANSWER["continuous"][0], note="see above")]),
])
def test_a_stray_field_on_a_nested_entry_is_refused(
        tmp_path, out, question, field, entries):
    """The prediction object is closed and so is every entry inside it.

    `test_the_prediction_object_is_closed` judges the outer object only. Each
    nested entry has its own closed field set in `docs/CHECKLIST.md` §7 and each
    `_fields` call enforcing one of them had no judge, so a `note` beside a
    finding — or a second point estimate beside `point` — was written into the
    control file whole, under a column §8 has no way to score.
    """
    answers = dict(ANSWERS)
    answers[question] = dict(ANSWERS[question], **{field: entries})
    with pytest.raises(ControlError) as caught:
        run_crossed(tmp_path, out, StandInSupervisor(answers))
    said = str(caught.value)
    assert "note" in said
    assert "docs/CHECKLIST.md §7 gives it" in said
    assert list(out.iterdir()) == []


@pytest.mark.parametrize("key", ["", "   ", None, 3, ["a"]])
@pytest.mark.parametrize("question,field", [
    ("accounting_reliability", "checklist"),
    ("accounting_reliability", "events"),
    ("financial_pressure", "continuous"),
])
def test_an_entry_naming_no_key_is_refused(tmp_path, out, question, field, key):
    """One indicator, one key — and a key that is not a name names nothing.

    The uniqueness rule below reads these keys and a scorer joins on them, so an
    empty string or a `None` is a row of the scorecard that cannot be matched to
    an indicator. `_text` is the rule, and none of its seven call sites had a
    judge: turning its own guard off left this file green.
    """
    answers = dict(ANSWERS)
    answers[question] = dict(
        ANSWERS[question], **{field: [dict(ANSWERS[question][field][0], key=key)]})
    with pytest.raises(ControlError) as caught:
        run_crossed(tmp_path, out, StandInSupervisor(answers))
    said = str(caught.value)
    assert f"{field}[1].key" in said
    assert "the schema gives it a name" in said
    assert list(out.iterdir()) == []


@pytest.mark.parametrize("named", ["", "   ", None, 3])
def test_an_explanation_naming_no_id_is_refused(tmp_path, out, named):
    """An explanation's `id` is what it resolves against: the gate looks it up in
    the four reports the crossing handed over, and an empty id resolves against
    nothing while reading as an id that failed to resolve. The two are different
    rows of the scorecard — one is a malformed answer, the other a dropped
    item — so the malformed one is refused before the gate counts anything."""
    answers = dict(ANSWERS)
    answers["accounting_reliability"] = dict(
        ACCOUNTING_ANSWER,
        explanations=[{"id": named, "support": "sufficient", "realization_p": 0.4}])
    with pytest.raises(ControlError) as caught:
        run_crossed(tmp_path, out, StandInSupervisor(answers))
    said = str(caught.value)
    assert "explanations[1].id" in said
    assert "the schema gives it a name" in said
    assert list(out.iterdir()) == []


@pytest.mark.parametrize("named", ["", "   ", None, 3])
def test_an_evidence_entry_naming_no_id_is_refused(tmp_path, out, named):
    """`test_an_evidence_entry_that_is_not_the_schemas_shape_is_refused` judges
    the entry's field set; this judges the field. An entry carrying the right
    field and an empty string in it reached the citation gate, which resolved it
    against nothing and dropped the item — a malformed answer counted as a
    failed citation, which is the count §8 reports beside the score."""
    answers = dict(ANSWERS)
    answers["accounting_reliability"] = dict(
        ACCOUNTING_ANSWER,
        checklist=[dict(ACCOUNTING_ANSWER["checklist"][0],
                        evidence=[{"upstream_item_id": named}])])
    with pytest.raises(ControlError) as caught:
        run_crossed(tmp_path, out, StandInSupervisor(answers))
    said = str(caught.value)
    assert "checklist[1].evidence[1].upstream_item_id" in said
    assert "the schema gives it a name" in said
    assert list(out.iterdir()) == []


@pytest.mark.parametrize("direction", ["", "   ", None, 3])
def test_a_continuous_entry_naming_no_direction_is_refused(tmp_path, out, direction):
    """§7 gives `direction` a string and does not enumerate its values, so a
    name is the whole of what this rule can ask — and it was asking nobody."""
    answers = dict(ANSWERS)
    answers["financial_pressure"] = dict(
        PRESSURE_ANSWER,
        continuous=[dict(PRESSURE_ANSWER["continuous"][0], direction=direction)])
    with pytest.raises(ControlError) as caught:
        run_crossed(tmp_path, out, StandInSupervisor(answers))
    said = str(caught.value)
    assert "continuous[1].direction" in said
    assert "the schema gives it a name" in said
    assert list(out.iterdir()) == []


def test_two_continuous_entries_under_one_key_are_refused(tmp_path, out):
    """Financial pressure predicts three numbers, one per key, and §8 scores
    each against the reported value. Two entries under `revenue_next_quarter`
    are two predictions of one number, and the scorer reading the first would
    score whichever the model happened to write first."""
    entry = PRESSURE_ANSWER["continuous"][0]
    answers = dict(ANSWERS)
    answers["financial_pressure"] = dict(
        PRESSURE_ANSWER, continuous=[entry, dict(entry, point=250.0, high=300.0)])
    with pytest.raises(ControlError) as caught:
        run_crossed(tmp_path, out, StandInSupervisor(answers))
    said = str(caught.value)
    assert "revenue_next_quarter" in said
    assert "more than once" in said
    assert list(out.iterdir()) == []


def test_two_events_under_one_key_are_refused(tmp_path, out):
    """§8 scores events by Brier, one probability per event."""
    entry = ACCOUNTING_ANSWER["events"][0]
    answers = dict(ANSWERS)
    answers["accounting_reliability"] = dict(
        ACCOUNTING_ANSWER, events=[entry, dict(entry, p_within_horizon=0.9)])
    with pytest.raises(ControlError) as caught:
        run_crossed(tmp_path, out, StandInSupervisor(answers))
    said = str(caught.value)
    assert "restatement" in said
    assert "more than once" in said
    assert list(out.iterdir()) == []


@pytest.mark.parametrize("chance", [1.4, -0.1, "likely", None, True])
def test_a_realization_probability_that_is_not_one_is_refused(tmp_path, out, chance):
    """An explanation carries how likely the supervisor thinks its own account is
    to be borne out, and §8 scores that number. `True` is in the list because
    `isinstance(True, int)` is true in Python and a boolean scored as a
    probability is a 1.0 nobody wrote."""
    answers = dict(ANSWERS)
    answers["accounting_reliability"] = dict(
        ACCOUNTING_ANSWER,
        explanations=[{"id": CROSSED_ITEM, "support": "sufficient",
                       "realization_p": chance}])
    with pytest.raises(ControlError) as caught:
        run_crossed(tmp_path, out, StandInSupervisor(answers))
    assert "realization_p" in str(caught.value)
    assert list(out.iterdir()) == []


def test_financial_pressure_with_no_continuous_is_refused(tmp_path, out):
    """The field the schema gives this question and no other, absent."""
    answers = dict(ANSWERS)
    answers["financial_pressure"] = {
        key: value for key, value in PRESSURE_ANSWER.items() if key != "continuous"}
    with pytest.raises(ControlError) as caught:
        run_crossed(tmp_path, out, StandInSupervisor(answers))
    said = str(caught.value)
    assert "has no continuous" in said
    assert "the schema requires of this question" in said
    assert list(out.iterdir()) == []


def test_accounting_reliability_carrying_continuous_is_refused(tmp_path, out):
    """And the same field on the question it does not belong to, which said the
    wrong thing for a different reason: the closed-prediction check answered
    first and reported `continuous` as a field §7 does not have, which is not
    what is wrong with it — §7 has it, for the other question. The branch
    saying so was unreachable, so it is asked before the closed check now."""
    answers = dict(ANSWERS)
    answers["accounting_reliability"] = dict(
        ACCOUNTING_ANSWER, continuous=PRESSURE_ANSWER["continuous"])
    with pytest.raises(ControlError) as caught:
        run_crossed(tmp_path, out, StandInSupervisor(answers))
    said = str(caught.value)
    assert "carries continuous" in said
    assert "gives to financial pressure alone" in said
    assert list(out.iterdir()) == []


def test_neither_control_writes_a_number_that_is_not_json(tmp_path, out):
    """A prediction the scorer cannot read back is the prediction lost.

    Run before the rule existed, this wrote `"point": Infinity` into
    `control_shuffled_pressure.json` — `json.dumps` spells an infinity with a
    bare token RFC 8259 does not have, and a reader passing `parse_constant`
    refuses the file. Nothing else in §7 was asking: every other number is a
    probability with a range, and `0 <= inf <= 1` is false, so the range rule
    caught it there. `point`, `low` and `high` have no range.

    The sibling is asserted in the same test because the two controls answer one
    schema, and this is the third rule found on one of them and missing from the
    other.
    """
    from src import control_single_agent
    reckless = dict(PRESSURE_ANSWER,
                    continuous=[dict(PRESSURE_ANSWER["continuous"][0],
                                     point=math.inf, high=math.inf)])
    with pytest.raises(ControlError, match="not JSON"):
        control_shuffled._predicted("financial_pressure", reckless)
    quoted = dict(reckless, checklist=[
        dict(entry, evidence=[dict(cited, quote="as filed")
                              for cited in entry["evidence"]])
        for entry in reckless["checklist"]])
    with pytest.raises(control_single_agent.ControlError, match="not JSON"):
        control_single_agent.check_schema(
            dict(quoted, question="financial_pressure", rules_version="0.1"),
            "financial_pressure", rules_version="0.1")

    answers = dict(ANSWERS)
    answers["financial_pressure"] = reckless
    with pytest.raises(ControlError, match="not JSON"):
        run_crossed(tmp_path, out, StandInSupervisor(answers))
    assert list(out.iterdir()) == []


@pytest.mark.parametrize("field", ["point", "low", "high"])
def test_a_continuous_bound_that_is_not_a_number_at_all_is_refused(
        tmp_path, out, field):
    """`nan` compares false against everything, so `low <= point <= high` was
    false and the range rule refused it with the wrong sentence — the interval
    is not the problem, the value is not a number."""
    answers = dict(ANSWERS)
    answers["financial_pressure"] = dict(
        PRESSURE_ANSWER,
        continuous=[dict(PRESSURE_ANSWER["continuous"][0], **{field: math.nan})])
    with pytest.raises(ControlError) as caught:
        run_crossed(tmp_path, out, StandInSupervisor(answers))
    said = str(caught.value)
    assert f"continuous[1].{field}" in said
    assert "not JSON" in said
    assert list(out.iterdir()) == []


def test_the_written_control_files_are_json_a_strict_reader_accepts(crossed_run):
    """`json.loads` accepts `Infinity` and `NaN` by default, so reading a file
    back with it is not evidence the file is JSON. `parse_constant` is where a
    reader that refuses them says so."""
    _, _, out = crossed_run

    def refuse(name):
        raise AssertionError(f"{name} is not a JSON value")

    for name in (ACCOUNTING_FILE, PRESSURE_FILE):
        json.loads((out / name).read_text(encoding="utf-8"), parse_constant=refuse)


def test_one_accession_recorded_on_two_dates_is_refused(tmp_path):
    """The sharp one: this is the cutoff.

    `filed` is what dates both halves, and with two dates on one accession the
    set it built had two members and `.pop()` returned an arbitrary one — so
    "nothing filed after the triggering report enters the input" would be read
    off a record contradicting itself, and which way it fell would depend on set
    ordering. No committed manifest records an accession twice, and writing one
    that does under `tests/fixtures/` would be inventing the record this control
    reads, so the two rows are written here.
    """
    accession = "0001783180-26-000008"
    two_dates = tmp_path / "two-dates"
    (two_dates / NUMBERS_COMPANY).mkdir(parents=True)
    (two_dates / NUMBERS_COMPANY / "manifest.json").write_text(json.dumps({
        "as_of": "2026-02-05",
        "documents": [
            {"accession": accession, "form": "10-K", "role": "primary_html",
             "path": "primary.html", "filing_date": "2026-02-05"},
            {"accession": accession, "form": "10-K", "role": "exhibit",
             "path": "exhibit.html", "filing_date": "2026-02-06"}]},
        indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with pytest.raises(ControlError) as caught:
        control_shuffled.filed(NUMBERS_COMPANY, accession, fixtures_root=two_dates)
    said = str(caught.value)
    assert "2026-02-05" in said and "2026-02-06" in said
    assert "one accession is one filing on one day" in said

    # And the same reader on the same two rows filed on the same day, so that
    # the refusal above is about the disagreement and not about two rows.
    one_date = tmp_path / "one-date"
    (one_date / NUMBERS_COMPANY).mkdir(parents=True)
    (one_date / NUMBERS_COMPANY / "manifest.json").write_text(json.dumps({
        "as_of": "2026-02-05",
        "documents": [
            {"accession": accession, "form": "10-K", "role": "primary_html",
             "path": "primary.html", "filing_date": "2026-02-05"},
            {"accession": accession, "form": "10-K", "role": "exhibit",
             "path": "exhibit.html", "filing_date": "2026-02-05"}]},
        indent=2, sort_keys=True) + "\n", encoding="utf-8")
    assert control_shuffled.filed(
        NUMBERS_COMPANY, accession, fixtures_root=one_date) == dt.date(2026, 2, 5)


def test_a_company_with_no_record_at_all_dates_no_half(tmp_path):
    """The first of `filed`'s two translations, which carry no `if` of their own.

    A refusal that is an `except` clause rather than an `if` is still a rule,
    and the two in `filed` had no judge: the probe enumerates `if`s, and neither
    of these is one. This is the fail-closed direction of the cutoff at its
    root -- a company whose record cannot be opened at all dates nothing, and an
    unopenable record is not an early date. The reader's own words come through
    the translation, because a refusal that drops its cause says a filing is
    undatable without saying why.
    """
    empty = tmp_path / "no-record"
    empty.mkdir()
    with pytest.raises(ControlError) as caught:
        control_shuffled.filed(NUMBERS_COMPANY, NUMBERS_ACCESSION, fixtures_root=empty)
    said = str(caught.value)
    assert f"{NUMBERS_COMPANY} has no record to date {NUMBERS_ACCESSION}" in said
    assert "manifest.json does not exist" in said


def test_a_recorded_filing_date_that_is_not_a_date_dates_no_half(tmp_path):
    """The second translation: a row that is there and says nothing readable.

    `cutoff_guard.parse_date` refuses rather than guesses, and `filed` hands
    that refusal on under this control's own error type so the caller sees one
    kind of failure. Mutated to return the string untouched, the comparison in
    `_within_cutoff` would be `str > date`, which raises `TypeError` somewhere
    else entirely -- so the judge is on the message, and it names which
    company's which accession could not be dated.
    """
    root = tmp_path / "unreadable-date"
    (root / NUMBERS_COMPANY).mkdir(parents=True)
    (root / NUMBERS_COMPANY / "manifest.json").write_text(json.dumps({
        "as_of": "2026-02-05",
        "documents": [
            {"accession": NUMBERS_ACCESSION, "form": "10-K", "role": "primary_html",
             "path": "primary.html", "filing_date": "the fifth of February"}]},
        indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with pytest.raises(ControlError) as caught:
        control_shuffled.filed(NUMBERS_COMPANY, NUMBERS_ACCESSION, fixtures_root=root)
    said = str(caught.value)
    assert f"{NUMBERS_COMPANY} {NUMBERS_ACCESSION} filing_date" in said
    assert "is not an ISO date" in said


# --- the four the first sweep missed -----------------------------------------
#
# The sweep above was a table of twenty rules, and a table is not a sweep: an
# exhaustive mutation of all sixty-six guarded rules in the module found four
# more that left this file green. Two are inside `_predicted` itself. All four
# are live rules with their own sentences, and with any of them off a clean
# refusal becomes an uncaught `TypeError` — or, for the explanation id, nothing
# at all.
#
# Three of the sixty-six are judged as a function contract and not as pipeline
# coverage: the two entry-carries-no-key rules and the top_signals-is-a-list
# rule sit inside `resolved`, behind a `_predicted` that refuses those shapes
# first, so no input handed to `run` can reach them and the three tests below
# call the gate directly. A mutation row for one of them says the rule is
# judged. It does not say a run could trip it — and the day `resolved` gains a
# second caller, that is the difference between defence in depth and a rule
# nothing upstream is holding.


class LiteralSupervisor:
    """Hands back exactly what it was given, object or not.

    `StandInSupervisor` copies its answer with `dict()`, so a non-object cannot
    survive the stub — which is why the rule refusing one could not be reached
    through it and had no judge. A real model call returns whatever the model
    returned.
    """

    def __init__(self, answer):
        self.answer = answer

    def __call__(self, question: str, reports: dict):
        return self.answer


@pytest.mark.parametrize("answer", [7, None, "watch", ["checklist"]])
def test_a_supervisor_answering_with_something_other_than_an_object_is_refused(
        tmp_path, out, answer):
    """The first line of the schema check: the model is a subprocess and a
    control file holds a prediction. With the rule off, `7` reaches
    `key not in answer` and raises `TypeError: argument of type 'int' is not
    iterable`."""
    with pytest.raises(ControlError) as caught:
        run_crossed(tmp_path, out, LiteralSupervisor(answer))
    said = str(caught.value)
    assert "and a control file holds a prediction" in said
    assert type(answer).__name__ in said
    assert list(out.iterdir()) == []


@pytest.mark.parametrize("signal", [3, None, ["receivables_growth_outruns_revenue"], ""])
def test_a_top_signal_that_is_not_a_name_is_refused(tmp_path, out, signal):
    """A signal is the key of a checklist entry, so it is a name.

    Three rules downstream read this list — uniqueness, the ceiling, and the
    resolution against the entries that stood — and each of them was reached
    with a non-name in it. With the rule off, `3` raises `TypeError: sequence
    item 0: expected str instance, int found` inside the refusal that names the
    signals, and `["x"]` raises `unhashable type: 'list'` where that refusal
    asks which signals name no checklist entry. Not inside `_unique`, which
    this docstring said until the mutation was run: it counts before it
    collects, so a list appearing once is never hashed and `_unique` lets it
    straight through.
    """
    answers = dict(ANSWERS)
    answers["accounting_reliability"] = dict(ACCOUNTING_ANSWER, top_signals=[signal])
    with pytest.raises(ControlError) as caught:
        run_crossed(tmp_path, out, StandInSupervisor(answers))
    said = str(caught.value)
    assert "top_signals[1] is" in said
    assert "a signal is the key of a checklist entry" in said
    assert list(out.iterdir()) == []


@pytest.mark.parametrize("entry", ["oops", 3, None, {"finding": "flag"}])
def test_a_checklist_entry_the_gate_cannot_name_is_refused(entry):
    """`resolved()` called directly, the way the schema battery calls
    `_predicted` directly.

    In the one call path `_predicted` runs first and refuses this shape, so the
    rule is defence in depth — but it is the gate's own, and what the gate does
    with an entry is drop it *by name*, which an entry with no name cannot be.
    With the rule off, `"oops"` raises `TypeError: string indices must be
    integers` inside `_drop_reason`.
    """
    answer = dict(ACCOUNTING_ANSWER, checklist=[entry])
    with pytest.raises(ControlError) as caught:
        control_shuffled.resolved("accounting_reliability", answer, {CROSSED_ITEM})
    assert "checklist entry carries no key" in str(caught.value)


@pytest.mark.parametrize("entry", [{"id": 3, "support": "sufficient",
                                    "realization_p": 0.4},
                                   "an explanation", None])
def test_an_explanation_the_gate_cannot_name_is_refused(entry):
    """The same rule for the explanations, and the one of the four that failed
    silently rather than loudly: with it off, an explanation carrying `id: 3`
    was neither resolved nor dropped — it went onto the record standing, with an
    id no citation could ever resolve against."""
    answer = dict(ACCOUNTING_ANSWER, explanations=[entry])
    with pytest.raises(ControlError) as caught:
        control_shuffled.resolved("accounting_reliability", answer, {CROSSED_ITEM})
    assert "explanation carries no id" in str(caught.value)


@pytest.mark.parametrize("signals", ["receivables_growth_outruns_revenue", 3, None,
                                     {"receivables_growth_outruns_revenue": True}])
def test_the_gate_refuses_top_signals_that_are_not_a_list(signals):
    """The sixty-sixth rule, and the one the sweep could not express.

    Replacing this call with `pass` is a syntax error — it sits on the
    continuation line of a list comprehension — so the sweep reported "could not
    run" rather than a verdict, and the rule had to be mutated by hand into a
    passthrough to find out. It was green: a string reached the comprehension
    and was iterated character by character, and `top_signals` came out `[]`
    because no single letter is a checklist key. Behind `_predicted` in the one
    call path, like the two rules above, so the test calls the gate directly.
    """
    answer = dict(ACCOUNTING_ANSWER, top_signals=signals)
    with pytest.raises(ControlError) as caught:
        control_shuffled.resolved("accounting_reliability", answer, {CROSSED_ITEM})
    said = str(caught.value)
    assert "gives top_signals as" in said
    assert "docs/CHECKLIST.md §7 gives it as a list" in said


# --- the five a sweep that read only statements could not see ----------------
#
# The sweep enumerated a helper call only when the call was the whole statement,
# so `checklist = _a_list(...)` was not a rule it had ever heard of: five of the
# six `_a_list` call sites are assignments, and the sixth is the one it reported
# COULD NOT RUN. Enumerating the assignments too meant mutating them into a
# passthrough rather than into `pass` -- `pass` on an assignment leaves the name
# unbound, and the `NameError` that follows is red for the wrong reason -- and
# with the value handed through untouched, all five were green.
#
# What each one costs is what the sixth cost: a string is a sequence, so
# `for entry in "lots"` iterates letters and the refusal that arrives is the
# next rule's, about a letter, naming a position in a list that was never a
# list. `events` was the one of the six with a judge, and it has one by accident
# -- its test hands `3`, which is not iterable at all, so the `TypeError` is
# what fails the test rather than the rule being consulted. These assert the
# rule's own sentence.

@pytest.mark.parametrize("question, field, answer", [
    ("accounting_reliability", "checklist",
     dict(ACCOUNTING_ANSWER, checklist="two flags")),
    ("accounting_reliability", "checklist[1].evidence",
     dict(ACCOUNTING_ANSWER,
          checklist=[dict(ACCOUNTING_ANSWER["checklist"][0],
                          evidence="the crossed item")])),
    ("financial_pressure", "continuous",
     dict(PRESSURE_ANSWER, continuous="revenue down")),
    ("accounting_reliability", "explanations",
     dict(ACCOUNTING_ANSWER, explanations="none this time")),
    ("accounting_reliability", "top_signals",
     dict(ACCOUNTING_ANSWER, top_signals="receivables_growth_outruns_revenue")),
])
def test_a_field_the_schema_gives_as_a_list_is_refused_when_it_is_not_one(
        tmp_path, out, question, field, answer):
    """Every `_a_list` call site, named by the field it is standing over.

    A string reaching any of these is the answer iterated letter by letter, and
    the refusal that comes back is about `'t'` at `checklist[1]` -- so the file
    was green while a prediction shaped nothing like §7 was being read as one.
    The assertion is `_a_list`'s own sentence, which is the only thing a
    passthrough removes.
    """
    answers = dict(ANSWERS)
    answers[question] = answer
    with pytest.raises(ControlError) as caught:
        run_crossed(tmp_path, out, StandInSupervisor(answers))
    said = str(caught.value)
    assert f"the {question} answer gives {field} as str" in said
    assert "docs/CHECKLIST.md §7 gives it as a list" in said
    assert list(out.iterdir()) == []
