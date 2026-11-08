"""EDGAR as `tests/fixtures/event_filings/record.json` recorded it, and a store to fetch into.

The documents under `tests/fixtures/event_filings/` were fetched from
www.sec.gov on 2026-10-28 through `src/edgar_client.py`, each kept byte for byte
with its address and sha256 in `record.json`. `RecordedEdgar` serves them at
those addresses and refuses every other one, so a store fetched through it
cannot reach past what the record holds, and it lists every address it was
asked for, so a test can say what the store looked at.

The index rows are the committed fixture stores' own (`tests/fixtures/{ticker}/
submissions.json`, EDGAR's submissions index as fetched for the twelve and the
twenty-four), turned back into the index's shape here with nothing from `src/`.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
from pathlib import Path

FIXTURES = Path(__file__).resolve().parent / "fixtures"
EVENT_FIXTURES = FIXTURES / "event_filings"
RECORD = json.loads((EVENT_FIXTURES / "record.json").read_text(encoding="utf-8"))


class RecordedEdgar:
    """Serves the recorded documents at their EDGAR addresses, and nothing else."""

    def __init__(self) -> None:
        self.files = {entry["url"]: (EVENT_FIXTURES / key, entry["sha256"])
                      for key, entry in RECORD["files"].items()}
        self.asked: list[str] = []

    def get(self, url: str) -> bytes:
        self.asked.append(url)
        if url not in self.files:
            raise AssertionError(f"not on record: {url}")
        path, recorded = self.files[url]
        data = path.read_bytes()
        assert hashlib.sha256(data).hexdigest() == recorded, f"{path} is not the record"
        return data

    def get_json(self, url: str):
        raise AssertionError(f"not on record: {url}")


def recorded(accession: str, name: str) -> bytes:
    """One recorded document's bytes, for a test to read by eye."""
    return (EVENT_FIXTURES / accession / name).read_bytes()


def utc(stamp: str | None) -> str | None:
    """A committed Eastern stamp back in the index's own universal-time shape."""
    if not stamp:
        return None
    instant = dt.datetime.fromisoformat(stamp).astimezone(dt.timezone.utc)
    return instant.strftime("%Y-%m-%dT%H:%M:%S.000Z")


def index_rows(ticker: str) -> list[dict]:
    """A committed store's index rows in EDGAR's shape."""
    rows = json.loads((FIXTURES / ticker / "submissions.json").read_text(
        encoding="utf-8"))["filings"]
    return [{"accessionNumber": row["accession"], "filingDate": row["filing_date"],
             "reportDate": row.get("report_date") or "", "form": row["form"],
             "items": row.get("items") or "", "primaryDocument": row.get("primary_document"),
             "primaryDocDescription": row.get("primary_doc_description") or "",
             "acceptanceDateTime": utc(row.get("acceptance_datetime"))} for row in rows]


def row_of(ticker: str, accession: str) -> dict:
    return next(row for row in index_rows(ticker) if row["accessionNumber"] == accession)


def as_trigger(ticker: str, accession: str) -> dict:
    """The triggering report as a store's manifest row names it."""
    rows = json.loads((FIXTURES / ticker / "submissions.json").read_text(
        encoding="utf-8"))["filings"]
    row = next(one for one in rows if one["accession"] == accession)
    return {"form": row["form"], "role": "primary_html", "accession": row["accession"],
            "filing_date": row["filing_date"],
            "acceptance_datetime": row.get("acceptance_datetime")}


def store_up_to(tmp_path: Path, ticker: str, accession: str, known_rows: list[dict]) -> Path:
    """A store holding the index as it stood at the trigger, and nothing else yet:
    what `fetch_fixtures.fetch_event_filings` fetches into. Written here, the
    way `src/fetch_fixtures.py` writes the index row of a manifest."""
    from src import fetch_fixtures
    trigger = row_of(ticker, accession)
    root = tmp_path / f"store-{accession}"
    (root / ticker).mkdir(parents=True)
    cik = json.loads((FIXTURES / ticker / "manifest.json").read_text())["cik"]
    record, raw = fetch_fixtures.submissions_record(ticker, cik, trigger["filingDate"],
                                                    known_rows)
    (root / ticker / "submissions.json").write_bytes(raw)
    manifest = {"ticker": ticker, "cik": cik, "as_of": trigger["filingDate"],
                "source": "EDGAR", "documents": [{
                    "form": "submissions", "role": "submissions_index", "accession": "",
                    "filing_date": record["filings"][0]["filing_date"], "report_date": "",
                    "items": "", "url": record["url"], "path": "submissions.json",
                    "stored": "identity", "bytes": len(raw),
                    "sha256": hashlib.sha256(raw).hexdigest()}]}
    (root / ticker / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return root


def cik_of(ticker: str) -> str:
    return json.loads((FIXTURES / ticker / "manifest.json").read_text())["cik"]


def fetched(tmp_path: Path, ticker: str, accession: str, edgar: RecordedEdgar | None = None,
            extra_rows: list[dict] | None = None):
    """The window of `accession` fetched into a new store from the record:
    (the store root, the problems, the recorded EDGAR it asked). `extra_rows`
    are planted index rows, in EDGAR's shape, beside the committed ones."""
    from src import fetch_fixtures
    rows = index_rows(ticker) + list(extra_rows or [])
    trigger = row_of(ticker, accession)
    known = fetch_fixtures.known_at(rows, trigger)
    root = store_up_to(tmp_path, ticker, accession, known)
    edgar = edgar or RecordedEdgar()
    problems = fetch_fixtures.fetch_event_filings(edgar, ticker, cik_of(ticker), trigger,
                                                  root, known)
    return root, problems, edgar


def manifest_rows(root: Path, ticker: str) -> list[dict]:
    return json.loads((root / ticker / "manifest.json").read_text())["documents"]


def section(root: Path, ticker: str, accession: str) -> tuple[dict, str]:
    """The window as the bundle reads it, and the lines `input_8k.md` ends with."""
    from src import parse_8k
    trigger = as_trigger(ticker, accession)
    events = parse_8k.event_filings(ticker, cutoff=trigger["filing_date"],
                                    fixtures_root=root, trigger=trigger)
    return events, "\n".join(parse_8k.render_event_filings(events))
