"""The one §7 checker, held against `docs/CHECKLIST.md` by hand and parsed.

`src/prediction_schema.py` is the single copy of §7's field lists, its three
closed value lists and its signal ceiling, and `check` is the one function that
applies them. The first five tests stood in the shuffled-report control's test
file until the owner retired that control on 2026-09-23; the file is kept, not
run, under `archive/controls/shuffled/`. The module
they judge did not retire with it -- the single-agent control calls it -- so
they moved here with their expected values unchanged, and only the lines that
asked the retired control's own constants came off. The refusals after them
were asserted in that file through the retired control's run; they are asked of
the checker directly now, with the same inputs and the same sentences.

Where the expected values come from
-----------------------------------

`docs/CHECKLIST.md` §7 read by hand, and §1 for the one list §7 leaves blank.
Not read off the control and not off `src/prediction_schema.py`: a list copied
out of the code it judges agrees with it by construction. The block, as the
document prints it:

  { "question": "accounting_reliability" | "financial_pressure",
    "rules_version": "0.1",
    "checklist": [ {"key": "", "finding": "", "confidence": 0,
                    "evidence": [{"upstream_item_id": ""}]} ],
    "continuous": [ {"key": "", "point": 0, "direction": "", "low": 0, "high": 0} ],
    "events": [ {"key": "", "p_within_horizon": 0} ],
    "explanations": [ {"id": "", "support": "sufficient|insufficient|unknown",
                       "realization_p": 0} ],
    "market_direction": {"p_up": 0, "basis": []},
    "tier": "elevated" | "watch" | "clear",
    "top_signals": [] }

Under it: "`continuous` is financial pressure only. `top_signals` holds at
most five keys." and "`p_up` may be `"insufficient"` instead of a number".
§1: "An LLM answer is always `flag` / `no_flag` / `insufficient`".

`test_the_section_seven_value_lists_are_the_documents_own` parses the same
values out of the document instead, so the day §7 moves and the hand reading
is not updated, the two disagree here rather than both going quietly stale.
"""

from __future__ import annotations

import ast
import json
import math
import re
from pathlib import Path

import pytest

from src import prediction_schema

REPO_ROOT = Path(__file__).resolve().parent.parent

BY_HAND_FIELDS = ("question", "rules_version", "checklist", "continuous", "events",
                  "explanations", "market_direction", "tier", "top_signals")
BY_HAND_QUESTIONS = ("accounting_reliability", "financial_pressure")
BY_HAND_CHECKLIST = ("key", "finding", "confidence", "evidence")
BY_HAND_EVIDENCE = ("upstream_item_id",)
BY_HAND_CONTINUOUS = ("key", "point", "direction", "low", "high")
BY_HAND_EVENTS = ("key", "p_within_horizon")
BY_HAND_EXPLANATIONS = ("id", "support", "realization_p")
BY_HAND_MARKET = ("p_up", "basis")
BY_HAND_FINDINGS = ("flag", "no_flag", "insufficient")
BY_HAND_SUPPORT = ("sufficient", "insufficient", "unknown")
BY_HAND_TIERS = ("elevated", "watch", "clear")
BY_HAND_SIGNAL_CEILING = 5

# Any name will do for an upstream item: the checker asks that an id is a name
# and resolves nothing, which is the caller's job. This one is the id the
# retired control's tests cited, kept so the answers below are the ones those
# tests put to the checker.
UPSTREAM_ITEM = "0001783180-26-000008:numbers_vs_market:1"

