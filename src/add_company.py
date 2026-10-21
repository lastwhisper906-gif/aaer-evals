"""Add one company to the universe: everything mechanical in one command, and
the one thing that is not -- the expected values read off the source -- left as
a checklist the command refuses to fill.

    .venv/bin/python -m src.add_company TICKER --as-of 2026-10-21 [--cik 0000723125]

What it does, in order, each step skipped when its result is already there:

1. **The row.** CIK from EDGAR's company-tickers file unless `--cik` names it,
   SIC from the submissions index, `added_on` the as-of date; appended to
   `universe.json`. A ticker already in the universe is refused.
2. **The store.** `src.fetch_fixtures` as of the date, then
   `src.fetch_companyfacts`, into `tests/fixtures/<TICKER>/`.
3. **The headers.** The two latest 10-K submission headers and the Exhibit 21
   documents they name, recorded as the twenty carry them (the hand procedure
   of 2026-10-14, `record_headers`, now here).
4. **The drift baseline.** `expected.json`: the bundle counts of the 10-K and
   the 10-Q built from the committed store, which is what
   `src.extraction_checks` holds the next build to -- the pipeline's own
   counts on purpose, as that file's own note says.
5. **The checklist.** `expected_values.todo.json`: every key the twelve carry,
   with the source kind each one is read from and the independent reader that
   recounts it, and no value. `tests/expected_values.py` refuses a value with
   no source, and the command never writes `expected_values.json`: that file
   is read off the filing, by eye or by a reader that is not the parser, and
   named key by key. The checklist is the list of what to read.

Then it prints the commands that judge the new company -- the per-company
tests, the universe-wide counts -- and the one line `tests/test_universe.py`
still takes by hand, the batch tuple, because that test types its tickers
from the decision that added them and never imports them from the module it
tests. A parser defect the tests find on the new company is recorded as a
strict expected failure, never as an expectation moved toward the parser.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import sys
from pathlib import Path

try:
    from src import assemble_bundle, exhibits, fetch_companyfacts, fetch_fixtures, interpreter_pin
except ImportError:  # invoked as a plain script
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import assemble_bundle, exhibits, fetch_companyfacts, fetch_fixtures, interpreter_pin

REPO = Path(__file__).resolve().parent.parent
UNIVERSE = REPO / "universe.json"
FIXTURES = REPO / "tests" / "fixtures"
TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik}.json"
BASELINE_NOTE = ("the extraction-drift baseline src/extraction_checks.py reads, not an expected "
                 "value and not readable as one. Every count here is the pipeline's own output "
                 "on purpose: \"has this moved since last time?\" is a question you ask of a "
                 "previous run, and a baseline sourced from anywhere else answers a different "
                 "one. The expected values, each naming where it came from, are in "
                 "expected_values.json; where one of them disagrees with the count here, the "
                 "disagreement is a recorded parser defect and the test that holds it says so.")
BASELINE_KEYS = ("controls", "eight_k", "mdna", "note_history", "notes", "paragraphs")
REFERENCE = "AAPL"       # whose expected_values.json names the keys every company carries

# How each expected value is read, by key: the source kind `tests/expected_values.py`
# accepts, and the independent reader that recounts it where one exists. Typed from
# the notes the twelve carry, so the checklist says what to read and with what.
HOW_TO_READ = {
    "auditors_report.10-K.audit_firm": ("read by eye", "the auditor's signature line in the 10-K"),
    "auditors_report.10-K.critical_audit_matters": ("read by eye", "count the matters under the CAM heading"),
    "auditors_report.10-K.paragraphs": ("already judged", "tests/test_split_controls.py::recount"),
    "auditors_report.10-K.the_report_states": ("read by eye", "singular or plural in the report's own sentence"),
    "bundle.10-K.eight_k": ("hand computation", "manifest.json filing dates: the 8-K's release is in the 10-K bundle only when filed on or before it"),
    "bundle.10-Q.eight_k": ("hand computation", "manifest.json filing dates, then exhibit_99_1_blocks_outside_tables less exhibit_99_1_dropped"),
    "cleaner.10-K.tables": ("the filing", "count <table> in the primary document"),
    "cleaner.10-Q.tables": ("the filing", "count <table> in the primary document"),
    "cleaner.8-K.tables": ("the filing", "count <table> in Exhibit 99.1"),
    "cleaner.8-K.tables_already_in_xbrl": ("by construction", "tests/test_clean_text.py::test_the_cleaner_finds_every_table_the_document_holds"),
    "earnings_release.8-K.eight_k_filings_in_the_index": ("already judged", "tests/test_parse_8k.py::test_the_index_is_a_recount_of_the_stored_file"),
    "earnings_release.8-K.exhibit_99_1_blocks_outside_tables": ("the exhibit", "tests/independent_text.py::block_paragraphs"),
    "earnings_release.8-K.exhibit_99_1_dropped": ("read by eye", "the blocks the cleaner drops, each named"),
    "earnings_release.8-K.exhibit_99_1_tables": ("already judged", "tests/test_parse_8k.py::test_the_expected_counts_survive_an_independent_recount"),
    "earnings_release.8-K.held_items": ("the submissions index", "the items field of the stored 8-K"),
    "exhibits.10-K.exhibit_filename": ("read by eye", "the submission header's EX-21 line"),
    "exhibits.10-K.exhibit_type": ("read by eye", "the submission header's EX-21 line"),
    "exhibits.10-K.prior_year_exhibit_filename": ("read by eye", "the prior year's submission header"),
    "exhibits.10-K.prior_year_exhibit_type": ("read by eye", "the prior year's submission header"),
    "item_4_controls.10-Q.paragraphs": ("already judged", "tests/test_split_controls.py::recount"),
    "item_9a.10-K.paragraphs": ("already judged", "tests/test_split_controls.py::recount"),
    "mdna.10-K.ends_before": ("read by eye", "tests/independent_text.py::block_paragraphs, the first words of the heading after MD&A"),
    "mdna.10-K.heading_candidates": ("the filing", "every line reading like the MD&A heading"),
    "mdna.10-K.opens_at": ("read by eye", "tests/independent_text.py::block_paragraphs, the first words of the MD&A heading"),
    "mdna.10-K.paragraphs": ("already judged", "tests/test_split_mdna.py::recount"),
    "mdna.10-Q.ends_before": ("read by eye", "tests/independent_text.py::block_paragraphs"),
    "mdna.10-Q.heading_candidates": ("the filing", "every line reading like the MD&A heading"),
    "mdna.10-Q.opens_at": ("read by eye", "tests/independent_text.py::block_paragraphs"),
    "mdna.10-Q.paragraphs": ("already judged", "tests/test_split_mdna.py::recount"),
    "note_history.10-Q.key_note_tags": ("xbrl instance", "the TextBlock tags of the key notes in the 10-Q instance"),
    "note_history.10-Q.prior_accession": ("the submissions index", "tests/test_fixtures.py"),
    "note_history.10-Q.prior_key_note_tags": ("xbrl instance", "the same tags in the prior period's instance"),
    "notes.10-K.extension_tag_count": ("xbrl instance", "count the filer's own-namespace TextBlock tags"),
    "notes.10-K.textblock_count": ("already judged", "tests/test_extract_notes.py::_count_by_hand"),
    "notes.10-Q.extension_tag_count": ("xbrl instance", "count the filer's own-namespace TextBlock tags"),
    "notes.10-Q.textblock_count": ("already judged", "tests/test_extract_notes.py::_count_by_hand"),
    "numbers.10-K.fact_count": ("already judged", "tests/test_extract_numbers.py::_count_by_hand"),
    "numbers.10-Q.fact_count": ("already judged", "tests/test_extract_numbers.py::_count_by_hand"),
    "prior_period_diff.10-Q.prior_accession": ("the submissions index", "the latest 10-Q before the current one (tests/test_diff_periods.py)"),
    "risk_factors.10-K.ends_before": ("read by eye", "tests/independent_text.py::block_paragraphs"),
    "risk_factors.10-K.opens_at": ("read by eye", "tests/independent_text.py::block_paragraphs"),
    "risk_factors.10-Q.ends_before": ("read by eye", "tests/independent_text.py::block_paragraphs"),
    "risk_factors.10-Q.opens_at": ("read by eye", "tests/independent_text.py::block_paragraphs"),
}


class AddError(Exception):
    """The company cannot be added as asked. Nothing is half-written."""


# --- the row --------------------------------------------------------------------------------

def load_universe(path: Path = UNIVERSE) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def cik_for(fetcher, ticker: str) -> str:
    """The ten-digit CIK EDGAR's company-tickers file gives the ticker."""
    table = json.loads(fetcher.get(TICKERS_URL))
    for row in table.values():
        if str(row.get("ticker", "")).upper() == ticker.upper():
            return f"{int(row['cik_str']):010d}"
    raise AddError(f"{ticker} is not in {TICKERS_URL}; name the CIK with --cik")


