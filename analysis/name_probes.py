"""RP-10 Phase 3.6: 익명 숫자 페이로드만으로 회사 식별 가능성 — 30사.

판정 = 동결 scoring/probe_verdict.name_match 규칙 그대로 (재해석 금지).
입력: scoring/probe_results_v2/recognition/ (대조군 22 — Phase 1)
      + scoring/probe_results_v2/recognition_treatment/ (실험군 8 — 신규 draw)
비교 문맥: EDINET-Bench는 표 데이터에서 <5% 식별률 보고 — 본 결과와 병기.
출력: analysis/name_probe_results.json
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scoring"))
from probe_verdict import name_match  # noqa: E402 (동결 판정 규칙)


def main() -> int:
    m1 = json.loads((REPO / "scoring/id_mapping.json").read_text())["mapping"]
    m2 = json.loads((REPO / "scoring/id_mapping_v2.json").read_text())["mapping"]
    cands1 = {c["case_id"]: c for c in json.loads(
        (REPO / "data/candidates/candidates.json").read_text())["candidates"]}
    cands2 = {c["case_id"]: c for c in json.loads(
        (REPO / "data/candidates/candidates_v2_controls.json").read_text())["candidates"]}

    rows = []
    d = REPO / "scoring/probe_results_v2/recognition"
    for p in sorted(d.glob("case_*.json")):
        j = json.loads(p.read_text())
        cid = p.stem
        num = int(cid.split("_")[1])
        if num <= 16:
            mapping, cands, grp = m1, cands1, "fraud"
        else:
            mapping, cands, grp = m2, cands2, "control"
        if True:
            truth = cands[mapping[cid]]
            hit = name_match(j["company_guess"], truth)
            rows.append({"case_id": cid, "group": grp,
                         "truth_ticker": truth["ticker"].split("/")[0],
                         "guess": j["company_guess"], "confidence": j["confidence"],
                         "recognized": bool(hit)})
    n = len(rows)
    rec = sum(r["recognized"] for r in rows)
    by = {}
    for g in ("fraud", "control"):
        sub_rows = [r for r in rows if r["group"] == g]
        by[g] = {"n": len(sub_rows), "recognized": sum(r["recognized"] for r in sub_rows)}
    out = {"n_probes": n, "recognized_total": rec,
           "rate_pct": round(100 * rec / n, 1) if n else None,
           "by_group": by,
           "verdict_rule": "frozen scoring/probe_verdict.name_match",
           "context": "EDINET-Bench (2025): 표 데이터 식별률 <5% 보고",
           "rows": rows}
    (REPO / "analysis/name_probe_results.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: out[k] for k in ("n_probes", "recognized_total",
                                          "rate_pct", "by_group")}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
