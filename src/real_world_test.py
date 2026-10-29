"""The real-world test: does the accounting analysis point where the SEC later did?

The owner asked on 2026-10-28 whether the analysis is done the way a hedge fund
does it. The published runs cannot answer that: the companies of the universe
had no accounting enforcement case, and they test the pipeline, not the signal
(CLAUDE.md). This runs the same pipeline on filings the SEC later found
misstated, filed before anyone said so, and on filings of companies in the same
industry that no restatement followed, and counts, by a rule fixed here before
any of those runs exists, how often the analysis flagged the accounts the SEC
named.

**The cases** (`real_world/cases.json`) are the SEC's accounting and auditing
enforcement releases: the company, its CIK, the misstated periods, the accounts
the SEC's own document names (each a quote copied from it), the date the
problem first became public, and the 10-Q and 10-K filings inside the window
filed before that date. `check` fetches every source again and refuses a case
whose quote is not on its page or whose filing EDGAR does not record so.

**The run of a case** is its latest candidate filing: the one filed closest to
the day the problem became public, so the most of it is in the record.

**The controls** (`controls`): for each case, a company of the same
four-digit SIC code (else the same three digits; EDGAR's list of filers under
each code, at most sixty under the case's own code and fifteen under each of
the other nine) that filed the same form
within 92 days of the case's filing, has the 10-K, two 10-Qs and earnings 8-K a
run needs, and filed no 8-K with item 4.02 (non-reliance), no 10-K/A and no
10-Q/A in the three years after that filing. Among those, the one whose filing
date is nearest the case's, the lower CIK on a tie. Nothing about size is
matched; the results say so.

**What counts** (`score`), fixed before the runs: each account the SEC named
maps to the analysis areas that look at it (`AREAS_OF`). In a run's
`analysis_accounting.json`, the case is

- *flagged*, when an anomaly in one of those areas says the numbers
  **contradict** the company's prose;
- *questioned*, when an anomaly there is anything but "the numbers confirm".

A control is scored on the areas of the case it is matched to. An account the
mapping does not cover (`other`) is reported and scored for nothing. A run that
did not finish is a run that did not finish, listed, never dropped. The counts
are printed as they come; the twelve or so cases give a count, not a rate any
test of significance would stand behind, and the results say that too.

**What the model already knows** (`probe`): the analysts read filings that name
the company, and a model may remember that the company later restated. Each
company is asked, with no filing and no tool, what it remembers; the answer is
kept verbatim and the score is printed for the companies it remembered and for
the rest apart.

    python -m src.real_world_test check     --dir real_world
    python -m src.real_world_test controls  --dir real_world
    python -m src.real_world_test plan      --dir real_world
    python -m src.real_world_test run       --dir real_world --jobs 3
    python -m src.real_world_test probe     --dir real_world
    python -m src.real_world_test score     --dir real_world
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import io
import json
import re
import subprocess
import sys
import unicodedata
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path

try:
    from src import cutoff_guard, edgar_client, fetch_fixtures, interpreter_pin
except ImportError:  # invoked as a plain script
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import cutoff_guard, edgar_client, fetch_fixtures, interpreter_pin

BAD_INPUT = 2
ROOT = Path(__file__).resolve().parent.parent

# Each account an enforcement release names, to the areas of the accounting
# analysis that look at it (`.claude/agents/accounting-analyst.md`, its seven
# areas and industry lens). Fixed before the first run of this test.
AREAS_OF = {
    "revenue": ("revenue_recognition",),
    "receivables": ("revenue_recognition", "earnings_versus_cash"),
    "inventory": ("estimates_and_reserves", "industry_lens"),
    "cost_of_sales": ("estimates_and_reserves", "cost_deferral"),
    "expenses_capitalized": ("cost_deferral",),
    "reserves_and_estimates": ("estimates_and_reserves",),
    "one_time_items": ("cost_deferral",),
    "cash_flow_classification": ("cash_flow_engineering_and_off_balance_sheet",),
    "related_parties": ("controls_audit_and_filing_signals",
                        "cash_flow_engineering_and_off_balance_sheet"),
    "other": (),
}
CONTROL_WINDOW_DAYS = 92
CLEAN_YEARS = 3
AMENDMENTS = ("10-K/A", "10-Q/A")
SIC_LIST = ("https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&SIC={sic}"
            "&type={form}&dateb=&owner=include&start={start}&count=100&output=atom")
CANDIDATES_PER_SIC = 60
CANDIDATES_PER_OTHER_SIC = 15     # each of the nine other codes under the same three digits
PROBE_QUESTION = (
    "Answer from memory only; you have no documents and no tools. Company: {company} "
    "(SEC CIK {cik}). Did this company ever restate its financial statements, announce "
    "that earlier financial statements could not be relied on, or settle or litigate an "
    "SEC accounting enforcement case? If you remember one, say which fiscal years and "
    "which accounts or practices. If you do not remember one, say so. Reply with JSON "
    'only: {{"remembers_a_problem": true or false, "years": [...], "accounts": [...], '
    '"what": "..."}}')


class RealWorldError(Exception):
    """A case, a control or a run that cannot be used as asked."""


# -- reading a source page -----------------------------------------------------

class _Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_data(self, data):
        self.parts.append(data)

    def handle_starttag(self, tag, attrs):
        if tag in ("p", "div", "br", "tr", "li", "h1", "h2", "h3", "h4", "td"):
            self.parts.append(" ")


def page_text(raw: bytes) -> str:
    """A page's text: a PDF's extracted text, else an HTML page's text."""
    if raw[:5] == b"%PDF-":
        import pypdf    # only the label check reads a PDF
        reader = pypdf.PdfReader(io.BytesIO(raw))
        return " ".join(page.extract_text() or "" for page in reader.pages)
    parser = _Text()
    parser.feed(raw.decode("utf-8", "replace"))
    return "".join(parser.parts)


