"""The anomaly register, judged against the owner's words and against §7.

Two sources, and neither of them is `src/prediction_schema.py`.

**The owner's decision of 2026-09-23 is the answer key for the register.** In
the owner's words: "규칙 버전 1: 은 회계 지표가 4개 이상 ~ 이런걸 내가 원한게
아니라 회계 이상이 나온걸 모조리 찾는게 내 목표다" -- the goal is to find every
anomaly, not to count flags against a cutoff. The brief that carried it named
the register's fields and their values, and they are typed in below by hand:
`name`, `axis`, `what`, `numbers_vs_prose`, `evidence`, `market_label`; an
`axis` of `accounting_reliability` or `financial_pressure`; `confirms`,
`contradicts` or `unresolved`; `priced_in`, `not_priced`, `opposite_direction`
or `absent`; and `tier` and `top_signals` gone.

**`docs/CHECKLIST.md` §7 is the answer key for everything else, and it is
parsed rather than remembered.** The block is read out of the document and
held against the hand lists, so the day the document moves and this file does
not, the two disagree here. Every field set and closed list of §7 is held here,
not only the register's, so this file is the whole of §7's judge on its own.

Every planted answer is written out in this file. None of them is anything the
checker produced.
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
CHECKLIST = REPO_ROOT / "docs" / "CHECKLIST.md"

# --- the owner's words, typed in by hand -------------------------------------

BY_HAND_FIELDS = ("question", "rules_version", "checklist", "continuous", "events",
                  "explanations", "market_direction", "anomalies")
BY_HAND_ANOMALY = ("name", "axis", "what", "numbers_vs_prose", "evidence",
                   "market_label")
BY_HAND_AXES = ("accounting_reliability", "financial_pressure")
BY_HAND_NUMBERS_VS_PROSE = ("confirms", "contradicts", "unresolved")
BY_HAND_MARKET_LABELS = ("priced_in", "not_priced", "opposite_direction", "absent")
REMOVED = ("tier", "top_signals")

# --- §7 as a person reads it, for the fields the register did not touch ------
#
# Transcribed from the block, and §1 for the one list §7 leaves blank:
# "An LLM answer is always `flag` / `no_flag` / `insufficient`".
BY_HAND_QUESTIONS = ("accounting_reliability", "financial_pressure")
BY_HAND_CHECKLIST = ("key", "finding", "confidence", "evidence")
BY_HAND_EVIDENCE = ("upstream_item_id",)
BY_HAND_CONTINUOUS = ("key", "point", "direction", "low", "high")
BY_HAND_EVENTS = ("key", "p_within_horizon")
BY_HAND_EXPLANATIONS = ("id", "support", "realization_p")
BY_HAND_MARKET = ("p_up", "basis")
BY_HAND_FINDINGS = ("flag", "no_flag", "insufficient")
BY_HAND_SUPPORT = ("sufficient", "insufficient", "unknown")

# One upstream item id, the shape a supervisor cites.
ITEM = "0000320193-25-000079:notes:receivables:1"


def anomaly(**change) -> dict:
    """One register entry on the accounting axis, every field the owner named."""
    return {"name": "revenue_receivables_outrun_sales",
            "axis": "accounting_reliability",
            "what": "receivables grew three times as fast as revenue",
            "numbers_vs_prose": "contradicts",
            "evidence": [{"upstream_item_id": ITEM}],
            "market_label": "not_priced"} | change


def accounting(**change) -> dict:
    """An accounting answer without the two fields the run settles."""
    return {"checklist": [{"key": "receivables_outrun_revenue", "finding": "flag",
                           "confidence": 0.6,
                           "evidence": [{"upstream_item_id": ITEM}]}],
            "events": [{"key": "restatement", "p_within_horizon": 0.1}],
            "explanations": [],
            "market_direction": {"p_up": 0.4, "basis": [ITEM]},
            "anomalies": [anomaly()]} | change


def pressure(**change) -> dict:
    """A pressure answer: `continuous` is financial pressure only."""
    return {"checklist": [],
            "continuous": [{"key": "operating_margin", "point": 0.2,
                            "direction": "down", "low": 0.1, "high": 0.3}],
            "events": [],
            "explanations": [],
            "market_direction": {"p_up": "insufficient", "basis": []},
            "anomalies": [anomaly(name="liquidity_cash_runway_short",
                                  axis="financial_pressure",
                                  numbers_vs_prose="unresolved",
                                  market_label="absent")]} | change


def refusal(answer, question="accounting_reliability",
            evidence=BY_HAND_EVIDENCE) -> str | None:
    """The checker's refusal of an answer, or None when it stands."""
    try:
        prediction_schema.check(answer, question, evidence=evidence)
    except prediction_schema.SchemaError as refused:
        return str(refused)
    return None


