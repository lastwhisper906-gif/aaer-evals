# RUN_REPORT.md — D106 follow-up continuous session (2026-07-20 → 2026-07-21)

> Authored by Claude Code, pending human audit (D15). Authority: D106
> (`governance/FEEDBACK_RESPONSE_v1.md`, owner-signed 2026-07-20). Per-artifact
> line log: `RUN_LOG.md`. Zero frozen artifacts modified · zero published
> numbers changed · all accounting-judgment sections `human_finalized=false`.

## 1. Artifact inventory (by stage)

| Stage | Artifacts | Status |
|---|---|---|
| A1/A2 | `atlas/TEMPLATE.md` · `atlas/INDEX.md` | created |
| A3 | 35 entries: `atlas/case_{01,02,03,05,06,07,08,09,10,11,12,13,14,30,33,37,39,40,44,48,49,52,54,59,60,61,65,66,67,69,71,72,73}.md` · `atlas/hc_{03,07}.md` — 20 treatments (9 wave-2 · 8 wave-1 · 3 holdout), 11 FPs, 4 TN-flagged | all drafted; §7–9 pending owner |
| A4 | `atlas/PATTERNS.md` (406 lines, cross-case synthesis) | drafted [human_finalized=false] |
| B1 | `docs/CONTROL_CRITERIA_v3.md` | pre-existed (d096ff6); §4 roster corrected pre-run (1ce4cb8) |
| B2 | `controls/retrospective_audit_v1.md` + `.json` · `docs/methodology_limitations.md` L-8 | created/appended — 62 controls audited |
| C | `README.md` (277 lines, flat) · `README.ko.md` (201, flat) · `tools/lint_publication.py` rule (L) + surface coverage · `docs/reader_validation/ONE_PAGER.md` (2 tier tags) | done, lint PASS |
| D | `CONTRIBUTIONS.md` (+ links in both READMEs) | created |
| E | `surface/BRIEF.md` (268) · `surface/BRIEF_KR.md` (244) | DRAFT-watermarked |
| F | `experiments/CROSS_FAMILY_GRADING_SPEC_v1.md` | created, signature EMPTY |
| — | `RUN_LOG.md` · `RUN_REPORT.md` | this run's log/report |

Commits: `d555610`(A checkpoint) `10cba63`(A) `1ce4cb8`(B pre-run) `9737e55`(B)
`66f35b2`(C) `4c73ffb`(D) `c47a87b`(E) `c394e47`(F) + end-of-run commit.

## 2. OWNER ACTION QUEUE (priority order)

**(a) Atlas §7–9 finalization, case by case.** Estimated review time
(judgment-density based; total ≈ **9.5–11.5 h**):
- Wrong-reason TPs + FNs — **~30 min each** (the CPA-judgment core):
  case_52, case_67, case_03, case_06, case_08, case_12, case_13, case_65,
  case_72, case_73 (10 cases ≈ 5 h). Highest-value: case_65 (tax vs top-2
  unrelated hypotheses), case_67 (input-visibility floor), case_02 (ungraded
  E&O leg — CRITERIA-side question).
- Clean-mechanism TPs — **~15–20 min each**: case_39, case_40, case_59,
  case_60, case_61, case_66, case_01, case_02, case_09, case_71
  (10 ≈ 3 h).
- FPs — **~15 min each**: case_10, case_30, case_33, case_37, case_44,
  case_48, case_49, case_54, case_69, hc_03, hc_07 (11 ≈ 2.75 h). Note the
  audit overlap in (f-2) before finalizing hc_03/hc_07/case_30/case_10/case_11.
- TN-flagged — **~10 min each**: case_05, case_07, case_11, case_14 (4 ≈ 40 min).

**(b) `atlas/PATTERNS.md` finalization** (~45 min) — after (a); its three
load-bearing syntheses (wrong-reason TPs; FPs are over-readings of genuine
figures; missed families share no-XBRL-footprint) each carry [OWNER REVIEW]
items listed at its end.

**(c) `surface/BRIEF.md` + `BRIEF_KR.md` watermark removal** — blocked on
(a)+(b); then owner sign-off + ledger entry before any distribution.

**(d) `CONTRIBUTIONS.md` [OWNER CONFIRM]** — one row: pre-GA-001 commits lack
Co-Authored-By trailers; confirm the "effectively all code AI-drafted" row
(~5 min).

