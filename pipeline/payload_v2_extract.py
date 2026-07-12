"""payload_v2_extract.py — payload-v2 진단 추출기 (WS-1/F-4, specs/payload_v2.md).

진단 전용(diagnostic-only): 출력은 runs/diagnostics/payload_v2/ 로만 가며 어떤
피평가자 페이로드에도 편입되지 않는다 (편입 = 별도 소유자 게이트, 스펙 §0).

추출 2채널:
  (a) 8-K item 코드 — submissions JSON `items` 병렬 배열 (스펙 §3.2)
  (b) 주식수·EPS 사실 — companyfacts dei/us-gaap, shares·USD/shares 단위 (스펙 §2.2)

PIT 의미론은 동결 빌더(build_payload.py)와 동일: filed <= cutoff (등호 포함),
(tag, period) 최신 filed 승리(accession tie-break), 기간 밴드 동일. look-ahead
필터는 이 모듈의 cutoff 비교 두 지점(_iso_leq — 채널당 1개)으로 수렴하며
test_payload_v2.py 가 기계 검증한다. cutoff_guard.load_document() 비경유 사유는
스펙 §3.4 (동결 빌더의 피평가자측 벌크 패턴 선례 — 정답지 무접근, fail-closed 미러).

fail-closed: 파싱 불가 날짜 → 예외 (조용한 skip 금지). 파일 부재 → 코어 함수
예외, CLI 만 케이스 단위 포착·coverage 기록 (네트워크 fetch 금지).

사용: .venv/bin/python pipeline/payload_v2_extract.py [--out runs/diagnostics/payload_v2]
"""
from __future__ import annotations

import argparse
import datetime
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = Path.home() / "aaer-data"
CASE_FILES = ["cases.json", "cases_v2.json", "cases_wave2.json",
              "cases_holdout.json", "cases_holdout_controls.json"]
OUT_DIR = REPO_ROOT / "runs" / "diagnostics" / "payload_v2"

# 스펙 §2.2 — (namespace, tag, unit). 두 diluted 철자 병기 (정직 기록: 실측 태그는
# WeightedAverageNumberOfDilutedSharesOutstanding, 미션 문면 철자는 변형 대비 보존).
SHARE_TAGS = [
    ("dei", "EntityCommonStockSharesOutstanding", "shares"),
    ("us-gaap", "EarningsPerShareBasic", "USD/shares"),
    ("us-gaap", "EarningsPerShareDiluted", "USD/shares"),
    ("us-gaap", "WeightedAverageNumberOfSharesOutstandingBasic", "shares"),
    ("us-gaap", "WeightedAverageNumberOfDilutedSharesOutstanding", "shares"),
    ("us-gaap", "WeightedAverageNumberOfSharesOutstandingDiluted", "shares"),
    ("us-gaap", "CommonStockSharesOutstanding", "shares"),
]
EIGHTK_FORMS = ("8-K", "8-K/A")
ANNUAL_DAYS = (340, 400)    # 동결 빌더와 동일 밴드
QUARTER_DAYS = (75, 100)


class PayloadV2Error(Exception):
    """fail-closed: 파싱 불가 날짜·파일 부재 등 — 조용한 skip 금지."""


def _iso(value, field: str) -> datetime.date:
    try:
        return datetime.date.fromisoformat(str(value))
    except ValueError as e:
        raise PayloadV2Error(f"{field}={value!r}: ISO 날짜가 아님 — fail-closed") from e


def parse_items(items_raw: str) -> list[str]:
    """스펙 §3.2: 쉼표 분리 → strip → 빈 토큰 제거. 원시 문자열은 호출자가 보존."""
    return [tok.strip() for tok in (items_raw or "").split(",") if tok.strip()]


def _submissions_paths(ticker: str) -> list[Path]:
    edgar_dir = DATA_DIR / ticker / "edgar"
    paths = sorted(edgar_dir.glob("CIK*.json"))
    if not paths:
        raise PayloadV2Error(f"{edgar_dir}: submissions JSON 없음 — fail-closed (fetch 금지)")
    return paths


def extract_8k_items(ticker: str, cutoff: datetime.date,
                     data_dir: Path = DATA_DIR) -> tuple[list[dict], dict]:
    """컷오프 전(포함) 8-K/8-K/A 행의 item 코드. 반환: (rows, coverage)."""
    edgar_dir = data_dir / ticker / "edgar"
    paths = sorted(edgar_dir.glob("CIK*.json"))
    if not paths:
        raise PayloadV2Error(f"{edgar_dir}: submissions JSON 없음 — fail-closed (fetch 금지)")
    rows, missing_subfiles = [], []
    cached = {p.name for p in paths}
    for path in paths:
        j = json.loads(path.read_text(encoding="utf-8"))
        blocks = [j["filings"]["recent"]] if "filings" in j else [j]
        for sub in (j.get("filings", {}).get("files", []) if "filings" in j else []):
            if sub.get("name") and sub["name"] not in cached:
                missing_subfiles.append(sub["name"])
        for b in blocks:
            forms = b.get("form", [])
            dates = b.get("filingDate", [])
            accs = b.get("accessionNumber", [])
            items = b.get("items", [""] * len(forms))
            for i, form in enumerate(forms):
                if form not in EIGHTK_FORMS:
                    continue
                if _iso(dates[i], "filingDate") > cutoff:
                    continue  # (a)채널 유일 look-ahead 필터 지점
                raw = items[i] if i < len(items) else ""
                rows.append({"accession": accs[i], "form": form, "filing_date": dates[i],
                             "items_raw": raw, "items": parse_items(raw)})
    rows.sort(key=lambda r: (r["filing_date"], r["accession"]))
    # 다중 청크 병합 중복 제거 (accession 기준)
    dedup, seen = [], set()
    for r in rows:
        if r["accession"] not in seen:
            seen.add(r["accession"])
            dedup.append(r)
    coverage = {"submissions_files_read": len(paths),
                "paginated_subfiles_listed_not_cached": sorted(set(missing_subfiles))}
    return dedup, coverage


