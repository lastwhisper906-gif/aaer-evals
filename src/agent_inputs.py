"""One input directory per agent per run. The directory is the boundary.

`docs/INPUT_SPEC.md` states the rule as a table, and this file is that table
turned into directories:

| Layer | Sees | Never sees |
|---|---|---|
| readers | the filing bundle for one company | prices, short interest, any other company |
| comparers | both reader reports plus the market table | any filing |
| supervisor | the four reports | any filing, the market table |

A comparer holds **both** reader reports because the layer's directory is one
directory; it labels only the items of its own report, and that is a rule its
prompt carries, not something a directory can enforce. The spec's header says
the same and so do `.claude/agents/numbers-vs-market.md` and
`.claude/agents/notes-vs-market.md`; they agree today, and the moment they stop
agreeing the isolation test is judging one of two rules.

Two files are named in the spec so they are routed to somebody:
`input_notes_history.md` goes to the notes-text reader, and
`input_prior_predictions.md` goes to both readers **with the probability numbers
removed**. `src/assemble_bundle.py` drops the probability keys when it writes
that file; this file refuses to place one that still carries a probability,
because a prior run's own score in a reader's input is the one leak that makes
the next prediction unfalsifiable.

Layout, under the run directory the bundle already occupies::

    runs/{ticker}/{accession}/            the committed bundle -- the record
    runs/{ticker}/{accession}/agents/     nothing but the six directories
    runs/{ticker}/{accession}/agents/numbers-reader/   a session root

The agent directories do not sit directly beside the bundle files on purpose.
One step out of a session root has to land somewhere, and it lands in a
directory that holds no file at all -- not a report, not a filing, not the
market table. The run directory above that holds the whole bundle, because it
is the record of what was fetched.

**What a tree can promise and what it cannot.** A filesystem cannot make a
sibling unreachable: six directories that must coexist under one run share an
ancestor, and from that ancestor everything hangs. What this file guarantees is
the part a tree can carry -- each session root holds exactly its layer's files,
nothing inside a root resolves outside it (no symlink, no `..`, no path into the
bundle), no root sits inside another, and the directory that holds the six holds
nothing else. The last step, the one out of the root, is the one the session
root itself forbids, and that is why `docs/INPUT_SPEC.md` says the root is the
enforcement and the prompt is a statement of intent.

**`input_8k.md` goes to both readers**, and it is coarser than
`docs/INPUT_SPEC.md` §1, which routes the earnings-release figures to the
numbers reader and the 8-K 1.01/4.01/4.02/5.02 bodies to the notes-text reader.
`src/assemble_bundle.py` writes them into one file, so the split cannot be made
here without a second file. Both readers are the same layer, so nothing crosses
a layer; the coarseness is named rather than left to be noticed.

**`input_controls.md` is the ninth bundle file.** §6 does not list it and §1
requires what it holds -- the auditor's report with its critical audit matters,
Item 9A, and the 10-Q's Item 4 -- to reach the notes-text reader.
`src/assemble_bundle.py` records that conflict and writes the file; this routes
it where §1 sends it.

**A supervisor gets the four reports and nothing else today.** Its prompt says
its directory also holds the rules version's checklist keys and output schema.
§6 names no file for those and `rules/v0.1` does not exist, so there is nothing
to route; the default is the four reports, and the day the rules version exists
its files are added to the supervisors' `sees` and to the catalogue.

    python3.12 -m src.agent_inputs --run runs/AAPL/0000320193-25-000073
    python3.12 -m src.agent_inputs --run <dir> --agent numbers-reader

Exit 0 clean, 2 the run directory cannot be routed, 3 the wrong interpreter.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    from src import interpreter_pin
except ImportError:  # invoked as a plain script: python3.12 src/agent_inputs.py
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import interpreter_pin

BAD_INPUT = 2

# The directory that holds the six. It holds nothing else, ever. The run
# directory is named by `src/assemble_bundle.py`, which owns where a run lands;
# this file is handed one and never invents a path under `runs/`.
AGENTS_DIRNAME = "agents"

# Every file `docs/INPUT_SPEC.md` §6 names, plus `input_controls.md`. A name
# outside this set inside a session root is a file nobody decided to route, and
# an undecided file in an agent's directory is a leak nobody chose either.
BUNDLE_CATALOGUE = (
    "input_numbers.json",
    "input_companyfacts.json",
    "input_trends.json",
    "input_notes.md",
    "input_notes_history.md",
    "input_mdna.md",
    "input_controls.md",
    "input_exhibits.md",
    "input_risk_factors.md",
    "input_8k.md",
    "input_prior_predictions.md",
    "input_market.json",
    "input_manifest.json",
    "report_numbers.md",
    "report_notes_text.md",
    "report_numbers_vs_market.md",
    "report_notes_vs_market.md",
    "prediction_accounting.json",
    "prediction_pressure.json",
    "explanations.json",
    "baselines.json",
    "control_single_agent_accounting.json",
    "control_single_agent_pressure.json",
    "control_shuffled_accounting.json",
    "control_shuffled_pressure.json",
)

# The three §6 names no builder in this repository writes yet. They are routed
# when they exist and their absence is recorded rather than refused, because a
# run that has not got them is early, not broken. Everything else an agent is
# given must be there: a comparer directory assembled before the readers ran
# holds the market table and no reports, and that is a broken run wearing the
# right shape.
NOT_BUILT_YET = ("input_companyfacts.json", "input_exhibits.md",
                 "input_risk_factors.md")

# What a prior prediction may never carry into a reader's input. The pattern is
# the key shape a JSON dump leaves behind, not the bare word: the trend table
# legitimately names the Piotroski F-score and the Altman Z-score, and a check
# that read those as probabilities would refuse every run.
PROBABILITY_KEYS = ("probability", "probabilities", "score", "scores",
                    "likelihood", "confidence", "p_up")
PROBABILITY_KEY = re.compile(
    '"(' + "|".join(PROBABILITY_KEYS) + r')"\s*:', re.IGNORECASE)

READER_REPORTS = ("report_numbers.md", "report_notes_text.md")
ALL_REPORTS = READER_REPORTS + ("report_numbers_vs_market.md",
                                "report_notes_vs_market.md")
MARKET_TABLE = "input_market.json"


class AgentInputError(Exception):
    """The directory cannot be built as the layer table describes it."""


@dataclass(frozen=True)
class Agent:
    """One agent, its layer, and every file its directory may hold."""

    name: str
    layer: str
    sees: tuple[str, ...]
    may_be_absent: tuple[str, ...] = ()

    @property
    def never_sees(self) -> tuple[str, ...]:
        return tuple(name for name in BUNDLE_CATALOGUE if name not in self.sees)

    @property
    def required(self) -> tuple[str, ...]:
        allowed = set(self.may_be_absent) | set(NOT_BUILT_YET)
        return tuple(name for name in self.sees if name not in allowed)


AGENTS: dict[str, Agent] = {
    agent.name: agent for agent in (
        # readers: the filing bundle for one company, and never a price.
        Agent("numbers-reader", "reader",
              ("input_numbers.json", "input_companyfacts.json",
               "input_trends.json", "input_8k.md",
               "input_prior_predictions.md")),
        Agent("notes-text-reader", "reader",
              ("input_notes.md", "input_notes_history.md", "input_mdna.md",
               "input_controls.md", "input_exhibits.md",
               "input_risk_factors.md", "input_8k.md",
               "input_prior_predictions.md")),
        # comparers: both reader reports plus the market table, and never a filing.
        Agent("numbers-vs-market", "comparer", READER_REPORTS + (MARKET_TABLE,)),
        Agent("notes-vs-market", "comparer", READER_REPORTS + (MARKET_TABLE,)),
        # supervisors: the four reports, and neither a filing nor the market
        # table. The notes-versus-market report is the one that may be absent:
        # a light run on an 8-K 2.02 skips that comparer, because the notes are
        # not public yet, and produces three reports rather than four.
        Agent("supervisor-accounting", "supervisor", ALL_REPORTS,
              may_be_absent=("report_notes_vs_market.md",)),
        Agent("supervisor-pressure", "supervisor", ALL_REPORTS,
              may_be_absent=("report_notes_vs_market.md",)),
    )
}

# A light run on an 8-K 2.02 produces three reports, not four: both readers, the
# numbers-versus-market comparer and supervisor-pressure. `docs/INPUT_SPEC.md`
# §1 says why. Pass this to build_all when that is the run.
LIGHT_RUN = ("numbers-reader", "notes-text-reader", "numbers-vs-market",
             "supervisor-pressure")


def agents_root(run: Path) -> Path:
    """The one directory that holds the six. Naming it does not make it."""
    return Path(run) / AGENTS_DIRNAME


def session_root(run: Path, agent: str) -> Path:
    """Where an agent's session is rooted. Its own directory, never the run's."""
    if agent not in AGENTS:
        raise AgentInputError(f"{agent!r} is not an agent; "
                              f"one of {', '.join(AGENTS)}")
    return agents_root(run) / agent


def _probability_leak(text: str) -> str | None:
    found = PROBABILITY_KEY.search(text)
    return found.group(0) if found else None


def _place(source: Path, target: Path) -> None:
    """Copy the bytes. Never link: a link's ancestors are the bundle's.

    Bytes, and not `cutoff_guard.load_bundle_file`, which the rest of the
    repository reads a bundle with: that returns text, and text mode translates
    a `\\r\\n` into a `\\n`. What an agent is handed has to be what was committed,
    byte for byte, because every quote it writes is string-matched against it.
    The bundle carries no date gate of its own — `src/extraction_checks.py`
    checks a bundle's cutoff against its own manifest — so nothing is skipped
    by copying the bytes here.
    """
    data = source.read_bytes()
    if target.exists():
        if target.read_bytes() != data:
            raise AgentInputError(
                f"{target} already exists with different bytes. A run directory "
                "is append-only: existing content is never changed. A correction "
                "is a new run, not an overwrite.")
        return
    target.write_bytes(data)


def build(run: Path, agent: str) -> dict:
    """One agent's directory, holding its layer's files and nothing else.

    `run` is the run directory the bundle occupies. The directory is created
    under it; nothing else is created, and `runs/` is never made as a side
    effect of naming it.
    """
    run = Path(run)
    root = session_root(run, agent)  # refuses a name that is not an agent
    spec = AGENTS[agent]
    if not run.is_dir():
        raise AgentInputError(f"{run} is not a run directory")

    missing = [name for name in spec.required if not (run / name).is_file()]
    if missing:
        raise AgentInputError(
            f"{agent}: the run directory has no {', '.join(missing)}. A "
            f"{spec.layer} directory assembled before its inputs exist holds "
            "the right shape and the wrong run.")

    # Before anything is created: a prior run's own score in a reader's input
    # makes the next prediction unfalsifiable. The probabilities are dropped
    # where the file is written, in src/assemble_bundle.py; this is the gate
    # that says they were.
    prior = run / "input_prior_predictions.md"
    if "input_prior_predictions.md" in spec.sees and prior.is_file():
        leak = _probability_leak(prior.read_text(encoding="utf-8", errors="replace"))
        if leak is not None:
            raise AgentInputError(
                f"{prior} still carries a probability ({leak}); a prior run's "
                f"probability may not reach {agent}.")

    root.mkdir(parents=True, exist_ok=True)
    stray = sorted(path.name for path in root.iterdir()
                   if path.name not in spec.sees)
    if stray:
        raise AgentInputError(
            f"{root} already holds {', '.join(stray)}, which a {spec.layer} "
            "never sees. The directory is the boundary; it is not cleaned out "
            "and reused.")

    placed, absent = [], []
    for name in spec.sees:
        source = run / name
        if not source.is_file():
            absent.append(name)
            continue
        _place(source, root / name)
        placed.append(name)
    return {"agent": agent, "layer": spec.layer, "root": root,
            "files": placed, "absent": absent}


def build_all(run: Path, agents: tuple[str, ...] | None = None) -> list[dict]:
    """Every agent's directory for one run, in the order the layers run."""
    return [build(run, name) for name in (agents or tuple(AGENTS))]


