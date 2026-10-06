"""The owner's graders, two-sided: each fires on a planted fault and passes the clean run.

The clean run is a copy of CSCO's published run (#103). Each test plants one fault in
a fresh copy and expects exactly the grader that owns it to fail; the untouched copy
passes every grader. The DCF case is the hand-worked one in tests/test_calculator.py.
"""

from __future__ import annotations

import datetime
import json
import shutil
from pathlib import Path

import pytest

from evals.capability import golden
from evals.common import FAIL, PASS
from evals.golden_format import GoldenFormatError, loads
from evals.regression import coverage, mechanical

REPO = Path(__file__).resolve().parent.parent
CLEAN = REPO / "runs" / "CSCO" / "0000858877-26-000078"
# Read off the published run by hand: the accounting anomaly
# earnings_versus_cash_operating_cash_flow_falls_while_net_income_rises cites the
# reader item liquidity_and_capital_operating_cash_flow_nine_months, whose
# paragraph_id in report_numbers.md is the nine-month operating cash flow fact.
NINE_MONTH_CASH_FLOW = ("0000858877-26-000078:facts:NetCashProvidedByUsedInOperatingActivities:"
                        "2025-07-27..2026-04-25")


@pytest.fixture
def run(tmp_path):
    target = tmp_path / "CSCO" / CLEAN.name
    shutil.copytree(CLEAN, target, ignore=shutil.ignore_patterns("control-single-agent-analyses"))
    return target


def _edit(path: Path, change):
    data = json.loads(path.read_text(encoding="utf-8"))
    change(data)
    path.write_text(json.dumps(data), encoding="utf-8")


def _status(results, grader):
    return next(r.status for r in results if r.grader == grader)


def test_the_clean_run_passes_every_grader(run):
    results = mechanical.grade(run) + coverage.grade(run)
    assert [r.grader for r in results if r.status != PASS] == []


def test_the_graders_read_their_own_floors_and_cases_never_the_branchs(tmp_path, monkeypatch):
    """In CI the graders are main's copy and the tree is the branch's: the floors
    and the approved cases come from the copy that is running."""
    import evals.common as common
    assert runner.THRESHOLDS == common.EVALS / "thresholds.json"
    assert golden.CASES == common.EVALS / "golden" / "cases"
    assert common.EVALS == Path(mechanical.__file__).resolve().parent.parent
    assert not str(runner.THRESHOLDS).startswith(str(tmp_path))


def test_the_hand_worked_cases_reproduce():
    assert all(r.status == PASS for r in mechanical.check_hand_worked_cases())


def test_the_calculator_under_judgment_runs_in_its_own_process(tmp_path):
    """A src/ that rebinds the graders when imported would, run in-process, weaken
    the checks before any run was graded; in its own process it cannot reach them,
    and a calculator that gives the wrong number, or none, fails the case."""
    import textwrap
    tree = tmp_path / "branch"
    (tree / "src").mkdir(parents=True)
    (tree / "src" / "__init__.py").write_text(textwrap.dedent("""
        try:
            import evals.regression.mechanical as m
            m.RUN_CHECKS = ()
        except ImportError:
            pass      # in its own process the graders are out of reach
        """))
    (tree / "src" / "calculator.py").write_text(textwrap.dedent("""
        def forecast(fcf, drivers, tax, rate):
            return {"enterprise_value": 1.0}
        def bridge(ev, cash, debt, shares):
            return {"value_per_share": 1.0}
        """))
    before = mechanical.RUN_CHECKS
    results = mechanical.check_hand_worked_cases(tree)
    assert mechanical.RUN_CHECKS is before and before
    assert all(r.status == FAIL for r in results)
    assert any("src.calculator gives 1.0" in r.detail for r in results)
    (tree / "src" / "calculator.py").write_text("raise RuntimeError('no calculator here')\n")
    results = mechanical.check_hand_worked_cases(tree)
    assert all(r.status == FAIL and "exited" in r.detail for r in results)
    gordon = mechanical.forecast(1000.0, mechanical.GORDON, 0.25, 0.09)
    assert gordon["enterprise_value"] == pytest.approx(1545.0)       # 92.7 / 0.06
    fade = mechanical.forecast(1000.0, mechanical.FADE, 0.25, 0.09)
    assert fade["enterprise_value"] == pytest.approx(2240.8020, abs=1e-4)


def test_an_altered_quote_fails_quotes_resolve(run):
    _edit(run / "analysis_valuation.json",
          lambda d: d["most_sensitive"][0].update(quote="a sentence no filing printed"))
    assert _status(mechanical.grade(run), "mechanical.quotes_resolve") == FAIL


def test_a_reader_quote_attached_to_the_wrong_paragraph_fails_quotes_resolve(run):
    """The quote still exists in the input, under another id; the check holds it
    to the paragraph the item names."""
    report = run / "report_numbers.md"
    text = report.read_text(encoding="utf-8")
    assert NINE_MONTH_CASH_FLOW in text
    report.write_text(text.replace(NINE_MONTH_CASH_FLOW,
                                   "0000858877-26-000078:facts:EntityPublicFloat:2025-01-24", 1),
                      encoding="utf-8")
    result = _status(mechanical.grade(run), "mechanical.quotes_resolve")
    assert result == FAIL


def test_a_run_with_no_record_of_what_an_agent_saw_fails_quotes_resolve(run):
    shutil.rmtree(run / "agents" / "numbers-reader")
    assert _status(mechanical.grade(run), "mechanical.quotes_resolve") == FAIL


def test_a_source_read_past_the_cutoff_fails_nothing_after_cutoff(run):
    def late(d):
        for doc in d["documents"]:
            if doc.get("rows_used_through"):
                doc["rows_used_through"] = "2099-01-01"
    _edit(run / "input_manifest.json", late)
    assert _status(mechanical.grade(run), "mechanical.nothing_after_cutoff") == FAIL


def test_a_price_dated_after_the_cutoff_fails_nothing_after_cutoff(run):
    _edit(run / "calculator.json", lambda d: d["market"]["price"].update(date="2099-01-01"))
    assert _status(mechanical.grade(run), "mechanical.nothing_after_cutoff") == FAIL


def test_a_kept_reader_item_without_a_quote_fails_quotes_resolve(run):
    report = run / "report_numbers.md"
    text = report.read_text(encoding="utf-8")
    report.write_text(text.replace('"quote": "', '"quote": "", "was": "', 1), encoding="utf-8")
    assert _status(mechanical.grade(run), "mechanical.quotes_resolve") == FAIL


def test_a_late_row_in_a_readers_own_input_fails_nothing_after_cutoff(run):
    path = run / "agents" / "numbers-reader" / "input_numbers.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["facts"][0]["filing_date"] = "2099-01-01"
    path.write_text(json.dumps(data), encoding="utf-8")
    assert _status(mechanical.grade(run), "mechanical.nothing_after_cutoff") == FAIL


