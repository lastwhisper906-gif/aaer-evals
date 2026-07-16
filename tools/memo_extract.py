"""memo_extract.py — 티커 일반화 추출기 (blind_memo_extract.py의 매개변수화 후계, P1).

blind_memo_extract.py는 OUT-GIL-V1 기록으로 동결 — 본 파일은 문서 로스터·경로를
설정 파일로 받는다. HTML→텍스트 변환(FilingTextExtractor·html_to_text)은 바이트
동일 상속 (tools/test_memo_pipeline.py가 소스 동일성을 강제).

설정 파일 형식 (data/<ticker>/extract_docs.json):
  {"case_id": "OUT-<T>-V1", "cik": "0000000000",
   "cutoff_last_permitted_filing_date": "YYYY-MM-DD",
   "raw_dir": "<TICKER>/edgar",   # ~/aaer-data/ 하위 상대 경로
   "docs": [{"accession","filing_date","form","source_file","extracted_file"}...]}

Usage: python tools/memo_extract.py --config data/<t>/extract_docs.json \
           --registry data/<t>/registry.json --out-dir data/<t>
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "pipeline"))
from cutoff_guard import load_document  # noqa: E402

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
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True, type=Path)
    ap.add_argument("--registry", required=True, type=Path)
    ap.add_argument("--out-dir", required=True, type=Path)
    ap.add_argument("--raw-root", type=Path, default=Path.home() / "aaer-data",
                    help="원문 HTML 루트 (기본 ~/aaer-data — git 밖, data/README.md 규약)")
    args = ap.parse_args()

    cfg = json.loads(args.config.read_text(encoding="utf-8"))
    case_id, cik = cfg["case_id"], cfg["cik"]
    raw_dir = args.raw_root / cfg["raw_dir"]
    args.out_dir.mkdir(parents=True, exist_ok=True)

    manifest = []
    for d in cfg["docs"]:
        accession, filing_date = d["accession"], d["filing_date"]
        src, dst = d["source_file"], d["extracted_file"]
        raw_path = raw_dir / accession / src
        html = load_document(case_id, str(raw_path), filing_date,
                             accession_no=accession, registry_path=args.registry)
        text = html_to_text(html)
        (args.out_dir / dst).write_text(text, encoding="utf-8")
        nod = accession.replace("-", "")
        manifest.append({
            "form": d["form"], "filing_date": filing_date, "accession": accession,
            "source_file": src, "extracted_file": dst,
            "url": f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{nod}/{src}",
            "raw_sha256": hashlib.sha256(html.encode()).hexdigest(),
            "chars": len(text),
        })
        print(f"{dst}: {len(text):,} chars")
    (args.out_dir / "manifest.json").write_text(
        json.dumps({"case_id": case_id, "cik": cik,
                    "cutoff_last_permitted_filing_date":
                        cfg["cutoff_last_permitted_filing_date"],
                    "documents": manifest}, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
