"""One input directory per agent per run. The directory is the boundary.

`docs/INPUT_SPEC.md` states the rule as a table, and this file is that table
turned into directories:

| Layer | Sees | Never sees |
|---|---|---|
| readers | the filing bundle for one company | prices, short interest, any other company |
| accounting and financial analysts | the two reader reports and `calculator_filings_only.json` | any filing, any price, the market table |
| valuation analyst | the calculator with the price at the cutoff, both checked analyses, the MD&A and the earnings release | a price after the cutoff, the market table |

**The comparers are Python, and no directory is built for them.** The owner's
decision of 2026-10-06 turned the two comparers into `src/market_labels.py`,
which reads the two reader reports and the market table in the run directory
and writes `market_labels.json`; a function needs no session root. The two
comparer definitions and the two supervisor definitions moved to
`archive/agents/`. They are kept below in `RETIRED_AGENTS`, as the record of
what each of them saw and wrote on the pilot runs, so the quote gate can still
re-check what they wrote; nothing builds a directory for one, and nothing runs
one.

Two files are named in the spec so they are routed to somebody:
`input_notes_history.md` goes to the notes-text reader, and
`input_prior_predictions.md` goes to both readers **with the probability numbers
removed**. `src/assemble_bundle.py` drops the probability keys when it writes
that file; this file refuses to place one that still carries a probability,
because a prior run's own score in a reader's input is the one leak that makes
the next prediction unfalsifiable.

Layout, under the run directory the bundle already occupies::

    runs/{ticker}/{accession}/            the committed bundle -- the record
    runs/{ticker}/{accession}/agents/     nothing but the agents' directories
    runs/{ticker}/{accession}/agents/numbers-reader/   a session root

The agent directories do not sit directly beside the bundle files on purpose.
One step out of a session root has to land somewhere, and it lands in a
directory that holds no file at all -- not a report, not a filing, not the
market table. The run directory above that holds the whole bundle, because it
is the record of what was fetched.

**What a tree can promise and what it cannot.** A filesystem cannot make a
sibling unreachable: directories that must coexist under one run share an
ancestor, and from that ancestor everything hangs. What this file guarantees is
the part a tree can carry -- each session root holds exactly its layer's files,
nothing inside a root resolves outside it (no symlink, no `..`, no path into the
bundle), no root sits inside another, and the directory that holds them holds
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

**The retired supervisors' rules files.** `src/decide.py` wrote
`rules_output_schema.md` and `rules_checklist_keys.md` into the run directory
for the two supervisors, and they stay in the catalogue because the pilot runs
on record hold them. No live agent is routed either.

**A run with no market table.** `input_manifest.json` says so with
`market_table: "unavailable"` and a `market_table_reason`, which
`src/decide.py` writes, together with the label of each of the two market
comparisons -- numbers versus market, notes versus market -- written `absent`.
A manifest that says its market table is unavailable and labels either
comparison anything but `absent` is refused before any analyst's directory is
built. The owner's decisions of 2026-09-13 and 2026-09-23: the first analyses
publish on filings alone.

**Where an agent's own output lands.** Each prompt names exactly one file to
write — `report_numbers.md`, `report_notes_text.md`, the two analyses, the
valuation analyst's drivers and its reading — and each agent has `Write` and a
session rooted at its own directory, so that file can land nowhere else. It is
the agent's `writes`: never
placed by this file, allowed in the root afterwards, and not read as a leak. A
boundary check that called an agent's own report a stray would report every
completed run as broken, which is the same as reporting nothing.

    python3.12 -m src.agent_inputs --run runs/AAPL/0000320193-25-000073
    python3.12 -m src.agent_inputs --run <dir> --agent numbers-reader

Exit 0 clean, 2 the run directory cannot be routed, 3 the wrong interpreter.
"""

from __future__ import annotations

import argparse
import json
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

