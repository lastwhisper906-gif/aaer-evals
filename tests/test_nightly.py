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
    def __init__(self, failing=()):
        self.failing = failing

    def get_json(self, url):
        for cik, rows in PLANTED.items():
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
    monkeypatch.setattr(nightly.fetch_fixtures, "Fetcher",
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
    monkeypatch.setattr(nightly.fetch_fixtures, "Fetcher", lambda _agent: StandIn())
    summary = world["root"] / "history" / "nightly.jsonl"
    code = nightly.main(["--summary", str(summary), "--runs", str(world["root"] / "runs"),
                         "--work", str(world["root"] / "work"), "--since", "2026-09-23",
                         "--ticker", "AAA"])
    assert code == nightly.FAILED
    line = json.loads(summary.read_text().splitlines()[-1])
    assert line["failures"][0].startswith("workflow input: a ticker and an accession")
    assert line["lookups"]["passed"] is True


def test_a_night_that_raises_still_leaves_a_line(world, monkeypatch):
    monkeypatch.setattr(nightly.fetch_fixtures, "Fetcher", lambda _agent: StandIn())

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
def test_an_unreadable_summary_ledger_is_the_nights_failure_line(world, monkeypatch):
    monkeypatch.setattr(nightly.fetch_fixtures, "Fetcher", lambda _agent: StandIn())
    summary = world["root"] / "history" / "nightly.jsonl"
    summary.parent.mkdir(parents=True)
    summary.write_text("{not json\n")
    code = nightly.main(["--summary", str(summary), "--runs", str(world["root"] / "runs"),
                         "--work", str(world["root"] / "work")])
    assert code == nightly.FAILED
    line = json.loads(summary.read_text().splitlines()[-1])
    assert line["failures"][0].startswith("the night crashed: JSONDecodeError")