# Two answers written by hand in §7's shapes, `question` and `rules_version`
# left off because they are the caller's to settle. `continuous` is financial
# pressure only.
ACCOUNTING_ANSWER = {
    "checklist": [{"key": "receivables_growth_outruns_revenue", "finding": "flag",
                   "confidence": 0.6,
                   "evidence": [{"upstream_item_id": UPSTREAM_ITEM}]}],
    "events": [{"key": "restatement", "p_within_horizon": 0.1}],
    "explanations": [],
    "market_direction": {"p_up": 0.4, "basis": [UPSTREAM_ITEM]},
    "tier": "watch",
    "top_signals": ["receivables_growth_outruns_revenue"],
}
PRESSURE_ANSWER = {
    "checklist": [{"key": "liquidity_headroom", "finding": "no_flag", "confidence": 0.3,
                   "evidence": [{"upstream_item_id": UPSTREAM_ITEM}]}],
    "continuous": [{"key": "revenue_next_quarter", "point": 100.0,
                    "direction": "down", "low": 90.0, "high": 110.0}],
    "events": [{"key": "covenant_breach", "p_within_horizon": 0.05}],
    "explanations": [],
    "market_direction": {"p_up": "insufficient", "basis": []},
    "tier": "clear",
    "top_signals": [],
}
ANSWERS = {"accounting_reliability": ACCOUNTING_ANSWER,
           "financial_pressure": PRESSURE_ANSWER}


def test_the_one_checker_holds_what_section_seven_says():
    """The values the checker holds, against §7 as a person reads it.

    This stood as two controls' constants asserted equal to each other, which
    is a test standing in for a function: both could be wrong the same way and
    agree. There is one copy now, and it is held against the document.
    """
    assert prediction_schema.QUESTIONS == BY_HAND_QUESTIONS
    # `question` and `rules_version` are the run's, `continuous` is one
    # question's, and the rest is what every answer carries: nine between them.
    assert prediction_schema.RUN_KEYS == ("question", "rules_version")
    assert prediction_schema.CONTINUOUS == "continuous"
    assert prediction_schema.CONTINUOUS_QUESTION == "financial_pressure"
    assert sorted(prediction_schema.RUN_KEYS + prediction_schema.PREDICTED_KEYS
                  + (prediction_schema.CONTINUOUS,)) == sorted(BY_HAND_FIELDS)
    assert prediction_schema.CHECKLIST_FIELDS == BY_HAND_CHECKLIST
    assert prediction_schema.EVIDENCE_FIELDS == BY_HAND_EVIDENCE
    assert prediction_schema.CONTINUOUS_FIELDS == BY_HAND_CONTINUOUS
    assert prediction_schema.EVENT_FIELDS == BY_HAND_EVENTS
    assert prediction_schema.EXPLANATION_FIELDS == BY_HAND_EXPLANATIONS
    assert prediction_schema.MARKET_FIELDS == BY_HAND_MARKET
    assert prediction_schema.FINDINGS == BY_HAND_FINDINGS
    assert prediction_schema.SUPPORT == BY_HAND_SUPPORT
    assert prediction_schema.TIERS == BY_HAND_TIERS
    assert prediction_schema.TOP_SIGNALS_MAX == BY_HAND_SIGNAL_CEILING
    assert prediction_schema.INSUFFICIENT == "insufficient"


def schema_refuses(answer, question="accounting_reliability",
                   evidence=BY_HAND_EVIDENCE) -> str | None:
    """The one checker's refusal of an answer, or None when it stands."""
    try:
        prediction_schema.check(answer, question, evidence=evidence)
    except prediction_schema.SchemaError as refused:
        return str(refused)
    return None


