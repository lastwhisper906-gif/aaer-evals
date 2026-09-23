"""The two predictions' schema, `docs/CHECKLIST.md` §7, and the one check of it.

Both controls answer this schema: the single-agent control, which does the whole
job alone, and the shuffled control, whose supervisor reads one company's
numbers beside another company's notes. `docs/CHECKLIST.md` §8 scores them on
the same rows as the pipeline, so a field one of them checks and the other does
not is a difference between the controls that is not the thing either of them
tests. Each used to carry its own copy of the check: the field lists, the three
findings, the three support words, the three tiers and the signal ceiling were
written out twice, and a test asserted the two copies equal. They agreed by both
reading §7, and the assertion was a test standing in for a function. This is the
function, and both controls call it.

**`evidence` is the one field they legitimately differ on, so it is an
argument.** §7 gives an evidence entry one member, `upstream_item_id`, which
names an item of an upstream report. The shuffled control's supervisor has four
upstream reports, so §7's own shape is the whole of it. The single-agent
control's upstream is the committed filing itself, so the id it writes names a
paragraph, and `CLAUDE.md`'s rule -- "a verbatim quote or an upstream item id
that Python verifies" -- leaves it one way to verify one: a quote travels with
it. `check` takes the members an evidence entry carries and refuses a set that
leaves out §7's own, so a caller may add to the schema there and never take
away from it.

**`question` and `rules_version` are the run's, and are not checked here.** The
shuffled control writes both itself and refuses them in the supervisor's answer;
the single-agent control asks the model for both and holds them against the
question it asked and the run's manifest. Each does that before calling this,
and hands it the rest. A prediction scored against a rules version it named for
itself is scored against nothing, and only the caller knows the run's.

Every value below is §7 read by hand, and §1 for the one list §7 leaves blank:
`"finding": ""` names no values, and §1's "An LLM answer is always `flag` /
`no_flag` / `insufficient`" is the only place the three are written down.
`tests/test_control_shuffled.py` holds them against §7 twice over: once written
out by hand in the test, and once parsed out of the document.

This module raises `SchemaError` and nothing else. Each control turns it into
its own `ControlError` at the one line that calls `check`, so a refusal reads
the same whichever control met it.
"""

from __future__ import annotations

import json
import math
from collections import Counter

# `docs/CHECKLIST.md` §7: `"question": "accounting_reliability" | "financial_pressure"`.
QUESTIONS = ("accounting_reliability", "financial_pressure")

# The two fields of §7 that the run settles rather than the answer. See the
# module docstring: the caller checks them and hands the rest to `check`.
RUN_KEYS = ("question", "rules_version")

# Every other field of §7, in §7's order, except `continuous`: "`continuous` is
# financial pressure only", so it is required of one question and refused on
# the other rather than tolerated on both.
PREDICTED_KEYS = ("checklist", "events", "explanations", "market_direction",
                  "tier", "top_signals")
CONTINUOUS = "continuous"
CONTINUOUS_QUESTION = "financial_pressure"

# The members of each nested object, as §7 writes them.
CHECKLIST_FIELDS = ("key", "finding", "confidence", "evidence")
EVIDENCE_FIELDS = ("upstream_item_id",)
CONTINUOUS_FIELDS = ("key", "point", "direction", "low", "high")
EVENT_FIELDS = ("key", "p_within_horizon")
EXPLANATION_FIELDS = ("id", "support", "realization_p")
MARKET_FIELDS = ("p_up", "basis")

# The three closed value lists: §1's findings, and §7's support words and tiers.
FINDINGS = ("flag", "no_flag", "insufficient")
SUPPORT = ("sufficient", "insufficient", "unknown")
TIERS = ("elevated", "watch", "clear")

# "`p_up` may be `"insufficient"` instead of a number, and that is recorded and
# counted." Also the abstention a market call degrades to when its basis
# resolves to nothing: §7 requires the field, so it cannot be dropped.
INSUFFICIENT = "insufficient"

# "`top_signals` holds at most five keys."
TOP_SIGNALS_MAX = 5

SCHEMA = "docs/CHECKLIST.md §7"

