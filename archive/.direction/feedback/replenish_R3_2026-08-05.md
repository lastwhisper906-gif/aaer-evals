R3 review complete — **5 new findings clear the floor** (no NO_NEW_ITEMS). All five are seam defects between documents that today's per-doc reader gates structurally couldn't catch. File writes aren't permitted in this session (same as the R2 round), so the full report is delivered inline below, ready for the orchestrator to drop into `.direction/feedback/replenish_R3_2026-08-05.md` and append to BACKLOG v4.

---

# R3 REVIEW — external-reader delivery surface (loop v2, D-P45 §2)

Session notes: `git fetch origin` was blocked by the non-interactive sandbox (INV-17). Mitigation: `git status -sb` against the last-known origin ref shows `main...origin/main [ahead 31]` — local HEAD (096da55) is ahead, not behind, consistent with the no-push convention. No commits or file writes were made by this review.

## a. EVIDENCE

Primary artifacts read in full from disk (not builder summaries):

- Reader surfaces: `README.md` (all 189 lines, at HEAD), `RESULTS.md` (all 13 rows), `CLAIMS.json` (all 13 claims), `AUDIT_INDEX.md`, `docs/README_DETAIL.md`, `analysis/DECISION_TABLE.md`, `docs/methodology_limitations.md` (L-1…L-9 + instrument-bias table), `analysis/error_analysis_wave2_holdout.md`, `ERRATA.md` (E-001/E-002), `METHOD.md` and `REPRODUCING.md` (headers + §0–§1), `.github/ISSUE_TEMPLATE/` listing
- Mechanical verification: link-target existence checks (`ls` on every relative link/image target in the surfaces above — all 5 figure PNGs, `fig_tradeoff.py`, `review_packets/INDEX.md` exist; two README_DETAIL link targets do not); `git log`/`git show e05db78` (D-P51 commit: header list + `<details>` count = 0, confirming the defects shipped in the rewrite commit itself); `grep human_finalized` over `scoring/grades_wave2/*.json` (all `true`) and `scoring/decisions_log.md` D21; `grep "0.337\|0.265"` across all canonical surfaces; `grep CLAIMS.json` across all six entry-point docs (0 inbound links); `.protected-paths` in full (fix-routing)
- Exclusion sets read first: `.direction/feedback/BACKLOG.md` in full (FB/NB/P1/P2/R1/R2 series), `DECISIONS_PENDING.md` D-P51–D-P65 in full (incl. D-P51's five dispositioned reader confusions and D-P57's logged romanization/R4 follow-up), `docs/OWNER_QUEUE.md` Q-F10–Q-F17 (DP-Q10/Q-F13 scope), reader-test records listing, `CYCLE_LOG.md` spot-checks

## FINDINGS (BACKLOG format, ranked by claim impact)

