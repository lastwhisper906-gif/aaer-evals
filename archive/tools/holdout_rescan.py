"""holdout_rescan — 컷오프 후 신규 restatement/non-reliance(8-K Item 4.02) 월간 누적.

목적(P5): 피평가자 지식 컷오프(2026-01) 이후 최초 폭로된 회계 재작성 사건을 한 명령으로
스캔해 `docs/FUTURE_HOLDOUT_CANDIDATES.md` Tier-2를 채운다. 암기 불가 홀드아웃의 N을
키우는 재현 가능한 파이프라인(§9 G2 공공재).

방법: EDGAR full-text search(efts.sec.gov) — 8-K 폼 + "should no longer be relied upon"
구문 + Item 4.02. SEC fair-access UA(<5 req/s) 준수. **egress 차단 시 fetch 매니페스트
(질의 URL + 수기 취득 지침)를 출력**하고 정상 종료 — 무인 환경에서 조용히 실패하지 않는다.

출력: data/candidates/holdout_rescan/rescan_<enddt>.json (후보 목록 또는 fetch 매니페스트).
  — runs/(동결 채점 트리, 매니페스트·블라인드 스캔) 밖. 후보는 미검증 discovery다.
사용: python tools/holdout_rescan.py --since 2026-02-01 [--enddt 2026-07-08]
주의: 폭로일이 컷오프 경계에 가까우면(±수일) 훈련 데이터 경계 퍼짐 리스크 —
FUTURE_HOLDOUT_CANDIDATES.md의 Tier 1/2 구분(3월 이후·6월 이후 선호) 승계. 정답 키는
AAER 발행 시점에 완성(현재 전부 G2 provisional).
"""
import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
UA = {"User-Agent": "chaeper lastwhisper906@gmail.com"}  # SEC fair-access (fetch_primary_sources 승계)
EFTS = "https://efts.sec.gov/LATEST/search-index"
PHRASE = '"should no longer be relied upon"'
CUTOFF_DEFAULT = "2026-02-01"  # 지식 컷오프(2026-01) 직후. 경계 퍼짐 고려 시 3월+ 선호.


def query_url(since, enddt):
    from urllib.parse import urlencode
    return EFTS + "?" + urlencode({"q": PHRASE, "forms": "8-K", "startdt": since, "enddt": enddt})


def manifest(since, enddt, reason):
    """egress 차단·오류 시: 수기 취득 지침 포함 fetch 매니페스트."""
    return {
        "mode": "fetch_manifest",
        "reason": reason,
        "instructions": (
            "SEC egress 불가 — 아래 URL을 브라우저/타 환경에서 열어 JSON을 저장 후 "
            "runs/holdout/rescan/raw_<enddt>.json 로 배치하고 --parse 로 재실행. "
            "또는 EDGAR full-text UI(https://efts.sec.gov/LATEST/search-index)에서 "
            f"폼 8-K · 기간 {since}~{enddt} · 구문 {PHRASE} 로 조회."),
        "query_urls": [
            query_url(since, enddt),
            # Item 4.02 코드 교차검증용 (별도 확인)
            f"https://www.sec.gov/cgi-bin/srqsb?text=8-K+Item+4.02&first={since[:4]}",
        ],
        "since": since, "enddt": enddt,
        "next": "취득 JSON의 hits.hits[].._source (display_names/cik/file_date/accession) 파싱",
    }


def parse_hits(data):
    out = []
    for h in (data.get("hits", {}) or {}).get("hits", []):
        s = h.get("_source", {})
        names = s.get("display_names") or []
        out.append({"company": names[0] if names else s.get("cik"),
                    "cik": s.get("cik"), "file_date": s.get("file_date"),
                    "form": s.get("root_form") or s.get("file_type"),
                    "accession": (h.get("_id") or "").split(":")[0]})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", default=CUTOFF_DEFAULT)
    ap.add_argument("--enddt", default=None, help="종료일 YYYY-MM-DD (미지정 시 매니페스트만)")
    ap.add_argument("--parse", metavar="RAWJSON", help="이미 취득한 efts JSON을 파싱")
    args = ap.parse_args()
    enddt = args.enddt or args.since  # enddt 강제(Date.now 불가 — 무인 결정론)
    outdir = REPO / "data/candidates/holdout_rescan"
    outdir.mkdir(parents=True, exist_ok=True)

    if args.parse:
        data = json.loads(Path(args.parse).read_text(encoding="utf-8"))
        result = {"mode": "parsed", "since": args.since, "enddt": enddt,
                  "candidates": parse_hits(data),
                  "note": "전부 G2 provisional 후보 — Item 4.02 코드·XBRL 이력 수기 검증 필요."}
    else:
        try:
            import requests
            r = requests.get(query_url(args.since, enddt), headers=UA, timeout=30)
            r.raise_for_status()
            result = {"mode": "live", "since": args.since, "enddt": enddt,
                      "candidates": parse_hits(r.json()),
                      "note": "G2 provisional 후보 — Item 4.02·XBRL 이력 수기 검증 후 "
                              "FUTURE_HOLDOUT_CANDIDATES.md 편입."}
        except Exception as e:  # egress 차단 포함 — 조용히 실패 금지
            result = manifest(args.since, enddt, f"{type(e).__name__}: {e}")

    outpath = outdir / f"rescan_{enddt}.json"
    outpath.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    n = len(result.get("candidates", [])) if result["mode"] != "fetch_manifest" else 0
    print(f"[{result['mode']}] {outpath.relative_to(REPO)} — "
          f"{'후보 ' + str(n) + '건' if result['mode'] != 'fetch_manifest' else 'fetch 매니페스트(egress 차단)'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