def sic_for(fetcher, cik: str) -> str:
    sic = str(json.loads(fetcher.get(SUBMISSIONS_URL.format(cik=cik))).get("sic") or "").strip()
    if len(sic) != 4 or not sic.isdigit():
        raise AddError(f"the submissions index gives CIK {cik} no four-digit SIC ({sic!r})")
    return sic


def refuse_known(document: dict, ticker: str, cik: str | None) -> None:
    """A ticker or CIK already in the universe is refused, before anything is
    fetched, so a company is never in the file twice."""
    for row in document["companies"]:
        if row["ticker"].upper() == ticker.upper():
            raise AddError(f"{ticker} is already in the universe (added {row.get('added_on')})")
        if cik and row["cik"] == cik:
            raise AddError(f"CIK {cik} is already in the universe as {row['ticker']}")


def row_appended(document: dict, ticker: str, cik: str, sic: str, added_on: str) -> dict:
    """The universe document with the row at its end."""
    refuse_known(document, ticker, cik)
    out = dict(document)
    out["companies"] = list(document["companies"]) + [
        {"ticker": ticker.upper(), "cik": cik, "sic": sic, "added_on": added_on}]
    return out


# --- the headers (the hand procedure of 2026-10-14) -------------------------------------------

def record_headers(fetcher, ticker_dir: Path) -> list[dict]:
    """The two latest 10-K submission headers on or before the store's as-of, and
    the Exhibit 21 document each names, stored under the 10-K's accession and
    appended to the manifest as the rows the twenty carry. A row already there
    is left alone. An 8-K carrying item 1.01 is named, its header left to hand."""
    manifest = json.loads((ticker_dir / "manifest.json").read_text(encoding="utf-8"))
    as_of, cik = manifest["as_of"], manifest["cik"]
    filings = json.loads((ticker_dir / "submissions.json").read_text(encoding="utf-8"))["filings"]
    have = {(d["form"], d["role"]) for d in manifest["documents"]}
    tenks = sorted((r for r in filings if r["form"] == "10-K" and r["filing_date"] <= as_of),
                   key=lambda r: (r["filing_date"], r["accession"]), reverse=True)[:2]
    if len(tenks) < 2:
        raise AddError(f"{ticker_dir.name}: fewer than two 10-Ks on or before {as_of} in the index")
    new = []
    for header_role, exhibit_role, filing in (
            ("submission_header", "exhibit_21", tenks[0]),
            ("prior_year_submission_header", "prior_year_exhibit_21", tenks[1])):
        if ("10-K", header_role) in have:
            continue
        acc = filing["accession"]
        nodash = acc.replace("-", "")
        url = exhibits.HEADER_URL.format(cik=int(cik), accession=nodash, dashed=acc)
        raw = fetcher.get(url)
        named = exhibits.named_exhibit(html.unescape(raw.decode("utf-8", "replace")))
        base = {"form": "10-K", "accession": acc, "filing_date": filing["filing_date"],
                "report_date": filing.get("report_date"), "items": filing.get("items") or "",
                "stored": "identity"}
        for role, name, data, link in ((header_role, f"{acc}-index-headers.html", raw, url),):
            path = ticker_dir / "10-K" / acc / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            new.append(dict(base, role=role, url=link, path=str(path.relative_to(ticker_dir)),
                            bytes=len(data), sha256=hashlib.sha256(data).hexdigest()))
        ex_url = exhibits.ARCHIVE_URL.format(cik=int(cik), accession=nodash, name=named["filename"])
        ex_raw = fetcher.get(ex_url)
        ex_path = ticker_dir / "10-K" / acc / named["filename"]
        ex_path.write_bytes(ex_raw)
        new.append(dict(base, role=exhibit_role, url=ex_url,
                        path=str(ex_path.relative_to(ticker_dir)), bytes=len(ex_raw),
                        sha256=hashlib.sha256(ex_raw).hexdigest()))
    eightk = next((d for d in manifest["documents"]
                   if d["form"] == "8-K" and d["role"] == "primary_html"), None)
    if eightk and exhibits.TRIGGER_ITEM in (eightk.get("items") or "").split(","):
        print(f"{ticker_dir.name}: the stored 8-K carries item {exhibits.TRIGGER_ITEM}; its header "
              "and Exhibit 10 are recorded by hand", file=sys.stderr)
    if new:
        manifest["documents"].extend(new)
        (ticker_dir / "manifest.json").write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return new


