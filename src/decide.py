"""The decide stage's Python half: the rules a supervisor is handed, the market
table it is not, and what of its answer stands.

`docs/HOW_WE_WORK.md` gives `decide` two calls, supervisor-accounting and
supervisor-pressure, and three checks: the output schema is valid, every
citation resolves to an upstream report, and the served model equals the pin.
The calls are the supervisors' own, in sessions rooted at their directories.
This module is what Python does around them, and like `src/quote_gate.py` it
has no command line: no stage runner exists yet, and the one that calls these
functions hands them the answer it read back.

**The rules beside the reports.** Both supervisor prompts say their directory
holds, alongside the four reports, "the rules version's checklist keys and
output schema", and tell the supervisor to write its prediction "against the
schema in `docs/CHECKLIST.md`". Nothing routed either, and a session rooted at
the supervisor's directory cannot reach the document, so the committed prompt
asked for a §7 prediction and could not show one. `write_rules` writes the two
files into the run directory, out of `docs/CHECKLIST.md` and nothing else, and
`src/agent_inputs.py` routes them to the two supervisors and to no other agent:

    rules_output_schema.md    §7's block, with the run's rules version in it
    rules_checklist_keys.md   the key column of §1 and of §2, under their headings

The keys file carries names only -- not where each indicator is read, who
computes it or when it flags. They are rules and not evidence, and the prompt
says what that means: "you answer with them, never about them". A supervisor
still never sees `docs/CHECKLIST.md` itself.

**No market table.** The owner's decision of 2026-09-13: until a price source
answers, the comparers are off and the first predictions publish on filings
alone. Of 2026-09-23: the supervisors then run on the two reader reports,
`market_direction` is written `"insufficient"`, and the manifest says why --
`"no price source"`. `mark_market_unavailable` writes that into
`input_manifest.json` as `market_table: "unavailable"` beside
`market_table_reason`, with each comparer's label written `absent` under
`comparer_labels` -- not `not_priced`, which is a reading of a market, and not a
guess -- and refuses a run that holds a market table or a
comparer report, because such a run would be saying two things about its
market. `src/agent_inputs.py` reads the key, builds no comparer, and builds
each supervisor over the two reader reports. `published` writes the
abstention whatever the supervisor said, and `record` keeps what it said in
the manifest beside the reason, so the override is on the record and the
supervisor's own words are not lost.

**What of an answer stands.** `check` holds the answer to the question it was
asked and to the run's rules version, then to §7 field by field through
`src/prediction_schema.py`, the check both controls call. `gate_items` turns
the entries that cite into items `src/quote_gate.py`'s `gate` can hold, named
by the question and the entry's own key, so the stage runner gates the
supervisors in the same call as the readers and every drop in the run is
counted in one place. `published` is the answer with every item the gate
dropped taken out: a checklist entry whole, a `top_signals` name with its
entry, and a `market_direction` that cannot be dropped -- §7 requires the
field -- degraded to the abstention §7 allows. The prediction file is written
once, into the run directory; the supervisor's own file stays in its session
root as it wrote it.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    from src import agent_inputs, cutoff_guard, prediction_schema
except ImportError:  # invoked as a plain script
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import agent_inputs, cutoff_guard, prediction_schema

CHECKLIST = Path(__file__).resolve().parent.parent / "docs" / "CHECKLIST.md"
MANIFEST = agent_inputs.MANIFEST
INDENT = 2

# The two files, named where the layer table routes them.
KEYS_FILE, SCHEMA_FILE = agent_inputs.RULES_FILES

# Which supervisor answers which question, and the file its prompt names.
QUESTIONS = {
    "supervisor-accounting": "accounting_reliability",
    "supervisor-pressure": "financial_pressure",
}
PREDICTION_FILES = {question: agent_inputs.AGENTS[agent].writes
                    for agent, question in QUESTIONS.items()}

# `docs/CHECKLIST.md`'s own headings for the two key tables, and the section
# that ends each one. The count in each heading is the document's, and
# `checklist_keys` refuses a table that does not come to it.
KEY_SECTIONS = {
    "accounting_reliability": ("## 1. Input indicators — accounting reliability",
                               "## 2."),
    "financial_pressure": ("## 2. Input indicators — financial pressure", "## 3."),
}
KEY_ROW = re.compile(r"^\| `([a-z0-9_]+)` \|", re.MULTILINE)
KEY_COUNT = re.compile(r"\((\d+)\)\s*$")

# The owner's words for why a run has no market table, and what the manifest
# calls it.
MARKET_TABLE_KEY = agent_inputs.MARKET_TABLE_KEY
MARKET_REASON_KEY = agent_inputs.MARKET_REASON_KEY
UNAVAILABLE = agent_inputs.MARKET_UNAVAILABLE
NO_PRICE_SOURCE = "no price source"
ABSTAIN = {"p_up": prediction_schema.INSUFFICIENT, "basis": []}
OVERRIDE_KEY = "market_direction_written_insufficient"

# The label a comparer that did not run leaves, written for each one. Not
# `not_priced`: that says the market was read and showed nothing, and with no
# market table nobody read it. `src/agent_inputs.py` holds a manifest to it.
ABSENT = agent_inputs.ABSENT
COMPARER_LABELS_KEY = agent_inputs.COMPARER_LABELS_KEY
COMPARERS = agent_inputs.COMPARERS


class DecideError(Exception):
    """The decide stage cannot go on with what it was handed."""


# --- the manifest ------------------------------------------------------------

def _manifest(run) -> dict:
    try:
        manifest = json.loads(cutoff_guard.load_bundle_file(run, MANIFEST))
    except (cutoff_guard.CutoffGuardError, ValueError) as exc:
        raise DecideError(f"{Path(run) / MANIFEST} does not read: {exc}") from exc
    if not isinstance(manifest, dict):
        raise DecideError(f"{Path(run) / MANIFEST} is not an object")
    return manifest


def _update_manifest(run, changes: dict) -> dict:
    """The manifest with `changes` set and every other key left alone.

    The same convention `src/quote_gate.py` writes its counts by: the stages
    before `publish` add to the manifest, and nothing under `runs/` is written
    after it is committed.
    """
    manifest = _manifest(run)
    manifest.update(changes)
    (Path(run) / MANIFEST).write_text(
        json.dumps(manifest, indent=INDENT, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def mark_market_unavailable(run, reason: str = NO_PRICE_SOURCE) -> dict:
    """Say in the manifest that this run has no market table, and why, and
    that each comparer's label is `absent`."""
    run = Path(run)
    if not isinstance(reason, str) or not reason.strip():
        raise DecideError("a run with no market table says why, and no reason was given")
    present = [name for name in (agent_inputs.MARKET_TABLE,) + agent_inputs.COMPARER_REPORTS
               if (run / name).is_file()]
    # A comparer's directory is built over a market table, so one that exists
    # ran, or is about to, whether or not its report has reached the run.
    present += [f"{agent_inputs.AGENTS_DIRNAME}/{name}/" for name in COMPARERS
                if agent_inputs.session_root(run, name).exists()]
    if present:
        raise DecideError(
            f"{run} holds {', '.join(present)}, so it has a market table or a "
            "comparer has already read one; a run that also said its market "
            "table is unavailable would be saying two things")
    manifest = _manifest(run)
    labels = {name: ABSENT for name in COMPARERS}
    said = (manifest.get(MARKET_TABLE_KEY), manifest.get(MARKET_REASON_KEY),
            manifest.get(COMPARER_LABELS_KEY))
    if said != (None, None, None) and said != (UNAVAILABLE, reason, labels):
        raise DecideError(
            f"{run / MANIFEST} already says the market table is {said[0]!r} "
            f"({said[1]!r}) and the comparer labels are {said[2]!r}; it is "
            "written once")
    return _update_manifest(run, {MARKET_TABLE_KEY: UNAVAILABLE,
                                  MARKET_REASON_KEY: reason,
                                  COMPARER_LABELS_KEY: labels})


