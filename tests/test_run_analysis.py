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
# EDGAR's acceptance of that 10-Q: `filings.recent.acceptanceDateTime` for the
# accession in data.sec.gov/submissions/CIK0001045810.json, read on 2026-10-06 as
# 2026-08-26T20:36:00.000Z. EDGAR writes its trailing Z on a stamp whose clock is
# Eastern (src/market.py, `_acceptance`), so the Z is dropped and the stamp is
# the Eastern wall clock. The fixture carries no acceptance time; see the test.
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


def _fake_ask(seen: dict):
    def ask(directory, *, agent, writes, message, spec, log):
        seen[directory.name] = sorted(path.name for path in directory.iterdir())
        for name in writes:
            if name == "report_numbers.md":
                text = NUMBERS_REPORT
            elif name == "report_notes_text.md":
                text = "no items\n"
            elif name == "analysis_accounting.json":
                text = json.dumps(_analysis("accounting", "earnings_quality_accruals_rising"))
            elif name == "analysis_financial.json":
                text = json.dumps(_analysis("financial", "earnings_quality_accruals_rising"))
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
                                            prices=None)
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
                                        prices=None, model="opus")
    # both valuation passes run the one committed valuation-analyst definition
    assert sorted(agent for agent, _ in asked) == sorted([
        "numbers-reader", "notes-text-reader", "accounting-analyst", "financial-analyst",
        "valuation-analyst", "valuation-analyst", "control-single-agent"])
    assert {model for _, model in asked} == {"opus"}
    assert manifest["model_override"]["model"] == "opus"
    assert run_analysis.definition("accounting-analyst")["model"] == "fable"


def test_with_no_model_named_each_agent_asks_for_its_own(finished):
    _, manifest, _ = finished
    assert "model_override" not in manifest


def test_a_run_with_a_market_table_is_labelled_by_python_and_never_marked_unavailable(tmp_path, monkeypatch):
    """NVDA's 10-Q was filed on 2026-08-26, a Wednesday, and EDGAR accepted it at
    20:36 Eastern that day: `NVDA_ACCEPTED` below, from the submissions index.
    The fixture under tests/fixtures/NVDA carries no acceptance time (the fetch
    projects the index to filing dates, and every fixture file is held to the
    manifest's hash, so the stamp cannot be written onto a row by hand; queue.md
    carries the item that makes the fetch keep it). After the four o'clock close,
    so day zero is Thursday the 27th and the window runs to Monday the 31st.
    Abnormal returns 0.02, 0.01 and 0.00 sum to 0.03."""
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
                                        prices=None)
    assert manifest["analysis_stages"]["market_labels"]["written"] is True
    assert manifest.get("market_table") != "unavailable"
    labels = json.loads((run / "market_labels.json").read_text())
    assert [one["labels"][0]["label"] for one in labels["items"]] == ["priced_in"]
