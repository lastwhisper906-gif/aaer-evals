"""forward source_manifest.json 방출기 (R3-4 — 게이트 §4 (2)의 산출 의무).

usage: python tools/forward_source_manifest.py --fetch-dir <dest> \
    --cycle forward/cycle_001 [--cutoff YYYY-MM-DD]

fetch_xbrl_facts.py --universe 수집이 남긴 fetch_log.jsonl(url·retrieval_date·
sha256·path)과 수집 파일 자체(companyfacts의 accn·filed)에서
`forward_validate`가 요구하는 source_manifest.json을 기계 생성한다:
항목당 {accession_no, url, filing_date, retrieval_date, sha256}.

companyfacts는 누적 아카이브라 filed > cutoff 항목이 존재할 수 있다 —
그 accession은 매니페스트에 넣지 않는다(피평가자 페이로드도 컷오프
필터를 거치므로 documents_used ⊆ 매니페스트가 유지된다). 네트워크 0.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from forward_common import REPO, SCREENING_CUTOFF, parse_date, write_json


def accessions_in_companyfacts(path: Path, cutoff: str) -> dict[str, str]:
    """{accession_no: 최초 관측 filed} — filed ≤ cutoff 항목만."""
    doc = json.loads(path.read_text(encoding="utf-8"))
    out: dict[str, str] = {}
    for taxonomy in (doc.get("facts") or {}).values():
        for concept in taxonomy.values():
            for units in (concept.get("units") or {}).values():
                for fact in units:
                    accn, filed = fact.get("accn"), fact.get("filed")
                    if not accn or not filed:
                        continue
                    if parse_date(filed) > parse_date(cutoff):
                        continue
                    if accn not in out or filed < out[accn]:
                        out[accn] = filed
    return out


def build_sources(fetch_dir: Path, cutoff: str) -> list[dict]:
    log_path = fetch_dir / "fetch_log.jsonl"
    sources = []
    for line in log_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        for accn, filed in sorted(
                accessions_in_companyfacts(Path(row["path"]), cutoff).items()):
            sources.append({
                "accession_no": accn,
                "filing_date": filed,
                "url": row["url"],
                "retrieval_date": row["retrieval_date"],
                "sha256": row["sha256"],
            })
    return sources


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch-dir", required=True)
    ap.add_argument("--cycle", required=True)
    ap.add_argument("--cutoff", default=SCREENING_CUTOFF)
    args = ap.parse_args()
    sources = build_sources(Path(args.fetch_dir), args.cutoff)
    cycle = REPO / args.cycle
    write_json(cycle / "source_manifest.json", {
        "generated_by": "tools/forward_source_manifest.py",
        "cutoff": args.cutoff,
        "sources": sources,
    })
    print(f"OK — source_manifest.json: {len(sources)} accession 항목 "
          f"(cutoff {args.cutoff})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
