"""Mechanical regression checks on one run's outputs, and the hand-worked cases.

Each check reads files a run published and nothing about how they were made:
- `files_present`: the files every analysed run publishes.
- `agents_written`: every agent the manifest records wrote its file, and the run
  records no analysis failure.
- `quotes_resolve`: every quote a reader kept is in the paragraph its
  `paragraph_id` names, in that reader's own committed input; every quote an
  analysis kept is in the inputs that analyst was handed, character for character
  after the whitespace fold; a `quote_from` naming a file the analyst was not
  handed fails, and so does a run with no record of what an agent was handed.
- `cited_items_exist`: every evidence id an analysis cites is an item a reader
  report kept.
- `cited_numbers_exist`: every number an analysis cites names a field of the
  calculator file that analyst saw.
- `nothing_after_cutoff`: no input document is filed after the run's cutoff, no
  source without a filing date was read past it (`rows_used_through`), no row of
  the JSON inputs -- as the run holds them and as each agent was handed them --
  was filed after it, and no date written anywhere in any calculator file -- a
  fact's filing, a price, a window, a period -- is after it: every string value
  or key that is a date, a date pair or a date-time stamp in every calculator
  file, and every row of every input dated by one of ROW_DATE_KEYS. A date
  inside prose (a maturity, a guidance year) is a fact of the filing and is not
  held to the cutoff. And a market table
  holds exactly reaction days zero to two of each window, read off the window's
  acceptance stamp on the exchange calendar, with nothing past day two of the
  latest. The documents' rule is CLAUDE.md's, dates only; the market table's is
  `docs/HOW_WE_WORK.md` §4's.
- `calculator_finite`: every numeric value in calculator.json is finite.
- `dcf_recomputes`: every scenario's enterprise value and value per share, and the
  simple free cash flow, recompute from the run's own drivers with this file's own
  arithmetic, which reproduces the two hand-worked cases below.
"""

from __future__ import annotations

import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

from evals.common import (FAIL, NOT_APPLICABLE, PASS, PLACEHOLDER, REPO, Result, finite, fold,
                          load, number_at, resolve, run_name, walk_strings)

REQUIRED = ("input_manifest.json", "calculator.json", "calculator_filings_only.json",
            "analysis_accounting.json", "analysis_financial.json", "analysis_valuation.json",
            "report_numbers.md", "report_notes_text.md", "memo_ko.md")

# Which calculator file each analysis was handed (docs/HOW_WE_WORK.md §3): the
# accounting and financial analysts see no price; the valuation analyst's first pass
# sees the calculator before its drivers, its second pass the whole calculator.
SEEN = {"analysis_accounting.json": "calculator_filings_only.json",
        "analysis_financial.json": "calculator_filings_only.json",
        "assumptions.json": "calculator_before_drivers.json",
        "analysis_valuation.json": "calculator.json"}
ANALYSES = tuple(SEEN)
# The directory each analysis's agent was handed: its quotes are held to what it saw.
AGENT_DIR = {"analysis_accounting.json": "accounting-analyst",
             "analysis_financial.json": "financial-analyst",
             "assumptions.json": "valuation-analyst",
             "analysis_valuation.json": "valuation-analyst-second-pass"}

FENCE = re.compile(r"```json\s*\n(.*?)\n```", re.S)
# A date, or a period written as two dates, anywhere in a calculator file.
# a date, a date..date pair, or a date-time stamp; a date inside prose is not one
ISO_DATE = re.compile(r"(\d{4}-\d{2}-\d{2})(?:[T ][0-9:.+\-Z]*)?(?:\.\.(\d{4}-\d{2}-\d{2}))?")
# The keys that say when a row of an input arrived. The period a fact covers
# (`start`, `end`) is not one: a 10-K filed in February carries facts for the
# fiscal year it is in, whose period ends after the cutoff, and that is the filing's
# content, not a late arrival.
ROW_DATE_KEYS = ("filed", "filing_date", "filed_at", "accepted", "date", "as_of")
FOLLOWS_PATHS = ("fields",)          # list entries that are calculator paths


def report_items(path: Path) -> list[dict]:
    return read_report(path)[0]


def read_report(path: Path) -> tuple[list[dict], int]:
    """A report's items, and how many fenced blocks were not JSON: a block that
    cannot be read holds items nobody can check, and is counted, never skipped."""
    if not path.is_file():
        return [], 0
    return read_report_blocks(path.read_text(encoding="utf-8"))


def read_report_text(text: str) -> list[dict]:
    return read_report_blocks(text)[0]


def read_report_blocks(text: str) -> tuple[list[dict], int]:
    items, malformed = [], 0
    for block in FENCE.findall(text):
        try:
            data = json.loads(block)
        except ValueError:
            malformed += 1
            continue
        for item in data if isinstance(data, list) else [data]:
            if isinstance(item, dict):
                items.append(item)
    return items, malformed


