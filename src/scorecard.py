"""The scorecard, rendered from what the runs left behind. Nothing typed by hand.

`docs/HOW_WE_WORK.md` calls the monthly scorecard "the evaluation metric tables,
with no judgment added", and `docs/CHECKLIST.md` §8 says all of it is recomputed
deterministically from `runs/` and `events/` with nothing carried by hand. This
module is that sentence made mechanical: it walks a runs root, reads each run's
own files, does the arithmetic in Python, and fills the slots in
`src/scorecard_template.md`. Every word on the page comes from the template and
every number comes from a run, so there is no step in the middle where a figure
could be improved on its way to the page.

**The Beneish M-score is the first accounting row**, and the order of the rest is
`docs/CHECKLIST.md` §8's order, not this file's opinion. Beneish and Vorst (2022)
found it the most useful of seven fraud models, so if the three layers do not
beat it the page says the structure adds nothing, in those words, from the
template. The same comparison runs against the single-agent control, which the
checklist says falsifies the structure the same way: if the layers do not beat
one call, the structure is decoration.

**One target is scored** — the direction of the 60-trading-day abnormal return
from the third trading day after the filing, under each question separately.
Brier, direction hit rate, and the count of insufficient answers beside them, as
§8's metric table says. The other targets wait for their horizons; they are
absent from the page rather than estimated.

**The two caveats travel with that row**, both verbatim from `docs/CHECKLIST.md`
§5 and both in the template rather than here: post-2006 drift is close to zero
outside small capitalizations, and published anomalies lose roughly 58% of their
margin after publication. `tests/test_scorecard.py` reads them out of the
checklist and string-matches them against the rendered page, so the page and the
document cannot drift apart quietly.

**Every row carries which side of the rules-version freeze it came from.**
§10 draws that line by when the filing existed, not by which company filed it, so
each run's own `input_manifest.json` supplies two dates -- its `cutoff`, which the
cutoff rule makes the filing date of the triggering report, and
`rules_version_frozen` -- and the side is derived from the comparison rather than
recorded as a label that could be wrong. A run that names neither is refused; a
number that travels without that label eventually gets quoted without it. Pilot
rows carry `pipeline check` in the table itself, never a footnote.

One line on the gap that leaves: `src/assemble_bundle.py` does not write
`rules_version_frozen` yet, because `rules/v0.1` does not exist and there is no
freeze date to write. Refusing is the default this module proceeds with -- the
alternative is a hard-coded freeze date, which would be a threshold this module
has no source for. The key is read from the manifest so that whoever freezes the
rules version writes it once, beside `rules_version`, rather than here.

What a run has to leave behind
------------------------------

    input_manifest.json   rules_version, rules_version_frozen, cutoff
    outcome.json          the realized 60-trading-day abnormal return
    baselines.json        one entry per Python-computed row
    prediction_accounting.json, prediction_pressure.json
    control_single_agent_accounting.json, control_shuffled_accounting.json
    control_single_agent_pressure.json, control_shuffled_pressure.json

Each answer file carries `market_direction.p_up` in the shape
`docs/CHECKLIST.md` §7 gives the two predictions; `baselines.json` carries one
such object per row key, and whatever else the baseline computed is ignored
here. A file that is not there, or a key that is not in `baselines.json`, makes
that row read `not on record` -- the row keeps its place in the order and carries
no number. `naive_forecast` and `short_interest_ratio` are scorecard rows that
the formula-baselines item does not list, so they will read `not on record`
until something writes them into `baselines.json`; naming the gap here beats
inventing a second file for two rows.

`outcome.json` is not one of the files `docs/INPUT_SPEC.md` §6 lists, and that is
stated rather than hidden. §6 lists what every layer saw and what each one said,
and an outcome is neither: it is what happened afterwards, which is why the
scoring stage waits for horizon expiry. Adding a file to a run is what
append-only permits -- existing content is never changed or deleted -- so the
outcome lands beside the record instead of editing it. A run whose horizon has
not expired has no `outcome.json`, is scored in nothing, and is listed at the
foot of the page as still waiting.

Where the edges are drawn
-------------------------

* `p_up` may be the string `insufficient`, which §5 allows. It is counted, it is
  reported beside the score, and it is not scored. A row whose every answer is
  insufficient carries no Brier at all rather than a Brier over nothing.
* A hit needs the probability on the right side of one half. Exactly one half is
  not a hit, in either direction.
* An abnormal return of exactly zero is not positive, so the direction is down.
* A tie on Brier is not beating. The pipeline has to be strictly better than the
  first row for the page to say it beat it.
* A `p_up` that is neither a probability nor `insufficient` stops the render
  rather than being dropped quietly.

Every read of a run goes through `src/cutoff_guard.py`, which is what keeps the
bypass scan in `tests/test_cutoff_guard.py` a true statement about `src/`. No
date gate applies: these are the run's own outputs and its outcome, and the
outcome is later than the cutoff on purpose.

    python3.12 -m src.scorecard --runs runs
    python3.12 src/scorecard.py --runs tests/fixtures/scorecard/runs

Exit 0 clean, 2 the runs root cannot be scored, 3 the wrong interpreter.
"""