# The directory that holds the agents' directories. It holds nothing else, ever. The run
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
    "rules_checklist_keys.md",
    "rules_output_schema.md",
    "report_numbers.md",
    "report_notes_text.md",
    "report_numbers_vs_market.md",
    "report_notes_vs_market.md",
    "market_labels.json",
    "prediction_accounting.json",
    "prediction_pressure.json",
    "explanations.json",
    "baselines.json",
    "control_single_agent_accounting.json",
    "control_single_agent_pressure.json",
    # The owner's decision of 2026-09-28: the calculator, and the three analyses.
    "calculator.json",
    "calculator_before_analysts.json",
    "calculator_before_drivers.json",
    "calculator_filings_only.json",
    "analysis_accounting.json",
    "analysis_financial.json",
    "assumptions.json",
    "analysis_valuation.json",
    "memo_ko.md",
    "control_analysis_accounting.json",
    "control_analysis_financial.json",
    "control_assumptions.json",
)

# The three §6 names no builder in this repository writes yet. They are routed
# when they exist and their absence is recorded rather than refused, because a
# run that has not got them is early, not broken. Everything else an agent is
# given must be there: an analyst directory assembled before the readers ran
# holds the calculator and no reports, and that is a broken run wearing the
# right shape.
NOT_BUILT_YET = ("input_companyfacts.json", "input_exhibits.md",
                 "input_risk_factors.md")

# What a prior prediction may never carry into a reader's input. The pattern is
# the key shape a JSON dump leaves behind, not the bare word: the trend table
# legitimately names the Piotroski F-score and the Altman Z-score, and a check
# that read those as probabilities would refuse every run.
#
# The four the prediction schema in `docs/CHECKLIST.md` §7 gives a probability
# to are named one by one — `checklist[].confidence`, `events[].p_within_horizon`,
# `explanations[].realization_p`, `market_direction.p_up`. A gate that covered
# two of the four would say a file was clean while a prior run's own score sat
# in it; `continuous[]`'s `point`, `low` and `high` are intervals, not
# probabilities, and are not here.
PREDICTION_PROBABILITY_KEYS = ("confidence", "p_within_horizon",
                               "realization_p", "p_up")
PROBABILITY_KEYS = ("probability", "probabilities", "score", "scores",
                    "likelihood") + PREDICTION_PROBABILITY_KEYS
PROBABILITY_KEY = re.compile(
    '"(' + "|".join(PROBABILITY_KEYS) + r')"\s*:', re.IGNORECASE)

READER_REPORTS = ("report_numbers.md", "report_notes_text.md")
COMPARER_REPORTS = ("report_numbers_vs_market.md", "report_notes_vs_market.md")
ALL_REPORTS = READER_REPORTS + COMPARER_REPORTS
FILINGS_ONLY = "calculator_filings_only.json"
VALUATION_READS = ("analysis_accounting.json", "analysis_financial.json",
                   "input_mdna.md", "input_8k.md")
MARKET_TABLE = "input_market.json"
MANIFEST = "input_manifest.json"

# The rules version's checklist keys and output schema, which both retired
# supervisor prompts said their directory held. Written by `src/decide.py`.
RULES_FILES = ("rules_checklist_keys.md", "rules_output_schema.md")

# How a run's manifest says it has no market table, and why.
MARKET_TABLE_KEY = "market_table"
MARKET_REASON_KEY = "market_table_reason"
MARKET_UNAVAILABLE = "unavailable"


class AgentInputError(Exception):
    """The directory cannot be built as the layer table describes it."""


@dataclass(frozen=True)
class Agent:
    """One agent, its layer, the files it may read and the one file it writes.

    `writes` is the file the agent's own prompt tells it to write — "Write
    `report_numbers.md`. Nothing else, anywhere." — and its session is rooted at
    this directory, so that is where the file lands. It is not something the
    layer *sees*: the builder never places it, and the run that produced it is
    the only thing that may put it there.
    """

    name: str
    layer: str
    sees: tuple[str, ...]
    writes: str
    # The committed definition this directory runs, under `.claude/agents/`.
    # The directory's own name unless one definition runs in two directories,
    # as the valuation analyst's two passes do.
    runs: str | None = None

    @property
    def prompt(self) -> str:
        return self.runs or self.name

    @property
    def may_hold(self) -> tuple[str, ...]:
        """Everything the directory may ever hold: its inputs and its output."""
        return self.sees + (self.writes,)

    @property
    def never_sees(self) -> tuple[str, ...]:
        return tuple(name for name in BUNDLE_CATALOGUE
                     if name not in self.may_hold)

    def required(self) -> tuple[str, ...]:
        """The files that have to be on record before this directory is built."""
        return tuple(name for name in self.sees if name not in NOT_BUILT_YET)


