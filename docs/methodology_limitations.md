# Methodology limitations (§5-5 scope honesty — the list of limits to cite in publications)

> **Korean original: [methodology_limitations.ko.md](methodology_limitations.ko.md)** — this file is the English canonical surface.

> This document is a guard against result-embellishment: whenever backtest
> results are published or cited, the limitations below are stated alongside
> them. These results are **confined to a single Claude-based pipeline** and
> are not generalized to LLMs at large (PROJECT.md §5-5).

## L-1. Training-data memorization limit — recorded 2026-07-05

**Limit**: widely reported cases — in particular the China reverse-merger
(China RTO) cluster **T01 RINO / T03 CCME / T05 KEYP / T06 PUDA / T09 FEED /
T30 LK (Luckin)** and large events (T18 VRX, T25 GE, T28 KHC, etc.) — are
highly likely to be included in the evaluatee model's training data. A
'detection success' on these cases may therefore be **replay of memorized
outcomes**, not document-analysis ability.

- What `pipeline/cutoff_guard.py` controls is the **date of input documents**,
  not the model's internal knowledge — the cutoff guard cannot, in principle,
  close this channel.
- Neutral IDs (case_NN, OV-001) do not close this channel either:
  company_name·CIK·ticker identify the company, and identifying the company
  is precisely the key to event recall. The purpose of the anonymization is
  to hide group membership, not to hide the company.

**Partial mitigation (existing mechanism)**: `schemas/llm_output.json` v1.1
forces `documents_used` as required + minItems 1 — every verdict must state
the documents it used.

**Grading-protocol note (pre-fixed, part of the grading criteria — user
conditional endorsement 2026-07-05: "the flag criterion shall be mechanically
fixed in advance")**: the flag criterion is not discretionary ("a famous
case") but fixed as a **2-stage mechanical rule** — closing the room for
post-hoc manipulation:
1. **Roster condition (pre-fixed)**: the case belongs to the roster below.
   China RTO cluster of 6 cases = **T01 RINO / T03 CCME / T05 KEYP / T06
   PUDA / T09 FEED / T30 LK** (additions to or deletions from this roster are
   subject to the §5-6 history-disclosure condition).
2. **Mechanical citation-deficit condition**: the verdict output for the case
   either (a) merely lists whitelist documents in documents_used while the
   verdict rationale text points to none of those documents' concrete
   contents (figures, line items, paragraphs), or (b) has a rationale that
   mentions facts disclosed only after the cutoff (the exposure sequence,
   disposition outcomes).
`memorization_suspect` = condition 1 AND condition 2. For flagged cases,
precision/recall aggregates are **reported in two versions, flags included
and flags excluded**. Case-by-case application of condition 2 is subject to
§7 (Claude 1st pass + rationale + human signature). If condition 2 is
observed on a case outside the roster, it is recorded in the case notes only,
without a flag (no post-hoc roster expansion — possible only via history
disclosure).

**Learning note (§10)**: look-ahead has three channels — document dates
(blocked by cutoff_guard), the tense of field values (OV-002, blocked by
defense ④), and the model's internal knowledge (unblockable — it can only be
measured and disclosed). Making the third channel explicit is the substance
of §5-5.

## L-2. Execution layer = via the Claude Code harness (not the raw API) — recorded 2026-07-06

