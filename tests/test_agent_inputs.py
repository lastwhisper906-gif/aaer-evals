"""The layer table, asserted file by file, and the root that makes it hold.

The expected values come from `docs/INPUT_SPEC.md`: its layer table says what
each layer sees and never sees, and its §6 block names the files. Both are read
out of the document here — the three table rows verbatim, the file names parsed
out of the block — so this test fails on the day the spec changes rather than
going on judging a rule nobody holds any more. The per-agent lists below were
read off those two places by hand, file by file, and are written out in full:
a directory-by-directory check ("the reader has five files") passes a directory
holding the wrong five.

Two other documents are read the same way, because the rule they carry is one
this router has to hold: `docs/CHECKLIST.md` §7 names the keys a prediction
gives a probability to, which is what may not travel into a reader's input, and
each prompt in `.claude/agents/` names the one file its agent writes, which is
what its own directory legitimately holds afterwards.

Nothing here writes into the real `runs/`. Every run directory is under
pytest's `tmp_path`.

    python3.12 -m pytest tests/test_agent_inputs.py -q
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from src import agent_inputs
from src.agent_inputs import AgentInputError

REPO_ROOT = Path(__file__).resolve().parent.parent
INPUT_SPEC = REPO_ROOT / "docs" / "INPUT_SPEC.md"
CHECKLIST = REPO_ROOT / "docs" / "CHECKLIST.md"
PROMPTS = REPO_ROOT / ".claude" / "agents"
# Where the two comparer and two supervisor definitions went on 2026-10-06.
ARCHIVED_PROMPTS = REPO_ROOT / "archive" / "agents"

# docs/INPUT_SPEC.md, the rows of the layer table, verbatim.
LAYER_TABLE = (
    "| readers | the filing bundle for one company "
    "| prices, short interest, any other company |",
    "| comparers | both reader reports plus the market table — run only for the reaction-window labels | any filing |",
    "| accounting and financial analysts | the two reader reports and `calculator_filings_only.json` | any filing, any price, the market table |",
    "| valuation analyst | the calculator with the price at the cutoff (before its drivers, then with the DCF run on them), both checked analyses, and of the MD&A and the earnings release only the paragraphs the notes reader flagged, each verbatim, the manifest recording the trim | a price after the cutoff, the market table |",
    "| supervisor (retired from the live pipeline on 2026-09-28; its runs stay on record) | the four reports, and the rules version's checklist keys and output schema | any filing, the market table |",
)

# What each directory holds, sorted, read off the table above and off §1's
# "Goes to" column. The readers split the filing bundle between them — the
# numbers reader takes what Python computed, the notes-text reader takes the
# prose — and neither takes a price. `input_8k.md` is in both because §1 sends
# the earnings-release figures to one and the 8-K bodies to the other and
# `src/assemble_bundle.py` writes them into one file. `input_controls.md` is
# the auditor's report, Item 9A and Item 4, which §1 sends to the notes-text
# reader.
EXPECTED = {
    "numbers-reader": (
        "input_8k.md",
        "input_companyfacts.json",
        "input_numbers.json",
        "input_prior_predictions.md",
        "input_trends.json",
    ),
    "notes-text-reader": (
        "input_8k.md",
        "input_controls.md",
        "input_exhibits.md",
        "input_mdna.md",
        "input_notes.md",
        "input_notes_history.md",
        "input_prior_predictions.md",
        "input_risk_factors.md",
    ),
    # docs/INPUT_SPEC.md's layer table, the owner's decision of 2026-09-28.
    "accounting-analyst": (
        "calculator_filings_only.json",
        "report_notes_text.md",
        "report_numbers.md",
    ),
    "financial-analyst": (
        "calculator_filings_only.json",
        "report_notes_text.md",
        "report_numbers.md",
    ),
    "valuation-analyst": (
        "analysis_accounting.json",
        "analysis_financial.json",
        "calculator_before_drivers.json",
        "input_8k.md",
        "input_mdna.md",
    ),
    "valuation-analyst-second-pass": (
        "analysis_accounting.json",
        "analysis_financial.json",
        "assumptions.json",
        "calculator.json",
        "input_8k.md",
        "input_mdna.md",
    ),
}

READERS = ("numbers-reader", "notes-text-reader")
ANALYSTS = ("accounting-analyst", "financial-analyst")
# Retired from the live pipeline on 2026-10-06; their definitions are archived.
COMPARERS = ("numbers-vs-market", "notes-vs-market")

# The price file. "prices, short interest" is one file in the bundle: the
# market table §4 describes, whose last three columns are the short interest.
PRICE_FILE = "input_market.json"

# Every key the prediction schema in `docs/CHECKLIST.md` §7 gives a probability
# to, read off the block by hand: `checklist[].confidence`,
# `events[].p_within_horizon`, `explanations[].realization_p` and
# `market_direction.p_up`. Written out one by one, because a gate covering two
# of the four calls a file clean while a prior run's own score sits in it.
# `continuous[]`'s `point`, `low` and `high` are an interval, not a probability.
PREDICTION_PROBABILITY_KEYS = ("confidence", "p_within_horizon",
                               "realization_p", "p_up")

# What each agent writes, read off the "Write `x`. Nothing else, anywhere."
# line of its own prompt in `.claude/agents/`.
WRITES = {
    "numbers-reader": "report_numbers.md",
    "notes-text-reader": "report_notes_text.md",
    "accounting-analyst": "analysis_accounting.json",
    "financial-analyst": "analysis_financial.json",
    "valuation-analyst": "assumptions.json",
    "valuation-analyst-second-pass": "analysis_valuation.json",
}


def spec_bundle_names() -> tuple[str, ...]:
    """Every file name in §6's block, out of the document."""
    section = INPUT_SPEC.read_text(encoding="utf-8").split(
        "## 6. The committed bundle", 1)[1]
    block = section.split("```", 2)[1]
    names = [line.split()[0] for line in block.splitlines() if line.strip()]
    return tuple(name for name in names
                 if re.fullmatch(r"[a-z0-9_]+\.(json|md)", name))


def _run_directory(tmp_path: Path, *, skip: tuple[str, ...] = ()) -> Path:
    """A run directory holding every file the bundle names, one company.

    The bytes name the file, so a file that reached the wrong directory shows up
    as the wrong content and not only as the wrong name. `input_controls.md` is
    the ninth file `src/assemble_bundle.py` writes; §6 does not list it and §1
    requires what it holds.
    """
    run = tmp_path / "runs" / "AAPL" / "0000320193-25-000073"
    run.mkdir(parents=True)
    for name in spec_bundle_names() + ("input_controls.md",):
        if name in skip:
            continue
        (run / name).write_text(f"this is {name}\n", encoding="utf-8")
    # The manifest is routed to no agent, and a comparer or a supervisor reads
    # it for whether the run has a market table, so it is the JSON a run's is.
    # It carries the quote gate's drop list, empty: the valuation analyst's
    # directory is built after the gate, and the router refuses a run with no
    # record that the gate ran.
    if "input_manifest.json" not in skip:
        (run / "input_manifest.json").write_text(
            '{"accession": "0000320193-25-000073", "ticker": "AAPL", "dropped_items": []}\n',
            encoding="utf-8")
    return run


def _names(directory: Path) -> list[str]:
    return sorted(path.name for path in directory.iterdir())


def _ancestors(root: Path, stop: Path):
    """Every directory on the way up from `root`, stopping below `stop`."""
    for parent in root.parents:
        if parent == stop:
            return
        yield parent


