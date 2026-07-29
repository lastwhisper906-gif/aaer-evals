# AUDIT_INDEX.md — Audit identifier guide + ledger map + a real worked trace

> Authored by Claude Code, pending human audit (GA-001 (b)). For external
> readers: what this repository's decision, review, and freeze identifiers
> are and where each one lives, plus one actually resolved decision followed
> end to end.
> Korean original: [AUDIT_INDEX.ko.md](AUDIT_INDEX.ko.md).

## 1. Identifier system

| Prefix | Meaning | Ledger (where it lives) |
|---|---|---|
| **D-NNN** | Decision ledger entry — the unit record of every execution, signature, and scope change. One JSON line + a learning note | `scoring/decisions_log.md` |
| **Q-XNN** | Owner judgment queue item (E=experiment, F=finding, M=misc, O=signature gate, R=review-originated) — options/rationale/default format; sessions never self-resolve | `docs/OWNER_QUEUE.md` |
| **RP-NN** | Review Packet — a self-contained document for asynchronous owner review (diff, publication text, and reading included) | `review_packets/` (entry point `INDEX.md`) |
| **FREEZE_REV N** | Freeze revision — an explicit revision of a pre-frozen protocol or pin (valid only if the revision commit precedes the re-run) | `docs/FREEZE_REV*.md` |
| **GA-NNN** | Governance Amendment original text | `scoring/overrides.md` |
| **E-NNN** | Errata — the public record of defects found after publication | `ERRATA.md` |
| **L-N / J-NN** | Methodology limitation / analysis discretion judgment record | `docs/methodology_limitations.md` · RP-05 §9 |
| **R1–R4 / H1–H3** | Pre-committed conclusion trigger rules (wave / holdout) | `analysis/*_PLAN.md` (freeze-commit-then-run) |
| **E1–E5** | Experiment codes (metered batches): E1 holdout matched controls · E2 earliness trajectories · E3 wave-2 perturbed redraw · E4 cross-model (exploratory) · E5 wave-2 main-score redraw stability band | E1 `analysis/HOLDOUT_CONTROLS_PLAN.md` · E2 `analysis/EARLINESS_PLAN.md` · E3 `analysis/W2_PERTURB_REDRAW_PLAN.md` · E4 (exploratory) `analysis/CROSSMODEL_PLAN.md` · E5 `analysis/W2_MAINSCORE_REDRAW_PLAN.md` |
| **L1–L4** | Evidence-layer codes in the decision table: L1/L2 = TASK 1 · L3 = TASK 2 · L4 = exploratory E2 trajectory layer. Cells are per-layer, never summed across layers | `analysis/DECISION_TABLE.md` |
| **CP95** | Clopper–Pearson exact 95% confidence interval — the interval convention attached to every published proportion | `RESULTS.md` (per-row limits) · `analysis/DECISION_TABLE.md` |
| **B1–B4** | Deterministic baseline codes: B1 = Beneish M-score · B2 = Dechow F-score · B3 = pre-registered chronology meta-signal · B4 = abnormal short interest | `analysis/baseline_table.csv` · `specs/B3_metasignal.md` · `specs/B4_short_interest.md` |

Disambiguation: **E-NNN** (three digits, hyphenated — errata, e.g. E-001) is
a different identifier family from experiment codes **E1–E5** (single digit,
no hyphen). E-001 is a post-publication defect record; E1 is a metered
experiment batch.

Reading order (governance map): `PROJECT.md` → `scoring/decisions_log.md` →
`scoring/overrides.md` → `review_packets/INDEX.md` → frozen texts of the
published issues, `analysis/ISSUE_*_DRAFT.md`.

## 2. A real example — how the B3 threshold-asymmetry finding traveled to publication approval

The full path from the discovery of the B3 attribution-ratio asymmetry
between wave-1 and wave-2 (0.8947 vs 0.1468) to its approval as a public
memo. Each step is a live use of the identifier system above.

1. **Finding registration — D53** (`scoring/decisions_log.md`, 2026-07-13):
   registered the metric-prevalence decomposition of the asymmetry as
   `analysis/EXPLORATORY_wave1_b3_asymmetry.md`. Discipline:
   EXPLORATORY/not-for-publication banner, all four hypotheses phrased as
   questions (zero causal indicatives), zero edits to frozen files and zero
   recomputation. — *This is where the boundary is enforced: an exploratory
   finding may go no further than arithmetic rearrangement of tables, and
   narrative belongs to the owner.*
2. **Publication packet — RP-18**
   (`review_packets/RP-18_asymmetry_memo_publication.md`, D64): a
   publication-ready complete English text, two placement options
   (standalone Issue vs appendix comment on Issue #2), the publication
   command, and hypothesis-labeling review notes in a single document — a
   form the owner can decide with one line.
3. **Owner signature — D92** (2026-07-16): approved as placement (A), an
   appendix comment on Issue #2. Recorded rationale: "floating N=8/9
   arithmetic as a standalone Issue would be overpackaging" — the ledger
   keeps the judgment that, for the same text, the form of publication
   decides the status of the claim.
4. **Publication text freeze** — `review_packets/RP-18_body.md` (extracted
   from packet §2 with zero edits). Publication remains queued as an owner
   manual-execution item (`docs/OWNER_QUEUE.md` leverage summary 1-②) —
   after posting, the URL is to be recorded as a follow-up D-entry.

The invariant this chain shows: **finding → quarantined registration →
review packet → human signature → frozen text → (manual) publication** —
no step stands without the commit timestamp of the step before it, and a
session (AI) can never skip step 3.

## 3. Frequently looked up

- Source of a specific published number: the Source column of the
  `RESULTS.md` table → the corresponding JSON.
- Proof that grading criteria were committed before scores:
  `tools/verify_blindness.py` (history-proof gate — runs in CI on every
  push).
- Override and signature records: `scoring/overrides.md`.
- Post-publication defects: `ERRATA.md` (E-001, three rev2 mismatches;
  E-002, rev2 comparison).
