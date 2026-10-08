"""The run orchestrator's own logic, without calling a model.

A model call is the one thing this suite does not make. What is judged here is
what the orchestrator decides by itself: that every analyst runs its committed
definition and nothing written at run time, that the message it sends names the
directory's files and its one output, and that the reports downstream sees carry
only the items the quote gate kept.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import re
import shutil
import threading
import time

import pytest

from src import agent_inputs, fable_batch, run_analysis


def test_every_analyst_runs_its_committed_definition():
    for name in ("accounting-analyst", "financial-analyst", "valuation-analyst",
                 "valuation-analyst-second-pass"):
        spec = agent_inputs.AGENTS[name]
        definition = run_analysis.definition(spec.prompt)
        assert definition["model"] == "fable"
        assert definition["tools"] == ["Read", "Write"]
        assert f"Write `{spec.writes}`" in definition["prompt"]


def test_the_message_is_the_file_list_and_the_one_output():
    message = run_analysis.INSTRUCTION.format(files="a.md, b.json", writes="c.json")
    assert "a.md, b.json" in message and "c.json" in message
    assert "{" not in message


def test_the_control_prompt_names_its_three_files_and_the_ruled_out_words():
    prompt = run_analysis.CONTROL_PROMPT.format(files="input_notes.md")
    for name in run_analysis.CONTROL_WRITES:
        assert name in prompt
    for word in ("fraud", "manipulation", "buy", "sell", "alpha"):
        assert word in prompt


def test_report_items_are_read_off_the_fenced_blocks():
    text = '```json\n{ "id": "a_one", "quote": "q" }\n```\nprose\n```json\n{ "id": "b_two" }\n```\n'
    assert [item["id"] for item in run_analysis.report_items(text)] == ["a_one", "b_two"]


def test_the_copy_downstream_sees_holds_only_the_items_that_stood(tmp_path, monkeypatch):
    run = tmp_path / "run"
    for name, text in (("numbers-reader", '```json\n{ "id": "a_kept" }\n```\n'),
                       ("notes-text-reader", '```json\n{ "id": "b_dropped" }\n```\n'
                                             '```json\n{ "id": "b_kept" }\n```\n')):
        directory = agent_inputs.session_root(run, name)
        directory.mkdir(parents=True)
        (directory / agent_inputs.AGENTS[name].writes).write_text(text)
    (run / "input_manifest.json").write_text(json.dumps(
        {"dropped_items": [{"item_id": "b_dropped", "reason": "x",
                            "report": "report_notes_text.md"}]}))
    monkeypatch.setattr(run_analysis.quote_gate, "gate", lambda reports, root: {})
    run_analysis.gate_readers(run)
    notes = (run / "report_notes_text.md").read_text()
    assert "b_kept" in notes and "b_dropped" not in notes
    assert "removed 1 item" in notes
    assert "a_kept" in (run / "report_numbers.md").read_text()


def _stub_readers(tmp_path, numbers: str, notes: str, dropped: list[dict]):
    run = tmp_path / "run"
    for name, text in (("numbers-reader", numbers), ("notes-text-reader", notes)):
        directory = agent_inputs.session_root(run, name)
        directory.mkdir(parents=True)
        (directory / agent_inputs.AGENTS[name].writes).write_text(text)
    (run / "input_manifest.json").write_text(json.dumps({"dropped_items": dropped}))
    return run


def test_a_dropped_item_inside_a_list_block_is_taken_out_of_the_copy(tmp_path, monkeypatch):
    """ESE's notes reader wrote its twenty-seven items in one fenced list, and the
    gate removed a block only when every item in it was dropped: three dropped
    items stayed in the copy the analysts read, under a note saying it removed 0,
    and the owner's quotes_resolve failed each one. The list now loses each
    dropped element and is written again with the rest; the note counts items."""
    notes = '```json\n[{"id": "b_kept"}, {"id": "b_dropped"}]\n```\n'
    run = _stub_readers(tmp_path, '```json\n{ "id": "a_kept" }\n```\n', notes,
                        [{"item_id": "b_dropped", "reason": "x", "report": "report_notes_text.md"}])
    monkeypatch.setattr(run_analysis.quote_gate, "gate", lambda reports, root: {})
    run_analysis.gate_readers(run)
    copy = (run / "report_notes_text.md").read_text()
    assert run_analysis.report_items(copy) == [{"id": "b_kept"}]
    assert "removed 1 item(s) from this copy" in copy
    assert (run / "report_numbers.md").read_text().endswith('```json\n{ "id": "a_kept" }\n```\n')
    # the reader's own copy keeps what it wrote
    assert (agent_inputs.session_root(run, "notes-text-reader") / "report_notes_text.md"
            ).read_text() == notes


@pytest.mark.parametrize("case", ["untouched list", "single dropped", "other report",
                                  "kept element equal", "malformed"])
def test_the_copy_is_cut_item_by_item_and_nothing_else_moves(tmp_path, monkeypatch, case):
    """The other side, standing before the fix and after it: a list with nothing
    dropped stays byte for byte; a single dropped item's block is removed whole;
    a drop row of one report takes nothing out of the other (the row is keyed by
    report, as the owner's grader keys it); a kept element reads back as the dict
    the reader wrote; and a block that is not JSON is never rewritten."""
    listed = ('```json\n[{ "id": "b_one", "quote": "Raising the lower end",\n'
              '   "paragraph_id": "0001104659-26-092033:8k_2_02:36" },\n { "id": "b_two" }]\n```\n')
    rows = {"untouched list": [],
            "single dropped": [{"item_id": "a_gone", "reason": "x", "report": "report_numbers.md"}],
            "other report": [{"item_id": "b_one", "reason": "x", "report": "report_numbers.md"}],
            "kept element equal": [{"item_id": "b_two", "reason": "x",
                                    "report": "report_notes_text.md"}],
            "malformed": []}[case]
    numbers = '```json\n{ "id": "a_gone" }\n```\nprose stays\n'
    notes = listed if case != "malformed" else '```json\n[{"id": "b_one"},]\n```\n'
    run = _stub_readers(tmp_path, numbers, notes, rows)
    monkeypatch.setattr(run_analysis.quote_gate, "gate", lambda reports, root: {})
    run_analysis.gate_readers(run)
    copy = (run / "report_notes_text.md").read_text()
    body = copy.split("\n", 1)[1]
    if case in ("untouched list", "other report"):
        assert body == listed
    elif case == "single dropped":
        assert (run / "report_numbers.md").read_text().split("\n", 1)[1] == "prose stays\n"
        assert body == listed
    elif case == "kept element equal":
        assert run_analysis.report_items(copy) == [
            {"id": "b_one", "quote": "Raising the lower end",
             "paragraph_id": "0001104659-26-092033:8k_2_02:36"}]
    else:
        # removed, never rewritten: the gate recorded it as a drop with no id
        assert "```" not in body and "1 fenced block(s) that are not JSON" in copy


# The owner's grader on the real gate's output, the ESE shapes: twin ids on both
# reports, and an item whose paragraph id is no id, in one notes list. Paragraphs
# 36 and 37 of ESE's earnings release 0001104659-26-092033, as its input_8k.md
# printed them (run 0001104659-26-093266, 2026-10-07).
ESE_ACCESSION = "0001104659-26-093266"
ESE_SALES = ("Raising the lower end of FY 2026 Sales guidance and now expect Sales to be in the "
             "range of $1.30 to $1.33 billion (19 to 21 percent growth over the prior year).")
ESE_EPS = ("Raising full year Adjusted EPS guidance to a range of $8.30 - $8.40 per share (38 to "
           "39 percent growth)")
ESE_8K = ("# ESE 8-K\n\n## item 2.02\n\n"
          f"[0001104659-26-092033:8k_2_02:36]\n|  | · | {ESE_SALES} |\n\n"
          f"[0001104659-26-092033:8k_2_02:37]\n|  | · | {ESE_EPS}, which reflects a midpoint "
          "increase of $0.70 per share. |\n")


def _ese_item(identifier, quote, paragraph):
    return {"id": identifier, "quote": quote, "paragraph_id": paragraph}


def test_the_owner_finds_no_dropped_item_in_the_copy_the_real_gate_wrote(tmp_path):
    from evals.common import PASS
    from evals.regression import mechanical
    run = tmp_path / "run"
    run.mkdir()
    (run / "input_manifest.json").write_text(json.dumps({"accession": ESE_ACCESSION}))
    twin = "results_against_expectations_sales_guidance_lower_end_raised"
    sales = "0001104659-26-092033:8k_2_02:36"
    eps = "0001104659-26-092033:8k_2_02:37"
    numbers = [_ese_item(twin, ESE_SALES, sales),
               _ese_item("results_against_expectations_adjusted_eps_guidance_raised", ESE_EPS, eps)]
    notes = [_ese_item(twin, ESE_SALES, sales),
             _ese_item("across_documents_eight_k_termination_of_material_agreement_unexplained",
                       "2026-06-03 0001104659-26-070116 — 1.01, 1.02, 2.03, 9.01",
                       "input_8k item codes list (2026-06-03 entry)"),
             _ese_item("results_against_expectations_sales_range_restated", "Sales guidance", sales),
             _ese_item("results_against_expectations_eps_range_restated", "Adjusted EPS guidance", eps)]
    for name, text in (("numbers-reader", "".join(f"```json\n{json.dumps(item)}\n```\n"
                                                  for item in numbers)),
                       ("notes-text-reader", f"```json\n{json.dumps(notes, indent=1)}\n```\n")):
        directory = agent_inputs.session_root(run, name)
        directory.mkdir(parents=True)
        (directory / "input_8k.md").write_text(ESE_8K, encoding="utf-8")
        (directory / agent_inputs.AGENTS[name].writes).write_text(text, encoding="utf-8")
    run_analysis.gate_readers(run)
    manifest = json.loads((run / "input_manifest.json").read_text())
    assert {(row["report"], row["item_id"]) for row in manifest["dropped_items"]} == {
        ("report_numbers.md", twin), ("report_notes_text.md", twin),
        ("report_notes_text.md",
         "across_documents_eight_k_termination_of_material_agreement_unexplained")}
    result = mechanical.check_quotes_resolve(run)
    assert not any("dropped by the gate and still in the report" in line
                   for line in result.failures)
    assert result.status == PASS, result.failures
    assert mechanical.kept_items(run)["report_notes_text.md"] == {
        "results_against_expectations_sales_range_restated",
        "results_against_expectations_eps_range_restated"}
    assert "removed 2 item(s)" in (run / "report_notes_text.md").read_text()


# An item the gate finds no id on -- an id of "", of spaces, a number, true, a list,
# an object, null, or none written -- is dropped under a row with no item id
# (`quote_gate.item_id`). The runner matched the copy to the rows by the id as
# written, so the first four stayed in the copy the analysts read and the owner,
# whose drop rows are the gate's, held their quotes as kept items' (the critic's
# probe of 2026-10-08, on ESE's paragraph 36 above); a list or an object as an id
# stopped gate_readers (unhashable). The last two passed before, and are the other
# side. No reader report on record has such an id.
@pytest.mark.parametrize("shape", ["one list", "a block each"])
@pytest.mark.parametrize("identifier", ["", "  ", 7, True, ["x"], {"a": 1}, None, "unwritten"])
def test_an_item_the_gate_finds_no_id_on_leaves_the_copy(tmp_path, shape, identifier):
    from evals.common import PASS
    from evals.regression import mechanical
    run = tmp_path / "run"
    run.mkdir()
    (run / "input_manifest.json").write_text(json.dumps({"accession": ESE_ACCESSION}))
    sales = "0001104659-26-092033:8k_2_02:36"
    kept = _ese_item("results_against_expectations_sales_range_restated", "Sales guidance",
                     sales)
    nameless = {"quote": "words the filing never printed", "paragraph_id": sales}
    if identifier != "unwritten":
        nameless["id"] = identifier
    notes = (f"```json\n{json.dumps([kept, nameless], indent=1)}\n```\n" if shape == "one list"
             else "".join(f"```json\n{json.dumps(item)}\n```\n" for item in (kept, nameless)))
    for name, text in (("numbers-reader", "no items\n"), ("notes-text-reader", notes)):
        directory = agent_inputs.session_root(run, name)
        directory.mkdir(parents=True)
        (directory / "input_8k.md").write_text(ESE_8K, encoding="utf-8")
        (directory / agent_inputs.AGENTS[name].writes).write_text(text, encoding="utf-8")
    run_analysis.gate_readers(run)
    manifest = json.loads((run / "input_manifest.json").read_text())
    assert [(row["report"], row["item_id"]) for row in manifest["dropped_items"]] == [
        ("report_notes_text.md", None)]
    copy = (run / "report_notes_text.md").read_text(encoding="utf-8")
    assert run_analysis.report_items(copy) == [kept]
    assert "removed 1 item(s)" in copy
    if shape == "a block each":
        assert copy.endswith(f"```json\n{json.dumps(kept)}\n```\n")
    result = mechanical.check_quotes_resolve(run)
    assert result.status == PASS, result.failures
    assert mechanical.kept_items(run)["report_notes_text.md"] == {kept["id"]}
    # the reader's own copy keeps what it wrote
    assert (agent_inputs.session_root(run, "notes-text-reader") / "report_notes_text.md"
            ).read_text(encoding="utf-8") == notes


# A kept item whose own text holds three backticks, written in the reader's JSON as
# \u0060 escapes, in a list that loses an item the gate found no id on (the critic's
# probe of 2026-10-08, on ESE's paragraph 36 above). The reader's report reads clean to
# the owner. Written again by `json.dumps`, the escapes came back as backticks, which
# close the owner's fence early: the copy the analysts read held one block that is not
# JSON and no item, and quotes_resolve failed "1 fenced block(s) that are not JSON".
# No reader report on record carries a backtick.
def _notes_list_losing_one(run: Path, what_changed: str) -> tuple[dict, str, str]:
    """The kept item, its element as the reader wrote it, and the reader's report."""
    run.mkdir()
    (run / "input_manifest.json").write_text(json.dumps({"accession": ESE_ACCESSION}))
    sales = "0001104659-26-092033:8k_2_02:36"
    kept = dict(_ese_item("results_against_expectations_sales_range_restated",
                          "Sales guidance", sales), what_changed=what_changed)
    element = json.dumps(kept, indent=2).replace("`", "\\u0060")
    nameless = json.dumps({"quote": "words the filing never printed", "paragraph_id": sales})
    notes = f"# notes\n\n```json\n[\n{element},\n{nameless}\n]\n```\n"
    for name, text in (("numbers-reader", "no items\n"), ("notes-text-reader", notes)):
        directory = agent_inputs.session_root(run, name)
        directory.mkdir(parents=True)
        (directory / "input_8k.md").write_text(ESE_8K, encoding="utf-8")
        (directory / agent_inputs.AGENTS[name].writes).write_text(text, encoding="utf-8")
    return kept, element, notes


@pytest.mark.parametrize("what_changed", ["the release prints ``` in its table",
                                          "four ```` and three ``` again"])
def test_a_kept_element_holding_three_backticks_leaves_the_owner_s_fence_where_it_was(
        tmp_path, what_changed):
    from evals.common import PASS
    from evals.regression import mechanical
    run = tmp_path / "run"
    kept, element, notes = _notes_list_losing_one(run, what_changed)
    assert mechanical.read_report_blocks(notes)[1] == 0
    run_analysis.gate_readers(run)
    copy = (run / "report_notes_text.md").read_text(encoding="utf-8")
    assert mechanical.read_report_blocks(copy) == ([kept], 0)
    assert element in copy                  # the element that stood, as the reader wrote it
    assert "removed 1 item(s)" in copy
    result = mechanical.check_quotes_resolve(run)
    assert result.status == PASS, result.failures


@pytest.mark.parametrize("what_changed", ["a `code` word and a `` pair", "no backtick at all"])
def test_a_kept_element_with_fewer_than_three_backticks_reads_the_same(tmp_path, what_changed):
    """The other side, standing before the fix and after it."""
    from evals.common import PASS
    from evals.regression import mechanical
    run = tmp_path / "run"
    kept, _, _ = _notes_list_losing_one(run, what_changed)
    run_analysis.gate_readers(run)
    copy = (run / "report_notes_text.md").read_text(encoding="utf-8")
    assert mechanical.read_report_blocks(copy) == ([kept], 0)
    assert mechanical.check_quotes_resolve(run).status == PASS


def test_a_copy_that_does_not_read_as_the_items_that_stood_is_never_written(
        tmp_path, monkeypatch):
    """The copy is read again, as the owner reads it, before it is written: a cut
    that went wrong stops the gate rather than handing the analysts a block the
    owner cannot read or an item that did not stand."""
    run = tmp_path / "run"
    _notes_list_losing_one(run, "plain words")
    monkeypatch.setattr(run_analysis, "_array_elements",
                        lambda block: ['{"id": "results_against_expectations_sales_range_',
                                       '"restated"}'])
    with pytest.raises(run_analysis.quote_gate.QuoteGateError,
                       match="does not read as the items that stood: 1 fenced block"):
        run_analysis.gate_readers(run)
    assert not (run / "report_notes_text.md").exists()


@pytest.mark.parametrize("block", [
    '[]', ' [ ] \n', '[1, "two", null, true, {"a": [1, {"b": "]"}]}]',
    '[\n  {"id": "x", "quote": "a \\"quoted\\" ], comma"},\n  {"id": "y"}\n]\n',
    '[NaN, Infinity, -0.0, 1e400, "\\u0060\\u0060\\u0060"]', '[[1, 2], [], [[3]]]'])
def test_the_elements_of_a_list_block_read_back_as_the_list(block):
    written = run_analysis._array_elements(block)
    assert [run_analysis._canonical(json.loads(one)) for one in written] == [
        run_analysis._canonical(one) for one in json.loads(block)]
    assert all(one in block for one in written)


@pytest.mark.parametrize("block", ['{"id": "x"}', '"[1]"', '[1, 2', '[1,]', '[1] [2]', ''])
def test_a_block_that_is_not_one_list_has_no_elements(block):
    assert run_analysis._array_elements(block) is None


# --- a whole run, with every agent stubbed ------------------------------------------------
#
# The model is the one thing replaced. Everything else is the run as it is: the
# NVIDIA bundle assembled from the committed fixtures, the quote gate, the
# calculator on the committed record, the analysis gate, the memo, the market
# marker, and the layer checks over the finished directory. No price directory is
# given, which is the state the project runs in without a token.

import pytest

from src import assemble_bundle

NVDA_ACCESSION = "0001045810-26-000075"
# A planted acceptance stamp for that 10-Q, after the four o'clock close. The
# fixture carries no acceptance time. EDGAR's submissions API gives
# `filings.recent.acceptanceDateTime` = 2026-08-26T20:36:00.000Z for the
# accession (read 2026-10-06); whether that Z is decorative on an Eastern wall
# clock (the src/market.py reading, 20:36 Eastern) or marks UTC (16:36 Eastern)
# is a row in docs/needs_judgment.md, and the test below says what it holds.
NVDA_ACCEPTED = "2026-08-26T20:36:00"

NUMBERS_REPORT = '''```json
{ "id": "earnings_quality_accruals_rising", "what_changed": "x", "account": "a",
  "expected_direction": "up", "horizon": "h",
  "quote": "\\"value\\": 59.63738684902464",
  "paragraph_id": "0001045810-26-000075:trends:days_sales_outstanding:2026-04-27..2026-07-26" }
```
'''


def _analysis(kind: str, citing: str) -> dict:
    from src import analysis_check
    area = {"finding": "Cash over income is {earnings_versus_cash.operating_cash_flow_over_net_income}.",
            "verdict": "weaker", "evidence": [], "fields": [
                "earnings_versus_cash.operating_cash_flow_over_net_income"]}
    anomaly = {"id": "earnings_versus_cash_cash_lags_income", "name": "cash lags income",
               "name_ko": "현금이 이익에 뒤처짐", "area": "earnings_versus_cash",
               "what": "see the field", "numbers_vs_prose": "unresolved",
               "evidence": [citing], "fields": []}
    if kind == "accounting":
        return {"areas": {name: dict(area) for name in analysis_check.ACCOUNTING_AREAS},
                "reconciliation": [], "anomalies": [anomaly], "adjustments": [],
                "summary_ko": {"earnings_versus_cash": "비율 {earnings_versus_cash.operating_cash_flow_over_net_income}"},
                "limits": analysis_check.LIMITS["accounting"]}
    return {"sections": {name: {"reading": "read", "fields": [], "evidence": []}
                         for name in analysis_check.FINANCIAL_SECTIONS},
            "dupont": {"reading": "read", "fields": []},
            "anomalies": [dict(anomaly, id="profitability_margin_high", area="profitability",
                               numbers_vs_prose=None)],
            "path_to_distress": {"reading": "none", "fields": []},
            "summary_ko": {}, "limits": analysis_check.LIMITS["financial"]}


DRIVERS = {"revenue_growth_year_one": 0.2, "terminal_growth": 0.03,
           "operating_margin_year_one": 0.6, "operating_margin_year_ten": 0.4,
           "reinvestment_rate_year_one": 0.3, "reinvestment_rate_year_ten": 0.2}


def _fake_ask(seen: dict, notes_report: str = "no items\n", assumptions: dict | None = None,
              numbers_report: str = NUMBERS_REPORT, accounting_analysis: dict | None = None):
    """`notes_report` and `numbers_report` are what the stubbed readers write;
    `assumptions` the valuation analyst's first pass, by default three scenarios
    citing one field."""
    def ask(directory, *, agent, writes, message, spec, log):
        seen[directory.name] = sorted(path.name for path in directory.iterdir())
        for name in writes:
            if name == "report_numbers.md":
                text = numbers_report
            elif name == "report_notes_text.md":
                text = notes_report
            elif name == "analysis_accounting.json":
                text = json.dumps(accounting_analysis if accounting_analysis is not None
                                  else _analysis("accounting", "earnings_quality_accruals_rising"))
            elif name == "analysis_financial.json":
                text = json.dumps(_analysis("financial", "earnings_quality_accruals_rising"))
            elif name == "assumptions.json" and assumptions is not None:
                text = json.dumps(assumptions)
            elif name in ("assumptions.json", "control_assumptions.json"):
                reason = {"reason": "a reason", "fields": ["ratios.profitability.gross_margin"]}
                text = json.dumps({"scenarios": {s: dict(DRIVERS, reasons={d: reason for d in DRIVERS})
                                                 for s in ("bear", "base", "bull")}})
            elif name == "analysis_valuation.json":
                text = json.dumps({"value_range": {"reading": "not computed", "fields": []},
                                   "price_position": {"reading": "not computed", "fields": []},
                                   "market_implied_growth": {"reading": "not computed", "fields": []},
                                   "accounting_adjustments": {"reading": "none", "fields": []},
                                   "most_sensitive": [], "summary_ko": {}, "limits": ""})
            else:
                text = json.dumps({"summary_ko": {}, "limits": ""})
            (directory / name).write_text(text)
        return {"agent": agent, "result": "written", "input_tokens": 1, "output_tokens": 1}
    return ask


@pytest.fixture(scope="module")
def finished(tmp_path_factory):
    run = tmp_path_factory.mktemp("run") / "NVDA" / NVDA_ACCESSION
    bundle = assemble_bundle.build("NVDA", "10-Q", accession=NVDA_ACCESSION,
                                   prior_runs=run.parent.parent)
    assemble_bundle.write(bundle, run)
    seen: dict = {}
    original = run_analysis.ask
    run_analysis.ask = _fake_ask(seen)
    try:
        manifest = run_analysis.run_company(run=run, ticker="NVDA", form="10-Q",
                                            cutoff="2026-08-26", period_end="2026-07-26",
                                            store=run_analysis.cutoff_guard.FIXTURES,
                                            prices=None, control="always")
    finally:
        run_analysis.ask = original
    return run, manifest, seen


def test_a_run_with_no_price_reaches_the_memo(finished):
    run, manifest, _ = finished
    assert manifest["analysis_failure"] is None
    assert manifest["market_table"] == "unavailable"
    assert (run / "memo_ko.md").is_file()
    assert "Tiingo" in json.loads((run / "calculator.json").read_text())["valuation"]["missing"] \
        or "WACC" in json.loads((run / "calculator.json").read_text())["valuation"]["missing"]


def test_the_quote_gates_drops_survive_to_the_manifest(finished):
    run, manifest, _ = finished
    assert "dropped_items" in manifest
    assert set(manifest["agents"]) >= {"numbers-reader", "accounting-analyst",
                                       "valuation-analyst-second-pass", "control-single-agent"}


def test_every_calculator_stage_is_its_own_file_and_the_layers_are_intact(finished):
    run, _, _ = finished
    for name in ("calculator_before_analysts.json", "calculator_filings_only.json",
                 "calculator_before_drivers.json", "calculator.json"):
        assert (run / name).is_file(), name
    assert agent_inputs.isolation_violations(run) == []


def test_no_analyst_who_may_not_see_a_price_is_handed_one(finished):
    run, _, seen = finished
    for name in ("accounting-analyst", "financial-analyst"):
        text = (agent_inputs.session_root(run, name) / "calculator_filings_only.json").read_text()
        assert "price_at_cutoff" not in text and '"beta"' not in text


def test_the_control_never_sees_what_an_analyst_wrote(finished):
    run, _, seen = finished
    held = seen[run_analysis.CONTROL_DIRNAME]
    assert "calculator_before_analysts.json" in held
    for name in ("calculator.json", "calculator_before_drivers.json", "analysis_accounting.json",
                 "assumptions.json", "report_numbers.md", "input_market.json",
                 "input_manifest.json"):
        assert name not in held, name
    base = json.loads((run / run_analysis.CONTROL_DIRNAME
                       / "calculator_before_analysts.json").read_text())
    assert base["free_cash_flow"]["free_cash_flow_quality_adjusted"]["adjustments_applied"] == []


def test_the_scorecard_counts_the_controls_gated_file_beside_the_analysts(finished):
    from src import analysis_scorecard
    run, _, _ = finished
    row = analysis_scorecard.row(run)
    gated = json.loads((run / "control_analysis_accounting.json").read_text())
    assert row["control_accounting_anomalies"] == len(gated["anomalies"])
    assert row["accounting_anomalies"] == len(json.loads(
        (run / "analysis_accounting.json").read_text())["anomalies"])
    assert "valuation" in row and "not computed" in row["valuation"]


def test_the_planted_item_and_the_anomaly_citing_it_survive_both_gates(finished):
    """The planted reader item quotes the trend cell exactly as the committed bundle
    prints it; if the quote stopped matching, the item would drop at the quote gate
    and the anomaly citing it at the analysis gate. Both must stand here."""
    run, manifest, _ = finished
    dropped = {row.get("item_id") for row in manifest.get("dropped_items") or []}
    assert "earnings_quality_accruals_rising" not in dropped
    gated = json.loads((run / "analysis_accounting.json").read_text())
    assert [item["id"] for item in gated["anomalies"]] == ["earnings_versus_cash_cash_lags_income"]
    assert gated["dropped_count"] == 0


def test_a_failed_analyst_is_named_and_the_run_is_not_finished(tmp_path, monkeypatch):
    # The usage limit of 2026-09-28 failed four runs' analysts after both readers
    # wrote; each still exited 0 with analysis_failure null and a memo.
    run = tmp_path / "NVDA" / NVDA_ACCESSION
    bundle = assemble_bundle.build("NVDA", "10-Q", accession=NVDA_ACCESSION,
                                   prior_runs=run.parent.parent)
    assemble_bundle.write(bundle, run)
    written = _fake_ask({})

    def ask(directory, *, agent, writes, message, spec, log):
        if agent == "accounting-analyst":
            return {"agent": agent, "result": "failed", "reason": "exit 1; wrote []"}
        return written(directory, agent=agent, writes=writes, message=message,
                       spec=spec, log=log)

    monkeypatch.setattr(run_analysis, "ask", ask)
    manifest = run_analysis.run_company(run=run, ticker="NVDA", form="10-Q",
                                        cutoff="2026-08-26", period_end="2026-07-26",
                                        store=run_analysis.cutoff_guard.FIXTURES,
                                        prices=None)
    assert manifest["analysis_failure"] == "did not write: accounting-analyst"
    assert not (run / "analysis_accounting.json").exists()
    assert (run / "analysis_financial.json").is_file()
    assert "valuation-analyst" not in manifest["agents"]


def test_a_named_model_reaches_every_agent_and_the_manifest_says_so(tmp_path, monkeypatch):
    # The owner's decision of 2026-09-30: Opus only while the Fable limit holds.
    # The committed definitions carry fable for the analysts; with --model every
    # session is asked for the named model and the definitions stay as they are.
    assert run_analysis.definition("accounting-analyst")["model"] == "fable"
    run = tmp_path / "NVDA" / NVDA_ACCESSION
    bundle = assemble_bundle.build("NVDA", "10-Q", accession=NVDA_ACCESSION,
                                   prior_runs=run.parent.parent)
    assemble_bundle.write(bundle, run)
    written, asked = _fake_ask({}), []

    def ask(directory, *, agent, writes, message, spec, log):
        asked.append((agent, spec["model"]))
        return dict(written(directory, agent=agent, writes=writes, message=message,
                            spec=spec, log=log), model_requested=spec["model"])

    monkeypatch.setattr(run_analysis, "ask", ask)
    manifest = run_analysis.run_company(run=run, ticker="NVDA", form="10-Q",
                                        cutoff="2026-08-26", period_end="2026-07-26",
                                        store=run_analysis.cutoff_guard.FIXTURES,
                                        prices=None, model="opus", control="always")
    # both valuation passes run the one committed valuation-analyst definition
    assert sorted(agent for agent, _ in asked) == sorted([
        "numbers-reader", "notes-text-reader", "accounting-analyst", "financial-analyst",
        "valuation-analyst", "valuation-analyst", "control-single-agent"])
    assert {model for _, model in asked} == {"opus"}
    assert manifest["model_override"]["model"] == "opus"
    # applies_to names the agents this invocation called: all seven, here
    assert manifest["model_override"]["applies_to"] == [
        "numbers-reader", "notes-text-reader", "accounting-analyst", "financial-analyst",
        "valuation-analyst", "valuation-analyst-second-pass", "control-single-agent"]
    assert run_analysis.definition("accounting-analyst")["model"] == "fable"


def test_with_no_model_named_each_agent_asks_for_its_own(finished):
    _, manifest, _ = finished
    assert "model_override" not in manifest


def test_a_run_with_a_market_table_is_labelled_by_python_and_never_marked_unavailable(tmp_path, monkeypatch):
    """NVDA's 10-Q was filed on 2026-08-26, a Wednesday. The acceptance stamp here is
    planted: the fixture under tests/fixtures/NVDA holds no acceptance time (the
    fetch projects the index to filing dates, and every fixture file is held to
    the manifest's hash, so none can be written onto a row by hand; queue.md
    carries the item that makes the fetch keep it). EDGAR's submissions API gives
    2026-08-26T20:36:00.000Z for this accession. Read as Eastern, the
    src/market.py convention, that is 20:36, after EDGAR's half past five, and
    EDGAR would then date the filing the 27th -- while the fixture dates it the
    26th; read as UTC it is 16:36 Eastern and the 26th stands. So either the
    convention or the fixture's date is wrong, and docs/needs_judgment.md holds
    the question. This test holds only the window arithmetic for a stamp after
    the four o'clock close: under either reading day zero is Thursday the 27th
    and the window runs to Monday the 31st. Abnormal returns 0.02, 0.01 and 0.00
    sum to 0.03."""
    accepted = NVDA_ACCEPTED
    run = tmp_path / "NVDA" / NVDA_ACCESSION
    bundle = assemble_bundle.build("NVDA", "10-Q", accession=NVDA_ACCESSION,
                                   prior_runs=run.parent.parent)
    assemble_bundle.write(bundle, run)
    days = ["2026-08-27", "2026-08-28", "2026-08-31"]
    rows = [{"ticker": "NVDA", "date": d, "abnormal_return": a, "window": "filing",
             "reaction_window": 0.03, "short_interest_ratio": None,
             "short_interest_two_year_median": None, "short_interest_above_median": None}
            for d, a in zip(days, [0.02, 0.01, 0.0])]
    (run / "input_market.json").write_text(json.dumps(
        {"ticker": "NVDA", "cutoff": "2026-08-31", "rows": rows,
         "windows": [{"kind": "filing", "filing_date": "2026-08-26",
                      "accepted": accepted, "day_zero": days[0],
                      "days": days, "reaction_window": 0.03}]}))
    monkeypatch.setattr(run_analysis, "ask", _fake_ask({}))
    manifest = run_analysis.run_company(run=run, ticker="NVDA", form="10-Q",
                                        cutoff="2026-08-26", period_end="2026-07-26",
                                        store=run_analysis.cutoff_guard.FIXTURES,
                                        prices=None, control="always")
    assert manifest["analysis_stages"]["market_labels"]["written"] is True
    assert manifest["analysis_stages"]["market_labels_check"]["checked"] is True
    assert manifest.get("market_table") != "unavailable"
    # the table and the labels are the run's, and reach no agent: not the readers,
    # not the analysts, not the valuation analyst, not the single-agent control
    assert agent_inputs.isolation_violations(run) == []
    agent_files = {path.name for path in (run / "agents").rglob("*") if path.is_file()}
    assert "input_market.json" not in agent_files and "market_labels.json" not in agent_files
    control = run / run_analysis.CONTROL_DIRNAME
    assert control.is_dir()                                     # the control ran
    control_files = {path.name for path in control.rglob("*") if path.is_file()}
    assert "input_numbers.json" in control_files                # and holds the bundle
    assert "input_market.json" not in control_files and "market_labels.json" not in control_files
    labels = json.loads((run / "market_labels.json").read_text())
    assert [one["labels"][0]["label"] for one in labels["items"]] == ["priced_in"]


# --- Fable, used efficiently (the owner's decision of 2026-10-06) ---------------------------

class _Done:
    def __init__(self, returncode, stdout, stderr=""):
        self.returncode, self.stdout, self.stderr = returncode, stdout, stderr


def _cli(answers):
    """A stand-in for the claude CLI: each call pops the next (exit, json, files) answer."""
    calls = []

    def run(command, cwd, capture_output, text, timeout):
        exit_code, payload, files = answers.pop(0)
        for name, content in (files or {}).items():
            (cwd / name).write_text(content)
        calls.append(command)
        return _Done(exit_code, json.dumps(payload))
    return run, calls


def _ask(tmp_path, monkeypatch, answers, model):
    run, calls = _cli(answers)
    monkeypatch.setattr(run_analysis.subprocess, "run", run)
    record = run_analysis.ask(tmp_path, agent="x", writes=("out.json",), message="m",
                              spec={"model": model, "description": "d", "prompt": "p",
                                    "tools": ["Read"]}, log=tmp_path / "x.log")
    return record, calls


# A call that crashed after spending tokens: a plain failure, which a retry answers.
SPENT = {"input_tokens": 5, "output_tokens": 1}
FAILING = (1, {"is_error": True, "result": "crashed", "usage": SPENT}, None)


def test_a_failed_fable_call_is_run_again_at_most_twice(tmp_path, monkeypatch):
    record, calls = _ask(tmp_path, monkeypatch, [FAILING] * 5, "fable")
    assert record["result"] == "failed" and len(calls) == 3
    assert "limit_reached" not in record


# A call that passed: tokens spent, served by Fable, the file written.
PASSING = (0, {"usage": {"input_tokens": 7, "output_tokens": 2}, "total_cost_usd": 0.5,
               "modelUsage": {"claude-fable-5-1": {"outputTokens": 2}}}, {"out.json": "{}"})


def test_every_attempt_is_on_record_and_the_tokens_are_their_sum(tmp_path, monkeypatch):
    """Two failures then a pass: three attempts listed, each with its own usage
    and outcome, and the record's token fields the sum over them -- 5+5+7 in,
    1+1+2 out -- under the names a reader of the record already knows. A call
    that passed first lists one attempt, and its fields are that attempt's."""
    record, calls = _ask(tmp_path, monkeypatch, [FAILING, FAILING, PASSING], "fable")
    assert record["result"] == "written" and len(calls) == 3
    assert [row["attempt"] for row in record["attempts"]] == [1, 2, 3]
    assert [row["outcome"] for row in record["attempts"]] == ["failed", "failed", "written"]
    assert [row["input_tokens"] for row in record["attempts"]] == [5, 5, 7]
    assert record["attempts"][2]["model_served"] == "claude-fable-5-1"
    assert all(isinstance(row["duration_s"], float) for row in record["attempts"])
    assert record["input_tokens"] == 17 and record["output_tokens"] == 4
    assert record["cost_usd"] == 0.5                            # the one attempt that cost
    assert record["attempt"] == 3 and record["model_served"] == "claude-fable-5-1"
    record, _ = _ask(tmp_path, monkeypatch, [PASSING], "fable")
    assert len(record["attempts"]) == 1 and record["input_tokens"] == 7
    # the other outcome: a limit ends the list where it stands
    _two_second_clock(monkeypatch)
    record, _ = _ask(tmp_path, monkeypatch, [ZERO_TOKEN_FAILURE] * 3, "fable")
    assert [row["outcome"] for row in record["attempts"]] == ["limit"]


def test_a_failed_opus_call_is_run_again_once(tmp_path, monkeypatch):
    record, calls = _ask(tmp_path, monkeypatch, [FAILING] * 5, "opus")
    assert record["result"] == "failed" and len(calls) == 2


def test_a_call_whose_output_passed_is_never_run_again(tmp_path, monkeypatch):
    good = (0, {"is_error": False, "result": "ok"}, {"out.json": "{}"})
    record, calls = _ask(tmp_path, monkeypatch, [good] * 3, "fable")
    assert record["result"] == "written" and len(calls) == 1


def test_a_file_that_is_not_json_counts_as_a_failed_call(tmp_path, monkeypatch):
    bad = (0, {"is_error": False, "result": "ok", "usage": SPENT}, {"out.json": "not json"})
    good = (0, {"is_error": False, "result": "ok"}, {"out.json": "{}"})
    record, calls = _ask(tmp_path, monkeypatch, [bad, good], "fable")
    assert record["result"] == "written" and len(calls) == 2


def test_a_call_never_sees_its_own_earlier_output_and_a_session_that_writes_nothing_is_not_written(
        tmp_path, monkeypatch):
    (tmp_path / "out.json").write_text('{"stale": true}')
    silent = (0, {"is_error": False, "result": "ok", "usage": SPENT}, None)
    record, calls = _ask(tmp_path, monkeypatch, [silent] * 5, "fable")
    assert record["result"] == "failed" and len(calls) == 3
    assert "wrote []" in record["reason"]
    assert not (tmp_path / "out.json").exists()
    (tmp_path / "out.json").write_text('{"stale": true}')
    good = (0, {"is_error": False, "result": "ok"}, {"out.json": '{"fresh": true}'})
    record, calls = _ask(tmp_path, monkeypatch, [good], "fable")
    assert record["result"] == "written" and len(calls) == 1
    assert (tmp_path / "out.json").read_text() == '{"fresh": true}'


def test_one_predicate_says_what_is_fable_and_a_full_id_gets_the_fable_budget(
        tmp_path, monkeypatch):
    assert run_analysis.is_fable("fable") and run_analysis.is_fable("claude-fable-5-1")
    assert not run_analysis.is_fable("opus") and not run_analysis.is_fable("claude-opus-5-5")
    assert not run_analysis.is_fable(None)
    record, calls = _ask(tmp_path, monkeypatch, [FAILING] * 5, "claude-fable-5-1")
    assert record["result"] == "failed" and len(calls) == 3
    (tmp_path / "o").mkdir()
    record, calls = _ask(tmp_path / "o", monkeypatch, [FAILING] * 5, "claude-opus-5-5")
    assert record["result"] == "failed" and len(calls) == 2
    from src import fable_batch
    assert fable_batch.fable_tokens({"agents": {"a": {"model_served": "claude-fable-5-1",
                                                       "input_tokens": 7}}}) == 7
    assert fable_batch.fable_tokens({"agents": {"a": {"model_served": "claude-opus-5-5",
                                                       "input_tokens": 7}}}) == 0


def _two_second_clock(monkeypatch):
    """Each read of the clock moves it two seconds on, and a call reads it once
    before and once after the stubbed subprocess, so every call takes two seconds."""
    clock = [0.0]

    def monotonic():
        clock[0] += 2.0
        return clock[0]
    monkeypatch.setattr(run_analysis.time, "monotonic", monotonic)


ZERO_TOKEN_FAILURE = (1, {"is_error": True, "result": "",
                          "usage": {"input_tokens": 0, "output_tokens": 0}}, None)


def test_a_fable_call_failing_with_no_token_spent_in_two_seconds_is_the_limit(
        tmp_path, monkeypatch):
    """lessons.md 2026-09-29: the limit showed up as a failed call ending in about two
    seconds with zero tokens, and is read as the limit before anything else."""
    _two_second_clock(monkeypatch)
    record, calls = _ask(tmp_path, monkeypatch, [ZERO_TOKEN_FAILURE] * 3, "fable")
    assert record["limit_reached"] is True and len(calls) == 1
    assert "no token spent" in record["reason"] and "2.0s" in record["reason"]
    # The other sides: tokens spent is a plain failure, retried; an Opus call is
    # not read this way; a slow zero-token failure is not either.
    for name in ("spent", "opus", "slow"):
        (tmp_path / name).mkdir()
    record, calls = _ask(tmp_path / "spent", monkeypatch, [FAILING] * 3, "fable")
    assert "limit_reached" not in record and len(calls) == 3
    record, calls = _ask(tmp_path / "opus", monkeypatch, [ZERO_TOKEN_FAILURE] * 3, "opus")
    assert "limit_reached" not in record and len(calls) == 2
    slow = [0.0]

    def slow_clock():
        slow[0] += run_analysis.LIMIT_SECONDS
        return slow[0]
    monkeypatch.setattr(run_analysis.time, "monotonic", slow_clock)
    record, calls = _ask(tmp_path / "slow", monkeypatch, [ZERO_TOKEN_FAILURE] * 3, "fable")
    assert "limit_reached" not in record and len(calls) == 3


def _run_with_accounting_analyst_answering(tmp_path, monkeypatch, answers, on_fable_limit="opus"):
    """A whole run where the accounting analyst's calls go through the real `ask`
    over a stubbed CLI answering `answers`, and every other agent writes."""
    run = tmp_path / "NVDA" / NVDA_ACCESSION
    bundle = assemble_bundle.build("NVDA", "10-Q", accession=NVDA_ACCESSION,
                                   prior_runs=run.parent.parent)
    assemble_bundle.write(bundle, run)
    written, real_ask = _fake_ask({}), run_analysis.ask
    cli, calls = _cli(list(answers))

    def ask(directory, *, agent, writes, message, spec, log):
        if agent == "accounting-analyst":
            monkeypatch.setattr(run_analysis.subprocess, "run", cli)
            assert spec["model"] == "fable"
            return real_ask(directory, agent=agent, writes=writes, message=message,
                            spec=spec, log=log)
        return written(directory, agent=agent, writes=writes, message=message,
                       spec=spec, log=log)

    monkeypatch.setattr(run_analysis, "ask", ask)
    manifest = run_analysis.run_company(run=run, ticker="NVDA", form="10-Q",
                                        cutoff="2026-08-26", period_end="2026-07-26",
                                        store=run_analysis.cutoff_guard.FIXTURES,
                                        prices=None, control="never",
                                        on_fable_limit=on_fable_limit)
    return run, manifest, calls


def test_a_zero_token_two_second_failure_stops_the_run_and_exits_four(tmp_path, monkeypatch):
    """Under `--on-fable-limit stop`, the rule of 2026-10-06 kept as an option;
    the default, `opus`, is the owner's decision of 2026-10-07 and is tested
    under its own heading below."""
    _two_second_clock(monkeypatch)
    run, manifest, calls = _run_with_accounting_analyst_answering(
        tmp_path, monkeypatch, [ZERO_TOKEN_FAILURE] * 3, on_fable_limit="stop")
    assert len(calls) == 1
    assert manifest["fable_limit_reached"] == ["accounting-analyst"]
    assert "model_fallback" not in manifest
    assert "no token spent" in manifest["agents"]["accounting-analyst"]["reason"]
    assert (run / "analysis_financial.json").is_file() and (run / "memo_ko.md").is_file()
    monkeypatch.setattr(run_analysis, "run_company", lambda **kw: manifest)
    monkeypatch.setattr(run_analysis.interpreter_pin, "enforce", lambda: 0)
    assert run_analysis.main(["--run", str(run), "--ticker", "NVDA", "--form", "10-Q",
                              "--cutoff", "2026-08-26", "--period-end", "2026-07-26",
                              "--on-fable-limit", "stop"]) == 4


def test_a_failure_after_tokens_were_spent_is_retried_and_then_exits_one(tmp_path, monkeypatch):
    _two_second_clock(monkeypatch)
    run, manifest, calls = _run_with_accounting_analyst_answering(
        tmp_path, monkeypatch, [FAILING] * 5)
    assert len(calls) == 3
    assert "fable_limit_reached" not in manifest
    assert manifest["analysis_failure"] == "did not write: accounting-analyst"
    monkeypatch.setattr(run_analysis, "run_company", lambda **kw: manifest)
    monkeypatch.setattr(run_analysis.interpreter_pin, "enforce", lambda: 0)
    assert run_analysis.main(["--run", str(run), "--ticker", "NVDA", "--form", "10-Q",
                              "--cutoff", "2026-08-26", "--period-end", "2026-07-26"]) \
        == run_analysis.FAILED == 1


# --- a stopped run, continued the next night ------------------------------------------------

def _stopped_at_accounting_analyst(tmp_path, monkeypatch):
    """The limit at accounting-analyst, as the limit test above builds it."""
    run = tmp_path / "NVDA" / NVDA_ACCESSION
    bundle = assemble_bundle.build("NVDA", "10-Q", accession=NVDA_ACCESSION,
                                   prior_runs=run.parent.parent)
    assemble_bundle.write(bundle, run)
    written = _fake_ask({})

    def ask(directory, *, agent, writes, message, spec, log):
        if agent == "accounting-analyst":
            return {"agent": agent, "result": "failed", "limit_reached": True,
                    "reason": "You've reached your Fable limit."}
        return written(directory, agent=agent, writes=writes, message=message,
                       spec=spec, log=log)

    monkeypatch.setattr(run_analysis, "ask", ask)
    stopped = run_analysis.run_company(run=run, ticker="NVDA", form="10-Q",
                                       cutoff="2026-08-26", period_end="2026-07-26",
                                       store=run_analysis.cutoff_guard.FIXTURES,
                                       prices=None, control="never",
                                       on_fable_limit="stop")
    assert stopped["fable_limit_reached"] == ["accounting-analyst"]
    return run, stopped


def _counting_ask(seen: dict, **reports):
    """Every agent writes; the directories called are listed in order."""
    written, called = _fake_ask(seen, **reports), []

    def ask(directory, *, agent, writes, message, spec, log):
        called.append(directory.name)
        return written(directory, agent=agent, writes=writes, message=message,
                       spec=spec, log=log)
    return ask, called


@pytest.mark.parametrize("explicit", [False, True])
def test_a_stopped_run_resumes_in_place_and_calls_only_what_had_not_finished(
        tmp_path, monkeypatch, explicit):
    run, stopped = _stopped_at_accounting_analyst(tmp_path, monkeypatch)
    readers_before = {name: stopped["agents"][name] for name in ("numbers-reader",
                                                                   "notes-text-reader")}
    ask, called = _counting_ask({})
    monkeypatch.setattr(run_analysis, "ask", ask)
    manifest = run_analysis.run_company(run=run, ticker="NVDA", form="10-Q",
                                        cutoff="2026-08-26", period_end="2026-07-26",
                                        store=run_analysis.cutoff_guard.FIXTURES,
                                        prices=None, control="never", resume=explicit)
    # only the stopped agent and those after it were called, each once
    assert called == ["accounting-analyst", "valuation-analyst", "valuation-analyst-second-pass"]
    assert manifest["resume_skipped"] == ["numbers-reader", "notes-text-reader",
                                          "financial-analyst"]
    assert manifest["resumed_at"].endswith("Z")
    assert "fable_limit_reached" not in manifest
    assert manifest["analysis_failure"] is None
    assert {name: manifest["agents"][name] for name in readers_before} == readers_before
    assert all(manifest["agents"][name]["result"] == "written" for name in (
        "numbers-reader", "notes-text-reader", "accounting-analyst", "financial-analyst",
        "valuation-analyst", "valuation-analyst-second-pass"))
    for name in ("analysis_accounting.json", "analysis_financial.json", "assumptions.json",
                 "analysis_valuation.json", run_analysis.BEFORE_DRIVERS, run_analysis.FINAL,
                 "memo_ko.md", "baselines.json"):
        assert (run / name).is_file(), name
    assert manifest["analysis_stages"]["quote_gate"] == stopped["analysis_stages"]["quote_gate"]
    assert "analysis_accounting" in manifest["analysis_stages"]
    memo = (run / "memo_ko.md").read_text(encoding="utf-8")
    assert "실행되지 않았습니다" not in memo and "해석이 없습니다" not in memo
    assert agent_inputs.isolation_violations(run) == []
    # Resumed again: nothing is missing now.
    with pytest.raises(run_analysis.NothingToResume, match="nothing to resume"):
        run_analysis.run_company(run=run, ticker="NVDA", form="10-Q", cutoff="2026-08-26",
                                 period_end="2026-07-26",
                                 store=run_analysis.cutoff_guard.FIXTURES, prices=None,
                                 control="never", resume=True)


def _crashing_financial_analyst(seen: dict):
    """Every agent writes; the financial analyst's first answer is a JSON list,
    which `ask` reads as written (it is JSON) and the analysis gate refuses."""
    written, state = _fake_ask(seen), {"financial_calls": 0}

    def ask(directory, *, agent, writes, message, spec, log):
        if agent == "financial-analyst":
            state["financial_calls"] += 1
            if state["financial_calls"] == 1:
                (directory / "analysis_financial.json").write_text("[]")
                return {"agent": agent, "result": "written", "input_tokens": 1,
                        "output_tokens": 1, "model_served": "claude-fable-5-1",
                        "attempts": [{"attempt": 1, "model_served": "claude-fable-5-1",
                                      "input_tokens": 1, "output_tokens": 1,
                                      "outcome": "written"}]}
        return written(directory, agent=agent, writes=writes, message=message,
                       spec=spec, log=log)
    return ask


def _fable_served_ask(seen: dict):
    """Every agent writes, served by Fable, as the real `ask` records it."""
    written, called = _fake_ask(seen), []

    def ask(directory, *, agent, writes, message, spec, log):
        called.append(directory.name)
        return dict(written(directory, agent=agent, writes=writes, message=message,
                            spec=spec, log=log), model_served="claude-fable-5-1")
    return ask, called


def _run_keyword(control: str = "never") -> dict:
    return dict(ticker="NVDA", form="10-Q", cutoff="2026-08-26", period_end="2026-07-26",
                store=run_analysis.cutoff_guard.FIXTURES, prices=None, control=control)


def test_a_crash_at_the_analysis_gate_leaves_the_passed_analyst_on_record_and_resumes(
        tmp_path, monkeypatch):
    """The accounting analyst passed, the financial analyst wrote a JSON list,
    and the gate raised before `finish`. The record of every call that returned
    is already in the manifest, with what the run stopped on and no finish
    marker; the next invocation resumes it, calling the financial analyst and
    what comes after and never the accounting analyst again. Then the finished
    run is refused on resume."""
    run = tmp_path / "NVDA" / NVDA_ACCESSION
    assemble_bundle.write(assemble_bundle.build("NVDA", "10-Q", accession=NVDA_ACCESSION,
                                                prior_runs=run.parent.parent), run)
    monkeypatch.setattr(run_analysis, "ask", _crashing_financial_analyst({}))
    with pytest.raises(run_analysis.analysis_check.AnalysisInputError,
                       match="the financial analysis is not a JSON object"):
        run_analysis.run_company(run=run, **_run_keyword())
    manifest = json.loads((run / "input_manifest.json").read_text(encoding="utf-8"))
    assert run_analysis.FINISH_MARKER not in manifest and "fable_limit_reached" not in manifest
    assert manifest["stopped_on"] == ("AnalysisInputError: the financial analysis is not a "
                                      "JSON object")
    assert {name: record["result"] for name, record in manifest["agents"].items()} == {
        "numbers-reader": "written", "notes-text-reader": "written",
        "accounting-analyst": "written", "financial-analyst": "written"}
    assert (run / "analysis_accounting.json").is_file()
    assert not (run / "analysis_financial.json").exists()           # the gate refused it
    # the command: the gate's refusal is a stop like any other, exit 2 and a line
    monkeypatch.setattr(run_analysis.interpreter_pin, "enforce", lambda: 0)
    monkeypatch.setattr(run_analysis, "run_company", lambda **kw: (_ for _ in ()).throw(
        run_analysis.analysis_check.AnalysisInputError("the financial analysis is not a JSON object")))
    assert run_analysis.main(_main_command(run)) == run_analysis.BAD_INPUT == 2
    monkeypatch.undo()
    # resumed, by default: the record says what passed, and only the rest runs
    ask, called = _fable_served_ask({})
    monkeypatch.setattr(run_analysis, "ask", ask)
    manifest = run_analysis.run_company(run=run, **_run_keyword())
    assert called == ["financial-analyst", "valuation-analyst", "valuation-analyst-second-pass"]
    # the first financial-analyst call was paid for: its attempt stays on record
    # in front of the resume's own, numbered through, the tokens summed over both
    financial = manifest["agents"]["financial-analyst"]
    assert [row["attempt"] for row in financial["attempts"]] == [1, 2]
    assert [row["outcome"] for row in financial["attempts"]] == ["written", "written"]
    assert financial["input_tokens"] == 2 and financial["output_tokens"] == 2
    assert financial["attempt"] == 2 and financial["result"] == "written"
    assert fable_batch.agent_tokens(financial) == 4
    # the other side: an agent called for the first time holds only its own
    # attempt (the stub writes the older one-call shape; the real `ask` lists it)
    valuation = manifest["agents"]["valuation-analyst"]
    assert len(run_analysis.attempts_of(valuation)) == 1 and valuation["input_tokens"] == 1
    # and the batch is sized from the total the filing cost: the financial
    # analyst's two calls and the two valuation passes, each Fable-served
    assert fable_batch.on_record(run.parent.parent) == {f"NVDA/{NVDA_ACCESSION}": 8}
    assert manifest["resume_skipped"] == ["numbers-reader", "notes-text-reader",
                                          "accounting-analyst"]
    assert manifest["resumed_from"] == ("stopped on AnalysisInputError: the financial analysis "
                                        "is not a JSON object")
    assert "stopped_on" not in manifest and run_analysis.FINISH_MARKER in manifest
    assert manifest["analysis_failure"] is None
    assert (run / "analysis_financial.json").is_file() and (run / "memo_ko.md").is_file()
    assert agent_inputs.isolation_violations(run) == []
    # the finished run: --resume says nothing to resume, and without it the
    # run on record is refused
    monkeypatch.setattr(run_analysis, "ask",
                        lambda *a, **k: (_ for _ in ()).throw(AssertionError("an agent ran")))
    with pytest.raises(run_analysis.NothingToResume):
        run_analysis.run_company(run=run, resume=True, **_run_keyword())
    with pytest.raises(run_analysis.RunError, match="did not stop at the limit"):
        run_analysis.run_company(run=run, **_run_keyword())


def test_a_crash_in_the_calculator_after_both_analysts_leaves_both_on_record_and_resumes(
        tmp_path, monkeypatch):
    """`calculate(BEFORE_DRIVERS)` refuses an input after both analysts passed:
    both are on record, the run stops on the calculator's error, and the resume
    calls the valuation analyst and nothing before it."""
    run = tmp_path / "NVDA" / NVDA_ACCESSION
    assemble_bundle.write(assemble_bundle.build("NVDA", "10-Q", accession=NVDA_ACCESSION,
                                                prior_runs=run.parent.parent), run)
    monkeypatch.setattr(run_analysis, "ask", _fake_ask({}))
    real_calculate, state = run_analysis.calculator.calculate, {"raised": False}

    def calculate(**keyword):
        if "accounting" in keyword and "assumptions" not in keyword and not state["raised"]:
            state["raised"] = True
            raise run_analysis.calculator.CalculatorInputError("planted: an input is not there")
        return real_calculate(**keyword)

    monkeypatch.setattr(run_analysis.calculator, "calculate", calculate)
    with pytest.raises(run_analysis.calculator.CalculatorInputError, match="planted"):
        run_analysis.run_company(run=run, **_run_keyword())
    manifest = json.loads((run / "input_manifest.json").read_text(encoding="utf-8"))
    assert manifest["stopped_on"] == "CalculatorInputError: planted: an input is not there"
    assert run_analysis.FINISH_MARKER not in manifest
    assert all(manifest["agents"][name]["result"] == "written" for name in (
        "accounting-analyst", "financial-analyst"))
    assert (run / "analysis_accounting.json").is_file() and (run / "analysis_financial.json").is_file()
    assert not (run / run_analysis.BEFORE_DRIVERS).exists()
    ask, called = _counting_ask({})
    monkeypatch.setattr(run_analysis, "ask", ask)
    manifest = run_analysis.run_company(run=run, **_run_keyword())
    assert called == ["valuation-analyst", "valuation-analyst-second-pass"]
    assert manifest["resume_skipped"] == ["numbers-reader", "notes-text-reader",
                                          "accounting-analyst", "financial-analyst"]
    assert manifest["resumed_from"].startswith("stopped on CalculatorInputError: planted")
    assert "stopped_on" not in manifest and manifest["analysis_failure"] is None
    assert (run / run_analysis.BEFORE_DRIVERS).is_file() and (run / run_analysis.FINAL).is_file()


def _stopped_at(tmp_path, monkeypatch, stopped_agent: str, control: str,
                model: str | None = None, numbers_report: str = NUMBERS_REPORT):
    """The limit at `stopped_agent`; every other agent writes."""
    run = tmp_path / "NVDA" / NVDA_ACCESSION
    bundle = assemble_bundle.build("NVDA", "10-Q", accession=NVDA_ACCESSION,
                                   prior_runs=run.parent.parent)
    assemble_bundle.write(bundle, run)
    written = _fake_ask({}, numbers_report=numbers_report)

    def ask(directory, *, agent, writes, message, spec, log):
        if agent == stopped_agent:
            return {"agent": agent, "result": "failed", "limit_reached": True,
                    "reason": "You've reached your Fable limit."}
        return written(directory, agent=agent, writes=writes, message=message,
                       spec=spec, log=log)

    monkeypatch.setattr(run_analysis, "ask", ask)
    stopped = run_analysis.run_company(run=run, ticker="NVDA", form="10-Q",
                                       cutoff="2026-08-26", period_end="2026-07-26",
                                       store=run_analysis.cutoff_guard.FIXTURES,
                                       prices=None, control=control, model=model,
                                       on_fable_limit="stop")
    assert stopped["fable_limit_reached"] == [stopped_agent]
    return run, stopped


def _resumed(run, monkeypatch, control: str, model: str | None = None, **reports):
    """`reports`: what the stubbed agents write, as `_fake_ask` takes them."""
    ask, called = _counting_ask({}, **reports)
    monkeypatch.setattr(run_analysis, "ask", ask)
    manifest = run_analysis.run_company(run=run, ticker="NVDA", form="10-Q",
                                        cutoff="2026-08-26", period_end="2026-07-26",
                                        store=run_analysis.cutoff_guard.FIXTURES,
                                        prices=None, control=control, model=model)
    return manifest, called


def _main_command(run, *extra: str) -> list[str]:
    return ["--run", str(run), "--ticker", "NVDA", "--form", "10-Q", "--cutoff",
            "2026-08-26", "--period-end", "2026-07-26", "--control", "never", *extra]


def test_a_resume_under_another_model_than_the_stopped_run_s_is_refused(tmp_path, monkeypatch):
    """Stopped under the definitions' own models (no --model), resumed with
    `--model opus`: refused before any agent is called, exit 2, and the stopped
    run's record stands as it was."""
    run, stopped = _stopped_at_accounting_analyst(tmp_path, monkeypatch)
    assert "model_override" not in stopped
    before = (run / "input_manifest.json").read_bytes()
    with pytest.raises(run_analysis.RunError, match="the run stopped under the definitions' "
                       "own models; a resume under opus would mix models, which the record "
                       "cannot compare"):
        _resumed(run, monkeypatch, "never", model="opus")
    monkeypatch.setattr(run_analysis.interpreter_pin, "enforce", lambda: 0)
    monkeypatch.setattr(run_analysis, "ask",
                        lambda *a, **k: (_ for _ in ()).throw(AssertionError("an agent ran")))
    assert run_analysis.main(_main_command(run, "--model", "opus")) == run_analysis.BAD_INPUT == 2
    assert (run / "input_manifest.json").read_bytes() == before
    # the same resume under the stopped run's models runs
    manifest, called = _resumed(run, monkeypatch, "never")
    assert called == ["accounting-analyst", "valuation-analyst", "valuation-analyst-second-pass"]
    assert "model_override" not in manifest and manifest["analysis_failure"] is None


def test_a_resume_names_the_stopped_run_s_model_or_is_refused_and_the_override_names_what_ran(
        tmp_path, monkeypatch):
    """Stopped with `--model claude-fable-5-1`: a resume naming none is refused,
    one naming the same runs, and the manifest's `model_override.applies_to`
    lists only the agents called on resume -- the stopped run's own override,
    which named the four it called, is not carried forward."""
    run, stopped = _stopped_at(tmp_path, monkeypatch, "accounting-analyst", "never",
                               model="claude-fable-5-1")
    assert stopped["model_override"]["model"] == "claude-fable-5-1"
    assert stopped["model_override"]["applies_to"] == [
        "numbers-reader", "notes-text-reader", "accounting-analyst", "financial-analyst"]
    with pytest.raises(run_analysis.RunError, match="the run stopped under claude-fable-5-1; "
                       "a resume under the definitions' own models would mix models, which "
                       "the record cannot compare"):
        _resumed(run, monkeypatch, "never")
    with pytest.raises(run_analysis.RunError, match="a resume under opus would mix models"):
        _resumed(run, monkeypatch, "never", model="opus")
    monkeypatch.setattr(run_analysis.interpreter_pin, "enforce", lambda: 0)
    monkeypatch.setattr(run_analysis, "ask",
                        lambda *a, **k: (_ for _ in ()).throw(AssertionError("an agent ran")))
    assert run_analysis.main(_main_command(run, "--resume")) == run_analysis.BAD_INPUT == 2
    assert json.loads((run / "input_manifest.json").read_text())["fable_limit_reached"] == [
        "accounting-analyst"]
    manifest, called = _resumed(run, monkeypatch, "never", model="claude-fable-5-1")
    assert called == ["accounting-analyst", "valuation-analyst", "valuation-analyst-second-pass"]
    assert manifest["model_override"]["model"] == "claude-fable-5-1"
    assert manifest["model_override"]["applies_to"] == called
    assert manifest["resume_skipped"] == ["numbers-reader", "notes-text-reader",
                                          "financial-analyst"]
    assert "fable_limit_reached" not in manifest and manifest["analysis_failure"] is None
    # an agent on record whose own record asked for another model is a mixed record
    edited = json.loads((run / "input_manifest.json").read_text())
    edited["fable_limit_reached"] = ["valuation-analyst-second-pass"]
    edited["agents"]["financial-analyst"]["model_requested"] = "opus"
    (run / "input_manifest.json").write_text(json.dumps(edited))
    with pytest.raises(run_analysis.RunError, match="financial-analyst on record asked for opus"):
        _resumed(run, monkeypatch, "never", model="claude-fable-5-1")


def _stopped_recording_models(tmp_path, monkeypatch, stopped_agent: str):
    """The limit at `stopped_agent`; every other agent writes and records the
    model it asked for, as the real `ask` does."""
    run = tmp_path / "NVDA" / NVDA_ACCESSION
    assemble_bundle.write(assemble_bundle.build("NVDA", "10-Q", accession=NVDA_ACCESSION,
                                                prior_runs=run.parent.parent), run)
    written = _fake_ask({})

    def ask(directory, *, agent, writes, message, spec, log):
        if agent == stopped_agent:
            return {"agent": agent, "result": "failed", "limit_reached": True,
                    "reason": "You've reached your Fable limit.", "model_requested": spec["model"]}
        return dict(written(directory, agent=agent, writes=writes, message=message,
                            spec=spec, log=log), model_requested=spec["model"])

    monkeypatch.setattr(run_analysis, "ask", ask)
    stopped = run_analysis.run_company(run=run, on_fable_limit="stop", **_run_keyword())
    assert stopped["fable_limit_reached"] == [stopped_agent]
    return run, stopped


def _definitions_with(tmp_path, monkeypatch, edits: dict[str, str]) -> Path:
    """A copy of the committed definitions with `model:` lines edited, in place
    of the committed ones for the rest of the test."""
    copy = tmp_path / "definitions"
    if not copy.is_dir():
        shutil.copytree(run_analysis.DEFINITIONS, copy)
    for name, model in edits.items():
        path = copy / f"{name}.md"
        text, count = re.subn(r"^model: .*$", f"model: {model}", path.read_text(encoding="utf-8"),
                              count=1, flags=re.M)
        assert count == 1, name
        path.write_text(text, encoding="utf-8")
    monkeypatch.setattr(run_analysis, "DEFINITIONS", copy)
    return copy


def test_a_definition_edited_between_the_nights_is_refused_on_resume(tmp_path, monkeypatch):
    """Stopped under the definitions' own models at the accounting analyst, with
    the financial analyst on record asking for fable. The accounting analyst's
    definition edited to opus before the resume: refused, exit 2, naming the
    model the record ran under and the one the definition asks for now. The same
    for the valuation analyst's, which has no record of its own but is in the
    analysts' layer. Unchanged, the run resumes."""
    run, stopped = _stopped_recording_models(tmp_path, monkeypatch, "accounting-analyst")
    assert stopped["agents"]["financial-analyst"]["model_requested"] == "fable"
    assert "model_override" not in stopped
    before = (run / "input_manifest.json").read_bytes()
    _definitions_with(tmp_path, monkeypatch, {"accounting-analyst": "opus"})
    monkeypatch.setattr(run_analysis, "ask",
                        lambda *a, **k: (_ for _ in ()).throw(AssertionError("an agent ran")))
    with pytest.raises(run_analysis.RunError, match="the run stopped under fable; the definition "
                       "of accounting-analyst now asks for opus, which the record cannot compare"):
        run_analysis.run_company(run=run, **_run_keyword())
    monkeypatch.setattr(run_analysis.interpreter_pin, "enforce", lambda: 0)
    assert run_analysis.main(_main_command(run)) == run_analysis.BAD_INPUT == 2
    assert (run / "input_manifest.json").read_bytes() == before
    _definitions_with(tmp_path, monkeypatch, {"accounting-analyst": "fable",
                                              "valuation-analyst": "opus"})
    with pytest.raises(run_analysis.RunError, match="the definition of valuation-analyst now "
                       "asks for opus"):
        run_analysis.run_company(run=run, **_run_keyword())
    # unchanged definitions: the resume runs, and only what had not finished
    _definitions_with(tmp_path, monkeypatch, {"valuation-analyst": "fable"})
    ask, called = _counting_ask({})
    monkeypatch.setattr(run_analysis, "ask", ask)
    manifest = run_analysis.run_company(run=run, **_run_keyword())
    assert called == ["accounting-analyst", "valuation-analyst", "valuation-analyst-second-pass"]
    assert manifest["analysis_failure"] is None and "stopped_on" not in manifest


def test_a_stale_override_is_never_carried_forward_by_finish(tmp_path):
    run = tmp_path / "run"
    run.mkdir()
    (run / "input_manifest.json").write_text(json.dumps({
        "model_override": {"model": "opus", "applies_to": ["numbers-reader"]},
        "agents": {"numbers-reader": {"result": "written", "model_requested": "opus"}}}))
    agents = {"numbers-reader": {"result": "written", "model_requested": "opus"},
              "notes-text-reader": {"result": "written"}}
    manifest = run_analysis.finish(run, agents, {}, None, None, skipped=["numbers-reader"])
    assert "model_override" not in manifest
    manifest = run_analysis.finish(run, agents, {}, None, "opus", skipped=["numbers-reader"])
    assert manifest["model_override"]["applies_to"] == ["notes-text-reader"]


def test_a_run_stopped_at_the_control_resumes_and_calls_the_control_only(tmp_path, monkeypatch):
    run, stopped = _stopped_at(tmp_path, monkeypatch, "control-single-agent", "always")
    assert (run / run_analysis.CONTROL_DIRNAME).is_dir()        # built the night it stopped
    assert not any((run / name).is_file() for name in run_analysis.CONTROL_WRITES)
    manifest, called = _resumed(run, monkeypatch, "always")
    assert called == [run_analysis.CONTROL_DIRNAME]            # the control's directory
    assert manifest["resume_skipped"] == ["numbers-reader", "notes-text-reader",
                                          "accounting-analyst", "financial-analyst",
                                          "valuation-analyst", "valuation-analyst-second-pass"]
    assert "fable_limit_reached" not in manifest and manifest["analysis_failure"] is None
    assert manifest["agents"]["control-single-agent"]["result"] == "written"
    assert all((run / name).is_file() for name in run_analysis.CONTROL_WRITES)
    assert set(manifest["analysis_stages"]["control"]) == {"accounting", "financial",
                                                           "assumptions"}
    assert agent_inputs.isolation_violations(run) == []
    # The other side: a control directory on a run that is not resumed is built once.
    with pytest.raises(run_analysis.RunError, match="built once"):
        run_analysis.run_control(run, run.parent / "logs")


def test_a_limit_at_one_reader_leaves_the_other_on_record_and_never_calls_it_again(
        tmp_path, monkeypatch):
    run, stopped = _stopped_at(tmp_path, monkeypatch, "notes-text-reader", "never")
    # the finished reader's report was gated into the run root the night it stopped
    assert (run / "report_numbers.md").is_file()
    assert not (run / "report_notes_text.md").exists()
    assert stopped["agents"]["numbers-reader"]["result"] == "written"
    assert "quote_gate" not in stopped["analysis_stages"]
    numbers_before = (run / "report_numbers.md").read_bytes()
    manifest, called = _resumed(run, monkeypatch, "never")
    assert called[0] == "notes-text-reader" and "numbers-reader" not in called
    assert sorted(called) == ["accounting-analyst", "financial-analyst", "notes-text-reader",
                              "valuation-analyst", "valuation-analyst-second-pass"]
    assert manifest["resume_skipped"] == ["numbers-reader"]
    assert (run / "report_numbers.md").read_bytes() == numbers_before
    assert manifest["agents"]["numbers-reader"] == stopped["agents"]["numbers-reader"]
    assert "fable_limit_reached" not in manifest and manifest["analysis_failure"] is None
    assert manifest["analysis_stages"]["quote_gate"] == {"dropped": 0}
    assert (run / "report_notes_text.md").is_file() and (run / "memo_ko.md").is_file()
    assert agent_inputs.isolation_violations(run) == []


# One id on an item of each reader. The numbers reader's second item quotes a
# value the trends row does not print, so its row is on the drop list the night
# the numbers reader is gated; the notes reader's item quotes the MD&A's first
# paragraph, as FLAGGING_TWO does, under the numbers item's id.
SHARED_ID = "earnings_quality_accruals_rising"
NUMBERS_WITH_A_BAD_QUOTE = NUMBERS_REPORT + '''```json
{ "id": "earnings_quality_planted_bad_quote", "what_changed": "x", "account": "a",
  "expected_direction": "up", "horizon": "h",
  "quote": "\\"value\\": 1.0",
  "paragraph_id": "0001045810-26-000075:trends:days_sales_outstanding:2026-04-27..2026-07-26" }
```
'''
NOTES_SHARING_THE_ID = '''```json
[{ "id": "earnings_quality_accruals_rising", "paragraph_id": "0001045810-26-000075:mdna:1",
   "quote": "Analysis of Financial Condition" }]
```
'''


def test_a_resume_gates_only_the_reader_it_called_and_appends_its_rows(tmp_path, monkeypatch):
    """The limit at the notes reader, the numbers reader gated alone that night
    with one row dropped. Resumed, the notes reader writes an item under the
    numbers item's id: the run-root report_numbers.md and the night's drop row
    stand byte for byte, the notes report is gated alone and held to the ids
    standing in the report already gated, so its item under the shared id is
    dropped as a twin and its row appended after the earlier one -- the one
    id names the numbers item, as it would have on a fresh run."""
    run, stopped = _stopped_at(tmp_path, monkeypatch, "notes-text-reader", "never",
                               numbers_report=NUMBERS_WITH_A_BAD_QUOTE)
    assert [(row["report"], row["item_id"]) for row in stopped["dropped_items"]] == [
        ("report_numbers.md", "earnings_quality_planted_bad_quote")]
    assert "does not string-match" in stopped["dropped_items"][0]["reason"]
    numbers_before = (run / "report_numbers.md").read_bytes()
    assert SHARED_ID in numbers_before.decode("utf-8")
    twin_citing = _analysis("accounting", SHARED_ID)
    twin_citing["anomalies"].append(dict(twin_citing["anomalies"][0],
                                         id="earnings_versus_cash_cites_a_fallen_item",
                                         evidence=["earnings_quality_planted_bad_quote"]))
    # a reconciliation row naming the shared id as the notes item it fell from,
    # and one naming it as the numbers item it stands as (with no standing
    # notes item to pair it with, that row falls on its notes side alone)
    twin_citing["reconciliation"] = [
        {"notes_item": SHARED_ID, "numbers_items": [], "outcome": "unresolved", "why": "x"},
        {"notes_item": "earnings_quality_no_such_item", "numbers_items": [SHARED_ID],
         "outcome": "unresolved", "why": "y"}]
    manifest, called = _resumed(run, monkeypatch, "never", notes_report=NOTES_SHARING_THE_ID,
                                numbers_report=NUMBERS_WITH_A_BAD_QUOTE,
                                accounting_analysis=twin_citing)
    assert "numbers-reader" not in called
    # The analysis gate: a bare citation of the shared id is refused, as a fresh
    # run would have refused it -- the notes twin fell and may still be printed,
    # so by id alone the citation does not name one standing item -- and so is
    # the citation of the id dropped from the one report it stood in; the
    # reconciliation row naming the shared id as the notes item it fell from is
    # refused on that side, the row naming it as the numbers item it stands as
    # falls on its own notes side alone.
    accounting = json.loads((run / "analysis_accounting.json").read_text(encoding="utf-8"))
    assert accounting["anomalies"] == []
    assert [row["where"] for row in accounting["dropped_items"]] == [
        "reconciliation[0]", "reconciliation[1]", "anomalies[0]", "anomalies[1]"]
    assert accounting["dropped_items"][0]["reason"] == (
        f"notes_item {SHARED_ID!r} is not an item of report_notes_text.md")
    assert accounting["dropped_items"][1]["reason"] == (
        "notes_item 'earnings_quality_no_such_item' is not an item of report_notes_text.md")
    assert accounting["dropped_items"][2]["reason"] == (
        f"evidence: {SHARED_ID!r} is an id the quote gate dropped from a report this "
        "analyst saw, so by id alone it does not name one standing item")
    assert "earnings_quality_planted_bad_quote" in accounting["dropped_items"][3]["reason"]
    assert run_analysis.excluded_by_report(run) == {
        "report_numbers.md": {"earnings_quality_planted_bad_quote"},
        "report_notes_text.md": {SHARED_ID}}
    assert (run / "report_numbers.md").read_bytes() == numbers_before
    assert manifest["dropped_items"][:1] == stopped["dropped_items"]        # appended after
    assert [(row["report"], row["item_id"]) for row in manifest["dropped_items"]] == [
        ("report_numbers.md", "earnings_quality_planted_bad_quote"),
        ("report_notes_text.md", SHARED_ID)]
    assert ("on more than one item in this run: it is on an item of report_numbers.md"
            in manifest["dropped_items"][1]["reason"])
    assert manifest["counts"]["dropped_items"] == 2
    assert manifest["analysis_stages"]["quote_gate"] == {"dropped": 1}      # this night's
    notes = (run / "report_notes_text.md").read_text(encoding="utf-8")
    assert SHARED_ID not in notes and "removed 1 item(s)" in notes
    assert manifest["analysis_failure"] is None
    assert agent_inputs.isolation_violations(run) == []
    # The other side: a fresh run gates both readers in one call, and the shared
    # id is dropped from both, as the gate's rule says.
    fresh = tmp_path / "fresh" / "NVDA" / NVDA_ACCESSION
    assemble_bundle.write(assemble_bundle.build("NVDA", "10-Q", accession=NVDA_ACCESSION,
                                                prior_runs=fresh.parent.parent), fresh)
    monkeypatch.setattr(run_analysis, "ask", _fake_ask(
        {}, notes_report=NOTES_SHARING_THE_ID, numbers_report=NUMBERS_WITH_A_BAD_QUOTE))
    manifest = run_analysis.run_company(run=fresh, ticker="NVDA", form="10-Q",
                                        cutoff="2026-08-26", period_end="2026-07-26",
                                        store=run_analysis.cutoff_guard.FIXTURES,
                                        prices=None, control="never")
    assert [(row["report"], row["item_id"]) for row in manifest["dropped_items"]] == [
        ("report_numbers.md", SHARED_ID),
        ("report_numbers.md", "earnings_quality_planted_bad_quote"),
        ("report_notes_text.md", SHARED_ID)]
    assert all("on more than one item" in row["reason"]
               for row in manifest["dropped_items"] if row["item_id"] == SHARED_ID)
    assert manifest["analysis_stages"]["quote_gate"] == {"dropped": 3}
    assert SHARED_ID not in (fresh / "report_numbers.md").read_text(encoding="utf-8")
    assert SHARED_ID not in (fresh / "report_notes_text.md").read_text(encoding="utf-8")


def test_a_run_that_did_not_stop_is_not_resumed(tmp_path, monkeypatch, finished, capsys):
    run, _, _ = finished
    keyword = dict(ticker="NVDA", form="10-Q", cutoff="2026-08-26", period_end="2026-07-26",
                   store=run_analysis.cutoff_guard.FIXTURES, prices=None, control="never")
    # a finished run: `--resume` says nothing to resume and exits 0, without it the
    # run on record is refused, and nothing is called either way
    monkeypatch.setattr(run_analysis, "ask",
                        lambda *a, **k: (_ for _ in ()).throw(AssertionError("an agent ran")))
    with pytest.raises(run_analysis.NothingToResume):
        run_analysis.run_company(run=run, resume=True, **keyword)
    with pytest.raises(run_analysis.RunError, match="did not stop at the limit"):
        run_analysis.run_company(run=run, **keyword)
    monkeypatch.setattr(run_analysis.interpreter_pin, "enforce", lambda: 0)
    command = ["--run", str(run), "--ticker", "NVDA", "--form", "10-Q", "--cutoff",
               "2026-08-26", "--period-end", "2026-07-26", "--control", "never"]
    assert run_analysis.main(command + ["--resume"]) == 0
    assert "nothing to resume" in capsys.readouterr().out
    assert run_analysis.main(command) == run_analysis.BAD_INPUT
    # a run that failed some other way is not resumed either
    failed = tmp_path / "NVDA" / NVDA_ACCESSION
    assemble_bundle.write(assemble_bundle.build("NVDA", "10-Q", accession=NVDA_ACCESSION,
                                                prior_runs=failed.parent.parent), failed)
    with pytest.raises(run_analysis.RunError, match="no agent has run"):
        run_analysis.run_company(run=failed, resume=True, **keyword)
    manifest = json.loads((failed / "input_manifest.json").read_text())
    manifest["agents"] = {"numbers-reader": {"result": "failed", "reason": "exit 1"}}
    manifest["analysis_failure"] = "a reader failed twice"
    manifest[run_analysis.FINISH_MARKER] = "2026-10-07T00:00:00Z"   # finish wrote it
    (failed / "input_manifest.json").write_text(json.dumps(manifest))
    with pytest.raises(run_analysis.RunError, match="did not stop at the limit"):
        run_analysis.run_company(run=failed, resume=True, **keyword)
    # without the marker the same manifest is a run that stopped before finish
    # with nothing on record: --resume is refused as such, and nothing is run over
    del manifest[run_analysis.FINISH_MARKER]
    (failed / "input_manifest.json").write_text(json.dumps(manifest))
    with pytest.raises(run_analysis.RunError, match="no agent's gated output is on record"):
        run_analysis.run_company(run=failed, resume=True, **keyword)


def test_the_limit_stops_the_call_at_once_and_says_so(tmp_path, monkeypatch):
    limit = (1, {"is_error": True,
                 "result": "You've reached your Fable limit. Switch to another model to continue."},
             None)
    record, calls = _ask(tmp_path, monkeypatch, [limit] * 3, "fable")
    assert record["limit_reached"] is True and len(calls) == 1
    assert "Fable limit" in record["reason"]


def test_the_limit_stops_the_run_where_it_stands_publishes_what_finished_and_exits_four(
        tmp_path, monkeypatch):
    run = tmp_path / "NVDA" / NVDA_ACCESSION
    bundle = assemble_bundle.build("NVDA", "10-Q", accession=NVDA_ACCESSION,
                                   prior_runs=run.parent.parent)
    assemble_bundle.write(bundle, run)
    written = _fake_ask({})

    def ask(directory, *, agent, writes, message, spec, log):
        if agent == "accounting-analyst":
            return {"agent": agent, "result": "failed", "limit_reached": True,
                    "reason": "You've reached your Fable limit."}
        return written(directory, agent=agent, writes=writes, message=message,
                       spec=spec, log=log)

    monkeypatch.setattr(run_analysis, "ask", ask)
    manifest = run_analysis.run_company(run=run, ticker="NVDA", form="10-Q",
                                        cutoff="2026-08-26", period_end="2026-07-26",
                                        store=run_analysis.cutoff_guard.FIXTURES,
                                        prices=None, control="always",
                                        on_fable_limit="stop")
    assert manifest["fable_limit_reached"] == ["accounting-analyst"]
    assert "stopped there" in manifest["analysis_failure"]
    assert "valuation-analyst" not in manifest["agents"]       # nothing ran past it
    assert "control-single-agent" not in manifest["agents"]
    assert not (run / run_analysis.BEFORE_DRIVERS).exists()
    assert not (run / "analysis_accounting.json").exists()
    # What finished is published: the financial analyst's output gated into its
    # file, and the memo and baselines written from what exists.
    assert (run / "analysis_financial.json").is_file()
    assert "analysis_financial" in manifest["analysis_stages"]
    assert "analysis_accounting" not in manifest["analysis_stages"]
    assert (run / run_analysis.FINAL).is_file()
    assert manifest["analysis_stages"]["baselines"] == "written"
    assert (run / "baselines.json").is_file()
    memo = (run / "memo_ko.md").read_text(encoding="utf-8")
    assert ("회계 분석이 실행되지 않았습니다. 이유: accounting-analyst answered the Fable limit "
            "(You've reached your Fable limit.); nothing fell back to another model") in memo
    assert "재무 분석이 실행되지 않았습니다" not in memo
    assert ("가치평가 분석가의 해석이 없습니다. 이유: valuation-analyst did not run: the Fable "
            "limit was reached at accounting-analyst and the run stopped there") in memo
    # The limit's exit code is its own, and not the interpreter pin's: main()
    # returns the pin's before the run starts, the limit's after it.
    assert run_analysis.LIMIT_REACHED == 4
    assert run_analysis.interpreter_pin.WRONG_INTERPRETER == 3
    assert run_analysis.LIMIT_REACHED != run_analysis.interpreter_pin.WRONG_INTERPRETER
    command = ["--run", str(run), "--ticker", "NVDA", "--form", "10-Q",
               "--cutoff", "2026-08-26", "--period-end", "2026-07-26",
               "--on-fable-limit", "stop"]
    monkeypatch.setattr(run_analysis, "run_company", lambda **kw: manifest)
    monkeypatch.setattr(run_analysis.interpreter_pin, "enforce", lambda: 0)
    assert run_analysis.main(command) == run_analysis.LIMIT_REACHED
    monkeypatch.setattr(run_analysis, "run_company",
                        lambda **kw: (_ for _ in ()).throw(AssertionError("the run started")))
    monkeypatch.setattr(run_analysis.interpreter_pin, "enforce",
                        lambda: run_analysis.interpreter_pin.WRONG_INTERPRETER)
    assert run_analysis.main(command) == run_analysis.interpreter_pin.WRONG_INTERPRETER


def test_the_limit_at_the_valuation_analyst_still_publishes_both_analyses_and_the_memo(
        tmp_path, monkeypatch):
    run = tmp_path / "NVDA" / NVDA_ACCESSION
    bundle = assemble_bundle.build("NVDA", "10-Q", accession=NVDA_ACCESSION,
                                   prior_runs=run.parent.parent)
    assemble_bundle.write(bundle, run)
    written = _fake_ask({})

    def ask(directory, *, agent, writes, message, spec, log):
        if agent == "valuation-analyst":
            return {"agent": agent, "result": "failed", "limit_reached": True,
                    "reason": "You've reached your Fable limit."}
        return written(directory, agent=agent, writes=writes, message=message,
                       spec=spec, log=log)

    monkeypatch.setattr(run_analysis, "ask", ask)
    manifest = run_analysis.run_company(run=run, ticker="NVDA", form="10-Q",
                                        cutoff="2026-08-26", period_end="2026-07-26",
                                        store=run_analysis.cutoff_guard.FIXTURES,
                                        prices=None, control="always",
                                        on_fable_limit="stop")
    assert manifest["fable_limit_reached"] == ["valuation-analyst"]
    assert "valuation-analyst-second-pass" not in manifest["agents"]
    assert "control-single-agent" not in manifest["agents"]
    for name in ("analysis_accounting.json", "analysis_financial.json", run_analysis.FINAL,
                 "memo_ko.md", "baselines.json"):
        assert (run / name).is_file(), name
    assert not (run / "assumptions.json").exists()
    memo = (run / "memo_ko.md").read_text(encoding="utf-8")
    assert "가치평가 분석가의 해석이 없습니다. 이유: valuation-analyst answered the Fable limit" in memo
    assert "회계 분석이 실행되지 않았습니다" not in memo


def _run_with_control(tmp_path, monkeypatch, control, golden=None):
    """`golden` plants the answer of `is_golden_filing`; None leaves the real one,
    which reads this tree."""
    run = tmp_path / "NVDA" / NVDA_ACCESSION
    bundle = assemble_bundle.build("NVDA", "10-Q", accession=NVDA_ACCESSION,
                                   prior_runs=run.parent.parent)
    assemble_bundle.write(bundle, run)
    monkeypatch.setattr(run_analysis, "ask", _fake_ask({}))
    if golden is not None:
        monkeypatch.setattr(run_analysis, "is_golden_filing",
                            lambda accession: (golden, f"planted: {golden}"))
    return run_analysis.run_company(run=run, ticker="NVDA", form="10-Q",
                                    cutoff="2026-08-26", period_end="2026-07-26",
                                    store=run_analysis.cutoff_guard.FIXTURES,
                                    prices=None, control=control)


def test_the_control_runs_on_a_golden_filing_and_skips_the_rest(tmp_path, monkeypatch):
    skipped = _run_with_control(tmp_path, monkeypatch, "auto", golden=False)
    assert "control-single-agent" not in skipped["agents"]
    assert skipped["analysis_stages"]["control"] == "skipped: planted: False"
    assert skipped["control_reason"] == "planted: False"
    assert skipped["analysis_failure"] is None
    ran = _run_with_control(tmp_path / "g", monkeypatch, "auto", golden=True)
    assert ran["agents"]["control-single-agent"]["result"] == "written"
    assert ran["control_reason"] == "planted: True"


def test_this_tree_holds_the_cases_directory_with_no_approved_case_and_the_manifest_says_so(
        tmp_path, monkeypatch):
    """The evals branch landed: this tree holds `evals/golden/cases` and its
    reader, and no approved case yet. Under --control auto the control does not
    run, and the manifest names the accession no case names -- not that the tree
    has no cases directory, which is the other side, read on a tree without one."""
    assert run_analysis.GOLDEN_CASES.is_dir() and run_analysis.GOLDEN_FORMAT.is_file()
    assert list(run_analysis.GOLDEN_CASES.glob("*.yaml")) == []
    no_case = f"no approved golden case under evals/golden/cases names {NVDA_ACCESSION}"
    assert run_analysis.is_golden_filing(NVDA_ACCESSION) == (False, no_case)
    assert run_analysis.is_golden_filing(None) == (
        False, "the run's manifest names no accession, so no golden case can name it")
    manifest = _run_with_control(tmp_path, monkeypatch, "auto")
    assert "control-single-agent" not in manifest["agents"]
    assert manifest["control_reason"] == no_case
    assert manifest["analysis_stages"]["control"] == f"skipped: {no_case}"
    assert manifest["analysis_failure"] is None
    # the other side: a tree with no cases directory says so, before any reading
    monkeypatch.setattr(run_analysis, "GOLDEN_CASES", tmp_path / "no-such-tree" / "cases")
    assert run_analysis.is_golden_filing(NVDA_ACCESSION) == (False, run_analysis.NO_GOLDEN_CASES)
    assert run_analysis.is_golden_filing(None) == (False, run_analysis.NO_GOLDEN_CASES)


# A planted reader with the real reader's two names, `load_case` and
# `GoldenFormatError`, over the two-level `key: value` subset a case needs here.
GOLDEN_FORMAT_STUB = '''
from pathlib import Path


class GoldenFormatError(ValueError):
    pass


def _scalar(value):
    value = value.strip()
    if value in ("true", "false"):
        return value == "true"
    return value.strip('"')


def load_case(path):
    case, current = {}, None
    for number, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        key, colon, value = line.strip().partition(":")
        if not colon:
            raise GoldenFormatError(f"line {number}: expected key: value")
        if line.startswith("  "):
            case[current][key] = _scalar(value)
        else:
            current = key
            case[key] = _scalar(value) if value.strip() else {}
    return case
'''


def _golden_tree(tmp_path, monkeypatch, cases: dict[str, str]) -> Path:
    """A planted owner's tree: the cases directory and the reader beside it, the
    two paths `is_golden_filing` reads pointed at them."""
    tree = tmp_path / "golden_tree"
    cases_dir = tree / "golden" / "cases"
    cases_dir.mkdir(parents=True)
    (tree / "golden_format.py").write_text(GOLDEN_FORMAT_STUB, encoding="utf-8")
    for name, text in cases.items():
        (cases_dir / name).write_text(text, encoding="utf-8")
    monkeypatch.setattr(run_analysis, "GOLDEN_CASES", cases_dir)
    monkeypatch.setattr(run_analysis, "GOLDEN_FORMAT", tree / "golden_format.py")
    return tree


def test_an_approved_golden_case_naming_the_filing_runs_the_control(tmp_path, monkeypatch):
    """The positive path, through the YAML read: `approved_by_owner` true and
    `filing.accession` this one, in a planted tree."""
    approved = (f'filing:\n  ticker: NVDA\n  accession: "{NVDA_ACCESSION}"\n'
                "frame: accounting\napproved_by_owner: true\n")
    draft = approved.replace("approved_by_owner: true", "approved_by_owner: false")
    other = approved.replace(NVDA_ACCESSION, "0001045810-25-000001")
    broken = "no colon on this line\n"
    tree = _golden_tree(tmp_path, monkeypatch, {"approved.yaml": approved, "broken.yaml": broken,
                                                "draft.yaml": draft, "other.yaml": other})
    assert run_analysis.is_golden_filing(NVDA_ACCESSION) == (
        True, f"the approved golden case approved.yaml names {NVDA_ACCESSION}")
    assert run_analysis.is_golden_filing("0001045810-25-000001") == (
        True, "the approved golden case other.yaml names 0001045810-25-000001")
    assert run_analysis.is_golden_filing(None) == (
        False, "the run's manifest names no accession, so no golden case can name it")
    (tree / "golden" / "cases" / "approved.yaml").unlink()
    assert run_analysis.is_golden_filing(NVDA_ACCESSION) == (
        False, f"no approved golden case under evals/golden/cases names {NVDA_ACCESSION} "
               "(1 case file(s) could not be read: broken.yaml)")
    (tree / "golden_format.py").unlink()
    assert run_analysis.is_golden_filing(NVDA_ACCESSION) == (False, run_analysis.NO_GOLDEN_FORMAT)


def test_the_message_names_the_shared_files_first_in_a_fixed_order():
    names = {"input_mdna.md", "report_numbers.md", "calculator.json", "analysis_accounting.json",
             "report_notes_text.md", "assumptions.json"}
    assert run_analysis.message_files(names) == [
        "calculator.json", "report_numbers.md", "report_notes_text.md",
        "analysis_accounting.json", "assumptions.json", "input_mdna.md"]
    assert run_analysis.message_files({"input_notes.md", "input_8k.md"}) == \
        ["input_8k.md", "input_notes.md"]


# Two of the fixture's 112 MD&A paragraphs, flagged by the stubbed notes reader:
# the first and the third, which are not adjacent. Their blocks are copied here
# from the fixture's input_mdna.md by hand (the apostrophe in "Management's" is
# the filing's own U+2019), and the expected trimmed copy is the file's preamble,
# the first block and the third block, one after the other with nothing between
# them: the third block's own [id] line is the junction.
MDNA_ONE = "0001045810-26-000075:mdna:1"
MDNA_THREE = "0001045810-26-000075:mdna:3"
FLAGGING_TWO = '''```json
[{ "id": "earnings_quality_mdna_heading", "paragraph_id": "0001045810-26-000075:mdna:1",
   "quote": "Analysis of Financial Condition" },
 { "id": "earnings_quality_third_paragraph_unchanged", "paragraph_id": "0001045810-26-000075:mdna:3",
   "quote": "same as prior period" }]
```
'''
TRIMMED_TWO = (
    "# NVDA MD&A \u2014 0001045810-26-000075\n\n\n## mdna\n\n"
    "[0001045810-26-000075:mdna:1]\nItem 2. Management\u2019s Discussion and Analysis of "
    "Financial Condition and Results of Operations\n\n"
    "[0001045810-26-000075:mdna:3]\n[same as prior period, unchanged from "
    "0001045810-26-000052:mdna:3]\n\n")
INSIDE = {"reason": "a reason", "quote": "Analysis of Financial Condition",
          "quote_from": "input_mdna.md"}
ACROSS = {"reason": "a reason", "quote_from": "input_mdna.md",
          "quote": "Results of Operations\n\n[0001045810-26-000075:mdna:3]\n[same as"}


def test_a_whole_run_with_two_paragraphs_flagged_hands_the_valuation_analyst_those_two(
        tmp_path, monkeypatch):
    """The trimmed copy, the manifest's `trimmed` record, the boundary check and the
    seam rule of the first pass's gate, all on one run and all agreeing."""
    run = tmp_path / "NVDA" / NVDA_ACCESSION
    bundle = assemble_bundle.build("NVDA", "10-Q", accession=NVDA_ACCESSION,
                                   prior_runs=run.parent.parent)
    assemble_bundle.write(bundle, run)
    assumptions = {"scenarios": {
        "bear": dict(DRIVERS, reasons={d: ACROSS for d in DRIVERS}),
        "base": dict(DRIVERS, reasons={d: INSIDE for d in DRIVERS}),
        "bull": dict(DRIVERS, reasons={d: INSIDE for d in DRIVERS})}}
    monkeypatch.setattr(run_analysis, "ask",
                        _fake_ask({}, notes_report=FLAGGING_TWO, assumptions=assumptions))
    manifest = run_analysis.run_company(run=run, ticker="NVDA", form="10-Q",
                                        cutoff="2026-08-26", period_end="2026-07-26",
                                        store=run_analysis.cutoff_guard.FIXTURES,
                                        prices=None, control="never")
    assert manifest["analysis_failure"] is None
    assert manifest["dropped_items"] == []                      # both items stood the gate
    for name in ("valuation-analyst", "valuation-analyst-second-pass"):
        copy = run / "agents" / name / "input_mdna.md"
        assert copy.read_bytes() == TRIMMED_TWO.encode("utf-8")
        record = manifest["agents"][name]["trimmed"]
        assert record["input_mdna.md"] == {
            "kept": [MDNA_ONE, MDNA_THREE], "of": 112,
            "note": "2 of 112 paragraphs, the ones the notes reader flagged; the rest were "
                    "not placed"}
        assert record["input_8k.md"]["kept"] == []               # nothing of the 8-K flagged
    assert agent_inputs.isolation_violations(run) == []
    # The boundary check derives the flagged set again from the gated report and
    # the drop list: the record edited to keep every paragraph, over the full
    # file, is reported by the paragraphs no standing item flagged, and the
    # directory's file by its bytes.
    full = (run / "input_mdna.md").read_text(encoding="utf-8")
    every = agent_inputs.paragraph_ids(full)
    assert len(every) == 112 and every[0] == MDNA_ONE and every[2] == MDNA_THREE
    edited = json.loads((run / "input_manifest.json").read_text(encoding="utf-8"))
    edited["agents"]["valuation-analyst"]["trimmed"]["input_mdna.md"]["kept"] = every
    (run / "input_manifest.json").write_text(json.dumps(edited), encoding="utf-8")
    (run / "agents" / "valuation-analyst" / "input_mdna.md").write_text(full, encoding="utf-8")
    broken = agent_inputs.isolation_violations(run)
    assert len(broken) == 2 and all(line.startswith("valuation-analyst: ") for line in broken)
    unflagged = [identifier for identifier in every if identifier not in (MDNA_ONE, MDNA_THREE)]
    assert broken[0] == ("valuation-analyst: input_mdna.md: the manifest's trimmed record "
                         f"keeps {', '.join(unflagged)}, which no standing item of "
                         "report_notes_text.md flagged")
    assert "other bytes" in broken[1]
    # the record put back as it was over the full file: the bytes alone are reported
    edited["agents"]["valuation-analyst"]["trimmed"]["input_mdna.md"]["kept"] = [
        MDNA_ONE, MDNA_THREE]
    (run / "input_manifest.json").write_text(json.dumps(edited), encoding="utf-8")
    broken = agent_inputs.isolation_violations(run)
    assert len(broken) == 1 and "other bytes" in broken[0]
    (run / "agents" / "valuation-analyst" / "input_mdna.md").write_bytes(
        TRIMMED_TWO.encode("utf-8"))
    assert agent_inputs.isolation_violations(run) == []
    # the seam rule: the bear scenario quotes across the junction of the two
    # blocks, the third's own [id] line after the first's text, which
    # string-matches the copy the analyst saw and nothing the filing printed
    copy = (run / "agents" / "valuation-analyst" / "input_mdna.md").read_text(encoding="utf-8")
    full = (run / "input_mdna.md").read_text(encoding="utf-8")
    assert ACROSS["quote"] in copy and ACROSS["quote"] not in full
    assert INSIDE["quote"] in copy and INSIDE["quote"] in full
    published = json.loads((run / "assumptions.json").read_text(encoding="utf-8"))
    assert set(published["scenarios"]) == {"base", "bull"}
    assert published["dropped_items"] == [{"where": "scenarios.bear", "reason":
        "revenue_growth_year_one: the quote string-matches the trimmed input_mdna.md and "
        "not the filing: it runs across a seam between two paragraphs that were not adjacent"}]
    assert manifest["analysis_stages"]["assumptions"] == {"dropped": 1}


def test_the_valuation_analyst_is_handed_only_the_paragraphs_the_notes_reader_flagged(finished):
    """The stubbed notes reader wrote no items, so no MD&A paragraph was flagged: the
    valuation analyst is handed no MD&A at all -- a copy holding no paragraph is not
    some of the original's paragraphs, which the owner refuses ("the copy carries no
    [id] paragraphs") -- the manifest records the trim, 0 of 112, beside the agent's
    usage, and the notes reader's own copy holds every paragraph."""
    run, manifest, _ = finished
    for name in ("valuation-analyst", "valuation-analyst-second-pass"):
        assert not (run / "agents" / name / "input_mdna.md").exists()
        assert not (run / "agents" / name / "input_8k.md").exists()
    reader = (run / "agents" / "notes-text-reader" / "input_mdna.md").read_text()
    # 112 paragraphs: counted by hand on the fixture's MD&A, built once outside
    # the tests, with `grep -c '^\[0001045810-' input_mdna.md` (112), and the
    # same 112 for `grep -c '\[0001045810-'`, so no marker sits off a line start.
    assert reader.count("\n[0001045810-26-000075:mdna:") == 112
    assert reader.count("[0001045810-") == 112
    for name in ("valuation-analyst", "valuation-analyst-second-pass"):
        record = manifest["agents"][name]
        assert record["result"] == "written"                      # the usage record stayed
        assert record["trimmed"]["input_mdna.md"]["kept"] == []
        assert record["trimmed"]["input_mdna.md"]["of"] == 112
        assert record["trimmed"]["input_mdna.md"]["note"].startswith("0 of 112 paragraphs")


# --- the limit falls back to Opus (the owner's decision of 2026-10-07) --------------------
#
# "fable 사용량이 max 가 되면 오퍼스로 전환시키도록해": when Fable usage reaches its
# limit, switch to Opus. Expected values below are the stub CLI's own answers,
# the hand-written manifest edits, and the module's constants.

# The CLI answering the limit on a Fable call: two tokens in, none out, Fable named.
FABLE_LIMIT = (1, {"is_error": True,
                   "result": "You've reached your Fable limit. Switch to another model to continue.",
                   "usage": {"input_tokens": 2, "output_tokens": 0},
                   "modelUsage": {"claude-fable-5-1": {"outputTokens": 0}}}, None)
OPUS_LIMIT = (1, {"is_error": True, "result": "You've reached your Opus limit.",
                  "usage": {"input_tokens": 3, "output_tokens": 0},
                  "modelUsage": {"claude-opus-5-5": {"outputTokens": 0}}}, None)
# What a stubbed agent is served, by the name it asked for.
SERVED = {"fable": "claude-fable-5-1", "opus": "claude-opus-5-5"}


def _opus_writes(name: str, payload: dict):
    """The CLI, on Opus, writing `name`: seven tokens in, five out."""
    return (0, {"usage": {"input_tokens": 7, "output_tokens": 5}, "total_cost_usd": 0.25,
                "modelUsage": {"claude-opus-5-5": {"outputTokens": 5}}},
            {name: json.dumps(payload)})


def _sequential(run, names, logs, model=None, policy=None):
    """`parallel` in the pipeline's order, so which analyst the limit reaches
    first is the test's choice and not the scheduler's."""
    return {name: run_analysis.run_agent(run, name, logs, model, policy) for name in names}


def _financial_analyst_over_cli(tmp_path, monkeypatch, answers, run=None):
    """A run where the financial analyst's calls go through the real `ask` over
    a stubbed CLI answering `answers`, the analysts called in order; every other
    agent writes and records the model it was asked on, as the real `ask` does.
    Returns the run, the CLI commands made, and the models each agent was asked
    on, call by call, keyed by the directory called (the two valuation passes
    share one definition name). `run` names a bundle already in place, which is
    then used as it stands; by default NVDA's is built under `tmp_path`."""
    if run is None:
        run = tmp_path / "NVDA" / NVDA_ACCESSION
        assemble_bundle.write(assemble_bundle.build("NVDA", "10-Q", accession=NVDA_ACCESSION,
                                                    prior_runs=run.parent.parent), run)
    written, real_ask = _fake_ask({}), run_analysis.ask
    cli, calls = _cli(list(answers))
    asked: dict[str, list[str]] = {}

    def ask(directory, *, agent, writes, message, spec, log):
        asked.setdefault(directory.name, []).append(spec["model"])
        if agent == "financial-analyst":
            monkeypatch.setattr(run_analysis.subprocess, "run", cli)
            return real_ask(directory, agent=agent, writes=writes, message=message,
                            spec=spec, log=log)
        return dict(written(directory, agent=agent, writes=writes, message=message,
                            spec=spec, log=log),
                    model_requested=spec["model"], model_served=SERVED[spec["model"]])

    monkeypatch.setattr(run_analysis, "ask", ask)
    monkeypatch.setattr(run_analysis, "parallel", _sequential)
    return run, calls, asked


def _models_asked(calls) -> list[str]:
    return [command[command.index("--model") + 1] for command in calls]


def test_the_limit_falls_back_to_opus_for_the_agent_and_every_later_fable_agent(
        tmp_path, monkeypatch, capsys):
    """The financial analyst's Fable call answers the limit; the stub's next
    answer, on Opus, writes the analysis. The analyst is called again at once on
    Opus, the valuation analyst, its second pass and the control -- every later
    agent whose definition asks for Fable -- run on Opus, each recorded as a
    fallback by name; the accounting analyst, called before the limit, stays a
    Fable record; the manifest carries the one `model_fallback` row; the run
    finishes with no frame missing and exits 0, naming the flag that carries the
    fallback into the rest of the batch, because the limit's message confirmed
    it; the batch sizer leaves the filing out of its median and names it."""
    answers = [FABLE_LIMIT, _opus_writes("analysis_financial.json",
                                         _analysis("financial", "earnings_quality_accruals_rising"))]
    run, calls, asked = _financial_analyst_over_cli(tmp_path, monkeypatch, answers)
    manifest = run_analysis.run_company(run=run, **_run_keyword("always"))
    assert _models_asked(calls) == ["fable", "opus"]            # the limit, then Opus at once
    assert asked == {"numbers-reader": ["opus"], "notes-text-reader": ["opus"],
                     "accounting-analyst": ["fable"], "financial-analyst": ["fable", "opus"],
                     "valuation-analyst": ["opus"], "valuation-analyst-second-pass": ["opus"],
                     run_analysis.CONTROL_DIRNAME: ["opus"]}
    financial = manifest["agents"]["financial-analyst"]
    assert financial["result"] == "written" and "limit_reached" not in financial
    assert [(row["attempt"], row["model_requested"], row["model_served"], row["outcome"])
            for row in financial["attempts"]] == [(1, "fable", "claude-fable-5-1", "limit"),
                                                  (2, "opus", "claude-opus-5-5", "written")]
    assert financial["model_requested"] == "fable"
    assert financial["model_served"] == "claude-opus-5-5"
    assert financial["fallback_from"] == "fable"
    assert financial["fallback_reason"] == run_analysis.FALLBACK_REASON == "fable_limit_reached"
    assert financial["input_tokens"] == 2 + 7 and financial["output_tokens"] == 0 + 5
    assert financial["attempt"] == 2
    for name in ("valuation-analyst", "valuation-analyst-second-pass", "control-single-agent"):
        record = manifest["agents"][name]
        assert record["model_requested"] == "fable" and record["model_served"] == "claude-opus-5-5"
        assert record["fallback_from"] == "fable"
        assert record["fallback_reason"] == "fable_limit_reached", name
    for name in ("numbers-reader", "notes-text-reader", "accounting-analyst"):
        assert "fallback_from" not in manifest["agents"][name], name
    assert manifest["agents"]["accounting-analyst"]["model_served"] == "claude-fable-5-1"
    fallback = manifest["model_fallback"]
    assert fallback["from"] == "fable" and fallback["to"] == run_analysis.FALLBACK_MODEL == "opus"
    assert fallback["first_agent"] == "financial-analyst" and fallback["at"].endswith("Z")
    assert fallback["reason"] == "fable_limit_reached" and "confirmed_by" not in fallback
    assert "fable_limit_reached" not in manifest and manifest["analysis_failure"] is None
    assert run_analysis.FINISH_MARKER in manifest and "model_override" not in manifest
    for name in ("analysis_accounting.json", "analysis_financial.json", "assumptions.json",
                 "analysis_valuation.json", run_analysis.FINAL, "memo_ko.md",
                 *run_analysis.CONTROL_WRITES):
        assert (run / name).is_file(), name
    memo = (run / "memo_ko.md").read_text(encoding="utf-8")
    assert "실행되지 않았습니다" not in memo and "해석이 없습니다" not in memo
    assert agent_inputs.isolation_violations(run) == []
    monkeypatch.setattr(run_analysis, "run_company", lambda **kw: manifest)
    monkeypatch.setattr(run_analysis.interpreter_pin, "enforce", lambda: 0)
    capsys.readouterr()
    assert run_analysis.main(_main_command(run)) == 0
    err = capsys.readouterr().err
    assert f"every later run under {run.parent.parent} carries it on its own for 12 hours" in err
    assert f"a run elsewhere names it with --carry-fallback-from {run}" in err
    # the batch sizer: a published filing, its Fable tokens the accounting
    # analyst's 1+1 (the stub) and the limit attempt's 2+0, no Opus attempt; it
    # fell back, so it is left out of the median, and with no other filing on
    # record the batch is one filing
    assert fable_batch.published(manifest) is True
    assert fable_batch.on_record(run.parent.parent) == {f"NVDA/{NVDA_ACCESSION}": 4}
    assert fable_batch.fell_back(run.parent.parent) == [f"NVDA/{NVDA_ACCESSION}"]
    sized = fable_batch.size(40, fable_batch.on_record(run.parent.parent),
                             fable_batch.fell_back(run.parent.parent))
    assert sized["batch"] == 1 and sized["median_per_filing"] is None
    assert sized["fell_back"] == 1
    assert sized["fell_back_filings"] == [f"NVDA/{NVDA_ACCESSION}"]
    assert (f"1 filing(s) fell back to opus and are left out of the median "
            f"(NVDA/{NVDA_ACCESSION})") in sized["calculation"]


def test_under_stop_the_limit_stops_the_run_with_no_opus_call_and_exits_four(
        tmp_path, monkeypatch):
    """The other side: `--on-fable-limit stop` keeps the rule of 2026-10-06. The
    stub's Opus answer is never taken, nothing after the analyst runs, no
    fallback is recorded, and the command exits LIMIT_REACHED."""
    answers = [FABLE_LIMIT, _opus_writes("analysis_financial.json",
                                         _analysis("financial", "earnings_quality_accruals_rising"))]
    run, calls, asked = _financial_analyst_over_cli(tmp_path, monkeypatch, answers)
    manifest = run_analysis.run_company(run=run, on_fable_limit="stop", **_run_keyword("always"))
    assert _models_asked(calls) == ["fable"]
    assert asked["financial-analyst"] == ["fable"]
    assert "valuation-analyst" not in asked and run_analysis.CONTROL_DIRNAME not in asked
    assert manifest["fable_limit_reached"] == ["financial-analyst"]
    assert "model_fallback" not in manifest
    financial = manifest["agents"]["financial-analyst"]
    assert financial["limit_reached"] is True and "fallback_from" not in financial
    assert [row["outcome"] for row in financial["attempts"]] == ["limit"]
    assert "nothing fell back to another model" in manifest["analysis_failure"]
    assert (run / "analysis_accounting.json").is_file()
    assert not (run / "analysis_financial.json").exists()
    assert fable_batch.published(manifest) is False
    monkeypatch.setattr(run_analysis, "run_company", lambda **kw: manifest)
    monkeypatch.setattr(run_analysis.interpreter_pin, "enforce", lambda: 0)
    assert run_analysis.main(_main_command(run, "--on-fable-limit", "stop")) == 4
    # the switch takes the two values and nothing else; the default is opus
    with pytest.raises(run_analysis.RunError, match="not one of"):
        run_analysis.LimitPolicy("neither")
    assert run_analysis.DEFAULT_ON_FABLE_LIMIT == "opus"
    assert run_analysis.ON_FABLE_LIMIT == ("stop", "opus")


def test_a_limit_on_the_fallback_model_stops_and_an_opus_request_never_falls_back(
        tmp_path, monkeypatch):
    """One call under the policy: a Fable limit then an Opus limit is two
    attempts, both `limit`, and the record still says the limit was reached --
    there is nowhere further to go. A call that asked for Opus and answers the
    limit is one attempt, no fallback, nothing noted for the run."""
    run = tmp_path / "run"
    (run / "a").mkdir(parents=True)
    (run / "input_manifest.json").write_text("{}", encoding="utf-8")
    cli, calls = _cli([FABLE_LIMIT, OPUS_LIMIT])
    monkeypatch.setattr(run_analysis.subprocess, "run", cli)
    policy = run_analysis.LimitPolicy("opus")
    spec = {"model": "fable", "description": "d", "prompt": "p", "tools": ["Read"]}
    record = run_analysis.call(run, run / "a", agent="x", writes=("out.json",), message="m",
                               spec=spec, log=run / "x.log", policy=policy)
    assert _models_asked(calls) == ["fable", "opus"]
    assert record["limit_reached"] is True and record["fallback_from"] == "fable"
    assert [(row["model_requested"], row["outcome"]) for row in record["attempts"]] == [
        ("fable", "limit"), ("opus", "limit")]
    assert record["input_tokens"] == 2 + 3
    assert policy.fallback["first_agent"] == "x"
    assert json.loads((run / "input_manifest.json").read_text())["model_fallback"] == policy.fallback
    assert run_analysis.limit_hit({"x": record}) == ["x"]
    cli, calls = _cli([OPUS_LIMIT] * 2)
    monkeypatch.setattr(run_analysis.subprocess, "run", cli)
    policy = run_analysis.LimitPolicy("opus")
    record = run_analysis.call(run, run / "a", agent="y", writes=("out.json",), message="m",
                               spec=dict(spec, model="opus"), log=run / "y.log", policy=policy)
    assert _models_asked(calls) == ["opus"]
    assert record["limit_reached"] is True and "fallback_from" not in record
    assert policy.fallback is None


def test_a_fallback_run_that_stopped_on_an_error_resumes_on_opus_and_stays_labelled(
        tmp_path, monkeypatch):
    """The financial analyst fell back, then the calculator refused an input
    before the valuation analyst (planted as the crash test above plants it):
    the manifest carries `model_fallback` and `stopped_on`. The plan accepts a
    resume naming no model and one naming opus, and refuses one naming
    claude-fable-5-1. A definition edited between the nights is refused under
    the resume's --model opus as under none, and a resume under
    `--on-fable-limit stop` is refused before any agent runs. Resumed with no
    model, the pending valuation passes run on Opus, labelled, and the fallback
    row stands as first written."""
    answers = [FABLE_LIMIT, _opus_writes("analysis_financial.json",
                                         _analysis("financial", "earnings_quality_accruals_rising"))]
    run, calls, asked = _financial_analyst_over_cli(tmp_path, monkeypatch, answers)
    real_calculate, state = run_analysis.calculator.calculate, {"raised": False}

    def calculate(**keyword):
        if "accounting" in keyword and "assumptions" not in keyword and not state["raised"]:
            state["raised"] = True
            raise run_analysis.calculator.CalculatorInputError("planted: an input is not there")
        return real_calculate(**keyword)

    monkeypatch.setattr(run_analysis.calculator, "calculate", calculate)
    with pytest.raises(run_analysis.calculator.CalculatorInputError, match="planted"):
        run_analysis.run_company(run=run, **_run_keyword())
    stopped = json.loads((run / "input_manifest.json").read_text(encoding="utf-8"))
    assert run_analysis.FINISH_MARKER not in stopped and "stopped_on" in stopped
    row = stopped["model_fallback"]
    assert row["first_agent"] == "financial-analyst" and row["to"] == "opus"
    assert stopped["agents"]["financial-analyst"]["fallback_from"] == "fable"
    assert "valuation-analyst" not in asked
    for model in (None, "opus"):
        plan = run_analysis.resume_plan(run, stopped, False, model)
        assert plan["fallback"] == row and plan["skipped"] == [
            "numbers-reader", "notes-text-reader", "accounting-analyst", "financial-analyst"]
    with pytest.raises(run_analysis.RunError, match="fallen back to opus from financial-analyst; "
                       "a resume under claude-fable-5-1 would mix models"):
        run_analysis.resume_plan(run, stopped, False, "claude-fable-5-1")
    # resumed once under --model opus and stopped again, the manifest then names
    # opus as its override: the agents that asked for Fable -- the accounting
    # analyst before the limit, the financial analyst labelled after it -- are
    # explained by the row, and a resume under opus is accepted again
    overridden = dict(stopped, model_override={"model": "opus", "applies_to": [],
                                               "why": "planted"})
    assert run_analysis.resume_plan(run, overridden, False, "opus")["fallback"] == row
    # the other side: the same override with no row and no label -- the financial
    # analyst served by Fable -- refuses the Fable agents on record
    bare = {key: value for key, value in overridden.items() if key != "model_fallback"}
    bare["agents"] = dict(overridden["agents"], **{"financial-analyst": dict(
        {key: value for key, value in overridden["agents"]["financial-analyst"].items()
         if key not in ("fallback_from", "fallback_reason")},
        model_served="claude-fable-5-1")})
    with pytest.raises(run_analysis.RunError, match="the run stopped under opus, but "
                       "accounting-analyst on record asked for fable"):
        run_analysis.resume_plan(run, bare, False, "opus")
    # a definition edited between the nights -- the valuation analyst's, to the
    # fallback model itself -- is refused whether the resume names opus or no
    # model: the analysts on record asked for fable, the fallen-back one included
    _definitions_with(tmp_path, monkeypatch, {"valuation-analyst": "opus"})
    for model in (None, "opus"):
        with pytest.raises(run_analysis.RunError, match="the run stopped under fable; the "
                           "definition of valuation-analyst now asks for opus"):
            run_analysis.resume_plan(run, stopped, False, model)
    _definitions_with(tmp_path, monkeypatch, {"valuation-analyst": "fable"})
    assert run_analysis.resume_plan(run, stopped, False, "opus")["fallback"] == row
    # under `stop`: a resume of a run that fell back is refused, exit 2, before
    # any agent runs, and the policy never moves a call to Opus by the row
    before = (run / "input_manifest.json").read_bytes()
    with pytest.raises(run_analysis.RunError, match="fell back to opus at financial-analyst; "
                       "a --on-fable-limit stop resume would call its pending Fable agents "
                       "on Fable after that, mixing models the other way"):
        run_analysis.run_company(run=run, on_fable_limit="stop", **_run_keyword())
    monkeypatch.setattr(run_analysis.interpreter_pin, "enforce", lambda: 0)
    assert run_analysis.main(_main_command(run, "--on-fable-limit", "stop")) \
        == run_analysis.BAD_INPUT == 2
    assert "valuation-analyst" not in asked
    assert (run / "input_manifest.json").read_bytes() == before
    assert run_analysis.LimitPolicy("stop", row).model_for("fable") == "fable"
    assert run_analysis.LimitPolicy("opus", row).model_for("fable") == "opus"
    resumed = run_analysis.run_company(run=run, **_run_keyword())
    assert asked["valuation-analyst"] == ["opus"]
    assert asked["valuation-analyst-second-pass"] == ["opus"]
    assert asked["financial-analyst"] == ["fable", "opus"]       # not called again
    assert resumed["model_fallback"] == row
    for name in ("valuation-analyst", "valuation-analyst-second-pass"):
        record = resumed["agents"][name]
        assert record["model_requested"] == "fable" and record["model_served"] == "claude-opus-5-5"
        assert record["fallback_from"] == "fable" and record["fallback_reason"] == "fable_limit_reached"
    assert resumed["resume_skipped"] == ["numbers-reader", "notes-text-reader",
                                         "accounting-analyst", "financial-analyst"]
    assert resumed["analysis_failure"] is None and "stopped_on" not in resumed
    assert fable_batch.published(resumed) is True


def test_a_mix_the_record_does_not_explain_is_still_refused_on_resume(tmp_path, monkeypatch):
    """A stopped run whose financial analyst asked for Fable and was served Opus
    with no `fallback_from` is refused; so is one carrying `fallback_from` under
    a manifest with no `model_fallback`. With the row recorded, the resume runs
    and calls the pending Fable agents on Opus."""
    run, stopped = _stopped_at_accounting_analyst(tmp_path, monkeypatch)
    path = run / "input_manifest.json"
    edited = json.loads(path.read_text(encoding="utf-8"))
    financial = edited["agents"]["financial-analyst"]
    financial["model_requested"], financial["model_served"] = "fable", "claude-opus-5-5"
    path.write_text(json.dumps(edited), encoding="utf-8")
    monkeypatch.setattr(run_analysis, "ask",
                        lambda *a, **k: (_ for _ in ()).throw(AssertionError("an agent ran")))
    with pytest.raises(run_analysis.RunError, match="financial-analyst on record asked for fable "
                       "and was served claude-opus-5-5 with no recorded fallback"):
        run_analysis.run_company(run=run, **_run_keyword())
    financial["fallback_from"] = "fable"
    path.write_text(json.dumps(edited), encoding="utf-8")
    with pytest.raises(run_analysis.RunError, match="fell back from fable, but the manifest "
                       "records no model_fallback"):
        run_analysis.run_company(run=run, **_run_keyword())
    edited["model_fallback"] = {"from": "fable", "to": "opus", "at": "2026-10-07T00:00:00Z",
                                "first_agent": "financial-analyst"}
    path.write_text(json.dumps(edited), encoding="utf-8")
    written, asked = _fake_ask({}), {}

    def ask(directory, *, agent, writes, message, spec, log):
        asked.setdefault(directory.name, []).append(spec["model"])
        return dict(written(directory, agent=agent, writes=writes, message=message,
                            spec=spec, log=log),
                    model_requested=spec["model"], model_served=SERVED[spec["model"]])

    monkeypatch.setattr(run_analysis, "ask", ask)
    manifest = run_analysis.run_company(run=run, **_run_keyword())
    assert asked == {"accounting-analyst": ["opus"], "valuation-analyst": ["opus"],
                     "valuation-analyst-second-pass": ["opus"]}
    assert manifest["model_fallback"] == edited["model_fallback"]
    assert manifest["agents"]["accounting-analyst"]["fallback_from"] == "fable"
    assert manifest["analysis_failure"] is None and "fable_limit_reached" not in manifest


def test_a_run_with_no_limit_records_no_fallback(finished):
    run, manifest, _ = finished
    assert "model_fallback" not in manifest
    assert not any("fallback_from" in record or "fallback_reason" in record
                   for record in manifest["agents"].values())
    assert fable_batch.fell_back(run.parent.parent) == []
    assert fable_batch.size(1000, {"A/1": 400})["fell_back"] == 0


def _fable_writes(name: str, payload: dict):
    """The CLI, on Fable, writing `name`: three tokens in, two out."""
    return (0, {"usage": {"input_tokens": 3, "output_tokens": 2}, "total_cost_usd": 0.5,
                "modelUsage": {"claude-fable-5-1": {"outputTokens": 2}}},
            {name: json.dumps(payload)})


def test_a_limit_the_fallback_model_answers_too_stops_the_run_and_exits_one_not_four(
        tmp_path, monkeypatch, capsys):
    """The financial analyst's Fable call answers the limit and its Opus call
    answers the Opus limit: the run stops there, as it would under `stop`, the
    manifest naming the analyst under `fable_limit_reached` beside the
    fallback row, and nothing after the analysts runs. Under `opus` the command
    exits FAILED, 1: exit 4 is `stop`'s alone. The same manifest under `stop`
    reads 4, which is the stop test's own exit above. The stderr line says to
    stop the batch and never names the flag that would carry the fallback on."""
    run, calls, asked = _financial_analyst_over_cli(tmp_path, monkeypatch,
                                                    [FABLE_LIMIT, OPUS_LIMIT])
    manifest = run_analysis.run_company(run=run, **_run_keyword("always"))
    assert _models_asked(calls) == ["fable", "opus"]
    assert "valuation-analyst" not in asked and run_analysis.CONTROL_DIRNAME not in asked
    assert manifest["fable_limit_reached"] == ["financial-analyst"]
    assert manifest["model_fallback"]["first_agent"] == "financial-analyst"
    financial = manifest["agents"]["financial-analyst"]
    assert financial["limit_reached"] is True and financial["fallback_from"] == "fable"
    assert [(row["model_requested"], row["outcome"]) for row in financial["attempts"]] == [
        ("fable", "limit"), ("opus", "limit")]
    assert ("opus answered the limit too at financial-analyst"
            in manifest["analysis_failure"])
    assert run_analysis.missing_frames(run, manifest["agents"])["financial"].startswith(
        "financial-analyst answered the limit on opus too, after the Fable limit")
    assert fable_batch.published(manifest) is False
    monkeypatch.setattr(run_analysis, "run_company", lambda **kw: manifest)
    monkeypatch.setattr(run_analysis.interpreter_pin, "enforce", lambda: 0)
    capsys.readouterr()
    assert run_analysis.main(_main_command(run)) == run_analysis.FAILED == 1
    err = capsys.readouterr().err
    assert "--carry-fallback-from" not in err
    assert err.strip() == ("run_analysis: a limit stopped this run at financial-analyst on opus, "
                           "the model a Fable limit falls back to: stop the batch "
                           "(fable_limit_reached in the manifest); nothing is carried")
    assert run_analysis.main(_main_command(run, "--on-fable-limit", "stop")) \
        == run_analysis.LIMIT_REACHED == 4
    assert capsys.readouterr().err == ""             # exit 4 says it; nothing is carried


def test_the_rest_of_the_batch_carries_the_fallback_from_its_first_call(
        tmp_path, monkeypatch, capsys):
    """An earlier run of the batch fell back: its manifest, written here by hand,
    carries the row. This run, started with `--carry-fallback-from` naming it,
    never asks Fable: the financial analyst's one call is the stub's one answer,
    on Opus; every agent whose definition asks for Fable is asked on Opus at its
    first call and labelled; the row is noted at the first of them, the
    accounting analyst, and names the earlier run; no limit attempt is on
    record; the command exits 0 and names the flag for the next run. The other
    side: a run named that records no fallback, one whose limit was noted more
    than CARRY_HOURS before (another night's), and the flag under `stop`, are
    refused before any agent runs. The earlier row's time is written an hour
    before the clock this test reads, so the window is the test's own."""
    answers = [_opus_writes("analysis_financial.json",
                            _analysis("financial", "earnings_quality_accruals_rising"))]
    run, calls, asked = _financial_analyst_over_cli(tmp_path, monkeypatch, answers)
    earlier = tmp_path / "AMD" / "0000002488-26-000001"
    earlier.mkdir(parents=True)
    (earlier / "input_manifest.json").write_text(json.dumps({"agents": {}}), encoding="utf-8")
    with pytest.raises(run_analysis.RunError, match="records no model_fallback"):
        run_analysis.run_company(run=run, carry_fallback_from=earlier, **_run_keyword("always"))
    monkeypatch.setattr(run_analysis.interpreter_pin, "enforce", lambda: 0)
    assert run_analysis.main(_main_command(run, "--carry-fallback-from", str(earlier))) \
        == run_analysis.BAD_INPUT == 2
    now = dt.datetime.now(dt.timezone.utc)
    stamp = "%Y-%m-%dT%H:%M:%SZ"
    old = {"from": "fable", "to": "opus", "first_agent": "financial-analyst",
           "reason": "fable_limit_reached",
           "at": (now - dt.timedelta(hours=run_analysis.CARRY_HOURS + 1)).strftime(stamp)}
    (earlier / "input_manifest.json").write_text(json.dumps({"model_fallback": old}),
                                                 encoding="utf-8")
    with pytest.raises(run_analysis.RunError, match=f"its limit was noted at {old['at']}, not "
                       "within the 12 hours before this run, so it is not this batch's"):
        run_analysis.run_company(run=run, carry_fallback_from=earlier, **_run_keyword("always"))
    row = dict(old, at=(now - dt.timedelta(hours=1)).strftime(stamp))
    (earlier / "input_manifest.json").write_text(json.dumps({"model_fallback": row}),
                                                 encoding="utf-8")
    with pytest.raises(run_analysis.RunError, match="--on-fable-limit stop does not fall back"):
        run_analysis.run_company(run=run, carry_fallback_from=earlier, on_fable_limit="stop",
                                 **_run_keyword("always"))
    assert calls == [] and asked == {}                         # nothing ran on a refusal
    manifest = run_analysis.run_company(run=run, carry_fallback_from=earlier,
                                        **_run_keyword("always"))
    assert _models_asked(calls) == ["opus"]
    assert asked == {"numbers-reader": ["opus"], "notes-text-reader": ["opus"],
                     "accounting-analyst": ["opus"], "financial-analyst": ["opus"],
                     "valuation-analyst": ["opus"], "valuation-analyst-second-pass": ["opus"],
                     run_analysis.CONTROL_DIRNAME: ["opus"]}
    fallback = manifest["model_fallback"]
    assert set(fallback) == {"from", "to", "at", "first_agent", "reason", "carried_from",
                             "carried_limit_at"}
    assert fallback["reason"] == "fable_limit_reached"
    assert fallback["carried_limit_at"] == row["at"]
    assert fallback["from"] == "fable" and fallback["to"] == "opus"
    assert fallback["first_agent"] == "accounting-analyst"
    assert fallback["carried_from"] == "AMD/0000002488-26-000001"
    for name in ("accounting-analyst", "financial-analyst", "valuation-analyst",
                 "valuation-analyst-second-pass", "control-single-agent"):
        record = manifest["agents"][name]
        assert record["model_requested"] == "fable", name
        assert record["model_served"] == "claude-opus-5-5", name
        assert record["fallback_from"] == "fable", name
        assert record["fallback_reason"] == "fable_limit_reached", name
    for name in ("numbers-reader", "notes-text-reader"):
        assert "fallback_from" not in manifest["agents"][name], name
    financial = manifest["agents"]["financial-analyst"]
    assert [(row["model_requested"], row["outcome"]) for row in financial["attempts"]] == [
        ("opus", "written")]
    assert manifest["analysis_failure"] is None and "fable_limit_reached" not in manifest
    # no attempt Fable served: the filing costs no Fable token and is not on
    # record, and it is a published fallback run
    assert fable_batch.on_record(tmp_path) == {}
    assert fable_batch.fell_back(tmp_path) == [f"NVDA/{NVDA_ACCESSION}"]
    capsys.readouterr()
    monkeypatch.setattr(run_analysis, "run_company", lambda **kw: manifest)
    assert run_analysis.main(_main_command(run, "--carry-fallback-from", str(earlier))) == 0
    assert "fell back to opus at accounting-analyst" in capsys.readouterr().err


def test_a_run_that_fell_back_names_the_flag_for_the_rest_of_the_batch_and_one_that_did_not_is_silent(
        tmp_path, monkeypatch, capsys):
    """The stderr line says where the fallback carries -- every later run under
    the same root on its own, for twelve hours from the limit, and a run
    elsewhere by the flag: printed for a manifest carrying a confirmed row,
    never for one without it, and never on stdout, which stays the agents'
    JSON."""
    monkeypatch.setattr(run_analysis.interpreter_pin, "enforce", lambda: 0)
    run = tmp_path / "NVDA" / NVDA_ACCESSION
    row = {"from": "fable", "to": "opus", "at": "2026-10-07T03:00:00Z",
           "first_agent": "financial-analyst", "reason": "fable_limit_reached"}
    finished_clean = {"agents": {}, "analysis_failure": None,
                      run_analysis.FINISH_MARKER: "2026-10-07T04:00:00Z"}
    monkeypatch.setattr(run_analysis, "run_company",
                        lambda **kw: dict(finished_clean, model_fallback=row))
    assert run_analysis.main(_main_command(run)) == 0
    out = capsys.readouterr()
    assert json.loads(out.out) == {}
    assert out.err.strip() == (
        f"run_analysis: fell back to opus at financial-analyst (model_fallback in "
        f"{run / 'input_manifest.json'}); every later run under {tmp_path} carries it on its "
        f"own for 12 hours from 2026-10-07T03:00:00Z, and a run elsewhere names it with "
        f"--carry-fallback-from {run}")
    monkeypatch.setattr(run_analysis, "run_company", lambda **kw: dict(finished_clean))
    assert run_analysis.main(_main_command(run)) == 0
    assert capsys.readouterr().err == ""


def test_a_row_from_an_attempt_that_started_over_is_not_carried_into_a_run_that_did_not_fall_back(
        tmp_path, monkeypatch):
    """A row on disk with no agent on record (an earlier attempt noted the limit
    and stopped before any call returned): the run starts over, every Fable agent
    asks Fable, the financial analyst's one call is the stub's Fable answer, and
    the finished manifest carries no row this run never made."""
    answers = [_fable_writes("analysis_financial.json",
                             _analysis("financial", "earnings_quality_accruals_rising"))]
    run, calls, asked = _financial_analyst_over_cli(tmp_path, monkeypatch, answers)
    path = run / "input_manifest.json"
    planted = json.loads(path.read_text(encoding="utf-8"))
    planted["model_fallback"] = {"from": "fable", "to": "opus", "at": "2026-10-07T03:00:00Z",
                                 "first_agent": "financial-analyst"}
    path.write_text(json.dumps(planted), encoding="utf-8")
    manifest = run_analysis.run_company(run=run, **_run_keyword())
    assert _models_asked(calls) == ["fable"]
    assert asked["accounting-analyst"] == ["fable"] and asked["valuation-analyst"] == ["fable"]
    assert "model_fallback" not in manifest and manifest["analysis_failure"] is None
    assert manifest["agents"]["financial-analyst"]["model_served"] == "claude-fable-5-1"
    assert fable_batch.fell_back(run.parent.parent) == []


def test_a_limit_read_off_the_shape_falls_back_under_its_own_label_and_stays_in_its_run(
        tmp_path, monkeypatch, capsys):
    """Under `opus`, a Fable call that fails in two seconds having spent no token,
    with no limit message, still falls back (the owner's reading of that shape,
    lessons.md 2026-09-29), but the label says it was the shape:
    `fable_failed_like_the_limit` on the agent, on every later Fable agent and on
    the row. The command exits 0 and its stderr line says the fallback stays in
    this run; no carry line is printed, and naming this run with
    `--carry-fallback-from` is refused. The message case is the fallback test
    above: `fable_limit_reached` and the carry line."""
    _two_second_clock(monkeypatch)
    answers = [ZERO_TOKEN_FAILURE, _opus_writes("analysis_financial.json",
                                                _analysis("financial", "earnings_quality_accruals_rising"))]
    run, calls, asked = _financial_analyst_over_cli(tmp_path, monkeypatch, answers)
    manifest = run_analysis.run_company(run=run, **_run_keyword("always"))
    assert _models_asked(calls) == ["fable", "opus"]
    financial = manifest["agents"]["financial-analyst"]
    assert financial["result"] == "written" and financial["fallback_from"] == "fable"
    assert financial["fallback_reason"] == run_analysis.SHAPE_FALLBACK_REASON \
        == "fable_failed_like_the_limit"
    assert [(row["model_requested"], row["outcome"]) for row in financial["attempts"]] == [
        ("fable", "limit"), ("opus", "written")]
    for name in ("valuation-analyst", "valuation-analyst-second-pass", "control-single-agent"):
        record = manifest["agents"][name]
        assert record["model_served"] == "claude-opus-5-5", name
        assert record["fallback_reason"] == "fable_failed_like_the_limit", name
    fallback = manifest["model_fallback"]
    assert fallback["reason"] == "fable_failed_like_the_limit"
    assert fallback["first_agent"] == "financial-analyst"
    assert manifest["analysis_failure"] is None and "fable_limit_reached" not in manifest
    with pytest.raises(run_analysis.RunError, match="its fallback was set off by a Fable "
                       "failure shaped like the limit .fable_failed_like_the_limit., not by "
                       "the limit's message, so it stays inside its own run"):
        run_analysis.carried_fallback(run)
    monkeypatch.setattr(run_analysis.interpreter_pin, "enforce", lambda: 0)
    capsys.readouterr()
    assert run_analysis.main(_main_command(run, "--carry-fallback-from", str(run))) \
        == run_analysis.BAD_INPUT
    assert "so it stays inside its own run" in capsys.readouterr().err
    monkeypatch.setattr(run_analysis, "run_company", lambda **kw: manifest)
    assert run_analysis.main(_main_command(run)) == 0
    err = capsys.readouterr().err
    assert "carries it on its own" not in err
    assert err.strip() == (
        "run_analysis: fell back to opus at financial-analyst on a Fable failure shaped like "
        "the limit (fable_failed_like_the_limit: no token spent, under 10 seconds, no limit "
        "message), which does not confirm the limit; the fallback stays inside this run, and "
        "no later run carries it")


def test_a_shape_fallback_whose_opus_call_fails_the_same_way_exits_one_with_every_attempt(
        tmp_path, monkeypatch):
    """The Fable call fails like the limit, and the Opus call fails the same way:
    on Opus that is no limit (the shape is read for a Fable call alone), so it is
    a plain failure, run once more, and the analyst did not write. Every attempt
    is on record -- the Fable one and both Opus ones -- the label is the shape's,
    no limit stopped the run, and the command exits FAILED, 1."""
    _two_second_clock(monkeypatch)
    run, calls, asked = _financial_analyst_over_cli(tmp_path, monkeypatch,
                                                    [ZERO_TOKEN_FAILURE] * 3)
    manifest = run_analysis.run_company(run=run, **_run_keyword())
    assert _models_asked(calls) == ["fable", "opus", "opus"]
    financial = manifest["agents"]["financial-analyst"]
    assert financial["result"] == "failed" and "limit_reached" not in financial
    assert financial["fallback_reason"] == "fable_failed_like_the_limit"
    assert [(row["attempt"], row["model_requested"], row["outcome"])
            for row in financial["attempts"]] == [(1, "fable", "limit"), (2, "opus", "failed"),
                                                  (3, "opus", "failed")]
    assert "fable_limit_reached" not in manifest
    assert manifest["analysis_failure"] == "did not write: financial-analyst"
    assert "valuation-analyst" not in asked
    monkeypatch.setattr(run_analysis, "run_company", lambda **kw: manifest)
    monkeypatch.setattr(run_analysis.interpreter_pin, "enforce", lambda: 0)
    assert run_analysis.main(_main_command(run)) == run_analysis.FAILED == 1


def test_a_row_the_shape_opened_is_confirmed_by_a_later_limit_message(tmp_path):
    """Two analysts on Fable in parallel: the first fails like the limit and opens
    the row under the shape's label; the second answers the limit's message, and
    the row's reason becomes the limit's, `confirmed_by` naming it, the first
    agent kept. Another shape answer changes nothing. The other side: a row that
    names no reason is read as the shape, never as the limit."""
    run = tmp_path / "run"
    run.mkdir()
    (run / "input_manifest.json").write_text("{}", encoding="utf-8")
    policy = run_analysis.LimitPolicy("opus")
    row = policy.note(run, "accounting-analyst", run_analysis.SHAPE_FALLBACK_REASON)
    assert row["reason"] == "fable_failed_like_the_limit" and "confirmed_by" not in row
    assert run_analysis.fallback_reason(row) == "fable_failed_like_the_limit"
    policy.note(run, "control-single-agent", run_analysis.SHAPE_FALLBACK_REASON)
    assert "confirmed_by" not in policy.fallback
    policy.note(run, "financial-analyst", run_analysis.FALLBACK_REASON)
    assert policy.fallback["reason"] == "fable_limit_reached"
    assert policy.fallback["confirmed_by"] == "financial-analyst"
    assert policy.fallback["first_agent"] == "accounting-analyst"
    on_disk = json.loads((run / "input_manifest.json").read_text(encoding="utf-8"))
    assert on_disk["model_fallback"] == policy.fallback
    assert run_analysis.fallback_reason(policy.fallback) == "fable_limit_reached"
    assert run_analysis.fallback_reason({"from": "fable", "to": "opus"}) \
        == "fable_failed_like_the_limit"


def test_the_carry_window_is_read_off_the_first_limit_of_a_chain_and_never_the_future(tmp_path):
    """`carried_fallback` against a clock the test names, 2026-10-07T12:00:00Z,
    with CARRY_HOURS 12: a limit noted at 00:00 that day is twelve hours before
    and carried; one at 23:59 the day before is more than twelve and refused; one
    at 13:00, after the clock, is refused; and a row that itself carried a limit
    is read by the time it carried (`carried_limit_at`), so a chain of runs never
    stretches the window past the first limit."""
    now = dt.datetime(2026, 10, 7, 12, 0, 0, tzinfo=dt.timezone.utc)
    earlier = tmp_path / "AMD" / "0000002488-26-000001"
    earlier.mkdir(parents=True)

    def carried(row):
        (earlier / "input_manifest.json").write_text(json.dumps({"model_fallback": dict(
            {"from": "fable", "to": "opus", "first_agent": "accounting-analyst",
             "reason": "fable_limit_reached"}, **row)}), encoding="utf-8")
        return run_analysis.carried_fallback(earlier, now=now)

    assert run_analysis.CARRY_HOURS == 12
    assert carried({"at": "2026-10-07T00:00:00Z"}) == {
        "carried_from": "AMD/0000002488-26-000001", "carried_limit_at": "2026-10-07T00:00:00Z"}
    for at in ("2026-10-06T23:59:59Z", "2026-10-07T13:00:00Z"):
        with pytest.raises(run_analysis.RunError, match="not within the 12 hours"):
            carried({"at": at})
    assert carried({"at": "2026-10-07T11:00:00Z", "carried_limit_at": "2026-10-07T01:00:00Z"}) \
        == {"carried_from": "AMD/0000002488-26-000001",
            "carried_limit_at": "2026-10-07T01:00:00Z"}
    with pytest.raises(run_analysis.RunError, match="not within the 12 hours"):
        carried({"at": "2026-10-07T11:00:00Z", "carried_limit_at": "2026-10-06T22:00:00Z"})
    with pytest.raises(run_analysis.RunError, match="names no time the limit was noted at"):
        carried({"at": "yesterday"})


def test_a_fallback_run_resumed_under_model_opus_labels_every_pending_fable_agent(
        tmp_path, monkeypatch):
    """The fallback run the resume test above stops on an error, resumed with
    `--model opus`: the row already puts every pending Fable agent on Opus, so the
    flag is read as the fallback carried forward. The valuation passes are asked
    on Opus and recorded as fallbacks by name -- `model_requested: fable`,
    `fallback_from`, the row's reason -- and no `model_override` is written for
    them; the readers, on Opus by their own definitions, are not called again."""
    answers = [FABLE_LIMIT, _opus_writes("analysis_financial.json",
                                         _analysis("financial", "earnings_quality_accruals_rising"))]
    run, calls, asked = _financial_analyst_over_cli(tmp_path, monkeypatch, answers)
    real_calculate, state = run_analysis.calculator.calculate, {"raised": False}

    def calculate(**keyword):
        if "accounting" in keyword and "assumptions" not in keyword and not state["raised"]:
            state["raised"] = True
            raise run_analysis.calculator.CalculatorInputError("planted: an input is not there")
        return real_calculate(**keyword)

    monkeypatch.setattr(run_analysis.calculator, "calculate", calculate)
    with pytest.raises(run_analysis.calculator.CalculatorInputError, match="planted"):
        run_analysis.run_company(run=run, **_run_keyword())
    row = json.loads((run / "input_manifest.json").read_text(encoding="utf-8"))["model_fallback"]
    resumed = run_analysis.run_company(run=run, model="opus", **_run_keyword())
    assert asked["valuation-analyst"] == ["opus"]
    assert asked["valuation-analyst-second-pass"] == ["opus"]
    assert asked["numbers-reader"] == ["opus"] and asked["financial-analyst"] == ["fable", "opus"]
    for name in ("valuation-analyst", "valuation-analyst-second-pass"):
        record = resumed["agents"][name]
        assert record["model_requested"] == "fable", name
        assert record["model_served"] == "claude-opus-5-5", name
        assert record["fallback_from"] == "fable", name
        assert record["fallback_reason"] == "fable_limit_reached", name
    assert "model_override" not in resumed and resumed["model_fallback"] == row
    assert resumed["analysis_failure"] is None and fable_batch.published(resumed) is True



def _plant_row(directory, **row):
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "input_manifest.json").write_text(json.dumps({"model_fallback": dict(
        {"from": "fable", "to": "opus", "first_agent": "financial-analyst",
         "reason": "fable_limit_reached"}, **row)}), encoding="utf-8")