READER_DIR = {"report_numbers.md": "numbers-reader", "report_notes_text.md": "notes-text-reader"}
# What a quote may stand on: the filing as the run committed it (input_*) and the
# reader reports upstream of the analyst (report_*), never the calculator. The
# valuation analyst is also handed both gated analyses (#101), so its quote of one
# is a citation of an upstream layer; how many of its quotes rest on an analyst's
# words rather than a filing is reported as a capability score
# (`valuation_quotes_from_filings`), not passed silently.
QUOTABLE = ("input_", "report_")
QUOTABLE_FOR = {"assumptions.json": QUOTABLE + ("analysis_accounting.json",
                                                "analysis_financial.json"),
                "analysis_valuation.json": QUOTABLE + ("analysis_accounting.json",
                                                       "analysis_financial.json")}


def agent_saw(run: Path, agent: str, *, quotable=QUOTABLE) -> dict[str, str] | None:
    """The quotable files an agent was handed, as written (the fold is applied where
    a quote is compared, because the paragraph index needs the line breaks), or None
    when the run kept no directory for that agent: what it was handed is then not
    on record, and a quote cannot be held to it."""
    directory = run / "agents" / agent
    if not directory.is_dir():
        return None
    return {p.name: p.read_text(encoding="utf-8", errors="replace")
            for p in sorted(directory.iterdir()) if p.is_file() and p.name.startswith(quotable)}


ID_LINE = re.compile(r"^\[(\d{10}-\d{2}-\d{6}:[a-z0-9_]+:[^\]]+)\]\s*$", re.M)


def paragraphs_of(text: str) -> dict[str, str]:
    """The `[id]` blocks of a prose input: each id owns the text up to the next id."""
    out = {}
    matches = list(ID_LINE.finditer(text))
    for this, following in zip(matches, matches[1:] + [None]):
        end = following.start() if following else len(text)
        out[this.group(1)] = text[this.end():end]
    return out


def _enclosing_object(text: str, at: int) -> str | None:
    depth, start = 0, None
    for index in range(at, -1, -1):
        ch = text[index]
        if ch == "}":
            depth += 1
        elif ch == "{":
            if depth == 0:
                start = index
                break
            depth -= 1
    if start is None:
        return None
    depth = 0
    for index in range(start, len(text)):
        ch = text[index]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return text[start:index + 1]
    return None


def json_objects_printing(text: str, identifier: str) -> list[str]:
    """Every innermost JSON object in a pretty-printed file whose text holds the
    quoted id: the rows that print it. A filing that states one fact at two
    precisions prints the one id over two rows, and a quote of either stands."""
    out, at = [], text.find(f'"{identifier}"')
    while at >= 0:
        row = _enclosing_object(text, at)
        if row is not None and row not in out:
            out.append(row)
        at = text.find(f'"{identifier}"', at + 1)
    return out


def paragraph_text(seen: dict[str, str], identifier: str) -> str | None:
    """The committed text one paragraph id owns, out of the files an agent saw:
    an `[id]` block of a prose file, or the JSON row of a computed file that
    prints the id. None when no file the agent saw carries the id."""
    for name, text in seen.items():
        if name.endswith(".md"):
            block = paragraphs_of(text).get(identifier)
            if block is not None:
                return fold(block)
        elif name.endswith(".json"):
            rows = json_objects_printing(text, identifier)
            if rows:
                return fold("\n".join(rows))
    return None


def row_keys(row_text: str) -> set[str]:
    """Every key name a JSON row prints, at any depth."""
    try:
        row = json.loads(row_text)
    except ValueError:
        return set()
    out = set()

    def walk(node):
        if isinstance(node, dict):
            for key, value in node.items():
                out.add(key)
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(row)
    return out


# What a computed row carries about itself rather than about the company: the
# namespace, the unit, the form, the ids, the dates. A quote made of these alone
# says nothing the filing said. The tag is not among them: the concept a filer
# tagged a line with is the filer's own choice, and CIEN's numbers reader quoted a
# bad-debt allowance that moved from one tag to another between years, which is a
# fact about the filing.
ROW_METADATA_KEYS = ("prefix", "namespace", "unit", "form", "id", "paragraph_id",
                     "source_accession", "accession", "context_ref", "decimals",
                     "filing_date", "filed", "period", "start", "end", "instant")


def row_metadata(row_text: str) -> set[str]:
    """Every value a row prints under a metadata key, as printed."""
    try:
        row = json.loads(row_text)
    except ValueError:
        return set()
    out = set()

    def walk(node):
        if isinstance(node, dict):
            for key, value in node.items():
                if key in ROW_METADATA_KEYS and isinstance(value, (str, int, float)):
                    out.add(json.dumps(value))
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(row)
    return out


def says_something(quote: str, keys: set[str], identifier: str,
                   metadata: set[str] = frozenset()) -> bool:
    """Whether a quote of a JSON row carries anything beyond the row's key names,
    its metadata values, the id and JSON punctuation: those alone are not a quote
    of anything the filing said; a value, or a piece of one, is."""
    rest = quote.replace(f'"{identifier}"', " ")
    for key in sorted(keys, key=len, reverse=True):
        rest = rest.replace(f'"{key}"', " ")
    for value in sorted(metadata, key=len, reverse=True):
        rest = rest.replace(value, " ")
    return bool(re.sub(r"[\s:,{}\[\]\"]+", "", rest))