def extract_share_facts(ticker: str, cutoff: datetime.date,
                        data_dir: Path = DATA_DIR) -> tuple[dict, dict]:
    """컷오프 전(포함) 주식수·EPS PIT 시계열. 반환: (facts, coverage)."""
    xbrl_dir = data_dir / ticker / "xbrl"
    files = sorted(xbrl_dir.glob("*CIK*.json"))
    if not files:
        raise PayloadV2Error(f"{xbrl_dir}: companyfacts 없음 — fail-closed (fetch 금지)")
    table: dict[str, dict] = {}
    namespaces = set()
    for path in files:
        facts = json.loads(path.read_text(encoding="utf-8")).get("facts", {})
        namespaces.update(facts.keys())
        for ns, tag, unit in SHARE_TAGS:
            for f in facts.get(ns, {}).get(tag, {}).get("units", {}).get(unit, []):
                if _iso(f["filed"], "filed") > cutoff:
                    continue  # (b)채널 유일 look-ahead 필터 지점
                start = f.get("start")
                if start:
                    span = (_iso(f["end"], "end") - _iso(start, "start")).days
                    if ANNUAL_DAYS[0] <= span <= ANNUAL_DAYS[1]:
                        ptype = "annual"
                    elif QUARTER_DAYS[0] <= span <= QUARTER_DAYS[1]:
                        ptype = "quarterly"
                    else:
                        continue
                else:
                    ptype = "instant"
                key = (start or "") + "|" + f["end"]
                slot = table.setdefault(f"{ns}:{tag}", {})
                prev = slot.get(key)
                cand = {"start": start, "end": f["end"], "period_type": ptype,
                        "value": f["val"], "unit": unit, "filed": f["filed"],
                        "accession": f.get("accn"), "form": f.get("form")}
                if prev is None or (cand["filed"], cand["accession"] or "") > (prev["filed"], prev["accession"] or ""):
                    slot[key] = cand
    facts_out = {tag: sorted(vals.values(), key=lambda v: (v["end"], v["start"] or ""))
                 for tag, vals in sorted(table.items())}
    coverage = {"facts_namespaces_present": sorted(namespaces),
                "tags_found": {tag: len(vals) for tag, vals in facts_out.items()}}
    return facts_out, coverage


def extract_case(case: dict, source_file: str, data_dir: Path = DATA_DIR) -> dict:
    cutoff = _iso(case["cutoff_date"], "cutoff_date")
    eightk, cov_e = extract_8k_items(case["ticker"], cutoff, data_dir)
    shares, cov_x = extract_share_facts(case["ticker"], cutoff, data_dir)
    return {
        "spec": "specs/payload_v2.md",
        "diagnostic_only": True,
        "case_id": case["case_id"], "ticker": case["ticker"],
        "cutoff_date": case["cutoff_date"], "source_file": source_file,
        "eightk_items": eightk,
        "share_facts": shares,
        "coverage": {**cov_e, **cov_x},
    }


def load_universe(repo_root: Path = REPO_ROOT) -> list[tuple[dict, str]]:
    out = []
    for name in CASE_FILES:
        data = json.loads((repo_root / "data" / "evaluatee" / name).read_text(encoding="utf-8"))
        for case in data["cases"]:
            out.append((case, name))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default=str(OUT_DIR))
    args = ap.parse_args()
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    universe = load_universe()
    done, partial, missing = [], [], []
    for case, src in universe:
        cid = case["case_id"]
        try:
            payload = extract_case(case, src)
        except PayloadV2Error as e:
            missing.append({"case_id": cid, "ticker": case["ticker"], "reason": str(e)})
            continue
        (out_dir / f"{cid}.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
        done.append(cid)
        if payload["coverage"]["paginated_subfiles_listed_not_cached"]:
            partial.append({"case_id": cid, "ticker": case["ticker"],
                            "missing_subfiles": payload["coverage"]["paginated_subfiles_listed_not_cached"]})
    coverage = {
        "spec": "specs/payload_v2.md",
        "coverage": f"{len(done)}/{len(universe)}",
        "complete": len(done), "total": len(universe),
        "partial_cases_subfiles_not_cached": partial,
        "missing_cases": missing,
        "note": "partial = 본체 filings.files에 열거된 하위 파일이 로컬 미캐시 (fetch 금지 — OWNER_QUEUE 등록)",
    }
    (out_dir / "COVERAGE.json").write_text(
        json.dumps(coverage, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"payload-v2: {len(done)}/{len(universe)} 케이스 추출, partial {len(partial)}, missing {len(missing)}")
    for m in missing:
        print("  MISSING:", m["case_id"], m["ticker"], m["reason"])
    return 0 if not missing else 1


if __name__ == "__main__":
    raise SystemExit(main())
