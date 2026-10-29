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


@pytest.mark.parametrize("there", ["an empty directory", "a file"])
def test_a_run_directory_that_is_already_there_is_never_claimed(tmp_path, server, monkeypatch,
                                                               there):
    """Claimed by creating it, which one process alone can do: another
    invocation's directory, made a moment before, is refused as a published one is."""
    fetcher = client(tmp_path, server)
    monkeypatch.setattr(on_demand.edgar_client, "EdgarClient", lambda: fetcher)
    taken = tmp_path / "runs" / TICKER / ACCESSION
    taken.parent.mkdir(parents=True)
    if there == "a file":
        taken.write_text("kept\n")
    else:
        taken.mkdir()
    assert on_demand.main(["--ticker", TICKER, "--accession", ACCESSION,
                           "--out", str(taken)]) == on_demand.BAD_INPUT
    assert (taken.read_text() == "kept\n") if there == "a file" else not any(taken.iterdir())


def test_a_run_directory_that_holds_anything_is_never_written_over(tmp_path, server, monkeypatch):
    """`runs/` is append-only: a published run of the same filing stands as it is."""
    fetcher = client(tmp_path, server)
    monkeypatch.setattr(on_demand.edgar_client, "EdgarClient", lambda: fetcher)
    published = tmp_path / "runs" / TICKER / ACCESSION
    published.mkdir(parents=True)
    (published / "input_manifest.json").write_text('{"analysed_utc": "2026-10-08"}\n')
    assert on_demand.main(["--ticker", TICKER, "--accession", ACCESSION,
                           "--out", str(published)]) == on_demand.BAD_INPUT
    assert [p.name for p in published.iterdir()] == ["input_manifest.json"]
    assert (published / "input_manifest.json").read_text() == '{"analysed_utc": "2026-10-08"}\n'


# Planted stamps on the cutoff day, in the index's own universal time: NVIDIA's
# 10-Q at 20:36:00.000Z, EDGAR's stamp for it as the committed index rows in
# tests/fixtures/acceptance_stamp/nvda_submissions_rows.json carry it, and the
# rows the test plants around it.
STAMPS = {ACCESSION: "2026-08-26T20:36:00.000Z"}
ROWS = [
    {"accessionNumber": "a", "filingDate": "2026-08-26", "acceptanceDateTime": "2026-08-26T20:21:00.000Z"},
    {"accessionNumber": "b", "filingDate": "2026-08-26", "acceptanceDateTime": "2026-08-26T20:50:00.000Z"},
    {"accessionNumber": "c", "filingDate": "2026-08-26", "acceptanceDateTime": ""},
    {"accessionNumber": "d", "filingDate": "2026-08-27", "acceptanceDateTime": "2026-08-27T13:00:00.000Z"},
    {"accessionNumber": "e", "filingDate": "2026-08-25", "acceptanceDateTime": "2026-08-25T23:00:00.000Z"},
    # no stamp: the grader's proxy, the filer agent's own sequence
    {"accessionNumber": "0001045810-26-000074", "filingDate": "2026-08-26", "acceptanceDateTime": ""},
    {"accessionNumber": "0001045810-26-000077", "filingDate": "2026-08-26", "acceptanceDateTime": None},
    {"accessionNumber": "0001193125-26-000001", "filingDate": "2026-08-26", "acceptanceDateTime": ""},
]


def test_a_filing_made_later_on_the_triggers_day_is_not_known_at_it():
    """The owner's grader's rule (`accepted_before_trigger`): both stamps, else a
    lower number in the same filer agent's sequence, else not shown, so not kept."""
    trigger = {"accessionNumber": ACCESSION, "filingDate": "2026-08-26",
               "acceptanceDateTime": STAMPS[ACCESSION]}
    kept = [row["accessionNumber"] for row in on_demand.known_at(ROWS, trigger)]
    assert kept == ["a", "e", "0001045810-26-000074"]
    unstamped = dict(trigger, acceptanceDateTime="")
    assert [row["accessionNumber"] for row in on_demand.known_at(ROWS, unstamped)] == \
        ["e", "0001045810-26-000074"]


