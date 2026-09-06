#!/usr/bin/env python3
"""Load frozen confirmatory p-values and apply Holm--Bonferroni."""

import argparse
import json
from pathlib import Path


SOURCES = (
    ("RESULTS row 1: wave-1 identity-exposed", "analysis/results_stats.json", ("primary", "perm_p_one_sided")),
    ("RESULTS row 1: wave-1 identity-exposed Fisher", "analysis/results_stats.json", ("primary", "fisher_2x2", "p_one_sided")),
    ("RESULTS row 2: wave-1 perturbed", "analysis/results_stats.json", ("secondary", "perm_p_one_sided")),
    ("RESULTS row 2: wave-1 perturbed Fisher", "analysis/results_stats.json", ("secondary", "fisher_2x2", "p_one_sided")),
    ("RESULTS row 3: wave-2 standalone", "analysis/wave2_results.json", ("original", "perm_p")),
    ("RESULTS row 3: wave-2 perturbed", "analysis/wave2_results.json", ("perturbed", "perm_p")),
)


def holm_adjust(p_values):
    """Return Holm adjusted p-values in the input order."""
    count = len(p_values)
    if not count or any(not 0 <= value <= 1 for value in p_values):
        raise ValueError("p-values must be a non-empty sequence in [0, 1]")
    ordered = sorted(enumerate(p_values), key=lambda item: (item[1], item[0]))
    adjusted = [0.0] * count
    running = 0.0
    for rank, (index, value) in enumerate(ordered):
        running = max(running, (count - rank) * value)
        adjusted[index] = min(1.0, running)
    return adjusted


def load_confirmatory(root):
    """Load, never reconstruct, the frozen values named by RESULTS.md."""
    loaded = []
    cache = {}
    for label, relative, keys in SOURCES:
        path = Path(root) / relative
        if not path.is_file():
            raise FileNotFoundError(f"required frozen artifact missing: {path}")
        if relative not in cache:
            with path.open(encoding="utf-8") as handle:
                cache[relative] = json.load(handle)
        value = cache[relative]
        for key in keys:
            value = value[key]
        loaded.append((label, relative + ":" + ".".join(keys), float(value)))
    return loaded


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    rows = load_confirmatory(args.root)
    adjusted = holm_adjust([row[2] for row in rows])
    print("label | frozen source | raw p | Holm adjusted p")
    for (label, source, raw), corrected in zip(rows, adjusted):
        print(f"{label} | {source} | {raw!r} | {corrected:.12g}")


if __name__ == "__main__":
    main()
