# PKT-P108 — recruiting materials (OWNER PACKET — posting is owner-manual, INV-18)
**STATUS: SIGNED / materials approved (owner blanket, 2026-08-06, D-P83) — posting owner-manual; handle decision: keep lastwhisper906-gif. Q-F18 resolved (A): regrader terms = 25% sampling, ~1hr + 23 packets.**

Every number below cites its RESULTS.md row; nothing here is a publication
surface until the owner posts it. Links assume the public repo README.

## A. Two resume bullets (English)

1. Designed and open-sourced an LLM evaluation testing whether a language
   model can flag accounting-misstatement risk from point-in-time SEC
   filings alone — including identity-masking experiments that quantified
   how much of the signal was memorized company reputation (name-ID 50% →
   21.9%) and showed the separation survives decontamination (masked-frame
   permutation p = 0.0021).
2. Built a verification layer: one command recomputes every published
   number from committed artifacts behind 7 CI-enforced gates, so a fresh
   clone reproduces the full results table with zero accounts and zero
   data downloads — including a sandbox that mechanically proves the
   no-network/no-external-data claim on every run.
   (Row citations for every number: packet section C — repo-side, not
   resume-side, per reader-gate feedback.)

## B. LinkedIn post draft (finding-led, links to README)

I spent the last months building something unusual: an AI evaluation
where the most interesting result is the caveat.

The question: given only the financial disclosures a company had published
up to a cutoff date, can an LLM flag the companies that later became SEC
accounting-enforcement cases?

What I found:
- When I masked company identities, Hertz's risk score fell 78 → 55 while
  Monsanto's rose 28 → 58. Part of the "signal" was the model remembering
  reputations — in both directions. I measured that contamination
  (name-identification 50% → 21.9% across masking frames) and published
  it next to every headline number. [row 4]
- What survives the masking is the point: on the identity-masked frame the
  enforcement/control separation still holds (permutation p = 0.0021,
  wave-1 perturbed) — smaller and honester than the identity-exposed
  headline (AUC 0.83 [0.62, 0.98], p ≈ 0.001), and residual recognition
  (~22%) means even the masked frame is not perfectly clean; that residual
  is itself measured and published. [rows 1, 2, 3, 4]
- And there is no usable standalone alert threshold: the setting that
  catches 12/12 cases also false-alarms on 71.4% of controls; the setting
  that controls false alarms catches 1/12. That tradeoff chart IS the
  finding. [row 13]

Everything — including the errors, the errata, and a corrections ledger in
English — recomputes from the repo with one command, no accounts, no data
downloads: [README link]

If you work on model evaluation, financial ML, or just care about honest
benchmarks, I'd genuinely value skeptical eyes. The fastest way to
criticize it is to clone it.

## C′. Reader-gate record (2026-08-05, 2 personas — PASS with edits, applied)
- Recruiter: would flag for eval/research-engineering roles; edits applied:
  "published"→"open-sourced", self-praise clauses cut, jargon translated,
  row-cites moved repo-side, design-led ordering.
- Analyst: would click through; the "conspicuous omission" (post-masking
  performance) answered with RESULTS row 2 (p=0.0021) + residual-recognition
  honesty; reordered so decontamination leads.

## C. Citation check (packet QA)
- p 0.00114/0.00116 → "p ≈ 0.001" (rows 1, 3 — rounded conservatively,
  both rows cited); masked-frame p 0.0021 (row 2); AUC 0.829 [0.616, 0.983] → "0.83 [0.62, 0.98]"
  (row 3; rounding direction noted: interval endpoints rounded outward-
  safe); 50%→21.9% (row 4); Hertz 78→55 / Monsanto 28→58
  (analysis/baseline_table.csv, T13/T07 — same source as README first
  screen); 12/12, 71.4%, 1/12 (row 13). No number appears without a row.

## D. Owner click path
Resume bullets: paste into resume; adjust voice ("Built/Engineered" → as
preferred). LinkedIn: paste, replace [README link] with the repo URL,
post. Optional: attach analysis/fig_tradeoff.png (already ordinal-labeled).