EARLY, LATE = "0001045810-26-000073", "0001045810-26-000076"


def plant_rows(server, *rows: dict) -> None:
    """Index rows added to the planted index, the newest first as EDGAR lists."""
    index = json.loads(server.bodies[f"/submissions/CIK{CIK}.json"][0])
    recent = index["filings"]["recent"]
    for row in rows:
        for key in recent:
            recent[key].insert(0, row.get(key, ""))
    server.bodies[f"/submissions/CIK{CIK}.json"] = (json.dumps(index).encode(), "")


def plant_the_day(server) -> None:
    """Planted: the release 8-K stamped at 20:21Z, before the 10-Q's 20:36Z, and
    an 8-K with item 5.02 stamped at 21:30Z the same day, after it."""
    index = json.loads(server.bodies[f"/submissions/CIK{CIK}.json"][0])
    recent = index["filings"]["recent"]
    for i, accession in enumerate(recent["accessionNumber"]):
        if accession == ACCESSION:
            recent["acceptanceDateTime"][i] = STAMPS[ACCESSION]
        elif accession == EARLY:
            recent["acceptanceDateTime"][i] = "2026-08-26T20:21:00.000Z"
    server.bodies[f"/submissions/CIK{CIK}.json"] = (json.dumps(index).encode(), "")
    plant_rows(server, {"accessionNumber": LATE, "filingDate": "2026-08-26",
                        "reportDate": "2026-08-26", "form": "8-K", "items": "5.02",
                        "primaryDocument": "nvda-20260826b.htm",
                        "primaryDocDescription": "8-K", "isXBRL": 0,
                        "acceptanceDateTime": "2026-08-26T21:30:00.000Z"})


def stored_facts(store: Path) -> dict:
    return json.loads(gzip.decompress((store / TICKER / "companyfacts.json.gz").read_bytes()))


def test_a_filing_made_later_on_the_triggers_day_never_reaches_the_store(tmp_path, server):
    plant_the_day(server)
    held = on_demand.fetch_store(client(tmp_path, server), TICKER, accession=ACCESSION)
    rows = json.loads((held["store"] / TICKER / "submissions.json").read_text())["filings"]
    accessions = {row["accession"] for row in rows}
    assert LATE not in accessions
    assert EARLY in accessions


def test_a_companyfacts_row_filed_later_on_the_triggers_day_never_reaches_the_store(
        tmp_path, server):
    """Planted: two rows filed 2026-08-26, one by the 8-K accepted before the
    10-Q and one by the 8-K accepted after it. `filed` is a day, so only the
    accession tells them apart."""
    plant_the_day(server)
    path = f"/api/xbrl/companyfacts/CIK{CIK}.json"
    served = json.loads(server.bodies[path][0])
    concept = served["facts"]["us-gaap"]["Revenues"]["units"]["USD"]
    for accession, value in ((EARLY, 2), (LATE, 3)):
        concept.append({"start": "2026-04-27", "end": "2026-07-26", "val": value,
                        "accn": accession, "form": "8-K", "filed": "2026-08-26"})
    server.bodies[path] = (json.dumps(served).encode(), "")
    held = on_demand.fetch_store(client(tmp_path, server), TICKER, accession=ACCESSION)
    kept = {row.get("accn") for row in
            stored_facts(held["store"])["facts"]["us-gaap"]["Revenues"]["units"]["USD"]}
    assert EARLY in kept and ACCESSION in kept
    assert LATE not in kept


def test_a_store_built_under_another_rule_is_refused_not_reused(tmp_path, server, monkeypatch):
    """A store whose index lists the 8-K accepted after the 10-Q, as one built
    before `known_at` existed would, is refused though its bytes are its manifest's."""
    plant_the_day(server)
    fetcher = client(tmp_path, server)
    with monkeypatch.context() as patch:
        patch.setattr(on_demand, "known_at", lambda rows, filing: rows)
        on_demand.fetch_store(fetcher, TICKER, accession=ACCESSION)
    with pytest.raises(on_demand.OnDemandError, match="built under another rule"):
        on_demand.fetch_store(fetcher, TICKER, accession=ACCESSION)