# --- the rules beside the reports ---------------------------------------------

def checklist_keys(text: str | None = None) -> dict[str, tuple[str, ...]]:
    """The key column of §1 and of §2, in the document's order."""
    text = CHECKLIST.read_text(encoding="utf-8") if text is None else text
    found = {}
    for question, (heading, until) in KEY_SECTIONS.items():
        start = text.find(heading)
        if start < 0:
            raise DecideError(f"docs/CHECKLIST.md has no heading {heading!r}")
        line = text[start:text.index("\n", start)]
        end = text.find(until, start + len(heading))
        section = text[start:end if end >= 0 else len(text)]
        keys = tuple(KEY_ROW.findall(section))
        count = KEY_COUNT.search(line)
        if count is None or int(count.group(1)) != len(keys):
            raise DecideError(
                f"{line!r} and its tables disagree: the tables carry {len(keys)} "
                "keys, and a keys file that is not the document's count is not "
                "the document's list")
        if len(set(keys)) != len(keys):
            raise DecideError(f"{heading!r} names one key twice")
        found[question] = keys
    return found


def rules_texts(rules_version) -> dict[str, str]:
    """The two rules files, as a supervisor's directory holds them."""
    keys = checklist_keys()
    lines = ["# The checklist keys", "",
             "The key column of docs/CHECKLIST.md §1 and §2, names only.", ""]
    for question, names in keys.items():
        lines += [f"## {question}", ""] + [f"- `{name}`" for name in names] + [""]
    try:
        schema = prediction_schema.block(rules_version)
    except prediction_schema.SchemaError as exc:
        raise DecideError(str(exc)) from exc
    return {
        KEYS_FILE: "\n".join(lines),
        SCHEMA_FILE: ("# The output schema\n\n"
                      "docs/CHECKLIST.md §7, \"The two predictions\", with this "
                      "run's rules version.\n\n```json\n" + schema + "\n```\n"),
    }


