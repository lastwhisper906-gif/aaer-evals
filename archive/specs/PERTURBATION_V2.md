# PERTURBATION_V2 — symmetric perturbation design

> **SPECIFICATION ONLY — zero model calls.** This document specifies a future,
> owner-activated experiment. It creates no call path, authorizes no run, and
> changes no frozen or published artifact. It implements the owner-signed
> direction for DP-Q9 / **PKT-Q9** in the D-P44/D-P50 lineage and is the P4a
> document named by D-P73 Phase 4.

*본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).*
*채점: Claude 보조 + 인간 최종 확정.*
*포지션 없음. 교육·정보 목적이며 투자 조언이 아니다.*

## 1. Symmetric 2×2 design

Each activated wave uses the same cases, prompt, schema, harness pin, draw
count, and scoring protocol in all four cells:

| case group | original payload | perturbed payload |
|---|---|---|
| treatment | contemporaneous original draw | paired perturbed draw |
| control | contemporaneous original draw | paired perturbed draw |

An owner-activated v2 wave closes finding **R2-01 / PKT-R2** and the limit
stated in `analysis/DECISION_TABLE.md` §1: the frozen wave-1 table compared
perturbed treatment with original control because no perturbed-control grading
existed. The earlier J14 contract in `analysis/ANALYSIS_PLAN_WAVE2.md` §1
deliberately kept the sensitivity frame asymmetric to avoid new
perturbed-frame grading of controls and to avoid treating quota exhaustion as
a goal. That rationale remains valid for the frozen v1 results. It is
superseded only for owner-activated future waves
by this prospective contract: all four cells are collected together or the
wave is not interpreted as a v2 2×2 experiment. Frozen draws are context, not
substitutes for a missing cell.

The primary contrast is the within-case original-minus-perturbed change. The
group interaction is the difference between the treatment and control means of
those paired changes. Neither contrast changes a frozen threshold, label, or
published result.

## 2. Deterministic paired estimators

For case `i`, let `O_i` be its original score and `P_i` its perturbed score from
the same activated arm and draw index. Define `d_i = O_i - P_i`. Pairing is by
`(wave_id, arm_id, case_id, draw_index)`; a missing member makes that pair
INCOMPLETE and excludes it from paired summaries with the excluded count
reported. No imputation is allowed.

For each case group separately, with `n` complete pairs:

- paired mean: `mean_d = sum(d_i) / n`;
- paired sample standard deviation: `sd_d = sqrt(sum((d_i-mean_d)^2)/(n-1))`
  when `n >= 2`, otherwise `null`;
- original and perturbed means: `mean_O = sum(O_i)/n` and
  `mean_P = sum(P_i)/n`, with the identity `mean_d = mean_O - mean_P` checked;
- original−perturbed distribution: the complete ordered vector of records
  sorted lexicographically by `(case_id, draw_index)`, plus its deterministic
  empirical CDF `F(x) = count(d_i <= x)/n` at every distinct observed `x`.

The interaction estimator is
`mean_d_treatment - mean_d_control`. Its descriptive spread is reported as the
two group-specific `sd_d` values; this specification registers no new
significance threshold. All arithmetic uses Python decimal/integer inputs from
validated records, with no wall-clock branch and no unseeded randomness.

## 3. Two separate perturbation arms

The arms are separate experiments and are never pooled.

1. **Identity-removal arm.** Replace issuer name, ticker, CIK, and every real
   accession with stable synthetic identifiers; apply the relative date shift
   in §4; rescale values while preserving fiscal-period alignment. This arm
   tests the combined removal of explicit identity and absolute chronology.
2. **Chronology-preserving arm.** Replace the same identity fields and real
   accessions with stable synthetic identifiers and apply the same permitted
   value transformation, but retain all original dates and filing intervals.
   This arm isolates what remains when chronology is intentionally visible.

The separation is required because date shift interacts directly with **CL7**,
the checklist item asking about filing chronology (late/NT filings,
amendments, and unusual 8-K frequency; `scoring/eval_spec.md` §CL7). A uniform
shift preserves order and intervals but changes absolute calendar placement;
the chronology-preserving arm leaves both intact. Combining these arms would
confound identity removal with the CL7 input treatment.

The precedent is the v2ds implementation in `pipeline/date_shift.py` and its
owner-gated Q-F05 run: one deterministic offset is applied after the real-date
cutoff guard, and accession values are neutralized. That precedent defines
mechanics, not permission to execute this specification.

## 4. Perturbation mechanics and signal-preservation validation

- **Stable accession pseudonymization, not deletion.** Every distinct real
  accession maps bijectively within a case to a stable fake ID such as
  `acc-001`, ordered by `(filing_date, original_accession)` before the originals
  are discarded. Repeated citations retain the same fake ID. No fake ID may
  encode CIK, year, form, or arm.
- **Relative date shift.** In the identity-removal arm, add one deterministic
  case-level offset to cutoff, fact-period, and filing dates after
  `cutoff_guard` has approved the original data. Preserve all pairwise date
  differences, ordering, duration, and weekday. The chronology-preserving arm
  applies an offset of exactly `0 days` by definition.
