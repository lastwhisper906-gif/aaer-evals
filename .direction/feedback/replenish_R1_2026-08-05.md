All reading is done. Here is the R1 review.

---

# R1 REVIEW — code correctness & hidden bugs (loop v2, D-P50 continuous mode)

Session note: `git fetch origin` was blocked by the non-interactive sandbox (INV-17). Mitigation: `git merge-base --is-ancestor origin/main HEAD` confirms local HEAD (5c9d4b4) is **ahead of** origin/main (5abef48), not behind — consistent with the no-push convention, so work may proceed. No commits were created by this review.

## a. EVIDENCE

Primary artifacts read in full from disk (not summaries, not commit messages):

- `pipeline/`: `cutoff_guard.py`, `build_payload.py` (current **and** `git show eafc32b:pipeline/build_payload.py` for the frozen-frame parity check), `runner.py`, `cli_client.py`, `crossmodel_gpt.py`, `test_fingerprint_idempotency.py`; `test_crossmodel_gpt.py` (model-field grep, lines 44–160)
- `tools/`: `verify_blindness.py`, `forward_common.py`, `forward_seal.py`, `forward_verify_seal.py`, `reproduce_analysis.py`, `test_recompute_published.py`, `power_analysis.py`, `stats_annex.py`, `verify_figures.py`, `lint_publication.py`
- `analysis/`: `stats.py`, `wave2_analyze.py`, `decision_table.py`, `fig_tradeoff.py`
- `aaer_eval/statistics.py`, `aaer_eval/verdict.py`
- `scoring/experiment_registry.json` (all `*_globs` entries), `schemas/llm_output.json` (`model` / `fingerprint.model_requested` constraints), `runs/` directory listing
- Exclusion lists read first: `.direction/feedback/BACKLOG.md` (FB-01..09, NB, P1/P2, FB-01-FU1), `DECISIONS_PENDING.md` D-P34..D-P63 headers + D-P49/D-P50 full text, `BOTTLENECKS.md` headers.

## FINDINGS (BACKLOG item format)

### R1-01 Runner stale-superseding resume re-calls the model and overwrites a recorded run output
- category: CODE-FIX · size: S · status: NEW
- **claim affected:** provenance/reproducibility claim — "published numbers trace to fingerprinted outputs" (D-P37 lineage) and the runner's own contract `pipeline/runner.py:13` ("멱등: … 현재 실행 fingerprint 일치 시 skip") and `runner.py:231` ("재개 명령 (완료분 자동 skip)"). Secondary: zero-metered budget (duplicate subscription calls, INV-20 spirit) and INV-06 spirit (a recorded model output in `runs/` is silently replaced pre-commit).
- **evidence:** `pipeline/runner.py:107-141` — the idempotency check inspects only `out_dir/{cid}.json`. When that file exists with a *different* fingerprint, `write_path` becomes the deterministic sibling `{cid}.fp-{suffix}.json` (`runner.py:138-140`) and the model is called **without ever checking whether that sibling already exists with the current fingerprint**. `runner.py:189` then overwrites it. The behavior is *documented by its own test*: `pipeline/test_fingerprint_idempotency.py:119-138` (`test_stale_versioned_path_is_deterministic`) runs `_run` twice with the live `call_model` mock — i.e., the second run re-invokes the model and rewrites the sibling; equality only holds because the mock is deterministic. A live model is not.
- **failure scenario:** mid-run rate-limit HALT after case A was superseded successfully; owner executes the printed resume command; case A's model is called a second time and its previously recorded output is replaced by a different response. If the first sibling was already committed+manifested, `verify_blindness` (d) turns red instead — either way the "resume auto-skips completed work" property is false exactly on the superseding path.
- **fix shape:** before the call, if `write_path.exists()` and its `fingerprint` equals the current fingerprint → return `skip (멱등 — fp-sibling 일치)`. Regression test: third `_run` with `_never_called`. Two-line change + test; no frozen artifact touched; INV-03 disclosure entry (plumbing).

