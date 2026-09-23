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
    control_single_agent_accounting.json, control_single_agent_pressure.json

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
* A tie on Brier is not beating, and neither is a margin the page cannot show.
  The Briers compared are exact rationals over the decimals the runs carry, and
  the win has to survive the four places printed. Float sums call a tie a win in
  the last bit (`0.0075 beats 0.0075`); rounding those sums moves the seam to
  the rounding boundary (`0.5012 beats 0.5013`, both of them 2.005/4); and exact
  arithmetic alone lets `0.5000 beat 0.5000` on twenty-five millionths.
* **A verdict sentence compares two rows only on the runs both of them
  answered.** A Brier over four runs and a Brier over three are two
  measurements, not a comparison: a row that declines the run it would have got
  wrong is scored on what is left while the row beside it carries that run in
  full, and the page reads the missing term as a win. The sentence therefore
  says how many runs it was made on and how many it set aside -- and set aside
  is every other scorable run on that side, so that a run *both* rows declined
  is counted rather than falling between the two numbers. Two rows with no run
  in common get no sentence at all rather than a comparison across different
  runs. The table above it is unchanged: each row there is still scored over
  everything it answered.
* A `p_up` that is neither a probability nor `insufficient` stops the render
  rather than being dropped quietly.
* So does an answer that is there but has no `p_up` to read: an answer file,
  or a `baselines.json` entry (one written as null too), with no
  `market_direction` object or with one that carries no `p_up`. Absent is a file or key that is not there at all;
  a present answer with nothing in it is malformed, and reading it as absent
  would take the run out of that row's count and out of every comparison it
  is in, with nothing on the page to say so.

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
from fractions import Fraction
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
    brier: Fraction | None
    hit_rate: float | None


@dataclass(frozen=True)
class Comparison:
    """Two rows scored on exactly the runs both of them put a probability on.

    `runs` is how many runs that was and `set_aside` is every other run on that
    side of the freeze -- one row abstained, or both did, or one of them left no
    answer at all. The two add up to the side's whole scorable set on purpose: a
    count of only the runs *one* row declined says nought on the side where both
    declined the same run, which is an abstention hidden by the arithmetic that
    reports abstentions. Both Briers are over `runs`, so a sentence built from
    this is a comparison rather than two measurements printed side by side.
    `runs` of nought means the two rows answered nothing in common and there is
    no sentence to write.
    """

    runs: int
    set_aside: int
    pipeline: Fraction | None
    other: Fraction | None


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


