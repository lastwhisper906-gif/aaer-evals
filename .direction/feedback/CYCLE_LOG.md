# CYCLE_LOG.md — orchestrator loop (append-only, one entry per cycle)

Loop contract: owner prompt 2026-08-05. STOP condition: `~/tools/harness/STOP`.
Working copy: `~/repos/aaer-evals-work` (TCC mirror deviation — see D-P34 in
DECISIONS_PENDING.md; owner reconciliation command recorded there).

## Entry 0 — PHASE 0 bootstrap (2026-08-05)
- Done: `~/tools/harness/OWNER_MODEL.md` + `REVIEW_SPEC.md` created;
  `run_task.sh` reviewer prompt assembly now snapshots and injects both on
  every reviewer invocation (bash -n clean). ~/tools commit `457b77a`.
- Bootstrap diff: 3 files, +141 lines (run_task.sh: snapshot block after
  prompt snapshots; injection block in review-prompt assembly).
- Environment: macOS TCC denied ~/Documents mid-session (recurring flap;
  5 probes). Adopted mirror-clone workaround adapted to no-push rule:
  full clone of origin/main@37ac75b (== local main, verified in-sync and
  clean at session start) at ~/repos/aaer-evals-work. All repo commits land
  there, local only.
- Backlog depth: n/a (pre-intake). DECISIONS_PENDING count: 37 → 38 (D-P34).
- Resume: re-read this file + BACKLOG.md; loop continues in
  ~/repos/aaer-evals-work; harness at ~/tools/harness/run_task.sh.

## Entry 1 — PHASE 1 feedback intake (2026-08-05)
- Done: EXT_FB_A/B saved verbatim; BACKLOG.md written with per-item
  verification (evidence lines cited inline); D-P34 appended. Repo commit
  `b258e6d` (4 files, +412).
- Verification outcomes: B1/B2/B5/B6/B7 CONFIRMED in code; B9 partially
  REBUTTED (3.11/3.13 failures are visibly recorded via notice, ci.yml:15-27
  — SHA-pinning/permissions gaps stand). A-claims: design/stats items
  routed per priority rule.
- Routing: 9 executable items (FB-01..09); 10 owner-gated/INV-conflict
  queues (DP-Q1..Q10) — NOT built, queued in D-P34 for owner signature.
  INV-12 conflicts (N expansion, cross-model GPT/Gemini, ML baseline)
  explicitly not executed.
- Backlog depth: 9 executable. DECISIONS_PENDING count: 38 (D-P34 covers
  DP-Q1..Q10). 
- Resume: `~/tools/harness/run_task.sh --task ~/repos/aaer-evals-work/.direction/feedback/tasks/TASK_FB01.md --workdir ~/repos/aaer-evals-work`
  after pre-review verdict (scratchpad cycle1/pre_review_out.md).

## Entry 2 — Cycle 1: FB-01 perturbation blindness (2026-08-05) — DONE
- Pre-review: REVISE→amended (found probe_runner.py:62 unfiltered dump and
  date_shift.py:71 post-build variant re-injection; test pinned to rendered
  sent-string; disclosure requirement added). Scratchpad
  cycle1/pre_review_out.md.
- Build: run 1 (TASK_FB01_20260805_023947) STALLED — builder obeyed INV-17,
  `git fetch` fails on `.git/FETCH_HEAD` inside the workspace-write
  sandbox, aborted with no changes → identical-diff stall. Mitigation now
  standard: task PRE-FLIGHT states orchestrator performed the fetch; do not
  fetch in-sandbox. Cycle-1 diff checkpointed as `d8ae885` (honest WIP,
  7 tests failing). Run 2 (TASK_FB01_20260805_024411): APPROVE at cycle 1,
  full REVIEW_SPEC-compliant review with primary-artifact evidence.
- Independent evaluation: full suite 306 passed / 1 skipped; raw cumulative
  diff read (9 files, allowlist at 3 send sites verified);
  `make verify-public` all 5 gates PASS (RC=0); doc counts 297→307 via
  `make docs-refresh` (4 doc blocks).