from __future__ import annotations

import argparse
import functools
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from string import Template

try:
    from src import cutoff_guard, interpreter_pin
except ImportError:  # invoked as a plain script: python3.12 src/scorecard.py
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import cutoff_guard, interpreter_pin

BAD_INPUT = 2

TEMPLATE_PATH = Path(__file__).resolve().parent / "scorecard_template.md"
BLOCK_MARKER = re.compile(r"^=== ([a-z_]+) ===$")

# The two sides of the rules-version freeze, in the order the page prints them.
PILOT = "pilot"
FORWARD = "forward"
SIDES = (PILOT, FORWARD)

INSUFFICIENT = "insufficient"

MANIFEST = "input_manifest.json"
OUTCOME = "outcome.json"
BASELINES = "baselines.json"
ABNORMAL_RETURN = "abnormal_return_60_trading_days"

# Four decimals on every rate. One format for the whole page, so no cell can be
# shortened into looking better than the one above it.
PLACES = 4


class ScorecardError(Exception):
    """The page could not be rendered from the record. Never a filled-in default."""


@dataclass(frozen=True)
class Row:
    """One scorecard row: its key, who computes it, and where its answer lives."""

    key: str
    computed_by: str
    answered_in: str


# `docs/CHECKLIST.md` §8, in its order, with the Beneish M-score first.
ACCOUNTING_ROWS = (
    Row("beneish_m_score", "Python", BASELINES),
    Row("accruals_over_assets", "Python", BASELINES),
    Row("net_operating_assets", "Python", BASELINES),
    Row("note_cosine_similarity", "Python", BASELINES),
    Row("loughran_mcdonald_negative", "Python", BASELINES),
    Row("single_agent_accounting", "one model call",
        "control_single_agent_accounting.json"),
    Row("shuffled_accounting", "one model call", "control_shuffled_accounting.json"),
    Row("pipeline_accounting", "the pipeline", "prediction_accounting.json"),
)

PRESSURE_ROWS = (
    Row("naive_forecast", "Python", BASELINES),
    Row("piotroski_f_score", "Python", BASELINES),
    Row("ohlson_o_score", "Python", BASELINES),
    Row("altman_z_score", "Python", BASELINES),
    Row("short_interest_ratio", "Python", BASELINES),
    Row("single_agent_pressure", "one model call",
        "control_single_agent_pressure.json"),
    Row("shuffled_pressure", "one model call", "control_shuffled_pressure.json"),
    Row("pipeline_pressure", "the pipeline", "prediction_pressure.json"),
)

# The rows the two verdict sentences compare, per question. The first row of the
# accounting scorecard is the one the structure has to beat; the single-agent
# control is the one it has to beat to be more than decoration. Read off the
# order above rather than named again, so the two cannot drift apart.
FIRST_ROW = ACCOUNTING_ROWS[0].key


