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

import re
from pathlib import Path

import pytest

from src import agent_inputs
from src.agent_inputs import AgentInputError

REPO_ROOT = Path(__file__).resolve().parent.parent
INPUT_SPEC = REPO_ROOT / "docs" / "INPUT_SPEC.md"
CHECKLIST = REPO_ROOT / "docs" / "CHECKLIST.md"
PROMPTS = REPO_ROOT / ".claude" / "agents"

# docs/INPUT_SPEC.md, the three rows of the layer table, verbatim.
LAYER_TABLE = (
    "| readers | the filing bundle for one company "
    "| prices, short interest, any other company |",
    "| comparers | both reader reports plus the market table | any filing |",
    "| supervisor | the four reports | any filing, the market table |",
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
    "numbers-vs-market": (
        "input_market.json",
        "report_notes_text.md",
        "report_numbers.md",
    ),
    "notes-vs-market": (
        "input_market.json",
        "report_notes_text.md",
        "report_numbers.md",
    ),
    "supervisor-accounting": (
        "report_notes_text.md",
        "report_notes_vs_market.md",
        "report_numbers.md",
        "report_numbers_vs_market.md",
    ),
    "supervisor-pressure": (
        "report_notes_text.md",
        "report_notes_vs_market.md",
        "report_numbers.md",
        "report_numbers_vs_market.md",
    ),
}

READERS = ("numbers-reader", "notes-text-reader")
COMPARERS = ("numbers-vs-market", "notes-vs-market")
SUPERVISORS = ("supervisor-accounting", "supervisor-pressure")

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
    "numbers-vs-market": "report_numbers_vs_market.md",
    "notes-vs-market": "report_notes_vs_market.md",
    "supervisor-accounting": "prediction_accounting.json",
    "supervisor-pressure": "prediction_pressure.json",
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


def test_the_six_agents_are_the_six_prompts_committed():
    prompts = {path.stem for path in PROMPTS.glob("*.md")}
    # refute-check and reproduce-check are verification subagents, not layers.
    assert set(agent_inputs.AGENTS) == prompts - {"refute-check", "reproduce-check"}


@pytest.mark.parametrize("agent", COMPARERS)
def test_a_comparer_prompt_says_it_holds_both_reader_reports(agent):
    """The table and the prompts are the same rule written twice.

    This repository has already shipped a layer table saying a comparer sees
    both reader reports beside comparer prompts saying each sees one, so a
    directory the table calls correct was one its own prompt called broken.
    """
    prompt = (PROMPTS / f"{agent}.md").read_text(encoding="utf-8")
    for report in ("report_numbers.md", "report_notes_text.md"):
        assert report in prompt


@pytest.mark.parametrize("agent", sorted(WRITES))
def test_each_prompt_names_the_one_file_its_agent_writes(agent):
    """Where an agent's output lands is decided by its prompt, not guessed here.

    Each prompt says "Write `x`. Nothing else, anywhere.", and each agent has
    `Write` and a session rooted at its own directory, so `x` lands there and
    nowhere else. That is why a directory holding it after the run is clean.
    """
    prompt = (PROMPTS / f"{agent}.md").read_text(encoding="utf-8")
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
    agent_inputs.build(run, agent)
    root = agent_inputs.session_root(run, agent)

    assert _names(root) == list(EXPECTED[agent])
    assert PRICE_FILE not in _names(root)
    assert [name for name in _names(root) if name.startswith("report_")] == []
    assert [name for name in _names(root) if name.startswith("prediction_")] == []


@pytest.mark.parametrize("agent", COMPARERS)
def test_a_comparer_directory_holds_both_reader_reports_and_no_filing(agent, tmp_path):
    run = _run_directory(tmp_path)
    agent_inputs.build(run, agent)
    root = agent_inputs.session_root(run, agent)

    assert _names(root) == list(EXPECTED[agent])
    assert (root / "report_numbers.md").is_file()
    assert (root / "report_notes_text.md").is_file()
    # A filing is everything the extract stage wrote out of the documents. The
    # market table is the one `input_` file that is not one of them.
    filings = [name for name in _names(root)
               if name.startswith("input_") and name != PRICE_FILE]
    assert filings == []


@pytest.mark.parametrize("agent", SUPERVISORS)
def test_a_supervisor_directory_holds_neither_a_filing_nor_the_market_table(
        agent, tmp_path):
    run = _run_directory(tmp_path)
    agent_inputs.build(run, agent)
    root = agent_inputs.session_root(run, agent)

    assert _names(root) == list(EXPECTED[agent])
    assert PRICE_FILE not in _names(root)
    assert [name for name in _names(root) if name.startswith("input_")] == []


