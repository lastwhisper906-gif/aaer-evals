"""The SEC's Financial Statement and Notes data sets, 2009 to now: indexed, fetched, loaded.

The owner's instruction of 2026-09-28: every monthly or quarterly zip the SEC
publishes at `PAGE_URL`, loaded into `~/aaer-data/fsn.duckdb` -- the `sub`,
`num`, `pre`, `tag`, `txt`, `dim` and `ren` tables -- with the accession and
the filed date on every row, so that every query can be asked as of a date.
The raw data lives outside the repository. The repository holds the index
only: one line per zip, sharded by year under `src/fsn_index/`, each line
naming the URL, the period, the bytes and the sha256 of what the SEC served.

The disk floor
--------------

Nothing is written into `~/aaer-data` that would leave less than 50 GB free
on its disk (`FLOOR_BYTES`, decimal gigabytes, the unit the Finder shows):
`fetch` checks before each zip, `load` before each data set, and each stops
the moment the next one would cross the line. That is the owner's own stop.
`index` keeps nothing: it downloads one zip into a work directory, hashes it,
counts its rows, draws its reconciliation candidates, hands it to the calendar
(`src/event_calendar.py`, which reads the `txt` table for going-concern
language), and deletes it before the next. Its own floor is
`TRANSIENT_FLOOR_BYTES` below the one zip it is holding, which is a default
this module sets and `docs/needs_judgment.md` records.

Point in time
-------------

`sub` carries `filed` itself. `num`, `txt`, `pre` and `ren` carry `adsh`, and
get `filed` from their own data set's `sub` as they are loaded. `tag` and `dim`
are dictionaries shared by every filing in a data set and belong to no one
accession, so each of their rows carries the data set it came from and
`filed_through`, the latest `filed` in that data set's `sub`: a query as of a
date takes a definition only from a data set whose `filed_through` is on or
before it. Every row of every table also carries `dataset`, the period.

The ten values
--------------

A value is drawn at random but reproducibly: the filings are ranked by the
sha256 of their accession, and a filing's value is the eligible `num` row with
the smallest sha256 of its key. Eligible means what companyfacts can hold --
a standard taxonomy, no dimension, no co-registrant. Each zip's index line
keeps its `SAMPLE_CANDIDATES` lowest-ranked filings, so the ten lowest across
every data set are always among them, whichever order the zips were indexed
in. `reconcile` looks each one up in the filer's companyfacts document by
accession, tag, unit and period, and appends what it found to
`src/fsn_index/reconciliation.jsonl`.

    python3.12 -m src.fsn list
    python3.12 -m src.fsn index [--period 2011q2 ...]
    python3.12 -m src.fsn fetch      # make fetch
    python3.12 -m src.fsn load       # make fetch
    python3.12 -m src.fsn reconcile

Exit 0 when the command did everything it was asked, 1 when something it was
asked to do failed, 4 when the disk floor stopped it, 3 the wrong interpreter.
"""

from __future__ import annotations

import argparse
import datetime as dt
import functools
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import time
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

try:
    from src import fetch_companyfacts, fetch_fixtures, interpreter_pin
except ImportError:  # invoked as a plain script
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import fetch_companyfacts, fetch_fixtures, interpreter_pin

REPO_ROOT = Path(__file__).resolve().parent.parent
INDEX_DIR = REPO_ROOT / "src" / "fsn_index"
RECONCILIATION = "reconciliation.jsonl"
DATA_ROOT = Path.home() / "aaer-data"

PAGE_URL = ("https://www.sec.gov/data-research/sec-markets-data/"
            "financial-statement-notes-data-sets")
SITE = "https://www.sec.gov"
ZIP_HREF = re.compile(r'href="(/files/dera/data/financial-statement-notes-data-sets/'
                      r'([^"/]+_notes[^"/]*\.zip))"')
QUARTERLY = re.compile(r"^(\d{4})q([1-4])_notes")
MONTHLY = re.compile(r"^(\d{4})_(\d{2})_notes")

TABLES = ("sub", "num", "pre", "tag", "txt", "dim", "ren")
# The tables that carry an accession, and so take `filed` from `sub`.
BY_ACCESSION = ("num", "pre", "txt", "ren")
# Dictionaries shared by a whole data set.
BY_DATASET = ("tag", "dim")