# §7's block, copied out of the document character for character, so a model
# that is shown the schema is shown the document's own shape. The single-agent
# control's prompt carries it, and the decide stage hands it to both supervisors
# as a file of their directory. `tests/test_control_single_agent.py` asserts it
# is still a slice of `docs/CHECKLIST.md`.
BLOCK = '''{ "question": "accounting_reliability" | "financial_pressure",
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

# §7 prints "0.1" where a prediction's rules version goes, and the version is
# the run's, not the document's. So a model is shown the run's own, in that one
# place, and §7 character for character everywhere else. Asking for "0.1" and
# holding the answer to the run's null is how both single-agent calls on the
# second pipeline check (PR #73) were refused; a pilot run carries "pilot" since
# the owner's decision of 2026-09-23.
BLOCK_RULES_VERSION = '"rules_version": "0.1",'


def block(rules_version) -> str:
    """§7's schema, with the run's rules version where §7 prints "0.1"."""
    if BLOCK.count(BLOCK_RULES_VERSION) != 1:
        raise SchemaError(
            "the schema no longer carries §7's rules_version line once, so there "
            "is no one place to put the run's version")
    return BLOCK.replace(BLOCK_RULES_VERSION,
                         f'"rules_version": {json.dumps(rules_version)},')


class SchemaError(Exception):
    """An answer that is not the prediction `docs/CHECKLIST.md` §7 describes."""


def _fields(entry, expected: tuple[str, ...], where: str, *,
            given_by: str = SCHEMA) -> None:
    if not isinstance(entry, dict):
        raise SchemaError(f"{where} is {type(entry).__name__}, not an object")
    found = tuple(sorted(entry))
    if found != tuple(sorted(expected)):
        raise SchemaError(
            f"{where} carries {', '.join(found) or 'no fields'} and "
            f"{given_by} gives it {', '.join(sorted(expected))}")


def _a_list(question: str, key: str, value) -> list:
    """One list the schema promised, or a refusal rather than an iteration over it."""
    if not isinstance(value, list):
        raise SchemaError(
            f"the {question} answer gives {key} as {type(value).__name__}, and "
            f"{SCHEMA} gives it as a list")
    return value


def _text(entry, field: str, where: str) -> str:
    value = entry.get(field)
    if not isinstance(value, str) or not value.strip():
        raise SchemaError(
            f"{where}.{field} is {value!r}, and the schema gives it a name")
    return value


def _one_of(entry, field: str, allowed: tuple[str, ...], where: str) -> str:
    value = entry.get(field)
    if value not in allowed:
        raise SchemaError(
            f"{where}.{field} is {value!r}; the schema allows {', '.join(allowed)}")
    return value


def _number(entry, field: str, where: str, *, low=None, high=None) -> float:
    value = entry.get(field)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise SchemaError(
            f"{where}.{field} is {value!r}, and the schema gives it a number")
    # An infinity is an instance of `float`, and the range below runs only on a
    # field §7 gives a range to. `point`, `low` and `high` have none, so without
    # this an infinity there reaches the file and `json.dumps` writes it as
    # `Infinity` -- a bare token RFC 8259 does not have, which `json.loads`
    # reads back without complaint unless it is handed a `parse_constant`. A
    # number outside its range costs one item; a number outside JSON costs the
    # file.
    if not math.isfinite(value):
        raise SchemaError(
            f"{where}.{field} is {value!r} — json.dumps spells these Infinity "
            "and NaN, which are not JSON, and a prediction file the scorer "
            "cannot read back is the prediction lost")
    if low is not None and not low <= value <= high:
        raise SchemaError(
            f"{where}.{field} is {value}, outside {low} to {high} — a probability "
            "outside its own range is not a probability")
    return float(value)


def _unique(keys: list[str], where: str) -> None:
    """One indicator, one key — `docs/CHECKLIST.md` §2 says it in those words."""
    repeated = sorted(key for key, count in Counter(keys).items() if count > 1)
    if repeated:
        raise SchemaError(
            f"{where} names {', '.join(repeated)} more than once; one indicator, "
            "one key, and a repeated key names a set")


def check(answer, question: str, *, evidence: tuple[str, ...]) -> dict:
    """The answer against `docs/CHECKLIST.md` §7, field by field, or a refusal.

    `answer` is the prediction without `question` and `rules_version`, which
    are the caller's to settle. `evidence` is the members one evidence entry
    carries: §7's own `upstream_item_id`, and whatever the caller's upstream
    adds beside it. Returns the answer unchanged.

    A field with no citation in it is checked as closely as one with: a control
    file is scored -- §8 scores market direction by Brier and hit rate, events
    by Brier -- so an unscorable value on record is a row of the scorecard that
    cannot be computed, found later and with nothing to recover.
    """
    if question not in QUESTIONS:
        raise SchemaError(f"{question!r} is not a question; one of {', '.join(QUESTIONS)}")
    dropped = [member for member in EVIDENCE_FIELDS if member not in evidence]
    if dropped:
        raise SchemaError(
            f"an evidence entry asked to carry {', '.join(evidence) or 'nothing'} "
            f"leaves out {', '.join(dropped)}, which {SCHEMA} gives it. A caller "
            "may add to the evidence shape for its own upstream; it may not take "
            "the schema's own member away")
    if not isinstance(answer, dict):
        raise SchemaError(f"the prediction is {type(answer).__name__}, not an object")
    missing = [key for key in PREDICTED_KEYS if key not in answer]
    if missing:
        raise SchemaError(
            f"the {question} answer has no {', '.join(missing)}; a prediction is "
            "scored on every target the schema gives it and cannot be short of "
            f"one ({SCHEMA})")
    wants_continuous = question == CONTINUOUS_QUESTION
    # `continuous` before the closed-prediction check below, because that check
    # refuses every field §7 does not give this question -- `continuous` on
    # accounting reliability among them -- in one sentence. Asked in this order
    # the sentence naming this field is reachable and says its own thing.
    if wants_continuous and CONTINUOUS not in answer:
        raise SchemaError(f"the {question} answer has no {CONTINUOUS}, which the "
                          "schema requires of this question")
    if not wants_continuous and CONTINUOUS in answer:
        raise SchemaError(f"the {question} answer carries {CONTINUOUS}, which the "
                          "schema gives to financial pressure alone")
    # Closed, like every nested object below. A field the schema has no column
    # for would be written into the prediction file whole, beside the checked
    # ones, and nothing would ever score it.
    allowed = PREDICTED_KEYS + ((CONTINUOUS,) if wants_continuous else ())
    stray = sorted(set(answer) - set(allowed))
    if stray:
        raise SchemaError(
            f"the {question} answer carries {', '.join(stray)}, which {SCHEMA} "
            f"does not give an answer. {' and '.join(RUN_KEYS)} are the run's "
            "to settle, and a field the schema has no column for is a row of "
            "the scorecard nobody can score")

    added = tuple(member for member in evidence if member not in EVIDENCE_FIELDS)
    evidence_given_by = SCHEMA + (f", with {', '.join(added)} beside it," if added else "")
    checklist = _a_list(question, "checklist", answer["checklist"])
    for position, entry in enumerate(checklist, start=1):
        where = f"checklist[{position}]"
        _fields(entry, CHECKLIST_FIELDS, where)
        _text(entry, "key", where)
        _one_of(entry, "finding", FINDINGS, where)
        _number(entry, "confidence", where, low=0, high=1)
        cites = _a_list(question, f"{where}.evidence", entry["evidence"])
        for index, cited in enumerate(cites, start=1):
            cited_where = f"{where}.evidence[{index}]"
            _fields(cited, evidence, cited_where, given_by=evidence_given_by)
            for member in evidence:
                _text(cited, member, cited_where)
    _unique([entry["key"] for entry in checklist], "checklist")

    if wants_continuous:
        continuous = _a_list(question, CONTINUOUS, answer[CONTINUOUS])
        if not continuous:
            raise SchemaError(
                "continuous is empty; financial pressure predicts next quarter's "
                "revenue growth, operating margin and operating cash flow")
        for position, entry in enumerate(continuous, start=1):
            where = f"{CONTINUOUS}[{position}]"
            _fields(entry, CONTINUOUS_FIELDS, where)
            _text(entry, "key", where)
            # §7 gives `direction` a string and does not enumerate its values.
            _text(entry, "direction", where)
            point = _number(entry, "point", where)
            low = _number(entry, "low", where)
            high = _number(entry, "high", where)
            if not low <= point <= high:
                raise SchemaError(
                    f"{where} puts its point {point} outside its own range "
                    f"{low} to {high}")
        _unique([entry["key"] for entry in continuous], CONTINUOUS)

    events = _a_list(question, "events", answer["events"])
    for position, entry in enumerate(events, start=1):
        where = f"events[{position}]"
        _fields(entry, EVENT_FIELDS, where)
        _text(entry, "key", where)
        _number(entry, "p_within_horizon", where, low=0, high=1)
    _unique([entry["key"] for entry in events], "events")

    explanations = _a_list(question, "explanations", answer["explanations"])
    for position, entry in enumerate(explanations, start=1):
        where = f"explanations[{position}]"
        _fields(entry, EXPLANATION_FIELDS, where)
        _text(entry, "id", where)
        _one_of(entry, "support", SUPPORT, where)
        _number(entry, "realization_p", where, low=0, high=1)
    _unique([entry["id"] for entry in explanations], "explanations")

    market = answer["market_direction"]
    _fields(market, MARKET_FIELDS, "market_direction")
    if market["p_up"] != INSUFFICIENT:
        _number(market, "p_up", "market_direction", low=0, high=1)
    basis = market["basis"]
    if not isinstance(basis, list) or not all(
            isinstance(one, str) and one.strip() for one in basis):
        raise SchemaError(
            f"market_direction.basis is {basis!r}; {SCHEMA} gives it a list of "
            "the ids the probability rests on, and an id that is not a name "
            "resolves for nobody")

    _one_of(answer, "tier", TIERS, "the prediction")

    signals = _a_list(question, "top_signals", answer["top_signals"])
    for position, one in enumerate(signals, start=1):
        if not isinstance(one, str) or not one.strip():
            raise SchemaError(
                f"top_signals[{position}] is {one!r}, and a signal is the key of "
                "a checklist entry")
    _unique(signals, "top_signals")
    if len(signals) > TOP_SIGNALS_MAX:
        raise SchemaError(
            f"top_signals names {len(signals)} signals and {SCHEMA} allows at "
            f"most {TOP_SIGNALS_MAX}")
    # A signal naming no checklist entry at all is the answer contradicting
    # itself before any citation is resolved, so it is refused here rather than
    # dropped later. A signal whose entry is dropped later, for citing nothing a
    # control can resolve, leaves quietly with it: that drop is on record under
    # the entry's own key.
    keys = {entry["key"] for entry in checklist}
    unknown = [one for one in signals if one not in keys]
    if unknown:
        raise SchemaError(
            f"top_signals names {', '.join(unknown)}, which no checklist entry "
            "carries — a top signal that names no entry names nothing")
    return answer