def write_rules(run) -> list[Path]:
    """Both rules files, into the run directory, once."""
    run = Path(run)
    manifest = _manifest(run)
    if "rules_version" not in manifest:
        raise DecideError(
            f"{run / MANIFEST} names no rules_version, and the schema a "
            "supervisor is shown carries the run's")
    written = []
    for name, text in rules_texts(manifest["rules_version"]).items():
        path = run / name
        if path.exists() or path.is_symlink():
            if path.is_symlink() or path.read_text(encoding="utf-8") != text:
                raise DecideError(
                    f"{path} is already on record with different content. A run "
                    "directory is append-only; a correction is a new run")
        else:
            path.write_text(text, encoding="utf-8")
        written.append(path)
    return written


# --- what of an answer stands ------------------------------------------------

def check(run, question: str, answer) -> dict:
    """The answer against its question, the run's rules version and §7."""
    if question not in PREDICTION_FILES:
        raise DecideError(f"{question!r} is not a question; one of "
                          f"{', '.join(PREDICTION_FILES)}")
    if not isinstance(answer, dict):
        raise DecideError(f"the {question} answer is {type(answer).__name__}, "
                          "not an object")
    if answer.get("question") != question:
        raise DecideError(
            f"the prediction answers {answer.get('question')!r} and was asked "
            f"{question!r}; the two questions are never merged")
    manifest = _manifest(run)
    if "rules_version" not in answer or "rules_version" not in manifest:
        raise DecideError(
            "§7 gives every prediction the run's rules_version, and the answer "
            "or the run names none")
    if answer["rules_version"] != manifest["rules_version"]:
        raise DecideError(
            f"the prediction carries rules_version {answer['rules_version']!r} and "
            f"this run's is {manifest['rules_version']!r} — each prediction is "
            "scored against its own rules version, and that version is the run's")
    rest = {key: value for key, value in answer.items()
            if key not in prediction_schema.RUN_KEYS}
    try:
        prediction_schema.check(rest, question,
                                evidence=prediction_schema.EVIDENCE_FIELDS)
    except prediction_schema.SchemaError as exc:
        raise DecideError(str(exc)) from exc
    return answer


def checklist_id(question: str, key: str) -> str:
    return f"{question}:checklist:{key}"


def explanation_id(question: str, identifier: str) -> str:
    return f"{question}:explanations:{identifier}"


def market_id(question: str) -> str:
    return f"{question}:market_direction"


def gate_items(question: str, answer: dict) -> list[dict]:
    """Every entry of a checked answer that cites, as an item the gate can hold.

    A checklist entry carries its evidence; an explanation's `id` names the
    upstream item it is about, which is how the shuffled control reads it too
    and which `docs/needs_judgment.md` still holds open; `market_direction`
    cites through `basis`, and is an item only when it answers.
    """
    items = [{"id": checklist_id(question, entry["key"]),
              "evidence": entry["evidence"]} for entry in answer["checklist"]]
    items += [{"id": explanation_id(question, entry["id"]),
               "upstream_item_id": entry["id"]} for entry in answer["explanations"]]
    market = answer["market_direction"]
    if market["p_up"] != prediction_schema.INSUFFICIENT or market["basis"]:
        items.append({"id": market_id(question), "basis": market["basis"]})
    return items


def published(run, question: str, answer: dict, kept: list[dict]) -> tuple[dict, dict | None]:
    """The prediction as it is published, and the market override if there was one.

    `kept` is what the gate kept of `gate_items(question, answer)`.
    """
    standing = {item["id"] for item in kept}
    prediction = dict(answer)
    prediction["checklist"] = [entry for entry in answer["checklist"]
                               if checklist_id(question, entry["key"]) in standing]
    names = {entry["key"] for entry in prediction["checklist"]}
    prediction["top_signals"] = [one for one in answer["top_signals"] if one in names]
    prediction["explanations"] = [entry for entry in answer["explanations"]
                                  if explanation_id(question, entry["id"]) in standing]
    market = answer["market_direction"]
    cited = market["p_up"] != prediction_schema.INSUFFICIENT or market["basis"]
    if cited and market_id(question) not in standing:
        prediction["market_direction"] = dict(ABSTAIN)

    reason = agent_inputs.market_unavailable(run)
    override = None
    if reason is not None:
        prediction["market_direction"] = dict(ABSTAIN)
        override = {"prediction": PREDICTION_FILES[question], "reason": reason,
                    "supervisor_said": market}
    return prediction, override


def write_prediction(run, question: str, prediction: dict) -> Path:
    """The published prediction, into the run directory, once."""
    path = Path(run) / PREDICTION_FILES[question]
    text = json.dumps(prediction, indent=INDENT, sort_keys=True) + "\n"
    if path.exists() or path.is_symlink():
        if path.is_symlink() or path.read_text(encoding="utf-8") != text:
            raise DecideError(
                f"{path} is already on record with different content. A "
                "prediction is written once; a correction is a new run")
        return path
    path.write_text(text, encoding="utf-8")
    return path


def record(run, overrides: list[dict]) -> dict:
    """Every market direction written insufficient, and what the supervisor said."""
    return _update_manifest(run, {OVERRIDE_KEY: [dict(row) for row in overrides]})
