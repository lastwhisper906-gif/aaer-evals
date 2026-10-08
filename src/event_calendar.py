"""The event calendar: what happened to every EDGAR filer since 2009, as EDGAR recorded it.

The owner's instruction of 2026-09-28: this is the answer key, for the pattern
study and for the forward track. It records events and judges nothing -- which
filer an event is evidence against, and of what, is a question for whoever reads
it. `events/` is append-only, and so is every file here.

| event | what EDGAR recorded | read from |
|---|---|---|
| `non_reliance` | an 8-K or 8-K/A carrying item 4.02 | submissions, filing indexes |
| `auditor_change` | item 4.01 | same |
| `bankruptcy` | item 1.03 | same |
| `delisting_notice` | item 3.01 | same |
| `officer_director_change` | item 5.02 | same |
| `annual_report_amended` | a 10-K/A | same |
| `quarterly_report_amended` | a 10-Q/A | same |
| `staff_comment_letter` | an UPLOAD: the SEC staff's letter, released | same |
| `filer_response_letter` | a CORRESP: the filer's answer, released | same |
| `going_concern_language` | a value in a filing's `txt` table holding "substantial doubt" and "going concern" in one sentence | the notes data sets (`src/fsn.py`) |
| `enforcement_release` | an entry on the SEC's list of accounting and auditing enforcement releases | that list |

**Layout.** `events/calendar/{event}/{year}.jsonl`, the year the filing was
filed (for an enforcement release, the year it was published). One line per
filer and filing: a filing made by two registrants is an event for each, because
each has its own submissions record. Every line names its `source`.
`events/calendar/sources.jsonl` has one line per source read -- the bulk file's
sha256 and size, each quarter's index and what it added, each notes data set --
so a count can be traced to what was read.

**Submissions and the indexes.** The submissions bulk file is every filer's
filing history, with the 8-K item numbers the filer declared. The quarterly form
indexes (`full-index/{year}/QTR{n}/form.gz`) list every filing by form. Every
filing of a form above that an index lists and the bulk file does not is taken
from the index: its form and date come from the index line, and an 8-K's items
from the filing's own SGML header (`{accession}.hdr.sgml`), because the index
does not carry them. Such a line has `source` `full_index` and no acceptance time.
After the bulk file, the calendar is kept up by the daily form indexes
(`daily-index/{year}/QTR{n}/form.{YYYYMMDD}.idx`), read the same way, one
business day at a time from the day after the last one read; those lines have
`source` `daily_index`. The nightly crew runs it.

**Going concern.** Python finds the language and judges nothing. A line says
which tag held it first and how many sentences held it. It does not say whose
going concern the sentence is about, or whether it states a doubt at all: on
the notes data set of January 2026, sentences holding both phrases were a
filer's own doubt ("these conditions raise substantial doubt"), a policy
("the Company has the responsibility to evaluate whether conditions and/or
events raise substantial doubt"), a plan said to alleviate it, and a
counterparty's (a lender writing that a borrower's auditors doubted it), and
no wording rule separated them without a judgment. So that judgment is in
`docs/needs_judgment.md`, and the tag is where to look: the sentences are not
copied into the repository -- they are the filer's text, tens of thousands of
filings of it -- and the notes data set indexed in `src/fsn_index/` holds each
one at the accession and tag the line names.

**Enforcement releases.** The list gives a date, the respondents as the SEC
wrote them, the release numbers and the document; it gives no CIK, so the line
carries none. Tying a respondent's name to a filer is a judgment, and
`docs/needs_judgment.md` holds it. A row naming two accounting and auditing
enforcement releases is a line for each.

**Nothing here the plain-name check reads as a code.** `src/plain_name_check.py`
reads every line of `events/`, and EDGAR's own vocabulary takes the shape it
refuses: the quarter in an index's address, a registration statement's form,
the SEC's other release numbers, and a respondent's name (a company named with
a capital and a digit). None is this project's, and whether the check should
keep them as words is the owner's (`docs/needs_judgment.md`). Until then none is
written: an index read is named by its year and quarter, or its day, and its
address is `FORM_INDEX_URL` or `DAILY_INDEX_URL` filled in; a going-concern line
names its filing by accession and not by form, which the notes data set's `sub`
row holds; and an enforcement line carries the release as a number and the
document, which names the respondents and the other releases.

    python3.12 -m src.event_calendar submissions [--zip PATH]
    python3.12 -m src.event_calendar daily
    python3.12 -m src.event_calendar enforcement
    python3.12 -m src.event_calendar counts

Exit 0 when the source was read and its events appended, 1 when a source could
not be read, 3 the wrong interpreter.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import gzip
import hashlib
import io
import json
import os
import re
import sys
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from zoneinfo import ZoneInfo

try:
    from src import fetch_fixtures, interpreter_pin, universe
except ImportError:  # invoked as a plain script
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import fetch_fixtures, interpreter_pin, universe

REPO_ROOT = Path(__file__).resolve().parent.parent
CALENDAR = REPO_ROOT / "events" / "calendar"
SOURCES = "sources.jsonl"
SINCE = "2009-01-01"
DATA_ROOT = Path.home() / "aaer-data"

SUBMISSIONS_URL = "https://www.sec.gov/Archives/edgar/daily-index/bulkdata/submissions.zip"
FORM_INDEX_URL = "https://www.sec.gov/Archives/edgar/full-index/{year}/QTR{quarter}/form.gz"
HEADER_URL = "https://www.sec.gov/Archives/edgar/data/{cik}/{folder}/{accession}.hdr.sgml"
DAILY_INDEX_URL = ("https://www.sec.gov/Archives/edgar/daily-index/{year}/QTR{quarter}/"
                   "form.{day}.idx")
ENFORCEMENT_URL = ("https://www.sec.gov/enforcement-litigation/"
                   "accounting-auditing-enforcement-releases?page={page}")

ITEMS = {"4.02": "non_reliance", "4.01": "auditor_change", "1.03": "bankruptcy",
         "3.01": "delisting_notice", "5.02": "officer_director_change"}
ITEM_FORMS = ("8-K", "8-K/A")
FORMS = {"10-K/A": "annual_report_amended", "10-Q/A": "quarterly_report_amended",
         "UPLOAD": "staff_comment_letter", "CORRESP": "filer_response_letter"}
WATCHED_FORMS = ITEM_FORMS + tuple(FORMS)
GOING_CONCERN = "going_concern_language"
ENFORCEMENT = "enforcement_release"
EVENTS = tuple(ITEMS.values()) + tuple(FORMS.values()) + (GOING_CONCERN, ENFORCEMENT)

SENTENCE = re.compile(r"(?<=[.;!?])\s+")

EASTERN = ZoneInfo("America/New_York")
FAILED = 1


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def events_of(form: str, items: str) -> list[str]:
    """The events one filing is, by its form and its declared items."""
    if form in FORMS:
        return [FORMS[form]]
    if form in ITEM_FORMS:
        declared = {item.strip() for item in (items or "").split(",")}
        return [event for item, event in ITEMS.items() if item in declared]
    return []


def line_for(event: str, *, cik: int, accession: str, form: str, filed: str,
             source: str, accepted: str | None = None, items: str | None = None) -> dict:
    line = {"event": event, "cik": cik, "accession": accession, "form": form,
            "filed": filed, "accepted": accepted, "source": source}
    if form in ITEM_FORMS:
        line["items"] = items or ""
    return line


def key(line: dict) -> tuple:
    """What makes a line the same event twice."""
    if line["event"] == ENFORCEMENT:
        return (line["event"], line["release"], line["document"])
    return (line["event"], line["cik"], line["accession"])


def shard(root: Path, line: dict) -> Path:
    return root / line["event"] / f"{line['filed'][:4]}.jsonl"


def on_record(root: Path, event: str | None = None) -> set[tuple]:
    """The key of every line already in the calendar, or in one event's files."""
    folders = [root / event] if event else [path for path in root.iterdir() if path.is_dir()]
    held = set()
    for folder in folders:
        for path in sorted(folder.glob("*.jsonl")) if folder.is_dir() else []:
            for text in path.read_text(encoding="utf-8").splitlines():
                if text.strip():
                    held.add(key(json.loads(text)))
    return held


