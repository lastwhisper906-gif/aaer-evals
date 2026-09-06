"""홀드아웃 본채점 재추첨 분석 (결정론) — W2_MAINSCORE_REDRAW_PLAN §7 판정 규칙 그대로.

`python analysis/holdout_redraw_analyze.py`
입력: draw-1 = 동결 runs/holdout/scores/case_NN.json (published, 불침해)
      draw-2..5 = runs/holdout/mainscore_redraw/draw_{2..5}/case_NN.json
규칙 (§7-3, 사전 커밋 — 재해석 금지):
  1차: HUBG p>=50 이 5 draw 중 >=4 (draw-1 포함) → robust; <=3/5 → draw-민감, 완화 없음.
  2차: 3사 각각 median + [min,max] 밴드. WMK·GNE가 >=2 draw에서 p>=50 → '불안정' 보고
       (신규 탐지 승격 금지). H1 미주장 (N=3). 발행 per-case 수치는 draw-1 그대로.
절단: 완료 draw까지 부분 밴드 ("k=n/5", 미완 명시 — §7-4).
출력: analysis/holdout_redraw_results.json.
"""
import json
import statistics as st
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CASES = {"case_71": "HUBG", "case_72": "WMK", "case_73": "GNE"}
DRAWS = [1, 2, 3, 4, 5]


def load_p(path):
    p = REPO / path
    return json.load(open(p, encoding="utf-8"))["misstatement_probability"] if p.exists() else None


def main():
    scores = {c: {} for c in CASES}
    for c in CASES:
        scores[c][1] = load_p(f"runs/holdout/scores/{c}.json")
        for d in (2, 3, 4, 5):
            scores[c][d] = load_p(f"runs/holdout/mainscore_redraw/draw_{d}/{c}.json")

    assert all(scores[c][1] is not None for c in CASES), "draw-1 (동결 published) 부재"
    # 완료 draw = 3사 전건 존재하는 draw만 (draw 단위 발사 — §7-4)
    done = [d for d in DRAWS if all(scores[c][d] is not None for c in CASES)]
    k = len(done)

    per_case = {}
    for c, t in CASES.items():
        vals = [scores[c][d] for d in done]
        per_case[t] = {
            "published_draw1": scores[c][1],
            "by_draw": {f"draw_{d}": scores[c][d] for d in DRAWS},
            "median": st.median(vals),
            "band_min": min(vals),
            "band_max": max(vals),
            "n_ge50": sum(1 for v in vals if v >= 50),
            "k": k,
        }

    # 1차 규칙 (HUBG) — k=5 완료 시에만 확정 판정, 미완이면 partial
    hubg_ge50 = per_case["HUBG"]["n_ge50"]
    if k == 5:
        primary = ("H2 탐지는 draw 잡음에 강건(robust) — HUBG p>=50 {}/5 (>=4 충족)"
                   .format(hubg_ge50) if hubg_ge50 >= 4 else
                   "draw-민감으로 보고 (HUBG p>=50 {}/5 <=3) — 표현 완화 없음".format(hubg_ge50))
    else:
        primary = f"PARTIAL k={k}/5 — 판정 유보 (HUBG p>=50 잠정 {hubg_ge50}/{k})"

    # 2차 규칙 (WMK·GNE 뒤집힘 = 불안정, 승격 금지)
    instability = {t: per_case[t]["n_ge50"] for t in ("WMK", "GNE")}
    flags = [t for t, n in instability.items() if n >= 2]

    out = {
        "plan": "W2_MAINSCORE_REDRAW_PLAN.md §7 (로그된 개정 #1)",
        "k_completed": k, "draws_done": done,
        "per_case": per_case,
        "primary_rule_HUBG": {"n_ge50": hubg_ge50, "threshold": "4/5", "verdict": primary},
        "secondary_instability": {"counts": instability,
                                  "flagged": flags,
                                  "note": "'불안정' 보고 전용 — 신규 탐지 승격 금지 (§7-3)"},
        "invariants": "H1 미주장(N=3) · 발행 per-case = draw-1 유지 (§3 승계)",
    }
    (REPO / "analysis/holdout_redraw_results.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