# --- the baseline and the checklist -------------------------------------------------------

def baseline(counts_by_form: dict[str, dict]) -> dict:
    """`expected.json` from the bundle manifests' counts, the six keys the drift
    check reads and nothing else."""
    return {"_what_this_is": BASELINE_NOTE,
            "bundle": {form: {key: counts[key] for key in BASELINE_KEYS}
                       for form, counts in sorted(counts_by_form.items())}}


def bundle_counts(ticker: str, fixtures_root: Path = FIXTURES) -> dict[str, dict]:
    """Each triggering form's bundle built from the store, its manifest counts."""
    out = {}
    for form in ("10-K", "10-Q"):
        manifest = assemble_bundle.build(ticker, form, fixtures_root=fixtures_root)["manifest"]
        out[form] = dict(manifest["counts"])
    return out


def checklist(keys) -> dict:
    """Every key with how it is read and no value: what a person reads next."""
    out = {}
    for key in keys:
        kind, where = HOW_TO_READ.get(key, ("read by eye", "no reader named; read the source"))
        out[key] = {"value": None, "from": "", "read_as": kind, "with": where}
    return out


def reference_keys(fixtures_root: Path = FIXTURES) -> list[str]:
    return list(json.loads((Path(fixtures_root) / REFERENCE / "expected_values.json")
                           .read_text(encoding="utf-8")))