**(e) `experiments/CROSS_FAMILY_GRADING_SPEC_v1.md` signature** — deadline:
**before the next cycle's freeze date**. The next sealed cycle is forward
cycle_001 (seal 2026-11-15; launch gate `forward/cycle_001/OWNER_LAUNCH_GATE.md`)
— if cross-family grading is to apply to it, sign before its freeze/launch
window (early November at the latest). Grader pin gpt-5.4 is owner-replaceable
in the signature line.

**(f) Items needing owner adjudication from this run** (no BLOCKED-NEEDS-DECISION
stops occurred; these are flagged follow-ups):
1. `docs/reader_validation/ONE_PAGER.md` — 2 task-tier tags added to a
   pre-dispatch surface; **re-approve before reader dispatch**.
2. **Retrospective audit FAIL rows (B2)** — 8 rows / 8 companies incl. dup:
   NUVA·R(×2)·UPBD·LQDT·FLO ((f) MTD-survived class actions), GRDX ((e)
   resignation w/ Item 304 disagreement), GO ((d) unremediated MW).
   **Overlap finding**: GRDX, GO, NUVA, LQDT, R are exactly the atlas
   FP/TN-flagged companies — the "false positives" partially coincide with
   cleanliness failures (label-noise direction). Owner call: whether to add
   this observation to PATTERNS.md / a future claim surface (any such
   addition is a new analytical claim → owner-signed).
3. ISSUE_0 draft has 7 untagged results-blocks (all single-cohort; no pooling)
   — optional owner-signed diff to add [TASK 1] tags; not required.

## 3. CI status (full suite, run 2026-07-21 via `.venv` per Makefile)

| Gate | Result |
|---|---|
| pytest | **214 passed** |
| reproduce_analysis | **PASS 100/100** (published numbers ↔ recomputation) |
| verify_blindness | **PASS** (146 model-output files; name/canary scan) |
| verify_manifest | **PASS** (538 files, 585,654,364 bytes) |
| lint_publication (incl. new rule L) | **PASS** — no legacy failures remain (2 ONE_PAGER hits were resolved by tier tags, logged for re-approval in 2(f)1) |
| schemas | all JSON valid |

Environment note: system `python3` (3.14 Homebrew) lacks pytest/requests —
the suite must run via `.venv/bin/python` (Makefile standard). Not a repo
defect; recorded to save the next session the confusion.

## 4. Ambiguities resolved (owner may override)

1. **"FN/TN-flagged cases" (A3 group 5)**: FNs were already covered inside the
   treatment groups (outcome class FN). "TN-flagged" was interpreted as
   wave-1 controls flagged only in the E2 trajectory layer
   (`analysis/decision_table.json` L4 flagged_control): case_05/07/11/14
   (+case_10, covered in the FP group). If a different set was intended, the
   4 entries are additive — nothing was skipped.
2. **C2 scope on frozen memos**: owner-signed publication texts (ISSUE drafts,
   GIL memo) were audited report-only, not edited (RP-15/16 rule). Finding: no
   cross-task pooled claims exist in them. ONE_PAGER was treated as a living
   pre-dispatch surface and minimally tagged (→ 2(f)1).
3. **CONTROL_CRITERIA_v3 §4 roster**: the committed first edition mislabeled
   the RP-09 V-set as "wave-2" and omitted the real wave-2 W-set (23). Fixed
   as a mechanical coverage repair, committed BEFORE audit execution
   (freeze-commit-then-run), with the correction recorded in the doc.
4. **Audit window operationalization**: W start = paired treatment's
   manipulation_period_start (fallback cutoff−36 mo), W end = cutoff+24 mo —
   fixed pre-run in v3 §4.
5. **SCAC source**: the pre-registered `filings.html?ticker=` form is
   login-gated; the public fullsearch equivalent was used and documented
   per-query in the audit JSON (v3 §1(f) permits INCOMPLETE/alternate-source
   documentation).
6. **Cross-family grader naming**: F1 required a named pin now, diverging from
   `specs/cross_grader.md` §3's execution-time selection; recorded in the spec
   with an owner-replaceable pin at signature.
7. **Stage-A commit cadence**: two intra-stage checkpoint commits were added
   (message format "D106 follow-up: stage A checkpoint …") to protect ~4,600
   lines of drafted work; stage-end commits follow the prescribed format.
8. **Lint rule (L) exemption**: the literal phrase "task separation"/"태스크
   분리" is excluded from results-language detection (it contains
   "separation" but is governance prose). Rule strength otherwise unchanged.

*본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).
채점: Claude 보조 + 인간 최종 확정.*
