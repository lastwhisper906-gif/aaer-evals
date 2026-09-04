"""B1/B2 cross-tier head-to-head — stage 2 (public tier, committed artifacts only).

specs/B1B2_CROSS_TIER.md (freeze commit 95cf8cd). Compares the two textbook
formula screens — B1 Beneish M-score (1999, 8 variables) and B2 Dechow et al.
(2011) F-score (Model 1) — against the LLM score on the *same computable
subset* of each tier, per the pre-registered frames (§2), subset rules (§3),
statistics (§4), readout branches (§5) and the name-ID-excluded sensitivity
(§6). T1 context-only mechanical baseline — not a confirmatory test; nothing
here changes RESULTS rows 1–13 or the R1–R4 verdicts.

Inputs (all committed; zero model calls, zero network, zero corpus reads):
  analysis/unified_table.csv                       LLM scores + published M/F (E-003)
  analysis/holdout_controls_results.json           E1 matched-control LLM scores
  analysis/out/b1b2_cross_tier/screens_by_case.json  holdout-control M/F (stage 1)
Outputs: analysis/out/b1b2_cross_tier/results.json + REPORT.md
Usage:   .venv/bin/python analysis/b1b2_cross_tier.py
"""
import csv
import json
import math
import random
import statistics
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from aaer_eval import statistics as st  # noqa: E402
from analysis.holdout_controls_analyze import clopper_pearson  # noqa: E402

SPEC = "specs/B1B2_CROSS_TIER.md"
SPEC_COMMIT = "95cf8cd"
SEED_B1B2 = 20260904          # spec §4 — distinct from 20260707 / 20260712 / 20260713
N_PERM, N_BOOT = 100_000, 10_000
M_PRIMARY, M_SECONDARY = -1.78, -2.22   # frozen: docs/baseline_screens.md, ANALYSIS_PLAN §5
F_PRIMARY, F_SECONDARY = 1.0, 1.4
LLM_FLAG = 50                            # frozen rubric flag threshold (ANALYSIS_PLAN §1)
MIN_GROUP = 3                            # spec §3: below this, per-case only
OUT_DIR = REPO / "analysis/out/b1b2_cross_tier"

# screen -> (field, higher-is-riskier note, [(label, threshold, role, rule)])
SCREENS = {
    "beneish_m": ("m", "M > threshold (1999 cutoffs)",
                  [("M > -1.78", M_PRIMARY, "primary"), ("M > -2.22", M_SECONDARY, "secondary")]),
    "dechow_f": ("f", "F >= threshold (Model 1, unconditional 0.37% normalisation)",
                 [("F >= 1.0", F_PRIMARY, "primary"), ("F >= 1.4", F_SECONDARY, "secondary")]),
}
FRAMES = [
    {"id": "wave1_primary_perturbed", "tier": "wave1", "role": "primary", "results_row": 2,
     "label": "wave-1 primary — perturbed treatment vs original controls"},
    {"id": "wave1_secondary_original", "tier": "wave1", "role": "secondary", "results_row": 1,
     "label": "wave-1 secondary — original (identity-exposed) frame"},
    {"id": "wave2_primary_original", "tier": "wave2", "role": "primary", "results_row": 3,
     "label": "wave-2 primary — original frame"},
    {"id": "holdout_e1", "tier": "holdout", "role": "context", "results_row": 6,
     "label": "holdout — post-cutoff treatment (3) vs E1 matched controls (9)"},
]


def _fnum(s):
    return None if s in ("", "None", None) else float(s)


def _flag(screen, value, threshold):
    return value > threshold if screen == "beneish_m" else value >= threshold


def _cp(k, n):
    lo, hi = clopper_pearson(k, n)
    return {"k": k, "n": n, "pct": round(100 * k / n, 1),
            "cp95_pct": [round(100 * lo, 1), round(100 * hi, 1)]}