def _rate(value: Fraction) -> str:
    """An exact Brier as the page prints it. The rounding happens here alone."""
    return f"{float(value):.{PLACES}f}"


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
    for this row at all -- no file, or no key in `baselines.json`. An answer
    that is there but carries no probability is refused.
    """
    document = _document(run.directory, row.answered_in)
    if document is None:
        return None
    if row.answered_in == BASELINES:
        # A key that is not there is a row that did not run; a key written as
        # null is an entry with nothing in it, and falls through to the refusal.
        if row.key not in document:
            return None
        document = document[row.key]
        if not isinstance(document, dict):
            raise ScorecardError(
                f"{run.directory / BASELINES}: {row.key} is not an object")
    # The file (or the baseline's entry) is there, so the row did answer this
    # run; an answer with no probability in it is malformed, not absent. Read as
    # None it would leave this row's denominator and every comparison's shared
    # set with nothing said -- the quiet drop the edge list forbids.
    direction = document.get("market_direction")
    if not isinstance(direction, dict):
        raise ScorecardError(
            f"{run.directory / row.answered_in}: {row.key} carries no "
            f"market_direction object -- an answer file that is present but "
            f"malformed is refused rather than dropped from the ratio")
    if "p_up" not in direction:
        raise ScorecardError(
            f"{run.directory / row.answered_in}: {row.key} has a market_direction "
            f"with no p_up -- an answer file that is present but malformed is "
            f"refused rather than dropped from the ratio")
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


def _answers(runs: list[Run], row: Row) -> list[tuple[Run, float | str]]:
    """What this row said on each run that carries an answer for it at all."""
    said = [(run, answer(run, row)) for run in runs]
    return [(run, value) for run, value in said if value is not None]


def _probabilities(runs: list[Run], row: Row) -> dict[Run, float]:
    """The runs this row put a probability on, and the probability it put."""
    return {run: value for run, value in _answers(runs, row)
            if value != INSUFFICIENT}


def _brier(scored: list[tuple[Run, float]]) -> Fraction:
    """Mean squared error against the direction that happened, exactly.

    Exactly, because two Briers that are equal in arithmetic need not be equal
    in binary, and the page has one sentence that turns on whether they are:
    a tie on Brier is not beating. Summed as floats, 0.9, 0.9, 0.0, 0.1 and
    0.9, 1.0, 0.1, 0.1 on up, up, down, down land one bit apart although both
    are three four-hundredths, and rounding the sums to the four places the
    page prints only moves the seam -- 0.0, 0.0, 0.05, 0.05 against 0.0, 0.2,
    0.25, 0.55 are both 2.005/4 and straddle a rounding boundary, so the page
    printed 0.5012 beating 0.5013 on an exact tie.

    `p_up` and the outcome are decimal literals in the run's own JSON, so
    `Fraction(str(...))` recovers the decimal the record carries and the
    arithmetic over it has no seam anywhere. Never over nothing: the caller
    hands in the runs that were scored.
    """
    return sum((Fraction(str(value)) - (1 if run.up else 0)) ** 2
               for run, value in scored) / len(scored)


def score(runs: list[Run], row: Row) -> Score:
    """One row over the runs handed in. Brier and hit rate over what was scored."""
    answered = _answers(runs, row)
    scored = [(run, value) for run, value in answered if value != INSUFFICIENT]
    insufficient = len(answered) - len(scored)
    if not scored:
        return Score(len(answered), insufficient, 0, None, None)
    hits = sum(1 for run, value in scored if _hit(value, run.up))
    return Score(len(answered), insufficient, len(scored), _brier(scored),
                 hits / len(scored))


def compare(runs: list[Run], pipeline: Row, other: Row) -> Comparison:
    """Two rows scored on the runs both of them answered, and what that left out.

    Each row's own Brier is over whatever that row answered, and two of those
    are not comparable when the two rows answered different runs. A row that
    declines a run drops it from its own denominator while the row beside it
    carries that run in full, and the page would read the missing term as a
    win: `insufficient` is an answer, and a row that abstains its way to a good
    Brier has not predicted anything, which is the line `docs/CHECKLIST.md` §5
    draws. So the comparison is made on the runs both rows put a probability
    on, and every run it could not use is counted beside it rather than
    disappearing.
    """
    mine = _probabilities(runs, pipeline)
    theirs = _probabilities(runs, other)
    shared = [run for run in runs if run in mine and run in theirs]
    # Every run on this side that the comparison could not use, not only the
    # ones exactly one row declined. `runs + set_aside` is the side's whole
    # scorable set, so no abstention can fall between the two counts.
    set_aside = len(runs) - len(shared)
    if not shared:
        return Comparison(0, set_aside, None, None)
    return Comparison(len(shared), set_aside,
                      _brier([(run, mine[run]) for run in shared]),
                      _brier([(run, theirs[run]) for run in shared]))


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


def _verdict(side: str, made: Comparison, beats: str, misses: str) -> str | None:
    """One comparison sentence, or None when the two rows share no run.

    The sentence carries one run count because there is one: both Briers in it
    are over the same runs. It carries the set-aside count beside that, so a
    verdict resting on a handful of runs cannot be read without seeing how many
    were left out of it.

    Beaten takes both: `_brier` is exact, so a tie is a tie whatever order the
    terms arrived in, and the win then has to survive the four places the page
    prints. Exact arithmetic alone would let the page say `0.5000 beats
    0.5000` on a margin of twenty-five millionths, and four places alone are
    not enough either -- rounding two float sums of one exact number lands
    either side of a boundary. Rounding is monotonic, so a win that survives it
    is a real one; a margin that does not is one no reader can check against
    the numbers in front of them.
    """
    if made.runs == 0:
        return None
    pipeline, other = _rate(made.pipeline), _rate(made.other)
    block = beats if float(pipeline) < float(other) else misses
    return _fill(block, side=_side_label(side), runs=made.runs,
                 set_aside=made.set_aside, pipeline=pipeline, other=other)


def scores(rows: tuple[Row, ...], runs: list[Run]) -> dict[tuple[str, str], Score]:
    """One score per row per side of the freeze, for the table.

    Computed once, so no two cells of the table can quote different numbers for
    the same row. The sentences underneath the table are not built from this:
    they are comparisons, and a comparison is scored on the runs both of its
    rows answered rather than on each row's own. Where those differ the
    sentence says which runs it was made on.
    """
    return {(row.key, side): score([run for run in runs if run.side == side], row)
            for row in rows for side in SIDES}


def _table(rows: tuple[Row, ...], scored: dict[tuple[str, str], Score]) -> str:
    """Every row, on every side of the freeze, in the checklist's order."""
    return "\n".join(_row_line(row, side, scored[(row.key, side)])
                     for row in rows for side in SIDES)


def _verdicts(rows: tuple[Row, ...], runs: list[Run]) -> str:
    """What the page says about whether the layers beat what they have to beat."""
    by_key = {row.key: row for row in rows}
    pipeline = next(row for row in rows if row.computed_by == "the pipeline")
    single_agent = next(row for row in rows if row.key.startswith("single_agent"))
    # The Beneish M-score is an accounting row, so the pressure table compares
    # against its single-agent control alone.
    against = [(by_key[key], f"pipeline_beats_the_{name}",
                f"pipeline_misses_the_{name}")
               for key, name in ((FIRST_ROW, "first_row"),
                                 (single_agent.key, "single_agent"))
               if key in by_key]
    said = [_verdict(side,
                     compare([run for run in runs if run.side == side],
                             pipeline, other),
                     beats, misses)
            for side in SIDES for other, beats, misses in against]
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
    return _fill(
        "page",
        accounting_rows=_table(ACCOUNTING_ROWS, scores(ACCOUNTING_ROWS, scorable)),
        accounting_verdicts=_verdicts(ACCOUNTING_ROWS, scorable),
        pressure_rows=_table(PRESSURE_ROWS, scores(PRESSURE_ROWS, scorable)),
        pressure_verdicts=_verdicts(PRESSURE_ROWS, scorable),
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