def test_the_one_checker_takes_every_value_section_seven_allows_and_nothing_beside():
    """Equal constants are not a gate; what the function does with them is.

    Every value §7 and §1 allow stands, one at a time, and the first value
    beside them is refused -- so a list the checker holds and then never
    consults, or consults against the wrong field, turns this red.
    """
    good = dict(ACCOUNTING_ANSWER)
    assert schema_refuses(good) is None, "the good answer is the baseline"
    assert schema_refuses(dict(PRESSURE_ANSWER), "financial_pressure") is None

    # Two questions and no third. The control settles the question before it
    # calls the checker, so only a caller that did not is refused here -- and
    # without this an answer to a question §7 does not have is judged as
    # accounting reliability, the one that asks for no `continuous`.
    said = schema_refuses(good, "accounting")
    assert said is not None and "'accounting' is not a question" in said
    # And an answer that is an object. The control refuses anything else in its
    # own words first; a caller that did not would otherwise have a string's
    # letters read as its field names.
    for shaped in (["checklist"], "checklist events tier"):
        said = schema_refuses(shaped)
        assert said is not None and "not an object" in said, shaped

    entry = good["checklist"][0]
    for finding in BY_HAND_FINDINGS:
        assert schema_refuses(dict(good, checklist=[dict(entry, finding=finding)])) \
            is None, finding
    assert "finding" in schema_refuses(dict(good, checklist=[dict(entry, finding="yes")]))

    for support in BY_HAND_SUPPORT:
        explained = [{"id": UPSTREAM_ITEM, "support": support, "realization_p": 0.4}]
        assert schema_refuses(dict(good, explanations=explained)) is None, support
    assert "support" in schema_refuses(dict(good, explanations=[
        {"id": UPSTREAM_ITEM, "support": "maybe", "realization_p": 0.4}]))

    for tier in BY_HAND_TIERS:
        assert schema_refuses(dict(good, tier=tier)) is None, tier
    assert "tier" in schema_refuses(dict(good, tier="alert"))

    def signalled(count: int) -> dict:
        keys = [f"signal_{n}" for n in range(count)]
        return dict(good, checklist=[dict(entry, key=key) for key in keys],
                    top_signals=keys)
    assert schema_refuses(signalled(BY_HAND_SIGNAL_CEILING)) is None
    assert f"at most {BY_HAND_SIGNAL_CEILING}" in \
        schema_refuses(signalled(BY_HAND_SIGNAL_CEILING + 1))

    assert schema_refuses(dict(good, market_direction={
        "p_up": "insufficient", "basis": []})) is None
    assert "p_up" in schema_refuses(dict(good, market_direction={
        "p_up": "unsure", "basis": []}))

    # "`continuous` is financial pressure only": asked of one question,
    # refused on the other.
    assert "has no continuous" in schema_refuses(
        {key: value for key, value in PRESSURE_ANSWER.items() if key != "continuous"},
        "financial_pressure")
    assert "carries continuous" in schema_refuses(
        dict(good, continuous=PRESSURE_ANSWER["continuous"]))

    # A field of every nested object, taken away, is named.
    for field, broken in (
            ("confidence", dict(good, checklist=[
                {k: v for k, v in entry.items() if k != "confidence"}])),
            ("p_within_horizon", dict(good, events=[{"key": "restatement"}])),
            ("realization_p", dict(good, explanations=[
                {"id": UPSTREAM_ITEM, "support": "unknown"}])),
            ("basis", dict(good, market_direction={"p_up": 0.4})),
            ("high", dict(PRESSURE_ANSWER, continuous=[
                {k: v for k, v in PRESSURE_ANSWER["continuous"][0].items()
                 if k != "high"}]))):
        question = "financial_pressure" if "continuous" in broken else \
            "accounting_reliability"
        said = schema_refuses(broken, question)
        assert said is not None and field in said, field


def test_evidence_is_the_one_field_the_caller_names():
    """`evidence` is the argument, and it may add to §7's shape, never take
    from it.

    The single-agent control's upstream is the committed filing, so its ids
    name paragraphs and a quote travels with each; a caller whose upstream is
    reports has §7's own member as the whole of it.
    """
    plain = dict(ACCOUNTING_ANSWER)
    quoted = dict(plain, checklist=[dict(plain["checklist"][0], evidence=[
        {"upstream_item_id": UPSTREAM_ITEM, "quote": "a sentence"}])])
    with_quote = BY_HAND_EVIDENCE + ("quote",)

    assert schema_refuses(plain, evidence=BY_HAND_EVIDENCE) is None
    assert schema_refuses(quoted, evidence=with_quote) is None
    # Each shape is refused under the other's argument, naming the member.
    assert "quote" in schema_refuses(quoted, evidence=BY_HAND_EVIDENCE)
    assert "quote" in schema_refuses(plain, evidence=with_quote)
    # The member a caller adds is held to be a name like §7's own.
    blank = dict(plain, checklist=[dict(plain["checklist"][0], evidence=[
        {"upstream_item_id": UPSTREAM_ITEM, "quote": "  "}])])
    assert "evidence[1].quote" in schema_refuses(blank, evidence=with_quote)
    # An argument leaving out §7's own member is refused, whatever the answer.
    said = schema_refuses(quoted, evidence=("quote",))
    assert said is not None and "leaves out upstream_item_id" in said