@dataclass(frozen=True)
class Run:
    """One prediction, and what happened to it."""

    ticker: str
    accession: str
    directory: Path
    side: str
    filing_date: str
    rules_version: str
    rules_version_frozen: str
    abnormal_return: float | None

    @property
    def up(self) -> bool:
        """True when the 60-trading-day abnormal return was positive.

        Exactly zero is not positive. There is no third answer here: a run with
        no outcome on record never reaches this property, because it is filtered
        out before anything is scored.
        """
        return self.abnormal_return is not None and self.abnormal_return > 0


@dataclass(frozen=True)
class Score:
    """One row on one side of the freeze. `None` where there is nothing to score."""

    answers: int
    insufficient: int
    scored: int
    brier: float | None
    hit_rate: float | None


# --- the template ------------------------------------------------------------


@functools.cache
def blocks() -> dict[str, str]:
    """The template's named blocks. Every word the page prints is in here."""
    text = TEMPLATE_PATH.read_text(encoding="utf-8")
    found: dict[str, list[str]] = {}
    name = None
    for line in text.splitlines():
        marker = BLOCK_MARKER.match(line)
        if marker:
            name = marker.group(1)
            found[name] = []
        elif name is not None:
            found[name].append(line)
    if "page" not in found:
        raise ScorecardError(f"{TEMPLATE_PATH} has no `page` block to render")
    return {key: "\n".join(lines).strip("\n") for key, lines in found.items()}


def _fill(block: str, **values) -> str:
    """One template block with its slots filled. A missing slot is an error."""
    words = blocks()
    if block not in words:
        raise ScorecardError(f"{TEMPLATE_PATH} has no `{block}` block")
    return Template(words[block]).substitute(**values)


def _rate(value: float) -> str:
    return f"{value:.{PLACES}f}"


def _side_label(side: str) -> str:
    """How the page names one side of the rules-version freeze."""
    return blocks()[f"side_{side}"]


# --- what a run left behind --------------------------------------------------


def _document(directory: Path, name: str) -> dict | None:
    """One JSON file out of a run, or None when the run does not carry it."""
    try:
        text = cutoff_guard.load_bundle_file(directory, name)
    except cutoff_guard.CutoffGuardError:
        return None
    try:
        loaded = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ScorecardError(f"{directory / name} is not readable JSON") from exc
    if not isinstance(loaded, dict):
        raise ScorecardError(f"{directory / name} is not a JSON object")
    return loaded


def _side(directory: Path, filed: str, frozen: str) -> str:
    """Which side of the rules-version freeze this filing fell on.

    `docs/CHECKLIST.md` §10: a filing already on EDGAR when the rules version was
    frozen is pilot, and one that did not exist then is the forward cycle. The
    day of the freeze counts as already there.
    """
    try:
        filing_date = cutoff_guard.parse_date(filed, "cutoff")
        freeze_date = cutoff_guard.parse_date(frozen, "rules_version_frozen")
    except cutoff_guard.CutoffGuardError as exc:
        raise ScorecardError(f"{directory / MANIFEST}: {exc}") from exc
    return PILOT if filing_date <= freeze_date else FORWARD


def _abnormal_return(directory: Path) -> float | None:
    """The realized 60-trading-day abnormal return, or None before the horizon."""
    outcome = _document(directory, OUTCOME)
    if outcome is None:
        return None
    value = outcome.get(ABNORMAL_RETURN)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ScorecardError(
            f"{directory / OUTCOME}: {ABNORMAL_RETURN} is {value!r} — an outcome "
            f"that is not a number is refused rather than read as a direction")
    return float(value)