**Limit**: the evaluatee and grader calls of this run went through the
**Claude Code harness v2.1.201** (`claude -p` subscription headless, freeze
revision #2), not the raw API. The flag set and the isolation demonstration
(probe confession + debug-trace grep) are in RP-04·RP-05·the run_log gate
verdict tables. The harness was measured to inject system-reminder blocks
(userEmail·currentDate) even after system-prompt replacement (J13-e) —
applied identically to treatment and control, but a deviation from the letter
of GP-6 "0 context outside the payload". A harness version change is an
execution-environment change; reproduction requires pinning the same version.

**Causal specification (added per RP-06 B5(a), 2026-07-06)**: currentDate
injection weakens point-in-time framing on the harness path — the model knows
the current year, so it can infer that the cutoff date lies in the past,
which pushes in the direction of facilitating memorized retrieval. This
consequence was not left exposed by the design — **the recognition probe
measured it directly and D7 fired** (6/8 → CONTAMINATED → the perturbation
branch) — the risk was measured and absorbed, not blocked. However, the
standalone contribution of the currentDate channel was not measured
separately (it cannot be removed on the harness path — J13-e).

## L-3. Nondeterministic point estimate from a sample of 1 — recorded 2026-07-06

**Limit**: on this execution path, sampling parameters (temperature, etc.)
cannot be fixed. Each per-case verdict is therefore **a point estimate from a
sample of 1 drawn from a nondeterministic distribution** (combined with the
D5 single run). The spread of the perturbation delta (RP-05 §3, range −30 to
+23pp) mixes memorization contribution and sampling variance in an
unseparated state — any case-level delta interpretation must state this
non-separation.

## L-4. The V7 static scan's threat surface differs on the harness path — recorded 2026-07-06

**Limit**: the V7 static scan (pipeline↔scoring isolation · no guard bypass)
was designed against Python code inside the repository. On the harness path
the threat surface is different — the potential channel for grading-material
backflow is not code imports but **harness context assembly** (settings,
memory, hooks, MCP, CLAUDE.md). This cycle controlled it not by static
scanning but by **run-time demonstration** (isolation probe + trace grep,
gates 3·4) — the nature of the control changed from 'code invariant' to
'per-run verification', and reruns require gate re-verification.

## L-5. Perturbation scatters memorized numbers but does not remove identity recognition — recorded 2026-07-06 (RP-06 A1)

**Limit (mandatory wording, owner directive verbatim)**: "perturbation
disrupts memorized NUMBERS, not IDENTITY recognition." — even on inputs that
went through perturbation (company-name·ticker·CIK anonymization +
constant-multiple rescaling, D8), the evaluatee model named the real
identities of 6 of the 8 treatment firms (draw 1) / 5 firms (draw 2, RP-06
A1 redraw) (union 6/8, common to both draws 5/8: LOGI·HTZ·ICON·KHC·MRVL —
verdict rule: frozen probe_verdict). Ratio and trend patterns + original
dates retained (D8 owner decision) are enough to restore identity.

- Consequence: the "perturbed run" numbers are also **an upper bound under
  identity recognition** — what perturbation removes is exact numeric replay
  (verbatim recall 0/8), not case recognition. This is the measured
  confirmation of D8's design intent ("perturbation is a measurement device
  for the memorization contribution, not a removal device").
- **Published claims must carry this caution alongside the headline** (owner
  directive RP-06 A1 — reflected in README·RP-06).
- The recognition verdict is itself a nondeterministic sample: SCOR was
  recognized in draw 1 → unknown in draw 2. The D7 threshold (≥3) fired in
  both draws — the contamination verdict is robust to the redraw.
- **Addendum dated 2026-07-20 (D99 — post-hoc audit, not a retroactive
  edit)**: **retention of original accession numbers** is added to the
  identity-restoration paths. The v1 perturbed payload carried each financial
  fact's original SEC accession verbatim (prefix = filer CIK, middle part =
  filing year), and the output schema required accession citations. The
  earlier wording of this limit ("restorable from ratio/trend patterns +
  original dates retained alone") was therefore incomplete — the accession
  metadata path coexists, and separating the paths is impossible in the v1
  design. The perturbed frame is described only as "partial
  de-identification". Audit: `analysis/V1_PARTIAL_DEIDENTIFICATION_AUDIT.md`
  · notice: `docs/V1_PARTIAL_DEIDENTIFICATION_NOTE.md` · regression guard:
  `pipeline/test_deid_disclosure.py`.

## (Placeholder) L-6 and beyond

Further limitations are recorded in this document as discovered — no post-hoc deletion or softening; changes only via history disclosure (§5-6).

<!-- canary: A2D69CFE-CA8A-4DE1-8393-5B225099299B (D9 — 학습 유입 감지용) -->
## L-6. Intra-family grader bias — recorded 2026-07-09

**Limit**: the grader (`claude-fable-5`, fallback `claude-opus-4-8`) and the
evaluatee (`claude-sonnet-5`) are **both in the Anthropic Claude family**.
Since the grader is not independent of the evaluatee, a leniency toward the
output style and reasoning conventions of same-family models (grading
leniency) cannot be ruled out in principle — a limitation on the execution
layer along the same axis as L-2 (harness mediation), but where L-2 is
non-independence of the *environment*, L-6 is non-independence of the
*judge*.

- **Practical mitigation**: every grading record passes human final
  confirmation (§7, `human_finalized=true` + the override ledger
  `scoring/overrides.md`) — a structure in which leniency, had it occurred,
  would leave traces in the override records. This mitigation holds only on
  the premise that human review is exhaustive, not sampled (RP-13).
- **Prospective mitigation**: the E4 cross-model arm (EXPLORATORY —
  `analysis/CROSSMODEL_PLAN.md`) could provide a non-family grader contrast,
  but it has not been run, and even if run it is for limitation footnotes
  only (EXPLORATORY).
- This limitation acts on **the grading dimensions (d1~d4) and false-positive
  interpretation** rather than on separation itself (AUC·permutation p) —
  the p score is the evaluatee's output and the grader only converts it into
  bands, so the exposure of the 1st-order headline (permutation p) is
  limited.

## Instrument bias directions — recorded 2026-07-10 (D31, 2nd external review Phase 0-1)

> The 4 contamination-measurement instruments are each **a proxy for
> something different and biased in a different direction**. When a
> publication cites these instruments' numbers, it states these directions
> alongside. (The empirical numbers in this table are per frozen records —
> L-5·synthesis.json §reconcile·D27.)

| Instrument | Proxy for · bias direction | Empirical basis |
|---|---|---|
| **name-ID rate** (frozen `name_match` rule) | **Lower bound** on induced identification — false negatives exist (substantive recognition the rule misses) | DAR boundary false negative demonstrated: the probe response "Darling International Inc. (now Darling Ingredients Inc.)" is plain identity recognition, yet the frozen rule judged it False for not handling former names (`synthesis.json` §wave2_name_id_reconcile, Q-E02) |
| **Perturbation delta** (original−perturbed score gap) | **Lower bound** on the **surface** (name·scale) memorization contribution — the deep channels perturbation cannot remove (ratio·trend patterns) remain | Residual identity recognition after perturbation 5–6/8 (recognition-probe draw-1 6/8 · draw-2 5/8, L-5) — perturbation scatters memorized numbers but does not remove identity recognition |
| **Cognitive probe** (recognition probe, D7) | **Point estimate** from a single draw — nondeterministic sample with a demonstrated ±1 swing between draws | draw-1 6/8 → draw-2 5/8 (RP-06 A1 redraw; SCOR flipped between draws — L-5). The D7 threshold (≥3) fired in both draws, hence robust |
| **recognition gate (k=1)** (holdout eligibility gate) | Single-draw pass verdict — **false-negative arithmetic**: assuming a per-case per-draw recognition probability of 30%, the single-draw non-recognition (pass) probability is 70%, and the probability that 3 cases pass 3/3 ≈ 0.7³ ≈ **34%** — i.e., a "3/3 pass" is not rare by chance in a single draw | the gate was judged on the single draw-1 (`runs/holdout/recognition/`); promotion to k=5 is a D32 pre-registration item |

## L-7. Design confounder in arm (c) of the identity 3-arm experiment — recorded 2026-07-11 (D39, flagged by the 3rd external review)

**Limit**: in the identity 3-arm design (D36), reusing the frozen original
(real names + real numbers) as arm (c) kept the freeze invariant at 0 new
calls, but at the cost that **the c−b contrast is a confounded comparison of
the identity effect and the scale-restoration effect** — (b) is fabricated
names + perturbed (rescaled) numbers while (c) is real names + original
numbers, so the two axes move simultaneously. In this design the only clean
causal contrast is **b−a** (identical perturbed payload, differing only in
name tokens).

- **Resolution limit**: (a)·(c) are past frozen draws, (b) is a new draw —
  cross-arm comparisons include draw noise (per-case 5-draw band 12–18pp ≈
  ±10pp, measured in E5 §7 `analysis/holdout_redraw_results.json`). The
  ±6pp median is a directional reading within that resolution.
- **Publication convention (machine-enforced)**: whenever a publication
  surface cites a 3-arm delta, it must carry the confound and draw-noise
  caveats alongside — `tools/lint_publication.py` rule (I), D39.
- **Attribution record (accountability)**: this confounder was **identified
  in the design by the 3rd external review**. The design cause is that the
  D36 pre-registration defined arm (c) as frozen-draw reuse (the trade-off
  of the 0-new-calls constraint). The pure identity contrast (c′ = frozen
  perturbed payload + real-name tokens) has not been run — whether to run it
  is an owner gate (default SKIP; b−a and E3 point in the same direction, so
  it is not required before publication).
- Classification (ii) "the score contribution of memorization is small
  (a≈b≈c)" stands on the 1st-order evidence b−a (+6.0pp < the 10pp bar) and
  is not overturned by this limitation — what this limitation cuts is the
  standalone interpretability of the c−b axis.

## L-8. FAIL verdicts in the retrospective control-cleanliness audit — published FPRs are conditional on the original selection criteria — recorded 2026-07-21 (D106 §3, CONTROL_CRITERIA_v3 §4)

**Limit**: the retrospective audit (`controls/retrospective_audit_v1.md`,
disclosure-only) that retroactively applied the v3 §1 checklist
(pre-committed at 1ce4cb8) to all 62 existing controls found **8 rows (7
unique registrants) FAILing at least 1 criterion**. The original selection
criteria that grounded the control labels (v1/v1.1/v2 — centered on
non-enforcement screens) did not screen for the events below, so **every
published FPR is conditional on the original selection criteria** — no
retroactive recomputation or reclassification under the v3 criteria is done
(D106 common OUT).

- **FAIL list** (full citations in `controls/retrospective_audit_v1.md`
  §3.2):
  - **(f) securities class action surviving MTD** (alleged period
    intersecting the audit window): C02 (NUVA — suit filed after the window
    in 2013, merits proceeding and settlement after MTD), C04·V10 (R —
    filed 2020, MTD denied (in full) 2022-05-12, settled), V11
    (UPBD/Rent-A-Center — filed 2016, MTD denied 2017-12-14, settled), V20
    (LQDT — filed 2014, MTD denied in part 2016-03-31, class certified and
    settled), W13 (FLO — filed 2016, MTD denied in part 2018-03-23,
    settled).
  - **(e) auditor resignation + Item 304 disagreement**: GRDX (hc, 8-K
    2024-08-15 — auditor resignation accompanied by a company-disclosed
    'Disagreement').
  - **(d) material weakness uncured through the next annual assessment**:
    GO (hc — identified FY2023, still not effective in the FY2024 assessment
    (consecutive adverse ICFR opinions), cured in FY2025).
- **Reading direction**: these are facts of the disclosure and court record,
  not adverse labels on the companies — on (a) absence of SEC enforcement
  action, all 62 pass. From the control-cleanliness standpoint, however,
  published FPRs computed with FAIL controls included (including main-frame
  false-positive interpretation) must be read as numbers over a
  "non-enforcement per v1/v1.1/v2 criteria" sample, not a "clean per v3
  criteria" sample. FAIL row C04 (R) is the same registrant as a main-frame
  false-positive case in the frozen record (case_10, atlas/case_10.md) —
  state this overlap in any false-positive interpretation.
- **Invariant boundary**: published-FPR recomputations 0, retroactive
  control removals/reclassifications 0, frozen grading-record contacts 0
  (v3 §4 · D106 common OUT). The only deliverables are this disclosure and
  `controls/retrospective_audit_v1.{md,json}`.
- **Holdout provisional**: the 9 hc controls are all provisional under (g)
  as their 24-month window has not elapsed — (a)–(f) re-search is scheduled
  when the window is reached (GRDX (d) and GO (f) each also carry their own
  INCOMPLETE open items).
