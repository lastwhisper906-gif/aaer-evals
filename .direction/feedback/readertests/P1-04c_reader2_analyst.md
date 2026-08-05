**(a) Purpose.** This is an append-only corrections register for already-published analysis artifacts: it discloses where the published wave-2 fraud-signal analysis diverged from its preregistered plan, and publishes a corrected rerun (rev2) alongside — never overwriting — the frozen v1 outputs.

**(b) The two corrections.**
- **E-001:** The v1 wave-2 code diverged from the preregistered plan at three points — the R2 decision used absolute correlation alone instead of signed correlation *plus* a residual incremental test, several preregistered statistics (Fisher exact, Clopper–Pearson interval, worst-case sensitivity) were never computed, and the "verbatim rules / reproducible with one command" claims were inaccurate.
- **E-002:** The corrected rev2 rerun was executed and compared against v1 — it fixed a tie-averaging bug in the Spearman implementation, generated the omitted preregistered statistics, and confirmed the cited CP interval [7.5%, 43.7%] in code for the first time.

**(c) Did any published conclusion change?** No. The headline decision is unchanged (trigger rule R4 in both v1 and rev2), all primary statistics match exactly, and the only figures that moved were two Spearman correlations (0.337→0.333 and 0.265→0.293 — one down, one up), both nowhere near the 0.7 threshold that would flip the R2 decision. One caveat: the CP interval's *value* was always correct, but the claim that it was reproducible from the published command was false at v1 — that's a process defect, not a numbers change.

**Honest confusions (as a 90-second outside reader):**

1. **The romanized Korean is jarring.** "*igo* (and)" and "*gyojeong·byeonghaeng gesi*" appear mid-sentence with no explanation of why a conjunction needs romanizing; a reader unaware this is a translation of a Korean original will stumble. The `<!-- sanctioned romanization -->` HTML comments leak into rendered confusion too — they read like internal lint annotations, not disclosure text.
2. **I don't know what R4 means.** "Trigger rule R4 = R4" tells me the decision didn't change, but the document never says what R4 concludes substantively — was the signal confirmed, rejected, escalated? I can't assess materiality without it.
3. **Unexplained figures.** "flags 7/9 vs 5/23," the n=20 vs n=17 mismatch between the two correlations, and the "primary (1st)/secondary (2nd)" double-numbering are all opaque without the underlying plan document.
4. **The CP-interval story takes a re-read.** "The value was accurate but the reproducibility claim was inaccurate" is a subtle distinction; on first pass it reads as if the published interval was wrong.
