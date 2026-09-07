# Structure changes

One line per change to how the project is built or governed. Newest last. No
codes, no cross-references, no approval state.

2026-09-06 switched to forward prediction — seal and signature machinery removed, all names in plain language.
2026-09-06 old-design decision — superseded by the new direction.
2026-09-06 the earlier experiment moved to archive/ and frozen at tag archive-v1; its gates were green on Python 3.12 (966 passed) at that commit, and the new CI does not run them.
2026-09-06 the branch review-response/2026-09-04 — the head-to-head between the frozen formula baselines and the model, and the answer to the third external review — is preserved at tag archive-v1-review-response; it is not contained in archive-v1 and was not merged — needs judgment.
2026-09-06 review-response branch diverges from the archived tip; preserved as a tag; merging the two published-results histories needs judgment — not blocking.
2026-09-06 that tag is archive-review-response; the earlier archive-v1-review-response points at the same commit and is left in place rather than deleted, because a line above already names it.
2026-09-06 main requires the CI check and nothing else — no reviewer, auto-merge on, branch deleted on merge; a pull request waiting for a click was itself the bottleneck the rules forbid.
2026-09-06 the pinned interpreter is Python 3.12 and entry points refuse to run on anything else, not only CI.
2026-09-07 the duplicate tag archive-v1-review-response is deleted; archive-review-response is the one that survives, on the same commit — the line above naming the deleted one is history, not a live pointer.
2026-09-07 the directory pages moved to docs/runs.md and docs/rules.md, and the README exception in the append check is gone; everything under runs/ · rules/ · events/ is a record whatever it is called.
