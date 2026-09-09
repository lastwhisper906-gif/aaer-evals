"""One agent doing the whole job alone, so the scorecard can say what the layers add.

`docs/CHECKLIST.md` §8 names this row and what it falsifies: "**single-agent
baseline** -- one call per question, the same model as the supervisor, handed
the whole bundle plus the market table, answering the same schema. If the layers
do not beat it, the structure is decoration, and the scorecard says so in those
words." It is scored beside `pipeline_accounting` and `pipeline_pressure` and
**never merged into either** -- `docs/HOW_WE_WORK.md` §3, the `controls` stage:
"every baseline computed, both controls wrote their files, none merged into the
pipeline's number."

**The model is read off the supervisor's own prompt, not restated here.**
`docs/HOW_WE_WORK.md` §6: "a control on a different model would measure the
model, not the structure". `supervisor_model()` reads the `model:` line of
`.claude/agents/supervisor-accounting.md` and `.claude/agents/supervisor-pressure.md`
and refuses if the two disagree, so the control cannot drift off the supervisor
by a copy nobody updated. The prompt, by the same paragraph, "lives inside the
control's run script, not in `.claude/agents/` -- it is a control, not a layer,
and it must not become something a session can invoke by name", so it is
`CONTROL_PROMPT` below, a committed constant with the question and the file list
interpolated into it.

**What it sees is an allowlist.** The `input_` files of the catalogue, and
nothing else at all. A control that read `report_numbers.md` would be the
supervisor with extra steps, measuring the pipeline rather than standing beside
it; and a file nobody routed is worse, because nobody decided it -- a price file
carrying the outcome window, another company's notes, whatever a broken stage
left in the directory. `src/agent_inputs.py` refuses a name outside the
catalogue for that reason and says it in those words: "a name outside this set
inside a session root is a file nobody decided to route, and an undecided file
in an agent's directory is a leak nobody chose either." So the guard names what
may be there rather than what may not, and every other name is refused before
the call is made, whether the pipeline wrote it or nothing in this repository
did. The prompt tells the model it sees these files and nothing else, and the
allowlist is what makes that sentence true. That directory is not one
`src/agent_inputs.py` builds: that file builds the six layer directories and
its `agents/` holds nothing else, and a seventh is the stage runner's to place.
The shape is named here rather than minted there.

**The cutoff is read and honoured, not carried past.** `CLAUDE.md`: "Cutoff:
document filing date <= filing date of the triggering report. Nothing later
enters the input." This control does not assemble the bundle, so the boundary it
can check is the run's own record of one: `input_manifest.json` names the cutoff
and the filing date of the report that triggered the run, and
`src/extraction_checks.py`'s `check_cutoff` settles what the two have to say --
"the cutoff is the triggering report's own filing date". A manifest naming no
cutoff, an unparseable one, or one that is not that filing date is refused
before the model is called: a control run against a boundary nobody recorded is
scored on an input that may hold the outcome it is predicting, and that is not a
baseline, it is a leak with a number on it. The cutoff it ran under goes back
with the drop rows, for the runner to record.

**Evidence carries a quote, and here is why.** `CLAUDE.md`: "Every report item
carries a verbatim quote or an upstream item id that Python verifies." A
supervisor's `evidence[].upstream_item_id` names an item of one of the four
reports. This control has no upstream report -- its upstream is the committed
input itself -- so the id it can write names a *paragraph*, not an item, and an
id that names a paragraph is verified by quoting it. The quote branch is the
only branch available, which is why `EVIDENCE_FIELDS` carries `quote` beside the
`upstream_item_id` `docs/CHECKLIST.md` §7 shows. `src/quote_gate.py` does every
piece of the verifying: `quotable` builds the index of what the committed input
declares, `quote_drop_reason` matches one quote against it, and
`citation_drop_reason` resolves the ids. None of it is reimplemented here.

**`market_direction.basis` is a bare list of ids**, because §7 gives it that
shape and there is nowhere in it to put a quote. So existence in the committed
input is the whole of what Python can check there, through the gate's citation
path. An `"insufficient"` `p_up` may rest on an empty basis and that is the one
case nothing is resolved: §7 makes `"insufficient"` an allowed value "and that
is recorded and counted", and a probability resting on nothing is exactly what
it is for. A basis with ids in it is resolved whatever `p_up` says, because the
supervisors' own rule -- "Python checks that each one resolves, and an
unresolvable one is dropped and counted" -- does not go quiet when the
probability abstains.

**An `explanations` entry is the identical shape.** §7 gives it an `id`, a
`support` and a `realization_p`, and no more room for a quote than the basis
has, so its id is resolved the same way and by the same call: existence in the
committed input, through the gate's citation path. The build order in
`docs/HOW_WE_WORK.md` finishes the controls at "both control files, with every
citation resolving", and an id naming another company's accession and a
paragraph that exists nowhere is a citation that does not resolve. An entry
written into the control file unresolved would be an anchor the model was free
to invent, scored as if it had been checked.

**What a drop does.** A checklist entry whose evidence does not verify is
dropped whole, because that is what the gate does with an item -- one failing
citation drops the item, not the citation. A `market_direction` whose basis does
not resolve cannot be dropped, since §7 requires the field, so it degrades to
`"insufficient"` with an empty basis and the drop is counted: the schema's own
abstention, which the scorecard counts against the control, rather than a
probability standing on an id that resolves to nothing. A `top_signals` entry
naming a checklist key that went with a dropped entry goes with it. An
`explanations` entry goes whole like a checklist entry -- there is nothing else
in it to keep, and §7 does not require the list to hold anything, so there is
nothing to degrade to either.

**The drop rows and the served model are returned, not written.**
`docs/INPUT_SPEC.md` §6 gives `input_manifest.json` the dropped-item counts and
`docs/HOW_WE_WORK.md` §6 gives it the requested pin and the served model, but
`src/quote_gate.py`'s writer replaces `dropped_items` wholesale and this control
runs at `controls`, after the three layers have already put theirs there.
Writing from here would erase the run's own drop record. There is no stage
runner yet -- the same gap `src/quote_gate.py` names, "nothing calls `gate` yet
because there is no stage runner to call it" -- and the runner that calls this
holds both and records them.

This module never names `runs/`. It writes into the directory it is handed, and
it never writes over what is already there: a run directory is append-only, so a
second call carrying different content is refused and a correction is a new run.

    python3.12 -m src.control_single_agent --question accounting_reliability --input <dir>

prints the exact call the control would make. There is no model client in this
repository, so the command line prints the prompt rather than sending it; `run`
takes the caller's `ask` and makes the one call. Exit 0 clean, 2 the input
cannot be read, 3 the wrong interpreter.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from collections import Counter
from pathlib import Path

try:
    from src import agent_inputs, cutoff_guard, interpreter_pin, quote_gate
except ImportError:  # invoked as a plain script
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import agent_inputs, cutoff_guard, interpreter_pin, quote_gate

REPO_ROOT = Path(__file__).resolve().parent.parent
AGENT_PROMPTS = REPO_ROOT / ".claude" / "agents"

MANIFEST = "input_manifest.json"
INDENT = 2
BAD_INPUT = 2

# One file per question, as `docs/INPUT_SPEC.md` §6 names them.
CONTROL_FILES = {
    "accounting_reliability": "control_single_agent_accounting.json",
    "financial_pressure": "control_single_agent_pressure.json",
}

# What the control may be handed, by name: the catalogue's `input_` files and
# nothing else. Read off `src/agent_inputs.py`'s catalogue rather than listed
# again here, so a name routed there is routed here on the same day.
INPUT_PREFIX = "input_"
CONTROL_SEES = tuple(name for name in agent_inputs.BUNDLE_CATALOGUE
                     if name.startswith(INPUT_PREFIX))

# The two supervisors whose model this control borrows. Both, not one per
# question: they run under one pin and this refuses if they ever disagree.
# `docs/HOW_WE_WORK.md` §6.
SUPERVISOR_PROMPTS = ("supervisor-accounting.md", "supervisor-pressure.md")

# The output schema, copied out of `docs/CHECKLIST.md` §7 character for
# character so the prompt shows the model the document's own shape.
# `tests/test_control_single_agent.py` asserts it is still a slice of that file.
SCHEMA = '''{ "question": "accounting_reliability" | "financial_pressure",
  "rules_version": "0.1",
  "checklist": [ {"key": "", "finding": "", "confidence": 0,
                  "evidence": [{"upstream_item_id": ""}]} ],
  "continuous": [ {"key": "", "point": 0, "direction": "", "low": 0, "high": 0} ],
  "events": [ {"key": "", "p_within_horizon": 0} ],
  "explanations": [ {"id": "", "support": "sufficient|insufficient|unknown",
                     "realization_p": 0} ],
  "market_direction": {"p_up": 0, "basis": []},
  "tier": "elevated" | "watch" | "clear",
  "top_signals": [] }'''

# Every field of that schema, by the name it carries there. `continuous` is not
# in this list because it belongs to one question only.
FIELDS = ("question", "rules_version", "checklist", "events", "explanations",
          "market_direction", "tier", "top_signals")
CONTINUOUS = "continuous"
CHECKLIST_FIELDS = ("key", "finding", "confidence", "evidence")
CONTINUOUS_FIELDS = ("key", "point", "direction", "low", "high")
EVENT_FIELDS = ("key", "p_within_horizon")
EXPLANATION_FIELDS = ("id", "support", "realization_p")
MARKET_FIELDS = ("p_up", "basis")
# `upstream_item_id` is §7's; `quote` is the branch of `CLAUDE.md`'s rule that
# an agent with no upstream report has left. The docstring says why.
# Nothing ties this tuple to `docs/CHECKLIST.md` §7: it and the list in
# `tests/test_control_single_agent.py` were written by the same hand, so they
# agree with each other and would go on agreeing if §7 moved.
EVIDENCE_FIELDS = ("upstream_item_id", "quote")

# `docs/CHECKLIST.md` §1: "An LLM answer is always `flag` / `no_flag` /
# `insufficient`, plus a confidence and a verbatim quote with its paragraph id."
FINDINGS = ("flag", "no_flag", "insufficient")
SUPPORT = ("sufficient", "insufficient", "unknown")
TIERS = ("elevated", "watch", "clear")
INSUFFICIENT = "insufficient"
TOP_SIGNALS_MAX = 5

CONTROL_PROMPT = """You are the single-agent baseline control, and you do the
whole job alone: you read the filing bundle, you put it beside the market table,
and you answer one question. Nobody reads your output but the scorer. It is
scored beside the three-layer pipeline and never merged into it.

