"""A run on demand: the store fetched from a planted EDGAR is the committed one.

The planted EDGAR serves NVIDIA's committed fixture store at the addresses its
manifest records: every document's own bytes, the submissions index rebuilt in
EDGAR's columnar shape from the committed rows (each acceptance stamp turned
back to the universal time the index writes), a directory listing per filing
from the manifest's file names, a submission header naming the 8-K's
exhibit, and the committed companyfacts record in EDGAR's shape. The expected values are the
sha256 the committed manifest recorded when each document was fetched from
EDGAR itself, so nothing here is read off the code under test.
"""

from __future__ import annotations

import datetime as dt
import gzip
import json
import urllib.parse
import urllib.request
from pathlib import Path

import pytest

from src import edgar_client, fetch_fixtures, on_demand
from tests.planted_edgar import DIRECT, SAMPLE_CONTACT, serve

FIXTURES = Path(__file__).resolve().parent / "fixtures"
TICKER = "NVDA"
CIK = "0001045810"
ACCESSION = "0001045810-26-000075"        # the 10-Q filed 2026-08-26
MANIFEST = json.loads((FIXTURES / TICKER / "manifest.json").read_text(encoding="utf-8"))
FILING_ROLES = {"primary_html", "xbrl_instance", "exhibit_99_1", "prior_period",
                "prior_period_xbrl_instance"}


def stored_bytes(entry: dict) -> bytes:
    raw = (FIXTURES / TICKER / entry["path"]).read_bytes()
    return gzip.decompress(raw) if entry["stored"] == "gzip" else raw


def utc(stamp: str | None) -> str | None:
    """The committed Eastern stamp back in the index's own shape."""
    if not stamp:
        return None
    instant = dt.datetime.fromisoformat(stamp).astimezone(dt.timezone.utc)
    return instant.strftime("%Y-%m-%dT%H:%M:%S.000Z")


def raw_index() -> bytes:
    rows = json.loads((FIXTURES / TICKER / "submissions.json").read_text())["filings"]
    stamps = {entry["accession"]: entry.get("acceptance_datetime")
              for entry in MANIFEST["documents"] if entry.get("accession")}
    recent = {"accessionNumber": [], "filingDate": [], "reportDate": [], "form": [],
              "items": [], "primaryDocument": [], "primaryDocDescription": [],
              "isXBRL": [], "acceptanceDateTime": []}
    for row in rows:
        recent["accessionNumber"].append(row["accession"])
        recent["filingDate"].append(row["filing_date"])
        recent["reportDate"].append(row["report_date"])
        recent["form"].append(row["form"])
        recent["items"].append(row["items"])
        recent["primaryDocument"].append(row["primary_document"])
        recent["primaryDocDescription"].append(row["primary_doc_description"])
        recent["isXBRL"].append(1 if row["form"] in ("10-K", "10-Q") else 0)
        recent["acceptanceDateTime"].append(
            utc(row.get("acceptance_datetime") or stamps.get(row["accession"])) or "")
    return json.dumps({"cik": CIK, "filings": {"recent": recent, "files": []}}).encode()


def planted_edgar() -> dict[str, tuple[bytes, str]]:
    """Path on the planted server to (body, encoding)."""
    bodies: dict[str, tuple[bytes, str]] = {}
    by_accession: dict[str, list[dict]] = {}
    for entry in MANIFEST["documents"]:
        if entry["form"] == "submissions":
            continue
        path = urllib.parse.urlsplit(entry["url"]).path
        body = stored_bytes(entry)
        if entry["form"] == "companyfacts":
            # back in EDGAR's own shape: the record keeps the entity's name as
            # `entity_name` and the facts as EDGAR wrote them
            record = json.loads(body)
            body = json.dumps({"cik": int(CIK), "entityName": record["entity_name"],
                               "facts": record["facts"]}).encode()
        bodies[path] = (body, "")
        if entry.get("accession"):
            by_accession.setdefault(entry["accession"], []).append(entry)
    for accession, entries in by_accession.items():
        folder = f"/Archives/edgar/data/{int(CIK)}/{accession.replace('-', '')}/"
        names = sorted({urllib.parse.urlsplit(e["url"]).path.rsplit("/", 1)[1] for e in entries})
        bodies[folder + "index.json"] = (json.dumps(
            {"directory": {"item": [{"name": n} for n in names]}}).encode(), "")
        types = {"primary_html": entries[0]["form"], "exhibit_99_1": "EX-99.1"}
        header = "".join(f"<TYPE>{types.get(e['role'], 'EX-99')}\n<FILENAME>"
                         f"{urllib.parse.urlsplit(e['url']).path.rsplit('/', 1)[1]}\n"
                         for e in entries if e["role"] in types)
        bodies[folder + f"{accession}-index-headers.html"] = (header.encode(), "")
    bodies[f"/submissions/CIK{CIK}.json"] = (raw_index(), "")
    return bodies


def rewriting(opener, base: str):
    """The client's opener, with EDGAR's two hosts answered by the planted server."""
    def open_(request, timeout):
        parts = urllib.parse.urlsplit(request.full_url)
        moved = urllib.request.Request(base + parts.path, headers=dict(request.header_items()))
        return opener(moved, timeout=timeout)
    return open_


@pytest.fixture
def server():
    for planted in serve(default=None):
        planted.bodies.update(planted_edgar())
        yield planted


def client(tmp_path, server):
    return edgar_client.EdgarClient(
        environ={"EDGAR_USER_AGENT": SAMPLE_CONTACT, "AAER_CACHE": str(tmp_path / "cache")},
        opener=rewriting(DIRECT, server.url), sleep=lambda seconds: None)


