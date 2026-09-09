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

The crossing assertion carries its own control
----------------------------------------------

"The notes came from the other company" is only readable if the two companies'
notes reports are not the same text, so
`test_the_two_companies_reports_differ_file_by_file` asserts that first and the
crossing assertions have something to bite on. The sharp form of the crossing is
`test_the_notes_half_is_not_the_numbers_company_own_notes`: AAPL's own notes
report is in the fixture and sitting in the bundle, and the supervisor did not
get it.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src import control_shuffled
from src.control_shuffled import ControlError
from src.fetch_fixtures import TICKERS

REPO_ROOT = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures"
PAIR = FIXTURES / "shuffled_report_pair"

# Company A keeps the numbers side and is the company being scored; company B
# supplies the notes side. docs/CHECKLIST.md §8, applied to the twelve.
NUMBERS_COMPANY = "AAPL"
NOTES_COMPANY = "CARR"

# docs/INPUT_SPEC.md §6.
ACCOUNTING_FILE = "control_shuffled_accounting.json"
PRESSURE_FILE = "control_shuffled_pressure.json"

# What the pipeline's own supervisor would return, written here by hand so that
# nothing the runner writes is judged against something the runner produced. The
# shapes are docs/CHECKLIST.md §7; `continuous` is financial pressure only.
ACCOUNTING_ANSWER = {
    "checklist": [{"key": "receivables_growth_outruns_revenue", "finding": "yes",
                   "confidence": 0.6,
                   "evidence": [{"upstream_item_id":
                                 "0000320193-25-000079:numbers_vs_market:1"}]}],
    "events": [{"key": "restatement", "p_within_horizon": 0.1}],
    "explanations": [],
    "market_direction": {"p_up": 0.4, "basis": []},
    "tier": "watch",
    "top_signals": ["receivables_growth_outruns_revenue"],
}
PRESSURE_ANSWER = {
    "checklist": [{"key": "liquidity_headroom", "finding": "no", "confidence": 0.3,
                   "evidence": []}],
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


def run_crossed(tmp_path, out, predictor):
    """The crossed run under test: AAPL's numbers side, CARR's notes side.

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


# --- which company is B ------------------------------------------------------

def test_the_partner_is_the_next_company_in_the_twelve_by_ticker():
    assert control_shuffled.PAIRING_ORDER == tuple(sorted(TICKERS))
    assert control_shuffled.partner(NUMBERS_COMPANY) == NOTES_COMPANY


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


def test_the_control_file_records_which_company_each_half_came_from(crossed_run):
    _, _, out = crossed_run
    for name in (ACCOUNTING_FILE, PRESSURE_FILE):
        control = written(out, name)["control"]
        assert control["numbers_from"] == NUMBERS_COMPANY
        assert control["notes_from"] == NOTES_COMPANY
        assert control["reports"] == {
            "report_numbers.md": NUMBERS_COMPANY,
            "report_numbers_vs_market.md": NUMBERS_COMPANY,
            "report_notes_text.md": NOTES_COMPANY,
            "report_notes_vs_market.md": NOTES_COMPANY,
        }
        assert control["numbers_from"] != control["notes_from"]


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
    only = bundle(tmp_path, NUMBERS_COMPANY)
    with pytest.raises(ControlError):
        control_shuffled.run(NUMBERS_COMPANY, NOTES_COMPANY,
                             numbers_bundle=only, notes_bundle=only,
                             out=out, predictor=StandInSupervisor())
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
