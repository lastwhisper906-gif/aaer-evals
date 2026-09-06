#!/usr/bin/env python3
"""Report Monte-Carlo uncertainty and provenance from committed artifacts."""

import argparse
import json
import math
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]

# B citations (read-only sources): analysis/stats.py:16 and
# analysis/legacy/wave2_analyze_v1.py:29.  Estimator citations:
# analysis/stats.py:41 and analysis/legacy/wave2_analyze_v1.py:34.
SOURCES = {
    "wave1": {
        "b": 100_000,
        "b_source": "analysis/stats.py:16",
        "estimator_source": "analysis/stats.py:41",
    },
    "wave2": {
        "b": 100_000,
        "b_source": "analysis/legacy/wave2_analyze_v1.py:29",
        "estimator_source": "analysis/legacy/wave2_analyze_v1.py:34",
    },
}


def load_artifacts():
    with (REPO / "analysis/results_stats.json").open(encoding="utf-8") as f:
        wave1 = json.load(f)
    with (REPO / "analysis/wave2_results.json").open(encoding="utf-8") as f:
        wave2 = json.load(f)
    return wave1, wave2


def build_annex():
    wave1, wave2 = load_artifacts()
    specs = [
        ("wave1 primary", "analysis/results_stats.json", "primary.perm_p_one_sided", wave1["primary"]["perm_p_one_sided"], "wave1", "8v22"),
        ("wave1 secondary", "analysis/results_stats.json", "secondary.perm_p_one_sided", wave1["secondary"]["perm_p_one_sided"], "wave1", "8v22"),
        ("wave1 Beneish separation", "analysis/results_stats.json", "baselines.beneish_m.own_separation.perm_p", wave1["baselines"]["beneish_m"]["own_separation"]["perm_p"], "wave1", "6v16"),
        ("wave1 Beneish residual", "analysis/results_stats.json", "baselines.beneish_m.r2_residual_test.perm_p", wave1["baselines"]["beneish_m"]["r2_residual_test"]["perm_p"], "wave1", "6v16"),
        ("wave1 Dechow separation", "analysis/results_stats.json", "baselines.dechow_f.own_separation.perm_p", wave1["baselines"]["dechow_f"]["own_separation"]["perm_p"], "wave1", "6v16"),
        ("wave1 Dechow residual", "analysis/results_stats.json", "baselines.dechow_f.r2_residual_test.perm_p", wave1["baselines"]["dechow_f"]["r2_residual_test"]["perm_p"], "wave1", "6v16"),
        ("wave2 original", "analysis/wave2_results.json", "original.perm_p", wave2["original"]["perm_p"], "wave2", "9v23"),
        ("wave2 perturbed", "analysis/wave2_results.json", "perturbed.perm_p", wave2["perturbed"]["perm_p"], "wave2", "9v23"),
        ("pooled secondary", "analysis/wave2_results.json", "pooled_secondary.perm_p", wave2["pooled_secondary"]["perm_p"], "wave2", "17v45"),
    ]
    mc_rows = []
    for label, artifact, key, p, source_name, design in specs:
        source = SOURCES[source_name]
        b = source["b"]
        se = math.sqrt(p * (1.0 - p) / b)
        mc_rows.append({
            "label": label, "artifact": artifact, "key": key, "p": p,
            "B": b, "B_source": source["b_source"], "mc_se": se,
            "mc_interval_95": [p - 1.96 * se, p + 1.96 * se],
            "design": design,
            "estimator": "(ge+1)/(n+1)",
            "estimator_source": source["estimator_source"],
        })

    designs = [("6v16", 22, 6, True), ("8v22", 30, 8, True),
               ("9v23", 32, 9, True), ("17v45", 62, 17, False)]
    exact_rows = [{
        "design": name, "n": n, "n_t": n_t,
        "permutations": math.comb(n, n_t),
        "enumerable_on_commodity_hardware": feasible,
    } for name, n, n_t, feasible in designs]

    provenance = [
        {"artifact": "analysis/results_stats.json", "key": "seed", "value": wave1["seed"], "provenance": "recorded in artifact"},
        {"artifact": "analysis/results_stats.json", "key": "primary.auc_boot95", "value": wave1["primary"]["auc_boot95"], "provenance": "recorded in artifact"},
        {"artifact": "analysis/results_stats.json", "key": "secondary.auc_boot95", "value": wave1["secondary"]["auc_boot95"], "provenance": "recorded in artifact"},
        {"artifact": "analysis/wave2_results.json", "key": "seed", "value": 20260707, "provenance": "not in artifact; source: analysis/legacy/wave2_analyze_v1.py:12"},
        {"artifact": "analysis/wave2_results.json", "key": "original.auc_ci", "value": wave2["original"]["auc_ci"], "provenance": "recorded in artifact; method source: analysis/legacy/wave2_analyze_v1.py:40-44"},
    ]
    return {"mc_p_values": mc_rows, "exact_permutation_feasibility": exact_rows,
            "seed_and_ci_provenance": provenance}


def render(data):
    lines = ["MONTE-CARLO PERMUTATION P-VALUES",
             "label | artifact key | p | B (source) | MC-SE | 95% MC interval | estimator (source)"]
    for row in data["mc_p_values"]:
        lo, hi = row["mc_interval_95"]
        lines.append(
            f'{row["label"]} | {row["artifact"]}:{row["key"]} | {row["p"]!r} | '
            f'{row["B"]} ({row["B_source"]}) | {row["mc_se"]:.12g} | '
            f'[{lo:.12g}, {hi:.12g}] | {row["estimator"]} ({row["estimator_source"]})')
    lines += ["", "EXACT-PERMUTATION FEASIBILITY",
              "design | C(n,n_t) | enumerable on commodity hardware"]
    for row in data["exact_permutation_feasibility"]:
        yn = "yes" if row["enumerable_on_commodity_hardware"] else "no"
        lines.append(f'{row["design"]} | {row["permutations"]} | {yn}')
    lines += ["", "SEED AND AUC-CI PROVENANCE", "artifact key | value | provenance"]
    for row in data["seed_and_ci_provenance"]:
        value = json.dumps(row["value"], separators=(",", ":"))
        lines.append(f'{row["artifact"]}:{row["key"]} | {value} | {row["provenance"]}')
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    data = build_annex()
    if args.json:
        print(json.dumps(data, indent=2, sort_keys=True))
    else:
        print(render(data), end="")


if __name__ == "__main__":
    main()