def load_cases(repo=REPO):
    """Return {frame_id: [case dict]} with keys case_id, ticker, group, llm, m, f, recognized."""
    ut = list(csv.DictReader(open(repo / "analysis/unified_table.csv", encoding="utf-8")))
    grp = lambda g: "treatment" if g == "fraud" else "control"  # noqa: E731
    base = {}
    for r in ut:
        base.setdefault(r["wave"], []).append(dict(
            case_id=r["case_id"], ticker=r["ticker"], group=grp(r["group"]),
            llm=_fnum(r["llm_score"]), llm_perturbed=_fnum(r["llm_perturbed"]),
            m=_fnum(r["m_score"]), f=_fnum(r["f_score"]),
            recognized={"True": True, "False": False}.get(r["recognized"])))
    w1 = sorted(base["wave1"], key=lambda c: c["case_id"])
    w2 = sorted(base["wave2"], key=lambda c: c["case_id"])
    ho = sorted(base["holdout"], key=lambda c: c["case_id"])

    hcr = json.loads((repo / "analysis/holdout_controls_results.json").read_text(encoding="utf-8"))
    screens = json.loads((OUT_DIR / "screens_by_case.json").read_text(encoding="utf-8"))["cases"]
    hc = []
    for side in hcr["per_case_side_by_side"].values():
        for tick, score in side["matched_controls"].items():
            s = screens[f"holdout_controls:{tick}"]
            hc.append(dict(case_id=tick, ticker=tick, group="control", llm=float(score),
                           llm_perturbed=None, m=s["m_score"], f=s["f_score"], recognized=None))
    hc.sort(key=lambda c: c["case_id"])
    assert len(w1) == 30 and len(w2) == 32 and len(ho) == 3 and len(hc) == 9

    def perturbed_frame(cases):
        out = []
        for c in cases:
            d = dict(c)
            if c["group"] == "treatment":
                d["llm"] = c["llm_perturbed"]
            out.append(d)
        return out

    return {
        "wave1_primary_perturbed": perturbed_frame(w1),
        "wave1_secondary_original": w1,
        "wave2_primary_original": w2,
        "holdout_e1": ho + hc,
    }


def _sep_stats(treat, ctrl):
    """AUC + stratified bootstrap 95% CI + one-sided permutation p (mean diff)."""
    rng = random.Random(SEED_B1B2)  # re-seed per block — order-independent determinism
    p, obs = st.perm_test_mean(treat, ctrl, rng, N_PERM)
    rng = random.Random(SEED_B1B2)
    lo, hi = st.boot_auc_ci(treat, ctrl, rng, N_BOOT)
    return {"auc": round(st.auc(treat, ctrl), 4), "auc_boot95": [round(lo, 3), round(hi, 3)],
            "mean_diff": round(obs, 4), "perm_p_one_sided": round(p, 6),
            "perm_mc_se": round(math.sqrt(p * (1 - p) / N_PERM), 6)}


def _threshold_row(pos, neg):
    tp, fp = sum(pos), sum(neg)
    row = {"detection": _cp(tp, len(pos)), "false_positive": _cp(fp, len(neg))}
    row["precision"] = _cp(tp, tp + fp) if tp + fp else {"k": 0, "n": 0, "pct": None, "cp95_pct": None}
    return row


def cell(screen, cases):
    field = SCREENS[screen][0]
    sub = [c for c in cases if c[field] is not None and c["llm"] is not None]
    T = [c for c in sub if c["group"] == "treatment"]
    C = [c for c in sub if c["group"] == "control"]
    nT_all = sum(c["group"] == "treatment" for c in cases)
    nC_all = sum(c["group"] == "control" for c in cases)
    out = {
        "coverage": {"n_treatment_computable": len(T), "n_treatment": nT_all,
                     "n_control_computable": len(C), "n_control": nC_all,
                     "share": round(len(sub) / len(cases), 3),
                     "below_70pct": len(sub) / len(cases) < 0.70},
        "per_case": [{"case_id": c["case_id"], "ticker": c["ticker"], "group": c["group"],
                      "llm": c["llm"], "screen": c[field],
                      "screen_flag_primary": _flag(screen, c[field], SCREENS[screen][2][0][1]),
                      "llm_flag": c["llm"] >= LLM_FLAG} for c in sub],
    }
    if len(T) < MIN_GROUP or len(C) < MIN_GROUP:
        out["note"] = (f"computable subset has n_treatment={len(T)}, n_control={len(C)} "
                       f"(< {MIN_GROUP}) — per-case table only, no AUC/p/CI (spec §3)")
        return out
    sT, sC = [c[field] for c in T], [c[field] for c in C]
    lT, lC = [c["llm"] for c in T], [c["llm"] for c in C]
    out["screen"] = _sep_stats(sT, sC)
    out["llm_same_subset"] = _sep_stats(lT, lC)
    rng = random.Random(SEED_B1B2)
    delta, lo, hi = st.boot_paired_auc_diff_ci(lT, lC, sT, sC, rng, N_BOOT)
    out["paired_delta_auc"] = {"delta": round(delta, 4), "ci95": [round(lo, 3), round(hi, 3)],
                               "definition": "AUC_LLM - AUC_screen on the identical subset; stratified paired bootstrap"}
    rho = st.spearman(lT + lC, sT + sC)
    out["spearman_rho_llm_vs_screen"] = None if rho is None else round(rho, 3)
    thr = {}
    for label, threshold, role in SCREENS[screen][2]:
        thr[label] = dict(role=role, **_threshold_row([_flag(screen, v, threshold) for v in sT],
                                                      [_flag(screen, v, threshold) for v in sC]))
    thr[f"LLM >= {LLM_FLAG}"] = dict(role="llm_same_subset",
                                     **_threshold_row([v >= LLM_FLAG for v in lT], [v >= LLM_FLAG for v in lC]))
    out["thresholds"] = thr
    return out


