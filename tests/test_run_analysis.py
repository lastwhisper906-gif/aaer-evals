"""The run orchestrator's own logic, without calling a model.

A model call is the one thing this suite does not make. What is judged here is
what the orchestrator decides by itself: that every analyst runs its committed
definition and nothing written at run time, that the message it sends names the
directory's files and its one output, and that the reports downstream sees carry
only the items the quote gate kept.
"""

from __future__ import annotations

import json

from src import agent_inputs, run_analysis


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
              numbers_report: str = NUMBERS_REPORT):
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
                text = json.dumps(_analysis("accounting", "earnings_quality_accruals_rising"))
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


def _run_with_accounting_analyst_answering(tmp_path, monkeypatch, answers):
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
                                        prices=None, control="never")
    return run, manifest, calls


def test_a_zero_token_two_second_failure_stops_the_run_and_exits_four(tmp_path, monkeypatch):
    _two_second_clock(monkeypatch)
    run, manifest, calls = _run_with_accounting_analyst_answering(
        tmp_path, monkeypatch, [ZERO_TOKEN_FAILURE] * 3)
    assert len(calls) == 1
    assert manifest["fable_limit_reached"] == ["accounting-analyst"]
    assert "no token spent" in manifest["agents"]["accounting-analyst"]["reason"]
    assert (run / "analysis_financial.json").is_file() and (run / "memo_ko.md").is_file()
    monkeypatch.setattr(run_analysis, "run_company", lambda **kw: manifest)
    monkeypatch.setattr(run_analysis.interpreter_pin, "enforce", lambda: 0)
    assert run_analysis.main(["--run", str(run), "--ticker", "NVDA", "--form", "10-Q",
                              "--cutoff", "2026-08-26", "--period-end", "2026-07-26"]) == 4


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
                                       prices=None, control="never")
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
                                       prices=None, control=control, model=model)
    assert stopped["fable_limit_reached"] == [stopped_agent]
    return run, stopped


def _resumed(run, monkeypatch, control: str, model: str | None = None,
             notes_report: str = "no items\n", numbers_report: str = NUMBERS_REPORT):
    ask, called = _counting_ask({}, notes_report=notes_report, numbers_report=numbers_report)
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
    manifest, called = _resumed(run, monkeypatch, "never", notes_report=NOTES_SHARING_THE_ID,
                                numbers_report=NUMBERS_WITH_A_BAD_QUOTE)
    assert "numbers-reader" not in called
    assert (run / "report_numbers.md").read_bytes() == numbers_before
    assert manifest["dropped_items"][:1] == stopped["dropped_items"]        # appended after
    assert [(row["report"], row["item_id"]) for row in manifest["dropped_items"]] == [
        ("report_numbers.md", "earnings_quality_planted_bad_quote"),
        ("report_notes_text.md", SHARED_ID)]
    assert ("on more than one item in this run: it stands in report_numbers.md"
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
    (failed / "input_manifest.json").write_text(json.dumps(manifest))
    with pytest.raises(run_analysis.RunError, match="did not stop at the limit"):
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
                                        prices=None, control="always")
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
               "--cutoff", "2026-08-26", "--period-end", "2026-07-26"]
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
                                        prices=None, control="always")
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


def test_this_tree_has_no_golden_cases_and_the_manifest_says_so(tmp_path, monkeypatch):
    """The cases directory and its reader come with the evals branch; until it
    lands, the control does not run under --control auto, and the run's manifest
    says that rather than that no case names the filing."""
    assert not run_analysis.GOLDEN_CASES.exists()
    assert run_analysis.is_golden_filing(NVDA_ACCESSION) == (False, run_analysis.NO_GOLDEN_CASES)
    assert run_analysis.is_golden_filing(None) == (False, run_analysis.NO_GOLDEN_CASES)
    manifest = _run_with_control(tmp_path, monkeypatch, "auto")
    assert "control-single-agent" not in manifest["agents"]
    assert manifest["control_reason"] == run_analysis.NO_GOLDEN_CASES
    assert manifest["analysis_stages"]["control"] == f"skipped: {run_analysis.NO_GOLDEN_CASES}"
    assert manifest["analysis_failure"] is None


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
# the first block, one line holding the two markers, and the third block.
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
    "[0001045810-26-000075:mdna:1] [0001045810-26-000075:mdna:3]\n\n"
    "[0001045810-26-000075:mdna:3]\n[same as prior period, unchanged from "
    "0001045810-26-000052:mdna:3]\n\n")
INSIDE = {"reason": "a reason", "quote": "Analysis of Financial Condition",
          "quote_from": "input_mdna.md"}
ACROSS = {"reason": "a reason", "quote_from": "input_mdna.md",
          "quote": "Results of Operations\n\n[0001045810-26-000075:mdna:1] "
                   "[0001045810-26-000075:mdna:3]\n\n[0001045810-26-000075:mdna:3]\n[same as"}


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
    # the seam rule: the bear scenario quotes across the two blocks' seam, which
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
    valuation analyst's MD&A holds the file's preamble and no paragraph, the manifest
    records the trim beside the agent's usage, and the notes reader's own copy holds
    every paragraph."""
    run, manifest, _ = finished
    valuation = (run / "agents" / "valuation-analyst" / "input_mdna.md").read_text()
    reader = (run / "agents" / "notes-text-reader" / "input_mdna.md").read_text()
    assert valuation == reader[:reader.index("[0001045810-26-000075:mdna:")]
    assert "trimmed" not in valuation
    assert "[0001045810-" not in valuation                        # no marker survives
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