def test_a_fenced_block_that_is_not_json_fails_quotes_resolve(run):
    report = run / "report_numbers.md"
    report.write_text(report.read_text(encoding="utf-8") + "\n```json\n{not json\n```\n",
                      encoding="utf-8")
    assert _status(mechanical.grade(run), "mechanical.quotes_resolve") == FAIL


def test_a_late_fact_in_the_calculator_copy_an_agent_was_handed_fails_nothing_after_cutoff(run):
    path = run / "agents" / "valuation-analyst" / "calculator_before_drivers.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["market"]["price"]["date"] = "2099-01-01"
    path.write_text(json.dumps(data), encoding="utf-8")
    results = mechanical.grade(run)
    assert _status(results, "mechanical.nothing_after_cutoff") == FAIL
    assert any(d.startswith("agents/valuation-analyst/calculator_before_drivers.json") for d in
               next(r.failures for r in results if r.grader == "mechanical.nothing_after_cutoff"))


def test_a_late_stamp_key_or_dated_row_fails_nothing_after_cutoff(run):
    """A date-time stamp, a date used as a key, and a row dated by `date` or `end`
    are held to the cutoff; a date inside prose is not."""
    _edit(run / "calculator.json", lambda d: d.update(computed_at="2099-01-01T09:00:00+00:00"))
    assert _status(mechanical.grade(run), "mechanical.nothing_after_cutoff") == FAIL


def test_a_late_date_as_a_key_fails_nothing_after_cutoff(run):
    _edit(run / "calculator.json", lambda d: d.update(by_day={"2099-01-01": 1.0}))
    assert _status(mechanical.grade(run), "mechanical.nothing_after_cutoff") == FAIL


def test_a_late_row_dated_by_date_fails_and_a_period_ending_later_does_not(run):
    """`date` says when a row arrived; `end` says what period a fact covers, and a
    10-K filed in February carries facts for the year it is in."""
    path = run / "input_numbers.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["facts"][0]["end"] = "2099-01-01"
    path.write_text(json.dumps(data), encoding="utf-8")
    assert _status(mechanical.grade(run), "mechanical.nothing_after_cutoff") == PASS
    data["facts"][0]["date"] = "2099-01-01"
    path.write_text(json.dumps(data), encoding="utf-8")
    assert _status(mechanical.grade(run), "mechanical.nothing_after_cutoff") == FAIL


def test_a_date_inside_prose_is_not_held_to_the_cutoff(run):
    _edit(run / "calculator.json",
          lambda d: d.update(note="senior notes due 2099-01-01 carry a fixed coupon"))
    assert _status(mechanical.grade(run), "mechanical.nothing_after_cutoff") == PASS


def test_a_late_fact_in_a_calculator_stage_file_fails_nothing_after_cutoff(run):
    path = run / "calculator_filings_only.json"
    text = path.read_text(encoding="utf-8")
    data = json.loads(text)
    data["terms"]["balances_now"]["assets"]["filed"] = "2099-01-01"
    path.write_text(json.dumps(data), encoding="utf-8")
    assert _status(mechanical.grade(run), "mechanical.nothing_after_cutoff") == FAIL


def test_an_evidence_id_no_reader_kept_fails_cited_items_exist(run):
    _edit(run / "analysis_accounting.json",
          lambda d: d["anomalies"][0].update(evidence=["an_item_no_reader_wrote"]))
    assert _status(mechanical.grade(run), "mechanical.cited_items_exist") == FAIL


def test_a_citation_of_null_resolves_to_no_reader_item(run):
    """A reader item with no id is kept by nobody, so an analysis citing null cites
    nothing, even when such an item sits in the report."""
    report = run / "report_numbers.md"
    report.write_text(report.read_text(encoding="utf-8")
                      + '\n```json\n{"what": "an item with no id", "quote": "x"}\n```\n',
                      encoding="utf-8")
    _edit(run / "analysis_accounting.json",
          lambda d: d["anomalies"][0].update(evidence=[None]))
    assert _status(mechanical.grade(run), "mechanical.cited_items_exist") == FAIL


def test_evidence_that_is_not_a_list_fails_cited_items_exist(run):
    _edit(run / "analysis_accounting.json",
          lambda d: d["anomalies"][0].update(evidence=NINE_MONTH_CASH_FLOW))
    assert _status(mechanical.grade(run), "mechanical.cited_items_exist") == FAIL


def test_a_quote_from_a_file_the_analyst_was_not_handed_fails_quotes_resolve(run):
    _edit(run / "analysis_accounting.json", lambda d: d["anomalies"][0].update(
        quote="Revenue", quote_from="input_mdna.md"))        # the accounting analyst sees no filing
    assert _status(mechanical.grade(run), "mechanical.quotes_resolve") == FAIL


def test_a_quote_of_the_rows_unit_or_namespace_alone_fails_quotes_resolve(run):
    report = run / "report_numbers.md"
    text = report.read_text(encoding="utf-8")
    escaped = '\\"value\\": \\"8791000000\\"'
    assert escaped in text
    report.write_text(text.replace(escaped, '\\"prefix\\": \\"us-gaap\\", \\"unit\\": \\"iso4217:USD\\"', 1),
                      encoding="utf-8")
    assert _status(mechanical.grade(run), "mechanical.quotes_resolve") == FAIL


def test_a_quote_of_a_key_name_or_the_id_is_not_a_quote_of_the_row(run):
    """The nine-month cash flow row prints the tag and the key "value"; a quote of
    either carries nothing the filing said."""
    report = run / "report_numbers.md"
    text = report.read_text(encoding="utf-8")
    escaped = '\\"value\\": \\"8791000000\\"'       # as the fenced JSON prints the quote
    assert escaped in text
    report.write_text(text.replace(escaped, '\\"value\\"', 1), encoding="utf-8")
    assert _status(mechanical.grade(run), "mechanical.quotes_resolve") == FAIL
    assert mechanical.says_something('"value": "8791000000"', {"value", "tag"}, "x")
    assert mechanical.says_something('"missing": "no row for inventory_reserve: the', {"missing"}, "x")
    assert not mechanical.says_something('"value"', {"value"}, "x")
    assert not mechanical.says_something('"x", "tag":', {"value", "tag"}, "x")
    # the row's metadata is about the row, not the company; the tag is the filer's
    # own choice of concept, and a tag that changed between years is a finding
    metadata = {'"us-gaap"', '"iso4217:USD"', '"0000858877-26-000078:f-304"'}
    assert not mechanical.says_something('"prefix": "us-gaap", "unit": "iso4217:USD"',
                                         {"prefix", "unit"}, "x", metadata)
    assert not mechanical.says_something('"id": "0000858877-26-000078:f-304"', {"id"}, "x", metadata)
    assert mechanical.says_something('"tag": "NetCashProvidedByUsedInOperatingActivities"',
                                     {"tag", "value"}, "x", metadata)