You answer one question: **{question}**. The other question is not yours,
and the two are never merged.

You see these files and nothing else:

{files}

Text is verbatim. You never summarize a filing into your own words, and every
finding you record is anchored to a paragraph you quote.

Write one JSON document against this schema, and nothing else:

{schema}

`continuous` is financial pressure only.
`top_signals` holds at most five keys, and every one of them is the `key` of one
of your own checklist entries.
`tier` is `clear` when nothing is wrong. Say `clear` when things are clear, and
never soften an adverse read or manufacture one.
`market_direction.p_up` is the probability that the 60-trading-day abnormal
return is positive, read through this question only. `"insufficient"` is an
allowed value; use it when you mean it, and do not use it to avoid being scored.

Every entry of `evidence` carries two members: `upstream_item_id`, the paragraph
id of the file you read it in, and `quote`, that paragraph's own text, verbatim.
Python string-matches the quote against the file you were handed, character for
character -- not a dash, not a quotation mark, not a run of whitespace is
normalized -- and a checklist entry whose evidence does not match is dropped
whole and counted. Every id in `market_direction.basis` is a paragraph id of
those same files.
"""


class ControlError(Exception):
    """The control cannot be run, or its answer cannot be recorded as one."""


def _a_question(question: str) -> None:
    """One of the two questions there are, or a refusal."""
    if question not in CONTROL_FILES:
        raise ControlError(f"{question!r} is not a question; "
                           f"one of {', '.join(CONTROL_FILES)}")


# --- the model, borrowed from the supervisor ---------------------------------

def _front_matter_model(path: Path) -> str:
    """The `model:` line of an agent prompt's front matter."""
    lines = path.read_text(encoding="utf-8").split("\n")
    if not lines or lines[0].strip() != "---":
        raise ControlError(f"{path.name} opens with no front matter, so it names no model")
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if line.startswith("model:"):
            found = line.split(":", 1)[1].strip()
            if found:
                return found
    raise ControlError(f"{path.name} front matter carries no model line")