- **Fiscal-period stability.** A value rescale uses one deterministic case-level
  factor for compatible monetary series. It may not relabel annual/quarterly
  periods, move a fact between fiscal periods, change duration, or break
  balance-sheet and cash-flow alignment. Period keys and fact-to-period joins
  must be identical before and after transformation.

Before any model call, deterministic validators must pass on every case:

- identity leak scan: no original issuer token, ticker, CIK, accession, or (in
  the identity-removal arm) original ISO date survives;
- structural invariance: row counts, tags, units, missingness, fiscal-period
  keys, ordering relations, and all date differences match the arm contract;
- detector invariance: recompute Beneish M-Score and Dechow F-Score from the
  perturbed values using the existing deterministic formulas. Each computable
  component and final score must equal its pre-perturbation value under the
  repository's existing numeric tolerance; computability status must also be
  unchanged. Any mismatch is fail-closed and no call occurs.

This validation establishes preservation of the registered deterministic
signals; it does not establish that every semantic or recognition channel is
removed.

## 5. Owner-activated execution preconditions

No item below is self-resolving. A dated owner signature activating a named
wave is required after selecting the open options.

- [ ] **Scope and probes.** Re-run the frozen name-ID probe with its frozen
  wording and frozen `name_match` rule on both v2 arms; also re-run the frozen
  verbatim-recall probe where its exact frozen prompt exists. Do not substitute
  old probe draws for contemporaneous cells.
- [ ] **Roster option — unresolved.** Option A: wave-1 roster only (repository
  source: `8 treatment + 22 control = 30 cases`). Option B: wave-2 roster only
  (`9 treatment + 23 control = 32 cases`). Option C: both rosters (`30 + 32 =
  62 cases`). Rationale: C best exposes cross-wave stability but costs most.
  **Default: C, pending owner signature.** Sources:
  `analysis/DECISION_TABLE.md` §§1–2 and `specs/perturb_v2.md` §5.
- [ ] **Draw-count option — unresolved.** Option A: one paired draw per cell.
  Option B: a precommitted repeated-draw count chosen before outputs are seen.
  Rationale: B estimates draw variability but its count and budget require an
  owner decision. **Default: A, pending owner signature.**
- [ ] **Cost arithmetic.** Under default roster C and one draw, the 2×2 scoring
  design is `62 cases × 2 frames × 2 arms = 248 evaluatee calls (ESTIMATE)`.
  The required name-ID probes add `62 × 2 arms = 124 evaluatee calls
  (ESTIMATE)`, for `372 evaluatee calls total before any verbatim-probe calls
  (ESTIMATE)`. One grading-assist pass for every scoring-design output adds
  `248 grader calls (ESTIMATE)`, so the subtotal is `620 model calls
  (ESTIMATE)`. Verbatim-probe cost is `eligible cases × 2 arms (ESTIMATE)` and
  must be filled from the signed frozen-probe roster before activation. Any
  retry allowance is **TBD ESTIMATE** and excluded from that subtotal. Dollar
  cost is **TBD ESTIMATE** until the pinned subscription-equivalent accounting
  rule is signed; no API-key or metered path is authorized.
- [ ] **Pin and safety gates.** `enforce_harness_pin` must verify the INV-21 CLI
  and serving-model pins immediately before every call and fail closed on any
  mismatch. INV-20 subscription authentication, payload blindness, schema
  validation, and all five public gates must pass before launch.
- [ ] **Separated outputs and P1a manifests.** Write only to new directories:
  `runs/perturbation_v2/<wave_id>/identity_removal/{original,perturbed}/` and
  `runs/perturbation_v2/<wave_id>/chronology_preserving/{original,perturbed}/`.
  Each leaf has its own P1a `MANIFEST.json` with case IDs, hashes, protocol and
  model fingerprints; the global runs manifest is updated through the existing
  manifest tooling. No frozen v1 directory is read as an output destination.
- [ ] **Publication gate.** Human-final grading is complete for every included
  record, exclusions are enumerated, and the owner separately signs any public
  use. Activation alone does not authorize publication.

## 6. What v2 does not fix

The frozen v1 frame remains only **partially de-identified**, exactly as stated
in `docs/V1_PARTIAL_DEIDENTIFICATION_NOTE.md`: it retained real accessions and
exact chronology, and no v1 result is recomputed or relabeled here. V2 closes
those explicit metadata paths prospectively; it does not repair the frozen
measurement.

V2 also does not eliminate deep recognition channels. Ratios, trends,
accounting structure, unusual transaction sequences, and prose-independent
financial shapes may still identify a familiar case. This is the residual
channel documented in `docs/methodology_limitations.md` **L-5**. Nor does v2
retroactively remove the visible experiment markers that affected frozen
wave-1/2 and probe measurements; that separate unknown-direction limitation is
documented in **L-9**. Payload blindness must be revalidated for future runs,
but doing so cannot correct the old draws.

Accordingly, an original−perturbed delta is a contrast under the stated
transformations, not a clean estimate of all memorization, and a failed
recognition probe is not proof of anonymity.

<!-- Manual G2 / INV-13 vocabulary pass: PASS (2026-08-05); specs/ is not scanned by lint_publication.py. -->