def test_the_runner_finds_the_batch_s_fallback_under_its_own_root(tmp_path):
    """`batch_fallback` against a clock the test names, 2026-10-07T12:00:00Z: of
    the runs under the root, the most recent limit a carry would accept is the
    one carried -- CSCO's at 09:00 over AMD's at 08:00; AAPL's at 11:00 is the
    shape alone, DELL's the night before is past the window, FTNT's manifest is
    not JSON, and NVDA, the run itself, is passed over though its row is the
    newest. With none of them, nothing is carried."""
    now = dt.datetime(2026, 10, 7, 12, 0, 0, tzinfo=dt.timezone.utc)
    _plant_row(tmp_path / "AMD" / "1", at="2026-10-07T08:00:00Z")
    _plant_row(tmp_path / "CSCO" / "1", at="2026-10-07T09:00:00Z")
    _plant_row(tmp_path / "AAPL" / "1", at="2026-10-07T11:00:00Z",
               reason="fable_failed_like_the_limit")
    _plant_row(tmp_path / "DELL" / "1", at="2026-10-06T20:00:00Z")
    (tmp_path / "FTNT" / "1").mkdir(parents=True)
    (tmp_path / "FTNT" / "1" / "input_manifest.json").write_text("not json", encoding="utf-8")
    _plant_row(tmp_path / "NVDA" / "1", at="2026-10-07T11:30:00Z")
    assert run_analysis.batch_fallback(tmp_path / "NVDA" / "1", now=now) == {
        "carried_from": "CSCO/1", "carried_limit_at": "2026-10-07T09:00:00Z"}
    for name in ("AMD", "CSCO"):
        shutil.rmtree(tmp_path / name)
    assert run_analysis.batch_fallback(tmp_path / "NVDA" / "1", now=now) is None