_TYPOGRAPHY = str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"',
                             "–": "-", "—": "-", "­": None})


def readable(text: str) -> str:
    """Text as a quote is compared to it: compatibility characters folded (a PDF's
    ligatures), typographic quotes and dashes as their plain forms, a soft hyphen
    dropped, and every run of whitespace one space. Nothing else."""
    text = unicodedata.normalize("NFKC", html.unescape(text)).translate(_TYPOGRAPHY)
    return re.sub(r"\s+", " ", text).strip()


def quote_on_page(quote: str, text: str) -> bool:
    """Whether a quote is on a page, read as `readable` reads both. A PDF breaks a
    word at a line end with a hyphen; the page is also read with those joined."""
    needle, page = readable(quote), readable(text)
    return bool(needle) and (needle in page or needle in re.sub(r"(\w)- (\w)", r"\1\2", page))


# -- the cases -----------------------------------------------------------------

def load(directory: Path, name: str) -> list[dict]:
    path = directory / name
    if not path.is_file():
        raise RealWorldError(f"{path} is not there")
    return json.loads(path.read_text(encoding="utf-8"))


def latest_candidate(case: dict) -> dict:
    filings = case.get("candidate_filings") or []
    if not filings:
        raise RealWorldError(f"{case['company']}: no candidate filing")
    return max(filings, key=lambda f: (f["filing_date"], f["accession"]))


