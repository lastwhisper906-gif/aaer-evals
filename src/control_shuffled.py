"""The shuffled-report control: one company's numbers, another company's notes.

`docs/CHECKLIST.md` §8 states what this control falsifies:

    the supervisor is fed one company's numbers report together with **another
    company's** notes report, on every pilot filing. If its score matches the
    real run, the supervisor is not reconciling the two reports, it is
    pattern-matching one of them.

and states exactly what is swapped, because "one company's report" leaves the
comparer reports undefined: company A keeps `report_numbers.md` and
`report_numbers_vs_market.md`; `report_notes_text.md` and
`report_notes_vs_market.md` come from company B. The notes side travels with its
own comparer report, so the only thing broken is the correspondence between the
two sides -- which is the thing being tested.

The supervisor is the pipeline's own supervisor, unchanged: same prompt, same
model, same output schema. Nothing here writes a prompt. That is what makes the
control a control -- if the evidence were crossed *and* the prompt changed, a
score that matched the real run would say nothing about reconciliation. So this
module carries no prompt, unlike the single-agent control, whose prompt
`docs/HOW_WE_WORK.md` §6 puts inside its own run script.

What Python owns here, and what it does not
-------------------------------------------

Python crosses the four report files, records which company each half came from,
and writes the two control files. The one model call per question is the
supervisor's, and it is passed in as `predictor`. There is no command line: the
call cannot be made from one, and an entry point that could not make it would be
a script nobody could run.

    reports = crossed(numbers_bundle, notes_bundle)      # what the supervisor sees
    run("AAPL", partner("AAPL"), numbers_bundle=..., notes_bundle=...,
        out=..., predictor=...)                          # both control files

**Which company is B.** `docs/CHECKLIST.md` says "the next company in the twelve
by ticker, wrapping around, so the pairing is fixed rather than drawn". Read as
the twelve in ticker order -- `by ticker` is what distinguishes the pairing from
the order `src/fetch_fixtures.py` and `tests/fixtures/README.md` happen to list
them in, which is a fetch order and not a canonical one. That reading is
`PAIRING_ORDER` below and nothing else depends on it, so a correction is one
line.

**The control file is never merged into the pipeline's number.** It carries a
`control` block naming the scorecard row it is scored on and the company each
half came from, so a file that reached the wrong place can be told from a
prediction by reading it, not by trusting its name.
"""

from __future__ import annotations

import json
from pathlib import Path

from src import cutoff_guard
from src.fetch_fixtures import TICKERS

# The twelve in ticker order. See the module docstring for the reading.
PAIRING_ORDER = tuple(sorted(TICKERS))

# The two halves, by the names `docs/INPUT_SPEC.md` §6 gives them. A is the
# company being scored and keeps the numbers side; B supplies the notes side.
NUMBERS_SIDE = ("report_numbers.md", "report_numbers_vs_market.md")
NOTES_SIDE = ("report_notes_text.md", "report_notes_vs_market.md")
REPORTS = NUMBERS_SIDE + NOTES_SIDE

# One control file and one scorecard row per question.
CONTROL_FILES = {
    "accounting_reliability": "control_shuffled_accounting.json",
    "financial_pressure": "control_shuffled_pressure.json",
}
SCORECARD_ROWS = {
    "accounting_reliability": "shuffled_accounting",
    "financial_pressure": "shuffled_pressure",
}
QUESTIONS = tuple(CONTROL_FILES)

CONTROL_NAME = "shuffled_report"
RULES_VERSION = "0.1"

# The prediction schema, `docs/CHECKLIST.md` §7. `question` and `rules_version`
# are this module's to write -- the supervisor is answering the question it was
# handed -- so they are not asked of the predictor. `continuous` is financial
# pressure only, which the schema says in those words, so it is required on one
# question and refused on the other rather than merely tolerated on both.
PREDICTED_KEYS = ("checklist", "events", "explanations", "market_direction",
                  "tier", "top_signals")
CONTINUOUS = "continuous"
CONTINUOUS_QUESTION = "financial_pressure"


class ControlError(Exception):
    """The control cannot be run as `docs/CHECKLIST.md` §8 describes it."""


def partner(ticker: str, order: tuple[str, ...] = PAIRING_ORDER) -> str:
    """Company B for this company: the next in the twelve, wrapping around."""
    ticker = ticker.upper()
    if ticker not in order:
        raise ControlError(f"{ticker} is not one of the twelve: {', '.join(order)}")
    return order[(order.index(ticker) + 1) % len(order)]