def test_the_store_fetched_on_demand_holds_the_documents_edgar_served(tmp_path, server):
    held = on_demand.fetch_store(client(tmp_path, server), TICKER, accession=ACCESSION)
    assert (held["cik"], held["cik_from"], held["form"], held["filing_date"],
            held["period_end"]) == (CIK, "universe.json", "10-Q", "2026-08-26", "2026-07-26")
    fetched = fetch_fixtures.load_manifest(held["store"] / TICKER)["documents"]
    got = {(e["form"], e["role"], e["accession"]): e["sha256"] for e in fetched
           if e["role"] in FILING_ROLES}
    expected = {(e["form"], e["role"], e["accession"]): e["sha256"]
                for e in MANIFEST["documents"] if e["role"] in FILING_ROLES}
    assert got == expected
    assert held["store"] == tmp_path / "cache" / "stores" / f"{TICKER}-{ACCESSION}"


def test_nothing_filed_after_the_filing_is_in_the_store(tmp_path, server):
    held = on_demand.fetch_store(client(tmp_path, server), TICKER, accession=ACCESSION)
    manifest = fetch_fixtures.load_manifest(held["store"] / TICKER)
    assert manifest["as_of"] == "2026-08-26"
    assert all(e["filing_date"] <= "2026-08-26" for e in manifest["documents"])
    index = json.loads((held["store"] / TICKER / "submissions.json").read_text())
    assert max(row["filing_date"] for row in index["filings"]) <= "2026-08-26"
    facts = json.loads(gzip.decompress(
        (held["store"] / TICKER / "companyfacts.json.gz").read_bytes()))
    assert max(row["filed"] for concepts in facts["facts"].values()
               for concept in concepts.values() for rows in concept["units"].values()
               for row in rows) <= "2026-08-26"


def test_the_latest_filing_of_the_form_is_the_default(tmp_path, server):
    held = on_demand.fetch_store(client(tmp_path, server), TICKER, form="10-Q")
    # the committed index's newest 10-Q, read by eye in tests/fixtures/NVDA/submissions.json
    assert held["accession"] == ACCESSION


def test_a_store_already_fetched_is_used_as_it_is(tmp_path, server):
    fetcher = client(tmp_path, server)
    on_demand.fetch_store(fetcher, TICKER, accession=ACCESSION)
    before = sum(server.hits.values())
    on_demand.fetch_store(fetcher, TICKER, accession=ACCESSION)
    # the second time, the submissions index alone, to know which filing is asked for
    assert sum(server.hits.values()) - before == 1
    assert server.hits[f"/submissions/CIK{CIK}.json"] == 2


def test_a_store_whose_bytes_changed_is_refused(tmp_path, server):
    fetcher = client(tmp_path, server)
    held = on_demand.fetch_store(fetcher, TICKER, accession=ACCESSION)
    instance = held["store"] / TICKER / "10-Q" / "nvda-20260726_htm.xml"
    instance.write_bytes(instance.read_bytes() + b" ")
    with pytest.raises(on_demand.OnDemandError, match="changed"):
        on_demand.fetch_store(fetcher, TICKER, accession=ACCESSION)


def test_a_ticker_outside_the_universe_is_found_in_edgars_map(tmp_path, server):
    server.bodies["/files/company_tickers.json"] = (json.dumps({
        "0": {"cik_str": 789019, "ticker": "MSFT", "title": "MICROSOFT CORP"},
        "1": {"cik_str": 1045810, "ticker": "NVDA", "title": "NVIDIA CORP"}}).encode(), "")
    fetcher = client(tmp_path, server)
    assert on_demand.cik_of(fetcher, "msft") == ("0000789019", on_demand.TICKER_MAP)
    assert on_demand.cik_of(fetcher, "NVDA") == (CIK, "universe.json")
    with pytest.raises(on_demand.OnDemandError, match="names 0 registrants"):
        on_demand.cik_of(fetcher, "NOPE")


def test_an_accession_that_is_not_a_quarterly_or_annual_report_is_refused(tmp_path, server):
    with pytest.raises(on_demand.OnDemandError, match="is a 8-K"):
        on_demand.fetch_store(client(tmp_path, server), TICKER,
                              accession="0001045810-26-000073")
    with pytest.raises(on_demand.OnDemandError, match="not in the company's submissions index"):
        on_demand.fetch_store(client(tmp_path, server), TICKER,
                              accession="0001045810-26-999999")


def test_the_bundle_from_the_store_on_demand_is_the_bundle_from_the_committed_one(
        tmp_path, server):
    """What the agents would read: the same prose and the same numbers, whether
    the documents came from the committed store or from EDGAR on demand."""
    from src import assemble_bundle
    held = on_demand.fetch_store(client(tmp_path, server), TICKER, accession=ACCESSION)
    on_demand_run = tmp_path / "runs" / TICKER / ACCESSION
    committed_run = tmp_path / "committed" / "runs" / TICKER / ACCESSION
    for store, run in ((held["store"], on_demand_run), (FIXTURES, committed_run)):
        assemble_bundle.write(assemble_bundle.build(TICKER, "10-Q", accession=ACCESSION,
                                                    fixtures_root=store,
                                                    prior_runs=run.parent.parent), run)
    for name in ("input_notes.md", "input_mdna.md", "input_controls.md", "input_8k.md",
                 "input_numbers.json", "input_trends.json"):
        assert (on_demand_run / name).read_bytes() == (committed_run / name).read_bytes(), name