def test_a_later_run_under_the_root_carries_the_batch_s_fallback_without_a_flag(
        tmp_path, monkeypatch):
    """An earlier run under the same root fell back an hour before this test's
    clock, its limit confirmed by the message. This run, started with no flag,
    never asks Fable: every agent whose definition asks for Fable is asked on Opus
    from its first call and labelled, and the row names the earlier run. The
    other side: the same root under `--on-fable-limit stop` carries nothing, and
    every Fable agent is asked on Fable."""
    answers = [_opus_writes("analysis_financial.json",
                            _analysis("financial", "earnings_quality_accruals_rising"))]
    run, calls, asked = _financial_analyst_over_cli(tmp_path / "night", monkeypatch, answers)
    limit_at = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=1)).strftime(
        "%Y-%m-%dT%H:%M:%SZ")
    _plant_row(tmp_path / "night" / "AMD" / "0000002488-26-000001", at=limit_at)
    manifest = run_analysis.run_company(run=run, **_run_keyword())
    assert _models_asked(calls) == ["opus"]
    assert asked["accounting-analyst"] == ["opus"] and asked["valuation-analyst"] == ["opus"]
    fallback = manifest["model_fallback"]
    assert fallback["carried_from"] == "AMD/0000002488-26-000001"
    assert fallback["carried_limit_at"] == limit_at
    assert fallback["first_agent"] == "accounting-analyst"
    for name in ("accounting-analyst", "financial-analyst", "valuation-analyst"):
        assert manifest["agents"][name]["fallback_reason"] == "fable_limit_reached", name
    assert manifest["analysis_failure"] is None
    monkeypatch.undo()                     # the second run's stubs, not wrapped in the first's
    answers = [_fable_writes("analysis_financial.json",
                             _analysis("financial", "earnings_quality_accruals_rising"))]
    run, calls, asked = _financial_analyst_over_cli(tmp_path / "stop", monkeypatch, answers)
    _plant_row(tmp_path / "stop" / "AMD" / "0000002488-26-000001", at=limit_at)
    manifest = run_analysis.run_company(run=run, on_fable_limit="stop", **_run_keyword())
    assert _models_asked(calls) == ["fable"]
    assert asked["accounting-analyst"] == ["fable"] and asked["valuation-analyst"] == ["fable"]
    assert "model_fallback" not in manifest and manifest["analysis_failure"] is None


