# atlas/PATTERNS.md — Accounting Error Atlas: cross-case synthesis

Authored by Claude Code, pending human audit (D15). **human_finalized: false.**
Authority: D106 ② (ERROR_ATLAS_v1). Synthesis over atlas entries only — no new
scoring, no metric changes; every claim cites case IDs. 본 결과는 Claude 기반
단일 파이프라인에 한정된다 (PROJECT.md §5-5).

Basis: the 35 drafted entries in `atlas/INDEX.md` — 14 flagged treatments
(TP: case_01, case_02, case_08, case_09, case_12, case_13, case_39, case_40,
case_59, case_60, case_61, case_65, case_66; TP-provisional: case_71), 6
missed treatments (FN: case_03, case_06, case_52, case_67; FN-provisional:
case_72, case_73), 11 FP controls (case_10, case_30, case_33, case_37,
case_44, case_48, case_49, case_54, case_69, hc_03, hc_07), 4 TN-flagged
controls (case_05, case_07, case_11, case_14). All scores are frozen outcomes
quoted as recorded ("score NN" per RP-16/D91); nothing here re-scores any
case. Match-quality language uses each entry's §4 closed enum, cited as
drafted — those calls are themselves pending owner audit.

---

## (a) RECURRING ACCOUNT-LEVEL PATTERNS ACROSS TPs

Four account-level patterns recur across the correct flags; each entry's §4
verdicts separate "right flag, right mechanism" from "right flag, wrong
mechanism."

### a-1. AR-vs-revenue divergence (the workhorse signal)

Receivables outgrowing revenue is the most frequent contributor to flagged
treatments (case_01, case_02, case_08, case_09, case_39, case_40, case_59,
case_60, case_66). Its correspondence to the true mechanism splits three ways:

- **Matched the true mechanism** (the scheme genuinely produced uncollected
  receivables): case_02 (contingent distributor sales; §4 "exact mechanism";
  the order itself records "ballooning [Days Sales Outstanding]"), case_40
  (improper revenue carried as an unpaid-bill "receivables" backlog; "exact
  mechanism"), case_60 (pay-on-resale side arrangements converting shipments
  into uncollected AR; "exact mechanism"), case_39 (premature/price-inflated
  recognition; "exact mechanism" at family level, consignment not named).
- **Right account, wrong treatment**: case_01 (DSO-inferred premature
  recognition vs the actual NMT/barter valuation scheme; DIM2=1), case_09
  (premature recognition of real royalties vs fabricated round-trip JV gains
  plus uncollected royalties; DIM2=1 main), case_59 (allowance
  under-reserving story on the right receivables axis while the actual
  mechanism, quarter-end pull-forward, sat in hypothesis 2).
- **Divergence real but unrelated to the enforcement mechanism**: case_12
  (the 2018 AR ramp carried the top hypothesis; the order alleges a
  procurement COGS scheme with no receivables allegation; DIM2=0), case_61
  (hypothesis 2 receivables story has no complaint counterpart), case_65
  (receivables/margin flags coincide with a 2009 oilfield downturn, not the
  tax scheme; §7 "false-mechanism/true-flag").

### a-2. Reserve / allowance trajectories

Allowance/reserve series contributed to flags in case_02 (allowance +72.6%
build — matching the collectability failure), case_40 (allowance static at
$102K while AR more than doubled — matching the rejected reserve-increase
advice at complaint ¶73), and case_39/case_59 (allowance declines read as
under-reserving — a symptom reading the orders do not allege). The inverse —
attaching a reserve story to the wrong reserve — recurs: case_06
(AR-allowance release flagged; the released reserve was the LTA rebate
accrual), case_08 ("delayed write-offs" reaches the subrogation-allowance
conduct verbally but ranked second under a receivables framing), case_52
(CL6 anchored to a corrupted allowance tag, never examining the
AccruedLiabilitiesCurrent series housing the cookie-jar family). The
pipeline reliably notices *that* a reserve moved, unreliably *which* one.