# A light run on an 8-K 2.02 wakes the two readers on the earnings release. Its
# comparer and its supervisor were retired on 2026-10-06: the market label on
# the earnings-release window is `src/market_labels.py`'s, and which analyst a
# light run wakes is not decided, so it wakes none.
LIGHT_RUN = ("numbers-reader", "notes-text-reader")

AGENTS: dict[str, Agent] = {
    agent.name: agent for agent in (
        # readers: the filing bundle for one company, and never a price.
        Agent("numbers-reader", "reader",
              ("input_numbers.json", "input_companyfacts.json",
               "input_trends.json", "input_8k.md",
               "input_prior_predictions.md"),
              writes="report_numbers.md"),
        Agent("notes-text-reader", "reader",
              ("input_notes.md", "input_notes_history.md", "input_mdna.md",
               "input_controls.md", "input_exhibits.md",
               "input_risk_factors.md", "input_8k.md",
               "input_prior_predictions.md"),
              writes="report_notes_text.md"),
        # analysts: the two reader reports and what Python computed from the
        # filings alone -- never a filing, never a price. The owner's decision of
        # 2026-09-28; the three analyses are never merged.
        Agent("accounting-analyst", "analyst", READER_REPORTS + (FILINGS_ONLY,),
              writes="analysis_accounting.json"),
        Agent("financial-analyst", "analyst", READER_REPORTS + (FILINGS_ONLY,),
              writes="analysis_financial.json"),
        # the valuation analyst: the whole calculator, price at the cutoff
        # included, the two analyses, and the MD&A and the earnings release
        # verbatim. Two passes, two directories, one definition.
        # The first pass sees the calculator with the accounting adjustments
        # applied and no DCF; the second, the calculator with the DCF Python ran
        # on the first pass's drivers. Each is its own file, written once.
        Agent("valuation-analyst", "valuation",
              ("calculator_before_drivers.json",) + VALUATION_READS,
              writes="assumptions.json"),
        Agent("valuation-analyst-second-pass", "valuation",
              ("calculator.json",) + VALUATION_READS + ("assumptions.json",),
              writes="analysis_valuation.json", runs="valuation-analyst"),
    )
}

# The pilot layer, retired from the live pipeline: the two comparers on
# 2026-10-06, when their label became `src/market_labels.py`, and the two
# supervisors, which the analysts replaced on 2026-09-28. Their definitions are
# in `archive/agents/`. Nothing builds a directory for one and nothing runs one:
# `session_root` refuses each name. They stay here as the record of what each
# saw and wrote, because the pilot runs on record hold their reports and the
# quote gate re-checks those.
RETIRED_AGENTS: dict[str, Agent] = {
    agent.name: agent for agent in (
        Agent("numbers-vs-market", "comparer", READER_REPORTS + (MARKET_TABLE,),
              writes="report_numbers_vs_market.md"),
        Agent("notes-vs-market", "comparer", READER_REPORTS + (MARKET_TABLE,),
              writes="report_notes_vs_market.md"),
        Agent("supervisor-accounting", "supervisor", ALL_REPORTS + RULES_FILES,
              writes="prediction_accounting.json"),
        Agent("supervisor-pressure", "supervisor", ALL_REPORTS + RULES_FILES,
              writes="prediction_pressure.json"),
    )
}