def test_an_analysis_quote_of_key_names_or_across_report_items_fails_quotes_resolve(run):
    """A report is markdown wrapping JSON: a quote made only of key names and
    punctuation, or one that runs from the end of one item into the next, is a
    substring of the file and a quote of nothing it says."""
    for planted in ('"paragraph_id": "', '"quote": "', '"id": "', '},\n{'):
        _edit(run / "analysis_accounting.json",
              lambda d, p=planted: d["anomalies"][0].update(quote=p, quote_from="report_numbers.md"))
        results = mechanical.grade(run)
        assert _status(results, "mechanical.quotes_resolve") == FAIL, planted
    # the item's own words stand
    item = mechanical.report_items(run / "report_numbers.md")[0]
    _edit(run / "analysis_accounting.json",
          lambda d: d["anomalies"][0].update(quote=item["quote"][:40], quote_from="report_numbers.md"))
    assert _status(mechanical.grade(run), "mechanical.quotes_resolve") == PASS


def test_an_analysis_quote_across_two_paragraphs_of_a_filing_fails_quotes_resolve(run):
    """The valuation analyst quotes MD&A: a quote is of one paragraph, not of the
    text running from the end of one paragraph through the next id line."""
    text = (run / "agents" / "valuation-analyst" / "input_mdna.md").read_text(encoding="utf-8")
    ids = list(mechanical.ID_LINE.finditer(text))
    assert len(ids) > 1
    first, second = ids[0], ids[1]
    across = text[second.start() - 30: second.end() + 30]
    assert "[" in across and "]" in across
    _edit(run / "analysis_valuation.json",
          lambda d: d.setdefault("notes", []).append({"quote": across, "quote_from": "input_mdna.md"}))
    assert _status(mechanical.grade(run), "mechanical.quotes_resolve") == FAIL
    within = text[first.end(): second.start()].strip()[:60]
    _edit(run / "analysis_valuation.json",
          lambda d: d["notes"].__setitem__(-1, {"quote": within, "quote_from": "input_mdna.md"}))
    assert _status(mechanical.grade(run), "mechanical.quotes_resolve") == PASS


def test_a_quote_spanning_two_files_fails_quotes_resolve(run):
    directory = run / "agents" / "accounting-analyst"
    end = (directory / "report_notes_text.md").read_text(encoding="utf-8")[-30:]
    start = (directory / "report_numbers.md").read_text(encoding="utf-8")[:30]
    _edit(run / "analysis_accounting.json",
          lambda d: d["anomalies"][0].update(quote=end + "\n" + start))
    assert _status(mechanical.grade(run), "mechanical.quotes_resolve") == FAIL


def test_a_path_the_calculator_lacks_fails_cited_numbers_exist(run):
    _edit(run / "analysis_accounting.json", lambda d: d["areas"]["cost_deferral"].update(
        finding="Capitalized software is {terms.balances_now.no_such_balance}."))
    assert _status(mechanical.grade(run), "mechanical.cited_numbers_exist") == FAIL


def test_a_price_path_in_the_filings_only_view_fails_cited_numbers_exist(run):
    _edit(run / "analysis_financial.json", lambda d: d["sections"]["growth"].update(
        reading="The price is {cost_of_capital.price_at_cutoff}."))
    assert _status(mechanical.grade(run), "mechanical.cited_numbers_exist") == FAIL


def test_a_document_after_the_cutoff_fails_nothing_after_cutoff(run):
    _edit(run / "input_manifest.json",
          lambda d: d["documents"][0].update(filing_date="2099-01-01"))
    assert _status(mechanical.grade(run), "mechanical.nothing_after_cutoff") == FAIL


# A market table as src/market.py records one, worked by hand for CSCO's filing
# accepted Tuesday 2026-05-19 at 16:35 New York: after the close, so day zero is
# Wednesday the 20th and days one and two the 21st and 22nd; before EDGAR's half
# past five, so the filing date is the 19th, the run's cutoff; the table's cutoff
# is day two, the 22nd.
def _market_table(**changes):
    table = {"cutoff": "2026-05-22",
             "windows": [{"kind": "filing", "filing_date": "2026-05-19",
                          "accepted": "2026-05-19T16:35:00-04:00", "day_zero": "2026-05-20",
                          "days": ["2026-05-20", "2026-05-21", "2026-05-22"]}],
             "rows": [{"date": d} for d in ("2026-05-18", "2026-05-19", "2026-05-20",
                                            "2026-05-21", "2026-05-22")]}
    table.update(changes)
    return table


ACCEPTED = "2026-05-19T16:35:00-04:00"


def _with_acceptance(run, stamp=ACCEPTED):
    _edit(run / "input_manifest.json", lambda d: d.update(accepted=stamp))


def test_a_market_table_of_reaction_days_zero_to_two_passes_nothing_after_cutoff(run):
    _with_acceptance(run)
    (run / "input_market.json").write_text(json.dumps(_market_table()))
    assert _status(mechanical.grade(run), "mechanical.nothing_after_cutoff") == PASS
    # accepted before the close, day zero is the acceptance day itself
    early = _market_table(cutoff="2026-05-21")
    early["windows"][0].update(accepted="2026-05-19T09:00:00-04:00", day_zero="2026-05-19",
                               days=["2026-05-19", "2026-05-20", "2026-05-21"])
    early["rows"] = early["rows"][:4]
    assert mechanical.market_table_problems(early, datetime.date(2026, 5, 19),
                                            "2026-05-19T09:00:00-04:00") == []


def test_a_market_window_whose_stamp_is_not_the_manifests_fails_nothing_after_cutoff(run):
    """The stamp decides day zero, so the table is not believed about it: a window
    stamped 16:35 on a filing the manifest records as accepted at 15:00 is a day late;
    and a run whose manifest records no acceptance leaves the stamp on trust."""
    import datetime as dt
    assert mechanical.market_table_problems(_market_table(), dt.date(2026, 5, 19),
                                            "2026-05-19T15:00:00-04:00") == [
        "the filing window's acceptance stamp 2026-05-19T16:35:00-04:00 is not the manifest's "
        "2026-05-19T15:00:00-04:00"]
    assert mechanical.market_table_problems(_market_table(), dt.date(2026, 5, 19), None) == [
        "the manifest records no acceptance stamp for the filing, so the filing window's "
        "stamp would stand on trust"]
    (run / "input_market.json").write_text(json.dumps(_market_table()))
    assert _status(mechanical.grade(run), "mechanical.nothing_after_cutoff") == FAIL
    _with_acceptance(run, "2026-05-19T15:00:00-04:00")
    assert _status(mechanical.grade(run), "mechanical.nothing_after_cutoff") == FAIL