def test_the_control_writes_out_no_section_seven_list_of_its_own():
    """The lists are written once, in `src/prediction_schema.py`.

    Read off the control's source rather than asked of its attributes: a copy
    under a new name is still a copy, and the next one to drift.
    """
    by_hand = {BY_HAND_CHECKLIST, BY_HAND_EVIDENCE, BY_HAND_CONTINUOUS,
               BY_HAND_EVENTS, BY_HAND_EXPLANATIONS, BY_HAND_MARKET,
               BY_HAND_FINDINGS, BY_HAND_SUPPORT, BY_HAND_TIERS}
    name = "control_single_agent.py"
    tree = ast.parse((REPO_ROOT / "src" / name).read_text(encoding="utf-8"))
    written = {tuple(element.value for element in node.elts)
               for node in ast.walk(tree)
               if isinstance(node, (ast.Tuple, ast.List)) and node.elts
               and all(isinstance(element, ast.Constant)
                       and isinstance(element.value, str)
                       for element in node.elts)}
    assert not written & by_hand, f"{name} writes out {sorted(written & by_hand)}"


def section_seven() -> dict:
    """§7's prediction schema, parsed out of `docs/CHECKLIST.md` as JSON.

    The block in the document is not JSON -- three fields give their values as
    `"a" | "b"` unions -- so each union is collapsed into the one `|`-joined
    string §7 already uses for `support`. Nothing else is rewritten, and a
    document whose §7 block stops being parseable fails here rather than
    quietly falling back to what the module says.
    """
    document = (REPO_ROOT / "docs" / "CHECKLIST.md").read_text(encoding="utf-8")
    heading = document.index("## 7. Output schemas")
    block = document.index("```json", heading) + len("```json")
    pseudo = document[block:document.index("```", block)]
    real = re.sub(r'"[^"\n]*"(?:\s*\|\s*"[^"\n]*")+',
                  lambda union: '"%s"' % "|".join(
                      found.strip('"') for found in re.findall(r'"[^"\n]*"', union.group(0))),
                  pseudo)
    return json.loads(real)


