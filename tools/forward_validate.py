"""forward 사이클 봉인 전 기계 검증 (spec §3·§4·§6, D100).

usage: python tools/forward_validate.py --cycle forward/cycle_001

검사: ① universe 정합 ② source_manifest 전 항목 filing_date ≤ cutoff +
retrieval/filing 분리 저장 ③ scores 완결성(유니버스 전건 1레코드, not_scored
명시, 완료 분율 ≥11/12) ④ decision_state가 사전 등록 서수 컷과 기계 일치
⑤ 레코드 §6 전 필드 계약(두 배열 존재 의무 포함) + cited_sources ⊆
source_manifest + company.cik ↔ universe 교차 대조.
네트워크 0 · 모델 호출 0. 위반 시 exit 1.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from forward_common import (REPO, SCREENING_CUTOFF, MIN_SCORED, UNIVERSE_SIZE,
                            assert_subscription_only, read_json, parse_date)
from forward_prepare import check_universe

DECISION_STATES = {"flag", "review", "no_flag", "abstain"}
SUFFICIENCY = {"sufficient", "partial", "insufficient"}
CONFIDENCE = {"high", "medium", "low"}


def expected_state(score: int, sufficiency: str) -> str:
    if sufficiency == "insufficient":
        return "abstain"
    return "flag" if score >= 70 else ("review" if score >= 40 else "no_flag")


def _cited_source_attested(acc: str, sources: list[dict]) -> bool:
    """cited accession이 source_manifest에 등재되어 있는가 (§6 ⊆ 의무).

    accession_no 필드 일치 또는 URL 내 출현(대시 유무 양형)으로 판정."""
    bare = acc.replace("-", "")
    for s in sources:
        if acc == s.get("accession_no"):
            return True
        url = s.get("url") or ""
        if acc in url or (bare and bare in url):
            return True
    return False


def validate(cycle: Path) -> list[str]:
    errs = []
    u = read_json(cycle / "universe.json")
    errs += [f"universe: {e}" for e in check_universe(u)]
    universe_ids = {r["record_id"] for r in u.get("selected", [])}
    universe_cik = {r["record_id"]: str(r.get("cik", "")).zfill(10)
                    for r in u.get("selected", [])}

    cutoff = parse_date(SCREENING_CUTOFF)
    sources: list[dict] = []
    sm_path = cycle / "source_manifest.json"
    if sm_path.exists():
        sources = read_json(sm_path).get("sources", [])
        for i, e in enumerate(sources):
            for field in ("filing_date", "retrieval_date", "url", "sha256"):
                if not e.get(field):
                    errs.append(f"source[{i}]: {field} 결측 (retrieval/filing 분리 저장 의무)")
            try:
                if e.get("filing_date") and parse_date(e["filing_date"]) > cutoff:
                    errs.append(f"source[{i}] {e.get('url', '?')[:60]}: filing_date "
                                f"{e['filing_date']} > cutoff {SCREENING_CUTOFF}")
            except ValueError:
                errs.append(f"source[{i}]: filing_date 파싱 불가 {e.get('filing_date')!r}")
    else:
        errs.append("source_manifest.json 부재")

    sc_path = cycle / "scores.json"
    if sc_path.exists():
        records = read_json(sc_path).get("records", [])
        seen = {}
        scored = 0
        for r in records:
            rid = r.get("record_id")
            if rid in seen:
                errs.append(f"{rid}: 중복 레코드")
            seen[rid] = r
            if r.get("status") == "not_scored":
                continue
            scored += 1
            s = r.get("misstatement_risk_score")
            if not isinstance(s, int) or not (0 <= s <= 100):
                errs.append(f"{rid}: misstatement_risk_score 비정상 {s!r} (0–100 정수 서수)")
                continue
            suff = r.get("evidence_sufficiency")
            if suff not in SUFFICIENCY:
                errs.append(f"{rid}: evidence_sufficiency 비정상 {suff!r}")
            if r.get("assessment_confidence") not in CONFIDENCE:
                errs.append(f"{rid}: assessment_confidence 비정상")
            ds = r.get("decision_state")
            if ds not in DECISION_STATES:
                errs.append(f"{rid}: decision_state 비정상 {ds!r}")
            elif suff in SUFFICIENCY and ds != expected_state(s, suff):
                errs.append(f"{rid}: decision_state {ds} ≠ 서수 컷 기대 "
                            f"{expected_state(s, suff)} (score {s}, {suff})")
            for field in ("company", "top_signals", "cited_sources", "model_id",
                          "prompt_sha256", "schema_sha256", "scored_at"):
                if not r.get(field):
                    errs.append(f"{rid}: {field} 결측")
            # §6: 두 배열은 존재 의무 — 빈 배열은 적법, 키 부재는 위반
            for field in ("benign_alternative_explanations", "affected_account_areas"):
                if not isinstance(r.get(field), list):
                    errs.append(f"{rid}: {field} 부재/비배열 (§6 — 빈 배열 허용, 키 생략 불가)")
            for acc in r.get("cited_sources") or []:
                if not _cited_source_attested(str(acc), sources):
                    errs.append(f"{rid}: cited_sources {acc!r} — source_manifest 미등재 (§6 ⊆ 의무)")
            comp = r.get("company")
            if isinstance(comp, dict) and rid in universe_cik:
                cik = str(comp.get("cik", "")).zfill(10)
                if cik != universe_cik[rid]:
                    errs.append(f"{rid}: company.cik {comp.get('cik')!r} ≠ universe CIK "
                                f"{universe_cik[rid]} — 점수 후 교체 금지 (§1)")
        missing = universe_ids - set(seen)
        if missing:
            errs.append(f"유니버스 레코드 누락 {sorted(missing)} — not_scored라도 명시 등재 의무")
        extra = set(seen) - universe_ids
        if extra:
            errs.append(f"유니버스 밖 레코드 {sorted(extra)} — 점수 후 교체 금지 (§1)")
        if scored < MIN_SCORED:
            errs.append(f"완료 분율 미달: scored {scored} < {MIN_SCORED}/{UNIVERSE_SIZE} "
                        "— 봉인 불가, spec §3-3 (abort 규칙 §3-2 적용)")
    else:
        errs.append("scores.json 부재")
    return errs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cycle", required=True)
    args = ap.parse_args()
    assert_subscription_only()
    errs = validate(REPO / args.cycle)
    if errs:
        print("FAIL — forward 검증 위반:")
        for e in errs:
            print(f"  {e}")
        return 1
    print(f"PASS — forward 검증 (universe·cutoff·scores·decision 컷 정합, "
          f"cutoff {SCREENING_CUTOFF})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