def supervisor_model(prompts_dir: Path = AGENT_PROMPTS) -> str:
    """The model family both supervisors name, or a refusal.

    Read rather than restated: a control on a different model would measure the
    model and not the structure, and a constant here would be a copy of the
    supervisor's pin that nobody updates. The two supervisors run the same
    question under the same pin; if they ever disagree there is no single
    "the same model as the supervisor" to borrow, and this refuses instead of
    picking one.
    """
    found = {name: _front_matter_model(Path(prompts_dir) / name)
             for name in SUPERVISOR_PROMPTS}
    families = set(found.values())
    if len(families) != 1:
        named = ", ".join(f"{name} names {model}" for name, model in sorted(found.items()))
        raise ControlError(
            f"the supervisors name different models ({named}) — there is no one "
            "model the control can borrow, and choosing one would be this "
            "module deciding the pin")
    return families.pop()


def served_names_family(served: str, family: str) -> bool:
    """Whether a served model is one of the family the run asked for.

    `docs/HOW_WE_WORK.md` §6: an agent file "names a family, not a pin", and the
    dated model id lives in the rules version. `rules/v0.1` does not exist, so
    the family is the whole of the pin there is today and naming it is all this
    can ask. The day the rules version carries a dated id this tightens to
    equality against that id.
    """
    return isinstance(served, str) and family.lower() in served.lower()