def quote_stands(seen: dict[str, str], identifier: str, quote: str) -> str | None:
    """Why a reader's quote does not stand on the paragraph it names, or None."""
    paragraph = paragraph_text(seen, identifier)
    if paragraph is None:
        return f"paragraph {identifier} is not in the reader's input"
    if fold(quote) not in paragraph:
        return "the quote is not in the paragraph it names"
    if paragraph.lstrip().startswith("{"):
        rows = [row for text in seen.values() if text.lstrip().startswith("{")
                for row in json_objects_printing(text, identifier)]
        keys = set().union(*(row_keys(row) for row in rows))
        metadata = set().union(*(row_metadata(row) for row in rows))
        if not says_something(quote, keys, identifier, metadata):
            return "the quote carries only key names, the row's metadata or the id, nothing the row says"
    return None


def units_of(name: str, text: str) -> list[tuple[str, set[str], set[str]]]:
    """The units an analyst's quote can stand in, as (text, keys, metadata): one
    paragraph of a prose input; one string value of a JSON file; one item of a
    reader report, with its key names and metadata so that a quote made only of
    those is refused. A quote is of one thing one file said, not of the file."""
    if name.endswith(".md") and ID_LINE.search(text):
        return [(fold(body), set(), set()) for body in paragraphs_of(text).values()]
    if name.startswith("report_"):
        out = []
        for item in read_report_text(text):
            values = " \u241f ".join(fold(v) for _, v in walk_strings(item))
            printed = json.dumps(item)
            out.append((values, row_keys(printed), row_metadata(printed)))
        return out
    if name.endswith(".json"):
        try:
            tree = json.loads(text)
        except ValueError:
            return []
        return [(fold(value), set(), set()) for _, value in walk_strings(tree)]
    return [(fold(text), set(), set())]


def analysis_quote_stands(seen: dict[str, str], quote: str) -> str | None:
    """Why an analyst's quote stands in no unit of the files it was handed, or None."""
    wanted = fold(quote)
    found = False
    for name, text in seen.items():
        for body, keys, metadata in units_of(name, text):
            if wanted in body:
                found = True
                if says_something(quote, keys, "", metadata):
                    return None
    if found:
        return "the quote carries only key names, the item's metadata or the id, nothing it says"
    return "in no one paragraph, value or report item it was handed"


def quoted(node, where=""):
    """Every dictionary in a tree that carries a `quote`, with where it sits."""
    if isinstance(node, dict):
        if isinstance(node.get("quote"), str) and node["quote"].strip():
            yield where, node
        for key, value in node.items():
            if key in ("dropped_items",):
                continue
            yield from quoted(value, f"{where}.{key}" if where else key)
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from quoted(value, f"{where}[{index}]")


def check_files_present(run: Path) -> Result:
    missing = [name for name in REQUIRED if not (run / name).is_file()]
    return Result("mechanical.files_present", run_name(run), FAIL if missing else PASS,
                  f"missing {missing}" if missing else f"{len(REQUIRED)} files", missing)


def check_agents_written(run: Path) -> Result:
    manifest = load(run / "input_manifest.json") or {}
    agents = manifest.get("agents") or {}
    silent = [name for name, record in agents.items() if record.get("result") != "written"]
    problems = list(silent)
    if not agents:
        problems.append("the manifest records no agent")
    if manifest.get("analysis_failure"):
        problems.append(f"analysis_failure: {manifest['analysis_failure']}")
    return Result("mechanical.agents_written", run_name(run), FAIL if problems else PASS,
                  "; ".join(map(str, problems)) or f"{len(agents)} agents wrote", problems)


def check_quotes_resolve(run: Path) -> Result:
    failures, count = [], 0
    for report, reader in READER_DIR.items():
        seen = agent_saw(run, reader, quotable=("input_",))
        if seen is None:
            failures.append(f"{report}: no agents/{reader} directory, so what the reader was "
                            "handed is not on record")
            continue
        items, malformed = read_report(run / report)
        if malformed:
            count += malformed
            failures.append(f"{report}: {malformed} fenced block(s) that are not JSON")
        for item in items:
            quote = item.get("quote")
            count += 1
            if not isinstance(quote, str) or not quote.strip():
                failures.append(f"{report}:{item.get('id')}: a kept item with no quote")
                continue
            why = quote_stands(seen, str(item.get("paragraph_id")), quote)
            if why:
                failures.append(f"{report}:{item.get('id')}: {why}")
    for name in ANALYSES:
        tree = load(run / name)
        if tree is None:
            continue
        seen = agent_saw(run, AGENT_DIR[name], quotable=QUOTABLE_FOR.get(name, QUOTABLE))
        if seen is None:
            failures.append(f"{name}: no agents/{AGENT_DIR[name]} directory, so what the analyst "
                            "was handed is not on record")
            continue
        for where, node in quoted(tree):
            count += 1
            source = node.get("quote_from")
            quote = node["quote"]
            if isinstance(source, str) and source not in seen:
                failures.append(f"{name}:{where}: quote_from {source} is not a file it was handed")
                continue
            candidates = {source: seen[source]} if isinstance(source, str) else seen
            why = analysis_quote_stands(candidates, quote)
            if why:
                failures.append(f"{name}:{where}: {why}")
    return Result("mechanical.quotes_resolve", run_name(run), FAIL if failures else PASS,
                  f"{count - len(failures)} of {count} quotes found in what the agent was handed",
                  failures)