def test_the_company_is_named_as_the_filing_names_it(tmp_path, server):
    """Planted: EDGAR's companyfacts serves a later name. The 10-Q's instance
    states `NVIDIA CORP` (dei:EntityRegistrantName, fact f-6, read by eye)."""
    path = f"/api/xbrl/companyfacts/CIK{CIK}.json"
    served = json.loads(server.bodies[path][0])
    served["entityName"] = "NVIDIA LIQUIDATING TRUST"
    server.bodies[path] = (json.dumps(served).encode(), "")
    held = on_demand.fetch_store(client(tmp_path, server), TICKER, accession=ACCESSION)
    assert stored_facts(held["store"])["entity_name"] == "NVIDIA CORP"


def test_a_report_filed_after_the_filing_is_never_picked_for_the_store(tmp_path, server):
    """Planted: a 10-K filed 2026-09-01, after the 10-Q. The planted EDGAR does
    not serve it, so picking it would fail the fetch."""
    plant_rows(server, {"accessionNumber": "0001045810-26-000090", "filingDate": "2026-09-01",
                        "reportDate": "2026-07-26", "form": "10-K", "items": "",
                        "primaryDocument": "nvda-20260726x10k.htm",
                        "primaryDocDescription": "10-K", "isXBRL": 1,
                        "acceptanceDateTime": "2026-09-01T20:00:00.000Z"})
    held = on_demand.fetch_store(client(tmp_path, server), TICKER, accession=ACCESSION)
    manifest = fetch_fixtures.load_manifest(held["store"] / TICKER)
    assert "0001045810-26-000090" not in {e.get("accession") for e in manifest["documents"]}
    rows = json.loads((held["store"] / TICKER / "submissions.json").read_text())["filings"]
    assert "0001045810-26-000090" not in {row["accession"] for row in rows}


def test_a_companyfacts_row_filed_after_the_filing_never_reaches_the_store(tmp_path, server):
    """Planted: a row of revenue filed 2026-08-31, after the 10-Q of 2026-08-26."""
    path = f"/api/xbrl/companyfacts/CIK{CIK}.json"
    served = json.loads(server.bodies[path][0])
    concept = served["facts"]["us-gaap"]["Revenues"]["units"]["USD"]
    concept.append({"start": "2026-04-27", "end": "2026-07-26", "val": 1, "accn": "x",
                    "form": "10-Q/A", "filed": "2026-08-31"})
    server.bodies[path] = (json.dumps(served).encode(), "")
    held = on_demand.fetch_store(client(tmp_path, server), TICKER, accession=ACCESSION)
    facts = json.loads(gzip.decompress(
        (held["store"] / TICKER / "companyfacts.json.gz").read_bytes()))
    assert not any(row.get("filed") == "2026-08-31" for row in
                   facts["facts"]["us-gaap"]["Revenues"]["units"]["USD"])


def test_edgars_map_must_name_one_registrant(tmp_path, server):
    def plant(rows):
        server.bodies["/files/company_tickers.json"] = (json.dumps(
            {str(i): row for i, row in enumerate(rows)}).encode(), "")
    fetcher = client(tmp_path, server)
    plant([{"cik_str": 789019, "ticker": "MSFT"}, {"cik_str": 789019, "ticker": "msft"}])
    assert on_demand.cik_of(fetcher, "MSFT")[0] == "0000789019"
    plant([{"cik_str": 789019, "ticker": "MSFT"}, {"cik_str": 1, "ticker": "MSFT"}])
    with pytest.raises(on_demand.OnDemandError, match="names 2 registrants"):
        on_demand.cik_of(fetcher, "MSFT")


def test_a_universe_file_that_cannot_be_read_is_refused_not_passed_over(tmp_path, server,
                                                                      monkeypatch):
    def broken(path=None):
        raise on_demand.universe.UniverseError("NVDA is listed twice")
    monkeypatch.setattr(on_demand.universe, "tickers", broken)
    with pytest.raises(on_demand.OnDemandError, match="universe.json cannot be read"):
        on_demand.cik_of(client(tmp_path, server), "NVDA")