def test_two_analysts_in_parallel_the_shape_opens_the_row_and_the_message_confirms_it(
        tmp_path, monkeypatch, capsys):
    """The real `parallel`: the accounting analyst's Fable call fails like the
    limit and the financial analyst's, already on Fable beside it, answers the
    limit's message once the row is on record (the stub waits for it, so the
    order is the test's). Each analyst is called again on Opus and labelled by its
    own call's reading -- the shape, the message -- the row opened by the shape is
    raised to the limit's reason with `confirmed_by` naming the financial analyst,
    a later agent takes the row's reason at its call, and the run, its limit
    confirmed, prints the carry line."""
    _two_second_clock(monkeypatch)
    run = tmp_path / "NVDA" / NVDA_ACCESSION
    assemble_bundle.write(assemble_bundle.build("NVDA", "10-Q", accession=NVDA_ACCESSION,
                                                prior_runs=run.parent.parent), run)
    written, real_ask = _fake_ask({}), run_analysis.ask
    answers = {"accounting-analyst": [ZERO_TOKEN_FAILURE, _opus_writes(
                   "analysis_accounting.json",
                   _analysis("accounting", "earnings_quality_accruals_rising"))],
               "financial-analyst": [FABLE_LIMIT, _opus_writes(
                   "analysis_financial.json",
                   _analysis("financial", "earnings_quality_accruals_rising"))]}
    models: dict[str, list[str]] = {}
    lock, financial_on_fable = threading.Lock(), threading.Event()

    def cli(command, cwd, capture_output, text, timeout):
        agent = command[command.index("--agent") + 1]
        with lock:
            models.setdefault(agent, []).append(command[command.index("--model") + 1])
            exit_code, payload, files = answers[agent].pop(0)
        if agent == "accounting-analyst" and payload is ZERO_TOKEN_FAILURE[1]:
            # both on Fable at once: the shape answers once the other call is in
            financial_on_fable.wait(30)
        if agent == "financial-analyst" and payload is FABLE_LIMIT[1]:
            financial_on_fable.set()
            for _ in range(600):                       # up to thirty seconds
                if "model_fallback" in (run / "input_manifest.json").read_text(encoding="utf-8"):
                    break
                time.sleep(0.05)
        for name, content in (files or {}).items():
            (cwd / name).write_text(content)
        return _Done(exit_code, json.dumps(payload))

    def ask(directory, *, agent, writes, message, spec, log):
        if agent in answers:
            return real_ask(directory, agent=agent, writes=writes, message=message,
                            spec=spec, log=log)
        return dict(written(directory, agent=agent, writes=writes, message=message,
                            spec=spec, log=log),
                    model_requested=spec["model"], model_served=SERVED[spec["model"]])

    monkeypatch.setattr(run_analysis.subprocess, "run", cli)
    monkeypatch.setattr(run_analysis, "ask", ask)
    manifest = run_analysis.run_company(run=run, **_run_keyword())
    assert models == {"accounting-analyst": ["fable", "opus"],
                      "financial-analyst": ["fable", "opus"]}
    agents = manifest["agents"]
    assert agents["accounting-analyst"]["fallback_reason"] == "fable_failed_like_the_limit"
    assert agents["financial-analyst"]["fallback_reason"] == "fable_limit_reached"
    assert agents["valuation-analyst"]["fallback_reason"] == "fable_limit_reached"
    fallback = manifest["model_fallback"]
    assert fallback["first_agent"] == "accounting-analyst"
    assert fallback["reason"] == "fable_limit_reached"
    assert fallback["confirmed_by"] == "financial-analyst"
    assert manifest["analysis_failure"] is None
    monkeypatch.setattr(run_analysis, "run_company", lambda **kw: manifest)
    monkeypatch.setattr(run_analysis.interpreter_pin, "enforce", lambda: 0)
    capsys.readouterr()
    assert run_analysis.main(_main_command(run)) == 0
    assert "carries it on its own for 12 hours" in capsys.readouterr().err



