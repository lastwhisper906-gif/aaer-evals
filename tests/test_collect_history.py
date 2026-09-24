"""Historical collection: scope, order, one line per filing, the four checks.

Every EDGAR answer here is planted, or is the committed CIEN record served back
byte for byte. The expected values are read off the planted rows by hand --
which filings are in scope, which come first, what each line says -- and the
one hash a line records is the sha256 of a planted literal, computed here with
`hashlib` rather than read back from the collector.
"""

from __future__ import annotations

import gzip
import hashlib
import json

import pytest

from src import collect_history, fetch_fixtures
from tests.test_assemble_bundle import STORE_HOLDS, _CommittedEdgar


def _page(rows):
    """One page of EDGAR's parallel arrays. A row: (accession, date, form, items, xbrl)."""
    return {"accessionNumber": [r[0] for r in rows], "filingDate": [r[1] for r in rows],
            "reportDate": ["" for _ in rows], "form": [r[2] for r in rows],
            "items": [r[3] for r in rows],
            "primaryDocument": [f"{r[0]}.htm" for r in rows],
            "primaryDocDescription": ["" for _ in rows], "isXBRL": [r[4] for r in rows]}


# AAA's recent list holds only 2020 onward; its first XBRL filing is on the
# older page, so the scope starts there (2011-05-01) and not at the recent
# list's first row. The 2009 10-K predates XBRL and is out.
AAA_RECENT = [("0000000001-20-000005", "2020-02-01", "10-Q", "", 1),
              ("0000000001-20-000004", "2020-01-15", "8-K", "2.02,9.01", 0),
              ("0000000001-20-000003", "2020-01-10", "4", "", 0)]
AAA_OLDER = [("0000000001-12-000002", "2012-03-01", "10-K", "", 1),
             ("0000000001-11-000001", "2011-05-01", "10-Q", "", 1),
             ("0000000001-09-000000", "2009-03-01", "10-K", "", 0)]
# BBB's first XBRL filing is its 2011-08-01 10-Q, so its earnings release of
# 2011-05-01 is out and the one of 2011-08-15 is in.
BBB_RECENT = [("0000000002-11-000003", "2011-08-15", "8-K", "2.02", 0),
              ("0000000002-11-000002", "2011-08-01", "10-Q", "", 1),
              ("0000000002-11-000001", "2011-05-01", "8-K", "2.02", 0)]


class StandIn:
    def __init__(self):
        self.asked = []

    def get_json(self, url):
        self.asked.append(url)
        if url.endswith("CIK0000000001.json"):
            return {"filings": {"recent": _page(AAA_RECENT),
                                "files": [{"name": "CIK0000000001-submissions-001.json"}]}}
        if url.endswith("CIK0000000001-submissions-001.json"):
            return _page(AAA_OLDER)
        if url.endswith("CIK0000000002.json"):
            return {"filings": {"recent": _page(BBB_RECENT)}}
        raise AssertionError(url)

    def get(self, url):
        self.asked.append(url)
        return b"primary " + url.rsplit("/", 1)[1].encode()


COMPANIES = ({"ticker": "AAA", "cik": "0000000001"}, {"ticker": "BBB", "cik": "0000000002"})


@pytest.fixture
def no_extract(monkeypatch):
    seen = []

    def stand_in(fetcher, company, filing, filings, *, work, history_root):
        seen.append((company["ticker"], filing["accessionNumber"], len(filings)))
        return {"result": "passed", "stage": None, "reason": None,
                "checks": {"schema": "pass", "paragraph_counts": "pass",
                           "cutoff": "pass", "text_blocks": "pass"},
                "bundle": None, "bundle_gzip_bytes": None}
    monkeypatch.setattr(collect_history, "extract", stand_in)
    return seen


def test_every_filing_reads_the_older_pages_too():
    rows = fetch_fixtures.every_filing(StandIn(), "0000000001")
    assert [r["accessionNumber"] for r in rows] == [r[0] for r in AAA_RECENT + AAA_OLDER]
    assert rows[3]["isXBRL"] == 1


def test_scope_starts_at_the_first_xbrl_filing():
    rows = fetch_fixtures.every_filing(StandIn(), "0000000001")
    assert sorted(r["accessionNumber"] for r in collect_history.in_scope(rows)) == [
        "0000000001-11-000001", "0000000001-12-000002",
        "0000000001-20-000004", "0000000001-20-000005"]