FLOOR_BYTES = 50 * 10**9
TRANSIENT_FLOOR_BYTES = 10 * 10**9

SAMPLE_CANDIDATES = 20
SAMPLE_SIZE = 10
# companyfacts holds the standard taxonomies, keyed by these names.
TAXONOMY = {"us-gaap": "us-gaap", "ifrs": "ifrs-full", "dei": "dei", "srt": "srt"}
NO_DIMENSION = "0x00000000"

CHUNK = 1 << 20
FAILED = 1
FLOOR = 4


class FloorReached(Exception):
    """The next write would leave less free space than the floor allows."""


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def period_of(name: str) -> str:
    """`2009q2` for a quarterly zip, `2025-07` for a monthly one."""
    quarter = QUARTERLY.match(name)
    if quarter:
        return f"{quarter.group(1)}q{quarter.group(2)}"
    month = MONTHLY.match(name)
    if month:
        return f"{month.group(1)}-{month.group(2)}"
    raise ValueError(f"{name}: not a notes data set's file name")


def listed(page: str) -> list[dict]:
    """Every zip the SEC's page links to, oldest period first."""
    found = {}
    for href, name in ZIP_HREF.findall(page):
        found[name] = {"period": period_of(name), "name": name, "url": SITE + href}
    return sorted(found.values(), key=lambda entry: (entry["period"], entry["name"]))


def read_index(index_dir: Path = INDEX_DIR) -> list[dict]:
    """Every index line, in the order the shards hold them."""
    lines = []
    for shard in sorted(index_dir.glob("[0-9][0-9][0-9][0-9].jsonl")):
        lines.extend(json.loads(text) for text in shard.read_text(encoding="utf-8").splitlines()
                     if text.strip())
    return lines


def latest(index: list[dict]) -> dict[str, dict]:
    """Each period's newest line. A zip the SEC re-issues gets a new line, not an edit."""
    out: dict[str, dict] = {}
    for line in index:
        out[line["period"]] = line
    return dict(sorted(out.items()))


def append_index(line: dict, index_dir: Path = INDEX_DIR) -> Path:
    index_dir.mkdir(parents=True, exist_ok=True)
    shard = index_dir / f"{line['period'][:4]}.jsonl"
    with shard.open("a", encoding="utf-8") as out:
        out.write(json.dumps(line, sort_keys=True) + "\n")
    return shard


def free_bytes(path: Path) -> int:
    """Free space on the disk that holds `path`, or its nearest existing parent."""
    probe = Path(path)
    while not probe.exists():
        probe = probe.parent
    return shutil.disk_usage(probe).free


def room_for(path: Path, needed: int, floor: int, *, free=free_bytes) -> None:
    """Raise FloorReached when writing `needed` bytes at `path` crosses `floor`."""
    left = free(path) - needed
    if left < floor:
        raise FloorReached(
            f"{path}: {needed / 1e9:.1f} GB more would leave {left / 1e9:.1f} GB free, "
            f"under the {floor / 1e9:.0f} GB floor; nothing was written")