def check_case(case: dict, fetch, rows: list[dict]) -> list[str]:
    """What is wrong with one case: a quote not on its page, a filing EDGAR does
    not record so, an account the mapping does not know, a filing on or after
    the day the problem became public."""
    problems, pages = [], {}

    def on(url: str, quote: str, what: str):
        if url not in pages:
            try:
                pages[url] = page_text(fetch(url))
            except Exception as exc:     # a page that cannot be read is a problem named
                pages[url] = None
                problems.append(f"{what}: {url} could not be read ({type(exc).__name__})")
        if pages[url] is not None and not quote_on_page(quote, pages[url]):
            problems.append(f"{what}: the quote is not on {url}: {quote[:80]!r}")

    on(case["order_url"], case["periods_quote"], "periods")
    for account in case.get("accounts") or []:
        if account.get("account") not in AREAS_OF:
            problems.append(f"account {account.get('account')!r} is not one this test maps")
        on(case["order_url"], account["quote"], f"account {account.get('account')}")
    first = case["first_public"]
    on(first["source_url"], first["quote"], "first public")
    by_accession = {row["accessionNumber"]: row for row in rows}
    for filing in case.get("candidate_filings") or []:
        row = by_accession.get(filing["accession"])
        if row is None:
            problems.append(f"{filing['accession']} is not in CIK {case['cik']}'s index")
            continue
        if (row["form"], row["filingDate"], row["reportDate"]) != (
                filing["form"], filing["filing_date"], filing["period_end"]):
            problems.append(f"{filing['accession']}: EDGAR records {row['form']} filed "
                            f"{row['filingDate']} for {row['reportDate']}")
        if filing["filing_date"] >= first["date"]:
            problems.append(f"{filing['accession']} was filed on or after the problem "
                            f"became public ({first['date']})")
    return problems


# -- the controls --------------------------------------------------------------

def companies_of(fetch, sic: str, form: str) -> list[int]:
    """The CIKs EDGAR lists under a SIC code as filers of a form, at most
    `CANDIDATES_PER_SIC`, in the order it lists them."""
    found: list[int] = []
    for start in range(0, CANDIDATES_PER_SIC, 100):
        text = fetch(SIC_LIST.format(sic=sic, form=form, start=start)).decode("utf-8", "replace")
        ciks = [int(c) for c in re.findall(r"<cik>(\d+)</cik>", text)]
        found.extend(c for c in ciks if c not in found)
        if len(ciks) < 100:
            break
    return found[:CANDIDATES_PER_SIC]


def _day(text: str) -> dt.date:
    return dt.date.fromisoformat(text[:10])


def clean_filing(rows: list[dict], form: str, near: str) -> dict | None:
    """A company's filing of the form nearest `near` within the window, when it
    has what a run needs and nothing in the three years after it says its
    statements were wrong; else None."""
    target = _day(near)
    filings = [r for r in rows if r["form"] == form
               and abs((_day(r["filingDate"]) - target).days) <= CONTROL_WINDOW_DAYS]
    if not filings:
        return None
    filing = min(filings, key=lambda r: (abs((_day(r["filingDate"]) - target).days),
                                         r["accessionNumber"]))
    filed = _day(filing["filingDate"])
    after = [r for r in rows if filed < _day(r["filingDate"])
             <= filed + dt.timedelta(days=365 * CLEAN_YEARS)]
    if any(r["form"] in AMENDMENTS or "4.02" in (r.get("items") or "").split(",")
           for r in after):
        return None
    before = [r for r in rows if r["filingDate"] <= filing["filingDate"]]
    if not any(r["form"] == "10-K" for r in before) \
            or sum(r["form"] == "10-Q" for r in before) < 2 \
            or not any(r["form"] == "8-K" and "2.02" in (r.get("items") or "") for r in before):
        return None
    return filing


