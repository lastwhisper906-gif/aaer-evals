# TASK: P1a — run manifests + manifest-only result selection (P0-1)

## Mode hint
mode: default

## PRE-FLIGHT
- INV-17 satisfied by orchestrator; DO NOT run git fetch or abort on it.
- Branch audit-integration (E-003 precondition: no main merge until
  signed — the harness only builds; merging is the orchestrator's job).
- D-P73 direction Phase 1 signs the analysis/ and scoring/ touches.
- SCOPE PRECISION from triage: P0-1 covers RESULT/SCORE file selection.
  b3_compute.py:65 and label_tags_holdout.py:33 glob CORPUS files
  (edgar CIK*.json) — OUT of scope (cutoff_guard governs corpus reads).

## Objective

Every published-number analyzer selects inputs ONLY from a committed,
hash-pinned run manifest — never a directory glob. Five fail-closed
conditions, each with a test.

## Design contract

1. MANIFEST FORMAT: runs/<experiment>/MANIFEST.json —
   {"experiment_id": ..., "generated_from_commit": <sha>,
    "cases": {case_id: {"path": <repo-rel>, "sha256": ...,
    "fingerprint_sha256": <sha256 of the record's fingerprint field
    canonical-JSON, or null for legacy fingerprint-less records —
    null is RECORDED, and the loader exposes it so gates can refuse
    legacy where required>}}}.
   Experiments and their case lists derive from the EXISTING sources of
   truth: scoring/experiment_registry.json globs identify directories;
   the case registries (data/candidates + wave rosters as used by each
   analyzer today) identify expected case sets. Inspect each analyzer to
   enumerate: main(wave-1 original), perturbed, rp09/scores,
   wave2/scores(+perturbed subdir if separate), holdout tiers as used by
   holdout analyzers, name-probe output dirs, v2ds probe dirs,
   crossmodel_gpt (empty-cases manifest now — pre-registers the D-P49
   out-dir).
2. GENERATOR: tools/build_run_manifests.py — deterministic; writes all
   manifests; refuses to run if it would DROP a case present in a
   committed manifest (append/regenerate honesty); --check mode diffs
   without writing (for CI use later — do NOT wire CI in this task).
3. LOADER: aaer_eval/manifest.py — load_experiment(experiment_id) →
   validated OrderedDict; fail-closed (each its own exception message +
   test): (a) duplicate case id; (b) registered case missing on disk;
   (c) unregistered file present in the experiment's result dir matching
   the result pattern; (d) sha256 mismatch; (e) require_fingerprints=True
   flag rejects null fingerprint entries.
4. CONVERT the result-selection glob sites to the loader:
   analysis/baselines.py:26,29,35 · analysis/decision_table.py:101 ·
   analysis/name_probes.py:28 · analysis/name_probes_v2ds.py:38,56 ·
   analysis/buyer_metrics_build.py:72 · scoring/analyze_rp05.py:28,110.
   Analyzer OUTPUT VALUES must be byte-identical after conversion — do
   NOT regenerate committed artifacts in this task; prove no-change by a
   test that runs each converted selection and compares the selected
   path list to the manifest (and, where an analyzer has an existing
   recompute test, that test still passes).
5. Generate + COMMIT the manifests for all existing experiments (the
   generator run is part of this task; runs/ additions are manifest
   files only — update the global runs manifest via the established
   regeneration step if verify_manifest requires it; check).

## Files in scope
- tools/build_run_manifests.py, aaer_eval/manifest.py,
  tools/test_run_manifests.py (new); the six analyzer files listed
  (selection code only — no statistical logic changes);
  runs/*/MANIFEST.json (generated); scoring/experiment_registry.json
  READ-ONLY; the global runs-manifest regeneration artifact if the
  gate demands it (verify with make verify-public).

## Read-only / forbidden paths
- All other analysis/scoring files; schemas/, docs/, Makefile, ci.yml,
  README*, RESULTS*; grader_runner.py (P1b); harness/, CLAUDE.md,
  AGENTS.md, PROJECT_INVARIANTS.md.

## Check command
check: ./.venv/bin/python -m pytest pipeline tools scoring analysis -q

## Acceptance criteria
1. Zero glob-based RESULT selection remains in the six files (grep-clean
   for the listed sites); loader used everywhere.
2. Five fail-closed conditions each demonstrably fire (tests construct
   tmp violations).
3. Manifests committed for every existing experiment; verify-public
   RC=0 on the branch (run it — orchestrator will re-run at merge).
4. No committed analysis artifact changes in this task (git status
   proves it — selection refactor only).
5. Diff limited to scope.