def order(line: dict) -> tuple:
    return (line["filed"], line.get("accession") or "", line.get("cik") or 0,
            line.get("release") or 0)


def append(root: Path, lines, *, held: set[tuple] | None = None) -> Counter:
    """Append every line not already on record, oldest first within each file.

    Returns how many were added, by event. Nothing already written is touched.
    """
    held = on_record(root) if held is None else held
    fresh = defaultdict(list)
    for line in lines:
        if key(line) in held:
            continue
        held.add(key(line))
        fresh[shard(root, line)].append(line)
    added = Counter()
    for path, batch in sorted(fresh.items()):
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as out:
            for line in sorted(batch, key=order):
                out.write(json.dumps(line, sort_keys=True) + "\n")
                added[line["event"]] += 1
    return added


def record_source(root: Path, line: dict) -> None:
    root.mkdir(parents=True, exist_ok=True)
    with (root / SOURCES).open("a", encoding="utf-8") as out:
        out.write(json.dumps(dict(line, at=now()), sort_keys=True) + "\n")


def sources(root: Path) -> list[dict]:
    path = root / SOURCES
    if not path.is_file():
        return []
    return [json.loads(text) for text in path.read_text(encoding="utf-8").splitlines()
            if text.strip()]


# -- submissions ---------------------------------------------------------------

