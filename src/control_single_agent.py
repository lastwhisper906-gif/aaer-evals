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

**What it sees, and nothing else.** `CONTROL_SEES` is `docs/CHECKLIST.md` §8's
"the whole bundle plus the market table" as names, taken off
`src/agent_inputs.py`'s catalogue so §6 moves it. It is an **allowlist**: a name
outside it is refused, whatever it is. The first version was the other way
round -- it refused the catalogue names the pipeline wrote and let everything
else through -- so a report was caught and a price file carrying the outcome
window was not, and neither was another company's notes under a name nobody had
thought of. Both were then listed to the model under "you see these files and
nothing else", which is the sentence the directory has to make true.
`src/agent_inputs.py` refuses anything outside what a layer may hold for that
reason, and this is the same rule at the control's own directory -- read off
every entry there, because a name is checked against the allowlist but a symlink
carrying an allowed name carries another run's bytes and a directory carrying one
carries whatever is under it under no name at all. That directory
is not one `src/agent_inputs.py` builds: that file builds the six layer
directories and its `agents/` holds nothing else, and a seventh is the stage
runner's to place. The shape is named here rather than minted there.

**A name is not the whole of it.** Two of the allowlist's names carry more than
a name can say, and both are checked. `input_prior_predictions.md` is refused
when it still carries a probability, through `src/agent_inputs.py`'s own reader
-- §6 gives that file "prior flags and outcomes, probabilities removed", and
`docs/HOW_WE_WORK.md` §8 forbids putting a prior run's probability into any
agent's input. And any allowed name can hold another company's prose, so
`resolvable` refuses a directory declaring paragraphs of an accession the record
does not give this ticker by the cutoff; without it, NVDA's paragraphs in a file
called `input_notes.md` would have made every NVDA id the model wrote resolve,
gate clean and land in this company's control file.

Under all of it is the one check a name cannot stand in for: every file the
directory holds is held against the run's own file of that name, byte for byte,
through `src/agent_inputs.py`'s `_differs` -- "a hardlink to another file
resolves inside the root and answers to the right name". Two of the allowlist's
names declare no paragraph ids at all, `input_market.json` and
`input_companyfacts.json`, so nothing downstream can tell whose they are; and a
foreign `input_trends.json` is worse than invisible, because `src/quote_gate.py`
mints its cell ids from *this* run's accession rather than out of the file, so
another company's values string-match as verbatim quotes under this run's own
ids. `input_manifest.json` is not
on the allowlist at all: §6's line for it is "dropped-item counts ... served
models", which is the pipeline's own output, and `run` reads it from
`bundle_root` where the run keeps it rather than from what the control sees.

**The cutoff is bound here.** `cutoff_on_record` holds the bundle's `cutoff`
against the date EDGAR recorded for the accession the bundle itself names, and
`run` calls it before the model call rather than after. Nothing in this module
read the key at all before: a bundle carrying a cutoff of 1999, or carrying none,
was answered, gated and written out. `src/extraction_checks.py` carries the same
rule over a whole manifest and nothing in `src/`, the Makefile or CI calls it, so
there was no gate ordered ahead of this one either.

**Evidence carries a quote, and here is why.** `CLAUDE.md`: "Every report item
carries a verbatim quote or an upstream item id that Python verifies." A
supervisor's `evidence[].upstream_item_id` names an item of one of the four
reports. This control has no upstream report -- its upstream is the committed
input itself -- so the id it can write names a *paragraph*, not an item, and an
id that names a paragraph is verified by quoting it. The quote branch is the
only branch available, which is why `EVIDENCE_FIELDS` carries `quote` beside the
`upstream_item_id` `docs/CHECKLIST.md` §7 shows -- and it is the *only* thing
that tuple adds: the rest is `src/prediction_schema.py`'s own `EVIDENCE_FIELDS`.

**The schema is checked by the one function both controls call.**
`src/prediction_schema.py` holds §7's field lists, its three findings and support
words and the anomaly register's closed lists, once, and `check_schema` hands it
every field the model answers with this control's evidence shape as the
argument. What
stays here is the two fields that are the run's: the question this control
asked, and the rules version out of the run's manifest.