def check_cited_items_exist(run: Path) -> Result:
    """Every evidence id an analysis cites is an item a reader report kept."""
    # an item with no id is kept by nobody: a citation of null resolves to nothing
    kept = {item["id"] for report in READER_DIR for item in report_items(run / report)
            if isinstance(item.get("id"), str)}
    failures, count = [], 0
    for name in ("analysis_accounting.json", "analysis_financial.json", "analysis_valuation.json"):
        tree = load(run / name) or {}

        def walk(node, where):
            nonlocal count
            if isinstance(node, dict):
                for key, value in node.items():
                    if key == "dropped_items":
                        continue
                    here = f"{where}.{key}" if where else key
                    if key == "evidence":
                        if not isinstance(value, list):
                            count += 1
                            failures.append(f"{name}:{here}: evidence is not a list")
                            continue
                        for cited in value:
                            count += 1
                            if cited not in kept:
                                failures.append(f"{name}:{here}: {cited}")
                    else:
                        walk(value, here)
            elif isinstance(node, list):
                for index, value in enumerate(node):
                    walk(value, f"{where}[{index}]")

        walk(tree, "")
    return Result("mechanical.cited_items_exist", run_name(run), FAIL if failures else PASS,
                  f"{count - len(failures)} of {count} evidence ids are kept reader items",
                  failures)


def check_cited_numbers_exist(run: Path) -> Result:
    failures, count = [], 0
    for name, seen in SEEN.items():
        tree = load(run / name)
        if tree is None:
            continue
        calculator = load(run / seen)
        if calculator is None:
            failures.append(f"{name}: {seen} is missing")
            continue
        for where, text in walk_strings({k: v for k, v in tree.items() if k != "dropped_items"}):
            if where.endswith(".dropped") or where == "dropped":
                continue                     # the gate's own note on what it dropped
            paths = PLACEHOLDER.findall(text)
            if where.split("[")[0].endswith(FOLLOWS_PATHS) and not paths:
                paths = [(text, "")]
            for path, _ in paths:
                count += 1
                try:
                    resolve(calculator, path)
                except KeyError:
                    failures.append(f"{name}:{where}:{path}")
    return Result("mechanical.cited_numbers_exist", run_name(run), FAIL if failures else PASS,
                  f"{count - len(failures)} of {count} cited paths exist", failures)


def walk_keys(node, where: str = ""):
    """Every dict key in a JSON tree, with where it sits: a date can be a key."""
    if isinstance(node, dict):
        for key, value in node.items():
            here = f"{where}.{key}" if where else key
            yield here, str(key)
            yield from walk_keys(value, here)
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from walk_keys(value, f"{where}[{index}]")


def _dates_in(node, key: str):
    if isinstance(node, dict):
        for k, v in node.items():
            if k == key and isinstance(v, str):
                yield v
            else:
                yield from _dates_in(v, key)
    elif isinstance(node, list):
        for v in node:
            yield from _dates_in(v, key)


def check_nothing_after_cutoff(run: Path) -> Result:
    manifest = load(run / "input_manifest.json") or {}
    try:
        cutoff = dt.date.fromisoformat(manifest["cutoff"])
    except (KeyError, TypeError, ValueError):
        return Result("mechanical.nothing_after_cutoff", run_name(run), FAIL,
                      "the manifest names no cutoff")
    late = []
    for document in manifest.get("documents") or []:
        filed = document.get("filing_date")
        through = document.get("rows_used_through")
        if filed:
            if dt.date.fromisoformat(filed) > cutoff:
                late.append(f"document {document.get('accession')} filed {filed}")
        elif through:
            if dt.date.fromisoformat(through) > cutoff:
                late.append(f"{document.get('role')} rows used through {through}")
        else:
            late.append(f"{document.get('role') or document.get('path')}: neither a filing "
                        "date nor rows_used_through, so nothing holds it to the cutoff")
    # every calculator file: the run's own and the copies the agents were handed
    for path in sorted(run.glob("calculator*.json")) + sorted(run.glob("agents/*/calculator*.json")):
        tree = load(path) or {}
        for where, value in list(walk_strings(tree)) + list(walk_keys(tree)):
            match = ISO_DATE.fullmatch(value)
            if not match:
                continue
            for text in (match.group(1), match.group(2)):
                try:
                    late_one = text and dt.date.fromisoformat(text) > cutoff
                except ValueError:
                    late_one = False
                if late_one:
                    late.append(f"{path.relative_to(run)}: {where} = {value}")
    # the inputs themselves, as the run holds them and as each agent was handed
    # them: every row's own filing date, read rather than trusted to the manifest
    inputs = sorted(run.glob("input_*.json")) + sorted(run.glob("agents/*/input_*.json"))
    for path in inputs:
        if path.name == "input_manifest.json":
            continue
        tree = load(path)
        if path.name == "input_market.json":
            late += [f"{path.relative_to(run)}: {p}" for p in
                     market_table_problems(tree or {}, cutoff, manifest.get("accepted"))]
            continue
        for key in ROW_DATE_KEYS:
            for value in _dates_in(tree, key):
                try:
                    late_one = bool(re.match(r"\d{4}-\d{2}-\d{2}", value)) \
                        and dt.date.fromisoformat(value[:10]) > cutoff
                except ValueError:
                    late_one = False
                if late_one:
                    late.append(f"{path.relative_to(run)}: {key} {value}")
                    break
    return Result("mechanical.nothing_after_cutoff", run_name(run), FAIL if late else PASS,
                  f"cutoff {cutoff}" + (f"; {len(late)} late" if late else ""), late)