# --- the boundary, checked ----------------------------------------------------

def escapes(root: Path) -> list[str]:
    """Every path inside `root` that resolves outside it.

    A symlink into the bundle is the leak that matters: walking up from what it
    resolves to lands in the run directory, and every other agent's directory
    hangs off that. A copy's ancestors are its own root and nothing else.
    """
    root = Path(root)
    anchor = root.resolve()
    found = []
    for path in sorted(root.rglob("*")):
        resolved = path.resolve()
        if anchor not in resolved.parents:
            found.append(f"{path} resolves to {resolved}, outside {root}")
    return found


def agent_directories(run: Path) -> dict[Path, str]:
    """Every directory under `run` named for an agent, wherever it sits.

    Found rather than assumed. A layout that groups the six by layer —
    `agents/readers/numbers-reader` beside `agents/readers/notes-text-reader` —
    holds each agent's right files and puts the other reader one step out of the
    root, and a check that looked only where it expected the directory to be
    would report that layout clean.
    """
    return {path: path.name
            for path in sorted(Path(run).rglob("*"))
            if path.name in AGENTS and path.is_dir()}


def isolation_violations(run: Path) -> list[str]:
    """Every way an agent could reach what its layer never sees. Empty is clean.

    Five kinds, in the order they matter:

    1. an agent's directory somewhere other than its session root;
    2. a file in one that the layer never sees, or that nobody routed at all;
    3. something inside one that resolves outside it — a symlink or a `..` into
       the bundle, whose own ancestors are the run directory and every other
       agent's directory hanging off it;
    4. one agent's directory inside another's, the sharpest form of a readable
       sibling, because climbing out of the inner one lands in the outer;
    5. anything but an agent directory in the directory a session root sits in,
       so that one step out of a root yields no file. This is what keeps the
       roots out of the run directory itself, where the bundle is: a reader
       whose root sat beside it would have the market table one `..` away.
    """
    run = Path(run)
    live = agent_directories(run)
    found = []

    for root, name in live.items():
        spec = AGENTS[name]
        if root != session_root(run, name):
            found.append(f"{name}: its directory sits at {root}, not at its "
                         f"session root {session_root(run, name)}")
        for path in sorted(root.iterdir()):
            if path.name in spec.sees:
                continue
            reason = ("which its layer never sees" if path.name in spec.never_sees
                      else "which nobody routed")
            found.append(f"{name}: holds {path.name}, {reason}")
        found.extend(f"{name}: {line}" for line in escapes(root))
        for ancestor in root.parents:
            if ancestor in live:
                found.append(f"{name}: its session root sits inside {ancestor}, "
                             f"which is {live[ancestor]}'s directory")

    for holder in sorted({root.parent for root in live}):
        strangers = sorted(path.name for path in holder.iterdir()
                           if path not in live)
        if strangers:
            found.append(f"{holder} holds {', '.join(strangers)}; the directory "
                         "a session root sits in holds agent directories and "
                         "nothing else, so one step out of a root yields no file")
    return found


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="one input directory per agent, under a run directory")
    parser.add_argument("--run", required=True,
                        help="the run directory the bundle occupies")
    parser.add_argument("--agent", default=None, choices=list(AGENTS),
                        help="one agent; the default is all six")
    parser.add_argument("--light", action="store_true",
                        help="an 8-K 2.02 light run: three reports, not four")
    args = parser.parse_args(argv)

    if args.agent and args.light:
        print("agent_inputs: --agent and --light name different sets; pick one",
              file=sys.stderr)
        return BAD_INPUT
    chosen = (args.agent,) if args.agent else (LIGHT_RUN if args.light else None)
    run = Path(args.run)
    try:
        built = build_all(run, chosen)
    except (AgentInputError, OSError) as exc:
        print(f"agent_inputs: {exc}", file=sys.stderr)
        return BAD_INPUT

    broken = isolation_violations(run)
    for record in built:
        absent = f", {len(record['absent'])} not built yet" if record["absent"] else ""
        print(f"agent_inputs: {record['agent']} ({record['layer']}) "
              f"{len(record['files'])} files{absent} → {record['root']}")
    if broken:
        print(f"agent_inputs: the boundary is broken ({len(broken)}):",
              file=sys.stderr)
        for line in broken:
            print(f"  {line}", file=sys.stderr)
        return BAD_INPUT
    return 0


if __name__ == "__main__":
    raise SystemExit(interpreter_pin.enforce() or main())
