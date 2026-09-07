"""8-K item codes for every filing, and the text of the ones that matter.

Three jobs, from the input spec's table:

1. **Item codes and dates for every 8-K**, read from the stored submissions
   index. The index is the only place a filing's item codes are stated — the
   document itself carries them as prose — and `src/fetch_fixtures.py` stores
   it as `tests/fixtures/{ticker}/submissions.json`.
2. **Item 2.02**, the earnings release: paragraphs and tables from exhibit
   99.1. This is the first-reported value and the only source for guidance
   language.
3. **Verbatim bodies** for items 1.01, 4.01, 4.02 and 5.02 — covenant
   amendment, auditor change, non-reliance, officer departure — taken whole
   from the 8-K body, with no selection. A 4.02 non-reliance body is the event
   the accounting-reliability question exists to anticipate.

Every other item (5.07, 7.01, 8.01, 9.01) contributes its code and date only.

    python3.12 -m src.parse_8k --ticker AAPL --out input_8k.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    from src import cutoff_guard, html_text, interpreter_pin
except ImportError:  # invoked as a plain script
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import cutoff_guard, html_text, interpreter_pin

BAD_INPUT = 2

ITEM_CODE = re.compile(r"^\d+\.\d{2}$")
VERBATIM_ITEMS = ("1.01", "4.01", "4.02", "5.02")
EARNINGS_ITEM = "2.02"

# An item heading in an 8-K body: "Item 5.02 Departure of Directors…".
_BODY_ITEM = re.compile(r"^item\s*(\d+\.\d{2})\b")
_BODY_END = re.compile(r"^signatures?\b|^exhibit index\b")


def item_codes(items: str) -> list[str]:
    """The submissions index's `items` field, as codes. Nothing else is a code."""
    return [code for code in
            (part.strip() for part in (items or "").split(",")) if code]


def submissions(ticker: str, *, fixtures_root=cutoff_guard.FIXTURES) -> dict:
    """The stored submissions index, read through `cutoff_guard.load_index`.

    An index of filings is not itself a filing, so the date gate does not apply
    to the file — see that function. The cutoff applies to the rows, and
    `eight_k_filings` is where it is applied.
    """
    row = cutoff_guard.one_document(ticker, "submissions", "submissions_index",
                                    fixtures_root=fixtures_root)
    return json.loads(cutoff_guard.load_index(row["full_path"],
                                              fixtures_root=fixtures_root))


def eight_k_filings(index: dict, cutoff=None) -> list[dict]:
    """Every 8-K in the index filed at or before the cutoff, newest first.

    The filter is the look-ahead check: the index lists what the company has
    filed to date, and a bundle whose cutoff is earlier than that must not learn
    from it that a later 8-K exists.
    """
    limit = str(cutoff) if cutoff is not None else None
    found = []
    for row in index.get("filings", []):
        if row.get("form") != "8-K":
            continue
        if limit is not None and row["filing_date"] > limit:
            continue
        found.append({"accession": row["accession"],
                      "filing_date": row["filing_date"],
                      "items": item_codes(row.get("items", ""))})
    found.sort(key=lambda row: (row["filing_date"], row["accession"]), reverse=True)
    return found


def body_items(html: str) -> dict[str, dict]:
    """Each numbered item in an 8-K body, whole, keyed by its code."""
    text = html_text.strip_tags(html)
    line_spans = html_text.lines(text)
    marks = []
    for start, end in line_spans:
        match = _BODY_ITEM.match(html_text.normalized(text[start:end]))
        if match:
            marks.append((start, match.group(1)))
    stop_at = next((start for start, end in line_spans
                    if _BODY_END.match(html_text.normalized(text[start:end]))
                    and (not marks or start > marks[-1][0])), len(text))

    found: dict[str, dict] = {}
    for index, (start, code) in enumerate(marks):
        end = marks[index + 1][0] if index + 1 < len(marks) else stop_at
        body = text[start:end].strip()
        # A filer may name the same item twice (a heading and a cross
        # reference); the first occurrence carries the body.
        found.setdefault(code, {
            "code": code,
            "text": body,
            "paragraphs": [body[a:b] for a, b in html_text.spans(body)],
        })
    return found


