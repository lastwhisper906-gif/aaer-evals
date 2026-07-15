"""blind_memo_extract.py — GIL blind-memo experiment: filing HTML -> text (D-, consumable output v1).

Extracts table-aware plain text from EDGAR filing HTML for the evaluatee payload.
All document loads route through pipeline/cutoff_guard.load_document() with the
experiment-local registry data/gil/registry.json (case OUT-GIL-V1, cutoff
2026-06-15) and accession cross-check against ~/aaer-data/GIL/edgar/ submissions
JSON. Raw HTML lives outside git (~/aaer-data/GIL/edgar/<accession>/ per
data/README.md); extracted text lands in data/gil/.

Table handling: <tr> -> one line, cells joined with " | " so financial-statement
rows stay readable and quotable. display:none elements (hidden iXBRL header
facts) are dropped.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "pipeline"))
from cutoff_guard import load_document  # noqa: E402

REGISTRY = REPO / "data" / "gil" / "registry.json"
OUT_DIR = REPO / "data" / "gil"
RAW_DIR = Path.home() / "aaer-data" / "GIL" / "edgar"
CASE_ID = "OUT-GIL-V1"

# (accession, filing_date, form, source file, output name)
DOCS = [
    ("0001061894-26-000006", "2026-02-26", "40-F",
     "gil-20251228.htm", "40F_2026-02-26_body.txt"),
    ("0001061894-26-000006", "2026-02-26", "40-F",
     "gil-20251228_d2.htm", "40F_2026-02-26_ex99-2_financial_statements.txt"),
    ("0001061894-26-000006", "2026-02-26", "40-F",
     "exhibit991-mdax2025.htm", "40F_2026-02-26_ex99-1_mda.txt"),
    ("0001061894-26-000006", "2026-02-26", "40-F",
     "exhibit993-annualinformati.htm", "40F_2026-02-26_ex99-3_aif.txt"),
    ("0001061894-26-000013", "2026-04-30", "6-K",
     "form6-kxinterimfilingq12026.htm", "6K_2026-04-30_body.txt"),
    ("0001061894-26-000013", "2026-04-30", "6-K",
     "exhibit992q12026fs.htm", "6K_2026-04-30_ex99-2_interim_financial_statements.txt"),
    ("0001061894-26-000013", "2026-04-30", "6-K",
     "exhibit991q12026mda.htm", "6K_2026-04-30_ex99-1_interim_mda.txt"),
]

BLOCK_TAGS = {"p", "div", "table", "h1", "h2", "h3", "h4", "h5", "h6",
              "li", "ul", "ol", "section", "article"}


class FilingTextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self._skip_depth = 0
        self._hidden_stack: list[str] = []
        self._in_row = False
        self._cell: list[str] = []
        self._row: list[str] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        style = (a.get("style") or "").replace(" ", "").lower()
        if tag in ("script", "style") or "display:none" in style:
            self._skip_depth += 1
            self._hidden_stack.append(tag)
            return
        if self._skip_depth:
            return
        if tag == "tr":
            self._in_row, self._row, self._cell = True, [], []
        elif tag in ("td", "th"):
            self._cell = []
        elif tag == "br":
            (self._cell if self._in_row else self.out).append("\n")
        elif tag in BLOCK_TAGS and not self._in_row:
            self.out.append("\n")

    def handle_endtag(self, tag):
        if self._hidden_stack and tag == self._hidden_stack[-1]:
            self._hidden_stack.pop()
            self._skip_depth -= 1
            return
        if self._skip_depth:
            return
        if tag in ("td", "th"):
            cell = re.sub(r"\s+", " ", "".join(self._cell)).strip()
            self._row.append(cell)
            self._cell = []
        elif tag == "tr":
            self._in_row = False
            line = " | ".join(c for c in self._row if c)
            if line:
                self.out.append("\n" + line)
        elif tag in BLOCK_TAGS and not self._in_row:
            self.out.append("\n")

    def handle_data(self, data):
        if self._skip_depth:
            return
        (self._cell if self._in_row else self.out).append(data)


def html_to_text(html: str) -> str:
    p = FilingTextExtractor()
    p.feed(html)
    text = "".join(p.out)
    text = text.replace(" ", " ").replace("’", "'").replace("‘", "'")
    text = text.replace("“", '"').replace("”", '"')
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" ?\n ?", "\n", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest = []
    for accession, filing_date, form, src, dst in DOCS:
        raw_path = RAW_DIR / accession / src
        html = load_document(CASE_ID, str(raw_path), filing_date,
                             accession_no=accession, registry_path=REGISTRY)
        text = html_to_text(html)
        (OUT_DIR / dst).write_text(text, encoding="utf-8")
        nod = accession.replace("-", "")
        manifest.append({
            "form": form, "filing_date": filing_date, "accession": accession,
            "source_file": src, "extracted_file": dst,
            "url": f"https://www.sec.gov/Archives/edgar/data/1061894/{nod}/{src}",
            "raw_sha256": hashlib.sha256(html.encode()).hexdigest(),
            "chars": len(text),
        })
        print(f"{dst}: {len(text):,} chars")
    (OUT_DIR / "manifest.json").write_text(
        json.dumps({"case_id": CASE_ID, "cik": "0001061894",
                    "cutoff_last_permitted_filing_date": "2026-06-15",
                    "documents": manifest}, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