def test_a_market_table_reaching_past_reaction_day_two_fails_nothing_after_cutoff(run):
    import datetime as dt
    cutoff = dt.date(2026, 5, 19)
    # a row past day two of the latest window
    late = _market_table(rows=_market_table()["rows"] + [{"date": "2026-05-26"}])
    assert mechanical.market_table_problems(late, cutoff, ACCEPTED) == [
        "row 2026-05-26 is past reaction day two 2026-05-22 of the table's latest window"]
    # a cutoff set past day two of the latest window, with the rows following it
    stretched = _market_table(cutoff="2026-05-26", rows=late["rows"])
    assert mechanical.market_table_problems(stretched, cutoff, ACCEPTED) == [
        "the table's cutoff 2026-05-26 is not reaction day two of its latest window 2026-05-22",
        "row 2026-05-26 is past reaction day two 2026-05-22 of the table's latest window"]
    # days that are not reaction days zero to two of the acceptance stamp: here the
    # window counts from the acceptance day although EDGAR accepted after the close
    shifted = _market_table()
    shifted["windows"][0]["days"] = ["2026-05-19", "2026-05-20", "2026-05-21"]
    assert any("not reaction days zero to two" in p
               for p in mechanical.market_table_problems(shifted, cutoff, ACCEPTED))
    # a filing window for a filing that is not the run's cutoff
    other = _market_table()
    other["windows"][0]["filing_date"] = "2026-05-20"
    assert mechanical.market_table_problems(other, cutoff, ACCEPTED) == [
        "the filing window's filing date 2026-05-20 is not one EDGAR puts on an acceptance at "
        "2026-05-19T16:35:00-04:00",
        "the filing window is for a filing dated 2026-05-20, not the run's cutoff 2026-05-19"]
    # and the regression check reads the run's own table
    _with_acceptance(run)
    (run / "input_market.json").write_text(json.dumps(stretched))
    results = mechanical.grade(run)
    assert _status(results, "mechanical.nothing_after_cutoff") == FAIL
    assert any("input_market.json" in d for d in next(
        r.failures for r in results if r.grader == "mechanical.nothing_after_cutoff"))


def test_a_market_table_with_no_filing_window_fails_nothing_after_cutoff(run):
    """Without a filing window nothing ties the table to the run: a table whose
    cutoff and rows run to 2099 would otherwise be checked against itself alone."""
    import datetime as dt
    loose = {"cutoff": "2099-01-05", "windows": [],
             "rows": [{"date": d} for d in ("2026-05-19", "2099-01-02", "2099-01-05")]}
    assert mechanical.market_table_problems(loose, dt.date(2026, 5, 19), ACCEPTED) == [
        "the table has no filing window, so nothing ties it to the run's filing"]
    _with_acceptance(run)
    (run / "input_market.json").write_text(json.dumps(loose))
    assert _status(mechanical.grade(run), "mechanical.nothing_after_cutoff") == FAIL


def test_a_market_table_missing_a_row_of_the_window_fails_nothing_after_cutoff():
    """The rows are not the calendar the table is checked against: a table missing
    the row for the real day zero, or a row inside the window, is a day late."""
    import datetime as dt
    cutoff = dt.date(2026, 5, 19)
    # accepted Tuesday 09:00, before the close: the 19th is day zero and has to be a row
    early = _market_table(cutoff="2026-05-22")
    early["windows"][0].update(accepted="2026-05-19T09:00:00-04:00", day_zero="2026-05-20")
    early["rows"] = [{"date": d} for d in ("2026-05-18", "2026-05-20", "2026-05-21", "2026-05-22")]
    problems = mechanical.market_table_problems(early, cutoff, '2026-05-19T09:00:00-04:00')
    assert "the filing window: no row for 2026-05-19" in problems
    assert any("are not reaction days zero to two ['2026-05-19', '2026-05-20', '2026-05-21']"
               in p for p in problems)
    # Wednesday's row missing inside the window
    inside = _market_table(cutoff="2026-05-22")
    inside["windows"][0].update(accepted="2026-05-19T09:00:00-04:00", day_zero="2026-05-19",
                                days=["2026-05-19", "2026-05-21", "2026-05-22"])
    inside["rows"] = [{"date": d} for d in ("2026-05-18", "2026-05-19", "2026-05-21", "2026-05-22")]
    assert "the filing window: no row for 2026-05-20" in mechanical.market_table_problems(
        inside, cutoff, "2026-05-19T09:00:00-04:00")
    # a row on a Saturday
    weekend = _market_table(rows=_market_table()["rows"] + [{"date": "2026-05-16"}])
    assert mechanical.market_table_problems(weekend, cutoff, ACCEPTED) == ["row 2026-05-16 is not a trading day"]


def test_the_exchange_calendar_is_worked_by_hand():
    """Memorial Day 2026 is Monday the 25th of May; Good Friday 2026 is the 3rd of
    April (Easter the 5th); Juneteenth 2027 falls on a Saturday and is observed the
    Friday before; New Year's Day 2028 is a Saturday and is not observed; the exchange
    closed on 2025-01-09 outside its rules. EDGAR's next business day skips Columbus
    Day 2026, Monday the 12th of October, which the exchange does not close for."""
    import datetime as dt
    assert mechanical._easter(2026) == dt.date(2026, 4, 5)
    assert dt.date(2026, 5, 25) in mechanical.exchange_holidays(2026)
    assert dt.date(2026, 4, 3) in mechanical.exchange_holidays(2026)
    assert dt.date(2027, 6, 18) in mechanical.exchange_holidays(2027)
    assert dt.date(2028, 1, 1) not in mechanical.exchange_holidays(2028)
    assert dt.date(2027, 12, 31) not in mechanical.exchange_holidays(2027)
    assert not mechanical.is_trading_day(dt.date(2025, 1, 9))
    assert mechanical.is_trading_day(dt.date(2026, 10, 12))
    assert mechanical.next_business_day(dt.date(2026, 10, 9)) == dt.date(2026, 10, 13)
    # the federal calendar observes a Saturday New Year's Day on the Friday before;
    # the exchange does not: 2027-12-31 is open and EDGAR is closed
    assert dt.date(2027, 12, 31) in mechanical.federal_holidays(2027)
    assert mechanical.next_business_day(dt.date(2027, 12, 30)) == dt.date(2028, 1, 3)
    assert mechanical.is_trading_day(dt.date(2027, 12, 31))
    # early closes: the day after Thanksgiving 2026, Christmas Eve 2026 (a Thursday),
    # July 3 2025 (a Thursday); July 3 2026 is the observed holiday, not an early close
    assert mechanical.close_time(dt.date(2026, 11, 27)) == dt.time(13, 0)
    assert mechanical.close_time(dt.date(2026, 12, 24)) == dt.time(13, 0)
    assert mechanical.close_time(dt.date(2025, 7, 3)) == dt.time(13, 0)
    assert not mechanical.is_trading_day(dt.date(2026, 7, 3))
    assert mechanical.close_time(dt.date(2026, 5, 19)) == dt.time(16, 0)
    assert mechanical.trading_days_from(dt.date(2026, 5, 22), 3) == [
        dt.date(2026, 5, 22), dt.date(2026, 5, 26), dt.date(2026, 5, 27)]


