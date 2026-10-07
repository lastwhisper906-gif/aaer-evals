"""The night: detect, extract each new filing, check it, one summary line.

Every EDGAR answer here is planted, and every expected value is read off the
planted rows by hand: which filing is new, which is extracted, which is only
named, and what the summary line says failed. Nothing is fetched and nothing
here was produced by running the night.
"""

from __future__ import annotations

import datetime as dt
import json
import subprocess
import urllib.error

import pytest

from src import nightly

TODAY = dt.date(2026, 9, 24)


def _company(ticker: str, cik: str) -> dict:
    return {"ticker": ticker, "cik": cik, "sic": "3661", "added_on": "2026-09-01"}


def _index(rows):
    return {"filings": {"recent": {
        "accessionNumber": [r[0] for r in rows], "filingDate": [r[1] for r in rows],
        "reportDate": ["" for _ in rows], "form": [r[2] for r in rows],
        "items": [r[3] for r in rows], "primaryDocument": ["x.htm" for _ in rows],
        "primaryDocDescription": ["" for _ in rows]}}}


PLANTED = {
    "0000000001": [("0000000001-26-000002", "2026-09-23", "10-Q", ""),
                   ("0000000001-26-000001", "2026-09-23", "8-K", "2.02,9.01"),
                   ("0000000001-26-000000", "2026-06-01", "10-Q", "")],
    "0000000002": [],
}


class StandIn:
    def __init__(self, failing=(), planted=PLANTED):
        self.failing = failing
        self.planted = planted

    def get_json(self, url):
        for cik, rows in self.planted.items():
            if f"CIK{cik}.json" in url:
                if cik in self.failing:
                    raise urllib.error.HTTPError(url, 503, "Unavailable", {}, None)
                return _index(rows)
        raise AssertionError(url)


@pytest.fixture
def world(tmp_path, monkeypatch):
    path = tmp_path / "universe.json"
    path.write_text(json.dumps({"companies": [_company("AAA", "0000000001"),
                                              _company("BBB", "0000000002")]}))
    monkeypatch.setattr(nightly.universe, "PATH", path)
    # `main` hands the night the process's own environment. A shell that holds
    # the real credential would otherwise send every test through `main` to the
    # source; a test that wants a token sets its stand-in.
    monkeypatch.delenv("TIINGO_TOKEN", raising=False)
    monkeypatch.delenv("PRICE_BACKEND", raising=False)
    extracted = []

    def stand_in_extract(filing, *, work, runs_root, fixtures):
        extracted.append((filing["ticker"], filing["form"], filing["accession"],
                          filing["filing_date"]))
        return {"ticker": filing["ticker"], "form": filing["form"],
                "accession": filing["accession"], "filing_date": filing["filing_date"],
                "result": "passed", "stage": None, "reason": None, "checks": []}

    monkeypatch.setattr(nightly, "extract", stand_in_extract)
    return {"root": tmp_path, "universe": path, "extracted": extracted}


def _night(world, **kwargs):
    return nightly.night(since="2026-09-23", runs_root=world["root"] / "runs",
                         work=world["root"] / "work", fixtures=world["root"],
                         companies=nightly.universe.rows(world["universe"]), today=TODAY,
                         **kwargs)


# A token a test hands in. It stands in for the secret and is asserted never
# to reach any file the night writes or any line it prints.
STAND_IN_TOKEN = "stand-in-token"


def _everything_written(root) -> str:
    return "".join(path.read_text(errors="replace")
                   for path in root.rglob("*") if path.is_file())


def test_since_is_the_last_night_whose_lookups_all_passed(tmp_path):
    ledger = tmp_path / "nightly.jsonl"
    ledger.write_text(
        json.dumps({"date": "2026-09-20", "lookups": {"passed": True}}) + "\n"
        + json.dumps({"date": "2026-09-21", "lookups": {"passed": True}}) + "\n"
        + json.dumps({"date": "2026-09-22", "lookups": {"passed": False}}) + "\n")
    assert nightly.since_from(ledger, TODAY) == "2026-09-21"
    assert nightly.since_from(tmp_path / "absent.jsonl", TODAY) == "2026-09-23"


def test_a_new_quarterly_report_is_extracted_and_an_earnings_release_is_named(world):
    line = _night(world, fetcher=StandIn())
    assert world["extracted"] == [("AAA", "10-Q", "0000000001-26-000002", "2026-09-23")]
    assert line["new"] == ["AAA 8-K item 2.02 0000000001-26-000001 filed 2026-09-23",
                           "AAA 10-Q 0000000001-26-000002 filed 2026-09-23"]
    assert line["not_extracted"] == [
        "AAA 8-K item 2.02 0000000001-26-000001: extract builds 10-K and 10-Q bundles only"]
    assert line["lookups"] == {"succeeded": 2, "of": 2, "passed": True}
    assert line["failures"] == []