def test_the_row_a_real_fallback_writes_is_utc_now_and_carries_through_the_clock_seam(
        tmp_path, monkeypatch):
    """The time on the row is the one the carry window is measured from, so it is
    checked against a clock the test takes itself. A real fallback -- the stub
    CLI answering the limit by its message, then writing on Opus -- runs with the
    process's local time set five hours behind UTC, so a stamp written in local
    time with a "Z" on it would land five hours off. The `at` the run wrote
    parses as UTC and lies between `datetime.now(timezone.utc)` read just before
    the run and just after it. That very row is then carried into a second run of
    the same batch, under the same root: its Fable agents go to Opus from their
    first call, the row naming the first run and its `at`. With the runner's
    clock moved through its one seam, `run_analysis.clock`, to twelve hours and a
    second after that `at` -- the stored row untouched -- a third run of the
    batch carries nothing and asks Fable; at twelve hours exactly the carry
    still holds."""
    root = tmp_path / "night"
    answers = [FABLE_LIMIT, _opus_writes("analysis_financial.json",
                                         _analysis("financial", "earnings_quality_accruals_rising"))]
    run, calls, asked = _financial_analyst_over_cli(root, monkeypatch, answers)
    pristine = tmp_path / "bundle"                     # outside the root, never run
    shutil.copytree(run, pristine)
    old_tz = os.environ.get("TZ")
    os.environ["TZ"] = "EST5"
    time.tzset()
    try:
        assert time.timezone == 5 * 3600               # local time is UTC less five hours
        before = dt.datetime.now(dt.timezone.utc)
        first = run_analysis.run_company(run=run, **_run_keyword())
        after = dt.datetime.now(dt.timezone.utc)
    finally:
        if old_tz is None:
            os.environ.pop("TZ", None)
        else:
            os.environ["TZ"] = old_tz
        time.tzset()
    assert _models_asked(calls) == ["fable", "opus"]
    row = first["model_fallback"]
    assert row["reason"] == "fable_limit_reached"
    written = dt.datetime.strptime(row["at"], "%Y-%m-%dT%H:%M:%SZ").replace(
        tzinfo=dt.timezone.utc)
    # the stamp is whole seconds, so the clock read before is taken to its second
    assert before.replace(microsecond=0) <= written <= after
    assert after - before < dt.timedelta(minutes=5)
    stored = (run / "input_manifest.json").read_bytes()

    # a second run of the same batch carries that very row
    monkeypatch.undo()
    second = root / "SECOND" / NVDA_ACCESSION
    shutil.copytree(pristine, second)
    answers = [_opus_writes("analysis_financial.json",
                            _analysis("financial", "earnings_quality_accruals_rising"))]
    _, calls, asked = _financial_analyst_over_cli(None, monkeypatch, answers, run=second)
    carried = run_analysis.run_company(run=second, **_run_keyword())
    assert _models_asked(calls) == ["opus"]
    assert asked["accounting-analyst"] == ["opus"] and asked["valuation-analyst"] == ["opus"]
    assert carried["model_fallback"]["carried_from"] == f"NVDA/{NVDA_ACCESSION}"
    assert carried["model_fallback"]["carried_limit_at"] == row["at"]
    assert carried["analysis_failure"] is None

    # the clock moved past the window, through the seam: a third run carries nothing
    monkeypatch.undo()
    third = root / "THIRD" / NVDA_ACCESSION
    shutil.copytree(pristine, third)
    window = dt.timedelta(hours=run_analysis.CARRY_HOURS)
    monkeypatch.setattr(run_analysis, "clock", lambda: written + window)
    assert run_analysis.batch_fallback(third)["carried_limit_at"] == row["at"]
    monkeypatch.setattr(run_analysis, "clock", lambda: written + window + dt.timedelta(seconds=1))
    assert run_analysis.batch_fallback(third) is None
    answers = [_fable_writes("analysis_financial.json",
                             _analysis("financial", "earnings_quality_accruals_rising"))]
    _, calls, asked = _financial_analyst_over_cli(None, monkeypatch, answers, run=third)
    late = run_analysis.run_company(run=third, **_run_keyword())
    assert _models_asked(calls) == ["fable"]
    assert asked["accounting-analyst"] == ["fable"] and asked["valuation-analyst"] == ["fable"]
    assert "model_fallback" not in late and late["analysis_failure"] is None
    assert (run / "input_manifest.json").read_bytes() == stored     # the row never moved