# --- the market table: reaction days zero to two, and nothing past them ----------------
#
# The exchange calendar, by rule, so the grader does not read the table's rows as
# the calendar the table is checked against (a table missing a row would then pass
# one trading day late). The New York Stock Exchange closes on weekends and on the
# holidays below; closures outside the rules are listed by hand, and the owner
# extends that list. EDGAR's business days are the federal holidays, which differ
# from the exchange's on three days a year.

EASTERN = ZoneInfo("America/New_York")
MARKET_CLOSE = dt.time(16, 0)
EDGAR_CLOSE = dt.time(17, 30)
# days the exchange closed outside its holiday rules: national days of mourning
SPECIAL_CLOSURES = frozenset({dt.date(2018, 12, 5), dt.date(2025, 1, 9)})


def _nth_weekday(year: int, month: int, weekday: int, n: int) -> dt.date:
    first = dt.date(year, month, 1)
    return first + dt.timedelta(days=(weekday - first.weekday()) % 7 + 7 * (n - 1))


def _last_weekday(year: int, month: int, weekday: int) -> dt.date:
    last = (dt.date(year, month, 28) + dt.timedelta(days=4)).replace(day=1) - dt.timedelta(days=1)
    return last - dt.timedelta(days=(last.weekday() - weekday) % 7)


def _easter(year: int) -> dt.date:
    """Gregorian Easter Sunday (the anonymous algorithm); 2026-04-05 by hand."""
    a, b, c = year % 19, year // 100, year % 100
    d, e, f = b // 4, b % 4, (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    ll = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * ll) // 451
    month = (h + ll - 7 * m + 114) // 31
    day = (h + ll - 7 * m + 114) % 31 + 1
    return dt.date(year, month, day)


def _observed(day: dt.date) -> dt.date:
    """A fixed-date holiday on a Saturday is observed the Friday before, on a
    Sunday the Monday after."""
    if day.weekday() == 5:
        return day - dt.timedelta(days=1)
    if day.weekday() == 6:
        return day + dt.timedelta(days=1)
    return day


def _shared_holidays(year: int) -> set[dt.date]:
    out = set()
    new_year = dt.date(year, 1, 1)
    if new_year.weekday() == 6:
        out.add(new_year + dt.timedelta(days=1))
    elif new_year.weekday() < 5:
        out.add(new_year)      # on a Saturday it is not observed on the Friday
    out.add(_nth_weekday(year, 1, 0, 3))        # Martin Luther King Jr. Day
    out.add(_nth_weekday(year, 2, 0, 3))        # Presidents' Day
    out.add(_last_weekday(year, 5, 0))          # Memorial Day
    if year >= 2022:
        out.add(_observed(dt.date(year, 6, 19)))    # Juneteenth
    out.add(_observed(dt.date(year, 7, 4)))     # Independence Day
    out.add(_nth_weekday(year, 9, 0, 1))        # Labor Day
    out.add(_nth_weekday(year, 11, 3, 4))       # Thanksgiving
    out.add(_observed(dt.date(year, 12, 25)))   # Christmas
    return out


def exchange_holidays(year: int) -> set[dt.date]:
    return _shared_holidays(year) | {_easter(year) - dt.timedelta(days=2)}   # Good Friday


def federal_holidays(year: int) -> set[dt.date]:
    out = _shared_holidays(year) | {_nth_weekday(year, 10, 0, 2),          # Columbus Day
                                    _observed(dt.date(year, 11, 11))}      # Veterans Day
    if dt.date(year + 1, 1, 1).weekday() == 5:
        out.add(dt.date(year, 12, 31))     # a Saturday New Year's Day, observed the Friday before
    return out


EARLY_CLOSE = dt.time(13, 0)