def test_the_latest_of_two_reports_of_one_day_is_the_higher_accession():
    rows = [{"accessionNumber": "0001045810-26-000075", "filingDate": "2026-08-26",
             "form": "10-Q"},
            {"accessionNumber": "0001045810-26-000076", "filingDate": "2026-08-26",
             "form": "10-Q"}]
    assert on_demand.the_filing(rows, "10-Q", None)["accessionNumber"] == "0001045810-26-000076"


# --- round three of the refute check: every store held to the rule ----------------------


def test_a_stale_store_cut_short_is_held_to_the_rule_when_finished(tmp_path, server,
                                                                  monkeypatch):
    """A store built under the earlier rule that stopped before companyfacts is
    finished off from what it holds, and the check runs on it all the same."""
    plant_the_day(server)
    fetcher = client(tmp_path, server)
    with monkeypatch.context() as patch:
        patch.setattr(on_demand, "known_at", lambda rows, filing: rows)
        from src import fetch_companyfacts
        patch.setattr(fetch_companyfacts, "fetch_company", lambda *a, **k: ["cut short"])
        with pytest.raises(on_demand.OnDemandError, match="cut short"):
            on_demand.fetch_store(fetcher, TICKER, accession=ACCESSION)
    with pytest.raises(on_demand.OnDemandError, match="built under another rule"):
        on_demand.fetch_store(fetcher, TICKER, accession=ACCESSION)


def plant_late_rows(server) -> None:
    path = f"/api/xbrl/companyfacts/CIK{CIK}.json"
    served = json.loads(server.bodies[path][0])
    served["facts"]["us-gaap"]["Revenues"]["units"]["USD"].append(
        {"start": "2026-04-27", "end": "2026-07-26", "val": 3, "accn": LATE, "form": "8-K",
         "filed": "2026-08-26"})
    server.bodies[path] = (json.dumps(served).encode(), "")


def test_a_whole_store_holding_a_later_companyfacts_row_is_refused(tmp_path, server,
                                                                  monkeypatch):
    plant_the_day(server)
    plant_late_rows(server)
    fetcher = client(tmp_path, server)
    from src import fetch_companyfacts
    real = fetch_companyfacts.within_cutoff
    with monkeypatch.context() as patch:
        patch.setattr(fetch_companyfacts, "within_cutoff",
                      lambda facts, as_of, known=None: real(facts, as_of))
        # the store is held to the rule as it is built, too
        with pytest.raises(on_demand.OnDemandError,
                           match=f"accepted after the trigger: {LATE}"):
            on_demand.fetch_store(fetcher, TICKER, accession=ACCESSION)
    # and, whole now, it is refused rather than reused
    with pytest.raises(on_demand.OnDemandError, match=f"accepted after the trigger: {LATE}"):
        on_demand.fetch_store(fetcher, TICKER, accession=ACCESSION)


def test_a_whole_store_naming_the_company_otherwise_is_refused(tmp_path, server, monkeypatch):
    fetcher = client(tmp_path, server)
    with monkeypatch.context() as patch:
        patch.setattr(fetch_fixtures, "name_as_filed", lambda *a: "NVIDIA LIQUIDATING TRUST")
        on_demand.fetch_store(fetcher, TICKER, accession=ACCESSION)
    with pytest.raises(on_demand.OnDemandError, match="not the name the filing states"):
        on_demand.fetch_store(fetcher, TICKER, accession=ACCESSION)


def test_the_store_keeps_no_frame_and_no_taxonomy_words_of_today(tmp_path, server):
    """The committed record carries frames (`CY2026Q2`-style labels) and each
    concept's label and description, as EDGAR serves them now."""
    served = json.loads(server.bodies[f"/api/xbrl/companyfacts/CIK{CIK}.json"][0])
    assert any("frame" in row for _, _, _, row in fetch_fixtures_rows(served["facts"]))
    held = on_demand.fetch_store(client(tmp_path, server), TICKER, accession=ACCESSION)
    facts = stored_facts(held["store"])["facts"]
    assert not any("frame" in row for _, _, _, row in fetch_fixtures_rows(facts))
    assert not any({"label", "description"} & set(concept) for concepts in facts.values()
                   for concept in concepts.values())


