"""specs/B1B2_CROSS_TIER.md §8 test contract — public tier (no corpus, no network).

1 determinism · 2 recompute == committed results.json (MC tolerances for perm p /
bootstrap CI, exact elsewhere) · 3 frozen-threshold lock · 4 n<3 subset rule ·
5 paired-bootstrap helper · 6 screen values byte-identical to unified_table ·
7 stage-1 consistency block reports zero mismatches.
"""
import csv
import json
import random
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from aaer_eval import statistics as st  # noqa: E402
from analysis import b1b2_cross_tier as b  # noqa: E402

PERM_TOL = 3e-3   # tools/test_recompute_published.py convention
CI_TOL = 2e-2
OUT = REPO / "analysis/out/b1b2_cross_tier"
_cache = {}


def _computed():
    if "res" not in _cache:
        _cache["res"] = json.loads(json.dumps(b.compute(), sort_keys=True))
    return _cache["res"]


def _committed():
    return json.loads((OUT / "results.json").read_text(encoding="utf-8"))


def _walk(a, b_, path=""):
    """Yield (path, a, b) leaves; both trees must share structure."""
    if isinstance(a, dict):
        assert isinstance(b_, dict) and a.keys() == b_.keys(), path
        for k in a:
            yield from _walk(a[k], b_[k], f"{path}/{k}")
    elif isinstance(a, list):
        assert isinstance(b_, list) and len(a) == len(b_), path
        for i, (x, y) in enumerate(zip(a, b_)):
            yield from _walk(x, y, f"{path}[{i}]")
    else:
        yield path, a, b_


def test_1_determinism_same_seed_same_result(monkeypatch):
    # determinism holds at any Monte-Carlo size; run small so the gate stays fast
    monkeypatch.setattr(b, "N_PERM", 2_000)
    monkeypatch.setattr(b, "N_BOOT", 500)
    first = json.dumps(b.compute(), sort_keys=True)
    second = json.dumps(b.compute(), sort_keys=True)
    assert first == second


def test_2_recompute_matches_committed_within_mc_tolerance():
    got, want = _computed(), _committed()
    for path, x, y in _walk(got, want):
        tail = path.rsplit("/", 1)[-1]
        if "perm_p_one_sided" in path or "perm_mc_se" in path:
            assert abs(x - y) <= PERM_TOL, (path, x, y)
        elif "auc_boot95" in path or "/ci95" in path:
            assert abs(x - y) <= CI_TOL, (path, x, y)
        else:
            assert x == y, (path, x, y)
    # the readout branches are exact-locked — a branch flip is a real change, not MC noise
    assert {k: v["branch"] for k, v in got["readout"].items()} == \
           {k: v["branch"] for k, v in want["readout"].items()}


def test_3_frozen_thresholds_locked():
    src = (REPO / "analysis/b1b2_cross_tier.py").read_text(encoding="utf-8")
    assert "M_PRIMARY, M_SECONDARY = -1.78, -2.22" in src
    assert "F_PRIMARY, F_SECONDARY = 1.0, 1.4" in src
    assert "LLM_FLAG = 50" in src
    assert "SEED_B1B2 = 20260904" in src
    frozen = (REPO / "scoring/baselines/screens.py").read_text(encoding="utf-8")
    assert "m > -1.78" in frozen and "m > -2.22" in frozen
    # no observed screen value sits exactly on a threshold, so '>' (screens.py) and '>=' (spec) coincide
    for fr in _computed()["frames"].values():
        for s, c in fr["screens"].items():
            for pc in c["per_case"]:
                assert pc["screen"] not in b.SCREENS[s][2][0][1:2] + b.SCREENS[s][2][1][1:2]


def test_4_small_subsets_are_per_case_only():
    res = _computed()
    for fid, fr in res["frames"].items():
        for s, c in fr["screens"].items():
            cov = c["coverage"]
            small = cov["n_treatment_computable"] < b.MIN_GROUP or cov["n_control_computable"] < b.MIN_GROUP
            assert small == ("screen" not in c), (fid, s)
            assert small == ("note" in c), (fid, s)
    ho = res["frames"]["holdout_e1"]["screens"]
    assert "screen" not in ho["beneish_m"] and "screen" not in ho["dechow_f"]
    assert all(k in res["readout"] for k in (
        "wave1_primary_perturbed:beneish_m", "wave1_primary_perturbed:dechow_f",
        "wave2_primary_original:beneish_m", "wave2_primary_original:dechow_f"))
    assert len(res["readout"]) == 4


def test_5_paired_bootstrap_helper():
    rng = random.Random(1)
    a, c = [70, 60, 55, 80], [30, 20, 40, 10, 25]
    delta, lo, hi = st.boot_paired_auc_diff_ci(a, c, a, c, rng, 500)
    assert (delta, lo, hi) == (0.0, 0.0, 0.0)
    rng = random.Random(1)
    flat_a, flat_c = [50] * 4, [50] * 5           # constant scorer: AUC 0.5 always
    delta, lo, hi = st.boot_paired_auc_diff_ci(a, c, flat_a, flat_c, rng, 500)
    assert delta == 0.5 and lo > 0 and hi == 0.5
    try:
        st.boot_paired_auc_diff_ci(a, c, a[:-1], c, rng, 10)
    except ValueError:
        pass
    else:
        raise AssertionError("misaligned inputs must be refused")


def test_6_screen_values_identical_to_unified_table():
    ut = {(r["wave"], r["case_id"]): r
          for r in csv.DictReader(open(REPO / "analysis/unified_table.csv", encoding="utf-8"))}
    wave_of = {"wave1_primary_perturbed": "wave1", "wave1_secondary_original": "wave1",
               "wave2_primary_original": "wave2"}
    res = _computed()
    n = 0
    for fid, w in wave_of.items():
        for s, c in res["frames"][fid]["screens"].items():
            col = {"beneish_m": "m_score", "dechow_f": "f_score"}[s]
            for pc in c["per_case"]:
                assert float(ut[(w, pc["case_id"])][col]) == pc["screen"], (fid, s, pc["case_id"])
                n += 1
    assert n == 2 * (22 + 22) + 20 + 17   # wave-1 both frames (M 22, F 22) + wave-2 (M 20, F 17)


def test_7_stage1_consistency_block_has_no_mismatch():
    s1 = json.loads((OUT / "screens_by_case.json").read_text(encoding="utf-8"))
    tally = s1["consistency_vs_unified_table"]["tally"]
    assert not any(k.endswith("mismatch") or k.endswith("mismatch_none") for k in tally), tally
    assert s1["n_cases"] == 74
    hc = {k: v for k, v in s1["cases"].items() if v["wave"] == "holdout_controls"}
    assert len(hc) == 9
    assert all(v["group"] == "control" for v in hc.values())