def test_a_failed_lookup_is_a_failure_in_the_summary(world):
    line = _night(world, fetcher=StandIn(failing=("0000000002",)))
    assert line["lookups"] == {"succeeded": 1, "of": 2, "passed": False}
    assert len(line["failures"]) == 1
    assert line["failures"][0].startswith("detect filing: BBB lookup failed: HTTPError")


def test_an_accession_that_does_not_exist_is_a_named_failure(world):
    line = _night(world, fetcher=StandIn(), hand=("AAA", "0000000001-26-999999"))
    planted = [record for record in line["extractions"] if record.get("named_by_hand")]
    assert [(r["result"], r["stage"]) for r in planted] == [("failed", "detect filing")]
    assert any("0000000001-26-999999 is not in the EDGAR submissions index" in failure
               for failure in line["failures"])


def test_a_filing_named_by_hand_is_extracted_even_when_not_new(world):
    line = _night(world, fetcher=StandIn(), hand=("AAA", "0000000001-26-000000"))
    assert ("AAA", "10-Q", "0000000001-26-000000", "2026-06-01") in world["extracted"]
    assert line["failures"] == []


def _fake_steps(monkeypatch, checks_exit, checks_err=""):
    def step(name, argv):
        if name == "extract":
            out = argv[argv.index("--out") + 1]
            from pathlib import Path
            Path(out).mkdir(parents=True)
            (Path(out) / "input_manifest.json").write_text("{}\n")
        return {"step": name, "exit": 0, "reason": None, "stdout": ""}

    monkeypatch.setattr(nightly, "step", step)
    monkeypatch.setattr(nightly.subprocess, "run", lambda *a, **k:
                        subprocess.CompletedProcess(a, checks_exit, "", checks_err))


FILING = {"ticker": "AAA", "form": "10-Q", "accession": "0000000001-26-000002",
          "filing_date": "2026-09-23"}


def test_a_bundle_that_passes_the_four_checks_lands_in_runs(tmp_path, monkeypatch):
    _fake_steps(monkeypatch, 0)
    record = nightly.extract(FILING, work=tmp_path / "work", runs_root=tmp_path / "runs",
                             fixtures=tmp_path)
    assert record["result"] == "passed"
    assert (tmp_path / "runs" / "AAA" / "0000000001-26-000002" / "input_manifest.json").is_file()


def test_a_bundle_that_fails_a_check_is_not_committed(tmp_path, monkeypatch):
    _fake_steps(monkeypatch, 1, "paragraph counts: FAIL — notes is 3, outside ±20%\n")
    record = nightly.extract(FILING, work=tmp_path / "work", runs_root=tmp_path / "runs",
                             fixtures=tmp_path)
    assert (record["result"], record["stage"]) == ("failed", "extraction checks")
    assert "paragraph counts: FAIL" in record["reason"]
    # The run and the company folder the assembler made for it are both gone.
    assert not (tmp_path / "runs" / "AAA").exists()


def test_a_run_already_on_record_is_never_overwritten(tmp_path, monkeypatch):
    _fake_steps(monkeypatch, 0)
    held = tmp_path / "runs" / "AAA" / "0000000001-26-000002"
    held.mkdir(parents=True)
    record = nightly.extract(FILING, work=tmp_path / "work", runs_root=tmp_path / "runs",
                             fixtures=tmp_path)
    assert record["result"] == "failed" and "append-only" in record["reason"]
    assert list(held.iterdir()) == []


def test_main_appends_one_line_and_exits_one_on_a_failure(world, monkeypatch):
    monkeypatch.setattr(nightly.collect_history, "CachingFetcher",
                        lambda _agent: StandIn(failing=("0000000002",)))
    summary = world["root"] / "history" / "nightly.jsonl"
    code = nightly.main(["--summary", str(summary), "--runs", str(world["root"] / "runs"),
                         "--work", str(world["root"] / "work"), "--since", "2026-09-23"])
    assert code == nightly.FAILED
    lines = summary.read_text().splitlines()
    assert len(lines) == 1
    assert json.loads(lines[0])["lookups"]["succeeded"] == 1


