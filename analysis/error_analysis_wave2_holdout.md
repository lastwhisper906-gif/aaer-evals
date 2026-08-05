> Korean original: [error_analysis_wave2_holdout.ko.md](error_analysis_wave2_holdout.ko.md) (frozen).

# Error anatomy — wave-2 (treatment 9 vs control 23) + holdout (HUBG·WMK·GNE)

> Authored by Claude Code, pending human audit (GA-001 (b)). 2026-07-08
> (OWNER-GATE-E session, P1).
> Target: an exhaustive error anatomy of the frozen grading results
> (`scoring/grades_wave2/`, `scoring/grades_holdout/`,
> human_finalized=false). Every quotation is verbatim from frozen artifacts
> (`runs/wave2/scores/`, `runs/holdout/scores/`) — no fabricated quotations
> (§5-3).
> **Scope limitation (§5-5)**: these results are confined to a single
> Claude-based pipeline (evaluatee pinned to claude-sonnet-5), no
> generalization to LLMs at large. Control label = "non-enforcement" (not
> "clean"). All holdout cases are **G2 provisional**
> <!-- Sanctioned one-to-one deviation: the Korean vocabulary quote is romanized. -->
> (restatement/non-reliance) — "fraud" and "bunsik" (a Korean term for
> accounting manipulation) are banned.
> **This document resolves the `wave2_summary.md` L52 stub ("follow-up
> classification").**

## §0. Classification scheme (inherited from RP-10 Phase 3.1, 4-way)

Each error gets one class; if mixed, a primary class + an annotation:

- **(i) evidence-absent**: the model invents a fact **not** in the payload
  (hallucination).
- **(ii) reasoning-failure**: the model misinterprets a figure that **is**
  in the payload — it cites the passage it misread. Subtypes: (ii-a) benign
  misreading (promoting a normal pattern to a risk), (ii-b) calibration
  failure (right direction, misplaced confidence/threshold), (ii-c)
  data-quality-artifact misreading (an XBRL tagging error taken as signal).
- **(iii) label problem**: the answer key is ambiguous/wrong.
- **(iv) structurally undetectable**: the signal is absent from the provided
  data (GAAP XBRL) **in the first place** — non-GAAP metrics, sub-ledgers,
  non-financial events.

## §1. False positives 5/23 (controls, p≥50) — **none are hallucinations, all are (ii) benign misreadings**

| Control | p | risk_tier | dim4 (evidence quality) | Primary class |
|---|---|---|---|---|
| IOVA (Iovance) | 58 | elevated | grounded (consistency OK) | (ii-a) |
| ADAM (Adamas / mortgage REIT) | 55 | elevated | grounded (no cap) | (ii-c)+(ii-a) |
| LEVI (Levi Strauss) | 55 | elevated | grounded (dim4=2) | (ii-a) |
| LPSN (LivePerson) | 55 | elevated | grounded (dim4=3) | (ii-a) |
| AORT (Artivion) | 50 | watch | grounded (dim4=3) | (ii-a) borderline |

**Key finding (resolves the L52 stub)**: the grader rationale judged **all
5** as "evidence is specific and grounded in provided data,
arithmetically verifiable ... rather than fabrication" (upper dim4). That
is, **the cause of the false positives is not fabricated numbers (i) but
over-interpretation of real numbers (ii-a)** — promoting normal
structural/ratio divergences into risk. This means the pipeline's trust
boundary lies on the **base-rate-neglect / missing-benign-explanation
(calibration)** side, not on hallucination (a failure type that is in
principle more correctable than hallucination).

- **IOVA (58)** — the payload signal is real:
  `NetIncomeLoss=-25,381,363 vs OCF=-3,662,192` (2013). Yet the model
  itself, in its top hypothesis, attributes the cause to "large non-cash
  charges ... **typical of reverse-merger micro-cap biotechs**" and still
  promotes to elevated — reading a pattern that is **normal by definition**
  (pre-clinical biotechs structurally show large non-cash-loss ↔ cash-outflow
  gaps) as risk. (ii-a).
- **ADAM (55)** — the headline signal "quarterly InterestExpense (Q4-2013
  `68,584,000`) vs annual (`6,655,000`)" is most plausibly a
  **quarterly-vs-annual-scope XBRL tagging artifact**. The model itself
  self-hedges with "possible understatement/**mis-tagging**" yet stays
  elevated. → data-quality artifact misread as signal (ii-c) + benign
  misreading (ii-a). *Pipeline implication*: a tagging-consistency pre-check
  could reduce this false positive (a fix candidate, within the
  max-2-touchpoint constraint).