def section_seven() -> dict:
    """§7's prediction schema, parsed out of `docs/CHECKLIST.md` as JSON.

    The block is not JSON: the fields with a closed list write it as a
    `"a" | "b"` union. Each union is collapsed into the one `|`-joined string
    §7 already uses for `support`, and nothing else is rewritten, so a block
    that stops being parseable fails here rather than falling back to anything.
    """
    document = CHECKLIST.read_text(encoding="utf-8")
    heading = document.index("## 7. Output schemas")
    start = document.index("```json", heading) + len("```json")
    pseudo = document[start:document.index("```", start)]
    real = re.sub(r'"[^"\n]*"(?:\s*\|\s*"[^"\n]*")+',
                  lambda union: '"%s"' % "|".join(
                      one.strip('"') for one in re.findall(r'"[^"\n]*"', union.group(0))),
                  pseudo)
    return json.loads(real)


def collapsed_checklist() -> str:
    return " ".join(CHECKLIST.read_text(encoding="utf-8").split())


# --- the owner's words against the document and the checker ------------------


def test_the_register_is_the_owners_in_the_document_and_in_the_checker():
    schema = section_seven()
    entry = schema["anomalies"][0]
    assert tuple(entry) == BY_HAND_ANOMALY
    assert tuple(entry["axis"].split("|")) == BY_HAND_AXES
    assert tuple(entry["numbers_vs_prose"].split("|")) == BY_HAND_NUMBERS_VS_PROSE
    assert tuple(entry["market_label"].split("|")) == BY_HAND_MARKET_LABELS
    # An anomaly's evidence is §7's evidence shape, the checklist's own.
    assert tuple(entry["evidence"][0]) == BY_HAND_EVIDENCE

    assert prediction_schema.ANOMALY_FIELDS == BY_HAND_ANOMALY
    assert prediction_schema.AXES == BY_HAND_AXES
    assert prediction_schema.NUMBERS_VS_PROSE == BY_HAND_NUMBERS_VS_PROSE
    assert prediction_schema.MARKET_LABELS == BY_HAND_MARKET_LABELS


def test_section_seven_has_every_field_the_owner_kept_and_neither_one_removed():
    schema = section_seven()
    assert tuple(schema) == BY_HAND_FIELDS
    for gone in REMOVED:
        assert gone not in schema
    # The checker's own split of those fields: two the run settles, one that is
    # financial pressure's alone, and the rest every answer carries.
    assert prediction_schema.RUN_KEYS == ("question", "rules_version")
    assert prediction_schema.CONTINUOUS == "continuous"
    assert prediction_schema.PREDICTED_KEYS == tuple(
        name for name in BY_HAND_FIELDS
        if name not in ("question", "rules_version", "continuous"))
    for gone in ("TIERS", "TOP_SIGNALS_MAX"):
        assert not hasattr(prediction_schema, gone), gone