def pick_control(case: dict, filing: dict, fetch, rows_of, avoid: set[int]) -> dict | None:
    """The control for one case, by the rule in this module's docstring."""
    sic = str(case["sic"])
    for code in (sic, sic[:3]):
        listed = companies_of(fetch, code, filing["form"]) if len(code) == 4 else [
            cik for four in sorted({sic[:3] + d for d in "0123456789"} - {sic})
            for cik in companies_of(fetch, four, filing["form"])[:CANDIDATES_PER_OTHER_SIC]]
        best = None
        for cik in listed:
            if cik in avoid or cik == int(case["cik"]):
                continue
            found = clean_filing(rows_of(cik), filing["form"], filing["filing_date"])
            if found is None:
                continue
            key = (abs((_day(found["filingDate"]) - _day(filing["filing_date"])).days), cik)
            if best is None or key < best[0]:
                best = (key, cik, found)
        if best is not None:
            _, cik, found = best
            return {"case": case["aaer_number"], "cik": cik, "sic_matched": code,
                    "accession": found["accessionNumber"], "form": found["form"],
                    "filing_date": found["filingDate"], "period_end": found["reportDate"]}
    return None


# -- the plan and the runs -----------------------------------------------------

def label_of(name: str, taken: set[str]) -> str:
    """A run's directory name from a company name: its letters, upper case, at
    most twelve, never a digit (CLAUDE.md: no letter-number codes), unique."""
    letters = re.sub(r"[^A-Z]", "", unicodedata.normalize("NFKD", name).upper())[:12] or "COMPANY"
    label, extra = letters, "BCDEFGHJKLMNPQRSTVWXZ"
    for letter in extra:
        if label not in taken:
            break
        label = letters[:11] + letter
    taken.add(label)
    return label


def plan(cases: list[dict], controls: list[dict], names: dict[int, str]) -> list[dict]:
    """Every run of the test: a case's latest candidate filing, and its control's."""
    taken: set[str] = set()
    out = []
    by_case = {c["case"]: c for c in controls}
    for case in cases:
        filing = latest_candidate(case)
        out.append({"role": "case", "pair": case["aaer_number"],
                    "label": label_of(case["company"], taken), "cik": int(case["cik"]),
                    "company": case["company"], **{k: filing[k] for k in
                                                   ("accession", "form", "filing_date",
                                                    "period_end")}})
        control = by_case.get(case["aaer_number"])
        if control is not None:
            company = names.get(control["cik"], f"company {control['cik']}")
            out.append({"role": "control", "pair": case["aaer_number"],
                        "label": label_of(company, taken), "cik": control["cik"],
                        "company": company, **{k: control[k] for k in
                                               ("accession", "form", "filing_date",
                                                "period_end")}})
    return out


def run_dir(directory: Path, row: dict) -> Path:
    return directory / "runs" / row["label"] / row["accession"]


def run_one(directory: Path, row: dict) -> dict:
    """One run through the on-demand command; what it exited with."""
    out = run_dir(directory, row).resolve()
    if (out / "analysis_accounting.json").is_file():
        return {"label": row["label"], "result": "already run"}
    command = [sys.executable, "-m", "src.on_demand", "--ticker", row["label"],
               "--cik", str(row["cik"]), "--accession", row["accession"],
               "--out", str(out), "--run"]
    log = (directory / "logs" / f"{row['label']}-{row['accession']}.log").resolve()
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("w", encoding="utf-8") as sink:
        done = subprocess.run(command, cwd=ROOT, stdout=sink, stderr=subprocess.STDOUT)
    return {"label": row["label"], "result": f"exit {done.returncode}", "log": str(log)}


# -- the probe -----------------------------------------------------------------

def probe_one(company: str, cik: int, model: str) -> dict:
    """What the model says it remembers of one company, asked with no tool."""
    question = PROBE_QUESTION.format(company=company, cik=cik)
    done = subprocess.run(["claude", "-p", "--restricted", "--model", model,
                           "--output-format", "json", question],
                          capture_output=True, text=True, timeout=600, cwd="/")
    try:
        answer = json.loads(done.stdout).get("result", "")
    except ValueError:
        answer = done.stdout[-2000:]
    found = re.search(r"\{.*\}", answer or "", re.S)
    try:
        parsed = json.loads(found.group(0)) if found else None
    except ValueError:
        parsed = None
    return {"cik": cik, "company": company, "model": model, "answer": answer,
            "remembers_a_problem": (parsed or {}).get("remembers_a_problem")}