# --- the source these expectations were read off ------------------------------

def test_the_layer_table_still_says_what_these_expectations_were_read_off():
    text = INPUT_SPEC.read_text(encoding="utf-8")
    for row in LAYER_TABLE:
        assert row in text, f"docs/INPUT_SPEC.md no longer carries: {row}"


def test_every_file_the_bundle_names_is_a_file_this_router_knows():
    named = spec_bundle_names()
    assert len(named) >= 20, "§6's block did not parse; the expectations below "\
                             "would be checked against nothing"
    unknown = sorted(set(named) - set(agent_inputs.BUNDLE_CATALOGUE))
    assert unknown == [], f"§6 names files nobody routed or refused: {unknown}"


def test_the_router_knows_no_file_the_bundle_does_not_name():
    """The other direction: every file the router knows is one §6 names.

    `input_controls.md` is the one the catalogue adds, for the reason written
    beside it. Anything else is a name the bundle has retired and the router
    still waves through -- the two shuffled-control files, the day the owner
    retired that control, until this was asked.
    """
    named = set(spec_bundle_names()) | {"input_controls.md"}
    stale = sorted(set(agent_inputs.BUNDLE_CATALOGUE) - named)
    assert stale == [], f"the router knows files §6 no longer names: {stale}"


def test_the_six_agents_are_the_six_prompts_committed():
    prompts = {path.stem for path in PROMPTS.glob("*.md")}
    # refute-check and reproduce-check are verification subagents, not layers, and
    # analysis-grader is the owner's model grader (evals/), run on published outputs
    # by src/grade_run.py: none of the three feeds a later stage.
    # One definition may run in two directories -- the valuation analyst's two
    # passes -- so the rule is on the definitions the directories run.
    assert {agent.prompt for agent in agent_inputs.AGENTS.values()} == \
        prompts - {"refute-check", "reproduce-check", "analysis-grader"}


@pytest.mark.parametrize("agent", COMPARERS)
def test_a_comparer_prompt_says_it_holds_both_reader_reports(agent):
    """The table and the prompts are the same rule written twice.

    This repository has already shipped a layer table saying a comparer sees
    both reader reports beside comparer prompts saying each sees one, so a
    directory the table calls correct was one its own prompt called broken.
    """
    prompt = (ARCHIVED_PROMPTS / f"{agent}.md").read_text(encoding="utf-8")
    for report in ("report_numbers.md", "report_notes_text.md"):
        assert report in prompt


@pytest.mark.parametrize("agent", sorted(WRITES))
def test_each_prompt_names_the_one_file_its_agent_writes(agent):
    """Where an agent's output lands is decided by its prompt, not guessed here.

    Each prompt says "Write `x`. Nothing else, anywhere.", and each agent has
    `Write` and a session rooted at its own directory, so `x` lands there and
    nowhere else. That is why a directory holding it after the run is clean.
    """
    prompt = (PROMPTS / f"{agent_inputs.AGENTS[agent].prompt}.md").read_text(encoding="utf-8")
    assert f"Write `{WRITES[agent]}`" in prompt
    assert agent_inputs.AGENTS[agent].writes == WRITES[agent]


def test_the_prediction_schema_still_names_every_probability_the_gate_covers():
    """The four keys the gate below is asserted against are §7's, still."""
    section = CHECKLIST.read_text(encoding="utf-8").split(
        "### The two predictions", 1)[1]
    schema = section.split("```", 2)[1]
    for key in PREDICTION_PROBABILITY_KEYS:
        assert f'"{key}"' in schema, f"docs/CHECKLIST.md §7 no longer names {key}"


# --- file by file -------------------------------------------------------------

@pytest.mark.parametrize("agent", READERS)
def test_a_reader_directory_holds_the_filing_bundle_and_no_price_file(agent, tmp_path):
    run = _run_directory(tmp_path)
    record = agent_inputs.build(run, agent)
    root = agent_inputs.session_root(run, agent)

    # §6 names three files no builder writes yet and the owner's layer table
    # (evals/regression/mechanical.py LAYER_SEES) does not: placed, they fail the
    # owner's layers_hold, so they are withheld until that table names them
    assert _names(root) == [name for name in EXPECTED[agent]
                            if name not in agent_inputs.NOT_BUILT_YET]
    assert sorted(record["withheld"]) == sorted(set(EXPECTED[agent]) & set(agent_inputs.NOT_BUILT_YET))
    assert PRICE_FILE not in _names(root)
    assert [name for name in _names(root) if name.startswith("report_")] == []
    assert [name for name in _names(root) if name.startswith("prediction_")] == []


@pytest.mark.parametrize("agent", sorted(agent_inputs.RETIRED_AGENTS))
def test_a_retired_agent_gets_no_directory(agent, tmp_path):
    """The comparers are Python and the supervisors are archived: nothing builds
    a directory for either, and the refusal says why."""
    run = _run_directory(tmp_path)
    with pytest.raises(AgentInputError, match="retired"):
        agent_inputs.build(run, agent)
    assert not agent_inputs.agents_root(run).exists()
    assert not (PROMPTS / f"{agent}.md").exists()
    assert (ARCHIVED_PROMPTS / f"{agent}.md").is_file()


def test_every_routed_file_arrives_verbatim(tmp_path):
    """The right name over the wrong bytes is the same leak with a better shape."""
    run = _run_directory(tmp_path)
    agent_inputs.build_all(run)
    for agent in agent_inputs.AGENTS:
        root = agent_inputs.session_root(run, agent)
        spec = agent_inputs.AGENTS[agent]
        for name in _names(root):
            # The valuation analyst's prose is the run's copy trimmed to the
            # flagged paragraphs (2026-10-06), and the planted file holds no
            # `[id]` paragraph, so the trim is the whole file, written out here
            # by hand rather than through the trim; the trim itself is judged
            # against a hand-written file below.
            assert (root / name).read_bytes() == (run / name).read_bytes() \
                == f"this is {name}\n".encode()


def test_no_file_reaches_an_agent_that_nobody_routed(tmp_path):
    run = _run_directory(tmp_path)
    agent_inputs.build_all(run)
    routed = {name for agent in agent_inputs.AGENTS
              for name in _names(agent_inputs.session_root(run, agent))}
    # input_manifest.json, the predictions, the baselines, the explanations and
    # the four controls are the run's record. No layer reads them.
    assert "input_manifest.json" not in routed
    assert routed == set().union(*(set(names) for names in EXPECTED.values())) \
        - set(agent_inputs.NOT_BUILT_YET)


# --- the session root ---------------------------------------------------------

def test_the_session_root_is_the_agent_s_own_directory(tmp_path):
    run = _run_directory(tmp_path)
    agent_inputs.build_all(run)
    roots = {agent: agent_inputs.session_root(run, agent)
             for agent in agent_inputs.AGENTS}

    for agent, root in roots.items():
        assert root.is_dir()
        assert root.name == agent
        # Not the run directory, which holds the bundle, and not the directory
        # that holds the six: rooting a session at either hands the agent every
        # other agent's files by walking down.
        assert root != run
        assert root != agent_inputs.agents_root(run)
        for other, elsewhere in roots.items():
            if other == agent:
                continue
            assert elsewhere not in root.parents
            assert root not in elsewhere.parents


def test_nothing_inside_a_session_root_resolves_outside_it(tmp_path):
    """Files, not links. A link's ancestors are the bundle's."""
    run = _run_directory(tmp_path)
    agent_inputs.build_all(run)
    for agent in agent_inputs.AGENTS:
        root = agent_inputs.session_root(run, agent)
        for path in root.rglob("*"):
            assert not path.is_symlink()
            assert root.resolve() in path.resolve().parents
        assert agent_inputs.escapes(root) == []