# The two market comparisons, numbers versus market and notes versus market.
# Python's now, and still two: a run's manifest names each one's label, and a
# run with no market table writes each as `absent` -- not `not_priced`, which is
# a reading of a market. The names are the ones the pilot manifests on record
# carry, so a manifest written today reads the same as one written then.
COMPARERS = ("numbers-vs-market", "notes-vs-market")
COMPARER_LABELS_KEY = "comparer_labels"
ABSENT = "absent"


def agents_root(run: Path) -> Path:
    """The one directory that holds the agents'. Naming it does not make it."""
    return Path(run) / AGENTS_DIRNAME


def session_root(run: Path, agent: str) -> Path:
    """Where an agent's session is rooted. Its own directory, never the run's."""
    if agent in RETIRED_AGENTS:
        raise AgentInputError(f"{agent!r} was retired from the live pipeline; its "
                              "definition is in archive/agents/ and nothing builds "
                              "a directory for it")
    if agent not in AGENTS:
        raise AgentInputError(f"{agent!r} is not an agent; "
                              f"one of {', '.join(AGENTS)}")
    return agents_root(run) / agent


def market_unavailable(run) -> str | None:
    """Why this run has no market table, or None when its manifest does not say it has none.

    A run with no manifest, or one that does not name `market_table`, is a run
    whose market table is expected like any other input. One that names it
    `unavailable` and gives no reason is refused: the reason is what the
    owner's decision puts on the record. So is one whose comparer labels are
    anything but `absent` for both comparisons: no market was read.
    """
    path = Path(run) / MANIFEST
    if not path.is_file():
        return None
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except ValueError as exc:
        raise AgentInputError(f"{path} does not read as JSON: {exc}") from exc
    if not isinstance(manifest, dict):
        raise AgentInputError(f"{path} is not an object")
    said = manifest.get(MARKET_TABLE_KEY)
    if said is None:
        return None
    reason = manifest.get(MARKET_REASON_KEY)
    if said != MARKET_UNAVAILABLE or not isinstance(reason, str) or not reason.strip():
        raise AgentInputError(
            f"{path} says the market table is {said!r} because {reason!r}. The "
            f"one thing it may say is {MARKET_UNAVAILABLE!r}, with a reason")
    labels = {name: ABSENT for name in COMPARERS}
    if manifest.get(COMPARER_LABELS_KEY) != labels:
        raise AgentInputError(
            f"{path} says the market table is unavailable and writes the comparer "
            f"labels as {manifest.get(COMPARER_LABELS_KEY)!r}. No comparer ran, so "
            f"each is {ABSENT!r}: {labels!r}")
    return reason


def _probability_leak(text: str) -> str | None:
    found = PROBABILITY_KEY.search(text)
    return found.group(0) if found else None


# The valuation analyst reads the MD&A and the earnings release only where the
# notes reader flagged a paragraph: Fable, used efficiently (the owner's decision
# of 2026-10-06, `docs/HOW_WE_WORK.md` §6). The file keeps its name and its `[id]`
# blocks byte for byte, so a quote of one still string-matches, and it holds no
# text the filing does not: where two kept blocks were not adjacent in the
# filing, one line holding only their two `[id]` markers stands between them, so
# a quote running off the end of one into the start of the next carries a line
# the filing never printed and matches nothing there. How much was left out is
# the manifest's to say, under `agents.<name>.trimmed`, written when the file is
# routed; the boundary check reads that record, never this trim, to say what the
# directory should hold. A paragraph the notes reader did not flag is not placed,
# and no agent can quote what it was not handed.
TRIMMED_FOR_VALUATION = ("input_mdna.md", "input_8k.md")
NOTES_REPORT = "report_notes_text.md"
TRIMMED_KEY = "trimmed"
ID_LINE = re.compile(r"^\[(\d{10}-\d{2}-\d{6}:[a-z0-9_]+:[^\]]+)\]\s*$", re.M)
FENCED_JSON = re.compile(r"```json\s*(.*?)```", re.S)