def test_the_rest_of_section_seven_is_the_documents_own():
    """Every other field set and closed list, parsed, against the hand reading."""
    schema = section_seven()
    assert tuple(schema["question"].split("|")) == BY_HAND_QUESTIONS
    assert tuple(schema["checklist"][0]) == BY_HAND_CHECKLIST
    assert tuple(schema["checklist"][0]["evidence"][0]) == BY_HAND_EVIDENCE
    assert tuple(schema["continuous"][0]) == BY_HAND_CONTINUOUS
    assert tuple(schema["events"][0]) == BY_HAND_EVENTS
    assert tuple(schema["explanations"][0]) == BY_HAND_EXPLANATIONS
    assert tuple(schema["explanations"][0]["support"].split("|")) == BY_HAND_SUPPORT
    assert tuple(schema["market_direction"]) == BY_HAND_MARKET
    said = re.search(r"An LLM answer is always (.+?), plus a confidence",
                     collapsed_checklist())
    assert said, "docs/CHECKLIST.md §1 no longer says what an LLM answer is"
    assert tuple(one.strip(" `") for one in said.group(1).split("/")) == BY_HAND_FINDINGS

    assert prediction_schema.QUESTIONS == BY_HAND_QUESTIONS
    assert prediction_schema.CHECKLIST_FIELDS == BY_HAND_CHECKLIST
    assert prediction_schema.EVIDENCE_FIELDS == BY_HAND_EVIDENCE
    assert prediction_schema.CONTINUOUS_FIELDS == BY_HAND_CONTINUOUS
    assert prediction_schema.EVENT_FIELDS == BY_HAND_EVENTS
    assert prediction_schema.EXPLANATION_FIELDS == BY_HAND_EXPLANATIONS
    assert prediction_schema.MARKET_FIELDS == BY_HAND_MARKET
    assert prediction_schema.FINDINGS == BY_HAND_FINDINGS
    assert prediction_schema.SUPPORT == BY_HAND_SUPPORT
    assert '`p_up` may be `"insufficient"` instead of a number' in collapsed_checklist()
    assert prediction_schema.INSUFFICIENT == "insufficient"


def test_the_control_writes_out_no_section_seven_list_of_its_own():
    """The lists are written once, in `src/prediction_schema.py`.

    Read off the control's source rather than asked of its attributes: a copy
    under a new name is still a copy, and the next one to drift. Moved here
    from the shuffled control's tests with the register's lists added to it;
    the shuffled control is retired to `archive/controls/shuffled/`, so the
    single-agent control is the one source left to read.
    """
    by_hand = {BY_HAND_CHECKLIST, BY_HAND_EVIDENCE, BY_HAND_CONTINUOUS,
               BY_HAND_EVENTS, BY_HAND_EXPLANATIONS, BY_HAND_MARKET,
               BY_HAND_FINDINGS, BY_HAND_SUPPORT, BY_HAND_ANOMALY, BY_HAND_AXES,
               BY_HAND_NUMBERS_VS_PROSE, BY_HAND_MARKET_LABELS}
    name = "control_single_agent.py"
    tree = ast.parse((REPO_ROOT / "src" / name).read_text(encoding="utf-8"))
    written = {tuple(element.value for element in node.elts)
               for node in ast.walk(tree)
               if isinstance(node, (ast.Tuple, ast.List)) and node.elts
               and all(isinstance(element, ast.Constant)
                       and isinstance(element.value, str)
                       for element in node.elts)}
    assert not written & by_hand, f"{name} writes out {sorted(written & by_hand)}"


def test_the_checklist_no_longer_turns_a_flag_count_into_a_verdict():
    """The two lines the owner's decision removes, and the ceiling beside them."""
    text = collapsed_checklist()
    for removed in ("4 or more of the 33 flags", "3 or more of the 17 flags",
                    "`top_signals` holds at most five keys",
                    '"tier": "elevated" | "watch" | "clear"'):
        assert removed not in text, removed
    # And what goes in their place: the cross-tabulation is descriptive now.
    assert "descriptive table with no count cut" in text


@pytest.mark.parametrize("prompt, axis", [
    ("supervisor-accounting.md", "accounting_reliability"),
    ("supervisor-pressure.md", "financial_pressure")])
