"""대조군 후보 스크리닝 (Phase 2-6, D17 규칙의 기계 검증 축).

후보별 수집·검증:
  ① CIK 해석 (EDGAR company search atom) ② submissions: SIC·회사명·FYE
  ③ companyfacts: 매칭 실험군 컷오프 기준 point-in-time 매출·총자산 (규모 축),
     컷오프 전 10-K/10-Q 수 (edgar_verification 규약 동일: /A 제외, strictly before는
     아니고 <= cutoff — cutoff_guard 규약과 일치), XBRL 가용성
  ④ AAER 색인 사명 검색 (비집행 1축 — 2차 웹 검색은 별도 기록)

출력: data/candidates/control_screening.json (+ 콘솔 표).
선정 자체는 하지 않는다 — D17 규칙 적용·기록은 Review Packet 01.
"""
import datetime
import json
import re
import sys
from pathlib import Path

from fetch_primary_sources import DATA_DIR, fetch

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "data/candidates/control_screening.json"
CTRL_DIR = DATA_DIR / "_controls"

# 실험군 → (컷오프, 후보 검색어 목록). 검색어는 EDGAR 정식 사명 접두.
POOLS = {
    "T07": ("2011-06-28", ["Mosaic Co", "FMC Corp", "du Pont"]),
    "T11": ("2013-07-28", ["NuVasive", "Integra LifeSciences", "Wright Medical Group"]),
    "T12": ("2013-08-06", ["Garmin", "Plantronics", "Universal Electronics"]),
    "T13": ("2014-05-12", ["Avis Budget", "Ryder System", "United Rentals"]),
    "T16": ("2015-08-09", ["Perry Ellis", "Cherokee Inc", "XCel Brands"]),
    "T17": ("2015-09-10", ["Xilinx", "Skyworks Solutions", "Cypress Semiconductor"]),
    "T21": ("2016-02-28", ["Forrester Research", "Gartner", "Nielsen"]),
    "T28": ("2019-02-20", ["Kellogg", "General Mills", "Campbell Soup"]),
}

SALES_TAGS = ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues",
              "SalesRevenueNet", "SalesRevenueGoodsNet", "SalesRevenueServicesNet"]
ANNUAL = {"10-K", "10-K405", "10-KT"}
QUARTER = {"10-Q", "10-QT"}


def resolve_cik(query: str):
    url = ("https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany"
           f"&company={query.replace(' ', '+')}&type=10-K&dateb=&owner=include&count=10&output=atom")
    text = fetch(url).text
    hits = re.findall(r"<title>(.*?)</title>.*?CIK=(\d{10})", text, re.S)
    return [(t.strip(), c) for t, c in hits if "EDGAR" not in t]


def filing_counts(cik10: str, cutoff: datetime.date, dest: Path):
    url = f"https://data.sec.gov/submissions/CIK{cik10}.json"
    j = fetch(url).json()
    dest.mkdir(parents=True, exist_ok=True)
    (dest / f"CIK{cik10}.json").write_text(json.dumps(j), encoding="utf-8")
    blocks = [j["filings"]["recent"]]
    for extra in j["filings"].get("files", []):
        j2 = fetch(f"https://data.sec.gov/submissions/{extra['name']}").json()
        (dest / extra["name"]).write_text(json.dumps(j2), encoding="utf-8")
        blocks.append(j2)
    ann = q = 0
    xbrl = False
    for b in blocks:
        for form, date, isx in zip(b["form"], b["filingDate"], b.get("isXBRL", [0] * len(b["form"]))):
            d = datetime.date.fromisoformat(date)
            if d > cutoff:
                continue
            if form in ANNUAL:
                ann += 1
            elif form in QUARTER:
                q += 1
            else:
                continue
            if isx:
                xbrl = True
    return j.get("sic"), j.get("sicDescription"), j.get("name"), j.get("fiscalYearEnd"), ann, q, xbrl