# -- the score -----------------------------------------------------------------

def areas_for(case: dict) -> tuple[str, ...]:
    return tuple(sorted({area for account in case.get("accounts") or []
                         for area in AREAS_OF.get(account.get("account"), ())}))


def read_run(analysis: dict | None, areas: tuple[str, ...]) -> dict:
    """One run read by the rule fixed above."""
    if analysis is None:
        return {"finished": False}
    named = [a for a in analysis.get("anomalies") or [] if a.get("area") in areas]
    contradicts = [a for a in named if a.get("numbers_vs_prose") == "contradicts"]
    questioned = [a for a in named if a.get("numbers_vs_prose") != "confirms"]
    dropped = [area for area in areas
               if isinstance((analysis.get("areas") or {}).get(area), dict)
               and "dropped" in analysis["areas"][area]]
    return {"finished": True, "flagged": bool(contradicts), "questioned": bool(questioned),
            "contradicts": len(contradicts), "questioned_count": len(questioned),
            "anomalies_in_named_areas": [
                {"id": a.get("id"), "name_ko": a.get("name_ko"), "area": a.get("area"),
                 "numbers_vs_prose": a.get("numbers_vs_prose")} for a in named],
            "areas_dropped_by_the_gate": dropped}


def score(directory: Path, cases: list[dict], runs: list[dict],
          probes: dict[int, dict]) -> dict:
    by_pair = {c["aaer_number"]: c for c in cases}
    rows = []
    for row in runs:
        case = by_pair[row["pair"]]
        # a run's own output, read the way every file of a run directory is
        # read (`cutoff_guard.load_bundle_file`); a run that wrote none is a
        # run that did not finish
        try:
            analysis = json.loads(cutoff_guard.load_bundle_file(run_dir(directory, row),
                                                                "analysis_accounting.json"))
        except cutoff_guard.CutoffGuardError:
            analysis = None
        rows.append({**row, "areas": list(areas_for(case)),
                     "accounts": [a.get("account") for a in case.get("accounts") or []],
                     "remembers_a_problem": (probes.get(int(row["cik"])) or {}).get(
                         "remembers_a_problem"),
                     **read_run(analysis, areas_for(case))})

    def tally(role: str, remembered=None) -> dict:
        mine = [r for r in rows if r["role"] == role and r["finished"]
                and (remembered is None or bool(r["remembers_a_problem"]) == remembered)]
        return {"finished": len(mine), "flagged": sum(r["flagged"] for r in mine),
                "questioned": sum(r["questioned"] for r in mine)}

    pairs = []
    for pair in by_pair:
        case = next((r for r in rows if r["pair"] == pair and r["role"] == "case"), None)
        control = next((r for r in rows if r["pair"] == pair and r["role"] == "control"), None)
        if case and control and case["finished"] and control["finished"]:
            pairs.append((case["questioned_count"] > control["questioned_count"]) -
                         (case["questioned_count"] < control["questioned_count"]))
    return {
        "rule": "flagged: an anomaly in an area the SEC's named accounts map to says the "
                "numbers contradict the prose; questioned: one there says anything but "
                "confirms (src/real_world_test.py, AREAS_OF)",
        "cases": tally("case"), "controls": tally("control"),
        "cases_the_model_remembered": tally("case", True),
        "cases_the_model_did_not_remember": tally("case", False),
        "pairs_case_questioned_more": pairs.count(1),
        "pairs_equal": pairs.count(0), "pairs_control_questioned_more": pairs.count(-1),
        "not_finished": [f"{r['role']} {r['label']} {r['accession']}" for r in rows
                         if not r["finished"]],
        "runs": rows,
    }


