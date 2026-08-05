# TASK: P1-03 — BN-12: ordinal axis label + sidecar figure-drift gate in verify-public

## Mode hint
mode: default

## PRE-FLIGHT — read first
- INV-17 already satisfied by the orchestrator. DO NOT run `git fetch`;
  do not abort on its failure.
- D-P50 owner direction explicitly orders this item (Phase 1 #3); the
  analysis/ and Makefile touches below are signed-scope, minimal, and the
  post-review must verify them hunk-by-hunk.

## Objective

BN-12 resolution condition, verbatim: "README-referenced figures
regenerate from committed artifacts with ordinal-convention labels and a
gate step fails on drift, with make verify-public RC=0 after wiring."
Two parts: (1) fix `analysis/fig_dotplot.py:40` axis label
"Misstatement probability (evaluatee output, original frame)" →
"Evaluatee risk score (0-100, ordinal; original frame)" and regenerate
the PNG deterministically; (2) add a cross-platform drift gate — NOT
pixel bytes (fonts differ across macOS/CI): each figure script emits a
JSON SIDECAR capturing what the figure claims (source-data digest + axis
labels + annotation strings), and a checker regenerates sidecars from
committed artifacts and fails on any difference vs the committed ones.

## Files in scope

- analysis/fig_dotplot.py — modify: (a) the label fix at :40 AND the
  line-25 annotation "flag threshold p=50" → "flag threshold T=50"
  (probability shorthand off the first-screen figure; nothing else in
  the plotting); (b) factor an importable `compute_sidecar()` and a
  sidecar-only entry point (`--sidecar-only` flag) so sidecar emission
  NEVER re-renders the PNG; add `--out` argparse (fig_tradeoff pattern)
  so render tests target tmp; when the script IS run for a full render
  it also writes
  `analysis/fig_dotplot_30firms.sidecar.json`: {"figure":
  "fig_dotplot_30firms.png", "data_sha256": sha256 of the canonical
  JSON of the exact plotted rows (case_id, group, llm_score sorted),
  "xlabel": ..., "annotations": [every ax.annotate/legend string],
  "generator": "analysis/fig_dotplot.py"} — derived ONLY from committed
  artifacts + the script's own constants.
- analysis/fig_tradeoff.py — modify: same compute_sidecar() +
  --sidecar-only pattern (`analysis/fig_tradeoff.sidecar.json`; data =
  the plotted layer cells canonical-JSON sha256, labels, the two
  operating-point annotation strings). Generating the sidecar must NOT
  rewrite fig_tradeoff.png (out of scope).
- analysis/fig_dotplot_30firms.png — regenerate (label change is the
  only visual delta).
- analysis/fig_dotplot_30firms.sidecar.json,
  analysis/fig_tradeoff.sidecar.json — create (run both scripts once).
- tools/verify_figures.py — create: for each registered figure script
  (explicit list of the two), import-and-run its sidecar-computation
  function (scripts must factor sidecar computation into an importable
  `compute_sidecar()` so the checker does NOT need to render pixels —
  fast, no matplotlib needed in the checker), compare against the
  committed sidecar file; any mismatch → nonzero exit naming the field.
  Also fail if a README-referenced PNG in the explicit list is missing.
  (The three legacy companion figures — reliability, dose-response,
  decomposition — are OUT of scope: register only the two
  current-generation figures, with a comment giving the SEMANTIC reason:
  the reliability diagram exists to test the probability hypothesis and
  the memorization figures are label-clean; their generators
  (calibration.py / synthesis.py / fig_memorization.py — note the real
  filenames) are frozen wave-1 outputs. Do NOT touch them.)
- Makefile — modify: verify-public gains ONE additive line
  `.venv/bin/python tools/verify_figures.py` (existing 6 commands
  verbatim, INV-05).
- tools/test_verify_figures.py — create: (a) checker passes on the
  committed tree; (b) a tampered sidecar (tmp copy, one label changed)
  fails naming the field; (c) fig_dotplot's compute_sidecar reflects the
  NEW ordinal label and the T=50 annotation (regression-pins BN-12);
  (d) checker needs no display/backend (no pyplot import at checker
  module level); (e) BOTH figures render to tmp as nonempty PNGs via
  --out (this makes "regenerates from committed artifacts" literally
  true inside verify-public's pytest gate).

## Read-only / forbidden paths
- harness/, CLAUDE.md, AGENTS.md, PROJECT_INVARIANTS.md (always)
- BOTTLENECKS.md (status flip = orchestrator at merge with D-entry),
  README*, RESULTS*, runs/, scoring/, schemas/, pipeline/
- analysis/calibration.py, synthesis.py, fig_memorization.py and the
  three legacy PNGs — frozen, untouched
- every other existing analysis/ file

## Check command
check: ./.venv/bin/python -m pytest analysis tools -q

## Acceptance criteria
1. fig_dotplot.py:40 label is the ordinal convention; PNG regenerated;
   no other visual-element change in the diff.
2. Both scripts factor an importable compute_sidecar(); sidecars
   committed; verify_figures.py compares recomputed-vs-committed and
   fails on drift naming the field.
3. Makefile verify-public = previous 6 commands verbatim + 1 additive
   figure line; `make verify-public` RC=0 on the finished tree.
4. Tests (a)-(d) pass; check command passes.
5. Diff touches ONLY the eight listed paths (2 scripts, 1 PNG, 2 sidecars, checker, Makefile, test).

## Explicitly out of scope
- Pixel/byte comparison gates (cross-platform fonts — sidecar semantics
  is the gate); legacy figure scripts; README caption edits; BN-12
  status flip (orchestrator).

## Notes / context
- MERGE PROTOCOL: docs-refresh at merge (test count changes); INV-03
  D-entry + BN-12 flip by orchestrator. Flip evidence must state
  honestly: 2 current-generation figures gated (semantics via sidecar +
  render-in-pytest); 3 legacy figures excluded with semantic reasons;
  committed PNG bytes attested by same-run convention + git review, not
  machine-compared.