def _run(ticker: str, directory: Path) -> Run:
    manifest = _document(directory, MANIFEST)
    if manifest is None:
        raise ScorecardError(
            f"{directory} has no {MANIFEST} — a run that does not say which rules "
            f"version it ran under cannot be placed on either side of the freeze")
    return Run(
        ticker=ticker,
        accession=directory.name,
        directory=directory,
        side=_side(directory, manifest.get("cutoff"),
                   manifest.get("rules_version_frozen")),
        filing_date=str(manifest.get("cutoff")),
        rules_version=str(manifest.get("rules_version")),
        rules_version_frozen=str(manifest.get("rules_version_frozen")),
        abnormal_return=_abnormal_return(directory),
    )


def load_runs(root) -> list[Run]:
    """Every run under a runs root, by company then accession."""
    folder = Path(root)
    if not folder.is_dir():
        raise ScorecardError(f"{folder} is not a directory — there is nothing to score")
    found = []
    for company in sorted(child for child in folder.iterdir() if child.is_dir()):
        for directory in cutoff_guard.prior_runs(folder, company.name):
            found.append(_run(company.name, directory))
    return found


# --- the arithmetic ----------------------------------------------------------


def answer(run: Run, row: Row):
    """This row's probability that the abnormal return was positive.

    A float, the string `insufficient`, or None when this run carries no answer
    for this row at all.
    """
    document = _document(run.directory, row.answered_in)
    if document is None:
        return None
    if row.answered_in == BASELINES:
        document = document.get(row.key)
        if document is None:
            return None
        if not isinstance(document, dict):
            raise ScorecardError(
                f"{run.directory / BASELINES}: {row.key} is not an object")
    direction = document.get("market_direction")
    if not isinstance(direction, dict) or "p_up" not in direction:
        return None
    p_up = direction["p_up"]
    if p_up == INSUFFICIENT:
        return INSUFFICIENT
    if isinstance(p_up, bool) or not isinstance(p_up, (int, float)):
        raise ScorecardError(
            f"{run.directory / row.answered_in}: {row.key} answered {p_up!r}, which "
            f"is neither a probability nor {INSUFFICIENT!r}")
    if not 0.0 <= float(p_up) <= 1.0:
        raise ScorecardError(
            f"{run.directory / row.answered_in}: {row.key} answered {p_up!r}, which "
            f"is outside nought to one")
    return float(p_up)


def _hit(p_up: float, up: bool) -> bool:
    """A direction hit. Exactly one half is on neither side, so it is no hit."""
    return (p_up > 0.5 and up) or (p_up < 0.5 and not up)


def score(runs: list[Run], row: Row) -> Score:
    """One row over the runs handed in. Brier and hit rate over what was scored."""
    answered = [(run, answer(run, row)) for run in runs]
    answered = [pair for pair in answered if pair[1] is not None]
    scored = [(run, value) for run, value in answered if value != INSUFFICIENT]
    insufficient = len(answered) - len(scored)
    if not scored:
        return Score(len(answered), insufficient, 0, None, None)
    brier = sum((value - (1.0 if run.up else 0.0)) ** 2
                for run, value in scored) / len(scored)
    hits = sum(1 for run, value in scored if _hit(value, run.up))
    return Score(len(answered), insufficient, len(scored), brier, hits / len(scored))


# --- the page ----------------------------------------------------------------


def _row_line(row: Row, side: str, one: Score) -> str:
    """One table line. A row with nothing to score carries words, not zeroes."""
    if one.scored:
        runs, brier, hit_rate = str(one.scored), _rate(one.brier), _rate(one.hit_rate)
    else:
        # Nothing answered at all reads differently from answered-but-abstained.
        nothing = blocks()["no_answer" if one.answers == 0 else "not_scored"]
        runs, brier, hit_rate = "0", nothing, nothing
    counted = (blocks()["no_answer"] if one.answers == 0 else
               _fill("insufficient_of", insufficient=one.insufficient,
                     answers=one.answers))
    return _fill("row", row=row.key, computed_by=row.computed_by,
                 side=_side_label(side), runs=runs, brier=brier,
                 hit_rate=hit_rate, insufficient=counted)