def fetch_fixtures_rows(facts):
    from src import fetch_companyfacts
    return fetch_companyfacts.rows(facts)


def test_the_run_directory_is_claimed_even_against_a_claim_made_a_moment_before(
        tmp_path, server, monkeypatch):
    """Another invocation creates the directory between this one's look and its
    own creation: the creation itself is the claim, so this one is refused."""
    fetcher = client(tmp_path, server)
    monkeypatch.setattr(on_demand.edgar_client, "EdgarClient", lambda: fetcher)
    out = tmp_path / "runs" / TICKER / ACCESSION
    real = Path.mkdir

    def raced(self, *args, **kwargs):
        if self == out and not self.exists():
            real(self)                      # the other invocation, first
            (self / "input_manifest.json").write_text("theirs\n")
        return real(self, *args, **kwargs)

    monkeypatch.setattr(Path, "mkdir", raced)
    assert on_demand.main(["--ticker", TICKER, "--accession", ACCESSION,
                           "--out", str(out)]) == on_demand.BAD_INPUT
    assert (out / "input_manifest.json").read_text() == "theirs\n"
    assert [p.name for p in out.iterdir()] == ["input_manifest.json"]


@pytest.mark.parametrize("failure", ["a status", "an exception"])
def test_a_bundle_that_fails_gives_the_claim_back(tmp_path, server, monkeypatch, failure):
    fetcher = client(tmp_path, server)
    monkeypatch.setattr(on_demand.edgar_client, "EdgarClient", lambda: fetcher)

    def fails(argv):
        if failure == "a status":
            return 2
        raise ValueError("a reader the bundle calls broke")

    monkeypatch.setattr(on_demand.assemble_bundle, "main", fails)
    out = tmp_path / "runs" / TICKER / ACCESSION
    argv = ["--ticker", TICKER, "--accession", ACCESSION, "--out", str(out)]
    if failure == "a status":
        assert on_demand.main(argv) == 2
    else:
        with pytest.raises(ValueError):
            on_demand.main(argv)
    assert not out.exists()


def test_the_same_instant_stood_and_a_stamp_of_another_shape_is_no_stamp():
    trigger = {"accessionNumber": ACCESSION, "filingDate": "2026-08-26",
               "acceptanceDateTime": STAMPS[ACCESSION]}
    same = {"accessionNumber": "0001193125-26-000002", "filingDate": "2026-08-26",
            "acceptanceDateTime": STAMPS[ACCESSION]}
    assert on_demand.stood_before(same, trigger)
    # shapes EDGAR's index does not write are read as no stamp, as the grader
    # reads a stamp it cannot parse: another filer agent's row is then not shown
    for stamp in ("2026-08-26T20:00:00+00:00", "2026-08-26T20:00:00.000",
                  "2026-08-26 20:00:00Z", "2026-08-26"):
        other = dict(same, acceptanceDateTime=stamp)
        assert not on_demand.stood_before(other, trigger), stamp
        assert on_demand.known_at([other], trigger) == []


def test_a_row_dated_earlier_but_accepted_after_the_trigger_is_not_known_at_it():
    """A report accepted after half past five is dated the next day, and a Form 4
    accepted before ten at night that same evening is dated the day it was
    accepted: earlier, though accepted after."""
    trigger = {"accessionNumber": ACCESSION, "filingDate": "2026-08-26",
               "acceptanceDateTime": "2026-08-25T21:45:00.000Z"}
    form4 = {"accessionNumber": "0001127602-26-000001", "filingDate": "2026-08-25",
             "acceptanceDateTime": "2026-08-26T01:30:00.000Z"}
    before = dict(form4, accessionNumber="0001127602-26-000000",
                  acceptanceDateTime="2026-08-25T20:00:00.000Z")
    assert [row["accessionNumber"] for row in on_demand.known_at([form4, before], trigger)] \
        == ["0001127602-26-000000"]


