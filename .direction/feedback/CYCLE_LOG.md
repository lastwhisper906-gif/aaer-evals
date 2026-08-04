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
