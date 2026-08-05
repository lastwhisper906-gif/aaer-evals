# BACKLOG.md — merged external-feedback backlog (2026-08-05)

Sources: EXT_FB_A_2026-08-05.md (A1–A8), EXT_FB_B_2026-08-05.md (B1–B11).
Every code-level claim was verified against the working tree at 37ac75b
before inclusion (verification evidence inline). Ordering follows the
owner's priority rule: (1) correctness bugs undermining published claims →
(2) cheap high-leverage → (3) executable design/stats → (4) OWNER-GATED /
INVARIANT-CONFLICT items to DECISIONS_PENDING only.

Loop protection rule in force: frozen/sealed/published artifacts (INV-06
set), measurement-condition definitions (schema semantics, thresholds,
metric names, evaluatee prompts), and owner-signature surfaces are never
edited by the build loop. Pipeline plumbing fixes named by the owner's
priority rule carry an INV-03 disclosure entry in DECISIONS_PENDING.md.

## Tier 1 — CODE-FIX, direct claim impact

### FB-01 Perturbation blindness: strip experiment markers from model payload
- source: B1 (A6 adjacent) · category: CODE-FIX · size: S · status: DONE (2026-08-05, D-P35, L-9)
- VERIFIED: `pipeline/build_payload.py:187` puts `"variant":
  "perturbed"|"original"` and `:188` `"perturb_factor_recorded_scoring_side_only":
  None` into the payload; `pipeline/runner.py:123` (and `runner_api.py:41`)
  strip only `_`-prefixed keys → both fields reach the model. The perturbed
  arm self-announces the experiment.
- claim strengthened: memorization-control (perturbation) claim — name-ID
  21.9%, B3 attribution 0.147.
- fix shape: model-visible payload contains only case/series/chronology
  fields; variant + factor live in run-side metadata (underscore-prefixed or
  separate record); regression test asserting no experiment-marker key names
  or values in the rendered user_payload, both arms (INV-04: same fields in
  both arms).