def _flagging_two_run(tmp_path, monkeypatch, **fake):
    run = tmp_path / "NVDA" / NVDA_ACCESSION
    bundle = assemble_bundle.build("NVDA", "10-Q", accession=NVDA_ACCESSION,
                                   prior_runs=run.parent.parent)
    assemble_bundle.write(bundle, run)
    monkeypatch.setattr(run_analysis, "ask", _fake_ask({}, **fake))
    manifest = run_analysis.run_company(run=run, ticker="NVDA", form="10-Q",
                                        cutoff="2026-08-26", period_end="2026-07-26",
                                        store=run_analysis.cutoff_guard.FIXTURES,
                                        prices=None, control="never")
    return run, manifest


def test_the_owner_finds_every_input_copy_of_a_whole_run_on_record(tmp_path, monkeypatch):
    """The owner's `inputs_on_record` over a whole stubbed run, both valuation
    passes graded: the MD&A cut to two paragraphs that were not adjacent, and
    the 8-K, none of whose 76 paragraphs was flagged, not placed. Under the seam
    trim it said "fail 31 of 35": the 8-K "carries no [id] paragraphs" and the
    MD&A "paragraph 0001045810-26-000075:mdna:1 ... word for word", in both
    passes. A seam-bearing copy put back in the second pass's directory is
    refused by the owner and by the boundary check."""
    from evals.common import PASS
    from evals.regression import mechanical
    run, manifest = _flagging_two_run(tmp_path, monkeypatch, notes_report=FLAGGING_TWO)
    assert manifest["analysis_failure"] is None
    # 76 paragraphs: counted on the fixture's 8-K, built once outside the tests
    # (2026-10-08), with `grep -c '^\[0001045810-26-000073:8k_2_02:' input_8k.md`
    # (76), the same 76 for `grep -c '\[0001045810-'`, so no marker sits off a
    # line start, and 76 distinct ids.
    for name in ("valuation-analyst", "valuation-analyst-second-pass"):
        record = manifest["agents"][name]["trimmed"]
        assert record["input_8k.md"]["kept"] == [] and record["input_8k.md"]["of"] == 76
        assert not (run / "agents" / name / "input_8k.md").exists()
    result = mechanical.check_inputs_on_record(run)
    assert result.status == PASS, result.failures
    assert agent_inputs.isolation_violations(run) == []
    seam = TRIMMED_TWO.replace(
        "Results of Operations\n\n",
        "Results of Operations\n\n[0001045810-26-000075:mdna:1] [0001045810-26-000075:mdna:3]\n\n")
    copy = run / "agents" / "valuation-analyst-second-pass" / "input_mdna.md"
    copy.unlink()
    copy.write_bytes(seam.encode("utf-8"))
    result = mechanical.check_inputs_on_record(run)
    assert result.status != PASS
    assert result.failures == ["agents/valuation-analyst-second-pass/input_mdna.md: paragraph "
                               "0001045810-26-000075:mdna:1 is not the file on record's, word "
                               "for word"]
    assert any(line.startswith("valuation-analyst-second-pass: input_mdna.md: paragraph "
                               "0001045810-26-000075:mdna:1")
               for line in agent_inputs.isolation_violations(run))