def test_a_failed_extraction_is_tried_again_on_later_nights(world, tmp_path):
    ledger = tmp_path / "nightly.jsonl"
    failed = {"ticker": "AAA", "form": "10-Q", "accession": "0000000001-26-000000",
              "filing_date": "2026-06-01", "result": "failed", "stage": "fetch filings",
              "reason": "HTTPError 503"}
    earnings = dict(failed, form="8-K", accession="0000000001-26-000001")
    ledger.write_text(json.dumps({"date": "2026-09-22", "extractions": [failed, earnings]})
                      + "\n" + json.dumps({"date": "2026-09-23", "extractions": [failed]})
                      + "\n")
    retry = nightly.to_retry(ledger)
    # Once, however many nights recorded it; and only the triggering report.
    assert [(r["accession"], r["filing_date"]) for r in retry] == [
        ("0000000001-26-000000", "2026-06-01")]
    line = _night(world, fetcher=StandIn(), retry=retry)
    assert ("AAA", "10-Q", "0000000001-26-000000", "2026-06-01") in world["extracted"]
    assert any(r.get("retried") for r in line["extractions"])


def test_a_failed_extraction_that_has_a_run_now_is_not_tried_again(world):
    (world["root"] / "runs" / "AAA" / "0000000001-26-000000").mkdir(parents=True)
    _night(world, fetcher=StandIn(), retry=[{"ticker": "AAA", "form": "10-Q",
                                            "accession": "0000000001-26-000000",
                                            "filing_date": "2026-06-01"}])
    assert all(e[2] != "0000000001-26-000000" for e in world["extracted"])


def test_an_earnings_release_named_by_hand_is_refused_by_name(world):
    line = _night(world, fetcher=StandIn(), hand=("AAA", "0000000001-26-000001"))
    named = [r for r in line["extractions"] if r.get("named_by_hand")]
    assert [(r["stage"], r["form"]) for r in named] == [("extract", "8-K")]
    assert "not a triggering report" in named[0]["reason"]


def test_a_ticker_outside_the_universe_is_refused_by_name(world):
    line = _night(world, fetcher=StandIn(), hand=("ZZZ", "0000000001-26-000002"))
    assert any("ZZZ is not in the universe" in failure for failure in line["failures"])


def test_a_step_that_fails_names_its_stage_and_leaves_no_run(tmp_path, monkeypatch):
    def step(name, argv):
        if name == "fetch companyfacts":
            return {"step": name, "exit": 2, "reason": "fetch_companyfacts: incomplete",
                    "stdout": ""}
        return {"step": name, "exit": 0, "reason": None, "stdout": ""}
    monkeypatch.setattr(nightly, "step", step)
    record = nightly.extract(FILING, work=tmp_path / "work", runs_root=tmp_path / "runs",
                             fixtures=tmp_path)
    assert (record["stage"], record["reason"]) == ("fetch companyfacts",
                                                   "fetch_companyfacts: incomplete")
    assert not (tmp_path / "runs" / "AAA").exists()


def test_one_half_of_a_named_filing_still_leaves_a_line_saying_so(world, monkeypatch):
    monkeypatch.setattr(nightly.collect_history, "CachingFetcher", lambda _agent: StandIn())
    summary = world["root"] / "history" / "nightly.jsonl"
    code = nightly.main(["--summary", str(summary), "--runs", str(world["root"] / "runs"),
                         "--work", str(world["root"] / "work"), "--since", "2026-09-23",
                         "--ticker", "AAA"])
    assert code == nightly.FAILED
    line = json.loads(summary.read_text().splitlines()[-1])
    assert line["failures"][0].startswith("workflow input: a ticker and an accession")
    assert line["lookups"]["passed"] is True


def test_a_night_that_raises_still_leaves_a_line(world, monkeypatch):
    monkeypatch.setattr(nightly.collect_history, "CachingFetcher", lambda _agent: StandIn())

    def boom(**_):
        raise RuntimeError("disk full")
    monkeypatch.setattr(nightly, "night", boom)
    summary = world["root"] / "history" / "nightly.jsonl"
    code = nightly.main(["--summary", str(summary), "--runs", str(world["root"] / "runs"),
                         "--work", str(world["root"] / "work"), "--since", "2026-09-23"])
    assert code == nightly.FAILED
    line = json.loads(summary.read_text())
    assert line["failures"] == ["the night crashed: RuntimeError: disk full"]
    assert line["lookups"]["passed"] is False