def filings_in(document: dict) -> dict:
    """The parallel arrays of one submissions document, main file or older page."""
    return document["filings"]["recent"] if "filings" in document else document


CIK_IN_NAME = re.compile(r"CIK(\d{10})")


def from_submissions(archive: zipfile.ZipFile, *, since: str = SINCE):
    """(events, every watched accession) from the bulk file, one member at a time.

    The accessions are kept as integers, to hold every watched filing since 2009
    in memory on a small machine.
    """
    seen: set[int] = set()
    found = []
    for name in archive.namelist():
        match = CIK_IN_NAME.search(name)
        if not match or not name.endswith(".json"):
            continue
        cik = int(match.group(1))
        with archive.open(name) as handle:
            document = json.load(handle)
        arrays = filings_in(document)
        forms = arrays.get("form", [])
        for i, form in enumerate(forms):
            if form not in WATCHED_FORMS or arrays["filingDate"][i] < since:
                continue
            accession = arrays["accessionNumber"][i]
            seen.add(int(accession.replace("-", "")))
            items = (arrays.get("items") or [""] * len(forms))[i] or ""
            for event in events_of(form, items):
                found.append(line_for(
                    event, cik=cik, accession=accession, form=form,
                    filed=arrays["filingDate"][i],
                    accepted=(arrays.get("acceptanceDateTime") or [None] * len(forms))[i],
                    items=items, source="submissions"))
    return found, seen


