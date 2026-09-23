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

import json
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


def test_neither_control_writes_out_a_section_seven_list_of_its_own():
    """The lists are written once, in `src/prediction_schema.py`.

    Read off each control's source rather than asked of its attributes: a copy
    under a new name is still a copy, and the next one to drift. Moved here
    from the shuffled control's tests with the register's lists added to it.
    """
    import ast
    by_hand = {BY_HAND_CHECKLIST, BY_HAND_EVIDENCE, BY_HAND_CONTINUOUS,
               BY_HAND_EVENTS, BY_HAND_EXPLANATIONS, BY_HAND_MARKET,
               BY_HAND_FINDINGS, BY_HAND_SUPPORT, BY_HAND_ANOMALY, BY_HAND_AXES,
               BY_HAND_NUMBERS_VS_PROSE, BY_HAND_MARKET_LABELS}
    for name in ("control_single_agent.py", "control_shuffled.py"):
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