# --- the schema, field by field ----------------------------------------------

def _fields(entry, expected: tuple[str, ...], where: str) -> None:
    if not isinstance(entry, dict):
        raise ControlError(f"{where} is {type(entry).__name__}, not an object")
    found = tuple(sorted(entry))
    if found != tuple(sorted(expected)):
        raise ControlError(
            f"{where} carries {', '.join(found) or 'no fields'} and the schema "
            f"gives it {', '.join(sorted(expected))}")


def _text(entry, field: str, where: str) -> str:
    value = entry.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ControlError(f"{where}.{field} is {value!r}, and the schema gives it a name")
    return value


def _one_of(entry, field: str, allowed: tuple[str, ...], where: str) -> str:
    value = entry.get(field)
    if value not in allowed:
        raise ControlError(
            f"{where}.{field} is {value!r}; the schema allows {', '.join(allowed)}")
    return value


def _number(entry, field: str, where: str, *, low=None, high=None) -> float:
    value = entry.get(field)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ControlError(f"{where}.{field} is {value!r}, and the schema gives it a number")
    if low is not None and not low <= value <= high:
        raise ControlError(
            f"{where}.{field} is {value}, outside {low} to {high} — a probability "
            "outside its own range is not a probability")
    return float(value)


def _unique(keys: list[str], where: str) -> None:
    """One indicator, one key — `docs/CHECKLIST.md` §2 says it in those words."""
    repeated = [key for key, count in Counter(keys).items() if count > 1]
    if repeated:
        raise ControlError(
            f"{where} names {', '.join(sorted(repeated))} more than once; one "
            "indicator, one key, and a repeated key names a set")


