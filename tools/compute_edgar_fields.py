"""Deterministically compute EDGAR-derived candidate fields (PROJECT.md §5-4: numbers in Python).

Reads submissions JSON fetched by fetch_primary_sources.py from ~/aaer-data/{ticker}/edgar/
and, per candidate:
  - counts pre-revelation periodic reports (filingDate strictly before first_revelation_date):
      10-K bucket = 10-K, 10-K405, 10-KT; 10-Q bucket = 10-Q, 10-QT (amendments /A excluded;
      10-KSB/10-QSB reported separately, not counted — Stage 3 convention)
  - reports FPI forms (20-F, 40-F, 6-K) separately for foreign private issuers
  - computes XBRL availability: any isXBRL=1 among counted pre-revelation filings
  - lists every filing within ±14 days of first_revelation_date (revelation-vehicle check)

Output: data/candidates/edgar_verification.json (metadata only — committable per data/README.md).

Counting is convention-bound, not judgment: where Stage 3 notes exclude pre-operating
shell/SPAC-era filings, the operating_start dates below reproduce that documented rule and
both raw and adjusted counts are emitted so a human can audit the exclusion.
"""

import json
from datetime import date, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DATA_DIR = Path.home() / "aaer-data"

TENK = {"10-K", "10-K405", "10-KT"}
TENQ = {"10-Q", "10-QT"}
SB = {"10-KSB", "10-QSB"}
FPI = {"20-F", "40-F", "6-K"}

# Documented operating-business start (reverse merger / SPAC combination) where Stage 3
# excluded pre-operating filings under the same CIK. Source: candidates.json notes.
OPERATING_START = {
    "T03": "2009-10-01",  # CCME: TM Entertainment SPAC reverse-merged Oct 2009
}

EXTRA_CIKS = {"T13": ["0001364479"]}  # predecessor Hertz entity that filed the misstated 10-Ks


def load_filings(ticker: str, cik: str) -> list[dict]:
    """All filings for a CIK as flat dicts, recent + older chunks."""
    edgar_dir = DATA_DIR / ticker / "edgar"
    cik10 = cik.zfill(10)
    main = edgar_dir / f"CIK{cik10}.json"
    if not main.exists():
        raise FileNotFoundError(main)
    j = json.loads(main.read_text(encoding="utf-8"))
    blocks = [j["filings"]["recent"]]
    for f in j["filings"].get("files", []):
        p = edgar_dir / f["name"]
        blocks.append(json.loads(p.read_text(encoding="utf-8")))
    out = []
    for b in blocks:
        n = len(b["form"])
        for i in range(n):
            out.append(
                {
                    "cik": cik10,
                    "form": b["form"][i],
                    "filingDate": b["filingDate"][i],
                    "reportDate": b["reportDate"][i],
                    "accession": b["accessionNumber"][i],
                    "primaryDocument": b.get("primaryDocument", [""] * n)[i],
                    "isXBRL": b.get("isXBRL", [0] * n)[i],
                }
            )
    return out


def summarize(case: dict) -> dict:
    ticker = case["ticker"].split("/")[0]
    ciks = [case["cik"], *EXTRA_CIKS.get(case["case_id"], [])]
    filings = []
    for cik in ciks:
        filings += load_filings(ticker, cik)
    rev = date.fromisoformat(case["first_revelation_date"])
    pre = [f for f in filings if date.fromisoformat(f["filingDate"]) < rev]

    def bucket(fs, forms):
        return sorted(
            (f for f in fs if f["form"] in forms), key=lambda f: f["filingDate"]
        )

    k, q = bucket(pre, TENK), bucket(pre, TENQ)
    counted = k + q
    result = {
        "case_id": case["case_id"],
        "ticker": ticker,
        "ciks": [c.zfill(10) for c in ciks],
        "first_revelation_date": case["first_revelation_date"],
        "recorded_quarters": case["pre_revelation_quarters_available"],
        "recorded_xbrl": case["xbrl_available"],
        "raw_10k": len(k),
        "raw_10q": len(q),
        "raw_total": len(k) + len(q),
        "sb_forms_excluded": len(bucket(pre, SB)),
        "amendments_excluded": len(
            [f for f in pre if f["form"].endswith("/A") and f["form"][:-2] in TENK | TENQ]
        ),
        "fpi_pre_revelation": {
            form: len([f for f in pre if f["form"] == form]) for form in sorted(FPI)
        },
        "xbrl_any_counted": any(f["isXBRL"] for f in counted),
        "xbrl_count": sum(1 for f in counted if f["isXBRL"]),
        "first_counted": counted and min(f["filingDate"] for f in counted) or None,
        "last_counted": counted and max(f["filingDate"] for f in counted) or None,
    }
    op = OPERATING_START.get(case["case_id"])
    if op:
        opd = date.fromisoformat(op)
        adj = [f for f in counted if date.fromisoformat(f["filingDate"]) >= opd]
        result["operating_start_applied"] = op
        result["adjusted_total"] = len(adj)
    win_lo, win_hi = rev - timedelta(days=14), rev + timedelta(days=14)
    result["revelation_window_filings"] = [
        {
            "form": f["form"],
            "filingDate": f["filingDate"],
            "reportDate": f["reportDate"],
            "cik": f["cik"],
            "accession": f["accession"],
            "primaryDocument": f["primaryDocument"],
        }
        for f in sorted(filings, key=lambda f: f["filingDate"])
        if win_lo <= date.fromisoformat(f["filingDate"]) <= win_hi
    ]
    return result


def main() -> None:
    candidates = json.loads(
        (REPO / "data/candidates/candidates.json").read_text(encoding="utf-8")
    )["candidates"]
    results, errors = [], []
    for c in candidates:
        try:
            results.append(summarize(c))
        except FileNotFoundError as e:
            errors.append(f"{c['case_id']}: missing {e}")
    out = {
        "_meta": {
            "purpose": "deterministic EDGAR recomputation for primary-source re-verification",
            "convention": "10-K/10-K405/10-KT + 10-Q/10-QT, no /A, no SB forms, "
            "filingDate strictly before first_revelation_date",
            "source": "data.sec.gov submissions API, fetched via tools/fetch_primary_sources.py",
            "errors": errors,
        },
        "cases": results,
    }
    dest = REPO / "data/candidates/edgar_verification.json"
    dest.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {dest} ({len(results)} cases, {len(errors)} errors)")
    for e in errors:
        print("  ERROR", e)
    hdr = f"{'ID':<5}{'TKR':<6}{'rec_q':>6}{'raw_q':>6}{'rec_x':>7}{'xbrl':>6}  window_forms"
    print(hdr)
    for r in results:
        forms = ",".join(
            f"{w['form']}@{w['filingDate']}" for w in r["revelation_window_filings"][:6]
        )
        print(
            f"{r['case_id']:<5}{r['ticker']:<6}"
            f"{str(r['recorded_quarters']):>6}{r['raw_total']:>6}"
            f"{str(r['recorded_xbrl']):>7}{str(r['xbrl_any_counted']):>6}  {forms}"
        )


if __name__ == "__main__":
    main()