def download(url: str, dest: Path, user_agent: str, *, attempts: int = 4) -> tuple[str, int]:
    """Stream `url` to `dest`, hashing as it goes. Returns (sha256, bytes)."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    partial = dest.with_name(dest.name + ".partial")
    for attempt in range(attempts):
        digest, size, promised = hashlib.sha256(), 0, None
        request = urllib.request.Request(url, headers={"User-Agent": user_agent,
                                                       "Accept-Encoding": "identity"})
        try:
            with urllib.request.urlopen(request, timeout=120) as response, \
                    partial.open("wb") as out:
                promised = response.headers.get("Content-Length")
                while True:
                    chunk = response.read(CHUNK)
                    if not chunk:
                        break
                    digest.update(chunk)
                    size += len(chunk)
                    out.write(chunk)
        except urllib.error.HTTPError as exc:
            partial.unlink(missing_ok=True)
            if exc.code in (403, 429, 500, 502, 503, 504) and attempt < attempts - 1:
                time.sleep(2 ** (attempt + 2))
                continue
            raise
        except (urllib.error.URLError, TimeoutError, ConnectionError):
            partial.unlink(missing_ok=True)
            if attempt < attempts - 1:
                time.sleep(2 ** (attempt + 2))
                continue
            raise
        # A connection that closes early ends the read quietly, with no error:
        # the length the server promised is the only thing that says so.
        if promised is not None and size != int(promised):
            partial.unlink(missing_ok=True)
            if attempt < attempts - 1:
                time.sleep(2 ** (attempt + 2))
                continue
            raise OSError(f"{url}: {size:,} of the {int(promised):,} bytes promised arrived")
        partial.replace(dest)
        return digest.hexdigest(), size
    raise RuntimeError(f"unreachable: {url}")


def size_of(url: str, user_agent: str) -> int | None:
    """What the server says the file weighs, before a byte of it is fetched."""
    request = urllib.request.Request(url, method="HEAD", headers={"User-Agent": user_agent})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            length = response.headers.get("Content-Length")
    except (urllib.error.URLError, TimeoutError):
        return None
    return int(length) if length else None


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(CHUNK), b""):
            digest.update(chunk)
    return digest.hexdigest()


def member(archive: zipfile.ZipFile, table: str) -> str:
    """The member holding `table`: `num.tsv`, or `num.txt` in some early zips."""
    for name in archive.namelist():
        if Path(name).stem.lower() == table and Path(name).suffix.lower() in (".tsv", ".txt"):
            return name
    raise KeyError(f"{archive.filename}: no {table} table")


def split(line: bytes) -> list[str]:
    """One row. Values are whitespace-normalised by the SEC, so a tab is always a separator."""
    return line.rstrip(b"\r\n").decode("utf-8", "replace").split("\t")


def rows(archive: zipfile.ZipFile, table: str):
    """(header, iterator of rows) for one table, streamed out of the zip."""
    handle = archive.open(member(archive, table))
    header = split(handle.readline())

    def body():
        with handle:
            for line in handle:
                yield split(line)
    return header, body()


def count_rows(archive: zipfile.ZipFile) -> dict[str, int]:
    """Rows per table, header excluded. Reading every byte also checks every CRC."""
    counts = {}
    for table in TABLES:
        lines, last = 0, b"\n"
        with archive.open(member(archive, table)) as handle:
            for chunk in iter(lambda: handle.read(CHUNK), b""):
                lines += chunk.count(b"\n")
                last = chunk[-1:]
        # A last row with no newline after it is still a row.
        counts[table] = max(lines + (last != b"\n") - 1, 0)
    return counts


def rank(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def eligible(row: dict) -> bool:
    """A num row companyfacts can hold: a standard taxonomy, no dimension, no co-registrant."""
    return (row["version"].split("/")[0] in TAXONOMY
            and row.get("dimh", NO_DIMENSION) == NO_DIMENSION
            and not row.get("coreg")
            and row.get("iprx", "0") == "0"
            and row["value"] != "")


def candidates(archive: zipfile.ZipFile, count: int = SAMPLE_CANDIDATES) -> list[dict]:
    """The `count` lowest-ranked filings, each with its one lowest-ranked eligible value."""
    header, body = rows(archive, "sub")
    filings = {}
    for values in body:
        record = dict(zip(header, values))
        filings[record["adsh"]] = {"accession": record["adsh"], "cik": int(record["cik"]),
                                   "form": record["form"], "filed": record["filed"],
                                   "rank": rank(record["adsh"])}
    chosen = dict(sorted(filings.items(), key=lambda item: item[1]["rank"])[:count])
    header, body = rows(archive, "num")
    best: dict[str, tuple[str, dict]] = {}
    for values in body:
        if values[0] not in chosen:
            continue
        record = dict(zip(header, values))
        if not eligible(record):
            continue
        key = "|".join(record[field] for field in ("adsh", "tag", "version", "ddate",
                                                   "qtrs", "uom"))
        held = best.get(record["adsh"])
        if held is None or rank(key) < held[0]:
            best[record["adsh"]] = (rank(key), record)
    out = []
    for accession, filing in chosen.items():
        if accession not in best:
            continue
        key_rank, record = best[accession]
        out.append(dict(filing, tag=record["tag"], version=record["version"],
                        ddate=record["ddate"], qtrs=int(record["qtrs"]), uom=record["uom"],
                        value=record["value"], value_rank=key_rank))
    return sorted(out, key=lambda entry: entry["rank"])


def take_in(entry: dict, *, work: Path, user_agent: str, index_dir: Path = INDEX_DIR,
            scan=None, keep: Path | None = None, free=free_bytes) -> dict:
    """One zip: download, hash, count, draw candidates, scan, index, then delete it.

    `scan(zip_path, line)` is the calendar's reader; its return value goes on the
    line under `scanned`. With `keep`, the zip is moved there instead of deleted,
    under the retained floor.
    """
    expected = entry.get("bytes") or size_of(entry["url"], user_agent) or 0
    room_for(work, expected, TRANSIENT_FLOOR_BYTES, free=free)
    path = work / entry["name"]
    try:
        digest, size = download(entry["url"], path, user_agent)
        with zipfile.ZipFile(path) as archive:
            counts = count_rows(archive)
            drawn = candidates(archive)
        line = {"period": entry["period"], "name": entry["name"], "url": entry["url"],
                "bytes": size, "sha256": digest, "rows": counts, "candidates": drawn,
                "indexed_utc": now()}
        if scan is not None:
            line["scanned"] = scan(path, line)
        append_index(line, index_dir)
        if keep is not None:
            room_for(keep, size, FLOOR_BYTES, free=free)
            keep.mkdir(parents=True, exist_ok=True)
            shutil.move(str(path), keep / entry["name"])
        return line
    finally:
        path.unlink(missing_ok=True)


def fetch(*, zips: Path, user_agent: str, index_dir: Path = INDEX_DIR,
          periods=None, free=free_bytes) -> list[str]:
    """Every indexed zip into `zips`, verified against its line. Problems, one per zip."""
    problems = []
    for period, line in latest(read_index(index_dir)).items():
        if periods and period not in periods:
            continue
        path = zips / line["name"]
        if path.is_file() and path.stat().st_size == line["bytes"] \
                and file_sha256(path) == line["sha256"]:
            continue
        room_for(zips, line["bytes"], FLOOR_BYTES, free=free)
        digest, size = download(line["url"], path, user_agent)
        if (digest, size) != (line["sha256"], line["bytes"]):
            path.unlink()
            problems.append(f"{period}: the SEC now serves {size:,} bytes with sha256 "
                            f"{digest}, and the index holds {line['bytes']:,} bytes with "
                            f"{line['sha256']}; not kept")
            continue
        print(f"  {period} {size:>13,d} B  verified", file=sys.stderr)
    return problems


def _connect(db: Path):
    import duckdb  # only the loader needs it
    connection = duckdb.connect(str(db))
    connection.execute("SET preserve_insertion_order = false")
    connection.execute("SET memory_limit = '2GB'")
    connection.execute("SET threads = 2")
    connection.execute("""CREATE TABLE IF NOT EXISTS loaded (
        dataset VARCHAR PRIMARY KEY, name VARCHAR, sha256 VARCHAR, rows JSON,
        loaded_utc VARCHAR)""")
    return connection


def load_one(connection, path: Path, line: dict, *, work: Path) -> dict:
    """One verified zip into the store, all seven tables or none."""
    period = line["period"]
    counts = {}
    with zipfile.ZipFile(path) as archive, tempfile.TemporaryDirectory(dir=work) as scratch:
        connection.execute("BEGIN TRANSACTION")
        try:
            for table in ("sub",) + tuple(t for t in TABLES if t != "sub"):
                source = Path(scratch) / f"{table}.tsv"
                with archive.open(member(archive, table)) as src, source.open("wb") as out:
                    shutil.copyfileobj(src, out, CHUNK)
                raw = (f"read_csv('{source}', delim='\\t', header=true, quote='\"', "
                       "escape='\"', all_varchar=true, strict_mode=false, "
                       "null_padding=true)")
                if table == "sub":
                    select = (f"SELECT *, strptime(filed, '%Y%m%d')::DATE AS filed_date, "
                              f"'{period}' AS dataset FROM {raw}")
                elif table in BY_ACCESSION:
                    select = (f"SELECT r.*, s.filed_date, '{period}' AS dataset FROM {raw} r "
                              f"JOIN (SELECT adsh, filed_date FROM sub WHERE dataset = "
                              f"'{period}') s USING (adsh)")
                else:
                    select = (f"SELECT r.*, (SELECT max(filed_date) FROM sub WHERE dataset = "
                              f"'{period}') AS filed_through, '{period}' AS dataset "
                              f"FROM {raw} r")
                if table not in [row[0] for row in connection.execute(
                        "SELECT table_name FROM information_schema.tables").fetchall()]:
                    connection.execute(f"CREATE TABLE {table} AS {select} LIMIT 0")
                before = connection.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
                connection.execute(f"INSERT INTO {table} BY NAME ({select})")
                after = connection.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
                counts[table] = after - before
                source.unlink()
            expected = line.get("rows") or {}
            short = {table: (counts[table], expected[table]) for table in counts
                     if table in expected and counts[table] != expected[table]}
            if short:
                raise ValueError(f"{period}: rows loaded differ from rows counted "
                                 f"(loaded, counted): {short}")
            connection.execute("INSERT INTO loaded VALUES (?, ?, ?, ?, ?)",
                               [period, line["name"], line["sha256"], json.dumps(counts), now()])
            connection.execute("COMMIT")
        except Exception:
            connection.execute("ROLLBACK")
            raise
    return counts


def uncompressed(path: Path) -> int:
    with zipfile.ZipFile(path) as archive:
        return sum(info.file_size for info in archive.infolist())


def load(*, db: Path, zips: Path, index_dir: Path = INDEX_DIR, periods=None,
         free=free_bytes) -> list[str]:
    """Every fetched and verified zip into `db`, skipping what is loaded already."""
    problems = []
    connection = _connect(db)
    done = {row[0] for row in connection.execute("SELECT dataset FROM loaded").fetchall()}
    work = db.parent / "tmp"
    work.mkdir(parents=True, exist_ok=True)
    try:
        for period, line in latest(read_index(index_dir)).items():
            if (periods and period not in periods) or period in done:
                continue
            path = zips / line["name"]
            if not path.is_file() or file_sha256(path) != line["sha256"]:
                problems.append(f"{period}: {path} is not the indexed zip; run fetch first")
                continue
            # The member files are written out beside the store while they load.
            room_for(db, 2 * uncompressed(path), FLOOR_BYTES, free=free)
            counts = load_one(connection, path, line, work=work)
            print(f"  {period} loaded {counts}", file=sys.stderr)
    finally:
        connection.close()
    return problems


def start_of(ddate: str, qtrs: int) -> str | None:
    """The duration's first day as companyfacts writes it, or None for an instant."""
    if qtrs == 0:
        return None
    end = dt.date(int(ddate[:4]), int(ddate[4:6]), int(ddate[6:8]))
    return (end - dt.timedelta(days=round(qtrs * 91.3125))).isoformat()


