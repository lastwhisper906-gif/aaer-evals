"""blind_memo_verify.py — GIL blind-memo experiment: programmatic citation check (Step 3).

For every verbatim quote in the evaluatee's flag output, string-match against the
extracted filing text (data/gil/*.txt). No LLM judgment — pure matching.

Classification:
  VERIFIED : normalized exact substring, or best fuzzy window similarity >= 0.95
  ALTERED  : best similarity >= 0.80 (< 0.95) — passage found but wording changed
  NOT FOUND: best similarity < 0.80 — treat as hallucinated

Normalization for matching only: collapse whitespace, unify quotes/dashes,
drop table-cell pipes. Fuzzy = difflib ratio over sliding windows with a
quick_ratio prefilter.

Usage: python tools/blind_memo_verify.py runs/gil_memo_v1/flags_combined.json
Output: <input dir>/citation_verification.json (+ prints a markdown table)
"""
from __future__ import annotations

import difflib
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DATA = REPO / "data" / "gil"

DOC_FILES = [
    "40F_2026-02-26_body.txt",
    "40F_2026-02-26_ex99-2_financial_statements.txt",
    "40F_2026-02-26_ex99-1_mda.txt",
    "40F_2026-02-26_ex99-3_aif.txt",
    "6K_2026-04-30_body.txt",
    "6K_2026-04-30_ex99-2_interim_financial_statements.txt",
    "6K_2026-04-30_ex99-1_interim_mda.txt",
]


def normalize(s: str) -> str:
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-").replace("|", " ")
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()


def best_window(quote: str, corpus: str) -> tuple[float, int]:
    """Best difflib ratio of quote vs sliding windows over corpus; returns (ratio, pos)."""
    L = len(quote)
    if L == 0 or L > len(corpus):
        return 0.0, -1
    win = int(L * 1.25) + 8
    step = max(1, L // 4)
    best, best_pos = 0.0, -1
    sm = difflib.SequenceMatcher(autojunk=False)
    sm.set_seq2(quote)  # seq2 is cached
    for pos in range(0, len(corpus) - L + 1, step):
        chunk = corpus[pos:pos + win]
        sm.set_seq1(chunk)
        if sm.real_quick_ratio() < best or sm.quick_ratio() < max(best, 0.6):
            continue
        r = sm.ratio()
        if r > best:
            best, best_pos = r, pos
    return best, best_pos


def check_quote(quote: str, corpora: dict[str, str]) -> dict:
    q = normalize(quote)
    result = {"exact": False, "similarity": 0.0, "matched_doc": None}
    for name, corpus in corpora.items():
        if q in corpus:
            return {"exact": True, "similarity": 1.0, "matched_doc": name}
    for name, corpus in corpora.items():
        r, _ = best_window(q, corpus)
        if r > result["similarity"]:
            result.update(similarity=round(r, 3), matched_doc=name)
    return result


def status_of(res: dict) -> str:
    if res["exact"] or res["similarity"] >= 0.95:
        return "VERIFIED"
    if res["similarity"] >= 0.80:
        return "ALTERED"
    return "NOT FOUND"


def main() -> int:
    flags_path = Path(sys.argv[1] if len(sys.argv) > 1
                      else REPO / "runs" / "gil_memo_v1" / "flags_combined.json")
    flags = json.loads(flags_path.read_text(encoding="utf-8"))["flags"]
    corpora = {f: normalize((DATA / f).read_text(encoding="utf-8")) for f in DOC_FILES}

    rows, n_verified = [], 0
    for fi, flag in enumerate(flags, 1):
        for qi, q in enumerate(flag["quotes"], 1):
            res = check_quote(q["text"], corpora)
            st = status_of(res)
            n_verified += st == "VERIFIED"
            rows.append({"flag": fi, "flag_title": flag["title"], "quote_no": qi,
                         "quote": q["text"], "claimed_location": q["location"],
                         "status": st, **res})

    out = flags_path.parent / "citation_verification.json"
    out.write_text(json.dumps({"source": str(flags_path.name), "quotes": len(rows),
                               "verified": n_verified, "rows": rows}, indent=2) + "\n",
                   encoding="utf-8")
    print(f"{n_verified}/{len(rows)} VERIFIED — detail: {out}\n")
    print("| # | Quote (truncated) | Claimed location | Status | Sim | Matched doc |")
    print("|---|---|---|---|---|---|")
    for r in rows:
        qt = (r["quote"][:60] + "…") if len(r["quote"]) > 60 else r["quote"]
        qt = qt.replace("|", "\\|")
        print(f"| {r['flag']}.{r['quote_no']} | {qt} | {r['claimed_location']} "
              f"| {r['status']} | {r['similarity']} | {r['matched_doc']} |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
