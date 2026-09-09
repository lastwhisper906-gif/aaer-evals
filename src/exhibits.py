"""Exhibit 21 — the subsidiary list — found by what the submission says it is.

`docs/INPUT_SPEC.md` §1 carries one line for this: *Exhibit 21, subsidiaries,
every 10-K, diffed — exhibit type from the submission's SGML header, never the
filename.* That last clause is the whole of the difficulty, and it is written
there because this project already lost a session to the other way round: the
8-K earnings release was picked by matching the filename and it found five of
twelve, because a filer may call `EX-99.1` anything at all.

**The filename is the filer's; the type is EDGAR's.** EDGAR republishes the
submission's own SGML header at `{accession}-index-headers.html`, one
`<DOCUMENT>` block per file:

    <DOCUMENT>
    <TYPE>EX-21.1
    <SEQUENCE>3
    <FILENAME>a10-kexhibit21109272025.htm
    <DESCRIPTION>EX-21.1

`<TYPE>` is the exhibit's type as the submission declares it. Everything else on
that block is the filer's own choice, `<DESCRIPTION>` included — Cisco's says
`SUBSIDIARIES OF THE REGISTRANT`, Generac's says `EXHIBIT 21.1`, Apple's says
`EX-21.1`, and all three are the same kind of document.

**What the filenames do in this fixture set**, which is why none of them is read
to decide anything. Generac files the exhibit as `ex_873991.htm` and NVIDIA as
`subsidiariesofregistrantfy.htm`, so a rule looking for `21` in the name never
reaches the exhibit for two of the twelve — and it does not come back
empty-handed either, because a Section 1350 certification is `EX-32.1` and gets
filed as `nvda-2026xex321.htm`. That is the general case, not the exception:
in twenty-two of these twenty-four submissions more than one filename carries
`21`, and in Apple's and Qualcomm's prior years one of them is an `EX-10.21`
material contract. `tests/test_exhibits.py` counts all of that rather than
leaving it as a claim here.

**Two types, not one.** Carrier, Qualcomm and ESCO file it as `EX-21`; the other
nine file it as `EX-21.1`. A match on the literal string `EX-21.1` finds nine of
twelve, so the rule is the `EX-21` family — the bare type or the type with a
suffix — and `is_subsidiary_exhibit` is where that is written down.

**Heading rows.** An Exhibit 21 is a table of name and jurisdiction, and most of
these twelve open it with a row of column labels: `Subsidiary` against `State or
Country of Incorporation or Organization`. Seagate's has no heading row at all,
so dropping the first row of the table would delete a real subsidiary. A row is
therefore dropped only when **both** of its first two cells read as column
labels, by the word list in `COLUMN_LABEL_WORDS` — a name cell reading
`Qualcomm Incorporated` beside a jurisdiction cell reading `Delaware` is kept,
because `Delaware` names no column. The list grows by adding a word when one
turns up, never by widening it into a shape.

**No fetcher here.** `src/fetch_fixtures.py` is the one module in `src/` that
talks to EDGAR, and it is the one module besides the gate that
`tests/test_cutoff_guard.py`'s bypass scan exempts, because it is upstream of
the gate rather than behind it. A second fetcher inside a reader would put a
fixture writer behind the gate. The four documents per company this module reads
were fetched from `HEADER_URL` and `ARCHIVE_URL` below and recorded in each
company's `manifest.json` with the url and the sha256 of the bytes EDGAR served,
which `tests/test_fixtures.py` re-checks on every run. Rebuilding the fixture set
from nothing still needs those two roles added to `src/fetch_fixtures.py`, which
this branch may not touch.

    python3.12 -m src.exhibits --ticker AAPL --out input_exhibits.md
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    from src import cutoff_guard, diff_periods, html_text, interpreter_pin
except ImportError:  # invoked as a plain script
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import cutoff_guard, diff_periods, html_text, interpreter_pin

BAD_INPUT = 2

# Where the two documents come from. Recorded here because the manifest records
# them per company and a reader of this file should not have to open one.
HEADER_URL = ("https://www.sec.gov/Archives/edgar/data/{cik}/{accession}/"
              "{dashed}-index-headers.html")
ARCHIVE_URL = "https://www.sec.gov/Archives/edgar/data/{cik}/{accession}/{name}"

# (submission header, exhibit) for the 10-K on record and the one before it.
ROLE_PAIRS = (("submission_header", "exhibit_21"),
              ("prior_year_submission_header", "prior_year_exhibit_21"))

# One `<DOCUMENT>` block of the header page, as EDGAR escapes it for the browser.
# The bare `<TYPE>` form is matched too, because the same header text appears
# unescaped inside the page's HTML comment and in the raw `.hdr.sgml`.
DOCUMENT_BLOCK = re.compile(
    r"(?:<|&lt;)TYPE(?:>|&gt;)\s*(?P<type>\S+)\s*\n"
    r"(?:<|&lt;)SEQUENCE(?:>|&gt;)\s*(?P<sequence>\S+)\s*\n"
    r"(?:<|&lt;)FILENAME(?:>|&gt;)\s*(?P<filename>\S+)",
    re.IGNORECASE)

SUBSIDIARY_EXHIBIT = "EX-21"

# Characters a filer uses as an empty cell that `str.strip()` leaves alone:
# zero-width space, byte-order mark, soft hyphen. ESCO's exhibit spaces its
# columns with the first of them, so without this every row reads as five cells.
BLANK_CHARACTERS = "\u200b\ufeff\u00ad"

# Words that appear in the column labels of an Exhibit 21 and never in a
# jurisdiction. A row is a heading only when its first two cells both carry one,
# so a subsidiary called `... Incorporated` in `Delaware` is not one.
COLUMN_LABEL_WORDS = ("jurisdiction", "incorporation", "organization",
                      "subsidiar", "name")


class ExhibitError(Exception):
    """The exhibit cannot be read from what the submission and the record say."""


# --- the submission header ---------------------------------------------------

def document_types(header: str) -> list[dict]:
    """Every document the submission header declares: type, sequence, filename.

    The type is upper-cased because EDGAR writes it that way and a comparison
    should not depend on that; the filename is left exactly as the header has it,
    since it is what the archive is addressed by.
    """
    return [{"type": found.group("type").upper(),
             "sequence": found.group("sequence"),
             "filename": found.group("filename")}
            for found in DOCUMENT_BLOCK.finditer(header)]


def is_subsidiary_exhibit(kind: str) -> bool:
    """True for `EX-21` and for `EX-21` with a suffix, and for nothing else.

    `EX-21.1` and `EX-21` are both in this fixture set. `EX-10.21` is not: it is
    a material contract whose number happens to end in the same two digits, and
    Apple's and Qualcomm's prior-year submissions both carry one.
    """
    upper = kind.upper()
    return upper == SUBSIDIARY_EXHIBIT or upper.startswith(SUBSIDIARY_EXHIBIT + ".")


def named_exhibit(header: str) -> dict:
    """The one document in the submission whose declared type is the EX-21 family.

    Exactly one, or a refusal. A submission with none has no subsidiary list to
    read, and a submission with two does not say which is the list.
    """
    found = [entry for entry in document_types(header)
             if is_subsidiary_exhibit(entry["type"])]
    if len(found) != 1:
        raise ExhibitError(
            f"the submission header declares {len(found)} documents of the "
            f"{SUBSIDIARY_EXHIBIT} family, and the exhibit is the one it names: "
            f"{[entry['type'] for entry in found]}")
    return found[0]


# --- the exhibit -------------------------------------------------------------

def _cell(text: str) -> str:
    """One table cell, edge-trimmed, with a filler-only cell reading as empty."""
    return text.strip().strip(BLANK_CHARACTERS).strip()


def is_column_label(text: str) -> bool:
    """True for text that names a column of an Exhibit 21 rather than a value."""
    lowered = text.lower()
    return any(word in lowered for word in COLUMN_LABEL_WORDS)


def subsidiaries(html: str) -> list[dict]:
    """Every subsidiary the exhibit lists, in the exhibit's own order.

    A row contributes one subsidiary when it has two or more cells with text in
    them: the first is the name, the second the jurisdiction. Filers space the
    columns with empty cells, and how many of them differs by filer, so the
    number of cells in a row is not the number of columns and cannot be matched
    on.
    """
    found = []
    for table in html_text.tables(html):
        for row in table:
            filled = [text for text in (_cell(cell) for cell in row) if text]
            if len(filled) < 2:
                continue
            name, jurisdiction = filled[0], filled[1]
            if is_column_label(name) and is_column_label(jurisdiction):
                continue
            found.append({"name": name, "jurisdiction": jurisdiction})
    return found


def _key(entry: dict) -> str:
    """What makes two rows the same subsidiary: the name, whitespace flattened.

    Flattened because a filer re-flows the same name across two lines from one
    year to the next; case is left alone, so a renamed capital is a change.
    """
    return html_text.normalized_spacing(entry["name"])


def diff(current: list[dict], prior: list[dict]) -> dict:
    """What the subsidiary list gained, lost and moved since the prior 10-K.

    Matched as a **multiset** by `src/diff_periods.py::match_paragraphs`, which
    is where that rule lives: a company that lists the same name twice has two
    entries and loses one of them when one goes, rather than the second
    collapsing onto the first. That module learned the expensive way what an
    index lookup does to a repeated line, and the rule is not worth writing
    twice.

    What is matched on is the name alone, so a subsidiary whose jurisdiction
    moved pairs with itself and is reported as a move rather than as one
    subsidiary gained and one lost. What is left over on either side comes back
    in the order its own exhibit lists it, which is the order `sections` renders.
    """
    paired = diff_periods.match_paragraphs([_key(entry) for entry in current],
                                           [_key(entry) for entry in prior])

    moved, unchanged = [], 0
    for now, before in paired["matched"]:
        this_year, last_year = current[now], prior[before]
        if this_year["jurisdiction"] == last_year["jurisdiction"]:
            unchanged += 1
        else:
            moved.append({"name": this_year["name"],
                          "prior_jurisdiction": last_year["jurisdiction"],
                          "jurisdiction": this_year["jurisdiction"]})

    return {"added": [current[index] for index in paired["added"]],
            "removed": [prior[index] for index in paired["removed"]],
            "jurisdiction_changed": moved, "unchanged": unchanged,
            "current_count": len(current), "prior_count": len(prior)}


# --- what is on record -------------------------------------------------------

def filings(ticker: str, *, cutoff, fixtures_root=cutoff_guard.FIXTURES) -> list[dict]:
    """The 10-K submissions whose Exhibit 21 is on record, newest first.

    A submission filed after the cutoff is not on record for this run — a 10-K
    published after the report that triggered it is exactly the look-ahead the
    gate exists for, and dropping it here is what lets an earlier cutoff read
    the earlier 10-K as the current one.
    """
    limit = str(cutoff)
    found = []
    for header_role, exhibit_role in ROLE_PAIRS:
        header = cutoff_guard.documents(ticker, form="10-K", role=header_role,
                                        fixtures_root=fixtures_root)
        exhibit = cutoff_guard.documents(ticker, form="10-K", role=exhibit_role,
                                         fixtures_root=fixtures_root)
        if not header or not exhibit:
            continue
        if len(header) != 1 or len(exhibit) != 1:
            raise ExhibitError(
                f"{ticker}: {header_role} and {exhibit_role} name "
                f"{len(header)} and {len(exhibit)} documents, and one submission "
                f"has one of each")
        if header[0]["accession"] != exhibit[0]["accession"]:
            raise ExhibitError(
                f"{ticker}: {exhibit_role} is from {exhibit[0]['accession']} and "
                f"{header_role} from {header[0]['accession']} — an exhibit is "
                f"read through its own submission's header, not another's")
        if header[0]["filing_date"] > limit:
            continue
        found.append({"header": header[0], "exhibit": exhibit[0]})
    found.sort(key=lambda pair: (pair["header"]["filing_date"],
                                 pair["header"]["accession"]), reverse=True)
    return found


def read_exhibit(pair: dict, *, cutoff, fixtures_root=cutoff_guard.FIXTURES) -> dict:
    """The subsidiary list of one 10-K, located through that 10-K's own header.

    The header names the file; the record has to hold that file and no other.
    Checking it here is what makes "never the filename" a property of the run
    rather than of the day the fixture was fetched — a stored document that is
    not the one the header names is refused instead of parsed.
    """
    header_text = cutoff_guard.load_document(pair["header"]["full_path"], cutoff,
                                             fixtures_root=fixtures_root)
    named = named_exhibit(header_text)
    stored = Path(pair["exhibit"]["path"]).name
    if stored != named["filename"]:
        raise ExhibitError(
            f"{pair['exhibit']['accession']}: the submission header names "
            f"{named['filename']} as its {named['type']} and the record holds "
            f"{stored}")
    html = cutoff_guard.load_document(pair["exhibit"]["full_path"], cutoff,
                                      fixtures_root=fixtures_root)
    return {"accession": pair["exhibit"]["accession"],
            "filing_date": pair["exhibit"]["filing_date"],
            "type": named["type"],
            "sequence": named["sequence"],
            "filename": named["filename"],
            "subsidiaries": subsidiaries(html)}


def extract(ticker: str, *, cutoff=None, fixtures_root=cutoff_guard.FIXTURES) -> dict:
    """Exhibit 21 for the latest 10-K on record, diffed against the one before."""
    cutoff = cutoff or cutoff_guard.default_cutoff(ticker, fixtures_root=fixtures_root)
    on_record = filings(ticker, cutoff=cutoff, fixtures_root=fixtures_root)
    if not on_record:
        raise ExhibitError(
            f"{ticker}: no 10-K with an Exhibit 21 on record at or before {cutoff}")

    current = read_exhibit(on_record[0], cutoff=cutoff, fixtures_root=fixtures_root)
    prior = (read_exhibit(on_record[1], cutoff=cutoff, fixtures_root=fixtures_root)
             if len(on_record) > 1 else None)
    return {
        "ticker": ticker,
        "cutoff": str(cutoff),
        "exhibit": current,
        "prior_exhibit": prior,
        # `docs/INPUT_SPEC.md` §2: the first filing for a company is read whole.
        "diff": diff(current["subsidiaries"], prior["subsidiaries"]) if prior else None,
    }


# --- what the notes-text reader sees -----------------------------------------

def row(entry: dict) -> str:
    """One subsidiary as a `|`-delimited row, the shape `docs/INPUT_SPEC.md` §2
    asks a table to arrive in. `html_text.pipe_rows` renders the same way."""
    return html_text.pipe_rows([[entry["name"], entry["jurisdiction"]]])[0]


def moved_row(entry: dict) -> str:
    return html_text.pipe_rows([[entry["name"], entry["prior_jurisdiction"],
                                 entry["jurisdiction"]]])[0]


def sections(payload: dict) -> list[tuple[str, list[str]]]:
    """(heading, rows) for the body of the file, in the order it is read.

    One list of sections whether or not there is a prior 10-K, so the paragraph
    ids are numbered once and the file has one shape.
    """
    changes = payload["diff"]
    if changes is None:
        # `docs/INPUT_SPEC.md` §2: the first filing on record is read whole.
        return [("subsidiaries in this 10-K, carried whole",
                 [row(entry) for entry in payload["exhibit"]["subsidiaries"]])]
    return [
        ("subsidiaries added since the prior 10-K",
         [row(entry) for entry in changes["added"]]),
        ("subsidiaries dropped since the prior 10-K",
         [row(entry) for entry in changes["removed"]]),
        ("subsidiaries whose jurisdiction changed — name, the prior 10-K's "
         "jurisdiction, this one's",
         [moved_row(entry) for entry in changes["jurisdiction_changed"]]),
    ]


def counts(payload: dict) -> str:
    """The one arithmetic line. Python does it; nobody downstream re-counts."""
    changes = payload["diff"]
    if changes is None:
        return (f"{len(payload['exhibit']['subsidiaries'])} subsidiaries in this "
                "10-K, and no earlier 10-K to diff against")
    return (f"{changes['current_count']} subsidiaries in this 10-K against "
            f"{changes['prior_count']} in the prior: {len(changes['added'])} added, "
            f"{len(changes['removed'])} dropped, "
            f"{len(changes['jurisdiction_changed'])} with a changed jurisdiction, "
            f"{changes['unchanged']} unchanged")


def names_line(label: str, exhibit: dict) -> str:
    """What the submission header said, for one of the two 10-Ks."""
    return (f"- {label} {exhibit['accession']} filed {exhibit['filing_date']}: "
            f"type {exhibit['type']}, document {exhibit['sequence']}, "
            f"file {exhibit['filename']}")


def render(payload: dict) -> str:
    current, prior = payload["exhibit"], payload["prior_exhibit"]
    accession = current["accession"]
    out = [f"# {payload['ticker']} Exhibit 21 — subsidiaries of the registrant", "",
           "## the exhibit each submission header names", "",
           names_line("10-K", current),
           names_line("prior 10-K", prior) if prior else
           f"- no earlier 10-K on record at or before {payload['cutoff']}",
           "", "The type is the `<TYPE>` line of each submission's own SGML header. "
           "No document here was chosen by the name of its file.", ""]

    # Below the first id, every line this module writes is a `#` heading and
    # every other line is a subsidiary row. `assemble_bundle.paragraph_blocks`
    # skips headings and folds anything else into the block of the id above it,
    # so an empty section and the counts sentence ride on their own headings:
    # otherwise they would land inside the last row's block and a quote gate
    # would match a reader quoting arithmetic against a subsidiary's id.
    number = 0
    for title, rows in sections(payload):
        out.extend([f"## {title}" if rows else f"## {title} (none)", ""])
        for line in rows:
            number += 1
            out.extend([f"[{accession}:exhibits:{number}]", line, ""])
    out.extend([f"## counts — {counts(payload)}", ""])
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Exhibit 21 subsidiaries, located by the submission header and diffed")
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--cutoff", default=None)
    parser.add_argument("--fixtures", default=str(cutoff_guard.FIXTURES))
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)

    ticker = args.ticker.upper()
    try:
        payload = extract(ticker, cutoff=args.cutoff,
                          fixtures_root=Path(args.fixtures))
    except (cutoff_guard.CutoffGuardError, ExhibitError) as exc:
        print(f"exhibits: {exc}", file=sys.stderr)
        return BAD_INPUT
    Path(args.out).write_text(render(payload), encoding="utf-8")

    current, changes = payload["exhibit"], payload["diff"]
    tail = (f"{len(changes['added'])} added, {len(changes['removed'])} dropped, "
            f"{len(changes['jurisdiction_changed'])} moved"
            if changes else "no earlier 10-K to diff against")
    print(f"exhibits: {ticker} {current['type']} {current['filename']} "
          f"({current['accession']}), {len(current['subsidiaries'])} subsidiaries, "
          f"{tail} → {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(interpreter_pin.enforce() or main())