### a-3. Inventory, margin, and capitalization/impairment balances

- Inventory/LCM: case_02 hypothesis 3 stated the E&O under-provisioning the
  order quantifies ($3.4M/$5.6M) — "exact mechanism," graded off-scheme under
  the single-mechanism key (§7 CRITERIA question). case_03 (FN) is the mirror
  image: the delayed-write-down hypothesis was "exact mechanism" but ranked
  third, dated one year late, under score 42.
- Soft-asset balloons: case_61 is the strongest asset-side hit — the
  OtherAssetsNoncurrent $1.5M → $46.6M → $9.7M balloon-and-collapse aligned
  temporally with the round-trip window ("right direction only"). case_09's
  perturbed frame stated the ASC 350 non-impairment mechanism the order
  quantifies at $239.4-259.4M ("exact mechanism," ranked second). Against
  these, case_08 leads with a goodwill/PPA narrative the order never alleges
  — self-refuted by the acquisition the output itself names (DIM2=0);
  case_03 anchors on the loud goodwill impairment, not the quiet inventory
  reserve.
- Depreciation/holding-period (case_08 fleet leg): not surfaced in either
  frame — no fleet-depreciation series in the deck.

### a-4. Filing-form chronology as a legitimate co-signal

Chronology carried real weight in several correct flags: case_08 (the one-day
10-K/A turnaround was the top signal; earliness recorded 0q), case_65 (the
10-Q/A amendments plus the 2010-2011 CORRESP/UPLOAD cycle — the only genuinely
scheme-linked pre-cutoff signal and the model's sole "high"-confidence flag),
case_71 (the 2018-01-05 amendment cluster as restatement propensity — "right
direction only"), case_39/case_40 (NT filings, amendment-only chronology).
The same instrument misfires on controls (§d-4) — chronology is the
pipeline's highest-variance source: decisive in case_08/case_65,
template-noise in case_13/case_33 (the backdating template fired 2/2
unhelpfully per `analysis/error_analysis.md` §5 as quoted in both entries).

---

## (b) PERFORMANCE BY MISSTATEMENT TYPE

Grouping treatment cases by each entry's §2 mechanism family. Counts describe
the frozen outcomes only.

### b-1. Revenue recognition / timing — the pipeline's home ground

Registered revenue-recognition/timing schemes: case_01, case_02, case_09,
case_13, case_39, case_40, case_59, case_60, case_66 — **9/9 flagged (TP at
threshold 50, main frame)**. Match quality splits: exact-mechanism-family
hits in case_02, case_39, case_40, case_60, case_66;
right-account-wrong-mechanism in case_01, case_09, case_59; one wrong-reason
TP, case_13 (top narrative was options backdating — a real prior event, not
the charged pull-in scheme; the substantively correct "pulling forward sales"
hypothesis ranked second and misdated; DIM2=0). Where the mechanism leaves a
balance-sheet residue (uncollected AR), the pipeline both flags and roughly
explains; where the scheme is quantitatively quiet (fabricated JV gains,
case_09; barter valuation, case_01; disclosure-side pull-ins,
case_13/case_66), the flag survives but mechanism content degrades.

### b-2. Reserves & allowances / estimate manipulation

case_08 (TP score 78 — but DIM2=0: subrogation-allowance and
fleet-depreciation mechanisms both missed; "점수는 맞고 기제는 틀림" per the
quoted error_analysis row), case_03 (FN score 42 — warranty under-accrual
never surfaced despite a flat-to-declining sealed warranty series; the
order's fraud-leg inventory hypothesis surfaced but ranked third), case_52
(FN score 40 — cookie-jar reserve axis returned insufficient_data on a
corrupted allowance tag). **0/3 right-mechanism flags in this family**; one
flagged for other reasons, two missed by score — the family where "right
flag" and "right mechanism" come apart most completely.

### b-3. Capitalization / impairment / asset overstatement

case_61 (TP score 72, DIM2=2 — treatment type "substantially matches"; the
strongest asset-side result), case_09's impairment leg (captured only in the
perturbed frame's second hypothesis), case_52's capitalization leg
(hypothesis 1 "exact mechanism" — surfaced but sub-threshold at score 40),
case_03's LCM leg (surfaced, mis-ranked, sub-threshold). Mixed: one clean
hit, one hit-by-second-rank, two correct-content-wrong-weight FNs.

### b-4. Cost / rebate schemes — systematically missed. No smoothing.

case_06 (FN score 28): the gross-margin collapse — the arithmetic footprint
of the rebate deferral — was flagged at CL4, quoted exactly, then discharged
with "well-known glyphosate/Roundup pricing pressure"; the identity-masked
frame scored 58 on the same numbers. case_12 (TP score 68): flag achieved on
an AR narrative with **no counterpart in the order**; no hypothesis in
either frame touches COGS/supplier rebates (DIM2=0 both frames). Combined
family record: **0/2 mechanism identifications; 1/2 flags, that one for
unrelated reasons.** The account these schemes live in
(vendor-consideration/rebate accruals) had no XBRL tag in either sealed
facts set — an input-visibility floor both entries flag for owner
attribution (case_06 §7 DATA(design); case_12 §7 detectability note).

### b-5. Tax accounts

case_65 (TP score 74): flagged, but the tax hypothesis — the only one
matching the income-tax provision manipulation — ranked third behind revenue
and goodwill stories with no enforcement counterpart (DIM2=0). A wrong-reason
TP: the scheme was built to defeat aggregate screening (the plug existed to
make ETR match guidance); the one genuinely scheme-linked signal weighted
highly was the amendment/comment-letter chronology. 0/1 top-ranked mechanism
identification in the family.

### b-6. Non-GAAP metric manipulation — structural zero

case_67 (FN score 20): the manipulated quantity (SP NOI Growth Rate) is
non-GAAP, un-tagged in companyfacts (zero matching concepts among 321), moved
partly on spreadsheets outside the accounting system, at $56K-$425K
magnitudes against consolidated income in the hundreds of millions. §6
records R1: signal absent from the input as a fact of the world — "입력에
신호 부재," type (iv) structural miss. **0/1; an
XBRL-financial-statements-only pipeline cannot detect this family**; the
entry treats the empty hypothesis list at score 20 as arguably the honest
output.

### b-7. Other / holdout mechanisms (provisional tier)

- Liability accounting, holdout tier: case_71 (TP-provisional score 70 —
  flag driven by 2018 amendment history and goodwill trend; neither leg of
  the 2023-24 unrecorded-AP mechanism covered; "tier hit, mechanism miss")
  and case_73 (FN-provisional score 42 — the captive-insurance liability
  complex was tagged, fast-growing, and inside documents_used, yet the
  output never touches an insurance tag; the checklist's
  income-overstatement aim points away from a liability-overstatement error).
- Localized (plant-level) inventory: case_72 (FN-provisional score 32 — CL4
  examined consolidated inventory and cleared it; ~$22M cumulative
  plant-level overstatement leaves no ratio signal at a ~$300M consolidated
  balance; (ii-a)+(iv) mixed).
- Disclosure-only limbs: case_66 and case_13 both flagged, but the
  MD&A-omission component — the conduct actually charged in case_66 — is
  uncovered by any hypothesis in either case (no narrative text in the decks).

**Plain summary**: the pipeline flags revenue-shaped and asset-shaped
schemes; it systematically missed cost/rebate mechanisms (case_06, case_12),
non-GAAP metric manipulation (case_67), below-consolidation-altitude or
omission-shaped misstatements (case_72, case_71, case_73), and identified the
tax mechanism only at third rank (case_65). Several headline TPs are
wrong-reason hits (case_08, case_12, case_13, case_65).

---

## (c) WHICH DISCLOSURE SOURCES CONTRIBUTED TO CORRECT FLAGS

The evaluatee decks carried two source classes: XBRL structured facts and
filing-form chronology metadata. Entries' §3 sections uniformly record that
**narrative text (MD&A, footnotes, press releases, comment-letter content)
was not in the input set** — stated explicitly in every FP and TN-flagged
entry and in case_08, case_09, case_66, case_67 among others.

- **XBRL structured facts** drove the substantive content of nearly every
  correct flag: the AR/revenue, allowance, inventory, deferred-revenue, and
  NI-vs-OCF series in case_01, case_02, case_09, case_39, case_40, case_59,
  case_60; the soft-asset balloon/collapse in case_61; the pre-restatement
  net-income figures in case_65 (tying to the order's ¶56 table). Where the
  scheme's account had no tag (rebates in case_06/case_12; SP NOI in
  case_67; plant-level inventory in case_72), the XBRL channel was silent
  and the flag either failed or succeeded for other reasons.
- **Filing-form chronology** (8-K items, amendment sequences, NT filings,
  CORRESP/UPLOAD cycles) was the decisive contributor in case_08 (one-day
  10-K/A, earliness 0q) and case_65 (amendment + comment-letter cycle, CL7
  "high"), and supporting in case_39 (NT 10-K), case_40 (amendment-only
  chronology), case_71 (2018 cluster as restatement-propensity prior). Its
  failure mode on controls is §d-4.
- **Narrative text — largely absent, and its absence is load-bearing**: the
  legs the pipeline could not reach live in narrative or contract-level
  disclosure — MD&A trend omissions (case_13, case_66), JV footnotes/deal
  terms (case_09), supplier contract documentation (case_12), non-GAAP
  supplemental tables (case_67), segment-level series (case_02, case_59).
  Multiple entries record this as an information-set ceiling rather than a
  model error (case_60 §6, case_61 §6, case_66 §6), owner attribution
  pending.

---

## (d) THE RECURRING ACCOUNTING SHAPE OF FALSE POSITIVES

Across the 11 FP and 4 TN-flagged entries one meta-shape repeats, recorded
almost verbatim in several entries' §7: **genuine, individually explainable
figures — no fabrication found in any FP entry (all quoted values verified
against sealed facts; dim4 ≥ 2 throughout) — compounded into an adverse
composite, with the benign alternative named but not weighed.** Five
recurring sub-shapes:

### d-1. Distress or disclosed impairment read as prior misstatement

- case_30 (score 65): ASC 805 acquisition goodwill followed by openly
  disclosed ASC 350 impairment charges read as evidence prior carrying values
  were overstated — "곤경(distress)과 분식(misstatement)의 혼동" per the
  quoted error_analysis §5; the impairment tags carrying the disclosed
  explanation sat in accessions the model listed in documents_used.
- case_05 and case_11 (TN-flagged, E2): FY2013 impairment / 2011
  acquisition-period volatility promoted to scores 50-62 on truncated
  windows; main frames held 48 and 45 with the reversal data in view.

### d-2. One-time and structurally ordinary items over-read

- case_69 (score 50, at-threshold): the Q4 2013 income spike read as
  reserve-release corroboration while the same sealed accession carries a
  disclosed $12.7M one-time investment gain larger than the quarter's
  entire net income.
- case_49 (score 58): the model itself attributed the NI/OCF gap to non-cash
  charges "typical of reverse-merger micro-cap biotechs," then elevated
  anyway — the self-hedge-then-elevate signature ((ii-a)). case_44 (score
  55): same shape on a mortgage REIT's fair-value NI/CFO gap.
- case_48 (score 55): a $457K allowance catch-up (~0.26% of revenue) and a
  SaaS non-cash NI/CFO gap that ties to add-backs within $23K.
- hc_07 (score 58): percentage growth on a de-minimis base — AR at 0.25-0.40%
  of revenue (DSO under 1.5 days) in a point-of-sale grocer.
- hc_03 (score 78 — the highest score in the entire holdout tier, on a
  control): micro-cap atypicality (two-point revenue series, held-for-sale
  reclassification, warrant/derivative gains) compounded to the arm's top
  score with CL8 itself recording insufficient data.

### d-3. Tag re-mapping and coverage artifacts read as anomalies

- case_44: the headline "internally inconsistent" interest-expense series is
  a concept re-mapping (InterestExpense → InterestExpenseBorrowings);
  quarterly figures tie to the borrowings totals to the dollar in the cited
  accession.
- case_49: a genuine XBRL sign inconsistency between two cash-flow tags, plus
  an "as restated" label on an ordinary cross-quarter comparison.
- case_07 (TN-flagged, E2): a convertible-debt reclassification
  (ConvertibleDebtCurrent appearing exactly when LiabilitiesCurrent steps up)
  scored 50-55 on truncated windows as an "unexplained" spike — not draw
  noise (main-frame re-draws 15-25).
- case_37: the false "restating period ended 2011-06-30, filed over a year
  after the original" chronology tracks a deck-construction artifact
  (originals omitted from documents_used; comparatives attributed to /A
  accessions) — R1 DATA-direction counter-argument on record.

### d-4. Amendment-chronology misreads (the Ryder axis)

The most repeated FP driver: reading 10-K/A / 10-Q/A / CORRESP metadata as
restatement evidence without the decisive test — *did any value change
across filings?* Sealed answer in every instance: no change found.

- case_10 (score 58): a Part III-practice 10-K/A promoted to "strong
  indicator of a financial restatement" (CL7 "high"); every spot-checked
  figure identical across filings; zero Item 4.02 in history.
- hc_07 (score 58): form+date entries promoted to "A confirmed restatement
  occurred"; zero facts sourced to the amendment accessions.
- case_48 (score 55): comment-letter cycle + 10-K/A read as "a common
  precursor to identification of misstatements"; the /A left no numeric
  revision trace and the FY2015 10-K followed on schedule.
- case_33 (score 55): a resolved 2006-07 episode ≥9 years pre-cutoff —
  outside the E5 label window — carried the top hypothesis via the reused
  backdating template; additionally a label-window/input-scope mismatch
  (분류 (iii)), the one FP whose primary bucket is not pure interpretation.
- case_54 (score 55) and case_44/case_49: stale chronology (2015 amendments
  with no footprint; 2004-2013 shell-era clusters) cited as current risk.

### d-5. Truncated-window effects in the E2 layer

All four TN-flagged entries (case_05, case_07, case_11, case_14; case_10
also E2-flagged) share one structure: the full-deck main frame integrated
reversals and mitigants into a sub-threshold score; the flag arises only
when the same genuine facts are re-read on shortened point-in-time windows
under the any-snapshot rule ("리드타임의 대가로 오탐 기회도 스냅샷 수만큼
늘어난다," quoted in each entry's §6). case_14 is the cleanest
demonstration: scores fall as the window lengthens (55-58 on 2011-2012
windows → 32 full-deck), with the AR reversal already inside j7's own window
but not cited. Benign resolutions recorded per entry: AR spike-and-reversal
(case_05, case_14), debt reclassification (case_07), acquisition purchase
accounting (case_11).

Common note for d-1 through d-5: the FP entries document model errors on
control companies, not company problems — PROJECT.md §6 vocabulary applies;
each entry's §2 records the "비집행 ≠ 무결" caveat, conservative direction.

---

## LIMITATIONS

- **Inherited draft status**: this synthesis inherits every entry's
  human_finalized=false status; entries' §4 calls and §6/§7 attributions are
  unaudited work product until owner sign-off (PROJECT.md §7).
- **Single-pipeline scope**: 본 결과는 Claude 기반 단일 파이프라인에 한정된다
  (PROJECT.md §5-5). Findings describe this pipeline on these frozen decks,
  not LLM capability in general.
- **Counts are description, not performance claims**: all tallies restate
  frozen, already-graded outcomes at the pre-registered score ≥50 threshold;
  no metric is recomputed, no threshold or definition introduced; holdout
  outcomes remain provisional (upgrade monitoring per
  `analysis/LABEL_REPORT.md`).
- **Small strata**: several family-level statements rest on 1-3 cases (tax:
  case_65; non-GAAP: case_67; cost/rebate: case_06, case_12) and cannot
  support generalization beyond this sample.
- **Frame and draw sensitivity carries through**: several outcomes are
  frame-dependent (case_02, case_13 TP in main frame only; case_06 FN in
  main frame only) or sit inside recorded draw-noise bands (case_10 4/5
  re-draws below 50; case_33 2/3 below 50; contrast draw-stable case_30,
  case_44, case_48, case_54); single-draw holdout controls (hc_03, hc_07)
  cannot be stability-tested.

## [OWNER REVIEW] — judgment calls most needing adjudication across entries

1. **Top-ranked-only rubric vs lower-ranked correct mechanisms** — the
   recurring cost driver of DIM2=0/1 on otherwise-correct analysis: case_03
   (rank 3 exact), case_13 (rank 2 exact, misdated), case_59 (rank 2
   channel-stuffing), case_65 (rank 3 tax), case_73 (rank 3 "materially
   closer"), case_09 (perturbed rank 2 impairment). Whether to carry
   rank-weighted credit is a cross-entry call.
2. **DATA vs MODEL attribution where the mechanism's account had no
   delivered series** — case_06 (rebate accruals, J10), case_08
   (allowance/depreciation), case_12 (vendor-consideration tags), case_67
   (non-GAAP), case_72 (plant-level), case_73/case_69/hc_03
   (payload-inclusion not determinable); several entries defer R1 closure
   to deck-payload inspection.
3. **§4 enum boundary cases** — case_13 "exact mechanism" despite the FY2013
   vs 2015 window offset; case_40 row 3 period misplacement; case_39
   family-level "exact mechanism" without consignment named; case_12
   hypothesis 3 "right direction only" vs "unrelated"; case_71 whether
   "right account wrong mechanism" overstates a coincidental overlap.
4. **Answer-key coverage** — case_02 hypothesis 3 (E&O) graded extraneous
   while order ¶85-91 describes the conduct; null genre_tag_rows leaving
   dim3 unscored (case_61, case_65, case_71, case_72, case_73); case_40
   dim3 deferred.
5. **Wrong-reason TPs in headline metrics** — whether case_08, case_12,
   case_13, case_65 (and provisional case_71) should be presented as risk
   triage rather than mechanism identification wherever detection counts
   are reported; case_65 §7's false-mechanism/true-flag inflation warning.
6. **Identity/recognition overlay** — the bidirectional familiarity effect
   proposed across case_06 (exculpatory, Δ+30 masked), case_08
   (imprinted-guilty, Δ−23 single-draw vs the −30.2 statistic needing basis
   confirmation), case_12 (recognized, Δ0), case_03 (recognized yet FN) —
   needs a consolidated owner reading before narrative use.
7. **E2 any-snapshot rule and near-threshold draw noise** — whether the four
   TN-flagged entries should be reported jointly with the rule's recorded
   cost line and the RP-06/RP-07 dispersion bands, given E2 is ungraded.
8. **Checklist design questions surfaced by the misses** —
   direction-symmetric reserve screens (case_73), most-recent-interim
   comparison in CL4 (case_72), completeness-oriented liability analytics
   (case_71), tagging-consistency pre-checks (case_44), non-GAAP input-scope
   expansion (case_67) — design questions, not re-scores; any change is
   subject to RP-17 post-hoc revision limits.
9. **Boundary and label nuances** — case_69's at-threshold score-50 FP as a
   threshold artifact; case_59's no-restatement books-and-records order and
   case_66's no-GAAP-findings disclosure case as TP-calibration nuances; the
   provisional tier's non-conflation rule (case_71, case_72, case_73).

---
*Document status: drafted — human_finalized: false; pending owner audit (D15).*
*채점: Claude 보조 + 인간 최종 확정. 교육·정보 목적, 투자 자문 아님.*