def test_the_night_carries_historical_progress_and_a_listing_failure(world, monkeypatch):
    asked = []

    def stand_in_collect(fetcher, *, companies, history_root, work, batch):
        asked.append((tuple(c["ticker"] for c in companies), batch))
        return {"batch": batch, "collected_tonight": 2, "passed_tonight": 1,
                "failed_tonight": ["AAA 10-Q 0000000001-11-000001 filed 2011-05-01: "
                                   "fetch filings: no XBRL instance"],
                "not_checkable_tonight": 0, "in_scope": 40, "collected": 2,
                "passed": 1, "remaining": 38,
                "listing_failures": ["BBB: the submissions index could not be listed"]}

    monkeypatch.setattr(nightly.collect_history, "collect", stand_in_collect)
    line = nightly.with_history(_night(world, fetcher=StandIn()), StandIn(),
                                history_root=world["root"] / "history",
                                work=world["root"] / "work", batch=30,
                                companies=nightly.universe.rows(world["universe"]))
    assert asked == [(("AAA", "BBB"), 30)]
    assert line["history"]["collected"] == 2
    # A past filing failing its checks is data, counted in `history`; a company
    # whose index could not be listed is a failure of the night.
    assert line["failures"] == [
        "historical collection: BBB: the submissions index could not be listed"]


def test_no_history_batch_collects_nothing(world, monkeypatch):
    monkeypatch.setattr(nightly.collect_history, "collect",
                        lambda *a, **k: pytest.fail("collected with a batch of 0"))
    line = nightly.with_history(_night(world, fetcher=StandIn()), StandIn(),
                                history_root=world["root"] / "history",
                                work=world["root"] / "work", batch=0)
    assert line["history"] is None


def test_a_history_crash_keeps_the_nights_own_results(world, monkeypatch):
    def boom(*a, **k):
        raise ValueError("a manifest line is not JSON")
    monkeypatch.setattr(nightly.collect_history, "collect", boom)
    night = _night(world, fetcher=StandIn())
    line = nightly.with_history(night, StandIn(), history_root=world["root"] / "history",
                                work=world["root"] / "work", batch=30,
                                companies=nightly.universe.rows(world["universe"]))
    assert line["extractions"] == night["extractions"] and line["lookups"]["passed"]
    assert line["failures"] == [
        "historical collection crashed: ValueError: a manifest line is not JSON"]


def test_an_unreadable_summary_ledger_is_the_nights_failure_line(world, monkeypatch):
    monkeypatch.setattr(nightly.collect_history, "CachingFetcher", lambda _agent: StandIn())
    summary = world["root"] / "history" / "nightly.jsonl"
    summary.parent.mkdir(parents=True)
    summary.write_text("{not json\n")
    code = nightly.main(["--summary", str(summary), "--runs", str(world["root"] / "runs"),
                         "--work", str(world["root"] / "work")])
    assert code == nightly.FAILED
    line = json.loads(summary.read_text().splitlines()[-1])
    assert line["failures"][0].startswith("the night crashed: JSONDecodeError")


# --- newest first --------------------------------------------------------------

# CCC's index, in the order EDGAR might list it, not by date: two filings of
# 2026-09-23 (the 10-K's accession is the later one), one of 09-22, one of
# 09-21. Read off these rows by hand, newest first means 09-23's 000012, then
# 09-23's 000011, then 09-22, then 09-21, and a retried filing of 2026-06-01
# goes last.
CCC = {"0000000003": [("0000000003-26-000010", "2026-09-22", "10-Q", ""),
                      ("0000000003-26-000012", "2026-09-23", "10-K", ""),
                      ("0000000003-26-000011", "2026-09-23", "10-Q", ""),
                      ("0000000003-26-000009", "2026-09-21", "10-Q", "")]}


def test_new_filings_are_extracted_newest_first(world):
    path = world["root"] / "ccc.json"
    path.write_text(json.dumps({"companies": [_company("CCC", "0000000003")]}))
    retry = [{"ticker": "CCC", "form": "10-Q", "accession": "0000000003-26-000000",
              "filing_date": "2026-06-01"}]
    line = nightly.night(fetcher=StandIn(planted=CCC), since="2026-09-21",
                         runs_root=world["root"] / "runs", work=world["root"] / "work",
                         fixtures=world["root"], companies=nightly.universe.rows(path),
                         today=TODAY, retry=retry)
    assert [(a, d) for _, _, a, d in world["extracted"]] == [
        ("0000000003-26-000012", "2026-09-23"), ("0000000003-26-000011", "2026-09-23"),
        ("0000000003-26-000010", "2026-09-22"), ("0000000003-26-000009", "2026-09-21"),
        ("0000000003-26-000000", "2026-06-01")]
    assert [r["accession"] for r in line["extractions"]] == [a for _, _, a, _ in
                                                              world["extracted"]]
    # The order is the rows', not the index's: the same rows listed oldest
    # first come out the same way.
    reversed_index = {"0000000003": list(reversed(CCC["0000000003"]))}
    world["extracted"].clear()
    nightly.night(fetcher=StandIn(planted=reversed_index), since="2026-09-21",
                  runs_root=world["root"] / "runs2", work=world["root"] / "work",
                  fixtures=world["root"], companies=nightly.universe.rows(path),
                  today=TODAY)
    assert [a for _, _, a, _ in world["extracted"]] == [
        "0000000003-26-000012", "0000000003-26-000011", "0000000003-26-000010",
        "0000000003-26-000009"]


