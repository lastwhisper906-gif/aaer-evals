#!/usr/bin/env python3
"""Closed-form power calculations for an AUC contrast."""

import argparse
import json
import math


# Acklam's inverse-normal rational approximation (2003), followed by one
# Halley correction using erf.  Acklam reports absolute error < 1.15e-9 for
# the rational approximation; the correction makes the probability
# round-trip error < 2e-9 over the finite grid exercised by the tests.
INV_CDF_ROUNDTRIP_MAX_ERROR = 2e-9


def normal_cdf(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def normal_ppf(p):
    """Return the standard-normal quantile for 0 < p < 1."""
    if not 0.0 < p < 1.0:
        raise ValueError("p must be strictly between zero and one")
    a = (-3.969683028665376e1, 2.209460984245205e2,
         -2.759285104469687e2, 1.383577518672690e2,
         -3.066479806614716e1, 2.506628277459239)
    b = (-5.447609879822406e1, 1.615858368580409e2,
         -1.556989798598866e2, 6.680131188771972e1,
         -1.328068155288572e1)
    c = (-7.784894002430293e-3, -3.223964580411365e-1,
         -2.400758277161838, -2.549732539343734,
         4.374664141464968, 2.938163982698783)
    d = (7.784695709041462e-3, 3.224671290700398e-1,
         2.445134137142996, 3.754408661907416)
    low = 0.02425
    if p < low:
        q = math.sqrt(-2.0 * math.log(p))
        x = (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q
              + c[4]) * q + c[5]) / ((((d[0] * q + d[1]) * q
              + d[2]) * q + d[3]) * q + 1.0)
    elif p > 1.0 - low:
        q = math.sqrt(-2.0 * math.log(1.0 - p))
        x = -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q
               + c[4]) * q + c[5]) / ((((d[0] * q + d[1]) * q
               + d[2]) * q + d[3]) * q + 1.0)
    else:
        q = p - 0.5
        r = q * q
        x = (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r
              + a[4]) * r + a[5]) * q / (((((b[0] * r + b[1]) * r
              + b[2]) * r + b[3]) * r + b[4]) * r + 1.0)
    error = normal_cdf(x) - p
    density = math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)
    return x - error / (density + 0.5 * x * error)


def auc_standard_error(auc, n_t, n_c):
    """Hanley--McNeil (1982) SE, with treatment as positive cases."""
    if not 0.0 < auc < 1.0 or n_t < 1 or n_c < 1:
        raise ValueError("auc must be in (0, 1) and group sizes positive")
    # Their exponential-distribution approximation uses
    # Q1=A/(2-A), Q2=2A^2/(1+A), and
    # Var(A)=[A(1-A)+(n_t-1)(Q1-A^2)+(n_c-1)(Q2-A^2)]/(n_t*n_c).
    # It is commonly conservative relative to paired/covariate-aware designs;
    # here the two independent case-control groups provide no such efficiency.
    q1 = auc / (2.0 - auc)
    q2 = 2.0 * auc * auc / (1.0 + auc)
    variance = (auc * (1.0 - auc) + (n_t - 1) * (q1 - auc * auc)
                + (n_c - 1) * (q2 - auc * auc)) / (n_t * n_c)
    return math.sqrt(variance)


def achieved_power(auc1, auc0, n_t, n_c, alpha):
    """Approximate power of a two-sided z-test under auc1."""
    if not 0.0 < alpha < 1.0:
        raise ValueError("alpha must be in (0, 1)")
    delta = auc1 - auc0
    se0 = auc_standard_error(auc0, n_t, n_c)
    se1 = auc_standard_error(auc1, n_t, n_c)
    critical = normal_ppf(1.0 - alpha / 2.0) * se0
    # Both rejection tails are retained, even though the planned alternatives
    # are above their nulls.
    return normal_cdf((delta - critical) / se1) + normal_cdf((-delta - critical) / se1)


def required_n(auc1, auc0, ratio, alpha, power):
    """Return minimum (treatment n, control n, total N); ratio is control:treatment."""
    if ratio <= 0.0 or not 0.0 < power < 1.0:
        raise ValueError("ratio must be positive and power must be in (0, 1)")
    for n_t in range(2, 100000):
        n_c = max(2, math.ceil(ratio * n_t))
        if achieved_power(auc1, auc0, n_t, n_c, alpha) >= power:
            return n_t, n_c, n_t + n_c
    raise ValueError("required sample size exceeds search limit")


def results():
    alternatives = ((0.83, 0.50), (0.83, 0.65))
    ratios = (("1:1", 1.0), ("1:2.75", 2.75))
    powers = (0.80, 0.90)
    required = []
    for auc1, auc0 in alternatives:
        for ratio_label, ratio in ratios:
            row = {"auc1": auc1, "auc0": auc0, "ratio": ratio_label}
            for target in powers:
                n_t, n_c, total = required_n(auc1, auc0, ratio, 0.05, target)
                row[f"power_{target:.2f}"] = {"n_t": n_t, "n_c": n_c, "total_n": total}
            required.append(row)
    actual = []
    for design, n_t, n_c in (("wave-1", 8, 22), ("wave-2", 9, 23),
                              ("E2 trajectory (exploratory, D94)", 12, 7)):
        row = {"design": design, "n_t": n_t, "n_c": n_c}
        for auc1, auc0 in alternatives:
            row[f"{auc1:.2f}_vs_{auc0:.2f}"] = achieved_power(auc1, auc0, n_t, n_c, 0.05)
        actual.append(row)
    return {"alpha": 0.05, "sidedness": "two-sided", "required_n": required,
            "achieved_power": actual}


def format_table(data):
    lines = ["Required N (alpha=0.05, two-sided)",
             "AUC contrast | control:treatment | 80% (n_t/n_c/total) | 90% (n_t/n_c/total)"]
    for row in data["required_n"]:
        p80 = row["power_0.80"]
        p90 = row["power_0.90"]
        lines.append(f'{row["auc1"]:.2f} vs {row["auc0"]:.2f} | {row["ratio"]} | '
                     f'{p80["n_t"]}/{p80["n_c"]}/{p80["total_n"]} | '
                     f'{p90["n_t"]}/{p90["n_c"]}/{p90["total_n"]}')
    lines.extend(["", "Achieved power (alpha=0.05, two-sided)",
                  "Design | n_t/n_c | 0.83 vs 0.50 | 0.83 vs 0.65"])
    for row in data["achieved_power"]:
        lines.append(f'{row["design"]} | {row["n_t"]}/{row["n_c"]} | '
                     f'{row["0.83_vs_0.50"]:.3f} | {row["0.83_vs_0.65"]:.3f}')
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit machine-readable results")
    args = parser.parse_args(argv)
    data = results()
    print(json.dumps(data, indent=2, sort_keys=True) if args.json else format_table(data))


if __name__ == "__main__":
    main()