def test_each_supervisor_writes_the_register_on_its_own_axis(prompt, axis):
    """The two supervisors write §7, so each prompt names every field of the
    register and every closed value, pins its own axis, says an empty register
    is an honest answer -- and says nothing of a tier any more."""
    text = " ".join((REPO_ROOT / ".claude" / "agents" / prompt)
                    .read_text(encoding="utf-8").split())
    for word in (BY_HAND_ANOMALY + BY_HAND_NUMBERS_VS_PROSE + BY_HAND_MARKET_LABELS):
        assert f"`{word}`" in text, word
    assert f"`axis` — `{axis}`, always" in text
    assert "An empty `anomalies` list is an allowed, honest answer" in text
    for gone in REMOVED + ("clear",):
        assert f"`{gone}`" not in text, gone


# --- what the checker does with the register ---------------------------------


def test_the_planted_answers_stand():
    """The baseline every refusal below departs from by one field."""
    assert refusal(accounting()) is None
    assert refusal(pressure(), "financial_pressure") is None


@pytest.mark.parametrize("field, value", [
    ("tier", "watch"), ("tier", "clear"), ("top_signals", []),
    ("top_signals", ["receivables_outrun_revenue"])])
def test_an_answer_carrying_a_removed_field_is_refused(field, value):
    said = refusal(accounting() | {field: value})
    assert said is not None and field in said
    assert "does not give an answer" in said


def test_an_anomaly_whose_market_label_is_absent_is_listed_and_stands():
    """"An anomaly with no market label is still listed (`absent`)."""
    answer = accounting(anomalies=[anomaly(market_label="absent")])
    assert refusal(answer) is None


@pytest.mark.parametrize("word", ["agrees", "confirmed", "Confirms", "", None, 1])
def test_an_anomaly_with_an_unknown_numbers_vs_prose_is_refused(word):
    said = refusal(accounting(anomalies=[anomaly(numbers_vs_prose=word)]))
    assert said is not None and "anomalies[1].numbers_vs_prose" in said


@pytest.mark.parametrize("label", ["unpriced", "Priced_in", "", None])
def test_an_anomaly_with_an_unknown_market_label_is_refused(label):
    said = refusal(accounting(anomalies=[anomaly(market_label=label)]))
    assert said is not None and "anomalies[1].market_label" in said


def test_every_value_the_owner_named_stands():
    for word in BY_HAND_NUMBERS_VS_PROSE:
        assert refusal(accounting(anomalies=[anomaly(numbers_vs_prose=word)])) \
            is None, word
    for label in BY_HAND_MARKET_LABELS:
        assert refusal(accounting(anomalies=[anomaly(market_label=label)])) \
            is None, label


def test_an_empty_register_is_an_honest_answer():
    assert refusal(accounting(anomalies=[])) is None
    assert refusal(pressure(anomalies=[]), "financial_pressure") is None


def test_an_answer_with_no_register_is_refused():
    answer = accounting()
    del answer["anomalies"]
    said = refusal(answer)
    assert said is not None and "has no anomalies" in said


@pytest.mark.parametrize("value", ["none", {"name": "x"}, 3, None])
def test_a_register_that_is_not_a_list_is_refused(value):
    said = refusal(accounting(anomalies=value))
    assert said is not None and "gives anomalies as" in said


@pytest.mark.parametrize("question, axis", [
    ("accounting_reliability", "financial_pressure"),
    ("financial_pressure", "accounting_reliability")])
def test_an_anomaly_on_the_other_axis_is_refused(question, axis):
    """Each supervisor lists the anomalies on its own axis, and the two are
    never merged."""
    answer = accounting() if question == "accounting_reliability" else pressure()
    answer["anomalies"] = [anomaly(axis=axis)]
    said = refusal(answer, question)
    assert said is not None and "anomalies[1].axis" in said
    assert "never merged" in said


@pytest.mark.parametrize("axis", ["accounting", "", None])
def test_an_axis_outside_the_two_is_refused(axis):
    said = refusal(accounting(anomalies=[anomaly(axis=axis)]))
    assert said is not None and "anomalies[1].axis" in said