def check_schema(payload, question: str, *, rules_version) -> dict:
    """The payload against `docs/CHECKLIST.md` §7, field by field, or a refusal.

    `rules_version` is the run's own, out of `input_manifest.json`. The model
    does not get to invent it: a prediction scored against a rules version it
    named itself is scored against nothing.
    """
    _a_question(question)
    if not isinstance(payload, dict):
        raise ControlError(
            f"the prediction is {type(payload).__name__}, not an object")
    # Before the field set, because `continuous` belongs to one question and an
    # answer to the wrong question would be reported as a stray field.
    if payload.get("question") != question:
        raise ControlError(
            f"the prediction answers {payload.get('question')!r} and was asked "
            f"{question!r}; the two questions are never merged")
    expected = FIELDS + ((CONTINUOUS,) if question == "financial_pressure" else ())
    _fields(payload, expected, "the prediction")

    if payload["rules_version"] != rules_version:
        raise ControlError(
            f"the prediction carries rules_version {payload['rules_version']!r} "
            f"and this run's is {rules_version!r} — each prediction is scored "
            "against its own rules version, and that version is the run's")

    checklist = payload["checklist"]
    if not isinstance(checklist, list):
        raise ControlError("checklist is not a list")
    for position, entry in enumerate(checklist, start=1):
        where = f"checklist[{position}]"
        _fields(entry, CHECKLIST_FIELDS, where)
        _text(entry, "key", where)
        _one_of(entry, "finding", FINDINGS, where)
        _number(entry, "confidence", where, low=0, high=1)
        evidence = entry["evidence"]
        if not isinstance(evidence, list):
            raise ControlError(f"{where}.evidence is not a list")
        for index, cited in enumerate(evidence, start=1):
            cited_where = f"{where}.evidence[{index}]"
            _fields(cited, EVIDENCE_FIELDS, cited_where)
            for field in EVIDENCE_FIELDS:
                _text(cited, field, cited_where)
    _unique([entry["key"] for entry in checklist], "checklist")

    if question == "financial_pressure":
        continuous = payload[CONTINUOUS]
        if not isinstance(continuous, list) or not continuous:
            raise ControlError(
                "continuous is empty; financial pressure predicts next quarter's "
                "revenue growth, operating margin and operating cash flow")
        for position, entry in enumerate(continuous, start=1):
            where = f"continuous[{position}]"
            _fields(entry, CONTINUOUS_FIELDS, where)
            _text(entry, "key", where)
            # §7 gives `direction` a string and does not enumerate its values.
            _text(entry, "direction", where)
            point = _number(entry, "point", where)
            low = _number(entry, "low", where)
            high = _number(entry, "high", where)
            if not low <= point <= high:
                raise ControlError(
                    f"{where} puts its point {point} outside its own range "
                    f"{low} to {high}")
        _unique([entry["key"] for entry in continuous], "continuous")

    events = payload["events"]
    if not isinstance(events, list):
        raise ControlError("events is not a list")
    for position, entry in enumerate(events, start=1):
        where = f"events[{position}]"
        _fields(entry, EVENT_FIELDS, where)
        _text(entry, "key", where)
        _number(entry, "p_within_horizon", where, low=0, high=1)
    _unique([entry["key"] for entry in events], "events")

    explanations = payload["explanations"]
    if not isinstance(explanations, list):
        raise ControlError("explanations is not a list")
    for position, entry in enumerate(explanations, start=1):
        where = f"explanations[{position}]"
        _fields(entry, EXPLANATION_FIELDS, where)
        _text(entry, "id", where)
        _one_of(entry, "support", SUPPORT, where)
        _number(entry, "realization_p", where, low=0, high=1)
    _unique([entry["id"] for entry in explanations], "explanations")

    market = payload["market_direction"]
    _fields(market, MARKET_FIELDS, "market_direction")
    if market["p_up"] != INSUFFICIENT:
        _number(market, "p_up", "market_direction", low=0, high=1)
    basis = market["basis"]
    if not isinstance(basis, list) or not all(
            isinstance(one, str) and one.strip() for one in basis):
        raise ControlError("market_direction.basis is not a list of paragraph ids")

    _one_of(payload, "tier", TIERS, "the prediction")

    signals = payload["top_signals"]
    if not isinstance(signals, list) or not all(isinstance(one, str) for one in signals):
        raise ControlError("top_signals is not a list of keys")
    if len(signals) > TOP_SIGNALS_MAX:
        raise ControlError(
            f"top_signals holds {len(signals)} keys and the schema allows "
            f"at most {TOP_SIGNALS_MAX}")
    _unique(signals, "top_signals")
    keys = {entry["key"] for entry in checklist}
    unknown = [one for one in signals if one not in keys]
    if unknown:
        raise ControlError(
            f"top_signals names {', '.join(unknown)}, which no checklist entry "
            "carries — a top signal that names no entry names nothing")
    return payload