# --- the price folder ----------------------------------------------------------

# The window for a filing of 2026-09-23, by hand: 400 days back is 365 days to
# 2025-09-23 (no leap day between them) and 35 more to 2025-08-19, because
# 2025-08-23 to 2025-09-23 is 31 days and four more days land on the 19th.
WINDOW = (dt.date(2025, 8, 19), dt.date(2026, 9, 23))

# The three series, read off `src/sic_to_sector_etf_map_v0.1.json` by hand:
# its `broad_market_series` is SPY, and the planted companies' SIC 3661 falls in
# division D, Manufacturing, 2000 to 3999, whose `sector_etf` is XLI.
SYMBOLS = ["AAA", "SPY", "XLI"]

# What a stand-in source answers: a record in the shape `market.fetch_prices`
# returns, written here by hand and never produced by a fetch.
FETCH_RECORD = {"backend": "tiingo", "fetched_at": "2026-09-24T07:05:00+00:00",
                "asked_for": {"start": "2025-08-19", "end": "2026-09-23"},
                "served": {symbol: {"rows": 275, "first_day": "2025-08-19",
                                    "last_day": "2026-09-23"} for symbol in SYMBOLS}}


def test_the_price_window_is_the_400_days_before_the_filing_date():
    assert nightly.price_window("2026-09-23") == WINDOW
    assert nightly.price_window("2026-09-22") == (dt.date(2025, 8, 18), dt.date(2026, 9, 22))


def test_the_series_are_the_ones_the_market_table_reads_off_the_map():
    # The map's division D, Manufacturing, 2000 to 3999, is XLI; its division K,
    # Nonclassifiable Establishments, 9900 to 9999, is SPY, the broad market's
    # own series, which is asked for once.
    assert nightly.price_series("AAA", "3661") == {"symbols": ["AAA", "SPY", "XLI"],
                                                   "reason": None}
    assert nightly.price_series("AAA", "9995") == {"symbols": ["AAA", "SPY"], "reason": None}


def test_a_sic_the_map_leaves_unclassified_is_the_runs_reason_and_no_fetch(tmp_path):
    def never(**_):
        pytest.fail("the source was asked for a company with no sector series")

    # 1800 to 1999 is one of the classification's unassigned ranges.
    bundle = tmp_path / "runs" / "AAA" / "0000000001-26-000002"
    series = nightly.price_series("AAA", "1850")
    assert series["symbols"] is None
    out = nightly.prices_for({"ticker": "AAA", "filing_date": "2026-09-23"}, series=series,
                             bundle=bundle, environ={"TIINGO_TOKEN": STAND_IN_TOKEN},
                             fetch=never)
    assert (out["folder"], out["record"]) == (None, None)
    assert out["reason"].startswith("MarketError: SIC 1850 falls in none of the "
                                    "classification's divisions")
    assert json.loads((bundle / "price_fetch.json").read_text()) == {
        "fetched": False, "reason": out["reason"]}
    assert STAND_IN_TOKEN not in _everything_written(tmp_path)


def test_a_passed_extraction_gets_its_price_folder_from_the_environment_handed_in(world):
    asked = []
    environ = {"TIINGO_TOKEN": STAND_IN_TOKEN}

    def stand_in_fetch(**kwargs):
        asked.append(kwargs)
        return dict(FETCH_RECORD)

    line = _night(world, fetcher=StandIn(), environ=environ, fetch_prices=stand_in_fetch)
    bundle = world["root"] / "runs" / "AAA" / "0000000001-26-000002"
    assert asked == [{"symbols": SYMBOLS, "start": WINDOW[0], "end": WINDOW[1],
                      "into": bundle / "prices", "environ": environ, "backend": "tiingo"}]
    assert asked[0]["environ"] is environ
    record = line["extractions"][0]["prices"]
    assert record == {"folder": str(bundle / "prices"),
                      "record": str(bundle / "price_fetch.json"), "reason": None}
    assert json.loads((bundle / "price_fetch.json").read_text()) == FETCH_RECORD
    assert line["failures"] == []
    # The token is read, never written: not in the line, not in any file.
    assert STAND_IN_TOKEN not in json.dumps(line)
    assert STAND_IN_TOKEN not in _everything_written(world["root"])


