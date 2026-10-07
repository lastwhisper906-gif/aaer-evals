"""The analysis gate and the memo, judged on analyses written here by hand.

Every expected value below is a rule stated in `docs/CHECKLIST.md` §7 or in the
three analyst prompts, applied by hand to an analysis written in this file:
a `{path}` that resolves stands, one that does not drops its item; a digit in an
analyst's own words drops its item; an evidence id that is not an item of a
report the analyst saw drops its item; a quote that is not in the file it names
drops its item; the owner's ruled-out words drop their item; and the memo puts
the calculator's number where the analyst put the path.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from src import analysis_check, memo

FIELDS = {
    "ticker": "TEST", "form": "10-Q", "period_end": "2026-06-30", "cutoff": "2026-07-30",
    "missing": [],
    "trend_table": {"quarters-back-0": {"ratios": {"gross_margin": {"value": 0.7}}}},
    "ratios": {"liquidity": {"current_ratio": {"value": 2.5, "unit": "ratio"},
                             "cash_runway_months": {"value": None, "not_burning_cash": True,
                                                    "reason": "free cash flow is positive"}},
               "profitability": {"gross_margin": {"value": 0.4, "unit": "ratio"}},
               "efficiency": {"days_sales_outstanding": {"value": 61.25, "unit": "days"}}},
    "terms": {"trailing_four_quarters": {"revenue": {"value": 1.5e9, "unit": "USD"},
                                         "share_based_compensation": {"value": 3e7, "unit": "USD"}}},
    "earnings_versus_cash": {"history": {"years": [{"revenue_growth": 0.1}]}},
    "free_cash_flow": {"free_cash_flow_quality_adjusted": {"adjustments_applied": []}},
    "valuation": {"missing": "no price"},
}

NUMBERS = '''```json
{ "id": "revenue_recognition_receivables_rising", "what_changed": "x", "quote": "q", "paragraph_id": "p" }
```'''
NOTES = '''```json
{ "id": "revenue_recognition_payment_terms_extended", "what_changed": "y",
  "expected_direction": "up", "quote": "extended payment terms to certain customers",
  "paragraph_id": "p2" }
```
[p2] We extended payment terms to certain customers during the quarter.'''
SOURCES = {"report_numbers.md": NUMBERS, "report_notes_text.md": NOTES}

AREA = {"finding": "Days sales outstanding rose to {ratios.efficiency.days_sales_outstanding}.",
        "verdict": "weaker", "evidence": ["revenue_recognition_receivables_rising"],
        "fields": ["ratios.efficiency.days_sales_outstanding"]}


def accounting(**changes):
    payload = {
        "question": "do reported earnings and cash reflect economic reality?",
        "areas": {name: copy.deepcopy(AREA) for name in analysis_check.ACCOUNTING_AREAS},
        "reconciliation": [{"notes_item": "revenue_recognition_payment_terms_extended",
                            "numbers_items": ["revenue_recognition_receivables_rising"],
                            "outcome": "confirms", "why": "both rise"}],
        "anomalies": [{"id": "revenue_recognition_receivables_outrun_revenue",
                       "name": "receivables outrun revenue", "area": "revenue_recognition",
                       "what": "DSO at {ratios.efficiency.days_sales_outstanding}",
                       "numbers_vs_prose": "confirms",
                       "evidence": ["revenue_recognition_payment_terms_extended"],
                       "fields": []}],
        "adjustments": [{"name": "extended terms", "direction": "reduce",
                         "applies_to": "cash_flow",
                         "calculator_field": "terms.trailing_four_quarters.revenue",
                         "quote": "extended payment terms to certain customers",
                         "quote_from": "report_notes_text.md", "evidence": []}],
        "summary_ko": {"earnings_versus_cash": "매출채권 회전일수는 {ratios.efficiency.days_sales_outstanding}입니다."},
        "limits": analysis_check.LIMITS["accounting"],
    }
    payload.update(changes)
    return payload


def test_an_exclusion_keyed_by_report_takes_the_id_out_of_that_report_alone():
    """One id printed in both reports, dropped from the notes report only (a
    resumed night's twin): a bare citation of it is refused, because by id alone
    it would name the dropped notes item as well as the standing numbers one;
    a reconciliation row naming it as the notes item is refused, naming it as
    the numbers item stands on that side; the same id as a plain set is out of
    both; and with nothing dropped the bare citation stands. The adjustment
    quotes the notes item that fell: a dropped item is no unit a quote can stand
    in (the owner's `units_of`), so it falls with it wherever the notes item is
    dropped, and stands where it stood."""
    shared = "revenue_recognition_payment_terms_extended"
    numbers = NUMBERS + f'''
```json
{{ "id": "{shared}", "what_changed": "z", "quote": "q", "paragraph_id": "p" }}
```'''
    sources = {"report_numbers.md": numbers, "report_notes_text.md": NOTES}
    payload = accounting(reconciliation=[
        {"notes_item": shared, "numbers_items": [], "outcome": "unresolved", "why": "a"},
        {"notes_item": "revenue_recognition_payment_terms_extended_twin_free",
         "numbers_items": [shared], "outcome": "unresolved", "why": "b"}])
    payload["anomalies"][0]["evidence"] = [shared]
    out = analysis_check.check("accounting", payload, fields=FIELDS, sources=sources,
                               excluded={"report_notes_text.md": {shared}})
    assert out["anomalies"] == []
    assert [row["where"] for row in out["dropped_items"]] == [
        "reconciliation[0]", "reconciliation[1]", "anomalies[0]", "adjustments[0]"]
    assert out["dropped_items"][3]["reason"] == (
        "adjustments[0]: the quote is in no one paragraph, value or kept report item of the "
        "file it names")
    assert out["dropped_items"][0]["reason"] == (
        f"notes_item {shared!r} is not an item of report_notes_text.md")
    assert "twin_free" in out["dropped_items"][1]["reason"]          # its own notes side
    assert out["dropped_items"][2]["reason"] == (
        f"evidence: {shared!r} is an id the quote gate dropped from a report this analyst "
        "saw, so by id alone it does not name one standing item")
    # the same id as a plain set: out of both reports, every citation falls
    out = analysis_check.check("accounting", payload, fields=FIELDS, sources=sources,
                               excluded={shared})
    assert out["anomalies"] == []
    assert [row["where"] for row in out["dropped_items"]] == [
        "reconciliation[0]", "reconciliation[1]", "anomalies[0]", "adjustments[0]"]
    # dropped from the numbers report alone: the notes-side row stands, the bare
    # citation still falls
    out = analysis_check.check("accounting", payload, fields=FIELDS, sources=sources,
                               excluded={"report_numbers.md": {shared}})
    assert [row["where"] for row in out["dropped_items"]] == ["reconciliation[1]",
                                                               "anomalies[0]"]
    # the other side: nothing dropped, the bare citation names the one item
    # printed in each report under that id and stands, as do both rows' sides
    out = analysis_check.check("accounting", payload, fields=FIELDS, sources=sources)
    assert [a["id"] for a in out["anomalies"]] == ["revenue_recognition_receivables_outrun_revenue"]
    assert [row["where"] for row in out["dropped_items"]] == ["reconciliation[1]"]


def test_a_clean_analysis_stands_whole():
    out = analysis_check.check("accounting", accounting(), fields=FIELDS, sources=SOURCES)
    assert out["dropped_count"] == 0
    assert len(out["anomalies"]) == 1 and len(out["adjustments"]) == 1


def test_a_number_in_the_analysts_own_words_drops_the_item():
    payload = accounting()
    payload["anomalies"][0]["what"] = "DSO rose to 61 days"
    out = analysis_check.check("accounting", payload, fields=FIELDS, sources=SOURCES)
    assert out["anomalies"] == []
    assert out["dropped_count"] == 1


def test_a_form_name_and_a_year_are_not_numbers():
    payload = accounting()
    payload["anomalies"][0]["what"] = "the 10-Q for fiscal 2026 says so"
    out = analysis_check.check("accounting", payload, fields=FIELDS, sources=SOURCES)
    assert out["dropped_count"] == 0


def test_a_path_that_is_not_a_number_drops_the_item():
    payload = accounting()
    payload["anomalies"][0]["what"] = "{ratios.efficiency.nothing_here}"
    out = analysis_check.check("accounting", payload, fields=FIELDS, sources=SOURCES)
    assert out["anomalies"] == []


def test_an_evidence_id_no_report_carries_drops_the_item():
    payload = accounting()
    payload["anomalies"][0]["evidence"] = ["revenue_recognition_invented"]
    out = analysis_check.check("accounting", payload, fields=FIELDS, sources=SOURCES)
    assert out["anomalies"] == []


def test_a_quote_not_in_the_named_report_drops_the_adjustment():
    payload = accounting()
    payload["adjustments"][0]["quote"] = "payment terms were never changed"
    out = analysis_check.check("accounting", payload, fields=FIELDS, sources=SOURCES)
    assert out["adjustments"] == []


def test_a_quote_folds_whitespace_one_for_one_as_the_quote_gate_does():
    """The owner's fold of 2026-09-23: each whitespace character reads as one space,
    one for one, and a quote that stood only through it is counted. A run of two
    spaces against one is not the same text and is not folded into it."""
    payload = accounting()
    payload["adjustments"][0]["quote"] = "extended payment\nterms to certain customers"
    out = analysis_check.check("accounting", payload, fields=FIELDS, sources=SOURCES)
    assert len(out["adjustments"]) == 1
    assert out["normalized_quotes"] == 1
    payload["adjustments"][0]["quote"] = "extended  payment terms to certain customers"
    out = analysis_check.check("accounting", payload, fields=FIELDS, sources=SOURCES)
    assert out["adjustments"] == []


def test_an_anomaly_that_cites_nothing_is_dropped():
    payload = accounting()
    payload["anomalies"][0]["evidence"] = []
    payload["anomalies"][0]["fields"] = []
    payload["anomalies"][0]["what"] = "something is off"
    assert analysis_check.check("accounting", payload, fields=FIELDS,
                                sources=SOURCES)["anomalies"] == []


def test_a_bare_four_digit_number_is_a_number_and_a_named_year_is_not():
    payload = accounting()
    payload["anomalies"][0]["what"] = "inventory of 2048 million"
    assert analysis_check.check("accounting", payload, fields=FIELDS,
                                sources=SOURCES)["anomalies"] == []
    payload["anomalies"][0]["what"] = "since fiscal 2024, under ASC 606 and ASU 2022-04, in Note 12"
    assert analysis_check.check("accounting", payload, fields=FIELDS,
                                sources=SOURCES)["dropped_count"] == 0


def test_a_derivative_or_a_korean_ruled_out_word_is_caught():
    for text in ("fraudulent activity", "the figures were manipulated", "분식 의심"):
        payload = accounting()
        payload["anomalies"][0]["what"] = text
        assert analysis_check.check("accounting", payload, fields=FIELDS,
                                    sources=SOURCES)["anomalies"] == [], text


def test_the_korean_name_is_held_to_the_same_rule():
    payload = accounting()
    payload["anomalies"][0]["name_ko"] = "매출채권 61일"
    assert analysis_check.check("accounting", payload, fields=FIELDS,
                                sources=SOURCES)["anomalies"] == []


def test_a_brace_that_is_not_a_placeholder_drops_the_item():
    payload = accounting()
    payload["anomalies"][0]["what"] = "DSO { ratios.efficiency.days_sales_outstanding }"
    assert analysis_check.check("accounting", payload, fields=FIELDS,
                                sources=SOURCES)["anomalies"] == []


def test_the_ruled_out_words_drop_their_item():
    payload = accounting()
    payload["anomalies"][0]["what"] = "this looks like fraud"
    out = analysis_check.check("accounting", payload, fields=FIELDS, sources=SOURCES)
    assert out["anomalies"] == []


def test_a_failing_area_keeps_its_name_and_says_it_was_dropped():
    payload = accounting()
    payload["areas"]["cost_deferral"]["finding"] = "capitalized cost rose 12 percent"
    out = analysis_check.check("accounting", payload, fields=FIELDS, sources=SOURCES)
    assert "dropped" in out["areas"]["cost_deferral"]
    assert set(out["areas"]) == set(analysis_check.ACCOUNTING_AREAS)


def test_an_area_left_out_is_named_as_missing():
    payload = accounting()
    del payload["areas"]["industry_lens"]
    out = analysis_check.check("accounting", payload, fields=FIELDS, sources=SOURCES)
    assert out["areas"]["industry_lens"] == {"dropped": "the analyst wrote nothing for it"}


def test_a_contradiction_is_an_outcome_and_a_made_up_one_is_not():
    payload = accounting()
    payload["reconciliation"][0]["outcome"] = "contradicts"
    assert analysis_check.check("accounting", payload, fields=FIELDS,
                                sources=SOURCES)["reconciliation"]
    payload["reconciliation"][0]["outcome"] = "mostly fine"
    assert not analysis_check.check("accounting", payload, fields=FIELDS,
                                    sources=SOURCES)["reconciliation"]


def test_an_anomaly_id_starts_with_its_area():
    payload = accounting()
    payload["anomalies"][0]["id"] = "receivables_outrun_revenue"
    assert analysis_check.check("accounting", payload, fields=FIELDS,
                                sources=SOURCES)["anomalies"] == []


def test_the_limits_sentence_is_the_rules_version_own():
    payload = accounting(limits="we looked hard")
    out = analysis_check.check("accounting", payload, fields=FIELDS, sources=SOURCES)
    assert out["limits"] == analysis_check.LIMITS["accounting"]
    assert any(row["where"] == "limits" for row in out["dropped_items"])


def test_the_valuation_analysis_may_not_say_buy():
    payload = {"value_range": {"reading": "a buy at this range", "fields": []},
               "price_position": {"reading": "not computed", "fields": []},
               "market_implied_growth": {"reading": "not computed", "fields": []},
               "accounting_adjustments": {"reading": "none", "fields": []},
               "most_sensitive": [], "summary_ko": {}, "limits": ""}
    out = analysis_check.check("valuation", payload, fields=FIELDS, sources={})
    assert "dropped" in out["value_range"]


def test_an_assumption_scenario_without_a_reason_is_dropped_whole():
    driver = {"reason": "the base case", "fields": ["ratios.profitability.gross_margin"]}
    scenario = {name: 0.02 for name in ("revenue_growth_year_one", "terminal_growth",
                                         "operating_margin_year_one",
                                         "operating_margin_year_ten",
                                         "reinvestment_rate_year_one",
                                         "reinvestment_rate_year_ten")}
    good = dict(scenario, reasons={name: driver for name in scenario})
    bad = dict(scenario, reasons={})
    out = analysis_check.check_assumptions({"scenarios": {"bear": bad, "base": good,
                                                          "bull": good}},
                                           fields=FIELDS, sources={})
    assert set(out["scenarios"]) == {"base", "bull"}
    assert out["dropped_count"] == 1


def test_a_quote_across_a_seam_of_the_trimmed_prose_fails_the_gate():
    """A copy cut to the flagged paragraphs with one line holding the two markers
    between kept blocks that were not adjacent -- the trim's shape until
    2026-10-07, kept here as the hardest case. A quote inside a kept block
    string-matches the copy and the filing; one running off the end of the
    second paragraph into the start of the fourth string-matches the copy, and
    nothing the filing printed. The copy alone now tells too: the quote stands
    in no one paragraph of it, which is the owner's rule."""
    two, four = "0000000000-00-000001:mdna:2", "0000000000-00-000001:mdna:4"
    filing = (f"# T mdna\n\n[0000000000-00-000001:mdna:1]\nFirst.\n\n[{two}]\nSecond, kept.\n\n"
              f"[0000000000-00-000001:mdna:3]\nThird.\n\n[{four}]\nFourth, kept.\n")
    copy_seen = (f"# T mdna\n\n[{two}]\nSecond, kept.\n\n[{two}] [{four}]\n\n"
                 f"[{four}]\nFourth, kept.\n")
    sources, full = {"input_mdna.md": copy_seen}, {"input_mdna.md": filing}
    inside = {"quote": "Second, kept.", "quote_from": "input_mdna.md"}
    across = {"quote": f"Second, kept.\n\n[{two}] [{four}]\n\n[{four}]\nFourth, kept.",
              "quote_from": "input_mdna.md"}
    assert across["quote"] in copy_seen and across["quote"] not in filing
    assert analysis_check.quote_problem(inside, sources, full) is None
    assert analysis_check.quote_problem(across, sources) is None     # the copy alone: passes
    problem = analysis_check.quote_problem(across, sources, full)
    assert problem is not None and "across a seam" in problem
    # And through the first pass's gate: the scenario quoting across the seam is dropped.
    scenario = {name: 0.02 for name in ("revenue_growth_year_one", "terminal_growth",
                                         "operating_margin_year_one",
                                         "operating_margin_year_ten",
                                         "reinvestment_rate_year_one",
                                         "reinvestment_rate_year_ten")}
    good = dict(scenario, reasons={name: dict(inside, reason="r") for name in scenario})
    bad = dict(scenario, reasons={name: dict(across, reason="r") for name in scenario})
    out = analysis_check.check_assumptions({"scenarios": {"bear": bad, "base": good, "bull": good}},
                                           fields=FIELDS, sources=sources, filing=full)
    assert set(out["scenarios"]) == {"base", "bull"}
    assert "across a seam" in out["dropped_items"][0]["reason"]
    without = analysis_check.check_assumptions({"scenarios": {"bear": bad, "base": good, "bull": good}},
                                               fields=FIELDS, sources=sources)
    assert set(without["scenarios"]) == {"base", "bull"}    # one paragraph of the copy alone
    assert "in no one paragraph" in without["dropped_items"][0]["reason"]


# --- the module's own command ------------------------------------------------------------

SEAM_TWO, SEAM_FOUR = "0000000000-00-000001:mdna:2", "0000000000-00-000001:mdna:4"
SEAM_FILING = (f"# T mdna\n\n[0000000000-00-000001:mdna:1]\nFirst.\n\n[{SEAM_TWO}]\nSecond, kept.\n\n"
               f"[0000000000-00-000001:mdna:3]\nThird.\n\n[{SEAM_FOUR}]\nFourth, kept.\n")
SEAM_COPY = (f"# T mdna\n\n[{SEAM_TWO}]\nSecond, kept.\n\n[{SEAM_TWO}] [{SEAM_FOUR}]\n\n"
             f"[{SEAM_FOUR}]\nFourth, kept.\n")
DRIVERS = ("revenue_growth_year_one", "terminal_growth", "operating_margin_year_one",
           "operating_margin_year_ten", "reinvestment_rate_year_one", "reinvestment_rate_year_ten")


def _scenarios(reason: dict) -> dict:
    scenario = {name: 0.02 for name in DRIVERS}
    return dict(scenario, reasons={name: dict(reason, reason="r") for name in DRIVERS})


def _command(tmp_path, *, kind: str, written: dict, agent_files: dict[str, str],
             run_files: dict[str, str] | None, dropped: list[dict] = ()) -> list[str]:
    """A run directory and an agent directory on disk, and the command over them;
    `run_files` None leaves `--run` off."""
    agent = tmp_path / "agents" / "valuation-analyst"
    agent.mkdir(parents=True, exist_ok=True)
    for name, text in agent_files.items():
        (agent / name).write_text(text, encoding="utf-8")
    (tmp_path / "written.json").write_text(json.dumps(written), encoding="utf-8")
    (tmp_path / "calculator.json").write_text(json.dumps(FIELDS), encoding="utf-8")
    command = ["--kind", kind, "--agent-dir", str(agent), "--written", str(tmp_path / "written.json"),
               "--calculator", str(tmp_path / "calculator.json"), "--out", str(tmp_path / "out.json")]
    if run_files is not None:
        for name, text in run_files.items():
            (tmp_path / name).write_text(text, encoding="utf-8")
        (tmp_path / "input_manifest.json").write_text(
            json.dumps({"accession": "0000000000-00-000001", "dropped_items": list(dropped)}),
            encoding="utf-8")
        command += ["--run", str(tmp_path)]
    return command


def test_the_command_holds_a_valuation_quote_to_the_filing_and_refuses_to_run_without_it(
        tmp_path, monkeypatch, capsys):
    """Through the command with --run, the scenario quoting across the seam of the
    trimmed copy is dropped, as in the pipeline; a quote the filing printed
    passes; and the assumptions kind without --run is refused with the reason."""
    monkeypatch.setattr(analysis_check.interpreter_pin, "enforce", lambda: 0)
    inside = {"quote": "Second, kept.", "quote_from": "input_mdna.md"}
    across = {"quote": f"Second, kept.\n\n[{SEAM_TWO}] [{SEAM_FOUR}]\n\n[{SEAM_FOUR}]\nFourth, kept.",
              "quote_from": "input_mdna.md"}
    written = {"scenarios": {"bear": _scenarios(across), "base": _scenarios(inside),
                             "bull": _scenarios(inside)}}
    command = _command(tmp_path / "seam", kind="assumptions", written=written,
                       agent_files={"input_mdna.md": SEAM_COPY},
                       run_files={"input_mdna.md": SEAM_FILING})
    assert analysis_check.main(command) == 0
    out = json.loads((tmp_path / "seam" / "out.json").read_text(encoding="utf-8"))
    assert set(out["scenarios"]) == {"base", "bull"}
    assert "across a seam" in out["dropped_items"][0]["reason"]
    assert "assumptions -- 1 dropped" in capsys.readouterr().err
    # the other side: every quote the filing printed, nothing dropped
    written = {"scenarios": {name: _scenarios(inside) for name in ("bear", "base", "bull")}}
    command = _command(tmp_path / "printed", kind="assumptions", written=written,
                       agent_files={"input_mdna.md": SEAM_COPY},
                       run_files={"input_mdna.md": SEAM_FILING})
    assert analysis_check.main(command) == 0
    out = json.loads((tmp_path / "printed" / "out.json").read_text(encoding="utf-8"))
    assert set(out["scenarios"]) == {"bear", "base", "bull"} and out["dropped_count"] == 0
    # without --run the valuation kinds are refused, before anything is read
    command = _command(tmp_path / "norun", kind="assumptions", written=written,
                       agent_files={"input_mdna.md": SEAM_COPY}, run_files=None)
    assert analysis_check.main(command) == analysis_check.BAD_INPUT
    err = capsys.readouterr().err
    assert "needs --run" in err and "across a seam" in err
    assert not (tmp_path / "norun" / "out.json").exists()
    command = _command(tmp_path / "norun_valuation", kind="valuation", written={},
                       agent_files={}, run_files=None)
    assert analysis_check.main(command) == analysis_check.BAD_INPUT


def test_the_command_refuses_a_citation_of_a_dropped_id_with_the_runs_drop_rows(
        tmp_path, monkeypatch, capsys):
    """An accounting analysis citing an id the manifest's drop rows name for the
    notes report: through the command with --run the citation is refused, as in
    the pipeline; without --run the rows are not read, the command says so, and
    the citation stands -- the copy alone cannot tell."""
    monkeypatch.setattr(analysis_check.interpreter_pin, "enforce", lambda: 0)
    dropped = [{"report": "report_notes_text.md", "reason": "planted",
                "item_id": "revenue_recognition_payment_terms_extended"}]
    command = _command(tmp_path / "rows", kind="accounting", written=accounting(),
                       agent_files=SOURCES, run_files={}, dropped=dropped)
    assert analysis_check.main(command) == 0
    out = json.loads((tmp_path / "rows" / "out.json").read_text(encoding="utf-8"))
    assert out["anomalies"] == []
    reasons = [row["reason"] for row in out["dropped_items"]]
    assert any("an id the quote gate dropped from a report this analyst saw" in r for r in reasons)
    capsys.readouterr()
    command = _command(tmp_path / "norows", kind="accounting", written=accounting(),
                       agent_files=SOURCES, run_files=None)
    assert analysis_check.main(command) == 0
    out = json.loads((tmp_path / "norows" / "out.json").read_text(encoding="utf-8"))
    assert [a["id"] for a in out["anomalies"]] == ["revenue_recognition_receivables_outrun_revenue"]
    assert "no --run: the gate's drop rows were not read" in capsys.readouterr().err


# --- the memo ---------------------------------------------------------------------------

def test_the_memo_puts_the_calculators_number_where_the_path_was():
    """61.25 days is written '61.2일' or '61.3일'; Python's own format rounds half to even
    on the binary value, so the test reads it as one decimal of 61.25."""
    text = memo.fill("회전일수 {ratios.efficiency.days_sales_outstanding}", FIELDS)
    assert text == f"회전일수 {61.25:,.1f}일"
    assert memo.fill("{ratios.profitability.gross_margin|pct}", FIELDS) == "40.0%"
    assert memo.fill("{terms.trailing_four_quarters.revenue}", FIELDS) == "15.0억 달러"


def test_the_memo_prints_a_unit_once_and_a_particle_that_agrees_with_it():
    """The CSCO memo of 2026-09-28 printed "37.2일일" and "65.2억 달러과". Expected
    Korean worked by hand: 달러 ends in a vowel, so 과 becomes 와 and 이 becomes 가;
    % is read 퍼센트, so 을 becomes 를; 5 is read 오 and 0 is read 영, so 1.5 takes
    로 and 2.50 takes 으로; 일 ends in ㄹ, which takes 로, never 으로."""
    fill = memo.fill
    assert fill("회전일수 {ratios.efficiency.days_sales_outstanding}일로 높다", FIELDS) \
        == f"회전일수 {61.25:,.1f}일로 높다"
    assert fill("매출 {terms.trailing_four_quarters.revenue}과 이익", FIELDS) == "매출 15.0억 달러와 이익"
    assert fill("매출 {terms.trailing_four_quarters.revenue}이 늘고", FIELDS) == "매출 15.0억 달러가 늘고"
    assert fill("{ratios.profitability.gross_margin|pct}%을 넘어", FIELDS) == "40.0%를 넘어"
    assert fill("{ratios.liquidity.current_ratio}으로", FIELDS) == "2.500으로"
    assert fill("{ratios.efficiency.days_sales_outstanding}으로", FIELDS) == f"{61.25:,.1f}일로"
    # a syllable that is not a particle stays as the analyst wrote it
    assert fill("{ratios.liquidity.current_ratio}이상", FIELDS) == "2.500이상"


def test_the_memo_keeps_the_three_analyses_apart_and_adds_nothing_up():
    checked = analysis_check.check("accounting", accounting(), fields=FIELDS, sources=SOURCES)
    text = memo.memo(ticker="TEST", form="10-Q", period_end="2026-06-30", cutoff="2026-07-30",
                     fields=FIELDS, accounting=checked, financial=None, valuation=None,
                     baselines=None)
    # Two top-level sections, 회계 and 재무, by the owner's decision of 2026-10-06;
    # the financial analysis and the valuation are the two subsections of 재무.
    assert (text.index("\n## 1. 회계\n") < text.index("\n### 1.1 회계 분석")
            < text.index("\n## 2. 재무\n") < text.index("\n### 2.1 재무 분석")
            < text.index("\n### 2.2 가치평가"))
    analyses = text[:text.index("\n## 참고")]
    assert [line for line in analyses.splitlines() if line.startswith("## ")] == [
        "## 1. 회계", "## 2. 재무"]
    assert "no price" in text
    for word in ("종합 점수", "순위", "매수", "매도"):
        assert word not in text.replace("회사 간 순위는 없습니다", "")


def test_a_trend_table_label_with_hyphens_is_a_path():
    payload = accounting()
    payload["anomalies"][0]["what"] = "gross margin {trend_table.quarters-back-0.ratios.gross_margin|pct}"
    out = analysis_check.check("accounting", payload, fields=FIELDS, sources=SOURCES)
    assert out["dropped_count"] == 0


def test_a_cited_field_that_states_why_it_has_no_value_stands_but_not_in_a_sentence():
    payload = accounting()
    payload["anomalies"][0]["fields"] = ["ratios.liquidity.cash_runway_months"]
    assert analysis_check.check("accounting", payload, fields=FIELDS,
                                sources=SOURCES)["dropped_count"] == 0
    payload["anomalies"][0]["what"] = "runway {ratios.liquidity.cash_runway_months}"
    assert analysis_check.check("accounting", payload, fields=FIELDS,
                                sources=SOURCES)["anomalies"] == []


def test_a_filing_date_an_item_number_and_a_form_before_a_korean_particle_are_not_numbers():
    payload = accounting()
    payload["anomalies"][0]["what"] = "an 8-K filed 2026-07-02 under Item 5.02"
    payload["summary_ko"]["earnings_versus_cash"] = "임원 변동 8-K의 본문은 없습니다."
    out = analysis_check.check("accounting", payload, fields=FIELDS, sources=SOURCES)
    assert out["dropped_count"] == 0


def test_the_memo_never_prints_what_the_gate_dropped():
    payload = accounting()
    payload["areas"]["cost_deferral"]["finding"] = "capitalized cost rose 12 percent, fraud risk"
    checked = analysis_check.check("accounting", payload, fields=FIELDS, sources=SOURCES)
    text = memo.memo(ticker="TEST", form="10-Q", period_end="2026-06-30", cutoff="2026-07-30",
                     fields=FIELDS, accounting=checked, financial=None, valuation=None,
                     baselines=None)
    assert "12 percent" not in text and "fraud" not in text
    assert "제외된 문장" in text


def test_the_memo_names_a_cost_of_debt_fallback_where_the_calculator_labels_one():
    """The decision of docs/needs_judgment.md: the fallback is labelled in
    calculator.json and in the memo. With `cost_of_capital.pre_tax_cost_of_debt.fallback`
    the valuation section carries one line with the label verbatim; without it, no
    such line, and the memo prints no number of its own either way."""
    label = ("the risk-free rate plus one point, because neither interest expense nor "
             "interest paid is on record: interest_expense: no row")
    with_fallback = copy.deepcopy(FIELDS)
    with_fallback["cost_of_capital"] = {"pre_tax_cost_of_debt": {"value": 0.0566,
                                                                   "fallback": label}}
    text = memo.memo(ticker="TEST", form="10-Q", period_end="2026-06-30", cutoff="2026-07-30",
                     fields=with_fallback, accounting=None, financial=None, valuation=None,
                     baselines=None)
    valuation = text[text.index("### 2.2 가치평가"):text.index("## 참고")]
    assert memo.FALLBACK_KO in valuation
    assert label in valuation
    assert "0.0566" not in text and "5.66" not in text

    without = copy.deepcopy(FIELDS)
    without["cost_of_capital"] = {"pre_tax_cost_of_debt": {"value": 0.05}}
    text = memo.memo(ticker="TEST", form="10-Q", period_end="2026-06-30", cutoff="2026-07-30",
                     fields=without, accounting=None, financial=None, valuation=None,
                     baselines=None)
    assert memo.FALLBACK_KO not in text and "risk-free" not in text
    assert memo.cost_of_debt_fallback_line(FIELDS) == []


def test_the_memo_prints_the_free_cash_flow_yield_wacc_components_and_growth_beside_history():
    """The three blocks beside the DCF, with numbers written here by hand, each
    printed in the valuation section the way the section prints its other lines:
    a rate as a percentage to one decimal (0.0371 is 3.7%, 0.03 is 3.0%), a dollar
    amount in 억 (1,531,119,000 is 15.3억 달러), a beta to three decimals, a source
    after a dash, and a row with no value naming the calculator's reason. A
    calculator.json without the blocks prints none of these lines."""
    fields = copy.deepcopy(FIELDS)
    fields["free_cash_flow_yield"] = {
        "free_cash_flow_to_firm_over_enterprise_value": {"value": 0.0371, "unit": "ratio"},
        "free_cash_flow_to_equity_over_market_value_of_equity": {"value": 0.058, "unit": "ratio"}}
    fields["wacc_components"] = {"rows": [
        {"input": "risk_free_rate", "value": 0.04, "source": "DGS10 on 2026-06-04; planted"},
        {"input": "beta", "value": 1.2, "source": "against SPY, 250 trading days"},
        {"input": "total_debt", "value": 1_531_119_000.0, "source": "debt_current + debt_noncurrent"},
        {"input": "wacc", "value": None, "missing": "the cost of equity needs a beta and a price"}]}
    fields["implied_growth_beside_history"] = {
        "implied_ten_year_revenue_growth": {"value": 0.03},
        "revenue_growth_three_year_compound": {"value": 0.095},
        "revenue_growth_five_year_compound": {"missing": "4 fiscal years on record, and "
                                                         "5-year compound growth needs 6"}}
    text = memo.memo(ticker="TEST", form="10-Q", period_end="2026-06-30", cutoff="2026-07-30",
                     fields=fields, accounting=None, financial=None, valuation=None,
                     baselines=None)
    valuation = text[text.index("### 2.2 가치평가"):text.index("## 참고")]
    assert (f"- {memo.GROWTH_BESIDE_HISTORY_KO}: 3.0% · 과거 3년 연평균: 9.5% · 과거 5년 연평균: "
            "(4 fiscal years on record, and 5-year compound growth needs 6)") in valuation
    assert (f"- {memo.YIELD_KO}: 기업 잉여현금흐름 / 기업가치 3.7% · "
            "주주 잉여현금흐름 / 시가총액 5.8%") in valuation
    assert f"- {memo.WACC_COMPONENTS_KO}:" in valuation
    assert "  - 무위험이자율: 4.0% — DGS10 on 2026-06-04; planted" in valuation
    assert "  - 베타: 1.200 — against SPY, 250 trading days" in valuation
    assert "  - 총차입금: 15.3억 달러 — debt_current + debt_noncurrent" in valuation
    assert "  - WACC: (계산 안 됨: the cost of equity needs a beta and a price)" in valuation
    assert memo.beside_the_dcf_lines(FIELDS) == []
    without = memo.memo(ticker="TEST", form="10-Q", period_end="2026-06-30", cutoff="2026-07-30",
                        fields=FIELDS, accounting=None, financial=None, valuation=None,
                        baselines=None)
    for word in (memo.GROWTH_BESIDE_HISTORY_KO, memo.YIELD_KO, memo.WACC_COMPONENTS_KO):
        assert word not in without


def test_the_memo_prints_one_growth_beside_history_line_with_a_computed_valuation():
    """Two-sided, after the second lens's second reading, through the branch a
    published calculator.json takes: a valuation with a value range and a reverse
    DCF with a value. Without the block the memo prints the line it always printed
    -- the reverse DCF's 0.04 beside the history's three-year 0.095 -- and no
    five-year figure; with the block it prints the block's line -- 0.03, 9.5%,
    6.2% -- and not the old one; never both."""
    priced = copy.deepcopy(FIELDS)
    priced["valuation"] = {"value_range_per_share": {"low": 50.0, "high": 70.0},
                           "price_at_cutoff": 60.0, "price_position": "inside the range",
                           "reverse_dcf": {"value": 0.04, "price": 60.0}}
    priced["earnings_versus_cash"]["history"]["revenue_growth_three_year_compound"] = 0.095

    def growth_lines(text: str) -> list[str]:
        return [line for line in text.splitlines()
                if line.startswith(f"- {memo.GROWTH_BESIDE_HISTORY_KO}")]

    without = memo.memo(ticker="TEST", form="10-Q", period_end="2026-06-30", cutoff="2026-07-30",
                        fields=priced, accounting=None, financial=None, valuation=None,
                        baselines=None)
    assert "주당 50.00달러 ~ 주당 70.00달러" in without
    assert growth_lines(without) == [
        f"- {memo.GROWTH_BESIDE_HISTORY_KO}: 4.0% · 과거 3년 연평균: 9.5%"]
    assert "과거 5년" not in without

    with_block = copy.deepcopy(priced)
    with_block["implied_growth_beside_history"] = {
        "implied_ten_year_revenue_growth": {"value": 0.03},
        "revenue_growth_three_year_compound": {"value": 0.095},
        "revenue_growth_five_year_compound": {"value": 0.062}}
    text = memo.memo(ticker="TEST", form="10-Q", period_end="2026-06-30", cutoff="2026-07-30",
                     fields=with_block, accounting=None, financial=None, valuation=None,
                     baselines=None)
    assert "주당 50.00달러 ~ 주당 70.00달러" in text
    assert growth_lines(text) == [
        f"- {memo.GROWTH_BESIDE_HISTORY_KO}: 3.0% · 과거 3년 연평균: 9.5% · 과거 5년 연평균: 6.2%"]
    assert "4.0%" not in text


def test_the_control_cites_the_paragraphs_of_its_own_input():
    sources = {"input_notes.md": "[acc:notes:1] We extended payment terms to certain customers.\n"}
    payload = accounting()
    payload["anomalies"][0]["evidence"] = ["acc:notes:1"]
    payload["reconciliation"] = []
    payload["adjustments"][0]["quote_from"] = "input_notes.md"
    for area in payload["areas"].values():
        area["evidence"] = ["acc:notes:1"]
    out = analysis_check.check("accounting", payload, fields=FIELDS, sources=sources,
                               paragraph_ids=True)
    assert out["dropped_count"] == 0


def test_a_bare_year_in_a_reason_is_a_year_not_a_number():
    """The phrasings, trimmed to the words that decide them; the reasons the eight
    published runs of 2026-09-29 recorded are below, verbatim and hand-read, in
    PUBLISHED_WINDOWS and PUBLISHED_ITEMS."""
    for text in ("the second half of 2026", "through 2027, then flat", "laps in December 2026",
                 "the June 2026 quarter", "year-end 2025",
                 # the second lens's cases of 2026-10-06: a year-context word before or
                 # after, a range dash, a fiscal prefix, a Korean year suffix
                 "in 2026", "fiscal 2027 guidance", "through 2030", "2026년",
                 "December 2026", "FY2026", "the second half of 2026", "2026 outlook",
                 "mid-2026", "as of 2026", "2026 하반기",
                 # phrasings the eight published analyses of 2026-09-29 use
                 "the first six months of 2026", "a first-quarter 2026 amendment",
                 "notes due 2030", "far above 2022's",
                 "회계연도 2025 수준", "the fiscal-2025 figure",
                 # a date or a range after a context word is read whole (AAPL's valuation
                 # analyst quoted "no row for interest_expense in 2024-09-29..2025-09-27")
                 "no row in 2024-09-29..2025-09-27", "in 2024-2026", "in 2024–2026",
                 # the third reading's cases: a year-terminator after the context word's
                 # year, and a list that borrows its context from a member
                 "by the end of 2030", "in 2030.", "in 2030 and 2031", "in 2026 the company",
                 "2021 and 2022 guidance", "the first six months of 2026 ran at",
                 # the fourth and fifth readings' cases, the words the published runs
                 # dropped: "for" or a period phrase -- an ordinal half or quarter, a
                 # year-end, a month, "due" -- before a year and a terminator after it,
                 # a verb the published text writes after a year among the terminators,
                 # "year-end" and a month whole after a year
                 "for 2027, a backlog", "the first half of 2027 turns",
                 "the first quarter of 2026 carried", "ended April 2026 printed",
                 "notes due 2030 assumed", "the first half of 2026 carries",
                 "second-half-2025 and 2026", "at the 2025 year-end", "2026 December",
                 "2026 May", "in 2026 May", "March 2026",
                 # a year outside 1950-2049 is a year by the same words: a net-zero
                 # target, a comparison with the crash
                 "2050년", "2055 fiscal year", "in 2050", "since 1929",
                 # a Korean unit written apart from the number is a word of its own
                 "2025년", "회계연도 2025 대비",
                 # queue item one's last reading: the words GNRC's and AAPL's valuation
                 # analysts wrote, read by eye as years in PUBLISHED_ITEMS, which the
                 # rule now reads with them (each side's counts are in
                 # test_each_named_year_context_reads_its_year_and_drops_the_count_beside_it)
                 "the margins of 2021, 2022 and 2023", "the growth of 2021 and 2022",
                 "the second half of 2025 loss-making recur"):
        payload = accounting()
        payload["anomalies"][0]["what"] = text
        assert analysis_check.check("accounting", payload, fields=FIELDS,
                                    sources=SOURCES)["dropped_count"] == 0, text


def test_a_korean_unit_against_a_number_makes_it_a_count():
    """The fourth reading: 억, 만, 천, 원, 개, 명, 주, 건, 대 written against a four-digit
    number are quantity words, with or without a context word before it."""
    for text in ("2025억", "2048개", "2026만", "2030천", "2027원", "2031명", "2029주",
                 "2032건", "2033대", "회계연도 2025억", "in 2048개", "2,025억 원"):
        payload = accounting()
        payload["anomalies"][0]["what"] = text
        out = analysis_check.check("accounting", payload, fields=FIELDS, sources=SOURCES)
        assert out["anomalies"] == [], text
        assert "a number written in the analyst's own words" in json.dumps(
            out["dropped_items"], ensure_ascii=False), text


RUNS = Path(__file__).resolve().parents[1] / "runs"

# Every `dropped_items` entry of the eight published runs of 2026-09-29 (AAPL, CARR,
# CIEN, CSCO, GNRC, LFUS, PANW, STX; `runs/<ticker>/<accession>/assumptions.json`,
# `analysis_accounting.json`, `analysis_financial.json`) whose reason carries a
# four-digit year: 91 items, gated then by the rule before this branch, which read no
# bare year at all. Two tables, each row carrying a reading made by eye before the
# rule was run on it -- "year" when every digit in the text is a year in the analyst's
# meaning, "number" when the text carries a figure the analyst wrote -- and, where the
# rule as written disagrees with that reading, why it does. The tests assert the rule
# agrees with every reading; a row with a reason is `xfail(strict=True)`, a recorded
# disagreement and not a pass. The first table holds the eighty-character window the
# old gate quoted around the first digit, verbatim (a placeholder folded to a blank, a
# window two items share listed once); the second holds the item itself, gated whole
# from the analyst's written file in the run's agents directory.
PUBLISHED_WINDOWS = (
    # run file item · the window · the hand reading · why the rule disagrees, or None
    ('AAPL assumptions.json scenarios.base',
     'ing, and above the flat stretch of   to 2025, on the view that a growing install',
     'year',
     '"to" is no year context: "leases to 2040" is a count'),
    ('AAPL assumptions.json scenarios.bull',
     'year in the record that grew faster was 2021 at  .',
     'year',
     None),
    ('CARR analysis_accounting.json areas.earnings_versus_cash',
     "ve the company's own fiscal years of   (2025),   (2023) and   (2021), and far ab",
     'year',
     'a parenthesised number has no year context: "(2025)" is a count'),
    ('CARR analysis_accounting.json areas.revenue_recognition',
     'econd highest of five years, above   in 2024 and   in 2023. Contract liabilities',
     'year',
     None),
    ('CARR analysis_accounting.json areas.estimates_and_reserves',
     'he lowest of five years, down from   in 2024 and   in 2023, with the allowance i',
     'year',
     None),
    ('CARR analysis_accounting.json areas.cost_deferral',
     'ailing four quarters against the fiscal-2025 figure, and lower in the six months',
     'year',
     None),
    ('CARR analysis_accounting.json areas.controls_audit_and_filing_signals',
     'pt differs from the annual one, and the 2021 net-income concept differs from lat',
     'year',
     '"the" is no year context'),
    ('CARR analysis_accounting.json areas.industry_lens',
     " above the year-ago quarter's   and the 2024 annual  ; days sales of inventory c",
     'year',
     '"the" is no year context'),
    ('CARR analysis_accounting.json anomalies[6]',
     'the earnings series is lumpy because of 2024 discontinued-operations gains and a',
     'year',
     '"of" alone is no year context: "inventory of 2048" is a count'),
    ('CARR analysis_accounting.json anomalies[24]',
     '  , highest of five years, against   in 2023; driven by lower cash and flat prop',
     'year',
     None),
    ('CARR analysis_accounting.json anomalies[25]',
     'iling R&D expense   is below the fiscal-2025 figure and the six months are below',
     'year',
     None),
    ('CARR analysis_accounting.json anomalies[37]',
     'cer-and-director item was filed in July 2026, four days before the  ; its body i',
     'year',
     None),
    ('CARR analysis_accounting.json anomalies[40]',
     'ept differs from the annual one and the 2021 net-income concept differs from lat',
     'year',
     '"the" is no year context'),
    ('CARR analysis_financial.json sections.profitability',
     "below  's  , and the MD&A says the June 2026 quarter's gross margin fell again o",
     'year',
     None),
    ('CARR analysis_financial.json sections.efficiency',
     " history the picture is mixed: the June 2026 quarter's DSO of   days is second l",
     'year',
     None),
    ('CARR analysis_financial.json sections.solvency',
     'ease also shows higher than at year-end 2025. Trailing EBITDA is   and debt over',
     'year',
     None),
    ('CARR analysis_financial.json sections.growth',
     'al fell. The Riello sale closed in July 2026 and Noresco is pending; both are st',
     'year',
     None),
    ('CARR analysis_financial.json dupont',
     "no stockholders' equity row at the June 2026 date, so the product is not compute",
     'year',
     None),
    ('CARR analysis_financial.json path_to_distress',
     'ions is met in the filings for the June 2026 quarter: free cash flow is positive',
     'year',
     None),
    ('CARR analysis_financial.json anomalies[4]',
     'ows total equity lower than at year-end 2025 as treasury stock grew. A large aut',
     'year',
     None),
    ('CARR analysis_financial.json anomalies[5]',
     'alance sheet rose sharply from year-end 2025. Operating cash flow over net incom',
     'year',
     None),
    ('CARR analysis_financial.json anomalies[9]',
     'ighest of five years, and   in the June 2026 quarter.',
     'year',
     None),
    ('CARR analysis_financial.json anomalies[11]',
     ' income is down  . The first quarter of 2026 carried heavy restructuring, and th',
     'year',
     None),
    ('CARR analysis_financial.json anomalies[14]',
     'ighest of five years, and   in the June 2026 quarter, third highest of seven. Da',
     'year',
     None),
    ('CARR analysis_financial.json anomalies[15]',
     "ond highest of five years and the March 2026 quarter's   days the highest of sev",
     'year',
     None),
    ('CARR analysis_financial.json anomalies[18]',
     'erest-expense row for the first half of 2026. Net non-operating interest expense',
     'year',
     None),
    ('CARR analysis_financial.json anomalies[19]',
     'ows total equity lower than at year-end 2025 with treasury stock and accumulated',
     'year',
     None),
    ('CIEN analysis_financial.json anomalies[7]',
     '회계연도 2025 연간 매출총이익률은 오 년 중 최저였고, 분기 회복도 과거 수준에는 미달',
     'year',
     None),
    ('CIEN analysis_financial.json summary_ko.solvency',
     '합니다. 다만 이 여유는 최근 급증한 영업이익에 기대고 있어, 회계연도 2025의 영업이익   수준으로 돌아가면 이자비용   대비 여유가 크게 ',
     'year',
     None),
    ('CIEN analysis_financial.json summary_ko.path_to_distress',
     '부담이 위기로 바뀌려면 영업이익이 회계연도 2025 수준인  으로 되돌아가 이자보상배율  배가 얇아지고, 구매약정  이 수요 둔화 속에 재고로 ',
     'year',
     None),
    ('CSCO analysis_accounting.json areas.controls_audit_and_filing_signals',
     'ndex lists two filings in April and May 2026 under the item code for officer or ',
     'year',
     None),
    ('CSCO analysis_accounting.json anomalies[22]',
     'ranged sale plans in February and March 2026, shortly after the prior  . Routine',
     'year',
     None),
    ('GNRC analysis_accounting.json areas.earnings_versus_cash',
     " and the year before's  , but far above 2022's  ; the annual accruals ratio   si",
     'year',
     None),
    ('GNRC analysis_accounting.json areas.revenue_recognition',
     "six months already exceeds the whole of 2025's, so deposits are converting faste",
     'year',
     None),
    ('GNRC analysis_accounting.json areas.estimates_and_reserves',
     '   a year earlier and   at the start of 2025; the allowance balance is   against',
     'year',
     None),
    ('GNRC analysis_accounting.json areas.industry_lens',
     "ears against   the year before, after a 2025 inventory build; the  's reserve ro",
     'year',
     '"a" is no year context'),
    ('GNRC analysis_accounting.json anomalies[5]',
     "ludes the loss-making fourth quarter of 2025 with its legal fees. The release's ",
     'year',
     None),
    ('GNRC analysis_accounting.json anomalies[7]',
     'd calls nearly seven hundred million of 2027 volume committed. Different dates, ',
     'year',
     '"of" alone is no year context: "inventory of 2048" is a count'),
    ('GNRC analysis_accounting.json anomalies[10]',
     '   a year earlier and   at the start of 2025; the balance fell to   from   while',
     'year',
     None),
    ('GNRC analysis_accounting.json anomalies[12]',
     ' legal add-back includes a release of a 2022 clean-energy warranty provision, un',
     'year',
     '"a" is no year context'),
    ('GNRC analysis_accounting.json anomalies[17]',
     ' concept; the   shows it rising through 2025 with a charge to expense, and no 20',
     'year',
     'the window cuts "no 2026" to "no 20", and "no" is no year context'),
    ('GNRC analysis_accounting.json anomalies[23]',
     'rscale supply agreements with committed 2027 volume, and the release describes a',
     'year',
     '"committed" is no year context'),
    ('GNRC analysis_accounting.json anomalies[34]',
     "arter's  . The  's reserve rose through 2025, no 2026 reserve exists, the tariff",
     'year',
     '"no" is no year context'),
    ('GNRC analysis_accounting.json anomalies[35]',
     'tomer above ten percent of sales (  for 2025) and one customer at   of receivabl',
     'year',
     None),
    ('GNRC analysis_financial.json sections.profitability',
     'ailing four quarters to the end of June 2026, gross margin is  , operating margi',
     'year',
     None),
    ('GNRC analysis_financial.json sections.efficiency',
     'lowest, after an inventory build in the 2025 cash flow and a larger inventory va',
     'year',
     '"the" is no year context'),
    ('GNRC analysis_financial.json sections.liquidity',
     'he legal settlement accrued at year-end 2025 was paid, which took other accrued ',
     'year',
     None),
    ('GNRC analysis_financial.json sections.solvency',
     'ility Python carries is  , the year-end 2025 balance, because the June filing do',
     'year',
     '"balance" is a noun after the year, which can open a counted noun phrase'),
    ('GNRC analysis_financial.json sections.growth',
     'wn (  and  ) because the second half of 2025 carried heavy legal charges. Operat',
     'year',
     None),
    ('GNRC analysis_financial.json sections.free_cash_flow',
     'ing window nets a settlement accrued in 2025 and paid in 2026 against tariff-ref',
     'year',
     None),
    ('GNRC analysis_financial.json path_to_distress',
     'ling level: a repeat of the second-half-2025 legal charges, the loss of the tari',
     'year',
     '"legal" is an adjective after the year, which can open a counted noun phrase'),
    ('GNRC analysis_financial.json anomalies[3]',
     'ar average of   only because the strong 2026 half offsets the 2025 second half, ',
     'year',
     '"the strong" is no year context, nor "the" before the second year'),
    ('GNRC analysis_financial.json anomalies[9]',
     'he legal settlement accrued at year-end 2025 was paid in the half, which is why ',
     'year',
     None),
    ('GNRC assumptions.json scenarios.bear',
     'ry charges that made the second half of 2025 loss-making recur in some form, and',
     'year',
     None),
    ('GNRC assumptions.json scenarios.base',
     ' twelve months blend the second half of 2026, for which the unchanged full-year ',
     'year',
     None),
    ('GNRC assumptions.json scenarios.bull',
     'th; the committed hyperscale volume for 2027, a data-center backlog that has gro',
     'year',
     None),
    ('LFUS analysis_accounting.json areas.revenue_recognition',
     ' its high point in the third quarter of 2025; receivables of   grew with revenue',
     'year',
     None),
    ('LFUS analysis_accounting.json areas.estimates_and_reserves',
     'd   at its high in the third quarter of 2025; the reserve balance of   fell whil',
     'year',
     None),
    ('LFUS analysis_accounting.json areas.cross_document_reconciliation',
     'to have moved from the third quarter of 2026 to the first quarter of 2027.',
     'year',
     None),
    ('LFUS analysis_accounting.json areas.industry_lens',
     'ile finished goods fell ("raw materials 198883000 against 186662000, work in pro',
     'number',
     None),
    ('LFUS analysis_accounting.json reconciliation[8]',
     ' period moved from the third quarter of 2026 to the first quarter of 2027, the c',
     'year',
     None),
    ('LFUS analysis_accounting.json anomalies[1]',
     '-price allocation brought in "inventory 20703000, receivables 14739000" and curr',
     'number',
     None),
    ('LFUS analysis_accounting.json anomalies[4]',
     'rly accrual ratio, the first quarter of 2026, is  , the highest of the two fille',
     'year',
     None),
    ('LFUS analysis_accounting.json anomalies[12]',
     'ttlement charge in the first quarter of 2027 estimated between $6 million and $8',
     'number',
     None),
    ('LFUS analysis_accounting.json anomalies[13]',
     't "Current employee-related liabilities 107717000 at   against 114662000 at  ." ',
     'number',
     None),
    ('LFUS analysis_accounting.json anomalies[35]',
     'The release states "2026 included the reversal of an indemnification receivable ',
     'year',
     'a year that opens a quotation has no word before it'),
    ('LFUS analysis_financial.json sections.liquidity',
     'ility was upsized and extended in March 2026. Financing in the six months was ne',
     'year',
     None),
    ('LFUS analysis_financial.json sections.solvency',
     " that is the balance at fiscal year-end 2025, the newest filed; the quarter's ba",
     'year',
     None),
    ('LFUS analysis_financial.json dupont',
     'rating margin collapsing from the   and 2023 levels to a fraction of the three-y',
     'year',
     'a list member with no year context of its own, and "levels" after it'),
    ('LFUS analysis_financial.json anomalies[1]',
     'ating margin at a fraction of the   and 2023 levels because of an unallocated co',
     'year',
     'a list member with no year context of its own, and "levels" after it'),
    ('LFUS analysis_financial.json anomalies[12]',
     'ent was amended in the first quarter of 2026 so that restructuring and business-',
     'year',
     None),
    ('LFUS assumptions.json scenarios.bear',
     'ide and Basler carry the second half of 2026, but the first half of 2027 turns d',
     'year',
     None),
    ('LFUS assumptions.json scenarios.base',
     'ler acquisition, which laps in December 2026, and the third-quarter guide of rou',
     'year',
     None),
    ('LFUS assumptions.json scenarios.bull',
     "ustrial organic growth persists through 2027, and that Basler's grid and power-g",
     'year',
     None),
    ('PANW analysis_accounting.json areas.cash_flow_engineering_and_off_balance_sheet',
     'he headquarters leases were extended to 2040 and right-of-use assets and noncurr',
     'year',
     '"to" is no year context: "leases to 2040" is a count'),
    ('PANW analysis_accounting.json anomalies[28]',
     'The   index lists an April 2026 filing reporting a material definitive agreement',
     'year',
     None),
    ('PANW analysis_financial.json sections.liquidity',
     'tible notes were settled in cash in May 2026, Portkey closed in May 2026 for cas',
     'year',
     None),
    ('PANW analysis_financial.json sections.solvency',
     'e CyberArk convertible senior notes due 2030 assumed in the quarter and carried ',
     'year',
     None),
    ('PANW analysis_financial.json anomalies[0]',
     'The quarter ended April 2026 printed an operating loss and a net loss against pr',
     'year',
     None),
    ('PANW analysis_financial.json anomalies[10]',
     'ised the buyback authorization in March 2026.',
     'year',
     None),
    ('PANW analysis_financial.json anomalies[11]',
     'onvertible notes settled in cash in May 2026; the Portkey acquisition completed ',
     'year',
     None),
    ('PANW analysis_financial.json anomalies[15]',
     'e CyberArk convertible senior notes due 2030 assumed in the quarter, carried at ',
     'year',
     None),
    ('PANW analysis_financial.json anomalies[17]',
     'ar-end, after three amendments in April 2026 extended the Santa Clara headquarte',
     'year',
     None),
    ('PANW analysis_financial.json anomalies[18]',
     'otes-text report finds an   dated April 2026 listing a material definitive agree',
     'year',
     '"listing" after the year can open a noun phrase ("listing fees")'),
    ('STX analysis_financial.json sections.solvency',
     'ssuance ( ); the exchangeable notes due 2028 were largely retired for cash and o',
     'year',
     None),
    ('STX analysis_financial.json path_to_distress',
     'every quarter and steps down after July 2027; the covenant is on net leverage, w',
     'year',
     None),
    ('STX analysis_financial.json anomalies[2]',
     'eps down for quarters ending after July 2027. The company states compliance and ',
     'year',
     None),
    ('STX analysis_financial.json anomalies[3]',
     'exchanges of the exchangeable notes due 2028, recognized under a newly adopted s',
     'year',
     None),
)
PUBLISHED_ITEMS = (
    # ticker · accession · file · item · the hand reading of its whole text · why the rule
    # disagrees, or None
    ('AAPL',
     '0000320193-26-000020',
     'assumptions.json',
     'scenarios.base',
     'year',
     None),
    ('AAPL',
     '0000320193-26-000020',
     'assumptions.json',
     'scenarios.bull',
     'year',
     None),
    ('CARR',
     '0001783180-26-000032',
     'analysis_accounting.json',
     'areas.earnings_versus_cash',
     'year',
     'a parenthesised number has no year context: "(2025)" is a count'),
    ('CARR',
     '0001783180-26-000032',
     'analysis_accounting.json',
     'areas.revenue_recognition',
     'year',
     None),
    ('CARR',
     '0001783180-26-000032',
     'analysis_accounting.json',
     'areas.estimates_and_reserves',
     'year',
     None),
    ('CARR',
     '0001783180-26-000032',
     'analysis_accounting.json',
     'areas.cost_deferral',
     'year',
     None),
    ('CARR',
     '0001783180-26-000032',
     'analysis_accounting.json',
     'areas.controls_audit_and_filing_signals',
     'year',
     '"the" is no year context'),
    ('CARR',
     '0001783180-26-000032',
     'analysis_accounting.json',
     'areas.industry_lens',
     'year',
     '"the" is no year context'),
    ('CARR',
     '0001783180-26-000032',
     'analysis_accounting.json',
     'anomalies[6]',
     'year',
     '"of" alone is no year context: "inventory of 2048" is a count'),
    ('CARR',
     '0001783180-26-000032',
     'analysis_accounting.json',
     'anomalies[24]',
     'year',
     None),
    ('CARR',
     '0001783180-26-000032',
     'analysis_accounting.json',
     'anomalies[25]',
     'year',
     None),
    ('CARR',
     '0001783180-26-000032',
     'analysis_accounting.json',
     'anomalies[37]',
     'year',
     None),
    ('CARR',
     '0001783180-26-000032',
     'analysis_accounting.json',
     'anomalies[40]',
     'year',
     '"the" is no year context'),
    ('CARR',
     '0001783180-26-000032',
     'analysis_financial.json',
     'sections.profitability',
     'year',
     None),
    ('CARR',
     '0001783180-26-000032',
     'analysis_financial.json',
     'sections.efficiency',
     'year',
     None),
    ('CARR',
     '0001783180-26-000032',
     'analysis_financial.json',
     'sections.solvency',
     'year',
     '"between" is no year context'),
    ('CARR',
     '0001783180-26-000032',
     'analysis_financial.json',
     'sections.growth',
     'year',
     None),
    ('CARR',
     '0001783180-26-000032',
     'analysis_financial.json',
     'dupont',
     'year',
     None),
    ('CARR',
     '0001783180-26-000032',
     'analysis_financial.json',
     'path_to_distress',
     'year',
     None),
    ('CARR',
     '0001783180-26-000032',
     'analysis_financial.json',
     'anomalies[4]',
     'year',
     None),
    ('CARR',
     '0001783180-26-000032',
     'analysis_financial.json',
     'anomalies[5]',
     'year',
     None),
    ('CARR',
     '0001783180-26-000032',
     'analysis_financial.json',
     'anomalies[9]',
     'year',
     None),
    ('CARR',
     '0001783180-26-000032',
     'analysis_financial.json',
     'anomalies[11]',
     'year',
     None),
    ('CARR',
     '0001783180-26-000032',
     'analysis_financial.json',
     'anomalies[14]',
     'year',
     None),
    ('CARR',
     '0001783180-26-000032',
     'analysis_financial.json',
     'anomalies[15]',
     'year',
     None),
    ('CARR',
     '0001783180-26-000032',
     'analysis_financial.json',
     'anomalies[17]',
     'year',
     None),
    ('CARR',
     '0001783180-26-000032',
     'analysis_financial.json',
     'anomalies[18]',
     'year',
     '"between" is no year context'),
    ('CARR',
     '0001783180-26-000032',
     'analysis_financial.json',
     'anomalies[19]',
     'year',
     None),
    ('CIEN',
     '0001628280-26-040767',
     'analysis_financial.json',
     'anomalies[7]',
     'year',
     None),
    ('CIEN',
     '0001628280-26-040767',
     'analysis_financial.json',
     'summary_ko.solvency',
     'year',
     None),
    ('CIEN',
     '0001628280-26-040767',
     'analysis_financial.json',
     'summary_ko.path_to_distress',
     'year',
     None),
    ('CSCO',
     '0000858877-26-000078',
     'analysis_accounting.json',
     'areas.controls_audit_and_filing_signals',
     'year',
     None),
    ('CSCO',
     '0000858877-26-000078',
     'analysis_accounting.json',
     'anomalies[21]',
     'year',
     None),
    ('CSCO',
     '0000858877-26-000078',
     'analysis_accounting.json',
     'anomalies[22]',
     'year',
     None),
    ('GNRC',
     '0001437749-26-025669',
     'analysis_accounting.json',
     'areas.earnings_versus_cash',
     'year',
     None),
    ('GNRC',
     '0001437749-26-025669',
     'analysis_accounting.json',
     'areas.revenue_recognition',
     'year',
     None),
    ('GNRC',
     '0001437749-26-025669',
     'analysis_accounting.json',
     'areas.estimates_and_reserves',
     'year',
     '"a" is no year context'),
    ('GNRC',
     '0001437749-26-025669',
     'analysis_accounting.json',
     'areas.industry_lens',
     'year',
     '"a" is no year context'),
    ('GNRC',
     '0001437749-26-025669',
     'analysis_accounting.json',
     'anomalies[5]',
     'year',
     None),
    ('GNRC',
     '0001437749-26-025669',
     'analysis_accounting.json',
     'anomalies[7]',
     'year',
     '"of" alone is no year context: "inventory of 2048" is a count'),
    ('GNRC',
     '0001437749-26-025669',
     'analysis_accounting.json',
     'anomalies[10]',
     'year',
     None),
    ('GNRC',
     '0001437749-26-025669',
     'analysis_accounting.json',
     'anomalies[12]',
     'year',
     '"a" is no year context'),
    ('GNRC',
     '0001437749-26-025669',
     'analysis_accounting.json',
     'anomalies[17]',
     'year',
     'the window cuts "no 2026" to "no 20", and "no" is no year context'),
    ('GNRC',
     '0001437749-26-025669',
     'analysis_accounting.json',
     'anomalies[23]',
     'year',
     '"committed" is no year context'),
    ('GNRC',
     '0001437749-26-025669',
     'analysis_accounting.json',
     'anomalies[34]',
     'year',
     '"no" is no year context'),
    ('GNRC',
     '0001437749-26-025669',
     'analysis_accounting.json',
     'anomalies[35]',
     'year',
     '"of" alone is no year context: "inventory of 2048" is a count'),
    ('GNRC',
     '0001437749-26-025669',
     'analysis_financial.json',
     'sections.profitability',
     'year',
     None),
    ('GNRC',
     '0001437749-26-025669',
     'analysis_financial.json',
     'sections.efficiency',
     'year',
     '"the" is no year context'),
    ('GNRC',
     '0001437749-26-025669',
     'analysis_financial.json',
     'sections.liquidity',
     'year',
     None),
    ('GNRC',
     '0001437749-26-025669',
     'analysis_financial.json',
     'sections.solvency',
     'year',
     '"balance" is a noun after the year, which can open a counted noun phrase'),
    ('GNRC',
     '0001437749-26-025669',
     'analysis_financial.json',
     'sections.growth',
     'year',
     None),
    ('GNRC',
     '0001437749-26-025669',
     'analysis_financial.json',
     'sections.free_cash_flow',
     'year',
     None),
    ('GNRC',
     '0001437749-26-025669',
     'analysis_financial.json',
     'path_to_distress',
     'year',
     '"legal" is an adjective after the year, which can open a counted noun phrase'),
    ('GNRC',
     '0001437749-26-025669',
     'analysis_financial.json',
     'anomalies[3]',
     'year',
     '"the strong" is no year context, nor "the" before the second year'),
    ('GNRC',
     '0001437749-26-025669',
     'analysis_financial.json',
     'anomalies[5]',
     'year',
     '"the" is no year context'),
    ('GNRC',
     '0001437749-26-025669',
     'analysis_financial.json',
     'anomalies[9]',
     'year',
     None),
    ('GNRC',
     '0001437749-26-025669',
     'assumptions.json',
     'scenarios.bear',
     'year',
     None),
    ('GNRC',
     '0001437749-26-025669',
     'assumptions.json',
     'scenarios.base',
     'year',
     None),
    ('GNRC',
     '0001437749-26-025669',
     'assumptions.json',
     'scenarios.bull',
     'year',
     None),
    ('LFUS',
     '0001628280-26-050481',
     'analysis_accounting.json',
     'areas.revenue_recognition',
     'number',
     None),
    ('LFUS',
     '0001628280-26-050481',
     'analysis_accounting.json',
     'areas.estimates_and_reserves',
     'number',
     None),
    ('LFUS',
     '0001628280-26-050481',
     'analysis_accounting.json',
     'areas.cross_document_reconciliation',
     'year',
     None),
    ('LFUS',
     '0001628280-26-050481',
     'analysis_accounting.json',
     'areas.industry_lens',
     'number',
     None),
    ('LFUS',
     '0001628280-26-050481',
     'analysis_accounting.json',
     'reconciliation[8]',
     'year',
     None),
    ('LFUS',
     '0001628280-26-050481',
     'analysis_accounting.json',
     'anomalies[1]',
     'number',
     None),
    ('LFUS',
     '0001628280-26-050481',
     'analysis_accounting.json',
     'anomalies[4]',
     'year',
     None),
    ('LFUS',
     '0001628280-26-050481',
     'analysis_accounting.json',
     'anomalies[12]',
     'number',
     None),
    ('LFUS',
     '0001628280-26-050481',
     'analysis_accounting.json',
     'anomalies[13]',
     'number',
     None),
    ('LFUS',
     '0001628280-26-050481',
     'analysis_accounting.json',
     'anomalies[35]',
     'year',
     'a year that opens a quotation has no word before it'),
    ('LFUS',
     '0001628280-26-050481',
     'analysis_financial.json',
     'sections.liquidity',
     'year',
     None),
    ('LFUS',
     '0001628280-26-050481',
     'analysis_financial.json',
     'sections.solvency',
     'year',
     '"to" is no year context: "leases to 2040" is a count'),
    ('LFUS',
     '0001628280-26-050481',
     'analysis_financial.json',
     'dupont',
     'year',
     'a list member with no year context of its own, and "levels" after it'),
    ('LFUS',
     '0001628280-26-050481',
     'analysis_financial.json',
     'anomalies[1]',
     'year',
     'a list member with no year context of its own, and "levels" after it'),
    ('LFUS',
     '0001628280-26-050481',
     'analysis_financial.json',
     'anomalies[12]',
     'year',
     None),
    ('LFUS',
     '0001628280-26-050481',
     'assumptions.json',
     'scenarios.bear',
     'year',
     None),
    ('LFUS',
     '0001628280-26-050481',
     'assumptions.json',
     'scenarios.base',
     'year',
     None),
    ('LFUS',
     '0001628280-26-050481',
     'assumptions.json',
     'scenarios.bull',
     'year',
     None),
    ('PANW',
     '0001327567-26-000015',
     'analysis_accounting.json',
     'areas.cash_flow_engineering_and_off_balance_sheet',
     'year',
     '"to" is no year context: "leases to 2040" is a count'),
    ('PANW',
     '0001327567-26-000015',
     'analysis_accounting.json',
     'anomalies[28]',
     'year',
     None),
    ('PANW',
     '0001327567-26-000015',
     'analysis_financial.json',
     'sections.liquidity',
     'year',
     None),
    ('PANW',
     '0001327567-26-000015',
     'analysis_financial.json',
     'sections.solvency',
     'year',
     '"to" is no year context: "leases to 2040" is a count'),
    ('PANW',
     '0001327567-26-000015',
     'analysis_financial.json',
     'anomalies[0]',
     'year',
     None),
    ('PANW',
     '0001327567-26-000015',
     'analysis_financial.json',
     'anomalies[10]',
     'year',
     None),
    ('PANW',
     '0001327567-26-000015',
     'analysis_financial.json',
     'anomalies[11]',
     'year',
     None),
    ('PANW',
     '0001327567-26-000015',
     'analysis_financial.json',
     'anomalies[15]',
     'year',
     None),
    ('PANW',
     '0001327567-26-000015',
     'analysis_financial.json',
     'anomalies[17]',
     'year',
     '"to" is no year context: "leases to 2040" is a count'),
    ('PANW',
     '0001327567-26-000015',
     'analysis_financial.json',
     'anomalies[18]',
     'year',
     '"listing" after the year can open a noun phrase ("listing fees")'),
    ('STX',
     '0001137789-26-000159',
     'analysis_financial.json',
     'sections.solvency',
     'year',
     None),
    ('STX',
     '0001137789-26-000159',
     'analysis_financial.json',
     'path_to_distress',
     'year',
     None),
    ('STX',
     '0001137789-26-000159',
     'analysis_financial.json',
     'anomalies[2]',
     'year',
     None),
    ('STX',
     '0001137789-26-000159',
     'analysis_financial.json',
     'anomalies[3]',
     'year',
     None),
)


def _param(row, text_at):
    reading, reason = row[-2], row[-1]
    marks = () if reason is None else (pytest.mark.xfail(strict=True, reason=reason),)
    return pytest.param(row, id=" ".join(str(x) for x in row[:text_at]), marks=marks)


@pytest.mark.parametrize("row", [_param(row, 1) for row in PUBLISHED_WINDOWS])
def test_the_rule_reads_each_published_window_as_the_hand_did(row):
    label, text, reading, _ = row
    payload = accounting()
    payload["anomalies"][0]["what"] = text
    out = analysis_check.check("accounting", payload, fields=FIELDS, sources=SOURCES)
    dropped_for_a_digit = any("a number written in the analyst's own words" in d["reason"]
                              for d in out["dropped_items"])
    assert dropped_for_a_digit == (reading == "number"), (label, text)


def gate_whole(ticker: str, accession: str, written: str) -> dict:
    """The real gate on the analyst's written file, with the calculator and the sources
    that analyst saw, as `src/analysis_check.py`'s command line runs it."""
    agent, kind = {"analysis_accounting.json": ("accounting-analyst", "accounting"),
                   "analysis_financial.json": ("financial-analyst", "financial"),
                   "assumptions.json": ("valuation-analyst", "assumptions")}[written]
    agent_dir = RUNS / ticker / accession / "agents" / agent
    payload = json.loads((agent_dir / written).read_text(encoding="utf-8"))
    calculator = next(agent_dir / name for name in ("calculator_filings_only.json",
                                                      "calculator_before_drivers.json")
                      if (agent_dir / name).is_file())
    fields = json.loads(calculator.read_text(encoding="utf-8"))
    sources = analysis_check.read_sources(agent_dir, analysis_check.SOURCES[kind])
    if kind == "assumptions":
        return analysis_check.check_assumptions(payload, fields=fields, sources=sources)
    return analysis_check.check(kind, payload, fields=fields, sources=sources)


@pytest.mark.parametrize("row", [_param(row, 4) for row in PUBLISHED_ITEMS])
def test_the_rule_reads_each_published_item_whole_as_the_hand_did(row):
    ticker, accession, written, where, reading, _ = row
    out = gate_whole(ticker, accession, written)
    dropped = {d["where"]: d["reason"] for d in out["dropped_items"]}
    if reading == "number":
        assert where in dropped and "a number written in the analyst's own words" in dropped[where]
    else:
        assert where not in dropped, dropped.get(where)


PUBLISHED_SCENARIOS = (
    pytest.param("AAPL", "0000320193-26-000020", id="AAPL"),
    pytest.param("GNRC", "0001437749-26-025669", id="GNRC"),
    pytest.param("LFUS", "0001628280-26-050481", id="LFUS"),
)


@pytest.mark.parametrize("ticker, accession", PUBLISHED_SCENARIOS)
def test_the_published_scenarios_of_the_valuation_analyst_pass_the_gate_whole(ticker,
                                                                             accession):
    """The gate comparison of queue item one, on the published run itself: the
    valuation analyst's scenarios as written (`agents/valuation-analyst/assumptions.json`),
    gated against the calculator and the sources that analyst saw, drop nothing. LFUS's
    three passed first; AAPL's two and GNRC's three pass since the rule read "fiscal 2022
    to 2025", "the only fiscal year ... was 2021 at", "the second half of 2025 loss-making
    recur", "the margin of 2023", "the growth of 2021 and 2022", "the 2022 peak", "the
    first half of 2026 once" and "the first half of 2026 earned" as the hand did."""
    agent_dir = RUNS / ticker / accession / "agents" / "valuation-analyst"
    payload = json.loads((agent_dir / "assumptions.json").read_text(encoding="utf-8"))
    fields = json.loads((agent_dir / "calculator_before_drivers.json").read_text(
        encoding="utf-8"))
    sources = analysis_check.read_sources(agent_dir, analysis_check.SOURCES["assumptions"])
    out = analysis_check.check_assumptions(payload, fields=fields, sources=sources)
    assert out["dropped_items"] == [], out["dropped_items"]
    assert set(out["scenarios"]) == {"bear", "base", "bull"}


def test_a_number_that_looks_like_a_year_is_still_a_number():
    for text in ("revenue of $2026 thousand", "a ratio of 2026.5", "2030 employees",
                 "2026 million of backlog", "1,995 units", "a 2049 percent rise"):
        payload = accounting()
        payload["anomalies"][0]["what"] = text
        assert analysis_check.check("accounting", payload, fields=FIELDS,
                                    sources=SOURCES)["anomalies"] == [], text


def test_a_quantity_with_no_unit_word_is_still_a_number():
    """The second lens's finding of 2026-10-06: none of these carries a unit word on
    any list, and none has a year-context word around it, so each is a number the
    analyst wrote. "inventory of 2048" is the case the comment in
    `src/analysis_check.py` has always named."""
    for text in ("inventory of 2048", "backlog rose to 2030 orders", "2026 stores", "€2026",
                 "USD 2026", "2026 Million", "2026 bn", "-2026", "margin 2026",
                 "from 2026 onward", "leases to 2040", "2021 and 2022 units", "(2025)",
                 "due 2030 shares",
                 # the second lens's third reading: a bare noun after the year, "by" with
                 # an amount, and a range or list with no context word of its own
                 "cut headcount by 2030", "grew by 2026", "a rise in 2030 orders",
                 "backlog grew by 2030 orders", "up by 1999", "in 2030 and 2031 orders",
                 # the fourth reading: "by" is no context at all, and no noun or adjective
                 # after the year is a terminator
                 "cut headcount by 2030.", "reduced inventory by 2048,", "by 2030.",
                 "sold in 2048 high-margin units", "in 2030 low-cost stores",
                 "an increase in 2048 of its stores",
                 "inventory of 2021 and 2022", "2024–2026",
                 # the fourth reading: "for" and "in" need a terminator, "by" is out
                 # whatever the value, and "half of" with no ordinal is a share of a count
                 "for 2027 stores", "in 2050 stores", "by 2050", "by 2050.",
                 "half of 2048 stores",
                 # the fifth reading: a period phrase takes the terminator like every
                 # other context, and a word that merely starts like a month's short
                 # form is no year-context-after word
                 "the second half of 2048 stores", "the close of 2048 stores",
                 "due 2030 vendors", "the second half of 2025 and 2048 stores",
                 "inventory of 2048 declined", "2048 marketing staff", "2030 novel products",
                 "2048 octane", "2048 junior engineers", "2030 mayors",
                 # the sixth reading: a month after a year is a month only capitalised
                 "inventory of 2048 may fall", "a backlog of 2030 may shrink",
                 "headcount of 2026 may decline", "2048 march",
                 # counts to the rule as written -- a noun or an adjective, not
                 # hyphenated, after the year -- though the published analysts meant
                 # years; PUBLISHED_WINDOWS marks those rows xfail with this reason
                 "the year-end 2025 balance", "second-half-2025 legal",
                 "dated April 2026 listing"):
        payload = accounting()
        payload["anomalies"][0]["what"] = text
        out = analysis_check.check("accounting", payload, fields=FIELDS, sources=SOURCES)
        assert out["anomalies"] == [], text
        assert "a number written in the analyst's own words" in json.dumps(
            out["dropped_items"], ensure_ascii=False), text


def test_a_quantity_after_a_year_word_or_a_notes_word_is_still_a_number():
    for text in ("grew by 1950 basis points", "sold in 2048 units", "senior notes 25 million",
                 "non-recurring items 12 percent",
                 # a quantity word vetoes a period phrase too
                 "for 2027 units", "the second half of 2048 units", "due 2030 shares",
                 "2026 augmented units"):
        payload = accounting()
        payload["anomalies"][0]["what"] = text
        assert analysis_check.check("accounting", payload, fields=FIELDS,
                                    sources=SOURCES)["anomalies"] == [], text


def test_each_named_year_context_reads_its_year_and_drops_the_count_beside_it():
    """Queue item one's last reading, two-sided for each word the rule learnt: the
    published phrase (GNRC's and AAPL's valuation analysts of 2026-09-29, their
    `assumptions.json`) or one in its shape stands, and the count written with the
    same word is dropped."""
    def gated(text):
        payload = accounting()
        payload["anomalies"][0]["what"] = text
        return analysis_check.check("accounting", payload, fields=FIELDS, sources=SOURCES)
    for year, count in (
            # "margin of", "margins of", "growth of", "surge of", and the elided "and of"
            ("below the margin of 2023;", "inventory of 2048"),
            ("the margins of 2021, 2022 and the year before last", "revenue of 2048"),
            ("below the growth of 2021 and 2022, which came", "the margin of 2048 units"),
            ("the pandemic-era surge of 2021, so even", "the margins of 2048 stores"),
            ("the margin of the year before last and of 2022, both years",
             "inventory of 2021 and 2022"),
            # a range opening with a fiscal year
            ("the flat stretch of fiscal 2022 to 2025, on the view", "fiscal 2022 to 2048 units"),
            ("the flat stretch of fiscal 2022 to 2025 to have been", "leases to 2040"),
            ("fiscal 2022 to 2025", "rose to 2030 orders"),
            # "was" after a subject that is a year
            ("the only fiscal year in the record that grew faster was 2021 at",
             "the headcount was 2048"),
            ("the year that grew faster was 2021.", "the year-end headcount was 2048"),
            ("the fiscal year that grew faster was 2021", "the headcount for the year was 2048 units"),
            # a hyphenated adjective, then a word that cannot be the noun it modifies
            ("the second half of 2025 loss-making recur in some form",
             "sold in 2048 high-margin units"),
            ("the second half of 2025 loss-making.", "in 2030 low-cost stores"),
            ("at the June 2026 balance-sheet date", "in 2048 high-margin and low-cost units"),
            ("the second half of 2025 loss-making", "in 2048 high-margin, low-volume units"),
            # "peak" after a year, "once" and "earned" after a year
            ("that window starts at the 2022 peak;", "the peak of 2048"),
            ("above the first half of 2026 once the refund is removed",
             "the first half of 2048 once-off units"),
            ("the level the first half of 2026 earned once the refund is taken out",
             "the second half of 2048 stores earned")):
        assert gated(year)["dropped_count"] == 0, year
        out = gated(count)
        assert out["anomalies"] == [], count
        assert "a number written in the analyst's own words" in json.dumps(
            out["dropped_items"], ensure_ascii=False), count


def test_innocent_korean_words_are_not_the_ruled_out_ones():
    payload = accounting()
    payload["anomalies"][0]["what"] = "사기업 고객과 검사기 재고, 자사주 매수, 매도가능증권"
    assert analysis_check.check("accounting", payload, fields=FIELDS,
                                sources=SOURCES)["dropped_count"] == 0


def test_an_adjustment_amount_is_a_dollar_cell_and_nothing_else():
    payload = accounting()
    payload["adjustments"][0]["calculator_field"] = "ratios.efficiency.days_sales_outstanding"
    assert analysis_check.check("accounting", payload, fields=FIELDS,
                                sources=SOURCES)["adjustments"] == []


def test_a_quarter_of_a_year_stands_and_a_labelled_quantity_does_not():
    payload = accounting()
    payload["anomalies"][0]["what"] = "Q4 2026 guidance, Q2 of fiscal 2027"
    assert analysis_check.check("accounting", payload, fields=FIELDS,
                                sources=SOURCES)["dropped_count"] == 0
    for text in ("Note 12 million", "Item 12 million", "ASC 606 million"):
        payload["anomalies"][0]["what"] = text
        assert analysis_check.check("accounting", payload, fields=FIELDS,
                                    sources=SOURCES)["anomalies"] == [], text