# --- the gate, over the control's own output ---------------------------------

def checklist_gate_id(question: str, key: str) -> str:
    """The handle the gate holds one checklist entry by.

    The prediction file carries no per-entry id -- `docs/CHECKLIST.md` §7 gives
    a checklist entry a `key` and no `id` -- so this is minted for the gate and
    for the drop row, and it is not written into the file. The question is in
    it because the two control files are gated in the same run and an item id
    repeated anywhere in a run resolves for nobody.
    """
    return f"{question}:checklist:{key}"


def market_gate_id(question: str) -> str:
    """The handle the gate holds `market_direction` by."""
    return f"{question}:market_direction"


def explanation_gate_id(question: str, identifier: str) -> str:
    """The handle the gate holds one `explanations` entry by.

    The entry's own `id` is the citation, not the handle: it names a paragraph
    of the committed input the way `market_direction.basis` does. The handle is
    minted here for the drop row, exactly as a checklist entry's is, and it is
    not written into the file.
    """
    return f"{question}:explanations:{identifier}"


def _first_bad_quote(identifier: str, evidence: list, index: dict) -> str | None:
    """The first of an entry's quotes that does not match, by the gate's reading."""
    for cited in evidence:
        why = quote_gate.quote_drop_reason(
            {"id": identifier, "paragraph_id": cited["upstream_item_id"],
             "quote": cited["quote"]}, index)
        if why is not None:
            return why
    return None


def drop_reasons(payload: dict, question: str, index: dict) -> dict[str, str]:
    """Why each part of this prediction is dropped, keyed by its gate id.

    Both halves are `src/quote_gate.py`'s. `citation_drop_reason` resolves the
    ids against what the committed input declares -- for this control the
    committed input *is* the upstream, so the id set it resolves against is the
    index's own -- and catches an entry citing nothing at all.
    `quote_drop_reason` then string-matches each quote against the paragraph it
    names. An `explanations` entry and `market_direction` have no quote to
    match, so for those the citation path is the whole of it.
    """
    declared = set(index)
    found: dict[str, str] = {}
    for entry in payload["checklist"]:
        identifier = checklist_gate_id(question, entry["key"])
        why = quote_gate.citation_drop_reason(
            {"id": identifier, "evidence": entry["evidence"]}, declared)
        if why is None:
            why = _first_bad_quote(identifier, entry["evidence"], index)
        if why is not None:
            found[identifier] = why

    for entry in payload["explanations"]:
        identifier = explanation_gate_id(question, entry["id"])
        why = quote_gate.citation_drop_reason(
            {"id": identifier, "upstream_item_id": entry["id"]}, declared)
        if why is not None:
            found[identifier] = why

    market = payload["market_direction"]
    # The abstention rests on nothing by design, so an `"insufficient"` p_up with
    # an empty basis is the one thing here that resolves nothing. Anything the
    # basis does name is resolved, whatever p_up says.
    if market["p_up"] != INSUFFICIENT or market["basis"]:
        market_id = market_gate_id(question)
        why = quote_gate.citation_drop_reason(
            {"id": market_id, "basis": market["basis"]}, declared)
        if why is not None:
            found[market_id] = why
    return found