def test_the_section_seven_value_lists_are_the_documents_own():
    """The lists read off §7 itself, not off the module.

    The tests above hold the one checker against §7 as a person reads it. This
    one parses the document instead. Everything comes out of
    `docs/CHECKLIST.md`: the field sets out of §7's own block, the three closed
    value lists out of the strings inside it and out of §1's sentence, and the
    ceiling out of the prose under the block.
    """
    schema = section_seven()
    # The keys, in §7's order. `question` and `rules_version` are the caller's
    # own to write and `continuous` is asked of one question only, so those
    # three are named here rather than counted in.
    assert tuple(name for name in schema
                 if name not in prediction_schema.RUN_KEYS + (prediction_schema.CONTINUOUS,)
                 ) == prediction_schema.PREDICTED_KEYS
    assert tuple(name for name in schema if name in prediction_schema.RUN_KEYS) == \
        prediction_schema.RUN_KEYS
    assert prediction_schema.CONTINUOUS in schema
    assert tuple(schema["question"].split("|")) == prediction_schema.QUESTIONS

    # Every nested entry's closed field set, and the evidence inside the
    # checklist entry rather than beside it.
    assert tuple(schema["checklist"][0]) == prediction_schema.CHECKLIST_FIELDS
    assert tuple(schema["checklist"][0]["evidence"][0]) == \
        prediction_schema.EVIDENCE_FIELDS
    assert tuple(schema["continuous"][0]) == prediction_schema.CONTINUOUS_FIELDS
    assert tuple(schema["events"][0]) == prediction_schema.EVENT_FIELDS
    assert tuple(schema["explanations"][0]) == prediction_schema.EXPLANATION_FIELDS
    assert tuple(schema["market_direction"]) == prediction_schema.MARKET_FIELDS

    # The two closed lists §7 spells out inside the block, and the one it
    # leaves empty there: `"finding": ""` says nothing, so the findings are §1's
    # sentence, which is the only place the three are written down.
    assert tuple(schema["tier"].split("|")) == prediction_schema.TIERS
    assert tuple(schema["explanations"][0]["support"].split("|")) == \
        prediction_schema.SUPPORT
    collapsed = " ".join(
        (REPO_ROOT / "docs" / "CHECKLIST.md").read_text(encoding="utf-8").split())
    said = re.search(r"An LLM answer is always (.+?), plus a confidence", collapsed)
    assert said, "docs/CHECKLIST.md §1 no longer says what an LLM answer is"
    assert tuple(one.strip(" `") for one in said.group(1).split("/")) == \
        prediction_schema.FINDINGS

    # The ceiling and the abstention, out of the prose under the block.
    assert "`top_signals` holds at most five keys" in collapsed
    assert prediction_schema.TOP_SIGNALS_MAX == 5
    assert '`p_up` may be `"insufficient"` instead of a number' in collapsed
    assert prediction_schema.INSUFFICIENT == "insufficient"


# --- the rules the retired control's run path was the only judge of -----------
#
# Every refusal below was asserted in the retired control's test file through
# that control's run, and nowhere else. Turning each rule of `check` off in turn
# -- an `if` guarding a refusal made false, a helper call made a passthrough --
# found thirty-one that `tests/test_control_single_agent.py` and the five tests
# above leave green once that file is archived. Each is asked of the checker
# directly here, with the input the retired test built and the sentence it
# asserted. The single-agent control reaches the same rules through its own
# run; these are the direct callers a shared function needs.


def refusal(answer, question) -> str:
    """The checker's sentence for an answer it has to refuse."""
    with pytest.raises(prediction_schema.SchemaError) as caught:
        prediction_schema.check(answer, question, evidence=BY_HAND_EVIDENCE)
    return str(caught.value)


@pytest.mark.parametrize("question", list(ANSWERS))
@pytest.mark.parametrize("missing", ["checklist", "market_direction", "tier"])
def test_an_answer_short_of_the_schema_is_refused(question, missing):
    short = {key: value for key, value in ANSWERS[question].items() if key != missing}
    said = refusal(short, question)
    assert f"the {question} answer has no {missing}" in said


def test_accounting_reliability_carrying_continuous_is_refused_in_its_own_words():
    """The closed-prediction check would refuse this too, as a field §7 does not
    have -- which is not what is wrong with it: §7 has it, for the other
    question. "carries continuous" is in both sentences, so the assertion is
    the one only the right rule writes."""
    said = refusal(dict(ACCOUNTING_ANSWER, continuous=PRESSURE_ANSWER["continuous"]),
                   "accounting_reliability")
    assert "carries continuous" in said
    assert "gives to financial pressure alone" in said


def test_the_prediction_object_is_closed():
    said = refusal(dict(ACCOUNTING_ANSWER, scored_filing_date="2030-01-01",
                        price_on_reaction_day_60=412.77,
                        note_to_the_scorer="merge this into the pipeline number"),
                   "accounting_reliability")
    for stray in ("note_to_the_scorer", "price_on_reaction_day_60",
                  "scored_filing_date"):
        assert stray in said
    assert "does not give an answer" in said


