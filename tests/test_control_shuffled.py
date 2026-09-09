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
from pathlib import Path

import pytest

from src import control_shuffled, cutoff_guard
from src.control_shuffled import ControlError
from src.fetch_fixtures import TICKERS

REPO_ROOT = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures"
PAIR = FIXTURES / "shuffled_report_pair"

# Company A keeps the numbers side and is the company being scored; company B
# supplies the notes side. docs/CHECKLIST.md §8, applied to the twelve.
NUMBERS_COMPANY = "AAPL"
NOTES_COMPANY = "CARR"

# The filing each company's committed reports were written from, read off
# tests/fixtures/{ticker}/manifest.json. Asserted against the manifests below
# rather than trusted here.
NUMBERS_ACCESSION = "0000320193-25-000079"
NOTES_ACCESSION = "0001783180-26-000008"
NUMBERS_FILED = "2025-10-31"
NOTES_FILED = "2026-02-05"

# One id AAPL's own notes-text report carries -- the report the crossing takes
# away from the supervisor, so it is in none of the four reports it was handed --
# and one the crossed set does hold, out of AAPL's numbers-versus-market report.
UNCROSSED_ITEM = "0000320193-25-000079:notes:receivables:1"
CROSSED_ITEM = "0000320193-25-000079:numbers_vs_market:1"

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


def test_the_partner_annual_report_is_ninety_seven_days_after_the_one_being_scored():
    """Read off the two manifests, and counted out here rather than trusted.

    2025-10-31 to 2025-11-30 is 30 days, to 2025-12-31 is 61, to 2026-01-31 is
    92, and to 2026-02-05 is 97. The company being scored keeps the numbers
    side, so the notes side is the later filing of the two.
    """
    assert annual(NUMBERS_COMPANY)["filing_date"] == NUMBERS_FILED
    assert annual(NOTES_COMPANY)["filing_date"] == NOTES_FILED
    apart = dt.date.fromisoformat(NOTES_FILED) - dt.date.fromisoformat(NUMBERS_FILED)
    assert apart.days == 97


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
        # Nothing here declared which filing was being scored, and rather than
        # pass in silence the file says so in its own text.
        assert control["scored_filing_date"] is None


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

    The pair is the one the pairing rule itself produces for AAPL, and CARR's
    annual report was filed ninety-seven days after the one being scored. The
    crossed four reports are not a bundle and carry no manifest, so this is the
    only place that gate can be applied.
    """
    numbers = scored_run(bundle(tmp_path, NUMBERS_COMPANY), NUMBERS_COMPANY)
    supervisor = StandInSupervisor()
    with pytest.raises(ControlError, match=NOTES_FILED):
        control_shuffled.run(NUMBERS_COMPANY, NOTES_COMPANY,
                             numbers_bundle=numbers,
                             notes_bundle=bundle(tmp_path, NOTES_COMPANY),
                             out=out, predictor=supervisor)
    assert list(out.iterdir()) == []
    assert supervisor.calls == []


def test_the_same_two_companies_crossed_the_other_way_is_inside_the_cutoff(tmp_path, out):
    """The gate refuses a late partner, not every partner.

    CARR filed after AAPL, so a run scoring CARR may be handed AAPL's notes.
    That crossing is not the one the pairing rule draws -- `partner("CARR")` is
    CIEN -- and `run` is handed two companies rather than drawing them, so it is
    the dates that decide here and not the rule.

    Nothing in the accounting answer resolves against this crossing: it cites
    AAPL's numbers-versus-market report, which is on the numbers side and so is
    CARR's here. One item drops, which is the citation gate working.
    """
    numbers = scored_run(bundle(tmp_path, NOTES_COMPANY), NOTES_COMPANY)
    control_shuffled.run(NOTES_COMPANY, NUMBERS_COMPANY, numbers_bundle=numbers,
                         notes_bundle=bundle(tmp_path, NUMBERS_COMPANY),
                         out=out, predictor=StandInSupervisor())
    assert sorted(path.name for path in out.iterdir()) == \
           sorted((ACCOUNTING_FILE, PRESSURE_FILE))
    control = written(out, ACCOUNTING_FILE)["control"]
    assert control["scored_filing_date"] == NOTES_FILED
    assert control["numbers_from"] == NOTES_COMPANY
    assert control["notes_from"] == NUMBERS_COMPANY
    assert control["counts"]["dropped_items"] == 1


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
            {"key": "reserve_release_unexplained", "finding": "yes",
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


def test_an_item_citing_the_crossed_set_stands(crossed_run):
    """The control on the drop tests: the answer that resolves is written whole."""
    _, _, out = crossed_run
    accounting = written(out, ACCOUNTING_FILE)
    assert accounting["checklist"] == ACCOUNTING_ANSWER["checklist"]
    assert accounting["control"]["counts"]["dropped_items"] == 0
    assert accounting["control"]["dropped_items"] == []
