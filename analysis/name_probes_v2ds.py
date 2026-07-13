"""Q-F05 v2 date-shift name-ID 판정 — 사전 등록 엔드포인트 (specs/perturb_v2.md §5).

판정 = 동결 scoring/probe_verdict.name_match 규칙 그대로 (재해석 금지 — Q-E02(A)
규약 유지: DAR형 구명 경계는 규칙 판정이 1차, 사람 판독은 각주 병기 대상).

입력: scoring/probe_results_v2ds_wave1/recognition/ (30 = 8 treatment + 22 control)
      scoring/probe_results_v2ds_wave2/recognition/ (32)
비교 기준선 (동결 v1, 사전 등록): wave-1 50% [15/30] · wave-2 21.9% [7/32].
출력: analysis/name_probe_results_v2ds.json

실행: .venv/bin/python analysis/name_probes_v2ds.py   (무호출·결정론)
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scoring"))
sys.path.insert(0, str(REPO / "analysis"))
from probe_verdict import name_match  # noqa: E402 (동결 판정 규칙)
import stats  # noqa: E402 (Clopper-Pearson)

V1_FROZEN = {"wave1": {"rate_pct": 50.0, "count": "15/30"},
             "wave2": {"rate_pct": 21.9, "count": "7/32"}}
W1_DIR = REPO / "scoring" / "probe_results_v2ds_wave1" / "recognition"
W2_DIR = REPO / "scoring" / "probe_results_v2ds_wave2" / "recognition"


def wave1_rows() -> list[dict]:
    """wave-1 30사 — 진실 매핑은 name_probes.py(동결 분석)와 동일 경로."""
    m1 = json.loads((REPO / "scoring/id_mapping.json").read_text())["mapping"]
    m2 = json.loads((REPO / "scoring/id_mapping_v2.json").read_text())["mapping"]
    cands1 = {c["case_id"]: c for c in json.loads(
        (REPO / "data/candidates/candidates.json").read_text())["candidates"]}
    cands2 = {c["case_id"]: c for c in json.loads(
        (REPO / "data/candidates/candidates_v2_controls.json").read_text())["candidates"]}
    rows = []
    for p in sorted(W1_DIR.glob("case_*.json")):
        j = json.loads(p.read_text(encoding="utf-8"))
        cid = p.stem
        num = int(cid.split("_")[1])
        mapping, cands, grp = (m1, cands1, "fraud") if num <= 16 else (m2, cands2, "control")
        truth = cands[mapping[cid]]
        rows.append({"case_id": cid, "group": grp,
                     "truth_ticker": truth["ticker"].split("/")[0],
                     "guess": j["company_guess"], "confidence": j["confidence"],
                     "recognized": bool(name_match(j["company_guess"],
                                                   truth["company_name"]))})
    return rows


def wave2_rows() -> list[dict]:
    cases = {c["case_id"]: c for c in json.loads(
        (REPO / "data/evaluatee/cases_wave2.json").read_text())["cases"]}
    rows = []
    for p in sorted(W2_DIR.glob("case_*.json")):
        j = json.loads(p.read_text(encoding="utf-8"))
        c = cases[p.stem]
        rows.append({"case_id": p.stem, "truth_ticker": c["ticker"],
                     "guess": j["company_guess"], "confidence": j["confidence"],
                     "recognized": bool(name_match(j["company_guess"],
                                                   c["company_name"]))})
    return rows


def frame(rows: list[dict], expect_n: int, tier: str) -> dict:
    if len(rows) != expect_n:
        raise SystemExit(f"{tier}: {len(rows)}/{expect_n} — 프로브 미완, 판정 보류")
    k = sum(r["recognized"] for r in rows)
    cp = stats.fpr_bound(k, len(rows))  # Clopper-Pearson 95% (범용 이항)
    return {"n": len(rows), "recognized": k,
            "rate_pct": round(100 * k / len(rows), 1),
            "cp95_pct": [cp.get("lo_pct", 0.0), cp["upper95_pct"]],
            "v1_frozen": V1_FROZEN[tier], "rows": rows}


def main() -> int:
    out = {"spec": "specs/perturb_v2.md §5 (사전 등록 엔드포인트)",
           "verdict_rule": "동결 scoring/probe_verdict.name_match — 재해석 금지",
           "wave1": frame(wave1_rows(), 30, "wave1"),
           "wave2": frame(wave2_rows(), 32, "wave2")}
    for tier in ("wave1", "wave2"):
        f = out[tier]
        f["delta_vs_v1_pp"] = round(f["rate_pct"] - f["v1_frozen"]["rate_pct"], 1)
    out["reading_guard"] = (
        "사전 등록 비교는 rate 병기까지 — v2가 낮으면 '날짜 지문 제거가 name-ID "
        "채널을 추가로 좁혔다', 같으면 '날짜 외 지문(수치 자체)이 지배'. 인과 "
        "서술은 이 두 문장 밖으로 나가지 않는다 (원인 분해는 소유자 검토 대상).")
    p = REPO / "analysis" / "name_probe_results_v2ds.json"
    p.write_text(json.dumps(out, ensure_ascii=False, sort_keys=True, indent=1) + "\n",
                 encoding="utf-8")
    print(f"wave-1 v2ds {out['wave1']['recognized']}/30 = {out['wave1']['rate_pct']}% "
          f"(v1 50%) · wave-2 {out['wave2']['recognized']}/32 = "
          f"{out['wave2']['rate_pct']}% (v1 21.9%) → {p.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