### R3-01 README top surface carries visible editing damage from the P1-01 rewrite (duplicate header, empty section, unfolded duplicated content)
- category: DELIVERY (defect repair) · size: S · status: NEW
- **evidence:** `README.md:55-56` — `## What this is` rendered twice, back to back. `README.md:138-140` — `## Want to check our work?` is an empty section (immediately followed by `## Where to go next`). Both shipped in the D-P51 rewrite commit `e05db78` itself (verified via `git show`; header list reproduced). Secondary, same repair: D-P51's record says prior content was preserved "접힘 아래" (under a fold), but the commit contains zero `<details>` elements — so the dot plot (`:22` and `:91`, same PNG) and the clone/verify command block (`:34-38` and `:106-111`, identical commands) each render twice as flat content within one scroll.
- **why it clears the floor:** this is the canonical entry surface; a skeptical reader's first screen-and-a-half shows copy-paste damage, which directly discounts the repo's central meta-claim (process rigor) before any evidence lands. The reader gate (2/2 PASS) saw the first screen only; lint checks vocabulary and counts, not structure — no existing gate can catch this.
- **not a re-raise:** D-P51's dispositioned confusions were content-level (AAER expansion, matching basis, etc.); DP-Q10/NB-05 is an owner-gated *restructure* — this is repair of defects in today's landed commit, within the already-signed D-P50 P1-01 scope. README.md is not in `.protected-paths`.
- **fix shape:** delete the duplicate header line; either give "Want to check our work?" its intended content (merge with "Where to go next") or drop the header; decide fold-vs-dedupe for the doubled figure/commands (a real `<details>` fold would make the D-P51 record's description true — smallest honest fix). INV-03 disclosure entry; `.ko` untouched.

### R3-02 README_DETAIL's only two evidence links both 404 on GitHub (relocation broke relative paths)
- category: DELIVERY (defect repair) · size: S · status: NEW
- **evidence:** `docs/README_DETAIL.md:50` links `analysis/DECISION_TABLE.md` → resolves to `docs/analysis/DECISION_TABLE.md` (does not exist, verified); `:62` links `docs/V1_PARTIAL_DEIDENTIFICATION_NOTE.md` → resolves to `docs/docs/…` (does not exist). These are the doc's *only* markdown links, and they anchor its two highest-stakes assertions: the owner-signed decision table (no-dominant-strategy headline) and the partial-de-identification disclosure. The D110 relocation from repo root broke them; nothing has caught it since.
- **why it clears the floor:** README explicitly routes deep-dive readers here ("Detailed narrative … `docs/README_DETAIL.md`"); the reader who takes that route and clicks through to verify hits two dead links — on the disclosure link, a dead 404 *on the de-identification caveat* reads worst.
- **not a re-raise:** no BACKLOG/BN/queue item mentions README_DETAIL links; DP-Q10 is restructure, not link repair. `docs/README_DETAIL.md` is unprotected.
- **fix shape:** prefix both with `../`. NO link-checker lint machinery with it (see c.).

### R3-03 README_DETAIL silently republishes the pre-errata Spearman values E-002 corrected
- category: DELIVERY (errata propagation) · size: S · status: NEW
- **evidence:** `docs/README_DETAIL.md:188` — "wave-2 0.337/0.265" presented as the live correlation values. `ERRATA.md:78-79` corrected exactly these to 0.333/0.293 (tie-aware rev2); `RESULTS.md:27` row 12 publishes the rev2 values and demotes 0.337/0.265 to "came from an implementation that did not average ties." No E-002 marker at the README_DETAIL site.
- **why it clears the floor:** "did they propagate their own errata?" is a skeptic's cheapest test, and this surface fails it — an English-canonical reader doc contradicts RESULTS and ERRATA on the same numbers. The whole disclose-don't-revise doctrine is undermined by a surface that still carries the superseded value uncorrected.
- **not a re-raise:** E-002 itself is dispositioned; its *propagation to README_DETAIL* appears nowhere. The doc is unprotected (docs/), header already defers to RESULTS as canonical, so an inline correction with an "(rev2, ERRATA E-002)" tag is legal and consistent with the doc's copy status.
- **fix shape:** replace with rev2 values + E-002 pointer at `:188` (or co-report both with the v1 values explicitly tagged superseded, mirroring RESULTS row 12).

### R3-04 The RESULTS row-9 source doc asserts `human_finalized=false` and "E1 not run" — both superseded — with no dated-snapshot marker
- category: DELIVERY (owner-routed: `analysis/` protected) · size: S · status: NEW
- **evidence:** `analysis/error_analysis_wave2_holdout.md:9` and `:219` state grading is `human_finalized=false` / "awaiting human final confirmation"; `:206-211` (§6) states "E1 … not run → placeholder". Ground truth: every `scoring/grades_wave2/*.json` carries `human_finalized: true` (sign-off chain D21/D24/D26, `scoring/decisions_log.md:751`); E1 was executed (D26) and RESULTS rows 6/10 publish its results. This doc is the Source column of RESULTS row 9 and is cited by row 9's limits ("grounded; top of dim4").
- **why it clears the floor:** every claim surface carries the INV-14 scope line "Grading: Claude-assisted, **human-finalized**." The reader who follows row 9 one click down finds the source document saying the opposite, twice, with no way to tell whether finalization ever happened. That is a direct hit on the grading-finalization claim — worse than a broken link because it reads as an inconsistency, not an accident.
- **not a re-raise:** D-P56 promoted the EN translation faithfully (the staleness is inherited from the frozen 2026-07-08 ko snapshot — correct there, unmarked here); its reader gate flagged HUBG self-demotion, not this. Not in any queue/packet.
- **fix shape:** one dated status line above the H1 (the pointer-line position the D-P56 equivalence-helper strip convention already exempts, so the token-equivalence lock with frozen `.ko` survives): "Snapshot as of 2026-07-08. Grades since finalized `human_finalized=true` (D21/D24/D26, `scoring/overrides.md`); E1 since executed (D26 — RESULTS rows 6/10)." `analysis/` is protected → route into the next signed direction or fold into the existing PKT-R2 signature packet (it already touches RESULTS rows 2/11 — same commit class), NOT a new queue entry.

### R3-05 CLAIMS.json — built as the external reader's machine-readable entry point — has zero inbound links from any reader surface
- category: DELIVERY · size: XS · status: NEW (smallest; explicit kill-candidate)
- **evidence:** FB-08 (DONE, D-P41) built `CLAIMS.json` because it "gives external readers one entry point: number → source artifact → limitation → status." `grep CLAIMS.json` over README.md, RESULTS.md, AUDIT_INDEX.md, REPRODUCING.md, METHOD.md, docs/README_DETAIL.md → 0 matches. It is reachable only by browsing the root file listing.
- **why it clears the floor (argued, not assumed):** the FB-08 claim itself — "one entry point for external readers" — is presently false in practice; the artifact exists but no reader path reaches it. Impact is discoverability, not misdirection, so this is the weakest item.
- **fix shape:** one line in README "Where to go next" or the RESULTS header — fold into the R3-01 README repair commit, zero standalone process cost.

## b. VERDICT

`REVISE` — the canonical numbers surfaces (RESULTS, CLAIMS.json, ERRATA, DECISION_TABLE) are internally consistent and read strongly; AUDIT_INDEX's disambiguation section and RESULTS' row-level-limits discipline are genuinely good external-reader work. But the delivery layer fails at the seams: the entry surface shipped visible editing damage today (R3-01), and three cross-document consistency breaks (R3-02/03/04) sit exactly on the paths a skeptical reader uses to check the repo's honesty claims — dead evidence links, an unpropagated erratum, and a source doc contradicting the human-finalized scope line. Four of five fixes are unprotected one-to-three-line edits; one routes through the existing signature channel.

VERDICT[R3]: REVISE

## c. KILL-OR-DEFER

- **Kill any markdown-link-checker or cross-doc-number-consistency lint machinery** as a follow-up to R3-02/03. Two links and one number get fixed by hand in minutes; a new gate is exactly the owner's documented over-instrumentation pattern. Revisit only if the same failure class recurs a third time (the BN-16 mole-whack precedent).
- **Kill R3-05 as a standalone item** — it survives only as one line folded into the R3-01 commit. If that fold is contested, drop it entirely.
- **Shrink R3-04's process cost:** no new OWNER_QUEUE entry — fold the one-line snapshot note into PKT-R2 (already open, same signature class, owner is relocating Aug 18).

## d. STEELMAN

The strongest case against REVISE: no canonical number is wrong anywhere — RESULTS, CLAIMS.json, ERRATA, and DECISION_TABLE all agree, and they are the surfaces the repo *tells* readers are authoritative (README_DETAIL's own header defers to RESULTS; error_analysis is dated in its header). Five simulated-reader gates passed today with zero of these issues surfacing, which is real evidence that real readers aren't blocked by them; and D-P50's direction is complete, so re-opening README a day after its signed rewrite risks churn on a surface the owner just approved. I hold REVISE because the gates were per-document and first-screen-scoped — every finding here lives in the seams *between* documents (link resolution, errata propagation, snapshot-vs-current status), which that gate design structurally cannot catch; and R3-01's damage post-dates nothing — it shipped *in* the approved commit, so fixing it is completing the signed work, not re-opening it. The "readers weren't confused" defense also fails asymmetrically: the readers who matter for this repo's goal are precisely the skeptics who click evidence links and diff numbers across documents.

## e. CLAIM IMPACT

- R3-01 → the entire external judgment surface (D-P45 DELIVERY qualification): first-impression rigor of the canonical entry point; also makes the D-P51 ledger description ("preserved under a fold") true.
- R3-02 → the no-dominant-strategy decision-table claim (D94) and the partial-de-identification disclosure claim — the deep-dive route's only clickable evidence.
- R3-03 → the R2 baseline-independence claim (row 12) and the errata-integrity meta-claim (disclose-don't-revise, E-002).
- R3-04 → the "Claude-assisted, human-finalized" grading claim (INV-14 wording on every surface) and rows 6/9/10 coherence.
- R3-05 → the FB-08 claim ("machine-readable entry point for external readers"). No finding here is governance apparatus; all five move outward-facing delivery.

## f. SELF-CRITIQUE PASS

Re-checked a–e. (1) Coverage gaps to record for future R3 rounds: GitHub Issues #1–3 rendered content not verifiable this session (network blocked; PKT-P102 already owns the known image breakage — excluded, not cleared); README.ko.md content not reviewed (frozen, F-01/F-02); `CITATION.cff` contents, `CONTRIBUTIONS.md`, and the release-tag v1.0.0 page not inspected — a future round should read them. (2) Verified my R3-01 claim against the current working tree, not just the commit — the damage persists at HEAD (README.md:55-56, :138-140). (3) Verified R3-04's fix wouldn't break the translation-equivalence lock — D-P56's pointer-line strip convention covers a pre-H1 line; flagged the protected-path routing rather than assuming loop-buildable. (4) Checked I wasn't re-raising: D-P57's logged romanization/R4 follow-up (adjacent to my surfaces) deliberately not re-raised; DP-Q10/Q-F13/NB-05 restructure scope explicitly distinguished in R3-01. (5) One first-pass claim I softened: I initially read the doubled figure/commands as unambiguous defects; on re-read they are defensible as intentional first-screen leads — so R3-01 anchors on the two unambiguous artifacts (duplicate header, empty section) and treats fold-vs-dedupe as the decision inside the fix. Sections b–e otherwise held on re-read.

---

**For the orchestrator — ready-to-append BACKLOG v4 section:**

```markdown
## R3 round (external-reader delivery, 2026-08-05 — full report: replenish_R3_2026-08-05.md)
### R3-01 README editing damage from P1-01 (dup "What this is" header :55-56, empty "Want to check our work?" :138-140, unfolded doubled figure/commands) — BUILD (unprotected; INV-03 disclosure; completes signed D-P50 P1-01)
### R3-02 README_DETAIL both evidence links 404 (docs/README_DETAIL.md:50,:62 — relative paths broken by D110 relocation) — BUILD (../ prefix; NO linter machinery)
### R3-03 README_DETAIL:188 republishes pre-E-002 Spearman 0.337/0.265 without marker (canonical: 0.333/0.293 rev2) — BUILD (rev2 values + E-002 pointer)
### R3-04 error_analysis EN (RESULTS row-9 source) asserts human_finalized=false ×2 + "E1 not run", both superseded, no snapshot marker — PACKET/signed direction (analysis/ protected; fold into PKT-R2; pre-H1 pointer line preserves ko equivalence lock)
### R3-05 CLAIMS.json has zero inbound reader-surface links (FB-08 "entry point" claim false in practice) — FOLD into R3-01 commit (one line) or kill
```