### R1-02 Cross-model GPT runner has no model pin — fail-open provenance for the L-6 claim
- category: CODE-FIX · size: S · status: NEW (blocks parked tranche)
- **claim affected:** the queued cross-model result (D-P48/D-P49: "L-6 same-family-leniency empirical test", A3 "best ROI") — specifically *which model* produced it — and the repo's INV-21 doctrine that harness/model pins are fail-closed before evaluatee calls.
- **evidence:** `pipeline/crossmodel_gpt.py:94-106` — `codex_command()` passes **no `--model` or `-c model=` override**; the served model is whatever the Codex CLI defaults to at launch time. The recorded model is inferred by a recursive any-key search of the event stream (`:109-139`) with a fail-open fallback `MODEL_FALLBACK = "model_string_unavailable"` (`:48`) that is accepted into the published run record (`:253`) and into `fingerprint.model_requested` (`:249`); `schemas/llm_output.json` types `model`/`model_requested` as plain strings, so both pass validation. `codex --version` is checked *after* a successful call and non-fatally degrades to `"harness_version_unavailable"` (`:237-241`). Contrast the Claude arm: `cli_client.py:128-146` (`enforce_harness_pin`, pre-call, fail-closed) and `:173-176`/`:283` (`pin_mismatch` → FAIL). `test_crossmodel_gpt.py:158-160` confirms the model string is recorded, never enforced. D-P49 discloses weaker *isolation* but not the absent pin.
- **failure scenario:** the 30-call tranche runs across a Codex CLI auto-update; cases 1–17 serve one GPT model, 18–30 another, or the event stream omits the model string and a schema-valid record ships with `model: "model_string_unavailable"`. The published cross-model number then cannot name its model — the exact provenance property the rest of the repo enforces mechanically.
- **fix shape:** add `-c model=<pinned-id>` to `codex_command`; post-call fail-closed check `reported model startswith pin` and reject `MODEL_FALLBACK`; pin the codex CLI version pre-call (mirror `enforce_harness_pin`); record the pin choice in the launch packet before the tranche. Tests via existing monkeypatch fixtures. Must land **before** the D-P49 launch command is executed.

### R1-03 Parked GPT tranche writes outside the blindness-scan perimeter — first sanctioned run turns verify-public red
- category: CODE-FIX · size: S · status: NEW (blocks parked tranche)
- **claim affected:** blindness/canary scan coverage claim (`verify_blindness` (b)/(c), INV-09) and the integrity of the D-P49 "ready-to-execute owner command" packet (owner-away constraint: no surprise red gates).
- **evidence:** `scoring/experiment_registry.json` contains **no glob covering `runs/crossmodel_gpt/`** (all `output_globs`/`perturbed_globs`/`aux_globs` enumerated — lines 7–30). `tools/verify_blindness.py:88-99` (`_discovered_paths`) sweeps `runs/**/*.json`, and `:154-155` fails every discovered-but-unregistered file. So the moment the parked launch command (`D-P49`, DECISIONS_PENDING.md:829-832) produces `{cid}.json` + `runmeta_*.json` under `runs/crossmodel_gpt/wave1_original/`, verify_blindness — and with it the 5-gate CI (INV-05) — fails on every file. Conversely, `audit_{frame}_{cid}.jsonl` (`crossmodel_gpt.py:196,223`) matches **no** discovery pattern (`*.json` only) and no registry glob, so the retained Codex event stream is never canary/answer-key scanned at all (only byte-manifested).
- **failure scenario:** owner, relocating and time-boxed, runs the packaged command; next `make verify-public` / push goes red with ~60 "unregistered output surface" failures; the plausible ad-hoc reaction (editing the registry mid-run, unreviewed) is exactly what the fail-closed design is meant to prevent.
- **fix shape:** add a `crossmodel_gpt` experiment entry: `output_globs: ["runs/crossmodel_gpt/**/*.json"]`, `aux_globs: ["runs/crossmodel_gpt/**/*.jsonl"]` (registered aux paths get the canary scan in `check_semantic_scans:186-188`, which reads any registered file regardless of extension) + a test asserting the D-P49 launch out-dir is registry-covered. Fold into the same pre-launch mini-diff as R1-02.

### R1-04 Figure-drift gate verifies the sidecar, never the committed PNG — stale-figure hole in the BN-12 resolution
- category: CODE-FIX · size: S · status: NEW (defect in shipped D-P52 resolution, not a re-raise of BN-12)
- **claim affected:** "published figures are inside the machine-check perimeter" (BN-12 → D-P52), README headline figures.
- **evidence:** `tools/verify_figures.py:45-61` checks (i) PNG *existence* (`:48-50`) and (ii) committed sidecar == `compute_sidecar()` recomputed from current data. The PNG's content is never tied to the data. `analysis/fig_tradeoff.py:104-106` offers `--sidecar-only`, which regenerates the sidecar without rendering — so after a data change, running `--sidecar-only` (or rendering on one machine and committing only the sidecar) yields a green gate with a README PNG that contradicts `decision_table.json`.
- **failure scenario:** decision table regenerated after an upstream fix; sidecar refreshed; PNG forgotten; verify-public PASS; external readers see a figure inconsistent with the committed numbers — the precise silent-drift class BN-12 was resolved to close.
- **fix shape:** generator records `png_sha256` of the freshly-rendered PNG in the sidecar (full-render path only); `verify_figures` compares the committed PNG's hash to it. Hashing the *committed* file sidesteps matplotlib cross-platform nondeterminism. Small; both figure scripts.