@pytest.mark.parametrize("name", [
    "receivables",                        # an area and nothing after it
    "Revenue_receivables_outrun_sales",   # a capital
    "revenue-receivables-outrun-sales",   # dashes
    "revenue receivables outrun sales",   # spaces
    "revenue_receivables_outrun_sales_2",  # a digit
    "_revenue_receivables",               # no area in front
    "revenue__receivables",               # an empty word
    "revenue_receivables_",               # a trailing underscore
    "", None, 7])
def test_an_anomaly_name_that_is_not_a_plain_descriptive_name_is_refused(name):
    said = refusal(accounting(anomalies=[anomaly(name=name)]))
    assert said is not None and "anomalies[1].name" in said


def test_two_anomalies_under_one_name_are_refused():
    said = refusal(accounting(anomalies=[anomaly(), anomaly(what="another reading")]))
    assert said is not None and "more than once" in said
    assert "revenue_receivables_outrun_sales" in said


@pytest.mark.parametrize("change", [
    lambda entry: entry.pop("what"),
    lambda entry: entry.pop("market_label"),
    lambda entry: entry.__setitem__("tier", "watch"),
    lambda entry: entry.__setitem__("rank", 1)])
def test_an_anomaly_is_a_closed_object(change):
    entry = anomaly()
    change(entry)
    said = refusal(accounting(anomalies=[entry]))
    assert said is not None and "anomalies[1]" in said


@pytest.mark.parametrize("what", ["", "   ", None, 3])
def test_an_anomaly_that_says_nothing_is_refused(what):
    said = refusal(accounting(anomalies=[anomaly(what=what)]))
    assert said is not None and "anomalies[1].what" in said


def test_an_anomalys_evidence_is_the_callers_evidence_shape():
    """The same argument the checklist's evidence takes: §7's member, and what
    the caller's upstream adds beside it -- the single-agent control's quote."""
    with_quote = BY_HAND_EVIDENCE + ("quote",)
    quoted = accounting(
        checklist=[],
        anomalies=[anomaly(evidence=[{"upstream_item_id": ITEM,
                                      "quote": "a sentence"}])])
    assert refusal(quoted, evidence=with_quote) is None
    assert "anomalies[1].evidence[1]" in refusal(quoted)
    plain = accounting(checklist=[])
    assert "anomalies[1].evidence[1]" in refusal(plain, evidence=with_quote)
    for broken in ("an id", [ITEM], [{"upstream_item_id": ""}]):
        said = refusal(accounting(anomalies=[anomaly(evidence=broken)]))
        assert said is not None and "anomalies[1].evidence" in said, broken


# --- the refusals the retired shuffled control's tests asserted ---------------
#
# The five tests above this line in the retired control's file, and the
# refusals below, stood in `tests/test_control_shuffled.py` until the owner
# retired that control on 2026-09-23. They were ported here to call the checker
# directly. The planted answers carry an empty register where they carried a
# tier and top signals, and the tests that asserted the tier and the top
# signals are gone with the rule they encoded, as the register change named.

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
    "anomalies": [],
}
PRESSURE_ANSWER = {
    "checklist": [{"key": "liquidity_headroom", "finding": "no_flag", "confidence": 0.3,
                   "evidence": [{"upstream_item_id": UPSTREAM_ITEM}]}],
    "continuous": [{"key": "revenue_next_quarter", "point": 100.0,
                    "direction": "down", "low": 90.0, "high": 110.0}],
    "events": [{"key": "covenant_breach", "p_within_horizon": 0.05}],
    "explanations": [],
    "market_direction": {"p_up": "insufficient", "basis": []},
    "anomalies": [],
}
ANSWERS = {"accounting_reliability": ACCOUNTING_ANSWER,
           "financial_pressure": PRESSURE_ANSWER}


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
    for shaped in (["checklist"], "checklist events anomalies"):
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