def test_a_market_window_over_a_holiday_passes_nothing_after_cutoff():
    """A filing accepted Friday 2026-05-22 at 16:35 has day zero on Tuesday the 26th,
    after Memorial Day; one accepted Thursday 2026-04-02 at 16:35 has day zero on
    Monday the 6th, after Good Friday; one accepted Wednesday 2025-01-08 at 16:35 has
    day zero on Friday the 10th, after the day of mourning."""
    import datetime as dt
    memorial = {"cutoff": "2026-05-28",
                "windows": [{"kind": "filing", "filing_date": "2026-05-22",
                             "accepted": "2026-05-22T16:35:00-04:00", "day_zero": "2026-05-26",
                             "days": ["2026-05-26", "2026-05-27", "2026-05-28"]}],
                "rows": [{"date": d} for d in ("2026-05-21", "2026-05-22", "2026-05-26",
                                               "2026-05-27", "2026-05-28")]}
    assert mechanical.market_table_problems(memorial, dt.date(2026, 5, 22), '2026-05-22T16:35:00-04:00') == []
    good_friday = {"cutoff": "2026-04-08",
                   "windows": [{"kind": "filing", "filing_date": "2026-04-02",
                                "accepted": "2026-04-02T16:35:00-04:00", "day_zero": "2026-04-06",
                                "days": ["2026-04-06", "2026-04-07", "2026-04-08"]}],
                   "rows": [{"date": d} for d in ("2026-04-01", "2026-04-02", "2026-04-06",
                                                  "2026-04-07", "2026-04-08")]}
    assert mechanical.market_table_problems(good_friday, dt.date(2026, 4, 2), '2026-04-02T16:35:00-04:00') == []
    mourning = {"cutoff": "2025-01-14",
                "windows": [{"kind": "filing", "filing_date": "2025-01-08",
                             "accepted": "2025-01-08T16:35:00-05:00", "day_zero": "2025-01-10",
                             "days": ["2025-01-10", "2025-01-13", "2025-01-14"]}],
                "rows": [{"date": d} for d in ("2025-01-07", "2025-01-08", "2025-01-10",
                                               "2025-01-13", "2025-01-14")]}
    assert mechanical.market_table_problems(mourning, dt.date(2025, 1, 8), '2025-01-08T16:35:00-05:00') == []


def test_a_market_window_on_an_early_close_day_counts_from_the_next_trading_day():
    """A filing accepted at 14:00 on 2026-11-27, the day after Thanksgiving, came
    after that day's one o'clock close: day zero is Monday the 30th."""
    import datetime as dt
    stamp = "2026-11-27T14:00:00-05:00"
    table = {"cutoff": "2026-12-02",
             "windows": [{"kind": "filing", "filing_date": "2026-11-27", "accepted": stamp,
                          "day_zero": "2026-11-30",
                          "days": ["2026-11-30", "2026-12-01", "2026-12-02"]}],
             "rows": [{"date": d} for d in ("2026-11-25", "2026-11-27", "2026-11-30",
                                            "2026-12-01", "2026-12-02")]}
    assert mechanical.market_table_problems(table, dt.date(2026, 11, 27), stamp) == []
    same_day = dict(table, cutoff="2026-12-01")
    same_day["windows"] = [dict(table["windows"][0], day_zero="2026-11-27",
                                days=["2026-11-27", "2026-11-30", "2026-12-01"])]
    assert any("not reaction days zero to two" in p for p in
               mechanical.market_table_problems(same_day, dt.date(2026, 11, 27), stamp))


def test_a_market_window_for_a_later_filing_fails_nothing_after_cutoff():
    """A window of another kind is an earlier filing's, say the earnings release
    before the 10-Q; one dated after the run's cutoff is not an input, and would
    otherwise carry the table's cutoff and late-row limit out to its own day two."""
    import datetime as dt
    table = _market_table(cutoff="2026-05-28")
    table["windows"].append({"kind": "earnings_release", "filing_date": "2026-05-22",
                             "accepted": "2026-05-22T16:35:00-04:00", "day_zero": "2026-05-26",
                             "days": ["2026-05-26", "2026-05-27", "2026-05-28"]})
    table["rows"] += [{"date": d} for d in ("2026-05-26", "2026-05-27", "2026-05-28")]
    assert mechanical.market_table_problems(table, dt.date(2026, 5, 19), ACCEPTED) == [
        "the earnings_release window is for a filing dated 2026-05-22, after the run's "
        "cutoff 2026-05-19"]
    # the same window a week earlier is the release before the filing, and stands
    earlier = _market_table()
    earlier["windows"].insert(0, {"kind": "earnings_release", "filing_date": "2026-05-13",
                                  "accepted": "2026-05-13T16:35:00-04:00",
                                  "day_zero": "2026-05-14",
                                  "days": ["2026-05-14", "2026-05-15", "2026-05-18"]})
    earlier["rows"] = [{"date": d} for d in ("2026-05-13", "2026-05-14", "2026-05-15")] \
        + earlier["rows"]
    assert mechanical.market_table_problems(earlier, dt.date(2026, 5, 19), ACCEPTED) == []


def test_a_market_table_with_no_acceptance_stamp_fails_nothing_after_cutoff():
    import datetime as dt
    unstamped = _market_table()
    del unstamped["windows"][0]["accepted"]
    assert mechanical.market_table_problems(unstamped, dt.date(2026, 5, 19), ACCEPTED) == [
        "the filing window carries no acceptance stamp"]


def test_a_non_finite_value_fails_calculator_finite(run):
    text = (run / "calculator.json").read_text(encoding="utf-8")
    data = json.loads(text)
    data["ratios"]["liquidity"]["current_ratio"]["value"] = float("nan")
    (run / "calculator.json").write_text(json.dumps(data), encoding="utf-8")
    assert _status(mechanical.grade(run), "mechanical.calculator_finite") == FAIL


def test_a_tampered_enterprise_value_fails_dcf_recomputes(run):
    _edit(run / "calculator.json",
          lambda d: d["valuation"]["scenarios"]["base"].update(enterprise_value=1.0))
    assert _status(mechanical.grade(run), "mechanical.dcf_recomputes") == FAIL


def test_a_failed_agent_fails_agents_written(run):
    _edit(run / "input_manifest.json",
          lambda d: d["agents"]["financial-analyst"].update(result="failed"))
    assert _status(mechanical.grade(run), "mechanical.agents_written") == FAIL


def test_a_missing_file_fails_files_present(run):
    (run / "memo_ko.md").unlink()
    assert _status(mechanical.grade(run), "mechanical.files_present") == FAIL


def test_an_absent_area_fails_and_a_dropped_one_does_not(run):
    _edit(run / "analysis_accounting.json",
          lambda d: d["areas"]["industry_lens"].update(dropped="finding: the gate's reason"))
    assert _status(coverage.grade(run), "coverage.accounting_areas") == PASS
    _edit(run / "analysis_accounting.json", lambda d: d["areas"].pop("industry_lens"))
    assert _status(coverage.grade(run), "coverage.accounting_areas") == FAIL