def close_time(day: dt.date) -> dt.time:
    """When the exchange closes on `day`: one o'clock on the day after Thanksgiving,
    on July the third and on Christmas Eve when those are trading days (when the
    holiday falls on a Saturday, the Friday is the observed holiday, not an early
    close), else four."""
    early = (_nth_weekday(day.year, 11, 3, 4) + dt.timedelta(days=1),
             dt.date(day.year, 7, 3), dt.date(day.year, 12, 24))
    if day in early and is_trading_day(day):
        return EARLY_CLOSE
    return MARKET_CLOSE


def is_trading_day(day: dt.date) -> bool:
    return day.weekday() < 5 and day not in exchange_holidays(day.year) \
        and day not in SPECIAL_CLOSURES


def trading_days_from(day: dt.date, count: int) -> list[dt.date]:
    """The first `count` trading days on or after `day`."""
    out = []
    while len(out) < count:
        if is_trading_day(day):
            out.append(day)
        day += dt.timedelta(days=1)
    return out


def next_business_day(day: dt.date) -> dt.date:
    """EDGAR's next business day after `day`: not a weekend, not a federal holiday."""
    day += dt.timedelta(days=1)
    while day.weekday() >= 5 or day in federal_holidays(day.year):
        day += dt.timedelta(days=1)
    return day


def _eastern(stamp: str) -> dt.datetime:
    when = dt.datetime.fromisoformat(stamp)
    return when.astimezone(EASTERN) if when.tzinfo else when.replace(tzinfo=EASTERN)


def market_table_problems(table: dict, cutoff: dt.date, accepted=None) -> list[str]:
    """Why a market table reaches past what an input may see, or []. The rule is
    CLAUDE.md's and `docs/HOW_WE_WORK.md` §4's, written out here against the
    exchange calendar above so the grader moves neither with `src/market.py` nor
    with the table's own rows: day zero is the acceptance day when EDGAR accepted
    before that day's close in New York (four o'clock, one on an early-close day)
    and the next trading day when
    after it; days one and two are the next two trading days; each is a row; the
    table carries a filing window, whose filing date is the run's cutoff and is
    the acceptance day or (accepted after half past five) EDGAR's next business
    day; every other window is an earlier filing's; the table's cutoff is day two
    of its latest window; no row lies past it, and every row is a trading day.
    The filing window's acceptance stamp is held to `accepted`, the run's own
    record of when EDGAR accepted the filing (the manifest's): the stamp decides
    day zero, so a table is not believed about it."""
    problems = []
    if not isinstance(accepted, str):
        problems.append("the manifest records no acceptance stamp for the filing, so the "
                        "filing window's stamp would stand on trust")
    rows = sorted(str(r.get("date")) for r in table.get("rows") or [] if isinstance(r, dict))
    table_cutoff = table.get("cutoff")
    if rows and not isinstance(table_cutoff, str):
        return ["the table names no cutoff"]
    windows = [w for w in table.get("windows") or [] if isinstance(w, dict)]
    if not any(w.get("kind") == "filing" for w in windows):
        problems.append("the table has no filing window, so nothing ties it to the run's filing")
    latest = None
    for window in windows:
        kind, days = window.get("kind"), [str(d) for d in window.get("days") or []]
        stamp = window.get("accepted")
        if not isinstance(stamp, str):
            problems.append(f"the {kind} window carries no acceptance stamp")
            continue
        try:
            when = _eastern(stamp)
        except ValueError:
            problems.append(f"the {kind} window's acceptance stamp {stamp!r} is not a time")
            continue
        accepted_on = when.date()
        start = accepted_on if when.time() < close_time(accepted_on) \
            else accepted_on + dt.timedelta(days=1)
        expected = [d.isoformat() for d in trading_days_from(start, 3)]
        if days != expected:
            problems.append(f"the {kind} window's days {days} are not reaction days zero to "
                            f"two {expected} of its acceptance {stamp} on the exchange calendar")
        problems += [f"the {kind} window: no row for {d}" for d in expected if d not in rows]
        filed = str(window.get("filing_date"))
        permitted = {accepted_on.isoformat()}
        if when.time() >= EDGAR_CLOSE:
            permitted.add(next_business_day(accepted_on).isoformat())
        if filed not in permitted:
            problems.append(f"the {kind} window's filing date {filed} is not one EDGAR puts "
                            f"on an acceptance at {stamp}")
        if kind == "filing" and isinstance(accepted, str) and stamp != accepted:
            problems.append(f"the filing window's acceptance stamp {stamp} is not the "
                            f"manifest's {accepted}")
        if kind == "filing" and filed != cutoff.isoformat():
            problems.append(f"the filing window is for a filing dated {filed}, not the run's "
                            f"cutoff {cutoff}")
        elif kind != "filing" and filed > cutoff.isoformat():
            # any other window is an earlier filing's: a later one is not an input
            problems.append(f"the {kind} window is for a filing dated {filed}, after the "
                            f"run's cutoff {cutoff}")
        latest = max(latest or expected[2], expected[2])
    if latest is not None and table_cutoff != latest:
        problems.append(f"the table's cutoff {table_cutoff} is not reaction day two of its "
                        f"latest window {latest}")
    limit = latest or table_cutoff
    problems += [f"row {d} is past reaction day two {limit} of the table's latest window"
                 for d in rows if limit and d > limit]
    for d in rows:
        try:
            if not is_trading_day(dt.date.fromisoformat(d)):
                problems.append(f"row {d} is not a trading day")
        except ValueError:
            problems.append(f"row {d!r} is not a date")
    return problems