- Disclosure: docs/methodology_limitations.md L-9 (frozen numbers measured
  with markers visible, bias direction unknown) + DECISIONS_PENDING D-P35.
- Commits: d8ae885 (WIP checkpoint) + this cycle's final commit.
- Reviewer kill/defer honored: no end-to-end capture-test scope growth
  (deferred to FB-03 orbit); no verify-public gate additions.
- Backlog depth: 8 executable (FB-02..09). DECISIONS_PENDING count: 39
  (D-P35). Next: FB-02 (cutoff payload-level invariant + log renames).
- Resume if session dies: work clone ~/repos/aaer-evals-work (local main),
  `~/tools/harness/run_task.sh --task .direction/feedback/tasks/TASK_FB02.md
  --workdir ~/repos/aaer-evals-work` after writing TASK_FB02 per BACKLOG
  FB-02; STOP file = ~/tools/harness/STOP.

## Entry 3 — Cycle 2: FB-02 cutoff payload-level fail-closed (2026-08-05) — DONE
- Pre-review: REVISE→amended. Caught a BLOCKING spec error (chronology scan
  key must be payload-side `filing_date`, not raw-EDGAR `filingDate` —
  build_payload.py:156 rename; as-written contract would push the builder
  to weaken fail-closed). Also: disclosure ownership line, retain §2
  cross-validation sentence, don't hardcode log keys in METHOD prose.
  Logged FB-01-FU1 (date_shift variant naming) as follow-up.
- Build: TASK_FB02_20260805 APPROVE at cycle 1 (no stall — PRE-FLIGHT
  no-fetch note now standard).
- Independent evaluation: full suite 311 passed / 1 skipped (5 new guard
  tests); raw diff read (5 files; assert function contract verified incl.
  missing-key fail-closed and == boundary); repo-wide grep confirms no
  old-log-key consumer remains; verify-public 5 gates PASS (RC=0) after
  docs-refresh (307→312).