def test_an_absent_dupont_fails_financial_sections(run):
    _edit(run / "analysis_financial.json", lambda d: d.pop("dupont"))
    assert _status(coverage.grade(run), "coverage.financial_sections") == FAIL


def test_no_range_and_no_reason_fails_valuation_answer(run):
    _edit(run / "calculator.json", lambda d: d["valuation"].update(
        value_range_per_share=None, scenarios={}))
    assert _status(coverage.grade(run), "coverage.valuation_answer") == FAIL


def test_a_memo_without_the_finance_frame_fails_memo_frames(run):
    memo = run / "memo_ko.md"
    memo.write_text("\n".join(line for line in memo.read_text(encoding="utf-8").splitlines()
                              if not (line.startswith("#") and "재무" in line)), encoding="utf-8")
    assert _status(coverage.grade(run), "coverage.memo_frames") == FAIL


def test_a_recommendation_in_the_valuation_fails_forbidden_words(run):
    _edit(run / "analysis_valuation.json", lambda d: d["value_range"].update(
        reading=d["value_range"]["reading"] + " Investors should buy."))
    assert _status(coverage.grade(run), "coverage.forbidden_words") == FAIL


def test_an_accusation_anywhere_fails_forbidden_words(run):
    _edit(run / "analysis_accounting.json", lambda d: d["areas"]["cost_deferral"].update(
        finding="This looks like fraud."))
    assert _status(coverage.grade(run), "coverage.forbidden_words") == FAIL


def test_a_company_selling_product_is_not_a_recommendation(run):
    _edit(run / "analysis_accounting.json", lambda d: d["areas"]["cost_deferral"].update(
        finding="Credit extended to sell product and an agreement to buy a supplier."))
    assert _status(coverage.grade(run), "coverage.forbidden_words") == PASS


def test_a_score_field_fails_no_combined_score(run):
    _edit(run / "analysis_financial.json", lambda d: d.update(overall_score=0.7))
    assert _status(coverage.grade(run), "coverage.no_combined_score") == FAIL


# --- golden cases ----------------------------------------------------------------------------

CASE = {"filing": {"accession": "0000858877-26-000078"}, "frame": "accounting",
        "must_find": [{"area": "earnings_versus_cash", "what": "income up, cash down",
                       "keywords": ["operating cash flow falls"]},
                      {"what": "a finding nobody made", "keywords": ["zeppelin"]}],
        "must_not_claim": [{"what": "a claim nobody made", "keywords": ["zeppelin"]}],
        "approved_by_owner": True}


def test_golden_scores_found_and_missed_with_partial_credit():
    row = golden.score_run(CASE, CLEAN)
    assert row["found"] == ["income up, cash down"]
    assert row["missed"] == ["a finding nobody made"]
    assert row["score"] == pytest.approx(0.5)


def test_golden_takes_credit_away_for_a_claim_it_must_not_make():
    case = dict(CASE, must_not_claim=[{"what": "x", "keywords": ["operating cash flow falls"]}])
    assert golden.score_run(case, CLEAN)["score"] == pytest.approx(0.0)


def test_golden_counts_only_approved_cases_in_cases():
    assert all(case.get("approved_by_owner") is True for _, case in golden.approved_cases())


def test_the_case_format_reads_the_template_and_refuses_what_it_cannot_read():
    template = loads((REPO / "evals" / "golden" / "TEMPLATE.yaml").read_text(encoding="utf-8"))
    assert template["approved_by_owner"] is False
    assert template["must_find"][0]["paragraph_ids"] == ["0000000000-00-000000:notes:0"]
    for bad in ("a:\n\tb: 1\n", 'a: "open\n', "a: 1\na: 2\n", "a: {b: 1}\n"):
        with pytest.raises(GoldenFormatError):
            loads(bad)


def test_golden_credits_a_filing_paragraph_reached_through_a_reader_item():
    case = dict(CASE, must_find=[{"what": "by paragraph", "paragraph_ids": [NINE_MONTH_CASH_FLOW]}],
                must_not_claim=[])
    assert golden.score_run(case, CLEAN)["score"] == pytest.approx(1.0)
    # a paragraph no reader item cites reaches nothing
    case = dict(case, must_find=[{"what": "x", "paragraph_ids": ["0000858877-26-000078:notes:1"]}])
    assert golden.score_run(case, CLEAN)["score"] == pytest.approx(0.0)


def test_golden_keywords_are_whole_words():
    anomaly = {"id": "a", "name": "an improbable shortfall to resell", "what": ""}
    for word in ("probable", "falls", "sell"):
        assert not golden.matches(anomaly, {"keywords": [word]}), word
    assert golden.matches(anomaly, {"keywords": ["improbable resell"]})


def test_golden_credits_nothing_to_evidence_that_resolves_to_no_reader_item():
    anomaly = {"id": "a", "area": "x", "evidence": ["0000858877-26-000078:notes:1"],
               "paragraphs": set()}
    assert not golden.matches(anomaly, {"paragraph_ids": ["0000858877-26-000078:notes:1"]})


# --- the capability graders that read more than one run -----------------------------------

from evals.capability import consistency, grader_agreement, memorization, outcomes, rubric_score  # noqa: E402


def test_consistency_is_one_for_identical_runs_and_less_when_they_differ(tmp_path, monkeypatch):
    first = tmp_path / "CSCO" / "a"
    second = tmp_path / "CSCO" / "b"
    for target in (first, second):
        shutil.copytree(CLEAN, target, ignore=shutil.ignore_patterns("agents", "control-*"))
    monkeypatch.setattr(golden, "approved_cases", lambda: [(Path("case.yaml"), CASE)])
    same = consistency.grade([first, second])
    assert same["cases"][0]["anomaly_overlap"] == pytest.approx(1.0)
    assert same["cases"][0]["value_spread"] == pytest.approx(0.0)
    _edit(second / "analysis_accounting.json", lambda d: d.update(anomalies=d["anomalies"][:1]))
    differ = consistency.grade([first, second])
    assert differ["cases"][0]["anomaly_overlap"] < 1.0


# Read off the published run by hand: the one accounting anomaly whose name holds
# the words "operating cash flow falls" is this one.
CASH_FALLS = "earnings_versus_cash_operating_cash_flow_falls_while_net_income_rises"