def lookup(facts: dict, value: dict) -> dict:
    """The candidate against companyfacts: `match`, `different_value` or `absent`."""
    taxonomy = TAXONOMY[value["version"].split("/")[0]]
    end = f"{value['ddate'][:4]}-{value['ddate'][4:6]}-{value['ddate'][6:8]}"
    units = facts.get("facts", {}).get(taxonomy, {}).get(value["tag"], {}).get("units", {})
    rows_here = [row for row in units.get(value["uom"], [])
                 if row.get("accn") == value["accession"] and row.get("end") == end]
    if value["qtrs"] == 0:
        rows_here = [row for row in rows_here if "start" not in row]
    else:
        approximate = dt.date.fromisoformat(start_of(value["ddate"], value["qtrs"]))
        rows_here = [row for row in rows_here if "start" in row
                     and abs((dt.date.fromisoformat(row["start"]) - approximate).days) <= 20]
    if not rows_here:
        return {"result": "absent", "companyfacts": None}
    wanted = float(value["value"])
    for row in rows_here:
        if float(row["val"]) == wanted:
            return {"result": "match", "companyfacts": row}
    return {"result": "different_value", "companyfacts": rows_here[0]}


def reconcile(fetcher, *, index_dir: Path = INDEX_DIR, size: int = SAMPLE_SIZE) -> dict:
    """The `size` lowest-ranked candidates across every data set, against companyfacts."""
    pool = [dict(value, dataset=period)
            for period, line in latest(read_index(index_dir)).items()
            for value in line.get("candidates", [])]
    pool.sort(key=lambda value: value["rank"])
    checked, documents = [], {}
    for value in pool[:size]:
        cik = f"{value['cik']:010d}"
        url = fetch_companyfacts.COMPANYFACTS_URL.format(cik=cik)
        if cik not in documents:
            try:
                documents[cik] = fetcher.get_json(url)
            except Exception as exc:  # noqa: BLE001 - recorded as the value's result
                documents[cik] = exc
        found = documents[cik]
        if isinstance(found, Exception):
            result = {"result": "companyfacts_unavailable",
                      "companyfacts": f"{type(found).__name__}: {found}"}
        else:
            result = lookup(found, value)
        checked.append({"fsn": value, "companyfacts_url": url, **result})
    record = {"at": now(), "datasets": len(latest(read_index(index_dir))),
              "pool": len(pool), "checked": checked,
              "matched": sum(1 for entry in checked if entry["result"] == "match")}
    with (index_dir / RECONCILIATION).open("a", encoding="utf-8") as out:
        out.write(json.dumps(record, sort_keys=True) + "\n")
    return record


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="the Financial Statement and Notes data sets")
    parser.add_argument("command", choices=("list", "index", "fetch", "load", "reconcile"))
    parser.add_argument("--root", default=str(DATA_ROOT), help="where the raw data lives")
    parser.add_argument("--index-dir", default=str(INDEX_DIR))
    parser.add_argument("--period", action="append", default=None,
                        help="only this period, e.g. 2011q2 or 2025-07; repeatable")
    parser.add_argument("--work", default=None,
                        help="index: where one zip is held while it is read")
    parser.add_argument("--keep", default=None,
                        help="index: move each zip here instead of deleting it")
    parser.add_argument("--no-calendar", action="store_true",
                        help="index: do not hand the zip to the calendar")
    parser.add_argument("--calendar-root", default=None,
                        help="index: the calendar to append to (default events/calendar)")
    args = parser.parse_args(argv)
    root, index_dir = Path(args.root).expanduser(), Path(args.index_dir)
    user_agent = os.environ.get("EDGAR_USER_AGENT", fetch_fixtures.DEFAULT_USER_AGENT)
    fetcher = fetch_fixtures.Fetcher(user_agent)
    try:
        if args.command == "list":
            for entry in listed(fetcher.get(PAGE_URL).decode("utf-8", "replace")):
                print(entry["period"], entry["url"])
            return 0
        if args.command == "index":
            have = latest(read_index(index_dir))
            todo = [entry for entry in listed(fetcher.get(PAGE_URL).decode("utf-8", "replace"))
                    if entry["period"] not in have
                    and (not args.period or entry["period"] in args.period)]
            scan = None
            if not args.no_calendar:
                from src import event_calendar
                scan = functools.partial(event_calendar.scan_notes, root=Path(
                    args.calendar_root) if args.calendar_root else event_calendar.CALENDAR)
            work = Path(args.work) if args.work else root / "tmp" / "fsn"
            for entry in todo:
                line = take_in(entry, work=work, user_agent=user_agent, index_dir=index_dir,
                               scan=scan, keep=Path(args.keep) if args.keep else None)
                print(f"  {line['period']} {line['bytes']:>13,d} B  rows {line['rows']}  "
                      f"{line.get('scanned')}", file=sys.stderr)
            print(json.dumps({"indexed": [entry["period"] for entry in todo]}))
            return 0
        if args.command == "fetch":
            problems = fetch(zips=root / "fsn" / "zips", user_agent=user_agent,
                             index_dir=index_dir, periods=args.period)
        elif args.command == "load":
            problems = load(db=root / "fsn.duckdb", zips=root / "fsn" / "zips",
                            index_dir=index_dir, periods=args.period)
        else:
            record = reconcile(fetcher, index_dir=index_dir)
            print(json.dumps({key: record[key] for key in ("matched", "pool", "datasets")}
                             | {"results": [entry["result"] for entry in record["checked"]]}))
            return 0 if record["matched"] == len(record["checked"]) else FAILED
    except FloorReached as exc:
        print(f"fsn: stopped at the disk floor: {exc}", file=sys.stderr)
        return FLOOR
    for problem in problems:
        print(f"fsn: {problem}", file=sys.stderr)
    return FAILED if problems else 0


if __name__ == "__main__":
    raise SystemExit(interpreter_pin.enforce() or main())