def test_no_token_means_no_price_series_by_name_and_no_fetch(world):
    def never(**_):
        pytest.fail("the source was asked with no token")

    line = _night(world, fetcher=StandIn(), environ={}, fetch_prices=never)
    record = line["extractions"][0]["prices"]
    assert record == {"folder": None, "record": None,
                      "reason": "no price series: TIINGO_TOKEN unset"}
    bundle = world["root"] / "runs" / "AAA" / "0000000001-26-000002"
    assert json.loads((bundle / "price_fetch.json").read_text()) == {
        "fetched": False, "reason": "no price series: TIINGO_TOKEN unset"}
    assert not (bundle / "prices").exists()
    assert line["failures"] == []
    # A blank token is no token, and no environment handed in is the same night.
    _night(world, fetcher=StandIn(), environ={"TIINGO_TOKEN": "  "}, fetch_prices=never)
    _night(world, fetcher=StandIn(), fetch_prices=never)


def test_a_source_that_refuses_leaves_the_extraction_and_names_no_token(world):
    from src import market

    def refusing(**_):
        raise market.MarketError(f"tiingo refused the request carrying {STAND_IN_TOKEN}")

    line = _night(world, fetcher=StandIn(), environ={"TIINGO_TOKEN": STAND_IN_TOKEN},
                  fetch_prices=refusing)
    record = line["extractions"][0]
    assert record["result"] == "passed" and line["failures"] == []
    assert record["prices"] == {"folder": None, "record": None,
                                "reason": "MarketError: tiingo refused the request "
                                          "carrying <TIINGO_TOKEN>"}
    assert STAND_IN_TOKEN not in json.dumps(line)
    assert STAND_IN_TOKEN not in _everything_written(world["root"])


def test_a_failed_extraction_asks_for_no_prices(world, monkeypatch):
    def failing_extract(filing, *, work, runs_root, fixtures):
        return {"ticker": filing["ticker"], "form": filing["form"],
                "accession": filing["accession"], "filing_date": filing["filing_date"],
                "result": "failed", "stage": "fetch filings", "reason": "HTTPError 503",
                "checks": []}

    def never(**_):
        pytest.fail("prices were fetched for a filing with no run")

    monkeypatch.setattr(nightly, "extract", failing_extract)
    line = _night(world, fetcher=StandIn(), environ={"TIINGO_TOKEN": STAND_IN_TOKEN},
                  fetch_prices=never)
    assert "prices" not in line["extractions"][0]
    assert not (world["root"] / "runs").exists()


# --- publish -------------------------------------------------------------------

RUN_URL = "https://example.invalid/actions/runs/1"


class Runner:
    """A stand-in for git and gh: records every command, answers as told."""

    def __init__(self, staged=True, failing=None, stderr="remote: denied", heads=()):
        self.commands = []
        self.staged = staged
        self.failing = failing
        self.stderr = stderr
        self.heads = heads

    def __call__(self, argv):
        self.commands.append(list(argv))
        if self.failing and argv[:len(self.failing)] == list(self.failing):
            return subprocess.CompletedProcess(argv, 1, "", self.stderr)
        if argv[:2] == ["git", "ls-remote"]:
            # `git ls-remote --heads` prints one `<sha>\trefs/heads/<name>` per branch.
            return subprocess.CompletedProcess(
                argv, 0, "".join(f"{'0' * 40}\trefs/heads/{name}\n" for name in self.heads), "")
        if argv[:3] == ["git", "diff", "--cached"]:
            return subprocess.CompletedProcess(argv, 1 if self.staged else 0, "", "")
        if argv[:3] == ["gh", "pr", "create"]:
            return subprocess.CompletedProcess(
                argv, 0, "Creating pull request\nhttps://github.com/o/r/pull/123\n", "")
        return subprocess.CompletedProcess(argv, 0, "", "")


def _pushes_to_main(commands) -> list:
    return [argv for argv in commands if "push" in argv
            and any(part == "main" or part.endswith(":main") for part in argv)]


def test_the_push_to_main_detector_fires_on_a_push_to_main():
    assert _pushes_to_main([["git", "push", "origin", "main"],
                            ["git", "push", "origin", "HEAD:main"],
                            ["git", "push", "-u", "origin", "nightly-2026-09-24"]]) == [
        ["git", "push", "origin", "main"], ["git", "push", "origin", "HEAD:main"]]