- **LEVI (55)** — "AR grew 40–68% YoY ... while revenue grew only 3.8–6.8%"
  is arithmetically verified (`722,001,000` vs `487,240,000`=+48.2%). But
  **Levi Strauss IPO'd in 2019-03** — the FY2019 receivables surge has the
  benign explanation of post-listing wholesale expansion/seasonality. The
  model never weighed that alternative. (ii-a).
- **LPSN (55)** — "allowance flat at $708,000 for seven quarter-ends ... AR
  +84%, then 65% catch-up" + SEC comment letters. Real but benign (comment
  letters ≠ wrongdoing; allowance catch-ups are common). (ii-a).
- **AORT (50)** — p=50 sits **exactly on the flag threshold**. The model
  itself declares only "watch". A **boundary artifact** that flips on a
  1-point difference — the mildest of the 5. (ii-a, borderline).

**FPR comparison (wave-1 3/22 vs wave-2 5/23)** — worsened but **not
provable**:
- wave-1: 13.6%, Clopper-Pearson 95% **[2.9%, 34.9%]**
- wave-2: 21.7%, Clopper-Pearson 95% **[7.5%, 43.7%]**
- the wave-2 point estimate 21.7% lies **inside** the wave-1 interval
  [2.9%, 34.9%] and the two CP intervals overlap heavily →
  "**worse-but-not-provably**" (indistinguishable at N~22–23). The
  no-0%-headline rule is observed.

## §2. Misses 2/9 — **two opposite types** (no averaging)

- **CSC (Computer Sciences, p=40 → unflagged) — (ii-b) calibration
  near-miss, the detected content is right**
  - Answer key (AAER-3662): UK NHS contract POC overstatement + Australian
    cookie-jar reserves + Nordic improper capitalization of prepaid
    expenses / asset overstatement.
  - Model top hypothesis: "continued capitalization of costs ...
    under-impairment", pointing at `OtherAssetsNoncurrent +25.7%` (with
    revenue −3.7% at the same time) → grader **dim2=2** ("substantially
    matches ... expense_capitalization / asset_overstatement, direction
    (overstated), treatment type"). **That is, account area, direction, and
    technique substantively match.**
  - **The substance of the miss is not detection failure but confidence
    shortfall**: it saw the right mechanism but p=40 fell short of the 50
    threshold. **10 points higher and it flags.** Type (ii-b) calibration
    failure — the pipeline saw the right thing. (The reserves_smoothing
    axis is uncovered as CL6=insufficient_data.)
- **BRX (Brixmor, p=20 → missed, dim2=0) — (iv) structurally undetectable,
  the cleanest (iv) case**
  - Answer key (AAER-4061): smoothing the **non-GAAP 'same property NOI
    (SP NOI)' growth rate** across quarters via the '2617' cookie-jar
    ledger + lease-termination income timing. → the manipulation is **not
    on any GAAP consolidated financial-statement line** (a non-GAAP
    operating metric + an internal sub-ledger).
  - The model correctly dismisses the NI/OCF gap as "largely explained by
    substantial real estate depreciation ... a normal REIT characteristic",
    and itself states the data gap: "**Missing key data (revenue,
    intangible assets, allowance/reserve balances) prevents full
    evaluation**". mechanism_hypotheses = empty list.
  - **An XBRL-financial-statements-only pipeline is structurally unable to
    detect non-GAAP metric manipulation.** This is the boundary case of the
    trust boundary (not a capability shortfall — the signal is absent from
    the input). Type (iv).

**Implication**: of the 9 cases, **only BRX, 1 case, is structurally out of
the pipeline's range**. CSC is a calibration near-miss (right mechanism,
below threshold). Lumping them as "2 misses" erases this asymmetry.

## §3. Holdout (memorization impossible, identity frame) — per-case

- **HUBG (70, flagged ✔, dim1=2 / dim2=1) — right score, wrong mechanism**
  - Answer key: purchased-transportation costs ~$77M understated ·
    unrecorded AP, FY2023-24 10-K misstatements, CFO·COO dismissed (8-K
    Item 4.02, 2026-02-05).
  - The model's top hypothesis and signals anchor on the **past 2018-01-05
    amendment cluster** (10-K/A FY2015 + 3×10-Q/A) and goodwill
    `262.4M→733.7M(+178%)` impairment risk — grader dim2=1: "TOP-ranked
    hypothesis instead centers on the **historical 2018-01-05 amendment
    cluster** ... not [the 2026 event]". **That is, it did not catch the
    right company at the right tier for the right reason.**
  - **Honest framing**: the HUBG "hit" is evidence of *risk-screening*
    ability (elevating a company with an amendment history + goodwill
    bloat), not evidence of *forensic detection of the 2026 mechanism*. The
    H2 narrative "we caught HUBG" must be confined to **tier hit /
    mechanism miss**. (Partial (ii-b): a risk signal in the right
    direction; the specific event mechanism unknown.)
