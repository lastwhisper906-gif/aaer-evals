"""The rendered scorecard, judged against the checklist and against arithmetic.

Two sources, and neither of them is the module under test.

**`docs/CHECKLIST.md` is the answer key for everything that is words.** §8 prints
the two scorecard row tables in the order the page has to print them, with the
Beneish M-score first, and §5 prints the two caveat sentences verbatim. Both are
read out of the document here and string-matched against the page, so the page
and the document cannot drift apart quietly and neither can be corrected by
editing the other.

**Hand arithmetic is the answer key for everything that is a number.** Every
Brier and hit rate below is written out term by term from the probabilities in
`tests/fixtures/scorecard/runs/`, which are inputs. Nothing here asks the module
what it computed and then agrees with it.

The fixture is seven runs. Four fell before the rules-version freeze on
2026-06-30 and are pilot — AAPL, CSCO, PANW, STX, in that order, whose 60-day
abnormal returns were up, up, down, down. Two fell after it and are the forward
cycle — NVDA up, QCOM down. The seventh, LFUS, was filed inside its horizon and
has left no outcome, so it is listed on the page and scored in nothing.
"""

from __future__ import annotations

import functools
import json
import shutil
from pathlib import Path

import pytest

from src import scorecard

REPO = Path(__file__).resolve().parent.parent
CHECKLIST = REPO / "docs" / "CHECKLIST.md"
FIXTURE = Path(__file__).resolve().parent / "fixtures" / "scorecard" / "runs"

PILOT = "pilot"
FORWARD = "forward"

# The runs on each side of the freeze, in the order the scorecard reads them:
# by company, then accession. The arithmetic below is written in this order too.
PILOT_RUNS = ("AAPL", "CSCO", "PANW", "STX")
FORWARD_RUNS = ("NVDA", "QCOM")


# --- what the checklist says -------------------------------------------------


