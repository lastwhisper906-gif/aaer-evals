"""The one gate every document passes through on its way into an extractor.

Carried over from `archive/pipeline/cutoff_guard.py`. What is carried is the
rule and its shape — one gateway function, the exception pair, `doc_date ==
cutoff_date` allowed, fail-closed on a missing, unparseable or unrecorded date.
The archived file's *mechanism* does not survive the move: it resolved a filing
date by looking an accession up in a bulk submissions cache under
`~/aaer-data/{ticker}/edgar/`, keyed by a case registry
(`data/candidates/candidates.json`, `TRUSTED_CASE_FILES`, `case_id`). None of
that exists in this project. Here the documents are the committed fixtures and
the record of what each one is and when it was filed is
`tests/fixtures/{ticker}/manifest.json`, so that is what the date is read from.
Nothing under `archive/` is modified.

**Fail closed.** A document whose path is not recorded in a fixture manifest,
or whose recorded filing date is missing or unparseable, is refused — it does
not fall back to "probably fine". An absent date is not an early date.

`doc_date == cutoff_date` is allowed: the cutoff is the filing date of the
report that triggered the run, and that report is itself an input.

Every other module in `src/` reads its documents through `load_document` /
`load_bytes`. `tests/test_cutoff_guard.py` walks `src/*.py` and fails on any
module that opens a fixture or a bundle behind the gate's back.
"""

from __future__ import annotations

import datetime as dt
import gzip
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
FIXTURES = REPO_ROOT / "tests" / "fixtures"


class CutoffGuardError(Exception):
    """The gate could not establish that a document is allowed. Always fail-closed."""


class CutoffViolationError(CutoffGuardError):
    """The document was filed after the cutoff. The run is invalid, not filtered."""

    def __init__(self, path, doc_date: dt.date, cutoff_date: dt.date):
        self.path = str(path)
        self.doc_date = doc_date
        self.cutoff_date = cutoff_date
        super().__init__(
            f"look-ahead violation: {self.path} was filed {doc_date}, "
            f"after the cutoff {cutoff_date}"
        )


def parse_date(value, field: str = "date") -> dt.date:
    """An ISO date, or a refusal. Never None, never a silent default."""
    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value
    if value is None or (isinstance(value, str) and not value.strip()):
        raise CutoffGuardError(f"{field} is missing — a document with no date is refused")
    try:
        return dt.date.fromisoformat(str(value).strip())
    except ValueError as exc:
        raise CutoffGuardError(
            f"{field}={value!r} is not an ISO date — refused rather than guessed"
        ) from exc


def _manifests(fixtures_root: Path) -> list[tuple[str, dict]]:
    root = Path(fixtures_root)
    found = []
    for manifest_path in sorted(root.glob("*/manifest.json")):
        found.append((manifest_path.parent.name,
                      json.loads(manifest_path.read_text(encoding="utf-8"))))
    return found


def _index(fixtures_root: Path) -> dict[Path, dict]:
    """Every recorded document path → its manifest row, with the ticker attached."""
    index: dict[Path, dict] = {}
    for ticker, manifest in _manifests(fixtures_root):
        ticker_dir = Path(fixtures_root) / ticker
        for entry in manifest.get("documents", []):
            row = dict(entry)
            row["ticker"] = ticker
            row["as_of"] = manifest.get("as_of")
            index[(ticker_dir / entry["path"]).resolve()] = row
    return index


def document_record(path, *, fixtures_root=FIXTURES) -> dict:
    """The manifest row for a document, or a refusal if nobody recorded it."""
    resolved = Path(path).resolve()
    row = _index(Path(fixtures_root)).get(resolved)
    if row is None:
        raise CutoffGuardError(
            f"{resolved} is not recorded in any fixture manifest under "
            f"{Path(fixtures_root)} — refused, because an unrecorded document has no "
            "filing date to check"
        )
    return row


