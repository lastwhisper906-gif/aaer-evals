# PKT-P102 — published-issue image fix (owner-manual posting)

## Finding
- Issue #1 (Issue 0 wave-1 memo): TWO image references use bare relative
  paths (`fig_dotplot_30firms.png` body line ~64,
  `fig_memorization_decomposition.png` ~line 92) — GitHub issues do not
  resolve relative paths, so both figures render broken for every reader.
- Issues #2 and #3: NO image references — no change needed (verified via
  gh api, 2026-08-05).

## Fidelity proof (mechanical, recorded in lieu of prose reader-gate —
no new reader-facing prose is authored by this packet)
- Replacement body = posted body with EXACTLY the two image lines changed
  to absolute raw URLs (unified diff = 4 lines: 2 pairs). Both targets
  verified to exist on origin/main via API (99,667 and 95,616 bytes).
- Frozen sources (analysis/ISSUE_0_DRAFT.md) untouched — the posted issue
  is the publication surface; this is a rendering repair, not a number
  change (disclose-don't-revise unaffected; GitHub keeps public edit
  history on the issue).

## Owner click path (manual, ~1 minute)
1. Open https://github.com/lastwhisper906-gif/aaer-evals/issues/1
2. "..." menu on the opening comment → Edit
3. Replace the ENTIRE body with the contents of
   `.direction/feedback/packets/PKT-P102_issue1_fixed_body.md`
4. "Update comment". Verify both figures render.

## BN-04 bundle note
This packet joins the BN-04 owner-manual publication bundle (Tier-3 value
verification). No posting is performed by the loop (INV-18).

Diff (the only 4 lines):
-![All 30 firms](fig_dotplot_30firms.png)
+![All 30 firms](https://raw.githubusercontent.com/lastwhisper906-gif/aaer-evals/main/analysis/fig_dotplot_30firms.png)
-![Memorization decomposition](fig_memorization_decomposition.png)
+![Memorization decomposition](https://raw.githubusercontent.com/lastwhisper906-gif/aaer-evals/main/analysis/fig_memorization_decomposition.png)