def test_climbing_out_of_a_session_root_meets_no_other_agent_directory(tmp_path):
    """Walk up from the root, and find nothing an agent may not see.

    `docs/INPUT_SPEC.md` says what "unreachable" means here: "The agent's
    session is **rooted at that directory**, so a sibling directory is not
    merely undeclared, it is unreachable." The spec expects the siblings to
    exist — six directories that coexist under one run share an ancestor, and no
    tree can do otherwise — and puts the last step, the one out of the root, on
    the session root rather than on the filesystem.

    So this asserts everything up to that step: no other agent's directory is on
    the way up, and every directory on the way up holds no file at all, so the
    step out of a session root yields no report, no filing and no market table.
    The run directory above that holds the committed bundle, because it is the
    record of what was fetched, and the session root is what stands between a
    reader and it.
    """
    run = _run_directory(tmp_path)
    agent_inputs.build_all(run)
    found = agent_inputs.agent_directories(run)
    assert sorted(found.values()) == sorted(agent_inputs.AGENTS)

    for root, agent in found.items():
        # One step out has to land somewhere, and it lands on no file at all:
        # not a report, not a filing, not the market table. A root beside the
        # bundle would have `input_market.json` one `..` away.
        loose = sorted(path.name for path in root.parent.iterdir() if path.is_file())
        assert loose == [], f"{root.parent} holds {loose}, one step out of {agent}"
        for ancestor in _ancestors(root, stop=run):
            assert ancestor not in found, (
                f"{agent} sits inside {found.get(ancestor)}'s directory")
            assert [path for path in ancestor.iterdir() if path.is_file()] == []

    # The one directory the step out of a root lands in: six directories and
    # nothing readable. A seventh entry here — a stray report, a scratch file —
    # is a file every agent reaches with one `..`.
    holder = agent_inputs.agents_root(run)
    assert sorted(path.name for path in holder.iterdir()) == sorted(agent_inputs.AGENTS)
    assert all(path.is_dir() for path in holder.iterdir())


def test_a_clean_build_reports_no_violation(tmp_path):
    run = _run_directory(tmp_path)
    agent_inputs.build_all(run)
    assert agent_inputs.isolation_violations(run) == []


# --- the checks have teeth ----------------------------------------------------

def test_a_symlink_into_the_bundle_is_a_broken_boundary(tmp_path):
    """The shape a reader would get the market table in without a copy."""
    run = _run_directory(tmp_path)
    agent_inputs.build_all(run)
    root = agent_inputs.session_root(run, "numbers-reader")
    (root / PRICE_FILE).symlink_to(Path("..") / ".." / PRICE_FILE)

    broken = agent_inputs.isolation_violations(run)
    assert any("resolves to" in line for line in broken)
    assert any("never sees" in line for line in broken)
    assert agent_inputs.escapes(root) != []


def test_grouping_the_six_by_layer_puts_a_sibling_one_step_out(tmp_path):
    """Right files, wrong tree: the other reader is one `..` from this one."""
    run = _run_directory(tmp_path)
    grouped = agent_inputs.agents_root(run) / "readers"
    for agent in READERS:
        (grouped / agent).mkdir(parents=True)
        for name in EXPECTED[agent]:
            (grouped / agent / name).write_bytes((run / name).read_bytes())

    broken = agent_inputs.isolation_violations(run)
    assert any("not at its session root" in line for line in broken)
    # And plainly: the other reader is one step out of this one.
    assert "notes-text-reader" in {path.name for path in
                                   (grouped / "numbers-reader").parent.iterdir()}


def test_one_agent_s_directory_inside_another_s_is_a_broken_boundary(tmp_path):
    run = _run_directory(tmp_path)
    agent_inputs.build_all(run)
    nested = agent_inputs.session_root(run, "accounting-analyst") / "financial-analyst"
    nested.mkdir()
    for name in EXPECTED["financial-analyst"]:
        (nested / name).write_bytes((run / name).read_bytes())

    broken = agent_inputs.isolation_violations(run)
    assert any("sits inside" in line for line in broken)


def test_a_session_root_beside_the_bundle_is_a_broken_boundary(tmp_path):
    """The layout the holder directory exists to forbid.

    Right files in the root, and the whole bundle one `..` away: the market
    table, the other reader's report, every filing. This is why the six do not
    sit directly under the run directory.
    """
    run = _run_directory(tmp_path)
    beside = run / "numbers-reader"
    beside.mkdir()
    for name in EXPECTED["numbers-reader"]:
        (beside / name).write_bytes((run / name).read_bytes())

    broken = agent_inputs.isolation_violations(run)
    assert any("not at its session root" in line for line in broken)
    assert any("yields no file" in line for line in broken)
    assert (beside.parent / PRICE_FILE).is_file()  # one step out, plainly


def test_a_file_the_layer_never_sees_is_a_broken_boundary(tmp_path):
    run = _run_directory(tmp_path)
    agent_inputs.build_all(run)
    root = agent_inputs.session_root(run, "accounting-analyst")
    (root / PRICE_FILE).write_bytes((run / PRICE_FILE).read_bytes())

    broken = agent_inputs.isolation_violations(run)
    assert any(PRICE_FILE in line and "never sees" in line for line in broken)


# --- what the build refuses ---------------------------------------------------

@pytest.mark.parametrize("key", ("probability",) + PREDICTION_PROBABILITY_KEYS)
def test_a_prior_prediction_that_still_carries_a_probability_is_refused(
        key, tmp_path):
    """A prior run's own score in a reader's input makes the next one unfalsifiable.

    Every key §7 gives a probability to, one by one. A gate that caught
    `confidence` and `p_up` and let `p_within_horizon` through would say the
    file was clean, and "the probabilities were removed" would be a sentence
    nobody had checked.
    """
    run = _run_directory(tmp_path)
    (run / "input_prior_predictions.md").write_text(
        '[0000320193-25-000073:prior:prediction_accounting:1]\n'
        f'{{"flag": "receivables_outrun_revenue", "{key}": 0.71}}\n',
        encoding="utf-8")
    with pytest.raises(AgentInputError) as caught:
        agent_inputs.build(run, "numbers-reader")
    assert key in str(caught.value)
    assert not agent_inputs.session_root(run, "numbers-reader").exists()


def test_a_named_baseline_is_not_read_as_a_probability(tmp_path):
    """`Piotroski F-score` and `Altman Z-score` are trend-table vocabulary."""
    run = _run_directory(tmp_path)
    (run / "input_prior_predictions.md").write_text(
        '[0000320193-25-000073:prior:prediction_accounting:1]\n'
        "the Piotroski F-score fell and the Altman Z-score held\n",
        encoding="utf-8")
    agent_inputs.build(run, "numbers-reader")
    root = agent_inputs.session_root(run, "numbers-reader")
    assert (root / "input_prior_predictions.md").read_bytes() == (
        run / "input_prior_predictions.md").read_bytes()


@pytest.mark.parametrize("agent", ANALYSTS)
def test_a_directory_assembled_before_its_inputs_exist_is_refused(agent, tmp_path):
    """An analyst built before the readers ran holds the right shape, wrong run."""
    run = _run_directory(tmp_path, skip=("report_numbers.md", "report_notes_text.md",
                                         "report_numbers_vs_market.md",
                                         "report_notes_vs_market.md"))
    with pytest.raises(AgentInputError) as caught:
        agent_inputs.build(run, agent)
    assert "report_" in str(caught.value)