def crossed(numbers_bundle, notes_bundle) -> dict[str, str]:
    """The four reports a shuffled supervisor sees: two out of each bundle.

    Whole files, byte for byte as the bundles hold them. Nothing here reads
    inside a report: what is being broken is the correspondence between the two
    sides, and a control that edited a report would be breaking something else
    as well and could not say which one the score answered.
    """
    text = {}
    for source, names in ((numbers_bundle, NUMBERS_SIDE),
                          (notes_bundle, NOTES_SIDE)):
        for name in names:
            try:
                text[name] = cutoff_guard.load_bundle_file(source, name)
            except cutoff_guard.CutoffGuardError as exc:
                raise ControlError(
                    f"the shuffled control needs {name}: {exc}") from exc
    return text


def provenance(numbers_from: str, notes_from: str, question: str) -> dict:
    """Which company each half came from, as the control file records it."""
    return {
        "name": CONTROL_NAME,
        "scorecard_row": SCORECARD_ROWS[question],
        "numbers_from": numbers_from,
        "notes_from": notes_from,
        "reports": {name: (numbers_from if name in NUMBERS_SIDE else notes_from)
                    for name in REPORTS},
    }


def _predicted(question: str, answer) -> dict:
    """The supervisor's answer, checked against the schema before it is written."""
    if not isinstance(answer, dict):
        raise ControlError(
            f"the supervisor answered {question} with {type(answer).__name__}, "
            "and a control file holds a prediction")
    missing = [key for key in PREDICTED_KEYS if key not in answer]
    if missing:
        raise ControlError(
            f"the {question} answer has no {', '.join(missing)}; a control is "
            "scored on the same targets as the pipeline and cannot be short of "
            "them (docs/CHECKLIST.md §7)")
    wants_continuous = question == CONTINUOUS_QUESTION
    if wants_continuous and CONTINUOUS not in answer:
        raise ControlError(f"the {question} answer has no {CONTINUOUS}, which the "
                           "schema requires of this question")
    if not wants_continuous and CONTINUOUS in answer:
        raise ControlError(f"the {question} answer carries {CONTINUOUS}, which the "
                           "schema gives to financial pressure alone")
    return dict(answer)


def _rendered(payload: dict) -> str:
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def _writable(out, name: str, text: str) -> Path:
    """Where one control file will land, refusing one already on record.

    A run directory is append-only: a new file may be added to it, and an
    existing one is never rewritten. A correction is a new run. Rewriting the
    identical bytes changes nothing on record and so is not a change.
    """
    folder = Path(out)
    if not folder.is_dir():
        raise ControlError(f"{folder} is not a directory to write a control into")
    if cutoff_guard.bundle_files(folder, name) and \
            cutoff_guard.load_bundle_file(folder, name) != text:
        raise ControlError(
            f"{folder / name} is already on record with different content. A "
            "control file is written once; a correction is a new run.")
    return folder / name


def run(numbers_from: str, notes_from: str, *, numbers_bundle, notes_bundle,
        out, predictor, rules_version: str = RULES_VERSION) -> dict:
    """Both control files for one crossed pair, and what was crossed to get them.

    `predictor(question, reports) -> dict` is the one model call per question:
    the pipeline's own supervisor, handed the crossed four reports and nothing
    else. It is called once for each question, on the same crossed evidence.
    """
    numbers_from, notes_from = numbers_from.upper(), notes_from.upper()
    if numbers_from == notes_from:
        raise ControlError(
            f"both halves would come from {numbers_from}. A supervisor given one "
            "company's own numbers and notes is the real run, not the shuffled "
            "control -- the control is the two halves not corresponding.")
    if Path(numbers_bundle).resolve() == Path(notes_bundle).resolve():
        raise ControlError(
            f"both halves would come out of {Path(numbers_bundle).resolve()}. "
            "Two companies' reports are two bundles.")

    reports = crossed(numbers_bundle, notes_bundle)

    # Both answers, and both destinations, before either file is opened. A
    # control is two rows of one scorecard, and a run that wrote one of them and
    # then refused the other would leave a half-crossed pair on record in a
    # directory where nothing may be rewritten to finish it.
    rendered = {}
    for question in QUESTIONS:
        answer = _predicted(question, predictor(question, dict(reports)))
        answer.update(question=question, rules_version=rules_version,
                      control=provenance(numbers_from, notes_from, question))
        rendered[question] = _rendered(answer)
    written = {question: _writable(out, CONTROL_FILES[question], text)
               for question, text in rendered.items()}

    for question, path in written.items():
        path.write_text(rendered[question], encoding="utf-8")
    return {"numbers_from": numbers_from, "notes_from": notes_from,
            "reports": reports, "files": written}
