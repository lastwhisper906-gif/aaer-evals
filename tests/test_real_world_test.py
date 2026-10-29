"""The real-world test's rule, judged on cases, filings and analyses planted here.

Every expected value is the rule of `src/real_world_test.py`'s docstring applied
by hand to what the test plants: a quote stands when it is on its page as the
page's text reads (whitespace, typographic quotes and dashes, a PDF's ligatures
and line-end hyphens folded, nothing else); a candidate filing stands when
EDGAR's index records it so and it was filed before the problem became public;
a control is the same form within 92 days, with what a run needs, and no
non-reliance 8-K and no amended report in the three years after; a case is
flagged when an anomaly in an area its named accounts map to says the numbers
contradict the prose, questioned when one there says anything but confirms.
"""

from __future__ import annotations

import json

import pytest

from src import real_world_test as rw


def test_a_quote_stands_through_whitespace_quotes_dashes_ligatures_and_line_breaks():
    page = ("The Company “prematurely recognized” revenue—on ship-\nments "
            "held at a third-party warehouse ﬁnanced by the reseller.")
    assert rw.quote_on_page('"prematurely recognized" revenue-on shipments held at', page)
    assert rw.quote_on_page("financed by the reseller", page)
    assert not rw.quote_on_page("recognized revenue on shipments", page)
    assert not rw.quote_on_page("", page)


def test_an_html_page_is_read_as_its_text():
    raw = b"<html><body><p>Super&nbsp;Micro <b>improperly</b> recognized</p><p>revenue</p>"
    assert rw.quote_on_page("Super Micro improperly recognized revenue", rw.page_text(raw))


CASE = {
    "aaer_number": "4000", "company": "Planted Devices Inc.", "cik": 1234567, "sic": "3572",
    "order_url": "https://www.sec.gov/order.htm",
    "periods_quote": "from fiscal 2015 through fiscal 2017",
    "accounts": [{"account": "revenue", "practice": "early shipments",
                  "quote": "recognized revenue on goods shipped early"},
                 {"account": "reserves_and_estimates", "practice": "reserve release",
                  "quote": "released its warranty reserve"}],
    "first_public": {"date": "2018-01-30", "what": "non-reliance 8-K",
                     "source_url": "https://www.sec.gov/8k.htm",
                     "quote": "should no longer be relied upon"},
    "candidate_filings": [
        {"form": "10-Q", "accession": "0001234567-17-000020", "filing_date": "2017-11-08",
         "period_end": "2017-09-30"},
        {"form": "10-K", "accession": "0001234567-17-000010", "filing_date": "2017-08-28",
         "period_end": "2017-06-30"}],
}
PAGES = {"https://www.sec.gov/order.htm":
         b"<p>from fiscal 2015 through fiscal 2017 it recognized revenue on goods shipped "
         b"early and released its warranty reserve</p>",
         "https://www.sec.gov/8k.htm": b"<p>financial statements should no longer be relied "
                                       b"upon</p>"}
INDEX = [{"accessionNumber": "0001234567-17-000020", "form": "10-Q", "filingDate": "2017-11-08",
          "reportDate": "2017-09-30", "items": ""},
         {"accessionNumber": "0001234567-17-000010", "form": "10-K", "filingDate": "2017-08-28",
          "reportDate": "2017-06-30", "items": ""}]


def test_a_case_whose_every_source_holds_has_no_problem():
    assert rw.check_case(CASE, PAGES.__getitem__, INDEX) == []
    assert rw.latest_candidate(CASE)["accession"] == "0001234567-17-000020"