# --- the command ----------------------------------------------------------------------------

def add(ticker: str, as_of: str, *, cik: str | None = None, fetcher=None,
        universe_path: Path = UNIVERSE, fixtures_root: Path = FIXTURES) -> dict:
    ticker = ticker.upper()
    fetcher = fetcher or fetch_fixtures.Fetcher(fetch_fixtures.DEFAULT_USER_AGENT)
    document = load_universe(universe_path)
    refuse_known(document, ticker, cik)                               # before any fetch
    cik = cik or cik_for(fetcher, ticker)
    sic = sic_for(fetcher, cik)
    document = row_appended(document, ticker, cik, sic, as_of)
    ticker_dir = Path(fixtures_root) / ticker
    _, problems = fetch_fixtures.fetch_company(fetcher, ticker, cik, as_of, Path(fixtures_root))
    if problems:
        raise AddError(f"{ticker}: the store fetch reports: " + "; ".join(problems))
    facts_problems = fetch_companyfacts.fetch_company(fetcher, ticker, as_of, Path(fixtures_root))
    if facts_problems:
        raise AddError(f"{ticker}: companyfacts reports: " + "; ".join(facts_problems))
    headers = record_headers(fetcher, ticker_dir)
    counts = bundle_counts(ticker, fixtures_root)
    (ticker_dir / "expected.json").write_text(
        json.dumps(baseline(counts), indent=2) + "\n", encoding="utf-8")
    todo = ticker_dir / "expected_values.todo.json"
    todo.write_text(json.dumps(checklist(reference_keys(fixtures_root)), indent=2,
                               ensure_ascii=False) + "\n", encoding="utf-8")
    Path(universe_path).write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    return {"ticker": ticker, "cik": cik, "sic": sic, "added_on": as_of,
            "headers_recorded": len(headers), "baseline": counts, "checklist": str(todo)}


def next_steps(record: dict) -> str:
    t = record["ticker"]
    return "\n".join([
        f"{t} is in universe.json (CIK {record['cik']}, SIC {record['sic']}, added {record['added_on']}).",
        f"1. Read the source for every key in {record['checklist']}, write each value with its "
        "`from` note, and save the result as expected_values.json beside it; delete the todo file.",
        f"2. .venv/bin/python -m pytest tests -q -k {t}    # the per-company tests; a failure is a "
        "parser defect to record as a strict xfail, never an expectation moved",
        "3. .venv/bin/python -m pytest tests/test_universe.py tests/test_fetch_companyfacts.py "
        "tests/test_articulation.py tests/test_clean_text.py tests/test_exhibits.py -q    # the "
        "universe-wide counts, derived from universe.json",
        f"4. tests/test_universe.py: add {t!r} to the batch tuple of its decision date, typed from "
        "docs/structure_changes.md, and the tuple to EVERY_ROW.",
    ])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="add one company: row, store, headers, baseline, checklist")
    parser.add_argument("ticker")
    parser.add_argument("--as-of", required=True)
    parser.add_argument("--cik", default=None)
    parser.add_argument("--fixtures", default=str(FIXTURES))
    parser.add_argument("--universe", default=str(UNIVERSE))
    args = parser.parse_args(argv)
    code = interpreter_pin.enforce()
    if code:
        return code
    try:
        record = add(args.ticker, args.as_of, cik=args.cik, universe_path=Path(args.universe),
                     fixtures_root=Path(args.fixtures))
    except (AddError, assemble_bundle.BundleError, OSError, ValueError) as exc:
        print(f"add_company: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(record, indent=1))
    print(next_steps(record), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
