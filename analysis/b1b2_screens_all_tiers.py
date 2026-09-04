"""B1/B2 cross-tier stage 1 — frozen formula screens for every tier (corpus tier).

specs/B1B2_CROSS_TIER.md §1. Re-runs the frozen ``scoring/baselines/screens.py``
``run_case`` (point-in-time: ``filed <= cutoff``, latest filed wins, no silent
imputation) over all 74 firms of the three tiers and writes
``analysis/out/b1b2_cross_tier/screens_by_case.json``.

Only the nine holdout controls are *new* inputs for stage 2; the other 65
firms are recomputed purely as a reproducibility check against the published
``analysis/unified_table.csv`` values (E-003 regeneration). Mismatches are
recorded, never silently substituted — stage 2 always uses the published value.

Needs ``~/aaer-data`` (``make verify-full`` tier). No network, no model calls,
no timestamps (byte-identical reruns).
Usage: .venv/bin/python analysis/b1b2_screens_all_tiers.py
"""
import csv
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scoring/baselines"))
from screens import DATA_DIR, run_case  # noqa: E402  (frozen PIT implementation)

OUT_DIR = REPO / "analysis/out/b1b2_cross_tier"
OUT = OUT_DIR / "screens_by_case.json"
SPEC = "specs/B1B2_CROSS_TIER.md"


def _load(rel):
    return json.loads((REPO / rel).read_text(encoding="utf-8"))


def _cands(rel):
    return {c["case_id"]: c for c in _load(rel)["candidates"]}


def _fnum(s):
    return None if s in ("", "None", None) else float(s)


def roster():
    """Return [(key, wave, candidate_record_with_group, published_m, published_f)]."""
    ut = list(csv.DictReader(open(REPO / "analysis/unified_table.csv", encoding="utf-8")))
    c1 = _cands("data/candidates/candidates.json")
    c1.update(_cands("data/candidates/candidates_v2_controls.json"))
    cw2 = _cands("data/candidates/candidates_wave2.json")
    idmap_w2 = _load("scoring/id_mapping_wave2.json")["mapping"]
    ch = _cands("data/candidates/candidates_holdout.json")
    hc = _cands("data/candidates/candidates_holdout_controls.json")

    rows = []
    for r in ut:
        w, cid = r["wave"], r["case_id"]
        if w == "wave1":
            cand = c1[cid]
        elif w == "wave2":
            cand = cw2[idmap_w2[cid]]
        elif w == "holdout":
            cand = ch[cid]
        else:
            raise SystemExit(f"unknown wave {w!r} in unified_table")
        rows.append((f"{w}:{cid}", w, dict(cand, group=r["group"]),
                     _fnum(r["m_score"]), _fnum(r["f_score"])))
    for tick in sorted(hc):
        rows.append((f"holdout_controls:{tick}", "holdout_controls",
                     dict(hc[tick], group="control"), None, None))
    assert len(rows) == 74, len(rows)
    return rows


def _match(published, recomputed, wave):
    """wave1 keeps full precision in unified_table; wave2/holdout are stored at 3 dp."""
    if published is None and recomputed is None:
        return "both_none"
    if published is None or recomputed is None:
        return "mismatch_none"
    if wave == "wave1":
        return "match" if abs(published - recomputed) < 1e-9 else "mismatch"
    return "match" if abs(published - round(recomputed, 3)) < 1e-9 else "mismatch"


def main() -> int:
    if not DATA_DIR.exists():
        print(f"corpus root missing: {DATA_DIR} — corpus tier only (make verify-full)")
        return 2
    cases, consistency = {}, {}
    for key, wave, cand, pm, pf in roster():
        r = run_case(cand)
        b, f = r.get("beneish", {}), r.get("dechow_f", {})
        m, fs = b.get("m_score"), f.get("f_score")
        cases[key] = {
            "wave": wave, "case_id": cand["case_id"], "ticker": r["ticker"],
            "group": cand["group"], "cutoff_date": r["cutoff_date"],
            "fiscal_year_ends_used": r.get("fiscal_year_ends_used"),
            "error": r.get("error"),
            "m_score": m, "m_missing": b.get("missing"),
            "f_score": fs, "f_missing": f.get("missing"),
        }
        if wave != "holdout_controls":
            consistency[key] = {"m": _match(pm, m, wave), "f": _match(pf, fs, wave)}
    tally = {}
    for v in consistency.values():
        for k in ("m", "f"):
            tally[f"{k}:{v[k]}"] = tally.get(f"{k}:{v[k]}", 0) + 1
    out = {
        "spec": SPEC,
        "generated_by": "analysis/b1b2_screens_all_tiers.py",
        "screens_source": "scoring/baselines/screens.py (frozen; run_case)",
        "point_in_time_rule": "facts with filed <= cutoff only; latest filed wins per (tag, period-end)",
        "stage2_usage": ("holdout_controls entries are stage-2 inputs; wave1/wave2/holdout "
                         "entries are a reproducibility check only — stage 2 reads the "
                         "published analysis/unified_table.csv values"),
        "n_cases": len(cases),
        "consistency_vs_unified_table": {"tally": dict(sorted(tally.items())),
                                         "per_case": consistency},
        "cases": cases,
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1, sort_keys=True,
                              default=str) + "\n", encoding="utf-8")
    for key, c in cases.items():
        if c["wave"] == "holdout_controls":
            fmt = lambda x: "N/A" if x is None else f"{x:.3f}"  # noqa: E731
            print(f"{key:28s} M={fmt(c['m_score'])} F={fmt(c['f_score'])} "
                  f"m_missing={c['m_missing']} f_missing={c['f_missing']} err={c['error']}")
    print("consistency:", out["consistency_vs_unified_table"]["tally"])
    print(f"wrote {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