def checklist_rows(heading: str) -> list[tuple[str, str]]:
    """One scorecard table out of `docs/CHECKLIST.md` §8: key, and who computes it."""
    lines = CHECKLIST.read_text(encoding="utf-8").splitlines()
    start = next(number for number, line in enumerate(lines) if heading in line)
    found = []
    for line in lines[start + 1:]:
        if found and not line.startswith("|"):
            break
        if not line.startswith("| `"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        found.append((cells[0].strip("`"), cells[-1]))
    return found


def checklist_caveats() -> list[str]:
    """The two block quotes §5 says go in the scorecard template, unwrapped."""
    text = CHECKLIST.read_text(encoding="utf-8")
    marker = "Two things go in the scorecard template next to this row"
    quotes: list[str] = []
    block: list[str] = []
    for line in text[text.index(marker):].splitlines()[1:]:
        if line.startswith("> "):
            block.append(line[2:])
        elif block:
            quotes.append(" ".join(block))
            block = []
            if len(quotes) == 2:
                break
    return quotes


def flat(text: str) -> str:
    """One line, single-spaced, block-quote markers off.

    A caveat is wrapped where it is written and quoted where it is printed, and
    neither is a difference in the sentence. Everything else is.
    """
    unquoted = " ".join(line.removeprefix(">").strip() for line in text.splitlines())
    return " ".join(unquoted.split())


# --- what the page says ------------------------------------------------------


@functools.cache
def page() -> str:
    return scorecard.render(FIXTURE)


def section(text: str, heading: str, until: str) -> str:
    return text.split(f"## {heading}")[1].split(f"## {until}")[0]


def table(text: str) -> list[list[str]]:
    """The cells of the one table in a section, header and rule dropped."""
    rows = []
    for line in text.splitlines():
        if not line.startswith("|"):
            if rows:
                break
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells[0] == "Row" or set(cells[0]) <= set("-"):
            continue
        rows.append(cells)
    return rows


def accounting() -> list[list[str]]:
    return table(section(page(), "Accounting reliability", "Financial pressure"))


def pressure() -> list[list[str]]:
    return table(section(page(), "Financial pressure", "The runs this was"))


def row_of(rows: list[list[str]], key: str, side: str) -> list[str]:
    found = [cells for cells in rows
             if cells[0] == key and cells[2].startswith(side)]
    assert len(found) == 1, f"{key} on the {side} side: found {len(found)} rows"
    return found[0]


def brier_of(rows, key, side) -> str:
    return row_of(rows, key, side)[4]


def hit_rate_of(rows, key, side) -> str:
    return row_of(rows, key, side)[5]


# --- the order, which is the checklist's ------------------------------------


def test_the_beneish_m_score_is_the_first_accounting_row():
    """§8: the first row, because if the layers do not beat it there is no
    structure to speak of. Read off the document rather than restated here."""
    first_in_the_checklist = checklist_rows("Accounting reliability scorecard")[0][0]
    assert first_in_the_checklist == "beneish_m_score"
    assert accounting()[0][0] == "beneish_m_score"


@pytest.mark.parametrize(
    "heading, rows",
    [("Accounting reliability scorecard", accounting),
     ("Financial pressure scorecard", pressure)])
def test_the_rows_are_in_the_checklists_order_and_say_who_computes_them(heading, rows):
    recorded = checklist_rows(heading)
    assert len(recorded) == 8, f"{heading}: the document lists {len(recorded)} rows"
    printed = rows()
    # Each row is printed once per side of the freeze, the sides adjacent.
    assert [cells[0] for cells in printed] == [key for key, _ in recorded
                                               for _ in (PILOT, FORWARD)]
    assert [cells[1] for cells in printed] == [computed_by for _, computed_by in recorded
                                               for _ in (PILOT, FORWARD)]


def test_every_row_carries_which_side_of_the_rules_version_freeze_it_came_from():
    """§10: the label goes in the table itself, never in a footnote, and a pilot
    number is a pipeline check rather than a result."""
    for rows in (accounting(), pressure()):
        sides = [cells[2] for cells in rows]
        assert all(side.startswith((PILOT, "forward cycle")) for side in sides), sides
        for side in sides:
            if side.startswith(PILOT):
                assert "pipeline check" in side
            else:
                assert "a result" in side


# --- the two caveats ---------------------------------------------------------


def test_both_caveat_sentences_travel_with_the_direction_rows():
    """§5 puts them next to this row, so they are printed under both tables."""
    caveats = checklist_caveats()
    assert len(caveats) == 2
    assert "Post-2006 drift is close to zero" in caveats[0]
    assert "lose roughly 58% of their margin after publication" in caveats[1]
    for question, until in (("Accounting reliability", "Financial pressure"),
                            ("Financial pressure", "The runs this was")):
        beside_the_rows = flat(section(page(), question, until))
        for caveat in caveats:
            assert flat(caveat) in beside_the_rows, f"{question} is missing: {caveat}"


def test_the_caveats_live_in_the_template_and_not_in_the_module():
    """The template is where the page's words are. A sentence in the module
    would be a sentence no reader of the template could see."""
    template = scorecard.TEMPLATE_PATH.read_text(encoding="utf-8")
    module = (REPO / "src" / "scorecard.py").read_text(encoding="utf-8")
    for caveat in checklist_caveats():
        assert flat(caveat) in flat(template)
        assert flat(caveat) not in flat(module)


# --- the arithmetic, term by term -------------------------------------------


def test_the_first_rows_pilot_score_is_the_hand_computation():
    """AAPL 0.6 up, CSCO 0.4 up, PANW 0.2 down, STX 0.3 down."""
    brier = ((0.6 - 1) ** 2 + (0.4 - 1) ** 2 + (0.2 - 0) ** 2 + (0.3 - 0) ** 2) / 4
    # 0.6 above one half on an up, 0.2 and 0.3 below it on two downs. 0.4 is
    # below one half on an up and is the miss.
    hit_rate = 3 / 4
    assert row_of(accounting(), "beneish_m_score", PILOT)[3] == "4"
    assert brier_of(accounting(), "beneish_m_score", PILOT) == f"{brier:.4f}" == "0.1625"
    assert hit_rate_of(accounting(), "beneish_m_score", PILOT) == f"{hit_rate:.4f}"


def test_the_first_rows_forward_score_is_the_hand_computation():
    """NVDA 0.8 up, QCOM 0.1 down — the two filings after the freeze."""
    brier = ((0.8 - 1) ** 2 + (0.1 - 0) ** 2) / 2
    assert brier_of(accounting(), "beneish_m_score", FORWARD) == f"{brier:.4f}" == "0.0250"
    assert hit_rate_of(accounting(), "beneish_m_score", FORWARD) == f"{2 / 2:.4f}"


def test_the_pipelines_pilot_score_is_the_hand_computation():
    """AAPL 0.9, CSCO 0.7, PANW 0.4, STX 0.2, against up, up, down, down."""
    brier = ((0.9 - 1) ** 2 + (0.7 - 1) ** 2 + (0.4 - 0) ** 2 + (0.2 - 0) ** 2) / 4
    assert brier_of(accounting(), "pipeline_accounting", PILOT) == f"{brier:.4f}" == "0.0750"
    assert hit_rate_of(accounting(), "pipeline_accounting", PILOT) == f"{4 / 4:.4f}"


def test_the_two_controls_are_scored_in_the_same_table_as_the_pipeline():
    """§8: every baseline and control on the same targets, none of them merged
    into the pipeline's number. The shuffled control was wrong every time."""
    single_agent = ((0.7 - 1) ** 2 + (0.6 - 1) ** 2 + (0.3 - 0) ** 2 + (0.4 - 0) ** 2) / 4
    shuffled = ((0.4 - 1) ** 2 + (0.3 - 1) ** 2 + (0.7 - 0) ** 2 + (0.6 - 0) ** 2) / 4
    assert brier_of(accounting(), "single_agent_accounting", PILOT) == \
        f"{single_agent:.4f}" == "0.1250"
    assert brier_of(accounting(), "shuffled_accounting", PILOT) == \
        f"{shuffled:.4f}" == "0.4250"
    assert hit_rate_of(accounting(), "shuffled_accounting", PILOT) == f"{0 / 4:.4f}"


def test_the_pressure_rows_are_the_hand_computation():
    """The pressure question scores the same target on its own rows."""
    piotroski = ((0.7 - 1) ** 2 + (0.4 - 1) ** 2 + (0.3 - 0) ** 2 + (0.6 - 0) ** 2) / 4
    pipeline = ((0.7 - 1) ** 2 + (0.2 - 0) ** 2) / 2
    assert brier_of(pressure(), "piotroski_f_score", PILOT) == f"{piotroski:.4f}" == "0.2250"
    # 0.7 and 0.3 on the right side of one half, 0.4 and 0.6 on the wrong one.
    assert hit_rate_of(pressure(), "piotroski_f_score", PILOT) == f"{2 / 4:.4f}"
    assert brier_of(pressure(), "pipeline_pressure", FORWARD) == f"{pipeline:.4f}" == "0.0650"


def test_an_insufficient_answer_is_counted_beside_the_score_and_not_scored():
    """§5 allows `insufficient`, and a model that abstains its way to a good
    Brier has not predicted anything — so the count is printed next to it."""
    cells = row_of(accounting(), "pipeline_accounting", FORWARD)
    brier = ((0.6 - 0) ** 2) / 1  # NVDA abstained; QCOM answered 0.6 and went down
    assert cells[3] == "1"
    assert cells[4] == f"{brier:.4f}" == "0.3600"
    assert cells[5] == f"{0 / 1:.4f}"
    assert cells[6] == "1 of 2"


def test_a_row_no_run_answered_keeps_its_place_and_carries_no_number():
    """A baseline nothing has computed yet is a row with no number in it, not a
    row that quietly disappears from the order."""
    for key in ("net_operating_assets", "note_cosine_similarity",
                "loughran_mcdonald_negative"):
        cells = row_of(accounting(), key, PILOT)
        assert cells[3:] == ["0", "not on record", "not on record", "not on record"]
    for key in ("naive_forecast", "ohlson_o_score", "altman_z_score",
                "short_interest_ratio", "shuffled_pressure"):
        assert row_of(pressure(), key, PILOT)[4] == "not on record"


def test_a_run_still_inside_its_horizon_is_listed_and_scored_in_nothing():
    """LFUS was filed after the freeze and has left no outcome. It appears at the
    foot of the page, and the forward denominators stay at two."""
    foot = page().split("## The runs this was computed from")[1]
    assert "LFUS 0000889331-26-000017" in foot
    assert "not on record" in [line for line in foot.splitlines()
                               if "LFUS" in line][0]
    assert row_of(accounting(), "beneish_m_score", FORWARD)[3] == "2"
    assert row_of(accounting(), "beneish_m_score", FORWARD)[6] == "0 of 2"


def test_every_run_is_listed_with_the_side_and_the_dates_it_was_placed_by():
    foot = page().split("## The runs this was computed from")[1]
    for ticker in PILOT_RUNS:
        line = [row for row in foot.splitlines() if row.startswith(f"- {ticker} ")][0]
        assert "pilot · pipeline check" in line
        assert "frozen 2026-06-30" in line
    for ticker in FORWARD_RUNS:
        line = [row for row in foot.splitlines() if row.startswith(f"- {ticker} ")][0]
        assert "forward cycle" in line


def test_a_runs_root_with_no_runs_in_it_renders_a_page_that_says_so(tmp_path):
    """The state the first cycle starts in. Every row keeps its place, the page
    says there is nothing to compare, and no cell is filled with a zero that
    could be read as a score."""
    empty = tmp_path / "runs"
    empty.mkdir()
    rendered = scorecard.render(empty)
    assert "No run has left an outcome on record" in rendered
    assert "Nothing to compare yet" in rendered
    rows = table(section(rendered, "Accounting reliability", "Financial pressure"))
    assert [cells[0] for cells in rows][:2] == ["beneish_m_score"] * 2
    assert all(cells[4] == "not on record" for cells in rows)


# --- what the page says when the answer is adverse ---------------------------


def test_the_scorecard_says_the_structure_adds_nothing_when_the_first_row_wins():
    """The forward pipeline scored 0.3600 against the Beneish M-score's 0.0250.
    §8 says that sentence in those words, and it is not softened."""
    verdicts = section(page(), "Accounting reliability", "Financial pressure")
    adverse = [line for line in verdicts.splitlines()
               if line.startswith("forward cycle")]
    assert len(adverse) == 1
    assert "does not beat the Beneish M-score's 0.0250" in adverse[0]
    assert adverse[0].endswith("The structure adds nothing.")
    # And the pilot side, where it did beat it, says so without the sentence.
    beaten = [line for line in verdicts.splitlines()
              if line.startswith(PILOT) and "Beneish" in line]
    assert len(beaten) == 1
    assert "beats the Beneish M-score's 0.1625" in beaten[0]
    assert "adds nothing" not in beaten[0]


def test_the_scorecard_says_the_structure_is_decoration_when_one_call_wins():
    """§8: if the layers do not beat the single-agent control, the structure is
    decoration, and the scorecard says so in those words. On the pressure
    question the control scored 0.0250 against the pipeline's 0.0750."""
    verdicts = section(page(), "Financial pressure", "The runs this was")
    adverse = [line for line in verdicts.splitlines() if line.startswith(PILOT)]
    assert len(adverse) == 1
    assert "does not beat the single-agent control's 0.0250" in adverse[0]
    assert adverse[0].endswith("The structure is decoration.")


# --- no hand edits anywhere in the path --------------------------------------


def copy_of(tmp_path: Path) -> Path:
    destination = tmp_path / "runs"
    shutil.copytree(FIXTURE, destination)
    return destination


def edit(directory: Path, name: str, change) -> None:
    """Change one number in one file of the record, the way a run would."""
    path = directory / name
    payload = json.loads(path.read_text(encoding="utf-8"))
    change(payload)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def test_the_page_follows_the_record_rather_than_the_other_way_round(tmp_path):
    """One probability changed in one run moves the Brier, moves the hit rate,
    and flips the verdict. Nothing on the page can be set any other way."""
    changed = copy_of(tmp_path)
    edit(changed / "AAPL" / "0000320193-26-000012", "prediction_accounting.json",
         lambda payload: payload["market_direction"].__setitem__("p_up", 0.1))

    rows = table(section(scorecard.render(changed),
                         "Accounting reliability", "Financial pressure"))
    brier = ((0.1 - 1) ** 2 + (0.7 - 1) ** 2 + (0.4 - 0) ** 2 + (0.2 - 0) ** 2) / 4
    assert brier_of(rows, "pipeline_accounting", PILOT) == f"{brier:.4f}" == "0.2750"
    assert hit_rate_of(rows, "pipeline_accounting", PILOT) == f"{3 / 4:.4f}"

    verdicts = section(scorecard.render(changed),
                       "Accounting reliability", "Financial pressure")
    pilot_line = [line for line in verdicts.splitlines()
                  if line.startswith(PILOT) and "Beneish" in line][0]
    assert pilot_line.endswith("The structure adds nothing.")


def test_a_tie_on_brier_is_not_beating(tmp_path):
    """The pipeline has to be strictly better. Equal is not better, and the
    sentence that follows from equal is the adverse one."""
    changed = copy_of(tmp_path)
    for ticker, accession, p_up in (("AAPL", "0000320193-26-000012", 0.8),
                                    ("CSCO", "0000858877-26-000015", 0.6),
                                    ("PANW", "0001327567-26-000009", 0.1),
                                    ("STX", "0001137789-26-000008", 0.3)):
        edit(changed / ticker / accession, "control_single_agent_pressure.json",
             lambda payload, value=p_up: payload["market_direction"].__setitem__(
                 "p_up", value))

    rendered = scorecard.render(changed)
    rows = table(section(rendered, "Financial pressure", "The runs this was"))
    assert brier_of(rows, "single_agent_pressure", PILOT) == \
        brier_of(rows, "pipeline_pressure", PILOT) == "0.0750"
    verdicts = section(rendered, "Financial pressure", "The runs this was")
    assert "The structure is decoration." in verdicts


def test_rendering_the_same_record_twice_gives_the_same_page():
    assert scorecard.render(FIXTURE) == scorecard.render(FIXTURE)


# --- what stops the render ---------------------------------------------------


def test_a_run_that_cannot_be_placed_on_a_side_of_the_freeze_is_refused(tmp_path):
    """A number that travels without that label eventually gets quoted without
    it, so an unplaceable run stops the page rather than defaulting to a side."""
    changed = copy_of(tmp_path)
    edit(changed / "AAPL" / "0000320193-26-000012", "input_manifest.json",
         lambda payload: payload.pop("rules_version_frozen"))
    with pytest.raises(scorecard.ScorecardError) as refused:
        scorecard.render(changed)
    assert "rules_version_frozen" in str(refused.value)


def test_a_run_with_no_manifest_is_refused(tmp_path):
    changed = copy_of(tmp_path)
    (changed / "AAPL" / "0000320193-26-000012" / "input_manifest.json").unlink()
    with pytest.raises(scorecard.ScorecardError):
        scorecard.render(changed)


def test_an_answer_that_is_neither_a_probability_nor_insufficient_stops_the_page(
        tmp_path):
    """Dropping it quietly would move a denominator nobody could see move."""
    changed = copy_of(tmp_path)
    edit(changed / "STX" / "0001137789-26-000008", "prediction_accounting.json",
         lambda payload: payload["market_direction"].__setitem__("p_up", "maybe"))
    with pytest.raises(scorecard.ScorecardError) as refused:
        scorecard.render(changed)
    assert "'maybe'" in str(refused.value)


def test_a_probability_outside_nought_to_one_stops_the_page(tmp_path):
    changed = copy_of(tmp_path)
    edit(changed / "STX" / "0001137789-26-000008", "baselines.json",
         lambda payload: payload["beneish_m_score"]["market_direction"].__setitem__(
             "p_up", 1.4))
    with pytest.raises(scorecard.ScorecardError):
        scorecard.render(changed)


def test_an_outcome_that_is_not_a_number_stops_the_page(tmp_path):
    changed = copy_of(tmp_path)
    edit(changed / "QCOM" / "0000804328-26-000033", "outcome.json",
         lambda payload: payload.__setitem__("abnormal_return_60_trading_days", "down"))
    with pytest.raises(scorecard.ScorecardError):
        scorecard.render(changed)


def test_a_runs_root_that_is_not_there_is_refused(tmp_path):
    with pytest.raises(scorecard.ScorecardError):
        scorecard.render(tmp_path / "nothing_here")


# --- the rules the arithmetic rests on ---------------------------------------


@pytest.mark.parametrize("p_up, up, expected", [
    (0.9, True, True), (0.9, False, False),
    (0.1, False, True), (0.1, True, False),
    # Exactly one half is on neither side of one half.
    (0.5, True, False), (0.5, False, False),
])
def test_a_direction_hit_needs_the_probability_off_one_half(p_up, up, expected):
    assert scorecard._hit(p_up, up) is expected


def test_an_abnormal_return_of_exactly_zero_is_not_positive(tmp_path):
    """Positive means above zero. A flat outcome is a down, not a half-hit."""
    changed = copy_of(tmp_path)
    edit(changed / "AAPL" / "0000320193-26-000012", "outcome.json",
         lambda payload: payload.__setitem__("abnormal_return_60_trading_days", 0.0))
    rows = table(section(scorecard.render(changed),
                         "Accounting reliability", "Financial pressure"))
    # AAPL now counts as a down, so the pipeline's 0.9 becomes its worst term.
    brier = ((0.9 - 0) ** 2 + (0.7 - 1) ** 2 + (0.4 - 0) ** 2 + (0.2 - 0) ** 2) / 4
    assert brier_of(rows, "pipeline_accounting", PILOT) == f"{brier:.4f}" == "0.2750"
    # And the hit it would have been is gone with it.
    assert hit_rate_of(rows, "pipeline_accounting", PILOT) == f"{3 / 4:.4f}"


# --- the command line --------------------------------------------------------


def test_the_command_line_prints_the_page(capsys):
    assert scorecard.main(["--runs", str(FIXTURE)]) == 0
    assert capsys.readouterr().out.strip() == page().strip()


def test_the_command_line_refuses_a_root_it_cannot_score(capsys, tmp_path):
    assert scorecard.main(["--runs", str(tmp_path / "nothing_here")]) == 2
    assert "scorecard:" in capsys.readouterr().err