def test_a_file_no_builder_writes_yet_is_recorded_and_not_refused(tmp_path):
    """§6 names three files nothing in this repository writes. Early, not broken."""
    run = _run_directory(tmp_path, skip=agent_inputs.NOT_BUILT_YET)
    record = agent_inputs.build(run, "notes-text-reader")
    assert sorted(record["absent"]) == ["input_exhibits.md", "input_risk_factors.md"]
    root = agent_inputs.session_root(run, "notes-text-reader")
    assert _names(root) == [name for name in EXPECTED["notes-text-reader"]
                            if name not in agent_inputs.NOT_BUILT_YET]


def test_rebuilding_places_the_same_bytes_and_refuses_different_ones(tmp_path):
    """A run directory is append-only: existing content is never changed."""
    run = _run_directory(tmp_path)
    agent_inputs.build(run, "numbers-reader")
    agent_inputs.build(run, "numbers-reader")  # identical bytes, nothing to do

    root = agent_inputs.session_root(run, "numbers-reader")
    (run / "input_trends.json").write_text("a different trend table\n",
                                           encoding="utf-8")
    with pytest.raises(AgentInputError) as caught:
        agent_inputs.build(run, "numbers-reader")
    assert "append-only" in str(caught.value)
    assert (root / "input_trends.json").read_text(encoding="utf-8") == (
        "this is input_trends.json\n")


def test_a_link_standing_where_a_copy_belongs_is_refused(tmp_path):
    """Right bytes, wrong ancestors: the link's `..` is the bundle.

    Reading through the link finds the bytes the builder was going to write, so
    a check that asked only "is it already there, and does it match?" leaves the
    link in place and records it as copied.
    """
    run = _run_directory(tmp_path)
    root = agent_inputs.session_root(run, "numbers-reader")
    root.mkdir(parents=True)
    (root / "input_trends.json").symlink_to(Path("..") / ".." / "input_trends.json")

    with pytest.raises(AgentInputError) as caught:
        agent_inputs.build(run, "numbers-reader")
    assert "symlink" in str(caught.value)
    assert (root / "input_trends.json").is_symlink()  # left as found, not rewritten


def test_a_completed_run_holds_each_agent_s_own_report_and_is_clean(tmp_path):
    """The agent wrote the one file its prompt names, into the only root it has.

    A boundary check that read that as a stray would report all six broken on
    every finished run, which is a check nobody can use.
    """
    run = _run_directory(tmp_path)
    agent_inputs.build_all(run)
    for agent, name in WRITES.items():
        (agent_inputs.session_root(run, agent) / name).write_text(
            f"{agent} wrote this\n", encoding="utf-8")

    assert agent_inputs.isolation_violations(run) == []
    # And the build stays idempotent over a directory the agent has run in.
    agent_inputs.build_all(run)
    for agent, name in WRITES.items():
        assert (agent_inputs.session_root(run, agent) / name).read_text(
            encoding="utf-8") == f"{agent} wrote this\n"


def test_another_agent_s_report_is_a_leak_even_where_its_own_is_not(tmp_path):
    """`writes` is one file, not a licence for the layer's whole vocabulary."""
    run = _run_directory(tmp_path)
    agent_inputs.build_all(run)
    root = agent_inputs.session_root(run, "accounting-analyst")
    (root / "analysis_financial.json").write_text("{}\n", encoding="utf-8")

    broken = agent_inputs.isolation_violations(run)
    assert any("analysis_financial.json" in line and "never sees" in line
               for line in broken)


def test_a_routed_name_over_other_bytes_is_a_broken_boundary(tmp_path):
    """The market table hardlinked in under a report's name passes on names alone.

    `resolve()` does not see a hardlink and the name is one the layer may hold,
    so nothing but the bytes tells this from the file the run committed.
    """
    run = _run_directory(tmp_path)
    agent_inputs.build_all(run)
    root = agent_inputs.session_root(run, "accounting-analyst")
    smuggled = root / "report_numbers.md"
    smuggled.unlink()
    smuggled.hardlink_to(run / PRICE_FILE)

    assert agent_inputs.escapes(root) == []  # a hardlink resolves inside the root
    broken = agent_inputs.isolation_violations(run)
    assert any("report_numbers.md" in line and "other bytes" in line
               for line in broken)


def test_a_run_directory_that_is_not_there_is_refused(tmp_path):
    with pytest.raises(AgentInputError):
        agent_inputs.build(tmp_path / "no-such-run", "numbers-reader")


def test_a_name_that_is_not_an_agent_is_refused(tmp_path):
    run = _run_directory(tmp_path)
    with pytest.raises(AgentInputError):
        agent_inputs.build(run, "supervisor")


def test_naming_a_session_root_does_not_create_one(tmp_path):
    """`runs/` is append-only, and naming a path under it must not make one."""
    run = tmp_path / "runs" / "AAPL" / "0000320193-25-000073"
    where = agent_inputs.session_root(run, "numbers-reader")
    assert where == run / "agents" / "numbers-reader"
    assert not (tmp_path / "runs").exists()


def test_the_light_run_wakes_the_two_readers_and_nothing_else(tmp_path):
    """An 8-K 2.02 wakes both readers. Its comparer is Python now and its
    supervisor is archived, and which analyst it wakes is not decided."""
    run = _run_directory(tmp_path)
    built = agent_inputs.build_all(run, agent_inputs.LIGHT_RUN, light=True)
    assert [record["agent"] for record in built] == list(READERS)
    assert sorted(path.name for path in agent_inputs.agents_root(run).iterdir()) \
        == sorted(READERS)


# --- the command --------------------------------------------------------------

def test_the_command_builds_the_six_and_reports_them(tmp_path, capsys):
    run = _run_directory(tmp_path)
    assert agent_inputs.main(["--run", str(run)]) == 0
    printed = capsys.readouterr().out
    for agent in agent_inputs.AGENTS:
        assert agent in printed
    assert agent_inputs.isolation_violations(run) == []


def test_the_command_builds_a_light_run_of_the_two_readers(tmp_path, capsys):
    run = _run_directory(tmp_path)
    assert agent_inputs.main(["--run", str(run), "--light"]) == 0
    printed = capsys.readouterr().out
    assert all(agent in printed for agent in READERS)
    assert "accounting-analyst" not in printed


def test_the_command_reports_a_broken_boundary_it_did_not_build(tmp_path, capsys):
    """The build can be clean and the tree still wrong; the exit code says so."""
    run = _run_directory(tmp_path)
    agent_inputs.build_all(run)
    (agent_inputs.agents_root(run) / "scratch").mkdir()

    assert agent_inputs.main(["--run", str(run)]) == agent_inputs.BAD_INPUT
    assert "the boundary is broken" in capsys.readouterr().err


def test_the_command_will_not_take_one_agent_and_a_light_run_at_once(tmp_path, capsys):
    """Two different sets of agents. Guessing which was meant builds the wrong one."""
    run = _run_directory(tmp_path)
    assert agent_inputs.main(
        ["--run", str(run), "--agent", "numbers-reader", "--light"]
    ) == agent_inputs.BAD_INPUT
    assert "pick one" in capsys.readouterr().err
    assert not agent_inputs.agents_root(run).exists()


def test_the_command_refuses_a_run_directory_that_is_not_there(tmp_path, capsys):
    assert agent_inputs.main(
        ["--run", str(tmp_path / "no-such-run")]) == agent_inputs.BAD_INPUT
    assert "not a run directory" in capsys.readouterr().err