def test_oldest_first_across_companies_and_one_line_each(tmp_path, no_extract):
    summary = collect_history.collect(StandIn(), companies=COMPANIES,
                                      history_root=tmp_path, work=tmp_path / "w", batch=3)
    # AAA's 2011-05-01, BBB's 2011-08-01, BBB's 2011-08-15: three, and only the
    # two quarterly reports go through extract.
    assert [(t, a) for t, a, _ in no_extract] == [("AAA", "0000000001-11-000001"),
                                                  ("BBB", "0000000002-11-000002")]
    aaa = [json.loads(l) for l in (tmp_path / "AAA" / "manifest.jsonl").read_text().splitlines()]
    bbb = [json.loads(l) for l in (tmp_path / "BBB" / "manifest.jsonl").read_text().splitlines()]
    assert [l["accession"] for l in aaa] == ["0000000001-11-000001"]
    assert [l["accession"] for l in bbb] == ["0000000002-11-000002", "0000000002-11-000003"]
    # The 8-K is recorded with its hash and no checks.
    earnings = bbb[1]
    assert earnings["result"] == "not_applicable" and earnings["checks"] is None
    assert earnings["url"] == ("https://www.sec.gov/Archives/edgar/data/2/"
                               "000000000211000003/0000000002-11-000003.htm")
    assert earnings["sha256"] == hashlib.sha256(b"primary 0000000002-11-000003.htm").hexdigest()
    # AAA has four in scope and BBB two; three collected, three to go.
    assert (summary["in_scope"], summary["collected"], summary["remaining"]) == (6, 3, 3)
    assert summary["passed"] == 2 and summary["not_checkable_tonight"] == 1


def test_a_filing_on_record_is_not_collected_again(tmp_path, no_extract):
    collect_history.collect(StandIn(), companies=COMPANIES, history_root=tmp_path,
                            work=tmp_path / "w", batch=3)
    first = (tmp_path / "AAA" / "manifest.jsonl").read_text()
    summary = collect_history.collect(StandIn(), companies=COMPANIES,
                                      history_root=tmp_path, work=tmp_path / "w", batch=30)
    # The rest: AAA's 2012 10-K, its 2020 8-K and 10-Q, oldest first.
    assert [a for _, a, _ in no_extract][2:] == ["0000000001-12-000002",
                                                 "0000000001-20-000005"]
    assert (tmp_path / "AAA" / "manifest.jsonl").read_text().startswith(first)
    assert (summary["collected"], summary["remaining"]) == (6, 0)


def test_a_company_whose_index_cannot_be_listed_is_named(tmp_path, no_extract):
    class Failing(StandIn):
        def get_json(self, url):
            if "0000000002" in url:
                raise OSError("tunnel refused")
            return super().get_json(url)
    summary = collect_history.collect(Failing(), companies=COMPANIES,
                                      history_root=tmp_path, work=tmp_path / "w", batch=30)
    assert summary["listing_failures"] == [
        "BBB: the submissions index could not be listed: OSError: tunnel refused"]


def test_the_four_gates_are_read_off_the_lines_the_checks_print():
    lines = ["schema: pass — nine files", "paragraph counts: FAIL — notes is 3",
             "paragraph counts: FAIL — mdna is 4", "cutoff: pass — 0 violations",
             "notes: pass — 12 TextBlock sections"]
    assert collect_history.checks_from(lines) == {
        "schema": "pass", "paragraph_counts": "fail", "cutoff": "pass",
        "text_blocks": "pass"}


def test_a_past_quarter_is_carried_through_extract_and_its_bundle_kept(tmp_path, monkeypatch):
    """The real store, assembler and checks, against EDGAR as the CIEN record has it.

    The quarter is the one filed 2026-06-04, the latest the committed store
    holds, so its counts are the ones `expected.json` records and all four
    checks are expected to pass. Its accession and date are the record's own
    index row.
    """
    monkeypatch.setattr(fetch_fixtures, "MIN_SECONDS_BETWEEN_REQUESTS", 0)
    edgar = _CommittedEdgar()
    filings = fetch_fixtures.recent_filings(edgar, "0000936395")
    filing = next(f for f in filings if f["accessionNumber"] == STORE_HOLDS[0])
    assert filing["filingDate"] == STORE_HOLDS[1]
    out = collect_history.extract(edgar, {"ticker": "CIEN", "cik": "0000936395"}, filing,
                                  filings, work=tmp_path / "work", history_root=tmp_path / "h")
    assert out["result"] == "passed", out
    assert out["checks"] == {"schema": "pass", "paragraph_counts": "pass",
                             "cutoff": "pass", "text_blocks": "pass"}
    folder = tmp_path / "h" / "CIEN" / STORE_HOLDS[0]
    manifest = json.loads(gzip.decompress((folder / "input_manifest.json.gz").read_bytes()))
    assert (manifest["accession"], manifest["filing_date"]) == STORE_HOLDS
    assert out["bundle_gzip_bytes"] == sum(p.stat().st_size for p in folder.iterdir())
    # The store and the unpacked bundle are scratch, and are gone.
    assert not (tmp_path / "work" / "store").exists() or not any(
        (tmp_path / "work" / "store").iterdir())


def test_a_403_is_backed_off_before_it_is_believed(monkeypatch):
    """EDGAR answers a client over its rate with 403; three are waited out."""
    import urllib.error
    answers = [403, 403, None]
    waited = []

    class Response:
        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

        def read(self):
            return b"served"

    def urlopen(request, timeout):
        code = answers.pop(0)
        if code:
            raise urllib.error.HTTPError(request.full_url, code, "Forbidden", {}, None)
        return Response()

    monkeypatch.setattr(fetch_fixtures.urllib.request, "urlopen", urlopen)
    monkeypatch.setattr(fetch_fixtures.time, "sleep", waited.append)
    assert fetch_fixtures.Fetcher("test agent test@example.invalid").get(
        "https://data.sec.gov/x") == b"served"
    assert [w for w in waited if w >= 1] == [1, 2]