`src/quote_gate.py` does every piece of the
verifying: `quotable` builds the index of what the committed input declares,
`quote_drop_reason` matches one quote against it, and `citation_drop_reason`
resolves the ids -- the `evidence` ids, `market_direction.basis`, and an
explanation's own `id`, which `explanation_gate_id` reads the same way and which
nothing here resolved at all until `docs/HOW_WE_WORK.md` §7, step 6 was held
against it: the controls are done when a fixture filing produces both control
files "with every citation resolving". None of it is reimplemented here.

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

**What a drop does.** A checklist entry whose evidence does not verify is
dropped whole, because that is what the gate does with an item -- one failing
citation drops the item, not the citation -- and an anomaly in the register is
gated and dropped the same way, under its name. An explanation whose id
resolves to nothing goes the same way: §7 requires the field and not a row in
it, so the entry leaves the list and the drop is counted. A `market_direction`
whose basis does not resolve cannot be dropped, since §7 requires the field, so
it degrades to `"insufficient"` with an empty basis and the drop is counted: the
schema's own abstention, which the scorecard counts against the control, rather
than a probability standing on an id that resolves to nothing.

**The drop rows and the served model are returned, not written.**
`docs/INPUT_SPEC.md` §6 gives `input_manifest.json` the dropped-item counts and
`docs/HOW_WE_WORK.md` §6 gives it the requested pin and the served model, but
`src/quote_gate.py`'s writer replaces `dropped_items` wholesale and this control
runs at `controls`, after the three layers have already put theirs there.
Writing from here would erase the run's own drop record. There is no stage
runner yet -- the same gap `src/quote_gate.py` names, "nothing calls `gate` yet
because there is no stage runner to call it" -- and the runner that calls this
holds both and records them.

This module never names `runs/`. It writes into the run directory it is handed,
which is where `docs/INPUT_SPEC.md` §6 lists the control files, and nowhere
inside a run's per-agent input tree: `destination` refuses a run directory
sitting in one, because that tree is committed as what each agent saw. It never
writes over what is already there: a run directory is append-only, so a second
call carrying different content is refused and a correction is a new run.

    python3.12 -m src.control_single_agent --question accounting_reliability \
        --input <the control's directory> --bundle <the run directory>

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
from pathlib import Path

try:
    from src import (agent_inputs, cutoff_guard, interpreter_pin,
                     prediction_schema, quote_gate)
except ImportError:  # invoked as a plain script
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import (agent_inputs, cutoff_guard, interpreter_pin,
                     prediction_schema, quote_gate)

REPO_ROOT = Path(__file__).resolve().parent.parent
AGENT_PROMPTS = REPO_ROOT / ".claude" / "agents"

MANIFEST = "input_manifest.json"
PRIOR_PREDICTIONS = "input_prior_predictions.md"
INDENT = 2
BAD_INPUT = 2


class ControlError(Exception):
    """The control cannot be run, or its answer cannot be recorded as one."""


# One file per question, as `docs/INPUT_SPEC.md` §6 names them.
CONTROL_FILES = {
    "accounting_reliability": "control_single_agent_accounting.json",
    "financial_pressure": "control_single_agent_pressure.json",
}

# The two supervisors whose model this control borrows. Both, not one per
# question: they run under one pin and this refuses if they ever disagree.
# `docs/HOW_WE_WORK.md` §6.
SUPERVISOR_PROMPTS = ("supervisor-accounting.md", "supervisor-pressure.md")

