"""forward source_manifest.json 방출기 (R3-4 — 게이트 §4 (2)의 산출 의무).

usage: python tools/forward_source_manifest.py --fetch-dir <dest> \
    --cycle forward/cycle_001 [--cutoff YYYY-MM-DD]

fetch_xbrl_facts.py --universe 수집이 남긴 정본 수집 로그
(data/provenance/fetch_log.jsonl — url·retrieval_date·sha256·path, R15-1)와
수집 파일 자체(companyfacts의 accn·filed)에서
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
from forward_common import (REPO, SCREENING_CUTOFF, SURFACE_MANIFEST,
                            assert_subscription_only, cutoff_agreement_errors,
                            is_sealed, parse_date, seal_residue_notice,
                            sha256_file, write_json)


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


def _resolve_logged_path(value: str, fetch_dir: Path) -> Path:
    """R4-7(d): fetch_log의 정박 표기(저장소 상대·~/)와 구세대 절대 경로 해석."""
    if value.startswith("~/"):
        return Path.home() / value[2:]
    p = Path(value)
    if p.is_absolute():
        return p
    if (REPO / value).exists():
        return REPO / value
    return fetch_dir / value


def build_sources(fetch_dir: Path, cutoff: str) -> list[dict]:
    # R15-1: 수집 로그의 정본 위치는 fetch_xbrl_facts가 소유한다 — fetch_dir
    # (= --fetch-dir)에서 파생하면 writer와 **다른 파일**을 읽는 네 번째
    # 소비자가 된다. fetch_dir은 로그 행의 상대 경로 해석에만 쓴다.
    import fetch_xbrl_facts  # noqa: PLC0415 — 지연 import (순환 없음)
    log_path = fetch_xbrl_facts.fetch_log_path()
    # R4-7(d): append 로그의 재시도 중복 — record_id당 최신 행만 채택
    # (뒤 행 우선). 없으면 재시도 후 매니페스트에 상충 sha256이 이중 등재된다.
    latest: dict[str, dict] = {}
    for line in log_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        # R8-1: submissions 행(kind)은 매니페스트 입력이 아니다 — record_id 키
        # 최신-행 dedup에 섞이면 companyfacts 행을 클로버해 해당 레코드의
        # 매니페스트가 조용히 빈다. kind 부재(구세대 로그)는 companyfacts.
        if row.get("kind", "companyfacts") != "companyfacts":
            continue
        latest[row["record_id"]] = row
    sources = []
    for rid in sorted(latest):
        row = latest[rid]
        path = _resolve_logged_path(row["path"], fetch_dir)
        # R16-5: 봉인되는 sha256은 **파싱한 그 바이트**의 것이어야 한다.
        # 종전에는 디스크에서 accession을 읽고 sha256은 로그 행에서 베껴 왔다 —
        # 두 값이 어긋나도 아무도 몰랐고, source_manifest.json은 SEALED_FILES이자
        # 이 저장소가 내세우는 INV-01 증거다. R4-4가 run_output_sha256을 실측
        # 재해시로 만든 것과 같은 이유: 아무도 다시 계산하지 않는 leg는 신뢰
        # 사슬이 아니라 장식이다.
        actual = sha256_file(path)
        if actual != row.get("sha256"):
            raise SystemExit(
                f"FAIL — {rid}: 수집 로그의 sha256과 디스크 바이트가 다르다 — "
                f"로그 {row.get('sha256')!r} ≠ 실측 {actual} ({path}). "
                "봉인될 출처 증명이 실제로 파싱된 바이트를 가리키지 않는다. "
                "로그를 고치지 말고 재수집하라 (fetch_xbrl_facts.py --universe) "
                "— 로그를 실측에 맞추면 증명이 아니라 전사(transcription)가 된다.")
        for accn, filed in sorted(accessions_in_companyfacts(path, cutoff).items()):
            sources.append({
                "accession_no": accn,
                "filing_date": filed,
                "url": row["url"],
                "retrieval_date": row["retrieval_date"],
                # 로그 행이 아니라 **실측값**을 봉인한다 (위 대조로 둘은 같다).
                "sha256": actual,
            })
    return sources


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch-dir", required=True)
    ap.add_argument("--cycle", required=True)
    ap.add_argument("--cutoff", default=SCREENING_CUTOFF)
    args = ap.parse_args()
    assert_subscription_only()
    cycle = REPO / args.cycle
    # R4-3: source_manifest.json은 SEALED_FILES — 봉인 후 재작성 금지
    # R11-8: 판정식은 '봉인 완결'(MANIFEST + SEAL_RECORD) — 중단 잔여물은 아니다
    if is_sealed(cycle):
        print(f"FAIL — {args.cycle}: 봉인 완결 — 봉인된 사이클의 "
              "source_manifest.json 재작성 금지 (spec §3-5, INV-22). 교정은 새 사이클로.")
        return 1
    if (notice := seal_residue_notice(cycle)):
        print(notice)
    # R17-1: `--cutoff`는 동결 상수를 기본값으로만 쓰는 자유 문자열이었다 — 아무도
    # 되비추지 않았으므로 임의 값이 그대로 봉인 대상 매니페스트에 실렸다. 이 사이클이
    # 이미 기재한 컷오프(PROTOCOL 스냅샷)와 이번 실행의 `--cutoff`를 함께 상수에
    # 대조하고, 어긋나면 **쓰기 전에** 멈춘다.
    # R18-1: 이 도구가 **쓰는** 파일이 source_manifest.json이므로, 사전 검사의
    # 전건에서는 그 표면 하나만 뺀다 (SURFACE_MANIFEST). 빼도 이번 실행이 쓸
    # 값은 검사된다 — 아래 extra의 `--cutoff (이번 실행)`가 곧 파일에 실릴 바로
    # 그 값이다. PROTOCOL 스냅샷은 그대로 전건에 남는다.
    errs = cutoff_agreement_errors(cycle, extra=[("--cutoff (이번 실행)", args.cutoff)],
                                   producing=[SURFACE_MANIFEST])
    if errs:
        print("FAIL — 스크리닝 컷오프 정합 위반 (봉인 대상 매니페스트를 쓰지 않는다):")
        for e in errs:
            print(f"  {e}")
        return 1
    sources = build_sources(Path(args.fetch_dir), args.cutoff)
    write_json(cycle / "source_manifest.json", {
        "generated_by": "tools/forward_source_manifest.py",
        "cutoff": args.cutoff,
        "sources": sources,
    })
    # 쓴 뒤 매니페스트 표면까지 포함해 한 번 더 — 사전 검사에서 뺀 표면을
    # 산출물 자체에 대고 되읽는다 (build_evaluatee_inputs의 레지스트리 재검사와
    # 같은 형태). 이 호출에는 producing이 없다.
    errs = cutoff_agreement_errors(cycle, extra=[("--cutoff (이번 실행)", args.cutoff)])
    if errs:
        print("FAIL — 작성된 source_manifest.json의 컷오프 정합 위반:")
        for e in errs:
            print(f"  {e}")
        return 1
    print(f"OK — source_manifest.json: {len(sources)} accession 항목 "
          f"(cutoff {args.cutoff})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