## b. VERDICT

`REVISE` — the frozen/published computation paths I audited (wave-1 stats, wave-2 rev2, decision table, recompute gate, reproduce gate, seal manifest, power analysis, MC annex) recompute cleanly and I found no error in any currently published number. The four findings are forward-path correctness bugs, and three of them sit directly on the two next external actions the repo has queued: the parked GPT tranche (R1-02, R1-03 — merged code + a ready-to-execute owner command that would today produce provenance-broken records and a red gate) and any evaluatee resume after a config drift (R1-01, whose double-call/overwrite behavior is even enshrined in its own test). These are exactly the class the priority rule ranks first: correctness defects that would undermine claims *at the moment they are next exercised*.

VERDICT[R1]: REVISE

## c. KILL-OR-DEFER

- **Defer R1-04** to a later batch: it hardens a gate rather than advancing an outward claim, and the immediate risk window is small (both figures and data are currently in sync; regeneration is rare). It is the closest of the four to the owner's over-instrumentation pattern — flagging it honestly rather than bundling it.
- **Shrink R1-03's fix to two registry lines + one test.** Do *not* build any generalized "auto-register new runs/ surfaces" machinery or a registry-coverage linter framework — the failure mode is one known directory created by one known command; generalizing it would be governance bloat.
- Kill nothing in the published-path code: I looked for reasons to and found none.

## d. STEELMAN

The strongest case against REVISE: **none of these bugs can fire today.** The GPT tranche is PARKED by D-P50's phase lock; R1-02/R1-03 are therefore defects in dormant code, arguably pre-launch checklist items rather than bugs, and fixing them now spends loop capacity on an inward-facing path while Phase-1/Observatory outward work is the declared bottleneck. R1-01 requires a fingerprint drift *and* a re-run — under freeze-commit-then-run discipline that conjunction is rare, and the committed-artifact case is already caught downstream by the manifest gate. On this view the correct disposition is APPROVE with four items queued to the owner's launch packet, not REVISE. I hold REVISE because two of the items (R1-02/03) must land *before* an owner-signed command that is already written down as ready-to-execute — leaving them unfixed converts a signed one-step action into a trap — and because R1-01's counter-evidence is its own test, meaning the harness currently *certifies* the wrong behavior.

## e. CLAIM IMPACT

- R1-01 → reproducibility/provenance claim (fingerprinted, idempotently resumable evaluatee runs; `runs/` record permanence).
- R1-02 → the planned cross-model GPT number ("LLM result, not just Claude result"; L-6 empirical test) and the INV-21 pin-provenance property it will be published under.
- R1-03 → blindness/canary scan coverage claim (INV-09) + 5-gate CI green claim (INV-05) on the first sanctioned cross-model run.
- R1-04 → "published figures are machine-checked" claim (BN-12/D-P52), README evidence surface.

No finding is governance-only; each names a mechanical gate or published/queued number. No `CANDIDATE GOVERNANCE BLOAT` flag applies to the findings themselves; R1-04 is the marginal case and is recommended for deferral partly on that ground.

## f. SELF-CRITIQUE PASS

Second pass over a–e:
- **Coverage honesty:** I did *not* read `scoring/grader_runner.py`, `pipeline/probe_runner.py`, `pipeline/date_shift.py` (protected, FU already logged), `pipeline/runner_api.py`/`api_client.py` (raw-API path suspended, D102), `tools/forward_validate.py`/`forward_enumerate.py`/`forward_prepare.py`, the memo pipeline, `analysis/calibration*.py`, `synthesis.py`, e2/e4 runners, `sandbox_guard.py`, `lint_doc_counts.py`. R1 coverage of those files remains open for a future round.
- **Below-floor observations, recorded so they aren't rediscovered:** (i) `verify_blindness.py:174` scans tickers case-*sensitively* (`pair[1].search(text)`) while names scan lowercased text — a model writing a real ticker in lowercase in a perturbed record would escape scan (b); plausibly a deliberate false-positive tradeoff for short tickers, low likelihood, so left below the floor. (ii) `forward_seal.py` writes `SEAL_RECORD.md` outside the manifest — intentional (the record hosts post-seal delay annotations), verified against `forward_common.SEALED_FILES`. (iii) I verified, rather than trusted, the `crossmodel_gpt` docstring's "byte-identical frozen frame" claim against `eafc32b` — key order and value paths match; no finding.
- **Checked and found solid:** the R1-01 evidence chain (I initially suspected the fp-sibling would collide only same-fingerprint; re-read confirmed the suffix is derived from the *current* fingerprint, so the overwrite target is precisely the record a skip-check would have protected), and the R1-03 glob enumeration (re-grepped all three glob kinds before asserting non-coverage).