def test_a_case_is_refused_for_a_missing_quote_a_wrong_filing_or_a_late_one():
    pages = dict(PAGES)
    pages["https://www.sec.gov/order.htm"] = b"<p>from fiscal 2015 through fiscal 2017</p>"
    index = [dict(INDEX[0], filingDate="2017-11-09"), INDEX[1]]
    late = json.loads(json.dumps(CASE))
    late["first_public"]["date"] = "2017-11-08"
    late["accounts"].append({"account": "goodwill", "quote": "x"})
    problems = rw.check_case(CASE, pages.__getitem__, index)
    assert sum("account revenue: the quote is not on" in p for p in problems) == 1
    assert sum("account reserves_and_estimates: the quote is not on" in p for p in problems) == 1
    assert any("EDGAR records 10-Q filed 2017-11-09" in p for p in problems)
    problems = rw.check_case(late, PAGES.__getitem__, INDEX)
    assert any("filed on or after the problem became public (2017-11-08)" in p for p in problems)
    assert any("'goodwill' is not one this test maps" in p for p in problems)


def _row(accession, form, filed, items="", period="2017-09-30"):
    return {"accessionNumber": accession, "form": form, "filingDate": filed,
            "reportDate": period, "items": items}


NEEDS = [_row("a-1", "10-K", "2017-02-20"), _row("a-2", "10-Q", "2017-05-01"),
         _row("a-3", "10-Q", "2017-08-01"), _row("a-4", "8-K", "2017-10-25", "2.02,9.01")]


def test_a_clean_filing_is_the_nearest_of_the_form_in_the_window():
    rows = NEEDS + [_row("c-1", "10-Q", "2017-11-01"), _row("c-2", "10-Q", "2018-02-05")]
    # 2017-11-01 is 7 days from 2017-11-08, 2018-02-05 is 89 days
    assert rw.clean_filing(rows, "10-Q", "2017-11-08")["accessionNumber"] == "c-1"
    # 93 days away is outside the window
    assert rw.clean_filing(NEEDS + [_row("c-3", "10-Q", "2018-02-09")], "10-Q",
                           "2017-11-08") is None


@pytest.mark.parametrize("later", [_row("x", "8-K", "2020-10-30", "4.02,9.01"),
                                   _row("x", "10-Q/A", "2019-03-01"),
                                   _row("x", "10-K/A", "2018-01-15")])
def test_a_filing_followed_by_non_reliance_or_an_amendment_within_three_years_is_not_clean(later):
    rows = NEEDS + [_row("c-1", "10-Q", "2017-11-01"), later]
    assert rw.clean_filing(rows, "10-Q", "2017-11-08") is None


def test_an_amendment_more_than_three_years_after_leaves_the_filing_clean():
    # 2017-11-01 plus 3 x 365 days is 2020-10-31; a 10-K/A on 2020-11-02 is after it
    rows = NEEDS + [_row("c-1", "10-Q", "2017-11-01"), _row("x", "10-K/A", "2020-11-02")]
    assert rw.clean_filing(rows, "10-Q", "2017-11-08")["accessionNumber"] == "c-1"


def test_a_company_without_what_a_run_needs_is_no_control():
    rows = [_row("a-2", "10-Q", "2017-05-01"), _row("c-1", "10-Q", "2017-11-01"),
            _row("a-4", "8-K", "2017-10-25", "2.02")]
    assert rw.clean_filing(rows, "10-Q", "2017-11-08") is None      # no 10-K before it


def test_the_control_is_the_nearest_clean_filer_of_the_same_code_and_never_a_case():
    listing = (b"<cik>0001234567</cik><cik>0000000011</cik><cik>0000000022</cik>"
               b"<cik>0000000033</cik>")
    histories = {
        11: NEEDS + [_row("e-1", "10-Q", "2017-10-30")],                       # 9 days
        22: NEEDS + [_row("f-1", "10-Q", "2017-11-10")],                       # 2 days
        33: NEEDS + [_row("g-1", "10-Q", "2017-11-08"),                        # 0 days, but
                     _row("g-2", "8-K", "2019-05-01", "4.02")],                # not clean
    }
    control = rw.pick_control(CASE, rw.latest_candidate(CASE), lambda url: listing,
                              histories.__getitem__, avoid=set())
    assert (control["cik"], control["accession"], control["sic_matched"]) == (22, "f-1", "3572")
    control = rw.pick_control(CASE, rw.latest_candidate(CASE), lambda url: listing,
                              histories.__getitem__, avoid={22})
    assert control["cik"] == 11
    # a report filed before the company's earnings 8-K of the quarter has no
    # release to read, so the filer is passed over, under every code
    histories[11] = NEEDS + [_row("e-1", "10-Q", "2017-10-20")]
    assert rw.pick_control(CASE, rw.latest_candidate(CASE), lambda url: listing,
                           histories.__getitem__, avoid={22}) is None