@pytest.mark.parametrize("question, field, answer", [
    ("accounting_reliability", "checklist",
     dict(ACCOUNTING_ANSWER, checklist="two flags")),
    ("accounting_reliability", "checklist[1].evidence",
     dict(ACCOUNTING_ANSWER,
          checklist=[dict(ACCOUNTING_ANSWER["checklist"][0],
                          evidence="the crossed item")])),
    ("financial_pressure", "continuous",
     dict(PRESSURE_ANSWER, continuous="revenue down")),
    ("accounting_reliability", "events",
     dict(ACCOUNTING_ANSWER, events="lots")),
    ("accounting_reliability", "explanations",
     dict(ACCOUNTING_ANSWER, explanations="none this time")),
    ("accounting_reliability", "top_signals",
     dict(ACCOUNTING_ANSWER, top_signals="receivables_growth_outruns_revenue")),
])
def test_a_field_the_schema_gives_as_a_list_is_refused_when_it_is_not_one(
        question, field, answer):
    """A string is a sequence, so a string reaching any of these is the answer
    iterated letter by letter and refused by the next rule, about a letter. The
    assertion is `_a_list`'s own sentence, which is the only thing a
    passthrough removes."""
    said = refusal(answer, question)
    assert f"the {question} answer gives {field} as str" in said
    assert "docs/CHECKLIST.md §7 gives it as a list" in said


@pytest.mark.parametrize("question, field, entry", [
    ("accounting_reliability", "checklist", "x"),
    ("accounting_reliability", "events", 3),
    ("accounting_reliability", "explanations", None),
    ("financial_pressure", "continuous", ["revenue_next_quarter"]),
])
def test_a_nested_entry_that_is_not_an_object_is_refused(question, field, entry):
    said = refusal(dict(ANSWERS[question], **{field: [entry]}), question)
    assert f"{field}[1] is {type(entry).__name__}, not an object" in said


@pytest.mark.parametrize("question,field,entries", [
    ("accounting_reliability", "checklist",
     [dict(ACCOUNTING_ANSWER["checklist"][0], note="see above")]),
    ("accounting_reliability", "events",
     [dict(ACCOUNTING_ANSWER["events"][0], note="see above")]),
    ("accounting_reliability", "explanations",
     [{"id": UPSTREAM_ITEM, "support": "sufficient", "realization_p": 0.4,
       "note": "see above"}]),
    ("financial_pressure", "continuous",
     [dict(PRESSURE_ANSWER["continuous"][0], note="see above")]),
])
def test_a_stray_field_on_a_nested_entry_is_refused(question, field, entries):
    """The prediction object is closed and so is every entry inside it."""
    said = refusal(dict(ANSWERS[question], **{field: entries}), question)
    assert f"{field}[1] carries" in said
    assert "note" in said
    assert "docs/CHECKLIST.md §7 gives it" in said


@pytest.mark.parametrize("shape", [0.7, "up", [0.7], {"p_up": 0.7},
                                   {"p_up": 0.7, "basis": [], "extra": 1}])
def test_a_market_direction_that_is_not_the_schemas_shape_is_refused(shape):
    """A bare probability is not an abstention, and a basis is what a market
    call's citations are read from."""
    said = refusal(dict(ACCOUNTING_ANSWER, market_direction=shape),
                   "accounting_reliability")
    assert said.startswith("market_direction ")


@pytest.mark.parametrize("p_up", ["up", "0.7", 1.7, -0.1, True, None])
def test_a_market_probability_that_is_not_one_is_refused(p_up):
    """§7 gives `p_up` a number in zero to one, or the word `insufficient`.
    `True` is in the list because Python calls it an `int` and `0 <= True <= 1`."""
    said = refusal(dict(ACCOUNTING_ANSWER,
                        market_direction={"p_up": p_up, "basis": [UPSTREAM_ITEM]}),
                   "accounting_reliability")
    assert "market_direction.p_up" in said