def extract(ticker: str, *, cutoff=None, fixtures_root=cutoff_guard.FIXTURES) -> dict:
    cutoff = cutoff or cutoff_guard.default_cutoff(ticker, fixtures_root=fixtures_root)
    index = submissions(ticker, fixtures_root=fixtures_root)
    filings = eight_k_filings(index, cutoff)

    held = cutoff_guard.one_document(ticker, "8-K", "primary_html",
                                     fixtures_root=fixtures_root)
    exhibit = cutoff_guard.one_document(ticker, "8-K", "exhibit_99_1",
                                        fixtures_root=fixtures_root)
    accession = held["accession"]

    exhibit_html = cutoff_guard.load_document(exhibit["full_path"], cutoff,
                                              fixtures_root=fixtures_root)
    body_html = cutoff_guard.load_document(held["full_path"], cutoff,
                                           fixtures_root=fixtures_root)

    release = html_text.paragraphs(exhibit_html)
    release_tables = html_text.tables(exhibit_html)
    items = body_items(body_html)

    verbatim, body_paragraphs = {}, []
    for code in VERBATIM_ITEMS:
        if code in items:
            first = len(body_paragraphs) + 1
            body_paragraphs.extend(items[code]["paragraphs"])
            verbatim[code] = {
                "code": code,
                "paragraphs": items[code]["paragraphs"],
                "paragraph_ids": [f"{accession}:8k_body:{index}" for index in
                                  range(first, len(body_paragraphs) + 1)],
            }

    return {
        "ticker": ticker,
        "cutoff": str(cutoff),
        "accession": accession,
        "filing_date": held["filing_date"],
        "held_items": item_codes(held.get("items", "")),
        "filings": filings,
        "item_2_02": {
            "paragraphs": release,
            "paragraph_ids": [f"{accession}:8k_2_02:{index}"
                              for index in range(1, len(release) + 1)],
            "tables": release_tables,
        },
        "verbatim_items": verbatim,
        "body_item_codes": sorted(items),
    }


def render(payload: dict) -> str:
    out = [f"# {payload['ticker']} 8-K — {payload['accession']} "
           f"filed {payload['filing_date']}", ""]
    out.append(f"## item codes, every 8-K on or before {payload['cutoff']}")
    out.append("")
    for row in payload["filings"]:
        out.append(f"- {row['filing_date']} {row['accession']} — "
                   f"{', '.join(row['items']) or '(none recorded)'}")
    out.append("")

    out.append("## item 2.02 — earnings release, exhibit 99.1")
    out.append("")
    for paragraph_id, paragraph in zip(payload["item_2_02"]["paragraph_ids"],
                                       payload["item_2_02"]["paragraphs"]):
        out.append(f"[{paragraph_id}]")
        out.append(paragraph)
        out.append("")
    for number, table in enumerate(payload["item_2_02"]["tables"], start=1):
        out.append(f"[{payload['accession']}:8k_2_02_table:{number}]")
        out.extend(html_text.pipe_rows(table))
        out.append("")

    for code in VERBATIM_ITEMS:
        item = payload["verbatim_items"].get(code)
        if item is None:
            continue
        out.append(f"## item {code} — body, verbatim")
        out.append("")
        for paragraph_id, paragraph in zip(item["paragraph_ids"], item["paragraphs"]):
            out.append(f"[{paragraph_id}]")
            out.append(paragraph)
            out.append("")
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="8-K item codes, earnings release, bodies")
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--cutoff", default=None)
    parser.add_argument("--fixtures", default=str(cutoff_guard.FIXTURES))
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)

    try:
        payload = extract(args.ticker.upper(), cutoff=args.cutoff,
                          fixtures_root=Path(args.fixtures))
    except cutoff_guard.CutoffGuardError as exc:
        print(f"parse_8k: {exc}", file=sys.stderr)
        return BAD_INPUT
    Path(args.out).write_text(render(payload), encoding="utf-8")
    print(f"parse_8k: {args.ticker.upper()} {len(payload['filings'])} 8-K filings, "
          f"{len(payload['item_2_02']['paragraphs'])} release paragraphs, "
          f"{len(payload['item_2_02']['tables'])} tables, "
          f"verbatim {sorted(payload['verbatim_items']) or 'none'} → {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(interpreter_pin.enforce() or main())