def verify(payload: dict, question: str, input_dir, accession: str) -> tuple[dict, list[dict]]:
    """The prediction with what did not verify taken out, and one row per drop.

    Runs after `check_schema`, which is what makes one checklist key one entry:
    two entries under one key would be two items under one gate id, and an id
    that names a set resolves for nobody.

    A checklist entry goes whole, because that is what the gate does with an
    item, and an `explanations` entry goes the same way. `market_direction`
    cannot go -- §7 requires the field -- so it degrades to the abstention §7
    already allows, `"insufficient"` with an empty basis, and the drop is
    counted like any other. A `top_signals` entry naming
    a key that left goes with it.
    """
    index = quote_gate.quotable(input_dir, accession)
    reasons = drop_reasons(payload, question, index)
    kept = dict(payload)
    kept["checklist"] = [entry for entry in payload["checklist"]
                         if checklist_gate_id(question, entry["key"]) not in reasons]
    kept["explanations"] = [
        entry for entry in payload["explanations"]
        if explanation_gate_id(question, entry["id"]) not in reasons]
    standing = {entry["key"] for entry in kept["checklist"]}
    kept["top_signals"] = [one for one in payload["top_signals"] if one in standing]
    if market_gate_id(question) in reasons:
        kept["market_direction"] = {"p_up": INSUFFICIENT, "basis": []}
    dropped = [{"report": CONTROL_FILES[question], "item_id": identifier,
                "reason": reason} for identifier, reason in sorted(reasons.items())]
    return kept, dropped


# --- the call ----------------------------------------------------------------

def input_files(input_dir) -> list[str]:
    """What the control was handed, or a refusal naming what it may not hold.

    `docs/CHECKLIST.md` §8 hands this control "the whole bundle plus the market
    table", and `CONTROL_SEES` is that bundle by name. The guard is an
    allowlist, not a list of the pipeline's own files: a report or a prediction
    would make this a reader of the pipeline rather than a control beside it,
    and a name in neither list is a file nobody decided to route, which is the
    worse of the two because nobody weighed it at all.
    """
    names = cutoff_guard.bundle_files(input_dir, "*")
    if not names:
        raise ControlError(
            f"{input_dir} holds no files — a control with no input is not a control")
    stray = [name for name in names if name not in CONTROL_SEES]
    if stray:
        raise ControlError(
            f"{input_dir} holds {', '.join(stray)}, which this control is not "
            f"handed. It sees the {len(CONTROL_SEES)} input files of the bundle "
            "and nothing else: the pipeline's own output would make it a reader "
            "of the pipeline, and a file nobody routed is a leak nobody chose")
    return names


def prompt(question: str, input_dir) -> str:
    """The one prompt this control sends, with the question and its files in it."""
    _a_question(question)
    listed = "\n".join(f"- {name}" for name in input_files(input_dir))
    return CONTROL_PROMPT.format(question=question.replace("_", " "),
                                 files=listed, schema=SCHEMA)


def _place(path: Path, text: str) -> Path:
    """The control file where it was asked for, without changing what is there.

    `CLAUDE.md`: existing content under `runs/` "is never changed or deleted".
    A control called twice over one run would otherwise write over a published
    prediction, so a second call carrying different content is refused and a
    correction is a new run. The symlink is tested before `exists()`, because
    both it and `write_text` follow a link and a link would put the file
    somewhere this was never handed -- `src/agent_inputs.py` refuses one for the
    same reason.
    """
    if path.is_symlink():
        raise ControlError(
            f"{path} is a symlink to {path.readlink()}. A control's file is "
            "written where it was handed, never through a link out of it")
    if path.exists() and path.read_text(encoding="utf-8") != text:
        raise ControlError(
            f"{path} is already there saying something else. A run directory is "
            "append-only: existing content is never changed, and a correction is "
            "a new run rather than a second call over the first")
    path.write_text(text, encoding="utf-8")
    return path