def test_the_command_lines_store_up_to_a_filing_holds_the_same_rule(tmp_path, server,
                                                                    monkeypatch):
    """`python -m src.fetch_fixtures --accession` builds through the same store."""
    plant_the_day(server)
    fetcher = client(tmp_path, server)
    monkeypatch.setattr(fetch_fixtures, "Fetcher", lambda _agent: fetcher)
    out = tmp_path / "store"
    assert fetch_fixtures.main(["--ticker", TICKER, "--accession", ACCESSION,
                                "--out", str(out)]) == 0
    rows = json.loads((out / TICKER / "submissions.json").read_text())["filings"]
    assert LATE not in {row["accession"] for row in rows}
    assert EARLY in {row["accession"] for row in rows}


# --- round four: one stamp reading, every rule checked on reuse, every page read ----------


def test_a_stamp_is_read_as_the_store_writes_it_and_the_grader_compares_it():
    """`eastern_stamp` takes a fraction of one to six digits; a stamp the rule
    read as none, while the store wrote it, let a later release through."""
    trigger = {"accessionNumber": ACCESSION, "filingDate": "2026-08-26",
               "acceptanceDateTime": STAMPS[ACCESSION]}
    later = {"accessionNumber": "0001045810-26-000073", "filingDate": "2026-08-26",
             "acceptanceDateTime": "2026-08-26T20:40:00.5Z"}
    assert not on_demand.stood_before(later, trigger)
    assert on_demand.known_at([later], trigger) == []
    # a stamp of the right shape naming no real day is no stamp, and no crash
    impossible = dict(later, accessionNumber="0001193125-26-000003",
                      acceptanceDateTime="2026-02-30T20:00:00.000Z")
    assert on_demand.known_at([impossible], trigger) == []


def test_a_whole_store_keeping_todays_frames_is_refused(tmp_path, server, monkeypatch):
    fetcher = client(tmp_path, server)
    from src import fetch_companyfacts
    with monkeypatch.context() as patch:
        patch.setattr(fetch_companyfacts, "as_of_the_filing", lambda facts: facts)
        on_demand.fetch_store(fetcher, TICKER, accession=ACCESSION)   # the earlier rule
    with pytest.raises(on_demand.OnDemandError, match="keeps a frame"):
        on_demand.fetch_store(fetcher, TICKER, accession=ACCESSION)


def test_a_whole_store_whose_record_is_dated_after_the_filing_is_refused(tmp_path, server):
    """The rule reads the store through the gate at the filing's date, so a
    record the manifest dates later is refused even where its rows are not."""
    fetcher = client(tmp_path, server)
    held = on_demand.fetch_store(fetcher, TICKER, accession=ACCESSION)
    path = held["store"] / TICKER / "manifest.json"
    manifest = json.loads(path.read_text())
    for entry in manifest["documents"]:
        if entry["form"] == "companyfacts":
            entry["filing_date"] = "2026-08-31"
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    with pytest.raises(on_demand.OnDemandError, match="through the gate"):
        on_demand.fetch_store(fetcher, TICKER, accession=ACCESSION)


OLDER = {"accessionNumber": "0001045810-10-000001", "filingDate": "2010-03-01",
         "reportDate": "2010-03-01", "form": "8-K", "items": "2.02",
         "primaryDocument": "old.htm", "primaryDocDescription": "8-K", "isXBRL": 0,
         "acceptanceDateTime": "2010-03-01T21:00:00.000Z"}


def plant_an_older_page(server) -> None:
    """A row EDGAR keeps on an older page of the index, past the recent list."""
    index = json.loads(server.bodies[f"/submissions/CIK{CIK}.json"][0])
    name = f"CIK{CIK}-submissions-001.json"
    index["filings"]["files"] = [{"name": name}]
    server.bodies[f"/submissions/CIK{CIK}.json"] = (json.dumps(index).encode(), "")
    server.bodies[f"/submissions/{name}"] = (json.dumps(
        {key: [value] for key, value in OLDER.items()}).encode(), "")