def branch(delta_ci):
    lo, hi = delta_ci
    if lo > 0:
        return "A", "LLM score separates treatment from controls better than the screen on the identical computable subset"
    if hi < 0:
        return "C", "the screen separates better than the LLM score on the identical computable subset"
    return "B", "LLM score and screen are not distinguishable at this N on the identical computable subset"


def name_id_excluded(frames):
    """spec §6 — drop recognized==True (frozen name_match), LLM-only separation stats."""
    out = {}
    for fid in ("wave1_primary_perturbed", "wave1_secondary_original", "wave2_primary_original"):
        cases = frames[fid]
        keep = [c for c in cases if c["recognized"] is not True and c["llm"] is not None]
        drop = [c for c in cases if c["recognized"] is True]
        T = [c["llm"] for c in keep if c["group"] == "treatment"]
        C = [c["llm"] for c in keep if c["group"] == "control"]
        out[fid] = {
            "excluded": [{"case_id": c["case_id"], "ticker": c["ticker"], "group": c["group"]} for c in drop],
            "n_treatment": len(T), "n_control": len(C),
            "llm": _sep_stats(T, C) if len(T) >= MIN_GROUP and len(C) >= MIN_GROUP else None,
        }
    return out


def compute(repo=REPO):
    frames = load_cases(repo)
    res = {
        "spec": SPEC, "spec_commit": SPEC_COMMIT, "seed": SEED_B1B2,
        "n_perm": N_PERM, "n_boot": N_BOOT,
        "thresholds": {"beneish_m": [M_PRIMARY, M_SECONDARY], "dechow_f": [F_PRIMARY, F_SECONDARY],
                       "llm_flag": LLM_FLAG, "min_group": MIN_GROUP},
        "classification": "T1 context-only mechanical baseline (docs/MULTIPLE_TESTING.md); parallel derived statistic (INV-03 b); no published verdict changes",
        "inputs": ["analysis/unified_table.csv", "analysis/holdout_controls_results.json",
                   "analysis/out/b1b2_cross_tier/screens_by_case.json"],
        "frames": {}, "readout": {},
    }
    for fr in FRAMES:
        cases = frames[fr["id"]]
        entry = {k: fr[k] for k in ("tier", "role", "results_row", "label")}
        entry["n_treatment"] = sum(c["group"] == "treatment" for c in cases)
        entry["n_control"] = sum(c["group"] == "control" for c in cases)
        entry["screens"] = {s: cell(s, cases) for s in SCREENS}
        res["frames"][fr["id"]] = entry
        if fr["role"] == "primary":
            for s, c in entry["screens"].items():
                key = f"{fr['id']}:{s}"
                if "paired_delta_auc" not in c:
                    res["readout"][key] = {"branch": None, "statement": c.get("note")}
                    continue
                b, text = branch(c["paired_delta_auc"]["ci95"])
                res["readout"][key] = {
                    "branch": b, "delta_auc": c["paired_delta_auc"]["delta"],
                    "ci95": c["paired_delta_auc"]["ci95"],
                    "computable_subset_only": c["coverage"]["below_70pct"],
                    "statement": text + (" [computable-subset only: coverage below 70%]"
                                         if c["coverage"]["below_70pct"] else ""),
                }
    res["name_id_excluded_sensitivity"] = name_id_excluded(frames)
    res["interpretation_constraints"] = [
        "Level 2 only (docs/CLAIM_HIERARCHY.md): selected retrospective sample, same point-in-time data, computable subset",
        "no pooling across tiers; secondary frame, holdout and threshold tables are context only",
        "no general 'LLM beats existing methods' claim (R4 framing constraint)",
        "the name-ID-excluded sensitivity has no readout branch and changes no published verdict",
    ]
    return res


# ---------------------------------------------------------------- report