# -- the command line ----------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=("check", "controls", "plan", "run", "probe", "score"))
    parser.add_argument("--dir", default="real_world")
    parser.add_argument("--jobs", type=int, default=2)
    parser.add_argument("--model", default=None,
                        help="the model the probe asks; default the one a case run's "
                             "accounting analyst was served")
    args = parser.parse_args(argv)
    directory = Path(args.dir)
    try:
        cases = load(directory, "cases.json")
        if args.command in ("check", "controls"):
            client = edgar_client.EdgarClient()
            rows_cache: dict[int, list[dict]] = {}

            def rows_of(cik: int) -> list[dict]:
                if cik not in rows_cache:
                    rows_cache[cik] = fetch_fixtures.every_filing(client, f"{int(cik):010d}")
                return rows_cache[cik]

            if args.command == "check":
                bad = 0
                for case in cases:
                    problems = check_case(case, client.get, rows_of(int(case["cik"])))
                    bad += bool(problems)
                    print(f"{case['aaer_number']} {case['company']}: "
                          + ("; ".join(problems) if problems else "every source holds"))
                return 1 if bad else 0
            avoid = {int(c["cik"]) for c in cases}
            controls = []
            for case in cases:
                control = pick_control(case, latest_candidate(case), client.get, rows_of, avoid)
                print(f"{case['aaer_number']} {case['company']}: "
                      + (f"control CIK {control['cik']} {control['form']} "
                         f"{control['accession']} filed {control['filing_date']}"
                         if control else "no control found by the rule"))
                if control:
                    avoid.add(control["cik"])
                    controls.append(control)
            (directory / "controls.json").write_text(json.dumps(controls, indent=1) + "\n")
            return 0
        if args.command == "plan":
            controls = load(directory, "controls.json")
            client = edgar_client.EdgarClient()
            names = {c["cik"]: client.get_json(fetch_fixtures.SUBMISSIONS_URL.format(
                cik=f"{int(c['cik']):010d}"))["name"] for c in controls}
            rows = plan(cases, controls, names)
            (directory / "plan.json").write_text(json.dumps(rows, indent=1) + "\n")
            print(f"{len(rows)} runs planned")
            return 0
        runs = load(directory, "plan.json")
        if args.command == "run":
            with ThreadPoolExecutor(max_workers=args.jobs) as pool:
                for done in pool.map(lambda row: run_one(directory, row), runs):
                    print(json.dumps(done))
            return 0
        if args.command == "probe":
            out = directory / "memory_probe.jsonl"
            have = {json.loads(line)["cik"] for line in out.read_text().splitlines()} \
                if out.is_file() else set()
            for row in runs:
                if row["cik"] in have:
                    continue
                model = args.model or _served(run_dir(directory, row))
                if model is None:
                    print(f"{row['label']}: no model named and no finished run to read one "
                          f"from; not asked")
                    continue
                with out.open("a", encoding="utf-8") as sink:
                    sink.write(json.dumps(probe_one(row["company"], row["cik"], model)) + "\n")
                have.add(row["cik"])
            return 0
        probes = {}
        probe_file = directory / "memory_probe.jsonl"
        if probe_file.is_file():
            probes = {json.loads(line)["cik"]: json.loads(line)
                      for line in probe_file.read_text().splitlines()}
        result = score(directory, cases, runs, probes)
        (directory / "results.json").write_text(json.dumps(result, indent=1,
                                                           ensure_ascii=False) + "\n")
        print(json.dumps({k: v for k, v in result.items() if k != "runs"}, indent=1,
                         ensure_ascii=False))
        return 0
    except (RealWorldError, edgar_client.EdgarError) as exc:
        print(f"real_world_test: {exc}", file=sys.stderr)
        return BAD_INPUT


def _served(run: Path) -> str | None:
    manifest = run / "input_manifest.json"
    if not manifest.is_file():
        return None
    agent = (json.loads(manifest.read_text()).get("agents") or {}).get("accounting-analyst") or {}
    return agent.get("model_served")


if __name__ == "__main__":
    raise SystemExit(interpreter_pin.enforce() or main())