- deps: none. NOTE: changes future fingerprints only; frozen `runs/`
  untouched (disclose-don't-revise). No evaluatee re-run in this loop.

### FB-02 Cutoff: payload-level fail-closed invariant + truthful log names + METHOD wording
- source: B2 · category: CODE-FIX · size: S · status: DONE (2026-08-05, D-P36)
- VERIFIED: bulk loaders filter rather than raise (`cutoff_guard.py:207`,
  `:236`); summary log key `"facts_after_cutoff": len(rows)` at `:212`
  actually records RETAINED (≤ cutoff) rows — name inverted. `load_document`
  (`:250`) does raise. METHOD.md §2 claims blanket "fail-closed".
- claim strengthened: point-in-time (look-ahead-free) claim — the repo's
  core methodological claim.
- fix shape: (i) final invariant — completed payload assembly re-scans all
  dated rows, raises CutoffGuardError on any > cutoff; (ii) rename log keys
  facts_total / facts_retained_pre_cutoff / facts_dropped_post_cutoff;
  (iii) METHOD.md wording: raw-file post-cutoff content allowed, assembly
  filters, completed-payload violation fail-closed. Tests for (i) and (ii).
- deps: none. INV-03 disclosure entry required (plumbing + doc alignment).

### FB-03 Legacy fingerprint auto-trust → fail-closed default
- source: B7 · category: CODE-FIX · size: S · status: DONE (2026-08-05, D-P37)
- VERIFIED: `pipeline/runner.py:113-115` — schema-valid output without
  fingerprint → "skip (legacy output — fingerprint 없음, 재실행 안 함)".
  Prompt/schema/code drift silently preserves stale outputs.
- claim strengthened: reproducibility/provenance claim (published numbers
  trace to fingerprinted outputs).
- fix shape: default = treat as STALE and refuse to silently skip (report,
  do NOT auto-call the model — evaluatee runs stay owner-land);
  `--accept-legacy-output` opt-in retains old behavior; provenance note in
  run report. Tests via existing fixture pattern
  (`test_fingerprint_idempotency.py`).
- deps: none.

### FB-04 FormatChecker on evaluatee-path validators
- source: B6 (validator half) · category: CODE-FIX · size: S · status: DONE (2026-08-05, D-P38)
- VERIFIED: `runner.py:169`, `cli_client.py:215,329` use `Draft7Validator`
  without `format_checker`; `tools/test_build_evaluatee_inputs.py:68` and
  `tools/validate_schemas.py:16` already use `FormatChecker` — evaluatee
  path is the lax one. (Schema `format` annotations to be confirmed at task
  time; add where dates/times are declared.)
- claim strengthened: schema-enforcement claim (INV-02 "출력은 schemas/
  스키마 준수").
- fix shape: add FormatChecker to the three call sites + failing-fixture
  test. NO semantic tightening of the schema itself (that half is
  owner-gated, see DP-Q1).
- deps: none.

## Tier 2 — cheap, high-leverage, executable

### FB-05 verify-* naming: additive targets + honest scope wording
- source: B8 · category: DELIVERY · size: S · status: REBUTTED (2026-08-05 — already satisfied)
- REBUTTAL EVIDENCE (checked at cycle time, before build): the two-tier
  interface B requests already exists as D108: README.md:62 advertises
  `make verify-public   # recomputes every published number from committed
  artifacts` (exactly the requested verify-claims semantics, in plain
  words, on the top surface); README.md:65-67 states the zero-corpus/
  zero-network scope with the clean-HOME sandbox transcript
  (audit/verify_public_sandbox_transcript_20260722.txt); REPRODUCING.md:17-18
  table separates the tiers; pipeline/fixtures/synthetic_corpus +
  test_payload_synthetic.py already give third parties the
  cutoff→payload-path check inside verify-public (B's fixture ask).
  Remaining delta would be a synonym make target with no new capability —
  candidate governance bloat under OWNER_MODEL. Owner may reinstate.
- VERIFIED: Makefile `verify-public` = 6 commands (5 gates + doc-count
  lint). Feedback: name overpromises ("public verify" reads as full
  reproduction).
- claim strengthened: reproduce-from-public claim (honest scoping).
- fix shape: ADDITIVE only — `verify-claims` alias for the current
  recompute set; README/REPRODUCING one-paragraph scope statement
  (recompute-committed-artifacts, not model re-run). verify-public keeps
  all 6 commands verbatim (INV-05). No target removed or weakened.
- deps: none. Makefile is INV-05 surface: diff must be provably additive.

### FB-06 Headline tradeoff figure (BN-19 resolution condition)
- source: A8 residual + BN-19 · category: DELIVERY · size: S · status: DONE (2026-08-05, D-P39, Q-F17)
- A8's "no visualizations" claim REBUTTED at cycle time: README.md:46-54
  already carries fig_dotplot_30firms.png + 3 companion figures (BN-08
  resolved 2026-07-29, D120). Residual genuine gap = BN-19: the headline
  no-dominant-strategy detection/FPR tradeoff exists only as prose + 4x4
  CP95 table.
- fix shape = BN-19's written resolution condition verbatim: committed
  deterministic script regenerating a threshold-sweep figure (detection
  and false-positive rates with CP95, ordinal-convention labels) from
  analysis/decision_table.json; PNG committed; owner adoption queue entry
  for README/DECISION_TABLE placement (placement itself owner-gated).
  Follows the fig_dotplot.py precedent (analysis/ new files only, no
  existing file edited). BOTTLENECKS.md status flip NOT done by this loop
  (guarded file — owner/direction-loop channel).
- deps: none. INV-13 (no fraud vocab on labels), ordinal axis convention.

### FB-07 Statistical power analysis doc (pre-registration groundwork for N expansion)
- source: A1 · category: STATS · size: S · status: DONE (2026-08-05, D-P40)
- claim strengthened: roadmap credibility of the N-expansion claim; makes
  the INV-12 scope-change decision (DP-Q3) evidence-based instead of vibes.
- fix shape: deterministic power analysis (seeded, exact where feasible):
  N required to distinguish AUC 0.83 from 0.5 (and from 0.65) at stated
  power; docs/POWER_ANALYSIS.md + small tools/ script + test. Does NOT
  register any new case (stays inside INV-12).
- deps: none.

## Tier 3 — executable design/stats (after Tiers 1–2)

### FB-08 CLAIMS.json machine-readable claims ledger
- source: B11 (subset) · category: DELIVERY · size: M · status: DONE (2026-08-05, D-P41)
- claim strengthened: every published claim (gives external readers one
  entry point: number → source artifact → limitation → status).
- fix shape: CLAIMS.json + generator/consistency check wired into existing
  lint (additive); no README restructure in this item.
- deps: FB-05 (wording), FB-06 (figure ref) soft.

### FB-09 Monte-Carlo SE / seed disclosure annotations for published stats
- source: B10 (subset executable without touching frozen outputs) ·
  category: STATS · size: M · status: DONE (2026-08-05, D-P42)
- fix shape: new annex doc + code that recomputes MC-SE from committed
  artifacts; no edits to frozen analysis outputs; exact-permutation note
  where N makes it feasible.
- deps: FB-07.

## DECISIONS_PENDING queue (never built by this loop)

- DP-Q1 — schema v2 semantic tightening + probability→risk_score rename
  (B5, B6 schema half; A metric framing). Measurement-condition change to
  the evaluatee contract mid-project; comparability with frozen waves 1–2.
  → ready-to-execute draft schema + migration note; owner signs.
- DP-Q2 — CI hardening: SHA-pinned actions, permissions: contents: read,
  scheduled compat workflow, Ruff/type/coverage/pip-audit (B9). Touches
  `.github/` (INV-24 surface; also INV-11 tension: Ruff/Pyright are new
  dev-deps). → ready-to-execute workflow diff; owner signs.
- DP-Q3 — retrospective N expansion to 50–100 + matched controls (A1).
  Direct INV-12 conflict (>8 experimental cases prohibited). → scope-change
  proposal with power-analysis evidence (FB-07 output); owner signs.
- DP-Q4 — cross-model GPT/Gemini pass over frozen payloads (A3). Direct
  INV-12 conflict ("타 LLM 벤치마크 확장 금지"; specs/cross_grader.md is
  SPECIFICATION ONLY) + INV-20 metered-key question for other vendors.
  → spec-only expansion draft; owner signs.
- DP-Q5 — modern ML baseline (RUSBoost/GBM per Bao et al. 2020) (A4).
  Beyond the INV-12 carve-out (deterministic formula baselines allowed;
  trained models are not covered). → spec draft with seeded-determinism
  plan; owner signs.
- DP-Q6 — forward-cycle universe/base-rate redesign: hundreds-of-firms
  universe or pre-registered intermediate labels (4.02, restatement)
  (A2, B4). Touches sealed forward-cycle protocol (INV-22, Nov 2026
  window). → design memo with base-rate math; owner signs.
- DP-Q7 — k≥5 redraw for waves 1–2 (A5) and any evaluatee re-run after
  FB-01/FB-02 land. Requires model runs — sealed-runner + owner launch
  only (harness is dev tooling; INV-19/21/22).
- DP-Q8 — external human blind re-scoring, κ reporting (B3); GA-001(b)
  human audit completion; DOI/Zenodo (A7); SSRN/arXiv packaging (A8).
  Owner-only actions (recruiting, signing, publishing).
- DP-Q9 — perturbation frame v2 (accession removal + chronology re-timing
  + signal-preservation check) (A6). New measurement condition + re-run.
  → spec draft; owner signs.
- DP-Q10 — README restructure / English canonicalization beyond FB-05/06
  (A8, B11): already partly queued as Q-F11/Q-F13/Q-F14 (OWNER_QUEUE);
  do not duplicate — link there.

## REBUTTED / corrected feedback claims

- B9 "3.11/3.13 failures are allowed" — allowed BUT visibly recorded via
  job-level notice (`ci.yml:15-27`), which B did not mention; the silent-
  green concern is already mitigated (INV-24). SHA-pinning and permissions
  hardening remain valid (→ DP-Q2).
- B2's implication that the guard never raises — `load_document`
  (`cutoff_guard.py:250-271`) does raise on violation/unregistered/
  unresolved; the filter behavior is specific to the two bulk loaders.
  Doc/log mismatch stands (→ FB-02).
- (No other factual errors found; A's numeric quotes match RESULTS.md
  rows 5/11 and README.)

## Follow-up candidates (logged by reviews, not yet items)

- FB-01-FU1 (from cycle-2 pre-review self-critique): `date_shift.py:71`
  still sets non-underscore `out["variant"] = "perturbed_v2_dateshift"`
  while FB-01 renamed the payload key to `_variant` — a shifted payload
  carries both. No leak (3-key send allowlist strips both) and
  date_shift.py is protected; candidate one-line rename for an
  owner-supervised session. Logged so it isn't rediscovered.

# BACKLOG v2 (D-P45 재분류, 2026-08-05) — continuous mode

## Executable (NB series, priority order)

### NB-01 Schema v2: risk_score rename (PKT-Q1, signed D-P44a)
- category: CODE · size: S · status: DONE (2026-08-05, D-P46)
- claim: metric-framing coherence of every future published number
  (probability/ordinal conflict resolved at the contract).
### NB-02 CI hardening, dependency-free half (DP-Q2a)
- category: CODE · size: S · status: DONE (2026-08-05, D-P47)
- claim: reproduce-from-public integrity (supply-chain: SHA-pinned
  actions, permissions: contents: read, doc/code job split). Ruff/type/
  coverage EXCLUDED (INV-11 — amendment draft queued).
### NB-03 INV-12 amendment commit (cite D-P44b) + cross-model GPT runner
- category: CODE+RUN · size: M+L · status: CODE DONE (2026-08-05, D-P48/D-P49); LIVE TRANCHE PARKED (D-P50 phase lock)
- claim: L-6 same-family-leniency limitation gets its empirical test;
  "Claude pipeline result" → "LLM result" reframing (A3: best ROI).
  Runs via subscription codex only; outputs to new separated path;
  publishing owner-gated.
### NB-04 Perturbation v2 signal-preservation validation (DP-Q9, pre-authorized)
- category: CODE · size: M · status: TODO
- claim: memorization-control claim robustness (A6: rescale/digit-pattern
  effects unverified; v2ds frame exists — validate detectors invariant).
### NB-05 delivery-restructure branch: README/docs restructure + 1-page summary
- category: DELIVERY · size: M · status: TODO
- claim: external-reader judgment surface (B11 structure, A8 summary).
  Branch only; merge owner-gated.
### NB-06 Forward redesign memo draft (PKT-Q6 non-protected parts)
- category: DESIGN · size: M · status: TODO · Nov 2026 clock
- claim: forward-cycle validability (base-rate math → design memo;
  protected-doc amendment text prepared for owner signature).
### NB-07 Universe expansion PREP (DP-Q3 subset: matching rules + fixture dry runs)
- category: DESIGN · size: M · status: TODO
- claim: N-expansion readiness (no fetch — INV-23; no case registration —
  INV-12).

## Queued with amendment drafts (invariant wins)
- Ruff/Pyright/coverage/pip-audit (INV-11) · ML baseline (INV-12) ·
  k>=5 redraw (INV-21/BN-03 pin, Nov window D113) · universe expansion
  execution (INV-23 supervised fetch + INV-12).


# BACKLOG v3 (D-P50 phase lock, 2026-08-05) — Reader Surface Completion

## Phase 1 (priority order; items 1/2/4/8 carry the 2-simulated-reader gate)
### P1-01 README reader-surface rewrite (Eng canonical, .ko preserved) — TODO
### P1-02 Published-issue image fix packet (Issues #1-3, absolute raw URLs; owner posts) — TODO
### P1-03 BN-12: fig_dotplot axis label → ordinal convention + figure-drift gate in verify-public — TODO
### P1-04 BN-11/14/18 batch: Eng-canonical DECISION_TABLE / methodology_limitations / ERRATA — TODO
### P1-05 BN-13: wave-2/holdout/E2 recompute wired into verify-public — TODO
### P1-06 BN-16: no-network/no-corpus guard enforcing verify-public RC=0 (sandbox_guard wiring, Q-F16) — TODO
### P1-07 BN-07 remainder: full-clone requirement line in REPRODUCING.md — TODO
### P1-08 Recruiting materials packet (2 resume bullets + LinkedIn draft; owner packet) — TODO

## Phase 2 (only after Phase 1 all DONE/owner-blocked; specs only, zero calls)
### P2-09 specs/OBSERVATORY_PILOT_V0.md (SPECIFICATION ONLY) — TODO
### P2-10 Sealed Analyst task schema v0.1 + deterministic scoring formulas (specs/) — TODO
### P2-11 Clean-case inventory plan N=3 → 15+ (plan only, INV-23) — TODO

## PARKED (post-Phase-1 re-evaluation, D-P50)
- NB-04 perturbation v2 validation · NB-06 forward memo (Nov clock — flag
  at Phase-1 exit) · NB-07 expansion PREP · GPT live tranche (launch
  command in D-P49)