@pytest.mark.parametrize("route", ["on demand", "the command line"])
def test_the_store_reads_every_page_of_the_index(tmp_path, server, monkeypatch, route):
    plant_an_older_page(server)
    fetcher = client(tmp_path, server)
    if route == "on demand":
        store = on_demand.fetch_store(fetcher, TICKER, accession=ACCESSION)["store"]
    else:
        monkeypatch.setattr(fetch_fixtures, "Fetcher", lambda _agent: fetcher)
        store = tmp_path / "store"
        assert fetch_fixtures.main(["--ticker", TICKER, "--accession", ACCESSION,
                                    "--out", str(store)]) == 0
    rows = json.loads((store / TICKER / "submissions.json").read_text())["filings"]
    assert OLDER["accessionNumber"] in {row["accession"] for row in rows}


# Apple's 10-Q filed 2016-07-27 (0001628280-16-017809), before inline XBRL: its
# folder listing and the type lines of its submission header, as EDGAR served
# them on 2026-10-28 (read from index.json and the -index-headers.html page).
APPLE_2016_NAMES = ["0001628280-16-017809-index-headers.html", "0001628280-16-017809-index.html",
                    "0001628280-16-017809.txt", "0001628280-16-017809-xbrl.zip",
                    "a10-qexhibit3116252016.htm", "a10-qexhibit3126252016.htm",
                    "a10-qexhibit3216252016.htm", "a10-qq320166252016.htm", "aapl-20160625.xml",
                    "aapl-20160625.xsd", "aapl-20160625_cal.xml", "aapl-20160625_def.xml",
                    "aapl-20160625_lab.xml", "aapl-20160625_pre.xml", "FilingSummary.xml",
                    "Financial_Report.xlsx", "R1.htm", "R2.htm"]
APPLE_2016_HEADER = ("&lt;TYPE&gt;10-Q\n&lt;FILENAME&gt;a10-qq320166252016.htm\n"
                     "&lt;TYPE&gt;EX-31.1\n&lt;FILENAME&gt;a10-qexhibit3116252016.htm\n"
                     "&lt;TYPE&gt;EX-101.INS\n&lt;FILENAME&gt;aapl-20160625.xml\n"
                     "&lt;TYPE&gt;EX-101.SCH\n&lt;FILENAME&gt;aapl-20160625.xsd\n"
                     "&lt;TYPE&gt;EX-101.CAL\n&lt;FILENAME&gt;aapl-20160625_cal.xml\n"
                     "&lt;TYPE&gt;XML\n&lt;FILENAME&gt;R1.htm\n")


def test_a_report_filed_before_inline_xbrl_keeps_its_instance_under_its_own_name():
    filing = {"accessionNumber": "0001628280-16-017809",
              "primaryDocument": "a10-qq320166252016.htm"}
    assert fetch_fixtures.needs_types("10-Q", filing, APPLE_2016_NAMES)
    types = [(kind.upper(), name)
             for kind, name in fetch_fixtures.DOCUMENT_TYPE.findall(APPLE_2016_HEADER)]
    wanted, missing = fetch_fixtures.wanted_documents("10-Q", filing, APPLE_2016_NAMES, types)
    assert wanted == [("primary_html", "a10-qq320166252016.htm"),
                      ("xbrl_instance", "aapl-20160625.xml")]
    assert missing == []
    # without the header's types nothing is guessed from the names
    _, missing = fetch_fixtures.wanted_documents("10-Q", filing, APPLE_2016_NAMES, [])
    assert [role for role, _ in missing] == ["xbrl_instance"]


