"""대조군 후보 전건에 베이스라인 4스크린 + Piotroski 실행 (Phase 2-6).

입력: data/candidates/control_screening.json + ~/aaer-data/_controls/{query}/.
출력: scoring/baselines/results/controls/{treatment}__{query}.json + 콘솔 요약.
컷오프 = 매칭 실험군 컷오프 (GP-9 ① 복사 규약과 동일 시점).
"""
import datetime
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scoring/baselines"))
import screens  # noqa: E402

CTRL = Path.home() / "aaer-data" / "_controls"
OUT = REPO / "scoring/baselines/results/controls"


def main() -> int:
    rows = json.loads((REPO / "data/candidates/control_screening.json").read_text())["results"]
    OUT.mkdir(parents=True, exist_ok=True)
    for r in rows:
        if "error" in r:
            continue
        q = r["query"]
        d = CTRL / re.sub(r"[^A-Za-z0-9]+", "_", q)
        cutoff = datetime.date.fromisoformat(r["matched_cutoff"])
        notes, prov = [], {}
        try:
            table = screens.load_facts("", cutoff, xbrl_dir=d)
        except FileNotFoundError:
            print(f"{r['treatment']} {q}: companyfacts 없음")
            continue
        ends = screens.fiscal_year_ends(table, cutoff)
        if len(ends) < 2:
            print(f"{r['treatment']} {q}: 연차 {len(ends)}개 — 계산 불능")
            continue
        years = [{c: screens.get(table, c, e, prov) for c in screens.CONCEPTS} for e in ends[:3]]
        v_t, v_p = years[0], years[1]
        v_pp = years[2] if len(years) > 2 else None
        b_vars, m, b_miss = screens.beneish(v_t, v_p, notes)
        f_vars, f, f_miss = screens.dechow_f(v_t, v_p, v_pp, notes)
        c_flags, c, c_miss = screens.montier_c(v_t, v_p)
        p_checks, pio, p_miss = screens.piotroski(v_t, v_p, v_pp)
        s = screens.sloan(v_t, v_p)
        result = {
            "treatment": r["treatment"], "candidate": q, "cik": r["cik"],
            "cutoff": r["matched_cutoff"], "fiscal_year_ends_used": [str(e) for e in ends],
            "beneish_m": m, "beneish_missing": b_miss,
            "dechow_f": f, "dechow_missing": f_miss,
            "montier_c": c, "piotroski_f9": pio, "sloan": s, "notes": notes,
        }
        fname = f"{r['treatment']}__{re.sub(r'[^A-Za-z0-9]+', '_', q)}.json"
        (OUT / fname).write_text(json.dumps(result, ensure_ascii=False, indent=2, default=str),
                                 encoding="utf-8")
        fmt = lambda x, p=2: "N/A" if x is None else f"{x:.{p}f}"  # noqa: E731
        print(f"{r['treatment']} {q:28s} M={fmt(m)} F={fmt(f)} C={c if c is not None else 'N/A'} "
              f"Pio={pio if pio is not None else 'N/A'} Sloan={fmt(s, 3)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