def flagged_paragraphs(run: Path) -> set[str]:
    """Every paragraph id the notes reader's standing items cite.

    The copy at the run root is the gated one, but the gate takes a fenced block
    out only when every item in it was dropped, and a reader writes its items as
    one list: a dropped item standing in a block beside a kept one is still in
    the file. The manifest's drop list is what says it fell -- read through
    `src.market_labels.gate_record`, the one reading of that list, keyed the way
    the gate keys it, (report, `quote_gate.item_id`) -- and an item it names
    flags nothing: it was dropped and counted, not passed through. A run with no
    record that the gate ran is refused, as the market labels refuse it.
    """
    # here, not at the top: both of these import this module when they load
    from src import market_labels, quote_gate
    report = Path(run) / NOTES_REPORT
    if not report.is_file():
        return set()
    try:
        _, dropped = market_labels.gate_record(run)
    except market_labels.MarketLabelError as exc:
        raise AgentInputError(
            f"{run}: no record that the quote gate ran over {NOTES_REPORT}, so no "
            f"paragraph can be read as flagged: {exc}") from exc
    found = set()
    for block in FENCED_JSON.findall(report.read_text(encoding="utf-8", errors="replace")):
        try:
            data = json.loads(block)
        except ValueError:
            continue
        for item in data if isinstance(data, list) else [data]:
            if (isinstance(item, dict) and isinstance(item.get("paragraph_id"), str)
                    and (NOTES_REPORT, quote_gate.item_id(item)) not in dropped):
                found.add(item["paragraph_id"])
    return found


def paragraph_ids(text: str) -> list[str]:
    """The `[id]` markers of a prose file, in the file's order."""
    return [mark.group(1) for mark in ID_LINE.finditer(text)]


def seam(before: str, after: str) -> str:
    """The one line that stands between two kept blocks that were not adjacent in
    the filing: their own two markers and nothing else."""
    return f"[{before}] [{after}]\n\n"


def trimmed(text: str, keep: set[str]) -> str:
    """The prose file with only the `[id]` blocks in `keep`, each verbatim, and a
    seam line between two kept blocks that were not adjacent. Nothing else: the
    note on how much was left out is the manifest's."""
    marks = list(ID_LINE.finditer(text))
    preamble = text[:marks[0].start()] if marks else text
    parts, previous = [], None
    for index, (this, following) in enumerate(zip(marks, marks[1:] + [None])):
        if this.group(1) not in keep:
            continue
        if previous is not None and index != previous + 1:
            parts.append(seam(marks[previous].group(1), this.group(1)))
        parts.append(text[this.start():following.start() if following else len(text)])
        previous = index
    return preamble + "".join(parts)


def trim_record(text: str, keep: set[str]) -> dict:
    """What the manifest records of one trimmed file: the ids kept, in the file's
    order, out of how many, and why."""
    ids = paragraph_ids(text)
    kept = [identifier for identifier in ids if identifier in keep]
    return {"kept": kept, "of": len(ids),
            "note": f"{len(kept)} of {len(ids)} paragraphs, the ones the notes reader "
                    "flagged; the rest were not placed"}


def handed(text: str, record: dict) -> str:
    """What a trimmed file should hold, re-derived from the run's own file and the
    manifest's record of the trim, and not from the trim: the preamble, then the
    block of each id the record lists, cut out of the file by its marker, in the
    order listed, with the seam line between two that were not adjacent.

    A record that does not fit the file -- an id the file has no block for, a
    count that is not the file's, an order that is not the file's -- is refused:
    it is not a record of this file.
    """
    marks = list(ID_LINE.finditer(text))
    cuts = [mark.start() for mark in marks] + [len(text)]
    blocks = {mark.group(1): (index, text[cuts[index]:cuts[index + 1]])
              for index, mark in enumerate(marks)}
    kept, total = record.get("kept"), record.get("of")
    if not isinstance(kept, list) or total != len(marks):
        raise AgentInputError(f"the manifest's trimmed record says {total!r} paragraphs "
                              f"and the run's file holds {len(marks)}")
    out, previous = [text[:marks[0].start()] if marks else text], None
    for identifier in kept:
        if identifier not in blocks:
            raise AgentInputError(f"the manifest's trimmed record keeps {identifier!r}, "
                                  "which the run's file has no block for")
        index, block = blocks[identifier]
        if previous is not None and index <= previous:
            raise AgentInputError(f"the manifest's trimmed record lists {identifier!r} "
                                  "out of the file's order")
        if previous is not None and index != previous + 1:
            out.append(seam(marks[previous].group(1), identifier))
        out.append(block)
        previous = index
    return "".join(out)