# --- the retired four, on a run on record ---------------------------------------

def test_a_leak_into_a_retired_agent_s_directory_is_a_broken_boundary(tmp_path):
    """A pilot run on record holds a supervisor's or a comparer's directory. The
    agent is retired -- nothing builds or runs one -- but its directory is the
    record of what it saw, and it is held to its layer as `RETIRED_AGENTS` keeps
    it: a supervisor never sees the market table, a comparer never sees a filing."""
    run = _run_directory(tmp_path)
    agent_inputs.build_all(run)
    supervisor = agent_inputs.agents_root(run) / "supervisor-pressure"
    supervisor.mkdir()
    (supervisor / PRICE_FILE).write_bytes((run / PRICE_FILE).read_bytes())
    comparer = agent_inputs.agents_root(run) / "numbers-vs-market"
    comparer.mkdir()
    (comparer / "input_notes.md").write_bytes((run / "input_notes.md").read_bytes())

    broken = agent_inputs.isolation_violations(run)
    assert any(line.startswith("supervisor-pressure:") and PRICE_FILE in line
               and "never sees" in line for line in broken)
    assert any(line.startswith("numbers-vs-market:") and "input_notes.md" in line
               and "never sees" in line for line in broken)


def test_a_clean_retired_agent_s_directory_is_not_a_violation(tmp_path):
    """The same two directories holding what their layers saw, and the file each
    wrote, are the record and are clean. Sitting anywhere but under `agents/`,
    or holding a file nobody routed, they are not."""
    run = _run_directory(tmp_path)
    agent_inputs.build_all(run)
    supervisor = agent_inputs.agents_root(run) / "supervisor-pressure"
    supervisor.mkdir()
    for name in agent_inputs.RETIRED_AGENTS["supervisor-pressure"].sees:
        if (run / name).is_file():
            (supervisor / name).write_bytes((run / name).read_bytes())
    (supervisor / "prediction_pressure.json").write_text("{}\n", encoding="utf-8")
    comparer = agent_inputs.agents_root(run) / "numbers-vs-market"
    comparer.mkdir()
    for name in agent_inputs.RETIRED_AGENTS["numbers-vs-market"].sees:
        if (run / name).is_file():
            (comparer / name).write_bytes((run / name).read_bytes())
    (comparer / "report_numbers_vs_market.md").write_text("x\n", encoding="utf-8")
    assert agent_inputs.isolation_violations(run) == []

    beside = run / "notes-vs-market"
    beside.mkdir()
    broken = agent_inputs.isolation_violations(run)
    assert any(line.startswith("notes-vs-market:") and "not at its session root" in line
               for line in broken)


# --- the valuation analyst's trimmed prose (the owner's decision of 2026-10-06) -------------
#
# The expected files are written out by hand. Four paragraphs; the notes reader
# flags the second and the fourth, and a third item flagging the third is on the
# manifest's drop list, so it flags nothing. Two kept blocks that were not adjacent
# are written one after the other with nothing between them: the owner reads
# everything after an `[id]` line up to the next one as that paragraph's body
# (evals/regression/mechanical.py, `paragraphs_of`), so a line between them would
# be read as the tail of the second paragraph. The file carries no note of its
# own, that is the manifest's.

ONE, TWO, THREE, FOUR = (f"0000000000-00-000001:mdna:{n}" for n in (1, 2, 3, 4))
MDNA = (f"# T mdna\n\n[{ONE}]\nFirst, not flagged.\n\n"
        f"[{TWO}]\nSecond,\u00a0flagged.\n\n"
        f"[{THREE}]\nThird, flagged by an item the gate dropped.\n\n"
        f"[{FOUR}]\nFourth, flagged.\n")
NOTES_REPORT = ("# notes\n```json\n"
                f'[{{"id": "a", "paragraph_id": "{TWO}", "quote": "Second"}},\n'
                f' {{"id": "c", "paragraph_id": "{THREE}", "quote": "Third"}}]\n'
                "```\n```json\n"
                f'{{"id": "b", "paragraph_id": "{FOUR}", "quote": "Fourth"}}\n'
                "```\n")
MANIFEST = ('{"accession": "0000320193-25-000073", "ticker": "AAPL", "dropped_items": '
            '[{"item_id": "c", "report": "report_notes_text.md", "reason": "planted"}]}\n')
TRIMMED = (f"# T mdna\n\n"
           f"[{TWO}]\nSecond,\u00a0flagged.\n\n"
           f"[{FOUR}]\nFourth, flagged.\n")
RECORD = {"kept": [TWO, FOUR], "of": 4,
          "note": "2 of 4 paragraphs, the ones the notes reader flagged; the rest were not placed"}
EMPTY_8K = {"kept": [], "of": 0,
            "note": "0 of 0 paragraphs, the ones the notes reader flagged; the rest were not placed"}


def _trimmed_run(tmp_path: Path) -> Path:
    run = _run_directory(tmp_path)
    (run / "input_mdna.md").write_text(MDNA, encoding="utf-8")
    (run / "report_notes_text.md").write_text(NOTES_REPORT, encoding="utf-8")
    (run / "input_manifest.json").write_text(MANIFEST, encoding="utf-8")
    return run


def test_the_valuation_analyst_is_handed_the_hand_written_trim_and_the_manifest_records_it(tmp_path):
    run = _trimmed_run(tmp_path)
    built = agent_inputs.build(run, "valuation-analyst")
    placed = agent_inputs.session_root(run, "valuation-analyst") / "input_mdna.md"
    assert placed.read_bytes() == TRIMMED.encode("utf-8")
    assert built["trimmed"]["input_mdna.md"] == RECORD
    manifest = json.loads((run / "input_manifest.json").read_text(encoding="utf-8"))
    assert manifest["agents"]["valuation-analyst"]["trimmed"]["input_mdna.md"] == RECORD
    assert manifest["dropped_items"][0]["item_id"] == "c"      # every other key left alone
    # The notes reader's own copy is the whole file, byte for byte.
    agent_inputs.build(run, "notes-text-reader")
    assert (agent_inputs.session_root(run, "notes-text-reader") / "input_mdna.md").read_bytes() \
        == MDNA.encode("utf-8")


def test_the_trimmed_file_holds_no_word_the_filing_does_not():
    assert set(TRIMMED.split()) <= set(MDNA.split())
    assert "trimmed" not in TRIMMED and "placed" not in TRIMMED


def test_kept_blocks_meet_with_nothing_between_them_adjacent_or_not():
    assert agent_inputs.trimmed(MDNA, {THREE, FOUR}) == (
        f"# T mdna\n\n[{THREE}]\nThird, flagged by an item the gate dropped.\n\n"
        f"[{FOUR}]\nFourth, flagged.\n")
    assert agent_inputs.trimmed(MDNA, {ONE, FOUR}) == (
        f"# T mdna\n\n[{ONE}]\nFirst, not flagged.\n\n"
        f"[{FOUR}]\nFourth, flagged.\n")
    # none of the file's paragraphs kept: nothing is placed, never the head alone
    assert agent_inputs.trimmed(MDNA, set()) is None
    # a file with no [id] paragraph at all is handed whole
    assert agent_inputs.trimmed("this is input_8k.md\n", set()) == "this is input_8k.md\n"