def test_every_routed_file_arrives_verbatim(tmp_path):
    """The right name over the wrong bytes is the same leak with a better shape."""
    run = _run_directory(tmp_path)
    agent_inputs.build_all(run)
    for agent in agent_inputs.AGENTS:
        root = agent_inputs.session_root(run, agent)
        for name in _names(root):
            assert (root / name).read_bytes() == (run / name).read_bytes()


def test_no_file_reaches_an_agent_that_nobody_routed(tmp_path):
    run = _run_directory(tmp_path)
    agent_inputs.build_all(run)
    routed = {name for agent in agent_inputs.AGENTS
              for name in _names(agent_inputs.session_root(run, agent))}
    # input_manifest.json, the predictions, the baselines, the explanations and
    # the four controls are the run's record. No layer reads them.
    assert "input_manifest.json" not in routed
    assert routed == set().union(*(set(names) for names in EXPECTED.values()))


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
    nested = agent_inputs.session_root(run, "numbers-vs-market") / "supervisor-pressure"
    nested.mkdir()
    for name in EXPECTED["supervisor-pressure"]:
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
    root = agent_inputs.session_root(run, "supervisor-accounting")
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


@pytest.mark.parametrize("agent", COMPARERS + SUPERVISORS)
def test_a_directory_assembled_before_its_inputs_exist_is_refused(agent, tmp_path):
    """A comparer built before the readers ran holds the right shape, wrong run."""
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
    root = agent_inputs.session_root(run, "supervisor-accounting")
    (root / "prediction_pressure.json").write_text("{}\n", encoding="utf-8")

    broken = agent_inputs.isolation_violations(run)
    assert any("prediction_pressure.json" in line and "never sees" in line
               for line in broken)


def test_a_routed_name_over_other_bytes_is_a_broken_boundary(tmp_path):
    """The market table hardlinked in under a report's name passes on names alone.

    `resolve()` does not see a hardlink and the name is one the layer may hold,
    so nothing but the bytes tells this from the file the run committed.
    """
    run = _run_directory(tmp_path)
    agent_inputs.build_all(run)
    root = agent_inputs.session_root(run, "numbers-vs-market")
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


def test_the_light_run_wakes_four_agents_and_not_the_other_two(tmp_path):
    """An 8-K 2.02 produces three reports, so supervisor-accounting does not run."""
    run = _run_directory(tmp_path, skip=agent_inputs.LIGHT_RUN_ABSENT)
    built = agent_inputs.build_all(run, agent_inputs.LIGHT_RUN, light=True)
    assert [record["agent"] for record in built] == list(agent_inputs.LIGHT_RUN)
    assert not agent_inputs.session_root(run, "supervisor-accounting").exists()
    assert not agent_inputs.session_root(run, "notes-vs-market").exists()


@pytest.mark.parametrize("agent", SUPERVISORS)
def test_a_supervisor_over_three_reports_is_the_light_run_and_nothing_else(
        agent, tmp_path):
    """The same directory: allowed on an 8-K 2.02, refused on a full run.

    `report_notes_vs_market.md` is absent on a light run because that comparer
    never runs, and absent on a full run because it has not run *yet*. The two
    look identical on disk and only one of them is a finished run, so the
    allowance is the light run's and the full run is refused rather than built
    over three reports and reported complete.
    """
    run = _run_directory(tmp_path, skip=agent_inputs.LIGHT_RUN_ABSENT)

    with pytest.raises(AgentInputError) as caught:
        agent_inputs.build(run, agent)
    assert "report_notes_vs_market.md" in str(caught.value)

    record = agent_inputs.build(run, agent, light=True)
    assert record["absent"] == list(agent_inputs.LIGHT_RUN_ABSENT)
    assert _names(agent_inputs.session_root(run, agent)) == [
        name for name in EXPECTED[agent]
        if name not in agent_inputs.LIGHT_RUN_ABSENT]


# --- the command --------------------------------------------------------------

def test_the_command_builds_the_six_and_reports_them(tmp_path, capsys):
    run = _run_directory(tmp_path)
    assert agent_inputs.main(["--run", str(run)]) == 0
    printed = capsys.readouterr().out
    for agent in agent_inputs.AGENTS:
        assert agent in printed
    assert agent_inputs.isolation_violations(run) == []


def test_the_command_builds_a_light_run_over_three_reports(tmp_path, capsys):
    run = _run_directory(tmp_path, skip=agent_inputs.LIGHT_RUN_ABSENT)
    assert agent_inputs.main(["--run", str(run), "--light"]) == 0
    assert "1 absent" in capsys.readouterr().out
    assert not agent_inputs.session_root(run, "notes-vs-market").exists()


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