def test_a_fenced_block_that_is_not_json_is_counted_and_taken_out_of_the_copy(tmp_path):
    """A reader that writes its items as one list loses all of them to one trailing
    comma: the gate saw none of them and the owner counted "1 fenced block(s)
    that are not JSON" in the copy the analysts read. The real gate now records
    the block as a drop with no item id, and the copy holds no such block."""
    from evals.common import PASS
    from evals.regression import mechanical
    run = tmp_path / "run"
    run.mkdir()
    (run / "input_manifest.json").write_text(json.dumps({"accession": ESE_ACCESSION}))
    sales = "0001104659-26-092033:8k_2_02:36"
    good = _ese_item("results_against_expectations_sales_range_restated", "Sales guidance", sales)
    texts = {"numbers-reader": f"```json\n{json.dumps(good)}\n```\n",
             "notes-text-reader": ('```json\n[{"id": "results_against_expectations_eps_range_'
                                   'restated", "quote": "Adjusted EPS", "paragraph_id": '
                                   '"0001104659-26-092033:8k_2_02:37"},]\n```\n')}
    for name, text in texts.items():
        directory = agent_inputs.session_root(run, name)
        directory.mkdir(parents=True)
        (directory / "input_8k.md").write_text(ESE_8K, encoding="utf-8")
        (directory / agent_inputs.AGENTS[name].writes).write_text(text, encoding="utf-8")
    run_analysis.gate_readers(run)
    manifest = json.loads((run / "input_manifest.json").read_text())
    assert manifest["dropped_items"] == [{"report": "report_notes_text.md", "item_id": None,
                                          "reason": run_analysis.quote_gate.UNREADABLE_BLOCK}]
    copy = (run / "report_notes_text.md").read_text()
    assert mechanical.read_report_blocks(copy)[1] == 0
    assert mechanical.check_quotes_resolve(run).status == PASS