def record_trim(run: Path, agent: str, record: dict[str, dict]) -> None:
    """`agents.<agent>.trimmed` into the run's manifest, every other key left alone,
    the convention the quote gate writes its counts by."""
    path = Path(run) / MANIFEST
    manifest = json.loads(path.read_text(encoding="utf-8"))
    agents = manifest.setdefault("agents", {})
    entry = agents.get(agent)
    if not isinstance(entry, dict):
        entry = agents[agent] = {}
    entry[TRIMMED_KEY] = record
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def recorded_trim(run: Path, agent: str) -> dict | None:
    """The manifest's record of what was trimmed for this agent's directory, or
    None when it records no trim: a directory built before the trim holds the
    full file, and the manifest's silence is the record of that."""
    path = Path(run) / MANIFEST
    if not path.is_file():
        return None
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except ValueError:
        return None
    entry = (manifest.get("agents") or {}).get(agent) if isinstance(manifest, dict) else None
    record = entry.get(TRIMMED_KEY) if isinstance(entry, dict) else None
    return record if isinstance(record, dict) else None


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
    if target.is_symlink():
        # Before the source is read, and before `exists()`: both it and
        # `read_bytes()` follow the link, so a link into the bundle holding the
        # right bytes reads as already placed and is left where it is — a file
        # whose `..` is the run directory, recorded as a copy.
        raise AgentInputError(
            f"{target} is a symlink to {target.readlink()}. An agent's file is "
            "copied, never linked: a link's ancestors are the bundle's.")
    _place_bytes(source.read_bytes(), target)


def _place_bytes(data: bytes, target: Path) -> None:
    if target.exists():
        if target.read_bytes() != data:
            raise AgentInputError(
                f"{target} already exists with different bytes. A run directory "
                "is append-only: existing content is never changed. A correction "
                "is a new run, not an overwrite.")
        return
    target.write_bytes(data)


def build(run: Path, agent: str, *, light: bool = False) -> dict:
    """One agent's directory, holding its layer's files and nothing else.

    `run` is the run directory the bundle occupies. The directory is created
    under it; nothing else is created, and `runs/` is never made as a side
    effect of naming it.

    `light` is the 8-K 2.02 run. It changes nothing a directory holds since its
    comparer and its supervisor were retired; it is kept so the command's
    `--light` still names the agents a light run wakes.
    """
    run = Path(run)
    root = session_root(run, agent)  # refuses a name that is not an agent
    spec = AGENTS[agent]
    if not run.is_dir():
        raise AgentInputError(f"{run} is not a run directory")

    # A reader's directory does not depend on the market. Every other layer
    # reads the manifest, which refuses one that says two things about it.
    if spec.layer != "reader":
        market_unavailable(run)

    missing = [name for name in spec.required()
               if not (run / name).is_file()]
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
    # `may_hold`, not `sees`: rebuilding after the agent has run must not read
    # the report the agent itself wrote here as somebody else's file.
    may_hold = set(spec.may_hold)
    stray = sorted(path.name for path in root.iterdir()
                   if path.name not in may_hold)
    if stray:
        raise AgentInputError(
            f"{root} already holds {', '.join(stray)}, which a {spec.layer} "
            "never sees. The directory is the boundary; it is not cleaned out "
            "and reused.")

    placed, absent, trims = [], [], {}
    flagged = flagged_paragraphs(run) if spec.layer == "valuation" else None
    for name in spec.sees:
        source = run / name
        if not source.is_file():
            absent.append(name)
            continue
        if flagged is not None and name in TRIMMED_FOR_VALUATION:
            if (root / name).is_symlink():
                raise AgentInputError(f"{root / name} is a symlink; an agent's file is copied")
            text = source.read_text(encoding="utf-8", errors="replace")
            _place_bytes(trimmed(text, flagged).encode("utf-8"), root / name)
            trims[name] = trim_record(text, flagged)
        else:
            _place(source, root / name)
        placed.append(name)
    if trims:
        # the record of what was handed, written as it is handed; the boundary
        # check reads this, not the trim, to say what the directory should hold
        record_trim(run, agent, trims)
    return {"agent": agent, "layer": spec.layer, "root": root,
            "files": placed, "absent": absent, TRIMMED_KEY: trims}