def test_publish_commits_on_the_nights_branch_and_opens_an_auto_merging_pull_request(tmp_path):
    (tmp_path / "history").mkdir()
    (tmp_path / "runs").mkdir()
    runner = Runner()
    out = nightly.publish(date="2026-09-24", run_url=RUN_URL, root=tmp_path, runner=runner)
    title = "the nightly crew's night of 2026-09-24"
    assert runner.commands == [
        ["git", "ls-remote", "--heads", "origin"],
        ["git", "checkout", "-b", "nightly-2026-09-24"],
        ["git", "add", "--", "history", "runs"],
        ["git", "diff", "--cached", "--quiet"],
        ["git", "commit", "-q", "-m", f"{title}: detect, extract, check, price, collect\n\n"
                                      f"Run: {RUN_URL}"],
        ["git", "push", "-u", "origin", "nightly-2026-09-24"],
        ["gh", "pr", "create", "--base", "main", "--head", "nightly-2026-09-24",
         "--title", title, "--body", f"Run: {RUN_URL}"],
        ["gh", "pr", "merge", "--auto", "--merge", "nightly-2026-09-24"],
    ]
    assert _pushes_to_main(runner.commands) == []
    assert out == {"branch": "nightly-2026-09-24",
                   "pull_request": "https://github.com/o/r/pull/123",
                   "auto_merge": True, "reason": None}


def test_publish_adds_only_what_the_night_wrote_and_opens_nothing_for_nothing(tmp_path):
    (tmp_path / "history").mkdir()
    runner = Runner(staged=False)
    out = nightly.publish(date="2026-09-24", run_url=None, root=tmp_path, runner=runner)
    assert runner.commands == [["git", "ls-remote", "--heads", "origin"],
                               ["git", "checkout", "-b", "nightly-2026-09-24"],
                               ["git", "add", "--", "history"],
                               ["git", "diff", "--cached", "--quiet"]]
    assert out["pull_request"] is None and out["auto_merge"] is False
    assert out["reason"].startswith("nothing to publish")


def test_publish_names_the_step_that_stopped_it(tmp_path):
    (tmp_path / "history").mkdir()
    runner = Runner(failing=("git", "push"))
    out = nightly.publish(date="2026-09-24", run_url=RUN_URL, root=tmp_path, runner=runner)
    assert out["reason"] == "git push: exit 1: remote: denied"
    assert out["pull_request"] is None and out["auto_merge"] is False
    assert [argv[0] for argv in runner.commands].count("gh") == 0
    assert _pushes_to_main(runner.commands) == []
    # Auto-merge refused after the pull request opened is still a stopped
    # publish: the line would be waiting for a click.
    runner = Runner(failing=("gh", "pr", "merge"), stderr="auto-merge is not allowed")
    out = nightly.publish(date="2026-09-24", run_url=RUN_URL, root=tmp_path, runner=runner)
    assert out["pull_request"] == "https://github.com/o/r/pull/123"
    assert out["auto_merge"] is False
    assert out["reason"] == "gh pr merge --auto: exit 1: auto-merge is not allowed"
    # A remote that cannot be listed stops it before any branch is made.
    runner = Runner(failing=("git", "ls-remote"), stderr="fatal: unable to access")
    out = nightly.publish(date="2026-09-24", run_url=RUN_URL, root=tmp_path, runner=runner)
    assert out["reason"] == "git ls-remote: exit 1: fatal: unable to access"
    assert runner.commands == [["git", "ls-remote", "--heads", "origin"]]


def test_a_second_run_on_one_date_takes_the_next_free_branch(tmp_path):
    (tmp_path / "history").mkdir()
    # The first night's branch is still on the remote: the second takes -2.
    runner = Runner(heads=("main", "nightly-2026-09-24"))
    out = nightly.publish(date="2026-09-24", run_url=RUN_URL, root=tmp_path, runner=runner)
    assert out["branch"] == "nightly-2026-09-24-2" and out["auto_merge"] is True
    assert ["git", "checkout", "-b", "nightly-2026-09-24-2"] in runner.commands
    assert ["git", "push", "-u", "origin", "nightly-2026-09-24-2"] in runner.commands
    assert ["gh", "pr", "merge", "--auto", "--merge", "nightly-2026-09-24-2"] in runner.commands
    # A third takes -3; another date's branch, or one that only begins with
    # this date, takes nothing from it.
    runner = Runner(heads=("nightly-2026-09-24", "nightly-2026-09-24-2", "nightly-2026-09-23"))
    assert nightly.publish(date="2026-09-24", run_url=RUN_URL, root=tmp_path,
                           runner=runner)["branch"] == "nightly-2026-09-24-3"
    runner = Runner(heads=("nightly-2026-09-23", "nightly-2026-09-24-2"))
    assert nightly.publish(date="2026-09-24", run_url=RUN_URL, root=tmp_path,
                           runner=runner)["branch"] == "nightly-2026-09-24"