def test_grader_agreement_counts_where_the_grader_matches_the_owner(tmp_path, monkeypatch):
    run = tmp_path / "CSCO" / CLEAN.name
    shutil.copytree(CLEAN, run, ignore=shutil.ignore_patterns("agents", "control-*"))
    (run / "grade.json").write_text(json.dumps({"items": [
        {"id": CASH_FALLS, "verdict": "supported", "severity": "high"}]}))
    monkeypatch.setattr(golden, "approved_cases", lambda: [(Path("case.yaml"), CASE)])
    assert grader_agreement.grade([run])["score"] == pytest.approx(1.0)
    (run / "grade.json").write_text(json.dumps({"items": [
        {"id": CASH_FALLS, "verdict": "unsupported", "severity": "high"}]}))
    assert grader_agreement.grade([run])["score"] == pytest.approx(0.0)


def test_outcomes_without_a_market_table_leave_four_weekdays_to_the_inputs():
    """CSCO's cutoff is 2026-05-19, a Tuesday, and the run holds no market table. Four
    weekdays after it is Monday the 25th (Memorial Day, which weekday counting does
    not know; the fourth weekday is the slack for it). The window opens Tuesday the
    26th. Counted by hand from the 26th: May 26-29 is 4 weekdays, June 22, July 23,
    August 3-14 is 10, so the fifty-ninth is 2026-08-14 and the sixtieth the 17th."""
    import datetime as dt
    assert outcomes.last_day_an_input_may_see(CLEAN, dt.date(2026, 5, 19)) == dt.date(2026, 5, 25)
    assert outcomes.first_outcome_day(CLEAN, dt.date(2026, 5, 19)) == dt.date(2026, 5, 26)
    early = outcomes.grade([CLEAN], today=dt.date(2026, 8, 14))["runs"][0]
    late = outcomes.grade([CLEAN], today=dt.date(2026, 8, 17))["runs"][0]
    assert early["status"] == "pending" and early["trading_days_in_window"] == 59
    assert late["status"] == "aged" and late["trading_days_in_window"] == 60
    assert late["first_outcome_day"] == "2026-05-26"


def test_outcomes_with_a_market_table_start_after_its_latest_day_two(tmp_path):
    """The outcome window opens the day after reaction day two of the table's latest
    window, read off the window's days and never off the table's own `cutoff`
    field: a filing accepted Tuesday 2026-05-19 before the close has day two on
    Thursday the 21st, and the window opens Friday the 22nd, whatever the field says."""
    import datetime as dt
    run = tmp_path / "CSCO" / CLEAN.name
    shutil.copytree(CLEAN, run, ignore=shutil.ignore_patterns("agents", "control-*"))
    table = {"cutoff": "2026-05-29", "rows": [],
             "windows": [{"kind": "filing", "filing_date": "2026-05-19",
                          "accepted": "2026-05-19T09:00:00-04:00",
                          "days": ["2026-05-19", "2026-05-20", "2026-05-21"]}]}
    (run / "input_market.json").write_text(json.dumps(table))
    assert outcomes.last_day_an_input_may_see(run, dt.date(2026, 5, 19)) == dt.date(2026, 5, 21)
    assert outcomes.first_outcome_day(run, dt.date(2026, 5, 19)) == dt.date(2026, 5, 22)
    # a table with no windows says nothing about day two: the four weekdays stand
    (run / "input_market.json").write_text(json.dumps({"cutoff": "2026-05-21", "rows": []}))
    assert outcomes.last_day_an_input_may_see(run, dt.date(2026, 5, 19)) == dt.date(2026, 5, 25)


def test_outcomes_count_company_events_and_never_the_ledgers_process_rows(tmp_path):
    import datetime as dt
    ledger = tmp_path / "ledger.jsonl"
    ledger.write_text("\n".join([
        json.dumps({"ticker": "CSCO", "date": "2026-06-01", "event": "restatement"}),
        json.dumps({"ticker": "CSCO", "date": "2026-05-25", "event": "a day an input may see"}),
        json.dumps({"ticker": "CSCO", "at": "2026-06-01T00:00:00+00:00", "accession": "x",
                    "layers_that_ran": ["detect filing"]}),
        json.dumps({"at": "2026-06-02T00:00:00+00:00", "lens": "codex", "verdict": "pass"}),
    ]) + "\n")
    out = outcomes.grade([CLEAN], today=dt.date(2026, 9, 1), ledger=ledger)
    assert out["runs"][0]["events"] == 1
    assert "no company event row" not in out["status"]
    assert "no company event row" in outcomes.grade([CLEAN], today=dt.date(2026, 9, 1),
                                                    ledger=tmp_path / "none")["status"]


def test_memorization_never_calls_a_run_clean_without_a_cutoff_on_record(monkeypatch):
    assert memorization.classify(CLEAN)["status"] == "unknown"
    monkeypatch.setattr(memorization, "TRAINING_CUTOFF",
                        {"claude-fable-5-1": ("2026-01", "s"), "claude-opus-5-5": ("2026-01", "s")})
    assert memorization.classify(CLEAN)["status"] == "forward"       # filed 2026-05
    monkeypatch.setattr(memorization, "TRAINING_CUTOFF",
                        {"claude-fable-5-1": ("2026-06", "s"), "claude-opus-5-5": ("2026-01", "s")})
    assert memorization.classify(CLEAN)["status"] == "historical"


def test_memorization_calls_a_run_with_no_served_model_unknown(tmp_path):
    run = tmp_path / "CSCO" / CLEAN.name
    shutil.copytree(CLEAN, run, ignore=shutil.ignore_patterns("agents", "control-*"))
    _edit(run / "input_manifest.json", lambda d: d.update(agents={}))
    assert memorization.classify(run)["status"] == "unknown"


def test_the_grader_score_is_recomputed_from_its_items():
    """High supported (3 x 1) + medium unclear (2 x 0.5) + low unsupported (1 x 0),
    over weight 6: 4 / 6. A dealbreaker on the first item takes its 3 away: 1 / 6."""
    grade = {"items": [{"id": "a", "verdict": "supported", "severity": "high"},
                       {"id": "b", "verdict": "unclear", "severity": "medium"},
                       {"id": "c", "verdict": "unsupported", "severity": "low"}],
             "score": 0.9}
    out = rubric_score.check(grade)
    assert out["score"] == pytest.approx(4 / 6) and out["agrees"] is False
    assert out["unreadable"] == []
    grade["dealbreakers"] = [{"kind": "number_not_from_calculator", "id": "a",
                              "where": "anomalies[0].what", "why": "a bare figure"}]
    assert rubric_score.recompute(grade) == pytest.approx(1 / 6)
    # a whole-run dealbreaker with no id strikes no item
    grade["dealbreakers"] = [{"kind": "post_cutoff_fact", "id": None, "where": "memo", "why": "x"}]
    assert rubric_score.recompute(grade) == pytest.approx(4 / 6)


# --- the eval runner: exit status, floors, the scoreboard and --quick ----------------------

from evals import __main__ as runner  # noqa: E402


def _isolated(monkeypatch, tmp_path, runs):
    monkeypatch.setattr(runner, "SCOREBOARD", tmp_path / "scoreboard.jsonl")
    monkeypatch.setattr(runner, "THRESHOLDS", tmp_path / "thresholds.json")
    monkeypatch.setattr(runner, "find_runs", lambda paths=None: runs)
    monkeypatch.setattr(runner, "changed_runs", lambda base="origin/main": runs)