def test_a_label_is_letters_only_and_unique():
    taken: set[str] = set()
    assert rw.label_of("Super Micro Computer, Inc.", taken) == "SUPERMICROCO"
    assert rw.label_of("Super Micro Computer Two", taken) == "SUPERMICROCB"
    assert rw.label_of("3D Systems Corp", taken) == "DSYSTEMSCORP"
    assert all(not any(ch.isdigit() for ch in label) for label in taken)


def _analysis(*anomalies, dropped=()):
    return {"anomalies": [{"id": f"{area}_{n}", "area": area, "numbers_vs_prose": outcome,
                           "name_ko": "이름"} for n, (area, outcome) in enumerate(anomalies)],
            "areas": {area: {"dropped": "reason"} for area in dropped}}


def test_a_run_is_flagged_only_by_a_contradiction_in_a_named_area():
    areas = rw.areas_for(CASE)
    assert areas == ("estimates_and_reserves", "revenue_recognition")
    read = rw.read_run(_analysis(("revenue_recognition", "unresolved"),
                                 ("cost_deferral", "contradicts"),
                                 ("estimates_and_reserves", "confirms")), areas)
    assert (read["flagged"], read["questioned"], read["contradicts"],
            read["questioned_count"]) == (False, True, 0, 1)
    read = rw.read_run(_analysis(("estimates_and_reserves", "contradicts"),
                                 ("revenue_recognition", "confirms"),
                                 dropped=("revenue_recognition",)), areas)
    assert (read["flagged"], read["questioned"], read["contradicts"],
            read["questioned_count"]) == (True, True, 1, 1)
    assert read["areas_dropped_by_the_gate"] == ["revenue_recognition"]
    assert rw.read_run(None, areas) == {"finished": False}


def test_the_score_counts_cases_controls_pairs_and_what_did_not_finish(tmp_path):
    runs = [{"role": "case", "pair": "4000", "label": "PLANTED", "cik": 1234567,
             "company": "Planted Devices Inc.", "accession": "a", "form": "10-Q",
             "filing_date": "2017-11-08", "period_end": "2017-09-30"},
            {"role": "control", "pair": "4000", "label": "OTHER", "cik": 22,
             "company": "Other", "accession": "b", "form": "10-Q",
             "filing_date": "2017-11-10", "period_end": "2017-09-30"},
            {"role": "case", "pair": "4001", "label": "NEVER", "cik": 9,
             "company": "Never Ran", "accession": "c", "form": "10-K",
             "filing_date": "2016-03-01", "period_end": "2015-12-31"}]
    for row, analysis in ((runs[0], _analysis(("revenue_recognition", "contradicts"),
                                              ("revenue_recognition", "unresolved"))),
                          (runs[1], _analysis(("revenue_recognition", "unresolved")))):
        folder = rw.run_dir(tmp_path, row)
        folder.mkdir(parents=True)
        (folder / "analysis_accounting.json").write_text(json.dumps(analysis))
    cases = [CASE, dict(CASE, aaer_number="4001", cik=9)]
    result = rw.score(tmp_path, cases, runs, {1234567: {"remembers_a_problem": True}})
    assert result["cases"] == {"finished": 1, "flagged": 1, "questioned": 1}
    assert result["controls"] == {"finished": 1, "flagged": 0, "questioned": 1}
    assert result["cases_the_model_remembered"] == {"finished": 1, "flagged": 1, "questioned": 1}
    assert result["cases_the_model_did_not_remember"] == {"finished": 0, "flagged": 0,
                                                          "questioned": 0}
    # the case questioned twice in the named areas, its control once
    assert (result["pairs_case_questioned_more"], result["pairs_equal"],
            result["pairs_control_questioned_more"]) == (1, 0, 0)
    assert result["not_finished"] == ["case NEVER c"]