def test_an_inline_report_needs_no_header_read():
    # NVIDIA's 10-Q of 2026-08-26, as the committed manifest names its documents
    filing = {"accessionNumber": ACCESSION, "primaryDocument": "nvda-20260726.htm"}
    names = ["nvda-20260726.htm", "nvda-20260726_htm.xml"]
    assert not fetch_fixtures.needs_types("10-Q", filing, names)
    assert fetch_fixtures.wanted_documents("10-Q", filing, names, [])[0][1] == (
        "xbrl_instance", "nvda-20260726_htm.xml")


def test_a_cik_names_the_registrant_and_the_ticker_only_the_run(tmp_path, server):
    held = on_demand.fetch_store(client(tmp_path, server), "someone", accession=ACCESSION,
                                 cik="1045810")
    assert (held["ticker"], held["cik"], held["cik_from"]) == ("SOMEONE", CIK, "--cik")
    assert held["store"] == tmp_path / "cache" / "stores" / f"SOMEONE-{ACCESSION}"
    assert server.hits.get("/files/company_tickers.json", 0) == 0
    with pytest.raises(on_demand.OnDemandError, match="not a number"):
        on_demand.fetch_store(client(tmp_path, server), "SOMEONE", accession=ACCESSION,
                              cik="NVDA")


# Axesstel's 10-K for fiscal 2012 (0001193125-13-084624): EDGAR answered 404 for
# its -index-headers.html on 2026-10-29, and its -index.htm carries these rows
# (two of the document table's, two of the data files table's), copied as served.
AXESSTEL_INDEX = """
         <tr>
            <td scope="row">1</td>
            <td scope="row">FORM 10-K</td>
            <td scope="row"><a href="/Archives/edgar/data/1092492/000119312513084624/d445189d10k.htm">d445189d10k.htm</a></td>
            <td scope="row">10-K</td>
            <td scope="row">1234</td>
         </tr>
         <tr class="evenRow">
            <td scope="row">&nbsp;</td>
            <td scope="row">Complete submission text file</td>
            <td scope="row"><a href="/Archives/edgar/data/1092492/000119312513084624/0001193125-13-084624.txt">0001193125-13-084624.txt</a></td>
            <td scope="row">&nbsp;</td>
            <td scope="row">4515635</td>
         </tr>
         <tr>
            <td scope="row">7</td>
            <td scope="row">XBRL INSTANCE DOCUMENT</td>
            <td scope="row"><a href="/Archives/edgar/data/1092492/000119312513084624/axst-20121231.xml">axst-20121231.xml</a></td>
            <td scope="row">EX-101.INS</td>
            <td scope="row">252621</td>
         </tr>
         <tr class="evenRow">
            <td scope="row">8</td>
            <td scope="row">XBRL TAXONOMY EXTENSION SCHEMA</td>
            <td scope="row"><a href="/Archives/edgar/data/1092492/000119312513084624/axst-20121231.xsd">axst-20121231.xsd</a></td>
            <td scope="row">EX-101.SCH</td>
            <td scope="row">1000</td>
         </tr>
"""


class _OldFolder:
    def __init__(self, error):
        self.error, self.asked = error, []

    def get(self, url):
        self.asked.append(url.rsplit("/", 1)[1])
        if url.endswith("-index-headers.html"):
            raise self.error
        return AXESSTEL_INDEX.encode()


def test_a_filing_older_than_its_header_page_is_read_from_its_index_page():
    fetcher = _OldFolder(edgar_client.EdgarError("https://www.sec.gov/...: HTTP 404"))
    types = fetch_fixtures.document_types(fetcher, "0001092492", "0001193125-13-084624")
    assert types == [("10-K", "d445189d10k.htm"), ("EX-101.INS", "axst-20121231.xml"),
                     ("EX-101.SCH", "axst-20121231.xsd")]
    assert fetcher.asked == ["0001193125-13-084624-index-headers.html",
                             "0001193125-13-084624-index.htm"]


def test_a_header_page_that_fails_otherwise_is_not_passed_over():
    fetcher = _OldFolder(edgar_client.EdgarError("https://www.sec.gov/...: HTTP 503"))
    with pytest.raises(edgar_client.EdgarError, match="503"):
        fetch_fixtures.document_types(fetcher, "0001092492", "0001193125-13-084624")