@pytest.mark.parametrize("basis", [UPSTREAM_ITEM, [""], ["  "], [UPSTREAM_ITEM, 7],
                                   {"0": UPSTREAM_ITEM}])
def test_a_basis_that_is_not_a_list_of_names_is_refused(basis):
    """An entry that is not a name resolves for nobody -- and a bare string is
    fifty-odd single characters, none of which is an item id."""
    said = refusal(dict(ACCOUNTING_ANSWER,
                        market_direction={"p_up": 0.4, "basis": basis}),
                   "accounting_reliability")
    assert "market_direction.basis is" in said
    assert "a list of the ids the probability rests on" in said


@pytest.mark.parametrize("key", ["", "   ", None, 3, ["a"]])
@pytest.mark.parametrize("question,field", [
    ("accounting_reliability", "checklist"),
    ("accounting_reliability", "events"),
    ("financial_pressure", "continuous"),
])
def test_an_entry_naming_no_key_is_refused(question, field, key):
    """One indicator, one key -- and a key that is not a name names nothing."""
    answer = dict(ANSWERS[question],
                  **{field: [dict(ANSWERS[question][field][0], key=key)]})
    said = refusal(answer, question)
    assert f"{field}[1].key" in said
    assert "the schema gives it a name" in said


@pytest.mark.parametrize("named", ["", "   ", None, 3])
def test_an_explanation_naming_no_id_is_refused(named):
    said = refusal(dict(ACCOUNTING_ANSWER, explanations=[
        {"id": named, "support": "sufficient", "realization_p": 0.4}]),
        "accounting_reliability")
    assert "explanations[1].id" in said
    assert "the schema gives it a name" in said


@pytest.mark.parametrize("direction", ["", "   ", None, 3])
def test_a_continuous_entry_naming_no_direction_is_refused(direction):
    """§7 gives `direction` a string and does not enumerate its values, so a
    name is the whole of what this rule can ask."""
    said = refusal(dict(PRESSURE_ANSWER, continuous=[
        dict(PRESSURE_ANSWER["continuous"][0], direction=direction)]),
        "financial_pressure")
    assert "continuous[1].direction" in said
    assert "the schema gives it a name" in said


@pytest.mark.parametrize("chance", [1.4, -0.1, "likely", None, True])
def test_a_realization_probability_that_is_not_one_is_refused(chance):
    said = refusal(dict(ACCOUNTING_ANSWER, explanations=[
        {"id": UPSTREAM_ITEM, "support": "sufficient", "realization_p": chance}]),
        "accounting_reliability")
    assert "explanations[1].realization_p" in said


@pytest.mark.parametrize("field", ["point", "low", "high"])
@pytest.mark.parametrize("value", [math.nan, math.inf])
def test_a_continuous_number_json_cannot_carry_is_refused(field, value):
    """`json.dumps` spells these `NaN` and `Infinity`, which are not JSON, and
    `point`, `low` and `high` have no range to catch them. A `nan` compares
    false against everything, so without this rule the range rule refused it
    with the wrong sentence."""
    said = refusal(dict(PRESSURE_ANSWER, continuous=[
        dict(PRESSURE_ANSWER["continuous"][0], **{field: value})]),
        "financial_pressure")
    assert f"continuous[1].{field}" in said
    assert "not JSON" in said


def test_two_continuous_entries_under_one_key_are_refused():
    entry = PRESSURE_ANSWER["continuous"][0]
    said = refusal(dict(PRESSURE_ANSWER,
                        continuous=[entry, dict(entry, point=250.0, high=300.0)]),
                   "financial_pressure")
    assert "revenue_next_quarter" in said
    assert "more than once" in said


def test_two_events_under_one_key_are_refused():
    entry = ACCOUNTING_ANSWER["events"][0]
    said = refusal(dict(ACCOUNTING_ANSWER,
                        events=[entry, dict(entry, p_within_horizon=0.9)]),
                   "accounting_reliability")
    assert "restatement" in said
    assert "more than once" in said