def test_make_eval_exits_zero_on_the_clean_run_and_appends_one_scoreboard_line(run, monkeypatch, tmp_path):
    _isolated(monkeypatch, tmp_path, [run])
    assert runner.main([]) == 0
    assert runner.main([]) == 0
    lines = (tmp_path / "scoreboard.jsonl").read_text().splitlines()
    assert len(lines) == 2
    assert json.loads(lines[0])["regression"]["fail"] == 0


def test_make_eval_exits_one_on_a_regression_failure(run, monkeypatch, tmp_path):
    _isolated(monkeypatch, tmp_path, [run])
    (run / "memo_ko.md").unlink()
    assert runner.main(["--no-scoreboard"]) == 1


def test_make_eval_exits_one_below_a_floor_the_owner_set(run, monkeypatch, tmp_path):
    _isolated(monkeypatch, tmp_path, [run])
    (tmp_path / "thresholds.json").write_text(json.dumps(
        {"capability": {"coverage.accounting_areas_answered": 1.01}}))
    assert runner.main(["--no-scoreboard"]) == 1
    (tmp_path / "thresholds.json").write_text("{}")
    assert runner.main(["--no-scoreboard"]) == 0


def test_eval_quick_grades_only_the_changed_runs_and_writes_no_scoreboard(run, monkeypatch, tmp_path):
    _isolated(monkeypatch, tmp_path, [run])
    assert runner.main(["--quick"]) == 0
    assert not (tmp_path / "scoreboard.jsonl").exists()
    monkeypatch.setattr(runner, "changed_runs", lambda base="origin/main": [])
    assert runner.main(["--quick"]) == 0


def test_a_grade_the_formula_cannot_read_scores_nothing_and_says_which_item():
    grade = {"items": [{"id": "a", "verdict": "supported", "severity": "high"},
                       {"id": "b", "verdict": "maybe", "severity": "high"},
                       {"id": "c", "verdict": "supported"}], "score": 1.0}
    out = rubric_score.check(grade)
    assert out["score"] is None
    assert out["unreadable"] == ["items[1]: verdict 'maybe'", "items[2]: severity None"]


def test_a_grade_with_a_repeated_item_or_a_dealbreaker_naming_no_item_scores_nothing():
    """A repeated supported item would outweigh an unsupported one: 3 + 3 + 0 over 7
    reads 0.857 where the honest grade is 3 + 0 over 4; the formula refuses it."""
    grade = {"items": [{"id": "a", "verdict": "supported", "severity": "high"},
                       {"id": "a", "verdict": "supported", "severity": "high"},
                       {"id": "b", "verdict": "unsupported", "severity": "low"}], "score": 0.857}
    assert rubric_score.unreadable(grade) == ["items[1]: id a given twice"]
    assert rubric_score.recompute(grade) is None
    honest = {"items": grade["items"][1:], "score": 0.75}
    assert rubric_score.recompute(honest) == pytest.approx(0.75)
    honest["dealbreakers"] = [{"kind": "post_cutoff_fact", "id": "zzz", "where": "x", "why": "y"}]
    assert rubric_score.unreadable(honest) == ["dealbreakers[0]: names no item 'zzz'"]
    assert rubric_score.recompute(honest) is None


def test_a_grade_must_cover_every_anomaly_of_the_run_and_nothing_else():
    """A grader that left out the item it would have called unsupported would score
    the rest alone; one that graded an anomaly the run does not list graded nothing."""
    grade = {"items": [{"id": "a", "verdict": "supported", "severity": "high"},
                       {"id": "b", "verdict": "unsupported", "severity": "low"}], "score": 0.75}
    assert rubric_score.check(grade, {"a", "b"})["unreadable"] == []
    assert rubric_score.recompute(grade, {"a", "b"}) == pytest.approx(0.75)
    assert rubric_score.unreadable(grade, {"a", "b", "c"}) == ["anomaly c has no item"]
    assert rubric_score.recompute(grade, {"a", "b", "c"}) is None
    assert rubric_score.unreadable(grade, {"a"}) == ["no anomaly b in the run"]
    assert rubric_score.check(grade, {"a"})["score"] is None
    # without the run's anomalies the items alone are read, as before
    assert rubric_score.unreadable(grade) == []


def test_the_runner_reads_the_anomaly_ids_off_both_frames():
    ids = runner.anomaly_ids(CLEAN)
    accounting = json.loads((CLEAN / "analysis_accounting.json").read_text())["anomalies"]
    financial = json.loads((CLEAN / "analysis_financial.json").read_text())["anomalies"]
    assert ids == {a["id"] for a in accounting} | {a["id"] for a in financial} and ids


def test_the_graders_read_the_tree_aaer_repo_names(tmp_path):
    """CI runs main's evals/ from outside the tree it grades: the environment names
    the tree, and without it the graders read the tree they sit in."""
    import os
    import subprocess
    import sys
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    # -I ignores PYTHONPATH, as it does in CI: the tree is put on the path by name
    code = f"import sys; sys.path.append({str(REPO)!r}); import evals.common as c; print(c.REPO)"
    env = {**os.environ, "AAER_REPO": str(elsewhere)}
    named = subprocess.run([sys.executable, "-I", "-c", code], env=env, cwd=tmp_path,
                           capture_output=True, text=True, check=True)
    assert Path(named.stdout.strip()) == elsewhere.resolve()
    env.pop("AAER_REPO")
    own = subprocess.run([sys.executable, "-I", "-c", code], env=env, cwd=tmp_path,
                         capture_output=True, text=True, check=True)
    assert Path(own.stdout.strip()) == REPO.resolve()


def test_changed_runs_reads_the_branch_against_origin_main(tmp_path, monkeypatch):
    import subprocess
    git = lambda *a: subprocess.run(["git", *a], cwd=tmp_path, check=True, capture_output=True)  # noqa: E731
    git("init", "-q", "-b", "work")
    git("config", "user.email", "t@t")
    git("config", "user.name", "t")
    for ticker in ("AAA", "BBB"):
        run = tmp_path / "runs" / ticker / "1"
        run.mkdir(parents=True)
        (run / "input_manifest.json").write_text("{}")
        (run / "calculator.json").write_text("{}")
    git("add", ".")
    git("commit", "-q", "-m", "base")
    git("update-ref", "refs/remotes/origin/main", "HEAD")
    monkeypatch.setattr(runner, "REPO", tmp_path)
    assert runner.changed_runs() == []
    (tmp_path / "runs" / "BBB" / "1" / "calculator.json").write_text('{"changed": 1}')
    git("commit", "-q", "-am", "change BBB")
    assert [r.name for r in runner.changed_runs()] == ["1"]
    assert [r.parent.name for r in runner.changed_runs()] == ["BBB"]