def test_a_dropped_item_flags_nothing_and_a_run_with_no_gate_record_is_refused(tmp_path):
    run = _trimmed_run(tmp_path)
    assert agent_inputs.flagged_paragraphs(run) == {TWO, FOUR}          # not THREE: c fell
    (run / "input_manifest.json").write_text(
        '{"accession": "0000320193-25-000073", "dropped_items": []}\n', encoding="utf-8")
    assert agent_inputs.flagged_paragraphs(run) == {TWO, THREE, FOUR}   # nothing fell
    (run / "input_manifest.json").write_text('{"accession": "0000320193-25-000073"}\n',
                                             encoding="utf-8")
    with pytest.raises(AgentInputError, match="no record that the quote gate ran"):
        agent_inputs.flagged_paragraphs(run)
    # no gated report at the run root: refused, never read as "none flagged"
    with pytest.raises(AgentInputError, match="holds no report_notes_text.md"):
        agent_inputs.flagged_paragraphs(tmp_path / "none")


def test_a_valuation_build_on_a_run_with_no_gated_notes_report_is_refused(tmp_path):
    """The valuation layer's `sees` does not name the notes report, so `required`
    does not refuse the build; the flagged set does, before anything is created,
    and the manifest records no trim. With the report back, the build goes
    through and records the hand-written trim."""
    run = _trimmed_run(tmp_path)
    (run / "report_notes_text.md").unlink()
    with pytest.raises(AgentInputError, match="holds no report_notes_text.md"):
        agent_inputs.build(run, "valuation-analyst")
    assert not agent_inputs.session_root(run, "valuation-analyst").exists()
    assert "agents" not in json.loads((run / "input_manifest.json").read_text(encoding="utf-8"))
    (run / "report_notes_text.md").write_text(NOTES_REPORT, encoding="utf-8")
    built = agent_inputs.build(run, "valuation-analyst")
    assert built["trimmed"]["input_mdna.md"] == RECORD
    assert agent_inputs.isolation_violations(run) == []


# The owner's decision that the valuation analyst reads only the flagged
# paragraphs is dated 2026-10-06; the eight published runs were analysed on
# 2026-09-29 (their manifests' `analysed_utc`) and hold the full file by right.
ANALYSED_BEFORE_THE_RULE = "2026-09-29T00:51:54Z"
ANALYSED_ON_THE_RULE_DAY = "2026-10-06T00:00:00Z"