def test_two_explanations_under_one_id_are_refused():
    entry = {"id": UPSTREAM_ITEM, "support": "sufficient", "realization_p": 0.4}
    said = refusal(dict(ACCOUNTING_ANSWER,
                        explanations=[entry, dict(entry, support="unknown")]),
                   "accounting_reliability")
    assert said.startswith("explanations names")
    assert "more than once" in said


def test_one_signal_repeated_is_refused():
    """Two of one key, not six: at six the ceiling answers first, so only
    uniqueness can refuse this."""
    said = refusal(dict(ACCOUNTING_ANSWER,
                        top_signals=["receivables_growth_outruns_revenue"] * 2),
                   "accounting_reliability")
    assert "more than once" in said
    assert "receivables_growth_outruns_revenue" in said


@pytest.mark.parametrize("signal", [3, None, ["receivables_growth_outruns_revenue"], ""])
def test_a_top_signal_that_is_not_a_name_is_refused(signal):
    """A signal is the key of a checklist entry, so it is a name."""
    said = refusal(dict(ACCOUNTING_ANSWER, top_signals=[signal]),
                   "accounting_reliability")
    assert "top_signals[1] is" in said
    assert "a signal is the key of a checklist entry" in said


# Six more the single-agent control's run judges and nothing above did, asked
# directly for the same reason: a shared function's rules need a caller that is
# not the control. With these, every one of the fifty-five rules the same sweep
# enumerates goes red with this file alone.


def test_a_signal_naming_no_checklist_entry_is_refused():
    """The answer contradicting itself before any citation is resolved."""
    said = refusal(dict(ACCOUNTING_ANSWER,
                        top_signals=["receivables_growth_outruns_revenue",
                                     "margin_collapse"]),
                   "accounting_reliability")
    assert "margin_collapse" in said
    assert "which no checklist entry carries" in said


def test_an_empty_continuous_is_refused():
    """Financial pressure predicts next quarter's three numbers; an empty list
    is the field present and the prediction absent."""
    said = refusal(dict(PRESSURE_ANSWER, continuous=[]), "financial_pressure")
    assert said.startswith("continuous is empty")


def test_two_checklist_entries_under_one_key_are_refused():
    """One indicator, one key: two entries under one key is a set, and the
    scorer reading the first would score whichever came back first."""
    entry = ACCOUNTING_ANSWER["checklist"][0]
    said = refusal(dict(ACCOUNTING_ANSWER,
                        checklist=[entry, dict(entry, finding="no_flag")]),
                   "accounting_reliability")
    assert said.startswith("checklist names receivables_growth_outruns_revenue")
    assert "more than once" in said


@pytest.mark.parametrize("confidence", [1.4, -0.2, "high", None, True])
def test_a_confidence_that_is_not_a_probability_is_refused(confidence):
    said = refusal(dict(ACCOUNTING_ANSWER, checklist=[
        dict(ACCOUNTING_ANSWER["checklist"][0], confidence=confidence)]),
        "accounting_reliability")
    assert "checklist[1].confidence" in said


@pytest.mark.parametrize("chance", [1.4, -0.1, "likely", None, True])
def test_an_event_probability_that_is_not_one_is_refused(chance):
    """§8 scores events by Brier, and Brier of `"likely"` is not a number."""
    said = refusal(dict(ACCOUNTING_ANSWER, events=[
        {"key": "restatement", "p_within_horizon": chance}]),
        "accounting_reliability")
    assert "events[1].p_within_horizon" in said


def test_a_continuous_point_outside_its_own_range_is_refused():
    """A point outside the interval it came with is two numbers that cannot
    both be the same prediction."""
    said = refusal(dict(PRESSURE_ANSWER, continuous=[
        dict(PRESSURE_ANSWER["continuous"][0], point=200.0)]), "financial_pressure")
    assert "outside its own range" in said
