# VALIDATION_CRITERIA v1 — Stage 1 (--review-only 3)
Registered: 2026-07-29 (before any review-only run — git timestamp is the
proof). Owner-fixed: V2=0, V4≥50%. V3/V5/V6 definitions chosen by the
delegated session (DECISIONS_PENDING.md D-P5), also frozen at registration.

PASS requires ALL of (V1 excepted — see its line):

V1  Novelty: OWNER-GRADED POST-HOC, explicitly ungraded at Stage 1
    sign-off time (owner directive 2026-07-29). The owner grades novelty
    against their own expected-findings list after the fact; the
    automated sign-off records this as pending. V1 does not gate the
    machine sign-off but DOES gate the owner's first merge decision.
V2  Grounding: ZERO unverifiable anchors — measured MECHANICALLY: the
    harness prints "unverifiable anchors: N" per review (H19, with the
    D-anchor ledger adaptation D-P2). N must be 0 for all three reviews.
V3  Discipline: ZERO items in either channel whose subject is style,
    naming, formatting, abstraction depth, or architectural taste.
    Decision rule: an item is a V3 violation if its `what`/`observation`
    contains no INV/BN/D-anchor-relevant factual claim beyond preference
    (assessed per item, with the item quoted in the verdict).
V4  Stability: pairwise anchor overlap (printed by the harness) ≥ 50%
    for each consecutive pair (review-1↔2, review-2↔3).
V5  Channel honesty: among the 3 largest executable findings (by files:
    list length, ties by diff surface named in `action`), none is a
    strategic-scale issue disguised as a small executable proxy.
    Decision rule: a finding fails V5 if its `done_when` checks a
    file-state/command condition that would NOT resolve the problem
    named in its `why` (verdict must quote both fields).
V6  Baseline: baseline.md is ≤150 lines AND names (a) module
    responsibilities for pipeline/, scoring/, analysis/, tools/,
    forward/, (b) at least 5 INV-xx enforcement points with code paths,
    (c) at least 3 BN-xx blocked sites. Checked by reading baseline.md
    only — if a named path does not exist on disk, V6 fails.

FAIL on any machine-gradable criterion (V2–V6) ⇒ stop: the three
judgment documents are the deliverable; do not run default mode. The
reviewer prompt may be revised at most TWICE; if V2–V6 do not pass
within two revisions, the conclusion is that this design is not viable
for this repo — record it and stop. These thresholds are frozen as of
this commit; a wrong threshold is an erratum for the next validation
round (v2, registered before running), never a live edit.