# --- what the runner stops on, run through the runner ------------------------------------------
#
# The whole stubbed NVDA run, each agent named in `leaves` writing the files named there
# beside its own output, as an agent with `Write` and a session rooted in its directory
# could. Each test says where the run stops, or that it finishes, and holds the run on
# disk to the owner's grader that answers for it (`evals/regression/`, read-only).

@pytest.fixture(scope="module")
def nvda_bundle(tmp_path_factory):
    """NVDA's 10-Q bundle, built once; each run below starts from a copy."""
    run = tmp_path_factory.mktemp("bundle") / "NVDA" / NVDA_ACCESSION
    assemble_bundle.write(assemble_bundle.build("NVDA", "10-Q", accession=NVDA_ACCESSION,
                                                prior_runs=run.parent.parent), run)
    return run


def _run_leaving(tmp_path, monkeypatch, bundle, leaves=None, *, then=None, control="never",
                 **fake):
    """The run, the directories asked in order, the manifest on disk, and the error
    the run stopped on (None when it finished). `then` maps a directory to what
    the agent does besides, after it wrote its files."""
    run = tmp_path / "NVDA" / NVDA_ACCESSION
    shutil.copytree(bundle, run)
    asked: list[str] = []
    answer = _fake_ask({}, **fake)

    def ask(directory, **keyword):
        asked.append(directory.name)
        record = answer(directory, **keyword)
        for name, data in (leaves or {}).get(directory.name, {}).items():
            (directory / name).write_bytes(data)
        if directory.name in (then or {}):
            then[directory.name](directory)
        return record

    monkeypatch.setattr(run_analysis, "ask", ask)
    stopped = None
    try:
        run_analysis.run_company(run=run, ticker="NVDA", form="10-Q", cutoff="2026-08-26",
                                 period_end="2026-07-26",
                                 store=run_analysis.cutoff_guard.FIXTURES, prices=None,
                                 control=control)
    except (agent_inputs.AgentInputError, run_analysis.analysis_check.AnalysisInputError,
            run_analysis.calculator.CalculatorInputError) as exc:
        stopped = exc
    manifest = json.loads((run / "input_manifest.json").read_text(encoding="utf-8"))
    return run, asked, manifest, stopped


def test_one_stray_word_a_reader_leaves_publishes_as_the_owner_passes_it(
        tmp_path, monkeypatch, nvda_bundle):
    """GNRC's notes reader left an eleven-byte "placeholder" beside its report
    (runs/GNRC/0001437749-26-025669/agents/notes-text-reader/scratch_check.txt), and
    the owner's layers_hold and inputs_on_record pass that published run and note
    the file. The runner's boundary check named it, so the run stopped once the
    readers returned, and the resume could not rebuild the reader's directory over
    it: a run the owner accepts was never published. It now finishes, and the
    owner passes it as it passed GNRC's."""
    from evals.common import PASS
    from evals.regression import mechanical
    run, asked, manifest, stopped = _run_leaving(
        tmp_path, monkeypatch, nvda_bundle,
        {"notes-text-reader": {"scratch_check.txt": b"placeholder"}})
    assert stopped is None, stopped
    assert manifest["analysis_failure"] is None and manifest.get(agent_inputs.ANALYSED_KEY)
    assert "valuation-analyst-second-pass" in asked
    layers, inputs = mechanical.check_layers_hold(run), mechanical.check_inputs_on_record(run)
    assert layers.status == PASS, layers.failures
    assert inputs.status == PASS, inputs.failures
    assert "['agents/notes-text-reader/scratch_check.txt']" in inputs.detail


def test_a_retired_agent_s_directory_made_during_a_call_stops_the_run(
        tmp_path, monkeypatch, nvda_bundle):
    """A directory under `agents/` named for a retired agent -- a comparer, a
    supervisor -- passed the boundary the runner checks, which judged it by the
    layer the agent had on the pilot runs, and the owner's layers_hold refuses it
    ("no layer the grader knows"). Made while the analysts run, it now stops the
    run once they return, before the valuation analyst is asked."""
    from evals.regression import mechanical
    run, asked, manifest, stopped = _run_leaving(
        tmp_path, monkeypatch, nvda_bundle,
        then={"financial-analyst": lambda directory: (
            directory.parent / "numbers-vs-market").mkdir()})
    assert isinstance(stopped, agent_inputs.AgentInputError), stopped
    assert "after accounting-analyst, financial-analyst returned" in str(stopped)
    assert "numbers-vs-market: a retired agent's directory" in manifest["stopped_on"]
    assert "valuation-analyst" not in asked and agent_inputs.ANALYSED_KEY not in manifest
    assert "agents/numbers-vs-market: no layer the grader knows" \
        in mechanical.check_layers_hold(run).failures


# Each stop below is pinned to the call that makes it: the place the run stopped is
# asserted, so a runner that no longer called the check there stops later, or not
# at all, and the test fails. What the run leaves on disk is held to the owner's
# grader that answers for it, which refuses it.

DRAFT = {"draft.json": b'{"items": []}'}


def test_a_file_a_reader_leaves_stops_the_run_before_any_analyst_is_asked(
        tmp_path, monkeypatch, nvda_bundle):
    from evals.regression import mechanical
    run, asked, manifest, stopped = _run_leaving(tmp_path, monkeypatch, nvda_bundle,
                                                 {"notes-text-reader": DRAFT})
    assert isinstance(stopped, agent_inputs.AgentInputError), stopped
    assert "after numbers-reader, notes-text-reader returned" in str(stopped)
    assert "notes-text-reader: holds draft.json" in manifest["stopped_on"]
    assert sorted(asked) == ["notes-text-reader", "numbers-reader"]
    assert agent_inputs.ANALYSED_KEY not in manifest
    assert "agents/notes-text-reader/draft.json: not a file the notes-text-reader layer sees" \
        in mechanical.check_layers_hold(run).failures


def _night(run, monkeypatch, **keyword):
    """One more invocation over the run on disk, every agent writing as the stub
    writes: the directories asked, in order, and the manifest the run finished
    with or the error it stopped on."""
    asked: list[str] = []
    answer = _fake_ask({})

    def ask(directory, **kw):
        asked.append(directory.name)
        return answer(directory, **kw)

    monkeypatch.setattr(run_analysis, "ask", ask)
    try:
        return asked, run_analysis.run_company(run=run, **_run_keyword(), **keyword), None
    except (agent_inputs.AgentInputError, run_analysis.RunError) as exc:
        return asked, None, exc


@pytest.mark.parametrize("left_by, clean", [("notes-text-reader", "numbers-reader"),
                                            ("accounting-analyst", "financial-analyst")])
def test_a_boundary_stop_after_two_agents_puts_the_one_that_left_nothing_on_record(
        tmp_path, monkeypatch, nvda_bundle, left_by, clean):
    """One of two agents called side by side leaves a file in its directory, and
    the run stops when both return. The other's output is gated into the run
    root first, so it is on record: while the file stands no agent is called at
    all, by default or under --resume, and once it is removed by hand the resume
    calls the agent that left it and what comes after, never the other. Nothing
    of the stage was on record before: each night the file stood called the
    clean reader or analyst again, a paid call, and once more after it was
    removed (the critic's probe, 2026-10-08: three numbers-reader calls, four
    financial-analyst calls). The other side, before and after: the agent that
    left the file is not on record and is called again, and the run finishes
    once the file is gone."""
    from evals.common import PASS
    from evals.regression import mechanical
    run, asked, manifest, stopped = _run_leaving(tmp_path, monkeypatch, nvda_bundle,
                                                 {left_by: DRAFT})
    assert isinstance(stopped, agent_inputs.AgentInputError), stopped
    assert f"{left_by}: holds draft.json" in manifest["stopped_on"]
    assert not (run / run_analysis.OUTPUT_ON_RECORD[left_by][0]).exists()
    assert not run_analysis.on_record(run, left_by, manifest["agents"][left_by])
    assert run_analysis.on_record(run, clean, manifest["agents"][clean])
    for resume in (False, True):
        called, _, error = _night(run, monkeypatch, resume=resume)
        assert called == [] and isinstance(error, agent_inputs.AgentInputError), (resume, error)
        assert str(error).startswith("the boundary is broken before this invocation called")
        assert f"{left_by}: holds draft.json" in str(error)
    (run / "agents" / left_by / "draft.json").unlink()
    called, manifest, error = _night(run, monkeypatch)
    assert error is None, error
    assert manifest["analysis_failure"] is None and agent_inputs.ANALYSED_KEY in manifest
    assert mechanical.check_layers_hold(run).status == PASS
    attempts = {name: len(run_analysis.attempts_of(record))
                for name, record in manifest["agents"].items()}
    assert attempts[left_by] == 2
    assert called[0] == left_by and clean not in called and attempts[clean] == 1
    assert clean in manifest["resume_skipped"]


def test_no_agent_is_called_while_the_boundary_stands_broken(tmp_path, monkeypatch, nvda_bundle):
    """A retired agent's directory made while the analysts ran sits in neither
    analyst's directory: both are gated into the run root before the run stops.
    While it stands, the next night calls no agent. The earlier runner called
    both analysts again and stopped after them; with the analysts on record and
    no check before the first call, the valuation analyst would be called, paid
    for, and stopped on the same directory. Removed by hand, the resume calls
    the two valuation passes and nothing before them. The other side, before
    and after: the owner refuses the run while the directory stands and passes
    the run that finishes once it is gone."""
    from evals.common import PASS
    from evals.regression import mechanical
    retired = {"financial-analyst": lambda directory: (
        directory.parent / "numbers-vs-market").mkdir()}
    run, asked, manifest, stopped = _run_leaving(tmp_path, monkeypatch, nvda_bundle,
                                                 then=retired)
    assert isinstance(stopped, agent_inputs.AgentInputError), stopped
    assert "agents/numbers-vs-market: no layer the grader knows" \
        in mechanical.check_layers_hold(run).failures
    assert all(run_analysis.on_record(run, name, manifest["agents"][name])
               for name in ("accounting-analyst", "financial-analyst"))
    called, _, error = _night(run, monkeypatch)
    assert called == [] and isinstance(error, agent_inputs.AgentInputError), error
    assert "numbers-vs-market: a retired agent's directory" in str(error)
    (run / "agents" / "numbers-vs-market").rmdir()
    called, manifest, error = _night(run, monkeypatch)
    assert error is None, error
    assert mechanical.check_layers_hold(run).status == PASS
    assert called == ["valuation-analyst", "valuation-analyst-second-pass"]


def test_a_file_the_valuation_analyst_leaves_stops_the_run_before_its_second_pass(
        tmp_path, monkeypatch, nvda_bundle):
    from evals.regression import mechanical
    run, asked, manifest, stopped = _run_leaving(tmp_path, monkeypatch, nvda_bundle,
                                                 {"valuation-analyst": DRAFT})
    assert isinstance(stopped, agent_inputs.AgentInputError), stopped
    assert str(stopped).startswith("the boundary is broken after valuation-analyst returned")
    assert asked[-1] == "valuation-analyst" and "valuation-analyst-second-pass" not in asked
    assert agent_inputs.ANALYSED_KEY not in manifest
    assert "agents/valuation-analyst/draft.json: not a file the valuation-analyst layer sees" \
        in mechanical.check_layers_hold(run).failures


def test_a_file_the_control_leaves_stops_the_run_before_its_files_are_gated(
        tmp_path, monkeypatch, nvda_bundle):
    from evals.regression import mechanical
    control = run_analysis.CONTROL_DIRNAME
    run, asked, manifest, stopped = _run_leaving(tmp_path, monkeypatch, nvda_bundle,
                                                 {control: DRAFT}, control="always")
    assert isinstance(stopped, agent_inputs.AgentInputError), stopped
    assert str(stopped).startswith("the boundary is broken after the control returned")
    assert asked[-1] == control
    assert not any((run / name).exists() for name in run_analysis.CONTROL_WRITES)
    assert agent_inputs.ANALYSED_KEY not in manifest
    assert f"{control}/draft.json: not a file the {control} layer sees" \
        in mechanical.check_layers_hold(run).failures


def test_a_stray_word_the_run_s_memo_contradicts_stops_the_run_before_it_is_finished(
        tmp_path, monkeypatch, nvda_bundle):
    """One word under the name `memo_ko.md`, left by the notes reader: the owner
    passes it while the run has no memo, so every check after an agent returned
    passes it too, and refuses it once the memo is written ("not the run's
    memo_ko.md"). The check before the run is recorded as finished meets it."""
    from evals.regression import mechanical
    run, asked, manifest, stopped = _run_leaving(
        tmp_path, monkeypatch, nvda_bundle,
        {"notes-text-reader": {"memo_ko.md": b"placeholder"}})
    assert isinstance(stopped, agent_inputs.AgentInputError), stopped
    assert str(stopped).startswith(
        "the boundary is broken before the run was recorded as finished")
    assert "valuation-analyst-second-pass" in asked and (run / "memo_ko.md").is_file()
    assert agent_inputs.ANALYSED_KEY not in manifest
    assert "agents/notes-text-reader/memo_ko.md: not the run's memo_ko.md" \
        in mechanical.check_inputs_on_record(run).failures


LATE_ADJUSTMENT = {"direction": "reduce", "applies_to": "cash_flow",
                   "calculator_field": "terms.trailing_four_quarters.revenue",
                   "quote": "59.63738684902464", "quote_from": "report_numbers.md"}


@pytest.mark.parametrize("name, stops", [("2027-06-30", True), ("deferred revenue", False)])
def test_a_calculator_stage_carrying_a_date_after_the_cutoff_stops_the_run(
        tmp_path, monkeypatch, nvda_bundle, name, stops):
    """AAPL's accounting analyst could name an adjustment "2027-06-30": the
    analysis gate keeps the name (a date is a name it allows), the calculator
    copies it into the quality-adjusted free cash flow, and the owner's
    nothing_after_cutoff reads every string of every calculator file. Here the
    NVDA analyst names it, quoting the numbers reader's kept item: the run stops
    before calculator_before_drivers.json is written. A name that is no date
    publishes."""
    from evals.common import PASS
    from evals.regression import mechanical
    analysis = _analysis("accounting", "earnings_quality_accruals_rising")
    analysis["adjustments"] = [dict(LATE_ADJUSTMENT, name=name)]
    run, asked, manifest, stopped = _run_leaving(tmp_path, monkeypatch, nvda_bundle,
                                                 accounting_analysis=analysis)
    if not stops:
        assert stopped is None, stopped
        assert mechanical.check_nothing_after_cutoff(run).status == PASS
        return
    assert isinstance(stopped, run_analysis.calculator.CalculatorInputError), stopped
    assert str(stopped).startswith(
        "calculator_before_drivers.json would carry what the cutoff and the finite-number "
        "rule refuse (1): free_cash_flow.free_cash_flow_quality_adjusted."
        "adjustments_applied[0].name = 2027-06-30 is after the cutoff 2026-08-26")
    assert not (run / "calculator_before_drivers.json").exists()
    assert "valuation-analyst" not in asked and agent_inputs.ANALYSED_KEY not in manifest


def test_with_the_calculator_check_taken_out_the_late_date_is_published_and_refused(
        tmp_path, monkeypatch, nvda_bundle):
    """The other side of the test above: the same run, with the runner's check
    of each calculator stage taken out, finishes and publishes the date, and the
    owner's nothing_after_cutoff refuses the run."""
    from evals.regression import mechanical
    monkeypatch.setattr(run_analysis, "calculator_problems", lambda payload, cutoff: [])
    analysis = _analysis("accounting", "earnings_quality_accruals_rising")
    analysis["adjustments"] = [dict(LATE_ADJUSTMENT, name="2027-06-30")]
    run, _, manifest, stopped = _run_leaving(tmp_path, monkeypatch, nvda_bundle,
                                             accounting_analysis=analysis)
    assert stopped is None and manifest.get(agent_inputs.ANALYSED_KEY)
    assert "calculator_before_drivers.json: free_cash_flow.free_cash_flow_quality_adjusted." \
        "adjustments_applied[0].name = 2027-06-30" \
        in mechanical.check_nothing_after_cutoff(run).failures


def test_a_memo_line_carrying_a_ruled_out_word_stops_the_run_before_it_is_finished(
        tmp_path, monkeypatch, nvda_bundle):
    """The analysis gate holds every word an analyst writes that the memo prints,
    so what is held here is the memo itself, whatever it comes to print: a line
    the memo composes with "매수 추천" in it stops the run once the memo is
    written, and the owner's forbidden_words refuses the memo left on disk."""
    from evals.regression import coverage
    composed = run_analysis.memo.memo

    def memo_with_a_line(**keyword):
        return composed(**keyword) + "- 매수 추천\n"

    monkeypatch.setattr(run_analysis.memo, "memo", memo_with_a_line)
    run, asked, manifest, stopped = _run_leaving(tmp_path, monkeypatch, nvda_bundle)
    assert isinstance(stopped, run_analysis.analysis_check.AnalysisInputError), stopped
    lines = (run / "memo_ko.md").read_text(encoding="utf-8").splitlines()
    assert str(stopped) == f"memo_ko.md:{len(lines)} carries a ruled-out word ('매수 추천')"
    assert "valuation-analyst-second-pass" in asked
    assert agent_inputs.ANALYSED_KEY not in manifest
    assert f"memo_ko.md:{len(lines)}: 매수 추천" in coverage.check_forbidden_words(run).failures