- **WMK (32, missed, dim2=0) — (ii-a)/(iv) mixed: immaterial at the
  consolidated level**
  - Answer key: meat-plant inventory overstatement ~$22M cumulative
    (FY2022-25), whistleblower.
  - The model chased AR/DSO divergence (`AR +28%/+25%` vs flat revenue,
    "DSO ~3.9→6.2 days") — **the wrong account area**. Grader: "CL4
    examined inventory", yet no flag. → a single meat plant's 4-year
    cumulative $22M overstatement **leaves no ratio signal in a grocery
    chain's consolidated inventory** (signal < noise). Type (ii-a)
    substitute-signal chasing + (iv) consolidated-level immateriality.
- **GNE (42, borderline, dim2=0) — (ii-a) borderline, coherent uncertainty
  on an error-like event**
  - Answer key: captive-insurance liability error (error-like, non-fraud).
  - The model pointed at the allowance/AR coverage drop (14.9%→8.8%) —
    account area missed. But p=42 "watch" is **coherent uncertainty** for
    an error-like event (not overconfidence). The mildest.

## §4. Calibration — wave-2 ECE **0.179** vs wave-1 0.209 (null-ish)

`analysis/calibration_wave2.py` → `calibration_wave2.json` (frozen scores
reused; definition identical to the frozen `calibration.py`: 10-bin ECE,
confidence = |p−50|/50).

- **ECE 0.179** (wave-1 0.209, Δ−0.03) — **same order, no substantive
  improvement**. Still ~0.18 miscalibrated. "Calibration did not get
  better" is a **null-ish result and reportable** (§ no self-embellishment).
- Confidence→correctness AUROC 0.746, threshold accuracy 25/32 (=7 errors:
  2 misses + 5 false positives). Confidence carries information but
  absolute calibration is poor — consistent with §1's "the failure is
  calibration, not hallucination".

## §5. Trust boundary synthesis (error attribution §5-3)

1. **The false positives (5/23) are benign misreadings (ii-a), not
   hallucinations (i)** — all grounded (upper dim4). The trust boundary is
   the base-rate / benign-explanation axis. Pipeline fix candidate:
   ADAM-style tagging-artifact pre-check (ii-c).
2. **The misses split asymmetrically into CSC (calibration near-miss, right
   mechanism below threshold) and BRX (structural (iv), non-GAAP)** — only
   1 case is out of range.
3. **The holdout hit (HUBG) is tier-right, mechanism-wrong** — risk
   screening ≠ forensic mechanism detection. Confine the H2 narrative to
   this strength.
4. Calibration shows no improvement over wave-1 (ECE ~0.18).

**What one must know from this judgment (learning note, §10)**: the binary
"hit/miss" tally erases the **kind** of error — among misses, (ii-b
calibration near-miss) and (iv structural miss) have opposite pipeline
implications (the former is a threshold/calibration tweak; the latter is
impossible without input expansion), and among hits, a tier hit without
mechanism agreement does not support a forensic claim. The fact that **the
false positives are all grounded** says this pipeline's failure mode is
"over-interpretation", not "making things up" — which defines the character
(correctability) of the trust boundary.

## §6. Incomplete / follow-up

- **E1 control false-positive anatomy**: E1 (holdout matched controls) not
  run → if control false positives occur, they are incorporated into §1 of
  this document in the same form (placeholder). Pre-registration:
  `analysis/HOLDOUT_CONTROLS_PLAN.md`.
- ADAM tagging-artifact (ii-c) pre-check = pipeline fix candidate (≤2
  touchpoints constraint, separate gate).

## §7. Disclaimer

Confined to a single Claude pipeline (claude-sonnet-5 pin); grading is
Claude-assisted + awaiting human final confirmation
(human_finalized=false). Controls = "non-enforcement" label (not "clean").
Holdout is G2 provisional — an opinion grounded in public 8-K (Item 4.02)
filings, not an SEC-confirmed finding of wrongdoing. No positions; no
non-public information used.