def size_at_cutoff(cik10: str, cutoff: datetime.date, dest: Path):
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik10}.json"
    try:
        j = fetch(url).json()
    except Exception:  # noqa: BLE001
        return None, None, False
    (dest / f"companyfacts_CIK{cik10}.json").write_text(json.dumps(j), encoding="utf-8")
    gaap = j.get("facts", {}).get("us-gaap", {})

    def best(tags, want_duration):
        cand = {}
        for tag in tags:
            for f in gaap.get(tag, {}).get("units", {}).get("USD", []):
                filed = datetime.date.fromisoformat(f["filed"])
                if filed > cutoff:
                    continue
                has_start = bool(f.get("start"))
                if want_duration:
                    if not has_start:
                        continue
                    span = (datetime.date.fromisoformat(f["end"]) - datetime.date.fromisoformat(f["start"])).days
                    if not (340 <= span <= 400):
                        continue
                elif has_start:
                    continue
                end = f["end"]
                prev = cand.get(end)
                if prev is None or f["filed"] > prev[1]:
                    cand[end] = (f["val"], f["filed"])
            if cand:
                break
        if not cand:
            return None
        latest_end = max(cand)
        return cand[latest_end][0]

    rev = best(SALES_TAGS, True)
    assets = best(["Assets"], False)
    return rev, assets, bool(gaap)


def aaer_hits(name: str):
    idx = json.loads((DATA_DIR / "_aaer_index/aaer_index.json").read_text(encoding="utf-8"))
    # 보수적 부분열: 사명 첫 토큰(법인 접미 제거) 매칭
    key = re.sub(r"[^A-Za-z ]", "", name).split()[0].lower()
    hits = [e for e in idx["entries"] if key in e["respondents"].lower()]
    return idx["fetched_at"], hits


def main() -> int:
    results = []
    for tid, (cutoff_s, queries) in POOLS.items():
        cutoff = datetime.date.fromisoformat(cutoff_s)
        for q in queries:
            print(f"\n=== {tid} 후보: {q} ===")
            try:
                matches = resolve_cik(q)
            except Exception as e:  # noqa: BLE001
                print(f"  CIK 해석 실패: {e}")
                results.append({"treatment": tid, "query": q, "error": f"cik_resolve: {e}"})
                continue
            if not matches:
                print("  CIK 미발견")
                results.append({"treatment": tid, "query": q, "error": "cik_not_found"})
                continue
            title, cik10 = matches[0]
            dest = CTRL_DIR / re.sub(r"[^A-Za-z0-9]+", "_", q)
            try:
                sic, sic_desc, name, fye, ann, qtr, xbrl_forms = filing_counts(cik10, cutoff, dest)
                rev, assets, has_facts = size_at_cutoff(cik10, cutoff, dest)
                fetched_at, hits = aaer_hits(name or q)
            except Exception as e:  # noqa: BLE001
                print(f"  수집 실패: {e}")
                results.append({"treatment": tid, "query": q, "cik": cik10, "error": str(e)})
                continue
            row = {
                "treatment": tid, "query": q, "cik": cik10, "edgar_name": name,
                "matched_cutoff": cutoff_s, "sic": sic, "sic_desc": sic_desc,
                "fiscal_year_end": fye,
                "pre_cutoff_10K": ann, "pre_cutoff_10Q": qtr,
                "xbrl_available_pre_cutoff": xbrl_forms,
                "revenue_at_cutoff_pit": rev, "assets_at_cutoff_pit": assets,
                "aaer_index_hits": [f"AAER-{h['aaer_no']} {h['respondents'][:60]}" for h in hits],
                "aaer_index_checked_at": fetched_at,
            }
            results.append(row)
            print(f"  {name} SIC={sic}({(sic_desc or '')[:30]}) FYE={fye} "
                  f"10-K={ann} 10-Q={qtr} XBRL={xbrl_forms} rev={rev} assets={assets} "
                  f"AAER hits={len(hits)}")
    OUT.write_text(json.dumps({"screened_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                               "rule": "D17", "results": results}, ensure_ascii=False, indent=1),
                   encoding="utf-8")
    print(f"\nsaved → {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