- Disclosure: D-P36 (records METHOD §2's former overclaim explicitly).
- Backlog depth: 7 executable (FB-03..09). DECISIONS_PENDING count: 40.
  Next: FB-03 (legacy fingerprint fail-closed default).
- Resume: write TASK_FB03 per BACKLOG; harness command pattern unchanged;
  STOP file = ~/tools/harness/STOP.

## Entry 4 — Cycle 3: FB-03 legacy fingerprint fail-closed (2026-08-05) — DONE
- Pre-review: REVISE→amended. Rejected my drafted auto-re-run default in
  favor of the pre-registered report-STALE-refuse shape (DP-Q7 owner gate,
  no surprise quota burn); fixed gated line range (:113-116 only; parse
  at :109-112 must stay for idempotent skip).
- Build: TASK_FB03_20260805_030750 APPROVE at cycle 2. Cycle-1 auto-REVISE
  exposed a spec defect: pre-existing test_cli_client test asserted the
  old legacy-skip; builder made the minimal forced 4-line adaptation;
  reviewer verified it as assertion-strengthening, disclosed the scope
  deviation explicitly (STEELMAN section), and confirmed other run_case
  callers (e2/e4 runners) stay compatible via keyword-only default.
- Reviewer kill/defer honored: no flag plumbing into e2/e4 experiment
  runners; analysis-side fingerprint gating stays deferred.
- Independent evaluation: runner.py diff matches contract (FAIL before
  build_payload, no write; ACCEPTED path; docstring updated); full suite
  312 passed / 1 skipped; verify-public 5 gates PASS (RC=0); docs 312→313.
- Disclosure: D-P37 (includes the scope-deviation record).
- Backlog depth: 6 executable (FB-04..09). DECISIONS_PENDING count: 41.
  Next: FB-04 (FormatChecker on evaluatee-path validators).
- Resume: write TASK_FB04 per BACKLOG; STOP file = ~/tools/harness/STOP.

## Entry 5 — Cycle 4: FB-04 FormatChecker on evaluatee-path validators (2026-08-05) — DONE
- Pre-review: REVISE→amended (transient CLI failure once, health-probed,
  retried). Found 4th call site (committed-output revalidation test must
  match production strictness); empirically cleared frozen outputs (all
  filing_date strict ISO — no gate flip); corrected boundary to date-only;
  extended fencing parity to runner.py.
- Build: APPROVE at cycle 1. Protected-file hunks verified minimal by me
  directly (2+1 argument additions + 2-line boundary comment).
- Evaluation: suite 313 passed / 1 skipped; verify-public 5 gates PASS
  (RC=0); docs 313→314.
- Disclosure: D-P38 (includes protected-path hunk audit + honest no-op
  note for cli_client:215).
- Tier 1 (correctness bugs undermining published claims) is now COMPLETE:
  FB-01..04 all DONE in 4 cycles, zero gate regressions.
- Backlog depth: 5 executable (FB-05..09). DECISIONS_PENDING count: 42.
  Next: FB-05 (verify-* additive naming + honest scope wording).
- Resume: write TASK_FB05 per BACKLOG; STOP file = ~/tools/harness/STOP.

## Entry 6 — Cycle 5: FB-05 REBUTTED + FB-06 BN-19 tradeoff figure (2026-08-05) — DONE
- FB-05 killed as already-satisfied (D108 two-tier + sandbox transcript +
  synthetic fixtures); rebuttal independently audited and UPHELD by
  pre-review ("a rename is not small; an alias adds a second name for the
  same thing — worse for a skeptical reader").
- A8 "no visualizations" also rebutted (fig_dotplot + 3 companions exist).
- Pre-review caught a dangerous spec ambiguity: exploratory_combo
  (post-hoc, performance-claims-barred) also matches n_treatment==12 —
  spec now pins selection to the layers object and the discriminating
  test fixture proves the post-hoc key is never selected.
- Build: APPROVE at cycle 2 (cycle-1 REVISE: non-discriminating fixture +
  Q-F17 format gaps — both fixed by builder).
- Evaluation: figure visually verified (sweep 40-70, CP95 bars, ordinal
  axis, neutral vocab, both operating points annotated); analysis suite
  71 passed; full suite green; verify-public PASS after docs-refresh
  (314→318).
- Disclosure: D-P39. Owner decision queued: Q-F17 (figure placement).
- Backlog depth: 3 executable (FB-07, FB-08, FB-09). DECISIONS_PENDING
  count: 43. Next: FB-07 (power analysis doc).
- Resume: write TASK_FB07 per BACKLOG; STOP file = ~/tools/harness/STOP.

## Entry 7 — Cycle 6: FB-07 power analysis (2026-08-05) — DONE
- Pre-review: REVISE→amended (E2 layer relabeled exploratory/D94; RP-09
  prior-art cross-reference; merge-protocol docs-refresh note). One
  amendment replace missed the doc-structure phrase — compensated at
  evaluation: orchestrator added the one-sentence hypothetical-design-power
  caveat post-build (disclosed in D-P40).
- Build: inverted mode (Claude builds, Codex reviews) — first inverted run
  of this loop; APPROVE at cycle 1.
- Evaluation: table sanity-checked (N 22-30 suffices vs 0.5; N 64-94
  needed vs 0.65; current designs 0.285-0.320 power vs 0.65 — quantifies
  A1's core complaint); doc has honest limits, no advocacy, INV-14
  phrasing; suite 323 passed / 1 skipped; verify-public PASS (319→324).
- Disclosure: D-P40. DP-Q3 now has its evidence input.
- Backlog depth: 2 executable (FB-08, FB-09). DECISIONS_PENDING count: 44.
  Next: FB-08 (CLAIMS.json machine-readable claims ledger).
- Resume: write TASK_FB08 per BACKLOG; STOP file = ~/tools/harness/STOP.

## Entry 8 — Cycle 7: FB-08 CLAIMS.json ledger (2026-08-05) — DONE
- Pre-review: APPROVE (first non-REVISE) — judged NOT governance bloat:
  verbatim artifact EXT_FB_B §11 named, external-reader entry point,
  sync-objection weak because RESULTS.md changes only via ERRATA/INV-03
  discipline. Kill locked: no generator script; status field do-not-grow.
- Build: APPROVE at cycle 1. Evaluation: shape exact (5 keys, 13 claims),
  verbatim lock verified by live corruption test (1 char → FAIL →
  restore → PASS); full suite 324/1; verify-public PASS (324→325).
- Disclosure: D-P41.
- Backlog depth: 1 executable (FB-09). DECISIONS_PENDING count: 45.
- Resume: write TASK_FB09 per BACKLOG; STOP file = ~/tools/harness/STOP.

## Entry 9 — Cycle 8: FB-09 stats annex (2026-08-05) — DONE
- Pre-review: APPROVE + 2 amendments (source-cited provenance instead of
  "absent" for wave-2 seed; 17v45 feasibility row; estimator-form
  citation) — all verified in the built artifact.
- Build: inverted mode, APPROVE at cycle 1. Evaluation: annex
  artifact-faithful (9 MC p-values, B and estimator source-cited incl.
  the E-001-preserved legacy analyzer path), suite 329/1, verify-public
  PASS (325→330).
- Disclosure: D-P42.
- BACKLOG EXECUTABLE QUEUE NOW EMPTY: FB-01..04, 06..09 DONE (8 built),
  FB-05 REBUTTED. Next: REPLENISH review per loop step 7.
- Resume: replenish review; STOP file = ~/tools/harness/STOP.

## FINAL ENTRY — WAITING ON OWNER (2026-08-05, clean stop by design)
- Replenish review verdict: NO_NEW_ITEMS (independent claude -p review,
  scratchpad replenish/out.md; all 8 built items re-verified in-tree at
  line level; the one plausible residual — v1 rescaling signal-preservation
  annex — killed with evidence: test_build_payload.py:69-79 already proves
  ratio invariance; FB-01-FU1 stays a note).
- Terminal state: executable backlog EMPTY (8 built + 1 rebutted of 9);
  ALL remaining feedback-derived work is owner-gated: DP-Q1..Q10 in
  DECISIONS_PENDING.md (D-P34) + Q-F17 (figure placement). Loop stop
  condition per owner prompt: "NO_NEW_ITEMS and DECISIONS_PENDING is the
  only thing left → stall by design → WAITING ON OWNER, stop cleanly."
- TIME-CRITICAL for owner ranking: DP-Q6 (forward universe/base-rate
  redesign) has the Nov 2026 seal-window clock (replenish review §f).
- Final certification (this session, live): git fetch origin — origin/main
  unchanged at 37ac75b, local main ahead 18, not behind (INV-17 clean);
  make verify-public ALL 5 GATES PASS (RC=0); suite 329 passed/1 skipped
  (330 collected).
- Ledger: 18 local commits (37ac75b..ac29b6d + this one); disclosures
  D-P34..D-P42 (9 entries); limitation L-9; owner queue Q-F17.
- OWNER RECONCILIATION (choose one):
  (a) TCC restored: `git -C ~/Documents/aaer-evals pull ~/repos/aaer-evals-work main`
      then review and push per owner-dispatch convention;
  (b) or review in ~/repos/aaer-evals-work directly and push from there.
- RESUME (if owner adds items or ranks DP-Q queue): re-read this file +
  BACKLOG.md; loop pattern: write TASK per BACKLOG →
  `~/tools/harness/run_task.sh --task .direction/feedback/tasks/TASK_X.md
  --workdir ~/repos/aaer-evals-work` → evaluate → disclose → commit.
  STOP file: ~/tools/harness/STOP. Harness reviewer contract:
  ~/tools/harness/{OWNER_MODEL,REVIEW_SPEC}.md (tools commit 457b77a).

## Entry 10 — OWNER SIGNATURE received + signed-default execution (2026-08-05)
- Owner input (verbatim, recorded in D-P43): "i will sign on all of above.
  approve."
- Applied per anti-rubber-stamp discipline (ORCHESTRATOR_NOTES):
  D-P34..D-P42 + 18 loop commits RATIFIED; Q-F17 default (C) EXECUTED
  (README companion line + DECISION_TABLE.md header figure); BN-19
  RESOLVED (condition met + signature); DP-Q items with embedded
  sub-choices remain packet-gated (Q1 rename-vs-calibrate, Q4
  vehicle/INV-20, Q6 universe-vs-intermediate-labels) — not guessed.
- Gates after execution: verify-public 5/5 PASS (RC=0), 330 collected.
- TCC still denies ~/Documents — reconciliation remains an owner command:
  `git -C ~/Documents/aaer-evals pull ~/repos/aaer-evals-work main`
  (or push from the mirror per owner dispatch).

## Entry 11 — D-P44 sub-choices executed + PUSHED (2026-08-05)
- Owner selected (recorded D-P44): Q1 rename→risk_score v2 · Q4
  Codex/GPT subscription vehicle (Gemini out) · Q6 both (universe
  expansion + intermediate labels) · push dispatched.
- Pushed: 37ac75b..7ed12aa (21 commits) then 15bca1c (packets). CI GREEN
  on both runs (30961024777, 30961103574 — canonical 3.12 pass; 3.13
  notice is the standing non-canonical record).
- Packets drafted and committed: PKT-Q1 (schema v2 rename),
  PKT-Q4 (INV-12 amendment text + codex run protocol — RUNS remain a
  separate owner-launched step), PKT-Q6 (forward redesign, Nov clock).
  Each contains exact commands; next build cycles convert packet→TASK.
- Local main == origin/main. ~/Documents copy still TCC-blocked — owner:
  `git -C ~/Documents/aaer-evals pull` (now just a fast-forward from
  origin) when access recovers.

## Entry 12 — Cycle 9 (loop v2): NB-01 schema v2 rename (2026-08-05) — DONE
- Standing-authorization category cited (D-P45 §3: "Schema v2 — new
  versioned files; v1 untouched").
- Pre-review: REVISE→amended (found the 7th/8th rename sites the spec
  missed: L112 description literal + $ref value strings; check_schema is
  blind to stale $refs — instance test covers).
- Build: APPROVE at cycle 1. Evaluation: v1 byte-untouched (git diff 0),
  8-site rename complete (sole remaining old-name string = intentional
  provenance sentence in v2 header), suite 333/1, validate_schemas PASS,
  verify-public PASS (330→334).
- Disclosure: D-P46 (incl. $comment→description packet deviation).
- NOTE (v2 rules): push is owner-gated again — commits accumulate locally.
- Backlog: NB-02..07 remain (6). Next: NB-02 CI hardening (dep-free half).

## Entry 13 — Cycle 10 (v2): NB-02 CI hardening dep-free half (2026-08-05) — DONE
- Standing-authorization category: D-P45 §3 "CI hardening (SHA pinning,
  permissions)". Direct edit (harness skipped per its own when-NOT-to-use
  doctrine — 3-line diff); disclosed in D-P47.
- permissions: contents: read + full-SHA pins for checkout/setup-python
  (SHAs fetched live from official repos). Job split killed (INV-24
  letter protects the 3.12 all-steps job). PKT-INV11 amendment draft
  queued for the dep-requiring half.
- Backlog: NB-03..07 (5). Next: NB-03 (INV-12 amendment + cross-model
  GPT runner) — the big one.

## Entry 14 — Cycle 12 (D-P50 Phase 1): P1-01 README reader surface (2026-08-05) — DONE
- Rewrite per direction: question→answer→figure→verify command, zero
  specialist identifiers first screen, all content preserved below fold,
  INV-14 clauses relocated intact, .ko untouched (F-01/F-02).
- Number verification: owner-quoted Hertz −30/Monsanto +16 did NOT match
  baseline_table.csv — used artifact values (−23/+30), flagged in D-P51.
- Reader gate: 2/2 PASS (recruiter + analyst personas, first-screen-only,
  restatement test); records committed under
  .direction/feedback/readertests/. Their 5 honest confusions folded in
  as additive clauses post-pass.
- Gates: lint_publication RC=0, verify-public RC=0 (repeatedly).
- Direct-edit (docs work); no harness cycle. Next: P1-02.

## Entry 15 — Cycle 13 (Phase 1): P1-03 BN-12 resolved (2026-08-05) — DONE
- Pre-review REVISE→5 amendments (p=50 annotation, sidecar-only entry
  point, render-in-pytest, factual list fixes, honest flip evidence);
  build APPROVE cycle 1. Figure visually verified. verify-public now 7
  commands (additive). BN-12 flipped with honest 2-gated/3-excluded
  evidence. Backlog: P1-04..08 remain in Phase 1.

## Entry 16 — Cycle 14 (Phase 1): P1-07 pre-existing + BN-07 RESOLVED by measurement (2026-08-05)
- Requested line already present (REPRODUCING.md:59-66, D123 sprint);
  completed the unmeasured third leg of BN-07's condition empirically
  (shallow clone → explicit FATAL, RC=1; full clone → PASS RC=0).
  BN-07 flipped. Zero new prose. Phase 1 remaining: P1-04, P1-05,
  P1-06, P1-08.

## Entry 17 — Cycle 15 (Phase 1): P1-04a BN-11 resolved (2026-08-05) — DONE
- Pre-review caught the pre-existing Q-F11 English draft (promotion, not
  retranslation) + token-scaffold trap + pointer precedent + atlas
  follow-up. Build APPROVE cycle 1. Reader gate 2/2 PASS (both readers
  correctly discounted the post-hoc combined rule — the honesty framing
  survives translation). BN-11 + Q-F11 flipped. Remaining Phase 1:
  P1-04b/c, P1-05, P1-06, P1-08.

## Entry 18 — Cycle 16 (Phase 1): P1-04b(1) limitations adoption (2026-08-05) — DONE
- Translation pre-existed; cycle = adoption mechanics. The equivalence
  lock caught 2 tokenizer artifacts (sentence-final numbers) and enrollment
  surfaced 2 pre-W3 lint violations — fixed in EN canonical only, frozen
  ko deferred with documented reason. Q-F14 RESOLVED; BN-14 half-open
  (error-analysis doc next).

## Entry 19 — Cycle 17 (Phase 1): P1-04b2 error-analysis EN — BN-14 RESOLVED (2026-08-05)
- Second consecutive pre-existing-draft catch by pre-review (now a
  standing spec step: check for drafts first). Build APPROVE cycle 1.
  Reader gate 2/2 with unprompted identification of the honesty
  architecture. Q-F15 + BN-14 flipped. Phase 1 remaining: P1-04c,
  P1-05, P1-06, P1-08.

## Entry 20 — Cycle 18 (Phase 1): P1-04c ERRATA EN — BN-18 RESOLVED, batch complete (2026-08-05)
- One transient CLI kill (health-probed, retried — 2nd of session, same
  pattern). Build APPROVE cycle 1. Frozen-packet byte recipe verified
  reproducing against ko (identical sha). Reader gate 2/2 ("trust more" /
  "no conclusion changed"). BN-18 flipped; P1-04 batch fully DONE
  (BN-07/11/12/14/18 resolved today across the direction's items).
- Phase 1 remaining: P1-05 (BN-13), P1-06 (BN-16), P1-08 (packet).

## Entry 21 — Cycle 19 (Phase 1): P1-05 pre-existing — BN-13 RESOLVED (2026-08-05)
- Pre-review REJECTed the duplicate build (3rd already-done catch) and
  exposed two spec traps (exact-equality on MC estimates; frozen-v1
  import). Existing F-01 test verified live (6/6, 6.97s). BN-13 flipped.
  Phase 1 remaining: P1-06, P1-08.

## Entry 22 — Cycle 20 (Phase 1): P1-06 BN-16 RESOLVED (2026-08-05)
- Q-F16 (A) wired; guarded full-gate RC=0 measured; denial probes verified.
  Three allowlist mole-whacks generalized to /System/Library (SIP-sealed).
  Q-F16 + BN-16 flipped. Phase 1 remaining: P1-08 only.

## Entry 23 — Cycle 21: P1-08 recruiting packet — PHASE 1 COMPLETE (2026-08-05)
- Reader gate PASS-with-edits (both personas would advance it); all edits
  applied incl. the analyst's key catch: lead with what survives masking
  (row 2, p=0.0021) instead of burying it — the honesty ordering the
  README itself now follows. Phase 1: 8/8 items closed, 7 bottlenecks
  resolved today. Entering Phase 2 (specs only, zero model calls).

## Entry 24 — Cycle 22 (Phase 2): P2-09 observatory pilot spec (2026-08-05) — DONE
- Pre-review's degenerate-contrast catch became the spec's §5.1
  feasibility gate — the owner signs either a real contrast or a knowing
  longitudinal reframe. Build APPROVE cycle 1. Suite + verify-public
  green (no test-count change — verified). Governance-diet doc slot 1/1
  used. Next: P2-10.

## Entry 25 — Cycle 23 (Phase 2): P2-10 Sealed Analyst spec (2026-08-05) — DONE
- Harness stalled on MY silent-no-match check amendment (post-mortem in
  D-P62; checker now a tool file; edit scripts now assert matches).
  Artifact itself was complete; missing review run directly — REVISE
  caught a gameable event-horizon rule (evaluatee-chosen resolution dates
  defining ground truth); fixed to pre-registered HORIZON_DAYS=730 before
  any signature (last legal moment under INV-03). Gates green.
- Phase 2 remaining: P2-11 only.

## Entry 26 — Cycle 24: P2-11 pre-existing (4th catch) — D-P50 DIRECTION COMPLETE (2026-08-05)
- POSTCUTOFF_ACCUMULATION.md (D111) already answers the inventory-plan
  ask; one interpolated N=15 row added per the table's own convention.
- Direction totals: Phase 1 8/8 + Phase 2 3/3; 7 BNs resolved, 4 Q-Fs
  closed, 2 specs authored, 2 owner packets, 5/5 reader gates, gates
  green throughout. Loop continues: replenish rotation R1 next
  (no-idle rule, D-P45 §2).

## Entry 27 — Cycle 25: R1-01/02/03 fixes landed (2026-08-05) — DONE
- APPROVE cycle 1. The parked D-P49 launch command is no longer a trap:
  registry covers its outputs, the runner refuses to fire unpinned, and
  resume is truly idempotent (previously certified-wrong by its own
  test). R1-04 stays deferred. Rotation next: R2 statistical validity.

## Entry 28 — Cycle 26: R2 round — 1 built, 2 packeted (2026-08-05)
- All published stats verified error-free against external references.
  R2-03 landed (power-doc mismatch disclosure); R2-01/02 → PKT-R2 owner
  packet (published-surface limits sentences). One transient CLI kill
  (5th, recovered). Rotation next: R3.

## Entry 29 — Cycle 27: R3 round — 4 repaired (incl. own P1-01 damage), 1 packeted (2026-08-05)
- The rotation caught editing damage in this loop's own flagship rewrite
  — recorded plainly, repaired, and the fold description made true.
  Seam-defect class (cross-document) now demonstrated as the per-doc
  gates' blind spot. Rotation next: R4.

## Entry 30 — Cycle 28: R4 test-quality bundle landed, mutation-verified (2026-08-05)
- Send-site blindness lock proven by live mutation test (2 red on
  pre-FB-01 revert). INV-07 proof and INV-01 scan now have discriminating
  tests. 6th transient CLI kill recovered earlier this round. Rotation
  next: R5 third-party reproducibility.

## Entry 31 — Cycle 29: R5 round — 5 repaired (incl. 2nd own-defect), 1 killed (2026-08-05)
- Tier-2's cannot-succeed-as-documented state repaired into honest scope;
  destructive-before-validation ordering fixed; CI parity restored
  (this loop's own P1-03 wiring gap — 2nd self-defect caught by rotation).
  Rotation next: R6 premise challenge (closes rotation 1).

## Entry 32 — Cycle 30: R6 + ROTATION 1 COMPLETE (2026-08-05)
- 7 premises attacked and held (1 by independent recomputation — committed
  as an external-credibility record); 4 published-sentence findings all
  folded into the single PKT-R2 signature packet (9 sentence edits + 3
  frozen-ISSUE notices, one signature applies all).
- Rotation 1 totals: 25 findings — 16 built (gates green throughout, 1
  mutation-verified), 7 packeted, 2 killed, 2 deferred; 2 own-defects
  honestly repaired; 0 errors in published numbers across two independent
  re-verifications.
- Rotation 2 begins per the escalation rule: component-first coverage of
  the R1 reserved list.

## Entry 33 — Cycle 31: rotation-2 C1 — FIRST published-number defects found; correction committed, regeneration packeted (2026-08-05)
- The escalation rule earned its keep on round one: two synthesis-layer
  published-artifact defects (inverted flag across 65 rows; wrong median
  estimator on the only even-n group). Code corrected BEFORE regeneration
  per INV-03(c) with a divergence-lock test; artifact regeneration and
  the E-003 erratum are owner-signature items (PKT-E003) — disclose-
  don't-revise held exactly as designed. 8 more C1 items registered.

## Entry 34 — Cycle 32: C1A bundle landed; forward trio packeted (2026-08-05)
- Five reserved-component fixes green (DNS escape live-probed shut;
  grandchild guard property now tested; doc-count fail-closed; probe
  variant isolation; transcript overwrite refusal). PKT-FWD queued for
  the Nov-window trio. Coverage map grows; rotation 2 continues.

## SAFETY HALT — quota-class long-call throttling (2026-08-05, clean stop)
- Trigger: 4 consecutive long-form claude -p review calls failed (2
  killed mid-run, 2 timed out at 900s with zero output) while short
  health probes answer instantly — the sustained-session long-call
  throttle pattern, treated as the loop's quota safety-halt per its
  standing rules. No half-applied state: the C2 component round had not
  begun; every landed cycle is committed and gate-green.
- Repo state at halt: HEAD dde6411+, all gates verify-public RC=0
  (7 commands + sandboxed variant), suite 376 passed / 1 skipped,
  ledger D-P34..D-P71, 34 prior log entries.
- RESUME INSTRUCTIONS (next session with fresh quota):
  1. Preflight: probe ~/Documents TCC; git -C ~/repos/aaer-evals-work
     fetch origin; check ~/tools/harness/STOP.
  2. Re-run the C2 component round: prompts are saved at scratchpad-
     independent paths? NO — regenerate from this file's C2 description
     (half A: payload_v2_extract, runner_api, api_client suspension
     check, run_identity_arms, e2_generate_cases; half B: memo-pipeline
     callers, e4_runner, e2_runner, regrade_spotcheck, holdout_rescan,
     build_evaluatee_inputs), BACKLOG format, exclusions through D-P71.
  3. Then continue the rotation-2 coverage map (remaining unreviewed
     modules listed in D-P71's 차기 field) and the loop's standing rules
     (v2 continuous mode, D-P45/D-P50, reader gates, packet channel).
  4. Owner signature queue (unchanged, order of value): PKT-E003 →
     PKT-R2 → PKT-FWD → PKT-P102 → PKT-P108 → PKT-Q1/Q4/Q6.
  5. Push remains owner-dispatch; ~/Documents copy needs `git pull`
     post-TCC recovery.