def run_cutoff(manifest: dict) -> dt.date:
    """The boundary this run was assembled under, or a refusal.

    Fail-closed on both keys and on their disagreement.
    `src/extraction_checks.py` settles what a bundle's own record has to say --
    "the cutoff is the triggering report's own filing date" -- and a manifest
    naming one key without the other, or a cutoff years off the filing, is a run
    whose boundary nobody can read. The control refuses it rather than answering
    against an input that may already hold the outcome.
    """
    try:
        cutoff = cutoff_guard.parse_date(manifest.get("cutoff"), f"{MANIFEST} cutoff")
        filed = cutoff_guard.parse_date(manifest.get("filing_date"),
                                        f"{MANIFEST} filing_date")
    except cutoff_guard.CutoffGuardError as exc:
        raise ControlError(
            f"{exc} — the control is handed a directory and not a boundary, so "
            "the run's own record of its cutoff is the whole of what it can "
            "check, and an unreadable one is refused") from exc
    if cutoff != filed:
        raise ControlError(
            f"{MANIFEST} names the cutoff {cutoff} and the triggering report's "
            f"filing date {filed}. The cutoff is that filing date; a run whose "
            "own record disagrees was assembled against a boundary nobody set")
    return cutoff


def run(question: str, *, input_dir, bundle_root, ask,
        prompts_dir: Path = AGENT_PROMPTS) -> dict:
    """One call, gated, and the control file on disk.

    `ask(prompt, model=...)` is the caller's one model call. It returns
    `{"served_model": ..., "text": ...}`: the model that actually answered, and
    its answer as characters. There is no model client in this repository, so
    the call belongs to whoever runs the stage; what belongs here is the prompt,
    the pin, the schema and the gate.

    Returns the payload as written, the file it was written to, the cutoff it
    ran under, the requested and served model, and one row per drop --
    `docs/INPUT_SPEC.md` §6 puts the drop count and the served model in
    `input_manifest.json` and the module
    docstring says why this hands them back rather than writing them there.
    """
    family = supervisor_model(prompts_dir)
    manifest = json.loads(cutoff_guard.load_bundle_file(bundle_root, MANIFEST))
    accession = manifest.get("accession")
    if not isinstance(accession, str) or not accession:
        raise ControlError(
            f"{MANIFEST} names no accession, and a computed row's id begins with one")
    cutoff = run_cutoff(manifest)

    answer = ask(prompt(question, input_dir), model=family)
    served = answer.get("served_model") if isinstance(answer, dict) else None
    if not served_names_family(served, family):
        raise ControlError(
            f"the control asked for {family} and {served!r} answered. A run whose "
            "served model differs from the pin is recorded as a failure, and a "
            "control on another model measures the model and not the structure")
    try:
        payload = json.loads(answer["text"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ControlError(f"the control's answer is not JSON: {exc}") from exc

    check_schema(payload, question, rules_version=manifest.get("rules_version"))
    kept, dropped = verify(payload, question, input_dir, accession)
    path = _place(Path(bundle_root) / CONTROL_FILES[question],
                  json.dumps(kept, indent=INDENT, sort_keys=True) + "\n")
    return {"question": question, "path": path, "prediction": kept,
            "dropped": dropped, "cutoff": str(cutoff),
            "requested_model": family, "served_model": served}


def main(argv=None) -> int:
    code = interpreter_pin.enforce()
    if code:
        return code
    parser = argparse.ArgumentParser(
        description="Print the single-agent control's one call for one question.")
    parser.add_argument("--question", required=True, choices=sorted(CONTROL_FILES))
    parser.add_argument("--input", required=True,
                        help="the directory the control is handed")
    parser.add_argument("--prompts", default=str(AGENT_PROMPTS),
                        help="where the supervisor prompts are, for the model pin")
    args = parser.parse_args(argv)
    try:
        model = supervisor_model(Path(args.prompts))
        text = prompt(args.question, args.input)
    except (ControlError, OSError) as exc:
        print(exc, file=sys.stderr)
        return BAD_INPUT
    print(f"model: {model}")
    print(f"writes: {CONTROL_FILES[args.question]}")
    print()
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