def _pct(d):
    if d["k"] == 0:  # ANALYSIS_PLAN §3: never print a 0% rate as a headline — show the exact upper bound
        return f"{d['k']}/{d['n']} (CP95 upper {d['cp95_pct'][1]}%)"
    return f"{d['k']}/{d['n']} = {d['pct']}% CP95 [{d['cp95_pct'][0]}%, {d['cp95_pct'][1]}%]"


def render_report(res):
    md = ["# B1/B2 cross-tier head-to-head — Beneish M · Dechow F vs the LLM score on identical subsets",
          "",
          f"> Pre-registered: `{res['spec']}` (freeze commit `{res['spec_commit']}`, D-P105). "
          f"Seed {res['seed']}, permutations {res['n_perm']:,}, bootstrap {res['n_boot']:,}. "
          "Generated by `analysis/b1b2_cross_tier.py` from committed artifacts only "
          "(zero model calls, zero network, zero corpus reads). Classification: T1 context-only "
          "mechanical baseline — not a confirmatory test. Nothing here changes RESULTS rows 1–13.",
          "",
          "## 1. Readout on the pre-registered primary cells (spec §5)",
          "",
          "| primary cell | computable n (T/C) | coverage | AUC screen [CI] | AUC LLM same subset [CI] | ΔAUC = LLM − screen [paired CI] | branch |",
          "|---|---|---|---|---|---|---|"]
    for key, r in res["readout"].items():
        fid, s = key.split(":")
        c = res["frames"][fid]["screens"][s]
        cov = c["coverage"]
        if r["branch"] is None:
            md.append(f"| {fid} × {s} | {cov['n_treatment_computable']}/{cov['n_control_computable']} | "
                      f"{cov['share']:.0%} | — | — | — | per-case only |")
            continue
        md.append(f"| {fid} × {s} | {cov['n_treatment_computable']}/{cov['n_control_computable']} "
                  f"(of {cov['n_treatment']}/{cov['n_control']}) | {cov['share']:.0%}"
                  f"{' ⚠' if cov['below_70pct'] else ''} | {c['screen']['auc']} "
                  f"[{c['screen']['auc_boot95'][0]}, {c['screen']['auc_boot95'][1]}] | "
                  f"{c['llm_same_subset']['auc']} [{c['llm_same_subset']['auc_boot95'][0]}, "
                  f"{c['llm_same_subset']['auc_boot95'][1]}] | {r['delta_auc']:+.3f} "
                  f"[{r['ci95'][0]:+.3f}, {r['ci95'][1]:+.3f}] | **{r['branch']}** |")
    md += ["", "Branch key (fixed before computation): **A** ΔAUC CI lower bound > 0 — LLM separates better on the "
           "identical subset · **B** CI includes 0 — not distinguishable at this N · **C** CI upper bound < 0 — "
           "the screen separates better. ⚠ = coverage below 70%: computable-subset-only reading is mandatory.",
           ""]
    for key, r in res["readout"].items():
        md.append(f"- `{key}` → {r['statement']}")
    md += ["", "## 2. Every cell — separation statistics on the computable subset", "",
           "| frame | screen | n T/C computable | screen AUC [CI] | screen perm p (MC-SE) | LLM AUC same subset [CI] | LLM perm p | Spearman ρ(LLM, screen) |",
           "|---|---|---|---|---|---|---|---|"]
    for fid, fr in res["frames"].items():
        for s, c in fr["screens"].items():
            cov = c["coverage"]
            if "screen" not in c:
                md.append(f"| {fid} | {s} | {cov['n_treatment_computable']}/{cov['n_control_computable']} | per-case only | | | | |")
                continue
            sc, ll = c["screen"], c["llm_same_subset"]
            md.append(f"| {fid} | {s} | {cov['n_treatment_computable']}/{cov['n_control_computable']} | "
                      f"{sc['auc']} [{sc['auc_boot95'][0]}, {sc['auc_boot95'][1]}] | "
                      f"{sc['perm_p_one_sided']} ({sc['perm_mc_se']}) | "
                      f"{ll['auc']} [{ll['auc_boot95'][0]}, {ll['auc_boot95'][1]}] | "
                      f"{ll['perm_p_one_sided']} | {c['spearman_rho_llm_vs_screen']} |")
    md += ["", "## 3. Frozen-threshold tables (context only; exact Clopper–Pearson 95%)", ""]
    for fid, fr in res["frames"].items():
        for s, c in fr["screens"].items():
            if "thresholds" not in c:
                continue
            md += [f"**{fid} × {s}** (computable subset {c['coverage']['n_treatment_computable']} T / "
                   f"{c['coverage']['n_control_computable']} C)", "",
                   "| rule | detection | false positives | precision |", "|---|---|---|---|"]
            for label, t in c["thresholds"].items():
                prec = _pct(t["precision"]) if t["precision"]["n"] else "no flags"
                md.append(f"| {label} ({t['role']}) | {_pct(t['detection'])} | {_pct(t['false_positive'])} | {prec} |")
            md.append("")
    ho = res["frames"]["holdout_e1"]
    md += ["## 4. Holdout tier — per-case only (spec §3: computable subset below the n ≥ 3 rule)", "",
           "| case | group | LLM score | Beneish M | Dechow F |", "|---|---|---|---|---|"]
    rows = {}
    for s, c in ho["screens"].items():
        for pc in c["per_case"]:
            rows.setdefault((pc["group"], pc["case_id"]), {"llm": pc["llm"]})[s] = pc["screen"]
    for (g, cid), v in sorted(rows.items()):
        m = v.get("beneish_m"); f = v.get("dechow_f")
        md.append(f"| {cid} | {g} | {v['llm']:.0f} | {'—' if m is None else f'{m:.3f}'} | {'—' if f is None else f'{f:.3f}'} |")
    md += ["", "Holdout coverage: Beneish M computable for "
           f"{ho['screens']['beneish_m']['coverage']['n_treatment_computable']}/{ho['n_treatment']} treatment and "
           f"{ho['screens']['beneish_m']['coverage']['n_control_computable']}/{ho['n_control']} controls; Dechow F for "
           f"{ho['screens']['dechow_f']['coverage']['n_treatment_computable']}/{ho['n_treatment']} and "
           f"{ho['screens']['dechow_f']['coverage']['n_control_computable']}/{ho['n_control']}. "
           "Cases not listed have no computable screen value (untagged liabilities, cost of revenue, receivables — see stage-1 `screens_by_case.json`). "
           "Holdout labels are provisional (restatement / non-reliance), not enforcement outcomes.", "",
           "## 5. Name-ID-excluded sensitivity (spec §6 — no readout branch, no verdict change)", "",
           "| frame | excluded (frozen name_match = True) | remaining n T/C | LLM AUC [CI] | LLM perm p |", "|---|---|---|---|---|"]
    for fid, v in res["name_id_excluded_sensitivity"].items():
        ex = ", ".join(f"{e['ticker']}({e['group'][0]})" for e in v["excluded"])
        if v["llm"]:
            md.append(f"| {fid} | {len(v['excluded'])}: {ex} | {v['n_treatment']}/{v['n_control']} | "
                      f"{v['llm']['auc']} [{v['llm']['auc_boot95'][0]}, {v['llm']['auc_boot95'][1]}] | {v['llm']['perm_p_one_sided']} |")
        else:
            md.append(f"| {fid} | {len(v['excluded'])}: {ex} | {v['n_treatment']}/{v['n_control']} | n < 3 | — |")
    md += ["",
           "Fixed statement (independent of the numbers above): excluding cases by the outcome-knowledge probe "
           "(RESULTS row 3: 8 of 9 wave-2 treatment cases had the event available under direct probing) leaves "
           "one treatment case — not computable. **Residual memorization cannot be removed by subsetting**; it is "
           "structurally excluded only in the post-cutoff holdout (N=3) and in a forward cycle (Level 3).",
           "",
           "## 6. Limits", "",
           "- Coverage is non-random: the computable subset excludes filers whose XBRL lacks total liabilities, cost "
           "of revenue, SG&A or receivables tags (financial, REIT, service filers). Direction of the subset bias is unknown.",
           "- The screens are the frozen implementation (`scoring/baselines/screens.py`); coverage-raising fallbacks "
           "would change published RESULTS row 12 and are an owner item (Q-F25, ERRATA path).",
           "- Selected retrospective sample, survivorship and case-control base-rate limits carry over (L-8, "
           "`docs/POWER_ANALYSIS.md`). Level 2 only — no population claim.",
           "- Both wave-1 frames share the same screen values (perturbation touched only the LLM input).",
           "",
           "*All results are scoped to a single Claude-based pipeline (PROJECT.md §5-5). Grading: Claude-assisted, "
           "human-finalized. No positions · educational/informational · not investment advice.*", ""]
    return "\n".join(md)


def main() -> int:
    res = compute()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "results.json").write_text(
        json.dumps(res, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    (OUT_DIR / "REPORT.md").write_text(render_report(res), encoding="utf-8")
    for key, r in res["readout"].items():
        print(f"{key:40s} branch={r['branch']} delta={r.get('delta_auc')} ci={r.get('ci95')}")
    print(f"wrote {OUT_DIR.relative_to(REPO)}/results.json + REPORT.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