def _verdict(side: str, pipeline: Score, other: Score,
             beats: str, misses: str) -> str | None:
    """One comparison sentence, or None when there is nothing to compare."""
    if pipeline.scored == 0 or other.scored == 0:
        return None
    block = beats if pipeline.brier < other.brier else misses
    return _fill(block, side=_side_label(side),
                 pipeline=_rate(pipeline.brier), pipeline_runs=pipeline.scored,
                 other=_rate(other.brier), other_runs=other.scored)


def scores(rows: tuple[Row, ...], runs: list[Run]) -> dict[tuple[str, str], Score]:
    """One score per row per side of the freeze, computed once.

    Once, so that the table and the sentences underneath it cannot quote
    different numbers for the same row — which is the one way a page assembled
    in two passes could contradict itself and still look finished.
    """
    return {(row.key, side): score([run for run in runs if run.side == side], row)
            for row in rows for side in SIDES}


def _table(rows: tuple[Row, ...], scored: dict[tuple[str, str], Score]) -> str:
    """Every row, on every side of the freeze, in the checklist's order."""
    return "\n".join(_row_line(row, side, scored[(row.key, side)])
                     for row in rows for side in SIDES)


def _verdicts(rows: tuple[Row, ...], scored: dict[tuple[str, str], Score]) -> str:
    """What the page says about whether the layers beat what they have to beat."""
    keys = {row.key for row in rows}
    pipeline = next(row for row in rows if row.computed_by == "the pipeline")
    single_agent = next(row for row in rows if row.key.startswith("single_agent"))
    # The Beneish M-score is an accounting row, so the pressure table compares
    # against its single-agent control alone.
    against = [(key, f"pipeline_beats_the_{name}", f"pipeline_misses_the_{name}")
               for key, name in ((FIRST_ROW, "first_row"),
                                 (single_agent.key, "single_agent"))
               if key in keys]
    said = [_verdict(side, scored[(pipeline.key, side)], scored[(key, side)],
                     beats, misses)
            for side in SIDES for key, beats, misses in against]
    said = [sentence for sentence in said if sentence is not None]
    return "\n\n".join(said) if said else blocks()["no_verdict"]


def _run_list(runs: list[Run]) -> str:
    if not runs:
        return blocks()["no_runs"]
    return "\n".join(
        _fill("run_entry", ticker=run.ticker, accession=run.accession,
              filing_date=run.filing_date, rules_version=run.rules_version,
              rules_version_frozen=run.rules_version_frozen,
              side=_side_label(run.side),
              abnormal_return=(blocks()["no_answer"] if run.abnormal_return is None
                               else f"{run.abnormal_return:+.{PLACES}f}"))
        for run in runs)


def render(root) -> str:
    """The whole page, from a runs root, with nothing added on the way through."""
    found = load_runs(root)
    scorable = [run for run in found if run.abnormal_return is not None]
    accounting = scores(ACCOUNTING_ROWS, scorable)
    pressure = scores(PRESSURE_ROWS, scorable)
    return _fill(
        "page",
        accounting_rows=_table(ACCOUNTING_ROWS, accounting),
        accounting_verdicts=_verdicts(ACCOUNTING_ROWS, accounting),
        pressure_rows=_table(PRESSURE_ROWS, pressure),
        pressure_verdicts=_verdicts(PRESSURE_ROWS, pressure),
        run_list=_run_list(found),
    )


def main(argv: list[str] | None = None) -> int:
    wrong_interpreter = interpreter_pin.enforce()
    if wrong_interpreter:
        return wrong_interpreter

    parser = argparse.ArgumentParser(
        description="Render the scorecard from a runs directory.")
    parser.add_argument("--runs", default="runs", type=Path,
                        help="the runs root to score (default: runs)")
    args = parser.parse_args(argv)

    try:
        print(render(args.runs))
    except ScorecardError as refused:
        print(f"scorecard: {refused}", file=sys.stderr)
        return BAD_INPUT
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