def documents(ticker: str, *, form: str | None = None, role: str | None = None,
              fixtures_root=FIXTURES) -> list[dict]:
    """Manifest rows for one company, each carrying an absolute `full_path`."""
    ticker_dir = Path(fixtures_root) / ticker
    manifest_path = ticker_dir / "manifest.json"
    if not manifest_path.is_file():
        raise CutoffGuardError(f"{manifest_path} does not exist — no record for {ticker}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    rows = []
    for entry in manifest.get("documents", []):
        if form is not None and entry.get("form") != form:
            continue
        if role is not None and entry.get("role") != role:
            continue
        row = dict(entry)
        row["ticker"] = ticker
        row["as_of"] = manifest.get("as_of")
        row["full_path"] = ticker_dir / entry["path"]
        rows.append(row)
    return rows


def one_document(ticker: str, form: str, role: str, *, fixtures_root=FIXTURES) -> dict:
    rows = documents(ticker, form=form, role=role, fixtures_root=fixtures_root)
    if len(rows) != 1:
        raise CutoffGuardError(
            f"{ticker} {form} {role}: expected exactly one recorded document, found {len(rows)}"
        )
    return rows[0]


def default_cutoff(ticker: str, *, fixtures_root=FIXTURES) -> dt.date:
    """The fixture set's own as-of date, used when a run does not name a cutoff."""
    manifest_path = Path(fixtures_root) / ticker / "manifest.json"
    if not manifest_path.is_file():
        raise CutoffGuardError(f"{manifest_path} does not exist — no cutoff for {ticker}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    return parse_date(manifest.get("as_of"), f"{ticker} manifest as_of")


def check(path, cutoff_date, *, fixtures_root=FIXTURES) -> dict:
    """Refuse the document, or return its manifest row. No I/O on the document."""
    cutoff = parse_date(cutoff_date, "cutoff_date")
    row = document_record(path, fixtures_root=fixtures_root)
    filed = parse_date(row.get("filing_date"),
                       f"{row.get('ticker', '?')} {row.get('path', path)} filing_date")
    if filed > cutoff:
        raise CutoffViolationError(path, filed, cutoff)
    return row


def load_bytes(path, cutoff_date, *, fixtures_root=FIXTURES) -> bytes:
    """The document's raw bytes as EDGAR served them, gate first."""
    row = check(path, cutoff_date, fixtures_root=fixtures_root)
    data = Path(path).read_bytes()
    return gzip.decompress(data) if row.get("stored") == "gzip" else data


def load_document(path, cutoff_date, *, fixtures_root=FIXTURES, encoding="utf-8") -> str:
    """The gateway every extractor calls. Text of a fixture document, gate first."""
    return load_bytes(path, cutoff_date, fixtures_root=fixtures_root).decode(encoding)


def load_index(path, *, fixtures_root=FIXTURES) -> bytes:
    """The submissions index, which is a list of filings and not a filing.

    The date gate does not apply and must not: the index is EDGAR's catalogue of
    what a company has filed, fetched once at the fixture set's as-of date, so
    its own recorded date is always the newest date in the set and gating it
    would make every earlier cutoff unusable. The cutoff still applies — to the
    *rows*, which is where the look-ahead actually lives, and the caller has to
    do that filtering. `src/parse_8k.py` is the only caller and
    `tests/test_parse_8k.py` asserts it drops every row past the cutoff.

    The path is still checked against the manifest, so an unrecorded file is
    refused here exactly as it is anywhere else.
    """
    row = document_record(path, fixtures_root=fixtures_root)
    if row.get("role") != "submissions_index":
        raise CutoffGuardError(
            f"{path} is a {row.get('role')}, not a submissions index — "
            "only the index of filings skips the date gate")
    data = Path(path).read_bytes()
    return gzip.decompress(data) if row.get("stored") == "gzip" else data


def prior_runs(root, ticker: str) -> list[Path]:
    """Run directories already published for this company, oldest first.

    Reading the published record goes through this module like everything else,
    so the bypass scan stays a true statement. A root that does not exist is not
    an error: the first run for a company has no predecessors.
    """
    folder = Path(root) / ticker
    if not folder.is_dir():
        return []
    return sorted(child for child in folder.iterdir() if child.is_dir())


def bundle_files(bundle_root, pattern: str) -> list[str]:
    """The names in one run directory matching a glob, sorted. Names only —
    reading them is still `load_bundle_file`, so there is one reader."""
    folder = Path(bundle_root)
    if not folder.is_dir():
        return []
    return sorted(path.name for path in folder.glob(pattern) if path.is_file())


def load_bundle_file(bundle_root, name: str) -> str:
    """Read one file out of an assembled run bundle.

    No date gate here on purpose: a bundle's cutoff is checked against its own
    `input_manifest.json` by `src/extraction_checks.py`, and that check has to be
    able to *report* a violation as a failed gate rather than die inside the
    reader. Routing bundle reads through this function is what keeps
    `extraction_checks` honest about the bypass scan.
    """
    path = Path(bundle_root) / name
    if not path.is_file():
        raise CutoffGuardError(f"{path} is not in the bundle")
    return path.read_text(encoding="utf-8")