def _valuation_directory(tmp_path: Path, *, holds: str, record: dict | None,
                         analysed: str | None = ANALYSED_BEFORE_THE_RULE) -> Path:
    """A run on record whose valuation analyst's directory holds `holds` as its
    MD&A, with the manifest recording `record` as the trim, or no trim, and
    `analysed` as when the analyses ran (None: the manifest does not say)."""
    run = _trimmed_run(tmp_path)
    manifest = json.loads(MANIFEST)
    if analysed is not None:
        manifest[agent_inputs.ANALYSED_KEY] = analysed
    if record is not None:
        # as `build` records it: every file it trims, the 8-K's placeholder here
        # holding no paragraph at all
        manifest["agents"] = {"valuation-analyst": {"result": "written",
                                                    "trimmed": {"input_mdna.md": record,
                                                                "input_8k.md": EMPTY_8K}}}
    (run / "input_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    root = agent_inputs.session_root(run, "valuation-analyst")
    root.mkdir(parents=True)
    for name in agent_inputs.AGENTS["valuation-analyst"].sees:
        if name != "input_mdna.md":
            (root / name).write_bytes((run / name).read_bytes())
    (root / "input_mdna.md").write_text(holds, encoding="utf-8")
    return run


def test_a_directory_the_manifest_records_no_trim_for_is_held_to_the_full_file(tmp_path):
    """The eight runs published before the trim hold the full MD&A in their
    valuation directories, and the manifest's silence, with a run analysed
    before the rule's day, is the record of that."""
    assert agent_inputs.isolation_violations(
        _valuation_directory(tmp_path / "full", holds=MDNA, record=None)) == []
    broken = agent_inputs.isolation_violations(
        _valuation_directory(tmp_path / "cut", holds=TRIMMED, record=None))
    assert any("input_mdna.md" in line and "other bytes" in line for line in broken)


def test_no_trim_on_record_is_named_for_a_run_analysed_from_the_rule_s_day(tmp_path):
    """The same full-file directory with no trim on record: clean on a run
    analysed the day before the rule, named on one analysed the day the rule
    came in, and named on one the manifest does not date."""
    assert agent_inputs.isolation_violations(_valuation_directory(
        tmp_path / "before", holds=MDNA, record=None, analysed="2026-10-05T23:59:59Z")) == []
    broken = agent_inputs.isolation_violations(_valuation_directory(
        tmp_path / "on", holds=MDNA, record=None, analysed=ANALYSED_ON_THE_RULE_DAY))
    assert broken == ["valuation-analyst: no trim on record for a run analysed after the trim "
                      "rule (analysed_utc 2026-10-06T00:00:00Z, the rule is from 2026-10-06)"]
    broken = agent_inputs.isolation_violations(_valuation_directory(
        tmp_path / "undated", holds=MDNA, record=None, analysed=None))
    assert len(broken) == 1 and broken[0].startswith(
        "valuation-analyst: no trim on record and no analysed_utc in the manifest")
    # with a trim on record the date is not read: the record is what is checked
    assert agent_inputs.isolation_violations(_valuation_directory(
        tmp_path / "recorded", holds=TRIMMED, record=RECORD, analysed=ANALYSED_ON_THE_RULE_DAY)) == []


def test_a_directory_the_manifest_records_a_trim_for_is_held_to_that_record(tmp_path):
    assert agent_inputs.isolation_violations(
        _valuation_directory(tmp_path / "cut", holds=TRIMMED, record=RECORD)) == []
    broken = agent_inputs.isolation_violations(
        _valuation_directory(tmp_path / "full", holds=MDNA, record=RECORD))
    assert any("input_mdna.md" in line and "other bytes" in line for line in broken)
    # A record that does not fit the run's file is not a record of it.
    broken = agent_inputs.isolation_violations(_valuation_directory(
        tmp_path / "odd", holds=TRIMMED, record={"kept": [TWO, "0000000000-00-000001:mdna:9"], "of": 4}))
    assert any("no block for" in line for line in broken)
    broken = agent_inputs.isolation_violations(_valuation_directory(
        tmp_path / "count", holds=TRIMMED, record={"kept": [TWO, FOUR], "of": 5}))
    assert any("says 5 paragraphs" in line for line in broken)


def test_the_boundary_check_re_derives_the_trim_from_the_record_and_not_from_the_trim(
        tmp_path, monkeypatch):
    """`handed` is the independent reading: the run's file cut by a list of ids.
    Neither it nor the boundary check calls `trimmed`, so a wrong trim and the
    check do not move together."""
    monkeypatch.setattr(agent_inputs, "trimmed", lambda *args: (_ for _ in ()).throw(
        AssertionError("the boundary check called the trim")))
    assert agent_inputs.handed(MDNA, RECORD) == TRIMMED
    assert agent_inputs.handed(MDNA, {"kept": [], "of": 4}) is None      # absent
    assert agent_inputs.isolation_violations(
        _valuation_directory(tmp_path / "cut", holds=TRIMMED, record=RECORD)) == []


# The flagged set, derived again by the boundary check from the gated report and
# the drop list: {TWO, FOUR}. A record is held to that set, whatever it says.
KEEPS_THREE = {"kept": [TWO, THREE, FOUR], "of": 4}
CUT_TO_THREE = (f"# T mdna\n\n"
                f"[{TWO}]\nSecond,\u00a0flagged.\n\n"
                f"[{THREE}]\nThird, flagged by an item the gate dropped.\n\n"
                f"[{FOUR}]\nFourth, flagged.\n")
KEEPS_EVERY = {"kept": [ONE, TWO, THREE, FOUR], "of": 4}
KEEPS_TWO_ONLY = {"kept": [TWO], "of": 4}
CUT_TO_TWO = f"# T mdna\n\n[{TWO}]\nSecond,\u00a0flagged.\n\n"


def test_a_record_keeping_a_paragraph_no_standing_item_flagged_is_a_broken_boundary(tmp_path):
    """The third paragraph was flagged only by item c, which the gate dropped. A
    record keeping it, over a copy cut to match the record, is reported naming
    the third paragraph and the bytes; a record keeping every paragraph over the
    full file names the first and the third."""
    broken = agent_inputs.isolation_violations(
        _valuation_directory(tmp_path / "three", holds=CUT_TO_THREE, record=KEEPS_THREE))
    assert broken == [
        f"valuation-analyst: input_mdna.md: the manifest's trimmed record keeps {THREE}, "
        "which no standing item of report_notes_text.md flagged",
        "valuation-analyst: holds a input_mdna.md that is not the run's — the right name "
        "over other bytes"]
    broken = agent_inputs.isolation_violations(
        _valuation_directory(tmp_path / "every", holds=MDNA, record=KEEPS_EVERY))
    assert broken[0] == (f"valuation-analyst: input_mdna.md: the manifest's trimmed record "
                         f"keeps {ONE}, {THREE}, which no standing item of "
                         "report_notes_text.md flagged")
    assert len(broken) == 2 and "other bytes" in broken[1]
    # the other side: a record leaving out a paragraph a standing item flagged
    broken = agent_inputs.isolation_violations(
        _valuation_directory(tmp_path / "fewer", holds=CUT_TO_TWO, record=KEEPS_TWO_ONLY))
    assert broken[0] == (f"valuation-analyst: input_mdna.md: the manifest's trimmed record "
                         f"leaves out {FOUR}, which a standing item of report_notes_text.md "
                         "flagged")
    assert len(broken) == 2 and "other bytes" in broken[1]
    # and the clean run: the record is the set and the file is the cut by it
    assert agent_inputs.isolation_violations(
        _valuation_directory(tmp_path / "clean", holds=TRIMMED, record=RECORD)) == []


def test_a_trimmed_file_the_record_leaves_out_is_named(tmp_path):
    """A record naming the MD&A and not the 8-K, the 8-K placed whole: named,
    whatever the 8-K holds, because the router records every file it trims and
    a file the record leaves out would be handed whole. Both named: clean."""
    run = _valuation_directory(tmp_path / "half", holds=TRIMMED, record=RECORD)
    manifest = json.loads((run / "input_manifest.json").read_text(encoding="utf-8"))
    del manifest["agents"]["valuation-analyst"]["trimmed"]["input_8k.md"]
    (run / "input_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    broken = agent_inputs.isolation_violations(run)
    assert broken == ["valuation-analyst: input_8k.md: placed with no trim of its own on "
                      "record, though the manifest records a trim for input_mdna.md; the "
                      "router records every file it trims"]
    assert agent_inputs.isolation_violations(
        _valuation_directory(tmp_path / "both", holds=TRIMMED, record=RECORD)) == []


def test_a_trim_built_from_a_wrong_set_is_reported_even_under_a_matching_record(tmp_path):
    """The record and the file agree with each other and both keep the third
    paragraph: the check does not take the record's word for the set."""
    run = _valuation_directory(tmp_path / "wrong", holds=CUT_TO_THREE, record=KEEPS_THREE)
    assert agent_inputs.handed(MDNA, KEEPS_THREE) == CUT_TO_THREE      # they agree
    broken = agent_inputs.isolation_violations(run)
    assert any(THREE in line and "no standing item" in line for line in broken)
    assert any("other bytes" in line for line in broken)
    # when the drop list is emptied, c stands, THREE is flagged, and the same
    # directory is clean: the set is read off the run's own record of the gate
    manifest = json.loads((run / "input_manifest.json").read_text(encoding="utf-8"))
    manifest["dropped_items"] = []
    (run / "input_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    assert agent_inputs.isolation_violations(run) == []


def test_a_trim_on_a_run_with_no_gate_record_is_a_broken_boundary(tmp_path):
    run = _valuation_directory(tmp_path / "nogate", holds=TRIMMED, record=RECORD)
    manifest = json.loads((run / "input_manifest.json").read_text(encoding="utf-8"))
    del manifest["dropped_items"]
    (run / "input_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    broken = agent_inputs.isolation_violations(run)
    assert len(broken) == 1 and broken[0].startswith(
        "valuation-analyst: the manifest records a trim, but ")
    assert "no record that the quote gate ran" in broken[0]


# --- the trim held to the owner's own reading of a copy --------------------------------------
#
# The owner's grader (`evals/regression/mechanical.py`, read and imported here,
# never written) reads a trimmed copy as some of the original's `[id]`
# paragraphs, each verbatim, and nothing else: everything after an `[id]` line up
# to the next one is that paragraph's body (`paragraphs_of`), compared exactly
# (`trimmed_copy_problems`). The first four Opus runs (ESE, QCOM, TTMI and NVDA,
# 2026-10-07) failed it in every trimmed copy, both passes, because the trim
# wrote a line naming two ids between two kept blocks that were not adjacent:
# ESE's input_8k.md read
#   [0001104659-26-092033:8k_2_02:15]
#   |  | · | Q3 2026 entered orders were $410 million, ... |
#
#   [0001104659-26-092033:8k_2_02:15] [0001104659-26-092033:8k_2_02:22]
#
#   [0001104659-26-092033:8k_2_02:22]
# and the owner read the middle line as the tail of paragraph 15. Every test
# below runs over both passes, which are handed the same two files.

from evals.regression import mechanical  # noqa: E402  (the owner's, read-only)

PASSES = ("valuation-analyst", "valuation-analyst-second-pass")
HEAD = "# T mdna\n\n"
BLOCK_TWO = f"[{TWO}]\nSecond, flagged.\n\n"
BLOCK_FOUR = f"[{FOUR}]\nFourth, flagged.\n"
# Every shape a copy can take that the owner refuses, as the trim or a softer
# variant of it could write it. The seam is ESE's shape on these four paragraphs.
REFUSED_SHAPES = {
    "the seam line": HEAD + BLOCK_TWO + f"[{TWO}] [{FOUR}]\n\n" + BLOCK_FOUR,
    "a blank line between blocks": HEAD + BLOCK_TWO + "\n" + BLOCK_FOUR,
    "a note before the first paragraph": HEAD + "2 of 4 paragraphs\n\n" + BLOCK_TWO + BLOCK_FOUR,
    "text after the last block": HEAD + BLOCK_TWO + BLOCK_FOUR + "\n[the rest were not placed]\n",
    "the last block rstripped": (HEAD + BLOCK_TWO + BLOCK_FOUR).rstrip(),
    "the preamble alone": HEAD,
}


def _both_passes(run: Path) -> None:
    for name in PASSES:
        agent_inputs.build(run, name)


def _replace(run: Path, agent: str, name: str, data: bytes) -> None:
    placed = agent_inputs.session_root(run, agent) / name
    if placed.exists():
        placed.unlink()
    placed.write_bytes(data)


def test_the_trimmed_copy_is_what_the_owner_reads_as_a_cut_of_the_run_file(tmp_path):
    """The trimmer's real output, both passes: the owner's rule finds nothing, every
    paragraph the copy holds is the run file's own (id, body) pair, the text
    before the first paragraph is the run file's byte for byte, and the boundary
    check is clean. On the seam trim the owner said "paragraph ...:mdna:2 is not
    the file on record's, word for word"."""
    run = _trimmed_run(tmp_path)
    _both_passes(run)
    original = (run / "input_mdna.md").read_bytes().decode("utf-8")
    for name in PASSES:
        copy = (agent_inputs.session_root(run, name) / "input_mdna.md").read_bytes().decode("utf-8")
        assert copy == TRIMMED
        assert mechanical.trimmed_copy_problems(copy, original) == []
        assert set(mechanical.paragraphs_of(copy).items()) <= set(
            mechanical.paragraphs_of(original).items())
        assert set(mechanical.paragraphs_of(copy)) == {TWO, FOUR}      # the last one too
        assert copy[:copy.index("[")] == original[:original.index("[")]
        assert agent_inputs.copy_shape_problems(copy, original) == []
    assert agent_inputs.isolation_violations(run) == []


@pytest.mark.parametrize("shape", sorted(REFUSED_SHAPES))
@pytest.mark.parametrize("agent", PASSES)
def test_a_copy_the_owner_refuses_the_boundary_check_names(tmp_path, shape, agent):
    """One direction, not an equivalence: whatever shape the owner refuses, the
    boundary check names too, under the trim record the router wrote. On the
    seam line and the preamble alone the boundary check named nothing before."""
    run = _trimmed_run(tmp_path)
    _both_passes(run)
    copy = REFUSED_SHAPES[shape]
    assert mechanical.trimmed_copy_problems(copy, MDNA) != []
    assert agent_inputs.copy_shape_problems(copy, MDNA) != []
    _replace(run, agent, "input_mdna.md", copy.encode("utf-8"))
    broken = agent_inputs.isolation_violations(run)
    assert broken and all(line.startswith(f"{agent}: input_mdna.md") or
                          line.startswith(f"{agent}: holds a input_mdna.md") for line in broken)
    other = PASSES[1 - PASSES.index(agent)]
    assert not any(line.startswith(f"{other}: ") for line in broken)


def test_the_seam_line_is_named_by_the_paragraph_it_lands_in(tmp_path):
    """The seam is read as the tail of the paragraph before it, by both rules."""
    run = _trimmed_run(tmp_path)
    _both_passes(run)
    seam = REFUSED_SHAPES["the seam line"]
    assert mechanical.trimmed_copy_problems(seam, MDNA) == [
        f"paragraph {TWO} is not the file on record's, word for word"]
    _replace(run, "valuation-analyst-second-pass", "input_mdna.md", seam.encode("utf-8"))
    assert (f"valuation-analyst-second-pass: input_mdna.md: paragraph {TWO} is not the run "
            "file's, word for word") in agent_inputs.isolation_violations(run)


def test_the_full_file_under_a_trim_record_is_refused_by_the_gate_and_not_by_the_owner(tmp_path):
    """Why the agreement above runs one way: the full file is some of the
    original's paragraphs, each verbatim, so the owner passes it, and the trim
    rule refuses it, because a paragraph no one flagged was handed."""
    run = _trimmed_run(tmp_path)
    _both_passes(run)
    assert mechanical.trimmed_copy_problems(MDNA, MDNA) == []
    _replace(run, "valuation-analyst", "input_mdna.md", MDNA.encode("utf-8"))
    assert any("other bytes" in line for line in agent_inputs.isolation_violations(run))


NO_ITEMS_MANIFEST = '{"accession": "0000320193-25-000073", "ticker": "AAPL", "dropped_items": []}\n'


def test_a_file_none_of_whose_paragraphs_was_flagged_is_not_placed(tmp_path):
    """A notes report holding no item flags nothing: both passes record 0 of 4
    for the MD&A and hold no copy of it, and the boundary check is clean. The
    head alone, placed by hand under that record, is what the owner refuses
    ("the copy carries no [id] paragraphs") and the boundary check names. The
    8-K here has no paragraph at all, so it is handed whole, as TTMI's was."""
    run = _trimmed_run(tmp_path)
    (run / "report_notes_text.md").write_text("no items\n", encoding="utf-8")
    (run / "input_manifest.json").write_text(NO_ITEMS_MANIFEST, encoding="utf-8")
    for name in PASSES:
        built = agent_inputs.build(run, name)
        assert built["trimmed"]["input_mdna.md"] == {
            "kept": [], "of": 4,
            "note": "0 of 4 paragraphs: the notes reader flagged none of them, so the file "
                    "was not placed"}
        assert "input_mdna.md" not in built["files"]
        assert not (agent_inputs.session_root(run, name) / "input_mdna.md").exists()
        assert (agent_inputs.session_root(run, name) / "input_8k.md").read_bytes() == \
            (run / "input_8k.md").read_bytes()
    assert agent_inputs.handed(MDNA, {"kept": [], "of": 4}) is None
    assert agent_inputs.isolation_violations(run) == []
    assert mechanical.trimmed_copy_problems(HEAD, MDNA) == [
        "the copy carries no [id] paragraphs, and is not the file on record"]
    for name in PASSES:
        _replace(run, name, "input_mdna.md", HEAD.encode("utf-8"))
    broken = agent_inputs.isolation_violations(run)
    for name in PASSES:
        assert (f"{name}: input_mdna.md: placed under a record that keeps none of its 4 "
                "paragraphs; a file none of whose paragraphs was flagged is not placed") in broken


CRLF_MDNA = MDNA.replace("\n", "\r\n")


def test_a_run_file_with_carriage_returns_is_cut_from_its_bytes(tmp_path):
    """The trim used to read the run's file in text mode, which turns `\\r\\n` into
    `\\n`: the copy then held no CR and the owner, decoding both from bytes, read
    the head and every paragraph as changed while the boundary check, reading
    the same way as the trim, passed it. Now the copy keeps the run file's CRs.
    The LF copy is refused by both."""
    run = _trimmed_run(tmp_path)
    (run / "input_mdna.md").write_bytes(CRLF_MDNA.encode("utf-8"))
    _both_passes(run)
    original = (run / "input_mdna.md").read_bytes()
    for name in PASSES:
        copy = (agent_inputs.session_root(run, name) / "input_mdna.md").read_bytes()
        assert b"\r\n" in copy
        assert copy == TRIMMED.replace("\n", "\r\n").encode("utf-8")
        assert mechanical.trimmed_copy_problems(copy.decode(), original.decode()) == []
    assert agent_inputs.isolation_violations(run) == []
    lf = TRIMMED.encode("utf-8")
    assert mechanical.trimmed_copy_problems(lf.decode(), original.decode()) != []
    _replace(run, "valuation-analyst", "input_mdna.md", lf)
    broken = agent_inputs.isolation_violations(run)
    assert any(line.startswith("valuation-analyst: input_mdna.md: the text before the first "
                               "paragraph") for line in broken)


def test_a_prose_file_that_is_not_utf8_is_refused_and_not_replaced(tmp_path):
    run = _trimmed_run(tmp_path)
    (run / "input_mdna.md").write_bytes(MDNA.encode("utf-8").replace(b"Second", b"Sec\xffond"))
    with pytest.raises(AgentInputError, match="is not UTF-8"):
        agent_inputs.build(run, "valuation-analyst")