def build_all(run: Path, agents: tuple[str, ...] | None = None, *,
              light: bool = False) -> list[dict]:
    """Every agent's directory for one run, in the order the layers run."""
    return [build(run, name, light=light)
            for name in (agents or tuple(AGENTS))]


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


def expected_bytes(run: Path, spec: Agent, name: str, trim: dict | None = None) -> bytes | None:
    """What a routed file should hold: the run's copy, byte for byte -- or, when
    the manifest records a trim of it for this agent (`trim`, the file's entry
    under `agents.<name>.trimmed`), the run's copy cut down by that record.

    The record, not the trim: `handed` re-derives the bytes from the run's file
    and the ids the manifest says were kept, so a wrong trim and this check do
    not move together. A valuation directory the manifest records no trim for
    was built before the trim and holds the full file, and that is what it is
    held to: a check that called every run on record broken could not tell a
    leak from the date a run was built.
    """
    source = run / name
    if not source.is_file():
        return None
    if trim is not None and spec.layer == "valuation" and name in TRIMMED_FOR_VALUATION:
        return handed(source.read_text(encoding="utf-8", errors="replace"), trim).encode("utf-8")
    return source.read_bytes()


def _differs(placed: Path, expected) -> bool:
    """Whether a routed file is not what the run routed to it, byte for byte:
    `expected` is the bytes, or the run's own file to read them from.

    The one thing a check on names cannot see: a hardlink to another file
    resolves inside the root and answers to the right name.
    """
    if isinstance(expected, Path):
        expected = expected.read_bytes() if expected.is_file() else None
    return placed.is_file() and expected is not None and placed.read_bytes() != expected


# Every agent a run on record may hold a directory for: the live six and the
# retired four. A retired agent's directory on a pilot run is still the record
# of what that agent saw, and is judged against its layer as it was.
KNOWN_AGENTS: dict[str, Agent] = {**AGENTS, **RETIRED_AGENTS}


def recorded_root(run: Path, agent: str) -> Path:
    """Where an agent's directory belongs on a run on record, live or retired.

    `session_root` is the live pipeline's and refuses a retired name, because
    nothing builds a directory for one any more; the boundary check reads a
    run that was built when the agent was live, and holds that directory to
    the same place.
    """
    if agent not in KNOWN_AGENTS:
        raise AgentInputError(f"{agent!r} is not an agent; "
                              f"one of {', '.join(KNOWN_AGENTS)}")
    return agents_root(run) / agent


def agent_directories(run: Path) -> dict[Path, str]:
    """Every directory under `run` named for an agent, live or retired, wherever it sits.

    Found rather than assumed. A layout that groups the six by layer —
    `agents/readers/numbers-reader` beside `agents/readers/notes-text-reader` —
    holds each agent's right files and puts the other reader one step out of the
    root, and a check that looked only where it expected the directory to be
    would report that layout clean. The retired four are found too: a pilot run
    on record holds their directories, and a leak into one of those is a leak
    into what the record says that agent saw.
    """
    return {path: path.name
            for path in sorted(Path(run).rglob("*"))
            if path.name in KNOWN_AGENTS and path.is_dir()}