def test_main_publishes_the_nights_date_only_when_asked(world, monkeypatch):
    monkeypatch.setattr(nightly.collect_history, "CachingFetcher", lambda _agent: StandIn())
    published = []

    def stand_in_publish(*, date, run_url):
        published.append((date, run_url))
        return {"branch": f"nightly-{date}", "pull_request": "https://github.com/o/r/pull/9",
                "auto_merge": True, "reason": None}

    monkeypatch.setattr(nightly, "publish", stand_in_publish)
    summary = world["root"] / "history" / "nightly.jsonl"
    argv = ["--summary", str(summary), "--runs", str(world["root"] / "runs"),
            "--work", str(world["root"] / "work"), "--since", "2026-09-23",
            "--run-url", RUN_URL]
    assert nightly.main(argv) == 0
    assert published == []
    assert nightly.main(argv + ["--publish"]) == 0
    line = json.loads(summary.read_text().splitlines()[-1])
    assert published == [(line["date"], RUN_URL)]
    # A publish that stopped short is the night's failure, named on stderr.
    monkeypatch.setattr(nightly, "publish", lambda *, date, run_url: {
        "branch": f"nightly-{date}", "pull_request": None, "auto_merge": False,
        "reason": "git push: exit 1: remote: denied"})
    assert nightly.main(argv + ["--publish"]) == nightly.FAILED
    monkeypatch.setattr(nightly, "publish", lambda *, date, run_url: {
        "branch": f"nightly-{date}", "pull_request": None, "auto_merge": False,
        "reason": "nothing to publish: the night committed no line and no run"})
    assert nightly.main(argv + ["--publish"]) == 0


def test_main_hands_the_process_environment_to_the_night(world, monkeypatch):
    monkeypatch.setattr(nightly.collect_history, "CachingFetcher", lambda _agent: StandIn())
    seen = []

    def stand_in_night(**kwargs):
        seen.append(kwargs["environ"])
        return {"date": "2026-09-24", "finished_utc": "", "run": None, "since": "2026-09-23",
                "lookups": {"succeeded": 2, "of": 2, "passed": True}, "new": [],
                "not_extracted": [], "extractions": [], "history": None, "failures": []}

    monkeypatch.setattr(nightly, "night", stand_in_night)
    monkeypatch.setenv("TIINGO_TOKEN", STAND_IN_TOKEN)
    summary = world["root"] / "history" / "nightly.jsonl"
    code = nightly.main(["--summary", str(summary), "--runs", str(world["root"] / "runs"),
                         "--work", str(world["root"] / "work"), "--since", "2026-09-23"])
    assert code == 0 and seen == [nightly.os.environ]
    assert STAND_IN_TOKEN not in summary.read_text()


def test_a_token_in_the_process_environment_reaches_no_output_and_no_file(world, monkeypatch,
                                                                         capsys):
    """The whole night through `main`, the token set, a source that echoes it."""
    monkeypatch.setattr(nightly.collect_history, "CachingFetcher", lambda _agent: StandIn())
    monkeypatch.setenv("TIINGO_TOKEN", STAND_IN_TOKEN)
    handed = []

    def echoing(**kwargs):
        handed.append(kwargs["environ"].get("TIINGO_TOKEN"))
        raise nightly.market.MarketError(f"tiingo refused the request carrying {STAND_IN_TOKEN}")

    monkeypatch.setattr(nightly.market, "fetch_prices", echoing)
    monkeypatch.setattr(nightly, "publish", lambda *, date, run_url: {
        "branch": f"nightly-{date}", "pull_request": "https://github.com/o/r/pull/9",
        "auto_merge": True, "reason": None})
    summary = world["root"] / "history" / "nightly.jsonl"
    code = nightly.main(["--summary", str(summary), "--runs", str(world["root"] / "runs"),
                         "--work", str(world["root"] / "work"), "--since", "2026-09-23",
                         "--run-url", RUN_URL, "--publish"])
    assert code == 0
    # The token was read and handed to the source ...
    assert handed == [STAND_IN_TOKEN]
    # ... and what came back is written with the variable's name in its place.
    printed = capsys.readouterr()
    assert "carrying <TIINGO_TOKEN>" in printed.out
    assert STAND_IN_TOKEN not in printed.out + printed.err
    assert STAND_IN_TOKEN not in _everything_written(world["root"])