def refused_with(answer, question) -> str:
    """The checker's sentence for an answer it has to refuse."""
    with pytest.raises(prediction_schema.SchemaError) as caught:
        prediction_schema.check(answer, question, evidence=BY_HAND_EVIDENCE)
    return str(caught.value)


@pytest.mark.parametrize("question", list(ANSWERS))
@pytest.mark.parametrize("missing", ["checklist", "market_direction"])
def test_an_answer_short_of_the_schema_is_refused(question, missing):
    short = {key: value for key, value in ANSWERS[question].items() if key != missing}
    said = refused_with(short, question)
    assert f"the {question} answer has no {missing}" in said


def test_accounting_reliability_carrying_continuous_is_refused_in_its_own_words():
    """The closed-prediction check would refuse this too, as a field §7 does not
    have -- which is not what is wrong with it: §7 has it, for the other
    question. "carries continuous" is in both sentences, so the assertion is
    the one only the right rule writes."""
    said = refused_with(dict(ACCOUNTING_ANSWER, continuous=PRESSURE_ANSWER["continuous"]),
                   "accounting_reliability")
    assert "carries continuous" in said
    assert "gives to financial pressure alone" in said


def test_the_prediction_object_is_closed():
    said = refused_with(dict(ACCOUNTING_ANSWER, scored_filing_date="2030-01-01",
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
])
def test_a_field_the_schema_gives_as_a_list_is_refused_when_it_is_not_one(
        question, field, answer):
    """A string is a sequence, so a string reaching any of these is the answer
    iterated letter by letter and refused by the next rule, about a letter. The
    assertion is `_a_list`'s own sentence, which is the only thing a
    passthrough removes."""
    said = refused_with(answer, question)
    assert f"the {question} answer gives {field} as str" in said
    assert "docs/CHECKLIST.md §7 gives it as a list" in said


@pytest.mark.parametrize("question, field, entry", [
    ("accounting_reliability", "checklist", "x"),
    ("accounting_reliability", "events", 3),
    ("accounting_reliability", "explanations", None),
    ("financial_pressure", "continuous", ["revenue_next_quarter"]),
])
def test_a_nested_entry_that_is_not_an_object_is_refused(question, field, entry):
    said = refused_with(dict(ANSWERS[question], **{field: [entry]}), question)
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
    said = refused_with(dict(ANSWERS[question], **{field: entries}), question)
    assert f"{field}[1] carries" in said
    assert "note" in said
    assert "docs/CHECKLIST.md §7 gives it" in said


@pytest.mark.parametrize("shape", [0.7, "up", [0.7], {"p_up": 0.7},
                                   {"p_up": 0.7, "basis": [], "extra": 1}])
def test_a_market_direction_that_is_not_the_schemas_shape_is_refused(shape):
    """A bare probability is not an abstention, and a basis is what a market
    call's citations are read from."""
    said = refused_with(dict(ACCOUNTING_ANSWER, market_direction=shape),
                   "accounting_reliability")
    assert said.startswith("market_direction ")


@pytest.mark.parametrize("p_up", ["up", "0.7", 1.7, -0.1, True, None])
def test_a_market_probability_that_is_not_one_is_refused(p_up):
    """§7 gives `p_up` a number in zero to one, or the word `insufficient`.
    `True` is in the list because Python calls it an `int` and `0 <= True <= 1`."""
    said = refused_with(dict(ACCOUNTING_ANSWER,
                        market_direction={"p_up": p_up, "basis": [UPSTREAM_ITEM]}),
                   "accounting_reliability")
    assert "market_direction.p_up" in said


@pytest.mark.parametrize("basis", [UPSTREAM_ITEM, [""], ["  "], [UPSTREAM_ITEM, 7],
                                   {"0": UPSTREAM_ITEM}])