def input_tree_holding(path) -> Path | None:
    """The agent directory, or the directory the agents' sit in, that holds `path`.

    None when no run's input tree holds it. The boundary is those directories,
    so a writer that is not an agent -- a control, a stage runner -- asks this
    before it puts a file anywhere: a file landing in one is written into what
    the directory records an agent as having seen.

    Resolved first, because a link's ancestors are wherever it points and a
    write follows the link. An agent's directory is found by its name wherever
    it sits, the way `agent_directories` finds one. `agents` is a common word,
    so it counts only where it is this layout's: beside a run's manifest, or
    holding an agent's directory.
    """
    resolved = Path(path).resolve()
    for place in (resolved, *resolved.parents):
        if place.name in KNOWN_AGENTS:
            return place
        if place.name == AGENTS_DIRNAME and (
                (place.parent / "input_manifest.json").is_file()
                or any((place / name).is_dir() for name in KNOWN_AGENTS)):
            return place
    return None


def isolation_violations(run: Path) -> list[str]:
    """Every way an agent could reach what its layer never sees. Empty is clean.

    Six kinds, in the order they matter:

    1. an agent's directory somewhere other than its session root;
    2. a file in one that the layer never sees, or that nobody routed at all.
       The agent's own output is not one of those: a reader with `Write` and a
       session rooted here can put `report_numbers.md` in no other directory,
       so a completed run holds it and is clean;
    3. a routed name over bytes that are not the run's — the leak that wears the
       right name, and the one a check on names alone cannot see, a hardlink
       included. The valuation analyst's prose is held to the run's file cut
       down by what the manifest records under `agents.<name>.trimmed`, and to
       the full file when the manifest records no trim for that directory;
    4. something inside one that resolves outside it — a symlink or a `..` into
       the bundle, whose own ancestors are the run directory and every other
       agent's directory hanging off it;
    5. one agent's directory inside another's, the sharpest form of a readable
       sibling, because climbing out of the inner one lands in the outer;
    6. anything but an agent directory in the directory a session root sits in,
       so that one step out of a root yields no file. This is what keeps the
       roots out of the run directory itself, where the bundle is: a reader
       whose root sat beside it would have the market table one `..` away.

    Every directory named for an agent is judged, the retired four included: a
    pilot run on record holds a comparer's or a supervisor's directory, and
    that directory is held to the layer the agent had, as `RETIRED_AGENTS`
    records it, because it is the record of what the agent saw.
    """
    run = Path(run)
    live = agent_directories(run)
    found = []

    for root, name in live.items():
        spec = KNOWN_AGENTS[name]
        if root != recorded_root(run, name):
            found.append(f"{name}: its directory sits at {root}, not at its "
                         f"session root {recorded_root(run, name)}")
        trims = recorded_trim(run, name) or {}
        for path in sorted(root.iterdir()):
            if path.name == spec.writes:
                continue  # the one file this agent writes, into its only root
            if path.name not in spec.sees:
                reason = ("which its layer never sees"
                          if path.name in spec.never_sees else "which nobody routed")
                found.append(f"{name}: holds {path.name}, {reason}")
                continue
            try:
                expected = expected_bytes(run, spec, path.name, trims.get(path.name))
            except AgentInputError as exc:
                found.append(f"{name}: {path.name}: {exc}")
                continue
            if _differs(path, expected):
                found.append(f"{name}: holds a {path.name} that is not the "
                             "run's — the right name over other bytes")
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
                        help="one agent; the default is every one")
    parser.add_argument("--light", action="store_true",
                        help="an 8-K 2.02 light run: the two readers")
    args = parser.parse_args(argv)

    if args.agent and args.light:
        print("agent_inputs: --agent and --light name different sets; pick one",
              file=sys.stderr)
        return BAD_INPUT
    chosen = (args.agent,) if args.agent else (LIGHT_RUN if args.light else None)
    run = Path(args.run)
    try:
        built = build_all(run, chosen, light=args.light)
    except (AgentInputError, OSError) as exc:
        print(f"agent_inputs: {exc}", file=sys.stderr)
        return BAD_INPUT

    broken = isolation_violations(run)
    for record in built:
        # "absent", not "not built yet": a file no builder writes yet is
        # recorded as missing from this run, not as late.
        absent = f", {len(record['absent'])} absent" if record["absent"] else ""
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