# Everything the control's directory may hold, and nothing else --
# `docs/CHECKLIST.md` §8 hands it "the whole bundle plus the market table", and
# those are the `input_` names `docs/INPUT_SPEC.md` §6 gives. Taken off the
# catalogue rather than written out again, so §6 moves it; used as an allowlist,
# so a name nobody has thought of is refused rather than waved through.
#
# `input_manifest.json` is the one `input_` name that is not the bundle. §6's own
# line for it reads "paragraph ids, exclusion reasons, dropped-item counts, rules
# version, cutoff, served models": the dropped-item counts are what
# `src/quote_gate.py` writes there for the three layers, which run before
# `controls` does, so a control reading it would be reading the pipeline's own
# output -- the thing `input_files` refuses a report for. No agent in
# `src/agent_inputs.py`'s `AGENTS` sees it either; it is the run's bookkeeping,
# and `run` reads it from `bundle_root` where the run keeps it.
CONTROL_SEES = tuple(name for name in agent_inputs.BUNDLE_CATALOGUE
                     if name.startswith("input_") and name != MANIFEST)

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
  "anomalies": [ {"name": "",
                  "axis": "accounting_reliability" | "financial_pressure",
                  "what": "",
                  "numbers_vs_prose": "confirms" | "contradicts" | "unresolved",
                  "evidence": [{"upstream_item_id": ""}],
                  "market_label": "priced_in" | "not_priced" | "opposite_direction" | "absent"} ] }'''

# §7 gives `evidence` one member, `upstream_item_id`. `quote` is the branch of
# `CLAUDE.md`'s rule that an agent with no upstream report has left, and the
# docstring says why; it is named here, once, and the rest of the shape is the
# document's, held in `src/prediction_schema.py`.
QUOTE = "quote"
EVIDENCE_FIELDS = prediction_schema.EVIDENCE_FIELDS + (QUOTE,)

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
`market_direction.p_up` is the probability that the 60-trading-day abnormal
return is positive, read through this question only. `"insufficient"` is an
allowed value; use it when you mean it, and do not use it to avoid being scored.

`anomalies` is the anomaly register: every anomaly you find on this question's
axis, each one listed. Your goal is to find every anomaly, not to count flags
against a cutoff, so nothing cuts the list, ranks it or counts it into a
verdict. Every `axis` is `{axis}`. `name` is a plain descriptive name in
lowercase letters and underscores, its area first and then what it is.
`numbers_vs_prose` is `confirms` when the numbers show what the prose says they
would, `contradicts` when they show the opposite, and `unresolved` when the
numbers say nothing either way. `market_label` is what the market table shows
for it -- `priced_in`, `not_priced` or `opposite_direction` -- or `absent` when
you cannot label it; an anomaly with no market label is still listed. An empty
`anomalies` list is an allowed, honest answer: give it when nothing is
anomalous, and never soften an adverse read or manufacture one.

Every entry of `evidence` carries two members: `upstream_item_id`, the paragraph
id of the file you read it in, and `quote`, that paragraph's own text, verbatim.
Python string-matches the quote against the file you were handed, character for
character -- not a dash, not a quotation mark, not a run of whitespace is
normalized -- and a checklist entry or an anomaly whose evidence does not match
is dropped whole and counted. Every id in `market_direction.basis` is a
paragraph id of those same files.
"""


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


# --- the schema -------------------------------------------------------------

def check_schema(payload, question: str, *, rules_version) -> dict:
    """The payload against `docs/CHECKLIST.md` §7, field by field, or a refusal.

    `question` and `rules_version` are checked here, because they are the
    run's: the answer has to be to the question this control asked, and the
    model does not get to invent the rules version -- a prediction scored
    against a rules version it named itself is scored against nothing, so it
    is the run's own, out of `input_manifest.json`. Every other field goes
    through `src/prediction_schema.py`, the one check both controls call, with
    this control's evidence shape as the argument.
    """
    _a_question(question)
    if not isinstance(payload, dict):
        raise ControlError(
            f"the prediction is {type(payload).__name__}, not an object")
    # Before anything else, because `continuous` belongs to one question and an
    # answer to the wrong question would be reported as a stray field.
    if payload.get("question") != question:
        raise ControlError(
            f"the prediction answers {payload.get('question')!r} and was asked "
            f"{question!r}; the two questions are never merged")
    # Asked for by name and not through `.get`: a run whose manifest carries
    # `rules_version: null` would otherwise take an answer with no such field
    # as one carrying the run's null.
    if "rules_version" not in payload:
        raise ControlError(
            "the prediction carries no rules_version, and §7 gives every "
            "prediction one: the run's")
    if payload["rules_version"] != rules_version:
        raise ControlError(
            f"the prediction carries rules_version {payload['rules_version']!r} "
            f"and this run's is {rules_version!r} — each prediction is scored "
            "against its own rules version, and that version is the run's")
    answer = {key: value for key, value in payload.items()
              if key not in prediction_schema.RUN_KEYS}
    try:
        prediction_schema.check(answer, question, evidence=EVIDENCE_FIELDS)
    except prediction_schema.SchemaError as exc:
        raise ControlError(str(exc)) from exc
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


def anomaly_gate_id(question: str, name: str) -> str:
    """The handle the gate holds one anomaly by: its name, which `check_schema`
    has already held to one entry per name, under the question."""
    return f"{question}:anomalies:{name}"


def market_gate_id(question: str) -> str:
    """The handle the gate holds `market_direction` by."""
    return f"{question}:market_direction"


def explanation_gate_id(question: str, identifier: str) -> str:
    """The handle the gate holds one explanation by.

    `docs/CHECKLIST.md` §7 gives an explanation an `id` and does not say what it
    names. §4 records each explanation "with the verbatim text and its paragraph
    id", and §7's reader item makes the notes reader's `explanation` flag "the
    only route into `explanations.json`" -- so for a supervisor the id names one
    of those reader items. This control has no upstream report, so the id it can
    write names a paragraph of the committed input, which is the same reading
    `evidence` and `market_direction.basis` already get here. The question is in
    the handle for the reason it is in the others: the two control files are
    gated in one run.
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
    names.
    """
    declared = set(index)
    found: dict[str, str] = {}
    cited = [(checklist_gate_id(question, entry["key"]), entry["evidence"])
             for entry in payload["checklist"]]
    # An anomaly rests on evidence of the checklist's own shape, so it is gated
    # the same way and goes the same way: whole, and counted.
    cited += [(anomaly_gate_id(question, entry["name"]), entry["evidence"])
              for entry in payload["anomalies"]]
    for identifier, evidence in cited:
        why = quote_gate.citation_drop_reason(
            {"id": identifier, "evidence": evidence}, declared)
        if why is None:
            why = _first_bad_quote(identifier, evidence, index)
        if why is not None:
            found[identifier] = why

    # `docs/HOW_WE_WORK.md` §7, step 6: the controls are done when a fixture
    # filing produces "both control files, with every citation resolving". An
    # explanation id is a citation like any other, and it was the one this
    # module never looked at -- an id naming another company's accession, or a
    # paragraph no committed file declares, was written through undropped and
    # uncounted.
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
    if market["p_up"] != prediction_schema.INSUFFICIENT or market["basis"]:
        market_id = market_gate_id(question)
        why = quote_gate.citation_drop_reason(
            {"id": market_id, "basis": market["basis"]}, declared)
        if why is not None:
            found[market_id] = why
    return found


def recorded_accessions(ticker: str, cutoff: dt.date, *,
                        fixtures_root=cutoff_guard.FIXTURES) -> set[str]:
    """Every accession EDGAR recorded for this company at or before the cutoff.

    `CLAUDE.md`: "document filing date ≤ filing date of the triggering report."
    The cutoff **is** that filing date, so this is that sentence as a set, over
    the record rather than over what the run says about itself.
    """
    found = set()
    for row in cutoff_guard.documents(ticker, fixtures_root=fixtures_root):
        accession, filed = row.get("accession"), row.get("filing_date")
        if not accession or not filed:
            continue
        if cutoff_guard.parse_date(filed, f"{accession} filing_date") <= cutoff:
            found.add(accession)
    return found


def resolvable(input_dir, manifest: dict, cutoff: dt.date, *,
               fixtures_root) -> dict[str, str]:
    """What the committed input declares, or a refusal naming whose it is.

    `src/quote_gate.py` builds the index by reading every `[id]` line in the
    directory, and it scopes nothing by accession -- correctly, because it
    cannot: `input_prior_predictions.md` legitimately carries ids minted from a
    *prior run's* accession, `src/assemble_bundle.py`'s `prior_predictions`
    writing `f"{accession}:prior:..."` off the earlier run's own directory name.
    So an id is not this run's because it repeats this run's accession, and a
    check written that way would refuse the prior flags the bundle is supposed
    to carry.

    What makes an id this *company's* is the record. Another company's prose
    copied into a file wearing an allowed name -- `input_notes.md`, say, holding
    NVDA's paragraphs -- passes `input_files`, which reads names, and would then
    make every NVDA id in it resolve: the explanation id this control now gates,
    its evidence quote, and `market_direction.basis` would all be written into
    this company's control file with nothing dropped and nothing counted. So
    every accession the directory declares has to be one EDGAR recorded for this
    ticker, filed at or before the cutoff -- which admits the prior runs and
    refuses both another company's filing and a later quarter of this one.

    Refused rather than dropped, and before the call rather than after: a
    directory holding another company's paragraphs is a directory that is wrong,
    not an answer that cited badly, and the layer rule is about what an agent was
    shown.
    """
    index = quote_gate.quotable(input_dir, manifest.get("accession"))
    allowed = recorded_accessions(manifest["ticker"], cutoff,
                                  fixtures_root=fixtures_root)
    foreign = sorted({identifier.split(":", 1)[0] for identifier in index}
                     - allowed)
    if foreign:
        raise ControlError(
            f"{input_dir} declares paragraphs of {', '.join(foreign)}, which is "
            f"no accession {manifest['ticker']} is recorded as having filed by "
            f"{cutoff}. A file wearing an allowed name can still hold another "
            "company's prose, or a later quarter's, and every id in it would "
            "then resolve for this run")
    return index


def verify(payload: dict, question: str, index: dict) -> tuple[dict, list[dict]]:
    """The prediction with what did not verify taken out, and one row per drop.

    Runs after `check_schema`, which is what makes one checklist key one entry:
    two entries under one key would be two items under one gate id, and an id
    that names a set resolves for nobody.

    A checklist entry goes whole, because that is what the gate does with an
    item, and so does an anomaly. An explanation goes the same way: §7 does not
    require the list to carry anything, so an explanation whose id resolves to
    nothing leaves and is counted. `market_direction` cannot go -- §7 requires
    the field -- so it degrades to the abstention §7 already allows,
    `"insufficient"` with an empty basis, and the drop is counted like any
    other.
    """
    reasons = drop_reasons(payload, question, index)
    kept = dict(payload)
    kept["checklist"] = [entry for entry in payload["checklist"]
                         if checklist_gate_id(question, entry["key"]) not in reasons]
    kept["explanations"] = [
        entry for entry in payload["explanations"]
        if explanation_gate_id(question, entry["id"]) not in reasons]
    kept["anomalies"] = [entry for entry in payload["anomalies"]
                         if anomaly_gate_id(question, entry["name"]) not in reasons]
    if market_gate_id(question) in reasons:
        kept["market_direction"] = {"p_up": prediction_schema.INSUFFICIENT, "basis": []}
    dropped = [{"report": CONTROL_FILES[question], "item_id": identifier,
                "reason": reason} for identifier, reason in sorted(reasons.items())]
    return kept, dropped


# --- the cutoff, off the record rather than off the run's own word -----------

def cutoff_on_record(manifest: dict, *,
                     fixtures_root=cutoff_guard.FIXTURES) -> dt.date:
    """The run's cutoff, held against when its own accession was filed.

    `CLAUDE.md`: "Cutoff: document filing date ≤ filing date of the triggering
    report. Nothing later enters the input." The cutoff **is** that filing date
    -- `src/assemble_bundle.py` refuses a bundle whose cutoff is either side of
    it, and `src/extraction_checks.py` carries the same rule over a whole
    manifest. Nothing here read the key at all, so a bundle carrying a cutoff of
    1999, or none, was answered by the model, gated and written out; and
    `extraction_checks.run` has no caller in `src/`, in the Makefile or in CI,
    so there is no gate ordered before this control opens the directory either.

    The date is read off `tests/fixtures/{ticker}/manifest.json` -- the record of
    what EDGAR published -- and not off `input_manifest.json`'s own
    `filing_date`. A manifest's two date keys can move together, and the run's
    word about its own boundary is the thing being checked.

    Fail-closed at every step, the gate's own rule: an absent date is not an
    early date, and an accession nobody recorded has no filing date its cutoff
    can be held to.
    """
    ticker = manifest.get("ticker")
    accession = manifest.get("accession")
    if not isinstance(ticker, str) or not ticker:
        raise ControlError(
            f"{MANIFEST} names no ticker, so the accession it names cannot be "
            "looked up and its cutoff cannot be checked against anything")
    try:
        cutoff = cutoff_guard.parse_date(manifest.get("cutoff"), f"{MANIFEST} cutoff")
        recorded = [row["filing_date"] for row
                    in cutoff_guard.documents(ticker, fixtures_root=fixtures_root)
                    if row.get("accession") == accession and row.get("filing_date")]
    except cutoff_guard.CutoffGuardError as exc:
        raise ControlError(
            f"{exc} — a control reads a bundle at its cutoff, and a run whose "
            "cutoff cannot be established is refused rather than assumed") from exc

    filed = set(recorded)
    if not filed:
        raise ControlError(
            f"{ticker} {accession} is in no fixture manifest — refused, because "
            "an unrecorded accession has no filing date for its cutoff to be "
            "held to")
    if len(filed) > 1:
        raise ControlError(
            f"{ticker} {accession} is recorded as filed on "
            f"{', '.join(sorted(filed))} — one accession is one filing, and a "
            "cutoff cannot be checked against two dates")
    filing_date = cutoff_guard.parse_date(filed.pop(), f"{accession} filing_date")
    if cutoff != filing_date:
        raise ControlError(
            f"the bundle's cutoff is {cutoff} and {ticker} {accession} was filed "
            f"{filing_date}. The cutoff is the triggering report's own filing "
            "date, and a run that moved its own boundary read documents it was "
            "not entitled to")
    return filing_date


# --- the call ----------------------------------------------------------------

def input_files(input_dir, bundle_root) -> list[str]:
    """What the control was handed, or a refusal naming what it may not hold.

    `docs/CHECKLIST.md` §8 hands this control "the whole bundle plus the market
    table", and `CONTROL_SEES` is that sentence as names. Anything else is
    refused, whatever it is called: `src/agent_inputs.py` refuses anything
    outside what a layer may hold, and its reason is this one -- "a name outside
    this set inside a session root is a file nobody decided to route, and an
    undecided file in an agent's directory is a leak nobody chose either".

    It used to be the other way round: the catalogue was read for names the
    pipeline wrote, so only a report, a prediction or another control was
    refused. Everything nobody had thought of went through and was listed to
    the model under "you see these files and nothing else" -- a price file
    carrying the outcome window, or another company's notes, neither of which
    has a name the catalogue carries. A guard that refuses only what it
    recognises is a denylist, and the second rule in `CLAUDE.md` is why this
    project does not build those.

    Every entry is read, not every file: `cutoff_guard.bundle_files` keeps what
    `is_file()` says yes to, and that both follows a symlink and drops a
    directory, so an allowlist built on it lets through the two things it has
    no name for. `src/agent_inputs.py` walks `iterdir()` and tests the symlink
    *before* anything that follows one, "because both it and `read_bytes()`
    follow the link"; the same order is the only one that works here, since
    `is_file()` on a link into another company's run says yes.

    **And then the bytes.** A name says which file this is meant to be and
    nothing about whose it is. Another company's `input_trends.json`,
    `input_market.json` or `input_companyfacts.json`, *copied* under its allowed
    name, answers every question above: it is not a link, it is not a directory,
    and its name is on the list. Two of those three declare no paragraph ids at
    all, so `resolvable` cannot see them either, and the third has its ids minted
    from this run's accession by `src/quote_gate.py` rather than read out of the
    file -- so a foreign trend table is indexed under this run's ids and its
    values string-match as verbatim quotes. `src/agent_inputs.py` has the check
    this needs and says why in one line: "the one thing a check on names cannot
    see: a hardlink to another file resolves inside the root and answers to the
    right name." So every admitted file is held against the run's own file of
    that name, byte for byte, through that same `_differs`. The run directory is
    what `docs/HOW_WE_WORK.md` §1.6 makes the boundary -- "the per-run, per-agent
    input directory ... is committed as what that agent saw" -- and a directory
    that is not a copy of the run is not a record of anything.
    """
    folder = Path(input_dir)
    entries = sorted(folder.iterdir(), key=lambda path: path.name) \
        if folder.is_dir() else []
    if not entries:
        raise ControlError(
            f"{input_dir} holds no files — a control with no input is not a control")
    linked = [path for path in entries if path.is_symlink()]
    if linked:
        named = ", ".join(f"{path.name} to {path.readlink()}" for path in linked)
        raise ControlError(
            f"{input_dir} holds {named}. A control reads the directory it was "
            "handed: a link's ancestors are somewhere else, so a file carrying "
            "an allowed name can still be another run's, and the allowlist "
            "above would have read the name and not the bytes")
    stray = [path.name for path in entries if path.name not in CONTROL_SEES]
    if stray:
        raise ControlError(
            f"{input_dir} holds {', '.join(stray)}, which this control may not "
            "see. It is handed the bundle and the market table and nothing "
            "else: the pipeline's own output here would make it a reader of the "
            "pipeline rather than a control beside it, and a file nobody routed "
            "here is a leak nobody chose. The prompt tells the model it sees "
            "these files and nothing else, so the directory is what that "
            "sentence means")
    nested = [path.name for path in entries if not path.is_file()]
    if nested:
        raise ControlError(
            f"{input_dir} holds {', '.join(nested)}, which is a directory and "
            "not one of the files. The prompt lists what the control sees, and "
            "a directory carrying an allowed name carries whatever is under it "
            "under no name at all")

    run_dir = Path(bundle_root)
    for path in entries:
        ours = run_dir / path.name
        if not ours.is_file():
            raise ControlError(
                f"{input_dir} holds {path.name} and {bundle_root} has none. The "
                "control's directory is a copy of the run's own files, and a "
                "file the run never wrote is one nobody assembled for it")
        if agent_inputs._differs(path, ours):
            raise ControlError(
                f"{input_dir} holds a {path.name} that is not the run's — the "
                "right name over other bytes. Another company's file answers to "
                "the same name, and a name is all the list above can read; the "
                "directory is committed as what the control saw, so what is in "
                "it has to be what the run assembled")

    prior = folder / PRIOR_PREDICTIONS
    if prior.is_file():
        # The name is allowed and the contents still have to be. `docs/INPUT_SPEC.md`
        # §6 gives this file "prior flags and outcomes, probabilities removed",
        # and `docs/HOW_WE_WORK.md` §8 forbids putting "a prior run's probability
        # into any agent's input" -- `src/agent_inputs.py` refuses to place one
        # that still carries one, calling it the leak that makes the next
        # prediction unfalsifiable. Its reader is used rather than a second
        # pattern written here, so one file decides what a probability looks
        # like.
        leak = agent_inputs._probability_leak(
            prior.read_text(encoding="utf-8", errors="replace"))
        if leak is not None:
            raise ControlError(
                f"{prior} still carries a probability ({leak}). A prior run's "
                "own score in this control's input makes the next prediction "
                "unfalsifiable, and the control is scored beside the pipeline "
                "on the same targets")
    return [path.name for path in entries]


def prompt(question: str, input_dir, bundle_root) -> str:
    """The one prompt this control sends, with the question and its files in it.

    `bundle_root` is here because the file list is not a listing: every name
    in it is a file `input_files` has held against the run's own copy, so the
    sentence "you see these files and nothing else" is about those bytes.
    """
    _a_question(question)
    listed = "\n".join(f"- {name}" for name in input_files(input_dir, bundle_root))
    return CONTROL_PROMPT.format(question=question.replace("_", " "),
                                 axis=question, files=listed, schema=SCHEMA)


def destination(bundle_root) -> Path:
    """Where this control's file may land: the run directory, and outside every input tree.

    `docs/INPUT_SPEC.md` §6 lists the two control files in the committed bundle,
    under `runs/{ticker}/{accession}/` -- the run directory, which is what
    `bundle_root` is and where `run` writes. The same paragraph makes "each
    agent's input directory" the isolation boundary, "committed as what it
    saw", and `docs/HOW_WE_WORK.md` §1.6 says it again. A run directory planted
    under another run's `agents/` tree reads, gates and answers like any other,
    and the file it would write is then part of what that tree records one of
    its agents as having seen. Checked before anything is read, so no model is
    asked a question whose answer has nowhere it may go.
    """
    held = agent_inputs.input_tree_holding(bundle_root)
    if held is not None:
        raise ControlError(
            f"{bundle_root} is inside {held}, a run's per-agent input tree. That "
            "tree is committed as what each agent saw, so a control file written "
            "there rewrites another agent's record of its input; a control's "
            "files land in the run directory, beside the bundle")
    return Path(bundle_root)


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


def run(question: str, *, input_dir, bundle_root, ask,
        prompts_dir: Path = AGENT_PROMPTS,
        fixtures_root=cutoff_guard.FIXTURES) -> dict:
    """One call, gated, and the control file on disk.

    `ask(prompt, model=...)` is the caller's one model call. It returns
    `{"served_model": ..., "text": ...}`: the model that actually answered, and
    its answer as characters. There is no model client in this repository, so
    the call belongs to whoever runs the stage; what belongs here is the prompt,
    the pin, the schema and the gate.

    Everything about the input is settled before the call, not after it: the
    directory holds what it may hold, `cutoff_on_record` holds the bundle's own
    `cutoff` against when EDGAR recorded its accession as filed, and `resolvable`
    reads what the directory declares and refuses another company's paragraphs.
    A refusal after the answer has come back is a refusal that has already paid
    for the look-ahead, and a directory that is wrong is one no model may see.

    Returns the payload as written, the file it was written to, the requested
    and served model, and one row per drop -- `docs/INPUT_SPEC.md` §6 puts the
    drop count and the served model in `input_manifest.json` and the module
    docstring says why this hands them back rather than writing them there.
    """
    out = destination(bundle_root)
    family = supervisor_model(prompts_dir)
    manifest = json.loads(cutoff_guard.load_bundle_file(bundle_root, MANIFEST))
    accession = manifest.get("accession")
    if not isinstance(accession, str) or not accession:
        raise ControlError(
            f"{MANIFEST} names no accession, and a computed row's id begins with one")
    # The directory first, because `quote_gate.quotable` reads every `.md` in it
    # and a stray one would be indexed before anything had said it may be there.
    text = prompt(question, input_dir, bundle_root)
    filed = cutoff_on_record(manifest, fixtures_root=fixtures_root)
    index = resolvable(input_dir, manifest, filed, fixtures_root=fixtures_root)

    answer = ask(text, model=family)
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
    kept, dropped = verify(payload, question, index)
    path = _place(out / CONTROL_FILES[question],
                  json.dumps(kept, indent=INDENT, sort_keys=True) + "\n")
    return {"question": question, "path": path, "prediction": kept,
            "dropped": dropped, "requested_model": family, "served_model": served}


def main(argv=None) -> int:
    code = interpreter_pin.enforce()
    if code:
        return code
    parser = argparse.ArgumentParser(
        description="Print the single-agent control's one call for one question.")
    parser.add_argument("--question", required=True, choices=sorted(CONTROL_FILES))
    parser.add_argument("--input", required=True,
                        help="the directory the control is handed")
    parser.add_argument("--bundle", required=True,
                        help="the run directory, whose files that directory copies")
    parser.add_argument("--prompts", default=str(AGENT_PROMPTS),
                        help="where the supervisor prompts are, for the model pin")
    args = parser.parse_args(argv)
    try:
        model = supervisor_model(Path(args.prompts))
        text = prompt(args.question, args.input, args.bundle)
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