def market_reaction_day_two(table) -> dt.date | None:
    """Day two of the table's latest window, read off its windows, or None."""
    if not isinstance(table, dict):
        return None
    days = [str(d) for w in table.get("windows") or [] for d in (w.get("days") or [])[-1:]]
    try:
        return max(dt.date.fromisoformat(d) for d in days) if days else None
    except ValueError:
        return None


def check_calculator_finite(run: Path) -> Result:
    bad = []

    def walk(node, where):
        if isinstance(node, dict):
            for key, value in node.items():
                here = f"{where}.{key}" if where else key
                if key == "value" and value is not None and not finite(value) \
                        and not isinstance(value, (str, list, dict)):
                    bad.append(here)
                walk(value, here)
        elif isinstance(node, list):
            for index, value in enumerate(node):
                walk(value, f"{where}[{index}]")
        elif isinstance(node, float) and not finite(node):
            bad.append(where)

    walk(load(run / "calculator.json") or {}, "")
    return Result("mechanical.calculator_finite", run_name(run), FAIL if bad else PASS,
                  f"{len(bad)} non-finite values" if bad else "every value finite", bad)


# --- the discounted cash flow, worked independently ----------------------------------------

YEARS = 10


def forecast(base_revenue: float, drivers: dict, tax: float, wacc: float) -> dict:
    """Growth fades linearly from year one to the terminal rate at year ten; margin and
    reinvestment move linearly from year one to year ten; free cash flow is revenue x
    margin x (1 - tax) x (1 - reinvestment); end-of-year discounting; the terminal value
    is year ten's cash flow grown once, over WACC less terminal growth."""
    g1, gt = drivers["revenue_growth_year_one"], drivers["terminal_growth"]
    m1, m10 = drivers["operating_margin_year_one"], drivers["operating_margin_year_ten"]
    r1, r10 = drivers["reinvestment_rate_year_one"], drivers["reinvestment_rate_year_ten"]
    revenue, present, cash = base_revenue, 0.0, 0.0
    for year in range(1, YEARS + 1):
        step = (year - 1) / (YEARS - 1)
        growth = g1 + (gt - g1) * step
        margin = m1 + (m10 - m1) * step
        reinvest = r1 + (r10 - r1) * step
        revenue *= 1 + growth
        cash = revenue * margin * (1 - tax) * (1 - reinvest)
        present += cash / (1 + wacc) ** year
    terminal = cash * (1 + gt) / (wacc - gt)
    return {"explicit_present": present, "terminal_value": terminal,
            "enterprise_value": present + terminal / (1 + wacc) ** YEARS}


GORDON = {"revenue_growth_year_one": 0.03, "terminal_growth": 0.03,
          "operating_margin_year_one": 0.20, "operating_margin_year_ten": 0.20,
          "reinvestment_rate_year_one": 0.40, "reinvestment_rate_year_ten": 0.40}
FADE = dict(GORDON, revenue_growth_year_one=0.12)
# Worked by hand (tests/test_calculator.py carries the full table):
#   Gordon: 1,000 x 1.03 x 0.20 x 0.75 x 0.60 = 92.7; 92.7 / (0.09 - 0.03) = 1,545.
#   Fade 12% to 3%: enterprise value 2,240.8020; (2,240.8020 - 100 - 45) / 10 = 209.5802.
HAND_WORKED = (("gordon", GORDON, 1545.0, 140.0), ("fade", FADE, 2240.8020, 209.5802))


# The calculator under judgment runs in a process of its own, with -I, so no code
# of the branch being graded ever runs inside the grading process: imported here,
# its src/__init__.py could rebind any check before a run was graded.
CALCULATOR_PROBE = """
import json, sys
sys.path.insert(0, sys.argv[2])      # -I puts no directory on the path by itself
from src import calculator
out = {}
for name, drivers in json.loads(sys.argv[1]).items():
    run = calculator.forecast(1000.0, drivers, 0.25, 0.09)
    out[name] = {"enterprise_value": run["enterprise_value"],
                 "value_per_share": calculator.bridge(run["enterprise_value"], 100.0, 45.0,
                                                      10.0)["value_per_share"]}
print(json.dumps(out))
"""