def quarters(since: str, today: dt.date) -> list[tuple[int, int]]:
    start = dt.date.fromisoformat(since)
    out, year, quarter = [], start.year, (start.month - 1) // 3 + 1
    while (year, quarter) <= (today.year, (today.month - 1) // 3 + 1):
        out.append((year, quarter))
        year, quarter = (year, quarter + 1) if quarter < 4 else (year + 1, 1)
    return out


def index_rows(text: str):
    """(form, cik, date, accession) for every watched form in one form index."""
    for raw in text.splitlines():
        form = raw[:12].strip() if len(raw) > 12 else ""
        if form not in WATCHED_FORMS or not raw.startswith(form + " "):
            continue
        parts = raw.rsplit(None, 3)
        if len(parts) != 4 or not parts[3].startswith("edgar/data/"):
            continue
        _, cik, date, path = parts
        if len(date) == 8 and date.isdigit():  # the daily index writes 20260925
            date = f"{date[:4]}-{date[4:6]}-{date[6:]}"
        yield form, int(cik), date, Path(path).stem


HEADER_ITEM = re.compile(r"^<ITEMS>\s*(\S+)", re.MULTILINE)


def items_from_header(fetcher, cik: int, accession: str) -> str:
    url = HEADER_URL.format(cik=cik, folder=accession.replace("-", ""), accession=accession)
    return ",".join(HEADER_ITEM.findall(fetcher.get(url).decode("utf-8", "replace")))


def from_index_text(fetcher, text: str, seen: set[int] | None, *, since: str):
    """(events, watched filings listed, not in the bulk file, headers unread, latest day).

    With `seen` None every watched filing is taken, which is how a day's index
    is read after the bulk file: whatever is already on record is skipped when
    the lines are appended.
    """
    found, unread = [], []
    listed = missing = 0
    through = None
    for form, cik, date, accession in index_rows(text):
        if date < since:
            continue
        listed += 1
        through = max(through or date, date)
        if seen is not None and int(accession.replace("-", "")) in seen:
            continue
        missing += 1
        items = None
        if form in ITEM_FORMS:
            try:
                items = items_from_header(fetcher, cik, accession)
            except Exception as exc:  # noqa: BLE001 - counted, and the index goes on
                unread.append(f"{accession}: {type(exc).__name__}: {exc}")
                continue
        for event in events_of(form, items or ""):
            found.append(line_for(event, cik=cik, accession=accession, form=form,
                                  filed=date, items=items,
                                  source="full_index" if seen is not None else "daily_index"))
    return found, listed, missing, unread, through


def from_indexes(fetcher, seen: set[int], *, since: str, today: dt.date, root: Path):
    """Every watched filing the quarterly indexes list and the bulk file does not."""
    found = []
    for year, quarter in quarters(since, today):
        url = FORM_INDEX_URL.format(year=year, quarter=quarter)
        raw = fetcher.get(url)
        text = gzip.decompress(raw).decode("latin-1")
        events, listed, missing, unread, through = from_index_text(fetcher, text, seen,
                                                                   since=since)
        found += events
        record_source(root, {"source": "full_index", "year": year, "quarter": quarter,
                             "bytes": len(raw),
                             "sha256": hashlib.sha256(raw).hexdigest(),
                             "watched_filings_listed": listed,
                             "not_in_submissions": missing, "headers_unread": unread,
                             "through": through})
        print(f"  {year} quarter {quarter}: {listed} watched filings, {missing} not in "
              "the bulk file", file=sys.stderr)
    return found


def read_through(root: Path) -> dt.date | None:
    """The last filing day the indexes have been read through, by the source lines.

    A quarterly index read before its line recorded that day stands for the
    week before the day it was read: reading a day twice appends nothing twice.
    A daily index that was not read (a holiday, a refusal) names no day and
    stands for none, whenever its line was written.
    """
    days = []
    for line in sources(root):
        if line.get("source") not in ("full_index", "daily_index"):
            continue
        if line.get("through"):
            days.append(dt.date.fromisoformat(line["through"]))
        elif line.get("at") and line["source"] == "full_index":
            days.append(dt.date.fromisoformat(line["at"][:10]) - dt.timedelta(days=7))
    return max(days) if days else None


def from_daily(fetcher, *, start: dt.date, end: dt.date, root: Path) -> list[dict]:
    """Every watched filing of each business day from `start` through `end`."""
    found = []
    day = start
    while day <= end:
        if day.weekday() < 5:
            url = DAILY_INDEX_URL.format(year=day.year, quarter=(day.month - 1) // 3 + 1,
                                         day=day.strftime("%Y%m%d"))
            try:
                raw = fetcher.get(url)
            except Exception as exc:  # noqa: BLE001 - a holiday has no index
                record_source(root, {"source": "daily_index", "day": day.isoformat(),
                                     "unread": f"{type(exc).__name__}: "
                                               f"{str(exc).replace(url, 'the index')}"})
            else:
                events, listed, _, unread, _ = from_index_text(
                    fetcher, raw.decode("latin-1"), None, since=SINCE)
                found += events
                record_source(root, {"source": "daily_index", "day": day.isoformat(),
                                     "bytes": len(raw),
                                     "sha256": hashlib.sha256(raw).hexdigest(),
                                     "watched_filings_listed": listed,
                                     "headers_unread": unread, "events": len(events),
                                     "through": day.isoformat()})
        day += dt.timedelta(days=1)
    return found


def daily(fetcher, *, root: Path, today: dt.date) -> dict:
    """The calendar brought up to yesterday from the daily indexes. What it added."""
    through = read_through(root)
    if through is None:
        return {"days": 0, "added": {}, "reason": "no index has been read yet; build the "
                "calendar from the bulk file first"}
    start, end = through + dt.timedelta(days=1), today - dt.timedelta(days=1)
    found = from_daily(fetcher, start=start, end=end, root=root)
    added = append(root, found)
    return {"from": start.isoformat(), "through": end.isoformat(),
            "days": max((end - start).days + 1, 0), "added": dict(added)}


# -- going concern -------------------------------------------------------------

def going_concern(value: str) -> int:
    """How many sentences of one value hold both "substantial doubt" and "going concern"."""
    lowered = value.lower()
    if "going concern" not in lowered or "substantial doubt" not in lowered:
        return 0
    return sum(1 for sentence in SENTENCE.split(lowered)
               if "going concern" in sentence and "substantial doubt" in sentence)


def notes_rows(archive: zipfile.ZipFile, table: str):
    """Rows of one table as dictionaries, through the csv reader for its quoting."""
    name = next(n for n in archive.namelist()
                if Path(n).stem.lower() == table and Path(n).suffix.lower() in (".tsv", ".txt"))
    csv.field_size_limit(1 << 30)
    with archive.open(name) as handle:
        yield from csv.DictReader(io.TextIOWrapper(handle, "utf-8", errors="replace",
                                                   newline=""), delimiter="\t")


def from_notes(archive: zipfile.ZipFile, dataset: str) -> list[dict]:
    """One going-concern line per filer and filing in one notes data set."""
    filings = {row["adsh"]: row for row in notes_rows(archive, "sub")}
    by_filing: dict[str, dict] = {}
    for row in notes_rows(archive, "txt"):
        sentences = going_concern(row.get("value") or "")
        if not sentences:
            continue
        held = by_filing.setdefault(row["adsh"], {"tag": row["tag"], "sentences": 0})
        held["sentences"] += sentences
    out = []
    for accession, said in by_filing.items():
        filing = filings.get(accession)
        if filing is None:
            continue
        filed = f"{filing['filed'][:4]}-{filing['filed'][4:6]}-{filing['filed'][6:8]}"
        # No form: the data sets hold registration statements, whose EDGAR names
        # the plain-name check reads as codes, and the `sub` row holds it.
        out.append({"event": GOING_CONCERN, "cik": int(filing["cik"]), "accession": accession,
                    "filed": filed, "accepted": filing.get("accepted") or None,
                    "source": "notes_data_set", "dataset": dataset, **said})
    return out


def scan_notes(path: Path, index_line: dict, *, root: Path = CALENDAR) -> dict:
    """`src/fsn.py`'s hook: a notes data set's going-concern lines, appended."""
    with zipfile.ZipFile(path) as archive:
        lines = from_notes(archive, index_line["period"])
    added = append(root, lines, held=on_record(root, GOING_CONCERN))
    record_source(root, {"source": "notes_data_set", "dataset": index_line["period"],
                         "url": index_line["url"], "sha256": index_line["sha256"],
                         "bytes": index_line["bytes"], "filings_with_language": len(lines),
                         "added": added.get(GOING_CONCERN, 0)})
    return {"going_concern_filings": len(lines), "added": added.get(GOING_CONCERN, 0)}


# -- enforcement releases ------------------------------------------------------

ROW = re.compile(r"<tr[^>]*>(.*?)</tr>", re.DOTALL)
PUBLISHED = re.compile(r'<time datetime="([^"]+)"')
RESPONDENTS = re.compile(r"release-view__respondents'?\"?>\s*<a href=['\"]([^'\"]+)['\"]>(.*?)</a>",
                         re.DOTALL)
NUMBERS = re.compile(r'view-table_subfield_value">\s*([^<]*)<')
# The number only: `AAER-3022A` on the list is release 3022 again.
AAER_NUMBER = re.compile(r"\bAAER-(\d+)")


def releases_on(page: str) -> list[dict]:
    """The enforcement releases one page of the list holds, a line for each number."""
    out = []
    for row in ROW.findall(page):
        published, named, numbers = (PUBLISHED.search(row), RESPONDENTS.search(row),
                                     NUMBERS.search(row))
        if not (published and named and numbers):
            continue
        stamp = dt.datetime.fromisoformat(published.group(1).replace("Z", "+00:00"))
        document = named.group(1)
        for release in dict.fromkeys(int(n) for n in AAER_NUMBER.findall(numbers.group(1))):
            out.append({"event": ENFORCEMENT, "release": release,
                        "filed": stamp.astimezone(EASTERN).date().isoformat(),
                        "document": document if document.startswith("http")
                        else "https://www.sec.gov" + document,
                        "cik": None, "source": "enforcement_list"})
    return out


def from_enforcement_list(fetcher, *, since: str = SINCE, pages: int = 200) -> list[dict]:
    """Every release on the list published on or after `since`, newest page first."""
    found = []
    for page in range(pages):
        batch = releases_on(fetcher.get(ENFORCEMENT_URL.format(page=page)).decode(
            "utf-8", "replace"))
        if not batch:
            break
        found.extend(line for line in batch if line["filed"] >= since)
        if min(line["filed"] for line in batch) < since:
            break
    return found


# -- counts --------------------------------------------------------------------

def counts(root: Path, ciks: set[int] | None = None) -> dict[str, int]:
    """Lines per event, over every filer or over the filers named."""
    out = {event: 0 for event in EVENTS}
    for event in EVENTS:
        for path in sorted((root / event).glob("*.jsonl")):
            for text in path.read_text(encoding="utf-8").splitlines():
                if not text.strip():
                    continue
                if ciks is None or json.loads(text).get("cik") in ciks:
                    out[event] += 1
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="the event calendar")
    parser.add_argument("command", choices=("submissions", "daily", "enforcement", "counts"))
    parser.add_argument("--root", default=str(CALENDAR))
    parser.add_argument("--zip", default=None, help="submissions: a bulk file already here")
    parser.add_argument("--work", default=str(DATA_ROOT / "tmp" / "calendar"))
    parser.add_argument("--since", default=SINCE)
    args = parser.parse_args(argv)
    root = Path(args.root)
    fetcher = fetch_fixtures.Fetcher(
        os.environ.get("EDGAR_USER_AGENT", fetch_fixtures.DEFAULT_USER_AGENT))
    if args.command == "counts":
        twelve = {int(row["cik"]) for row in universe.rows()}
        print(json.dumps({"every_filer": counts(root), "the_twelve": counts(root, twelve)},
                         indent=2))
        return 0
    if args.command == "daily":
        print(json.dumps(daily(fetcher, root=root,
                               today=dt.datetime.now(dt.timezone.utc).date())))
        return 0
    if args.command == "enforcement":
        found = from_enforcement_list(fetcher, since=args.since)
        added = append(root, found, held=on_record(root, ENFORCEMENT))
        record_source(root, {"source": "enforcement_list",
                             "url": ENFORCEMENT_URL.format(page=0),
                             "releases_listed_since": len(found), "since": args.since,
                             "added": added.get(ENFORCEMENT, 0)})
        print(json.dumps({"listed": len(found), "added": dict(added)}))
        return 0
    from src import fsn  # the streaming download lives there
    # The download makes the work directory, after the floor check has passed.
    work = Path(args.work)
    path = Path(args.zip) if args.zip else work / "submissions.zip"
    try:
        if not args.zip:
            fsn.room_for(work, 2 * 10**9, fsn.TRANSIENT_FLOOR_BYTES)
            digest, size = fsn.download(SUBMISSIONS_URL, path, fetcher.user_agent)
        else:
            digest, size = fsn.file_sha256(path), path.stat().st_size
        with zipfile.ZipFile(path) as archive:
            found, seen = from_submissions(archive, since=args.since)
        record_source(root, {"source": "submissions", "url": SUBMISSIONS_URL, "bytes": size,
                             "sha256": digest, "since": args.since,
                             "watched_filings": len(seen), "events": len(found)})
        added = append(root, found)
        print(f"  submissions: {len(seen)} watched filings, {len(found)} events, "
              f"added {dict(added)}", file=sys.stderr)
        found = from_indexes(fetcher, seen, since=args.since,
                             today=dt.datetime.now(dt.timezone.utc).date(), root=root)
    except fsn.FloorReached as exc:
        print(f"event_calendar: stopped at the disk floor: {exc}", file=sys.stderr)
        return FAILED
    finally:
        if not args.zip:
            path.unlink(missing_ok=True)
    added += append(root, found)
    print(json.dumps({"added": dict(added)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(interpreter_pin.enforce() or main())