def test_a_basis_that_is_not_a_list_of_names_is_refused(basis):
    """An entry that is not a name resolves for nobody -- and a bare string is
    fifty-odd single characters, none of which is an item id."""
    said = refused_with(dict(ACCOUNTING_ANSWER,
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
    said = refused_with(answer, question)
    assert f"{field}[1].key" in said
    assert "the schema gives it a name" in said


@pytest.mark.parametrize("named", ["", "   ", None, 3])
def test_an_explanation_naming_no_id_is_refused(named):
    said = refused_with(dict(ACCOUNTING_ANSWER, explanations=[
        {"id": named, "support": "sufficient", "realization_p": 0.4}]),
        "accounting_reliability")
    assert "explanations[1].id" in said
    assert "the schema gives it a name" in said


@pytest.mark.parametrize("direction", ["", "   ", None, 3])
def test_a_continuous_entry_naming_no_direction_is_refused(direction):
    """§7 gives `direction` a string and does not enumerate its values, so a
    name is the whole of what this rule can ask."""
    said = refused_with(dict(PRESSURE_ANSWER, continuous=[
        dict(PRESSURE_ANSWER["continuous"][0], direction=direction)]),
        "financial_pressure")
    assert "continuous[1].direction" in said
    assert "the schema gives it a name" in said


@pytest.mark.parametrize("chance", [1.4, -0.1, "likely", None, True])
def test_a_realization_probability_that_is_not_one_is_refused(chance):
    said = refused_with(dict(ACCOUNTING_ANSWER, explanations=[
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
    said = refused_with(dict(PRESSURE_ANSWER, continuous=[
        dict(PRESSURE_ANSWER["continuous"][0], **{field: value})]),
        "financial_pressure")
    assert f"continuous[1].{field}" in said
    assert "not JSON" in said


def test_two_continuous_entries_under_one_key_are_refused():
    entry = PRESSURE_ANSWER["continuous"][0]
    said = refused_with(dict(PRESSURE_ANSWER,
                        continuous=[entry, dict(entry, point=250.0, high=300.0)]),
                   "financial_pressure")
    assert "revenue_next_quarter" in said
    assert "more than once" in said


def test_two_events_under_one_key_are_refused():
    entry = ACCOUNTING_ANSWER["events"][0]
    said = refused_with(dict(ACCOUNTING_ANSWER,
                        events=[entry, dict(entry, p_within_horizon=0.9)]),
                   "accounting_reliability")
    assert "restatement" in said
    assert "more than once" in said


def test_two_explanations_under_one_id_are_refused():
    entry = {"id": UPSTREAM_ITEM, "support": "sufficient", "realization_p": 0.4}
    said = refused_with(dict(ACCOUNTING_ANSWER,
                        explanations=[entry, dict(entry, support="unknown")]),
                   "accounting_reliability")
    assert said.startswith("explanations names")
    assert "more than once" in said


# The sweep above turns a rule off; it does not weaken one, so a value list
# compared without case, or an evidence loop that checks the quote and skips
# `upstream_item_id`, leaves every mutant it makes red and the rule half-judged.
# The retired file held those with the values below, and they are held here the
# same way, value for value.


@pytest.mark.parametrize("finding", ["yes", "no", "flagged", "", None])
def test_a_checklist_finding_outside_the_three_is_refused(finding):
    said = refused_with(dict(ACCOUNTING_ANSWER, checklist=[
        dict(ACCOUNTING_ANSWER["checklist"][0], finding=finding)]),
        "accounting_reliability")
    assert "checklist[1].finding" in said


@pytest.mark.parametrize("support", ["maybe", "", None, "Sufficient"])
def test_an_explanation_support_outside_the_three_is_refused(support):
    said = refused_with(dict(ACCOUNTING_ANSWER, explanations=[
        {"id": UPSTREAM_ITEM, "support": support, "realization_p": 0.4}]),
        "accounting_reliability")
    assert "explanations[1].support" in said


@pytest.mark.parametrize("named", ["", "   ", None, 3])
def test_an_evidence_entry_naming_no_id_is_refused(named):
    """The entry carries the right field with nothing in it. Reaching a
    citation gate, it would resolve against nothing and be counted as a failed
    citation -- a malformed answer in the drop count §8 reports beside the
    score."""
    said = refused_with(dict(ACCOUNTING_ANSWER, checklist=[
        dict(ACCOUNTING_ANSWER["checklist"][0],
             evidence=[{"upstream_item_id": named}])]),
        "accounting_reliability")
    assert "checklist[1].evidence[1].upstream_item_id" in said
    assert "the schema gives it a name" in said


@pytest.mark.parametrize("cited", [UPSTREAM_ITEM, [UPSTREAM_ITEM],
                                   {"upstream_item_id": UPSTREAM_ITEM, "quote": "x"},
                                   {"quote": UPSTREAM_ITEM}, {}])
def test_an_evidence_entry_that_is_not_the_schemas_shape_is_refused(cited):
    """With §7's own member as the whole evidence shape, a bare string, a list,
    an extra member or a missing one is refused rather than read as uncited."""
    said = refused_with(dict(ACCOUNTING_ANSWER, checklist=[
        dict(ACCOUNTING_ANSWER["checklist"][0], evidence=[cited])]),
        "accounting_reliability")
    assert "checklist[1].evidence[1]" in said


@pytest.mark.parametrize("events", ["lots", {"restatement": 0.1}, 3])
def test_an_events_field_that_is_not_a_list_is_refused(events):
    said = refused_with(dict(ACCOUNTING_ANSWER, events=events), "accounting_reliability")
    assert f"gives events as {type(events).__name__}" in said


@pytest.mark.parametrize("answer", [7, None, "watch", ["checklist"]])
def test_an_answer_that_is_not_an_object_is_refused(answer):
    said = refused_with(answer, "accounting_reliability")
    assert f"the prediction is {type(answer).__name__}, not an object" in said


# Six more the single-agent control's run judges and nothing above did, asked
# directly for the same reason: a shared function's rules need a caller that is
# not the control. With these, every one of the fifty-five rules the same sweep
# enumerates goes red with this file alone.


def test_an_empty_continuous_is_refused():
    """Financial pressure predicts next quarter's three numbers; an empty list
    is the field present and the prediction absent."""
    said = refused_with(dict(PRESSURE_ANSWER, continuous=[]), "financial_pressure")
    assert said.startswith("continuous is empty")


def test_two_checklist_entries_under_one_key_are_refused():
    """One indicator, one key: two entries under one key is a set, and the
    scorer reading the first would score whichever came back first."""
    entry = ACCOUNTING_ANSWER["checklist"][0]
    said = refused_with(dict(ACCOUNTING_ANSWER,
                        checklist=[entry, dict(entry, finding="no_flag")]),
                   "accounting_reliability")
    assert said.startswith("checklist names receivables_growth_outruns_revenue")
    assert "more than once" in said


@pytest.mark.parametrize("confidence", [1.4, -0.2, "high", None, True])
def test_a_confidence_that_is_not_a_probability_is_refused(confidence):
    said = refused_with(dict(ACCOUNTING_ANSWER, checklist=[
        dict(ACCOUNTING_ANSWER["checklist"][0], confidence=confidence)]),
        "accounting_reliability")
    assert "checklist[1].confidence" in said


@pytest.mark.parametrize("chance", [1.4, -0.1, "likely", None, True])
def test_an_event_probability_that_is_not_one_is_refused(chance):
    """§8 scores events by Brier, and Brier of `"likely"` is not a number."""
    said = refused_with(dict(ACCOUNTING_ANSWER, events=[
        {"key": "restatement", "p_within_horizon": chance}]),
        "accounting_reliability")
    assert "events[1].p_within_horizon" in said


def test_a_continuous_point_outside_its_own_range_is_refused():
    """A point outside the interval it came with is two numbers that cannot
    both be the same prediction."""
    said = refused_with(dict(PRESSURE_ANSWER, continuous=[
        dict(PRESSURE_ANSWER["continuous"][0], point=200.0)]), "financial_pressure")
    assert "outside its own range" in said