def calculator_hand_values(repo: Path = REPO) -> tuple[dict, str | None]:
    """src.calculator's answers to the hand-worked cases, computed in its own process
    from `repo`; (values, None) or ({}, why it gave none)."""
    cases = {name: drivers for name, drivers, _, _ in HAND_WORKED}
    try:
        done = subprocess.run([sys.executable, "-I", "-c", CALCULATOR_PROBE, json.dumps(cases),
                               str(repo)], cwd=repo, capture_output=True, text=True, timeout=120)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {}, f"src.calculator could not be run: {exc}"
    if done.returncode:
        return {}, f"src.calculator exited {done.returncode}: {done.stderr.strip()[-300:]}"
    try:
        values = json.loads(done.stdout)
    except ValueError:
        return {}, f"src.calculator printed no JSON: {done.stdout.strip()[-300:]}"
    return values if isinstance(values, dict) else {}, None


def check_hand_worked_cases(repo: Path = REPO) -> list[Result]:
    """This file's arithmetic and the calculator's both reproduce the hand-worked cases."""
    results = []
    theirs, why = calculator_hand_values(repo)
    for name, drivers, enterprise, per_share in HAND_WORKED:
        own = forecast(1000.0, drivers, 0.25, 0.09)["enterprise_value"]
        problems = []
        if abs(own - enterprise) > 1e-3:
            problems.append(f"the grader's own arithmetic gives {own}, the hand case {enterprise}")
        if why:
            problems.append(why)
        elif not isinstance(theirs.get(name), dict):
            problems.append(f"src.calculator gave no answer for {name}")
        else:
            got = theirs[name]
            if not finite(got.get("enterprise_value")) or abs(got["enterprise_value"] - enterprise) > 1e-3:
                problems.append(f"src.calculator gives {got.get('enterprise_value')}, the hand case {enterprise}")
            if not finite(got.get("value_per_share")) or abs(got["value_per_share"] - per_share) > 1e-4:
                problems.append(f"src.calculator gives {got.get('value_per_share')} a share, the hand case {per_share}")
        results.append(Result(f"mechanical.hand_worked_{name}", "code",
                              FAIL if problems else PASS, "; ".join(problems) or
                              f"enterprise value {enterprise}, {per_share} a share", problems))
    return results


def check_dcf_recomputes(run: Path) -> Result:
    calculator = load(run / "calculator.json") or {}
    valuation = calculator.get("valuation") or {}
    failures, count = [], 0
    for name, scenario in (valuation.get("scenarios") or {}).items():
        if "enterprise_value" not in scenario:
            continue
        count += 1
        own = forecast(valuation["base_revenue"], scenario["drivers"], valuation["tax_rate"],
                       valuation["wacc"])["enterprise_value"]
        if abs(own - scenario["enterprise_value"]) > 1e-6 * max(1.0, abs(own)):
            failures.append(f"{name}: enterprise value {scenario['enterprise_value']} against {own}")
        share = (own - scenario["net_debt"] - scenario["operating_lease_liability"]) \
            / scenario["diluted_shares"]
        if abs(share - scenario["value_per_share"]) > 1e-6 * max(1.0, abs(share)):
            failures.append(f"{name}: {scenario['value_per_share']} a share against {share}")
    simple = (calculator.get("free_cash_flow") or {}).get("free_cash_flow_simple") or {}
    ttm = ((calculator.get("terms") or {}).get("trailing_four_quarters") or {})
    if finite(simple.get("value")):
        count += 1
        try:
            expected = number_at(ttm, "operating_cash_flow") - number_at(ttm, "capital_expenditure")
            if abs(expected - simple["value"]) > 1e-6 * max(1.0, abs(expected)):
                failures.append(f"simple free cash flow {simple['value']} against {expected}")
        except (KeyError, TypeError):
            failures.append("simple free cash flow without its operating cash flow and capex")
    if not count:
        return Result("mechanical.dcf_recomputes", run_name(run), NOT_APPLICABLE,
                      "no scenario and no free cash flow to recompute")
    return Result("mechanical.dcf_recomputes", run_name(run), FAIL if failures else PASS,
                  f"{count - len(failures)} of {count} recompute", failures)


RUN_CHECKS = (check_files_present, check_agents_written, check_quotes_resolve,
              check_cited_items_exist, check_cited_numbers_exist, check_nothing_after_cutoff, check_calculator_finite,
              check_dcf_recomputes)


def grade(run: Path) -> list[Result]:
    return [check(run) for check in RUN_CHECKS]


def valuation_quotes_from_filings(run: Path) -> float | None:
    """Capability: the share of the valuation analyst's quotes that stand on the
    filing or a reader report rather than on another analyst's words."""
    total = filings = 0
    for name in ("assumptions.json", "analysis_valuation.json"):
        tree = load(run / name)
        if tree is None:
            continue
        seen = agent_saw(run, AGENT_DIR[name])
        if seen is None:
            continue
        for _, node in quoted(tree):
            total += 1
            source = node.get("quote_from")
            quote = fold(node["quote"])
            texts = [seen[source]] if isinstance(source, str) and source in seen \
                else list(seen.values())
            filings += any(quote in fold(text) for text in texts)
    return filings / total if total else None
