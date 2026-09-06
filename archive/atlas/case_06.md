# atlas/case_06.md — Monsanto Company (MON) — wave-1 treatment T07

Authored by Claude Code, pending human audit (D15). Analytical document under D106 ② — not a scored output. 본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).

## 1. CASE HEADER

| field | value |
|---|---|
| Case ID (anonymized frame) | case_06 (scoring ID T07) |
| Cohort | wave-1 |
| Outcome class | FN (main frame, flag at score ≥50) |
| Ground-truth tier | AAER-confirmed (AAER-3741 / Securities Act Rel. 33-10037, File 3-17107) |
| Frozen score | score 28 (`runs/main/case_06.json`, run `original-case_06-r1`); perturbed frame score 58 (`runs/perturbed/case_06.json`, run `perturbed-case_06-r1`) |
| Grade record | `scoring/grades/main/case_06.json` and `scoring/grades/perturbed/case_06.json` (human_finalized: true, RP-09 Stage 0, commit 986a893, 2026-07-07) |

Company: Monsanto Company, CIK 0001110783, cutoff 2011-06-28
(`data/candidates/candidates.json` T07; `data/evaluatee/cases.json` case_06).
Perturbation delta: score 28 → 58 (+30). Per D8 the delta measures memorization
contribution — not a robustness pass/fail. The sign is the notable record: the
identity-masked, rescaled frame crossed the flag band (DIM1=1) while the
identity-bearing frame missed (DIM1=0) — a frame-specific miss.
`analysis/error_analysis.md` §1 records the k=5 perturbed mean as 54.8,
Δmean +15.8, outside 2SE (citing `scoring/rp07_stats.json`).

## 2. ACTUAL EVENT

SEC Order, In the Matter of Monsanto Company, Sara M. Brunnquell, CPA, Anthony
P. Hartke, CPA, and Jonathan W. Nienas, Securities Act Rel. 33-10037 /
AAER-3741 (Feb. 9, 2016), settled. Sealed local text:
`~/aaer-data/MON/33-10037.pdf.txt` (manifest-pinned,
`data/manifests/aaer_data_manifest.json`). Fiscal year ends August 31 (fn.2).

Per the Summary: in FY2009-2011 Monsanto "improperly accounted for millions of
dollars of rebates offered to Roundup" distributors and retailers, and recorded
rebate payments in Canada, France, and Germany as SG&A "rather than rebates" —
misclassification that "boosted Roundup gross profit in those countries" (¶1);
it thereby "materially misstated its consolidated earnings" and its Roundup-line
"revenues and earnings for its Roundup business lines", and "met consensus
earnings-per-share analyst estimates for fiscal year 2009" (¶2). Legs: (a) 2010
U.S. Loyalty Bonus Program — pre-announced late May 2009 to incent Q4 FY2009
purchases ("approximately 8.7 million Roundup Equivalent" gallons, ~"33% of the
Roundup" sold in the U.S. in FY2009, ¶16), costs recognized in FY2010 instead of
FY2009 (¶14-21; prepayments "totaled approximately $194 million", ¶18); (b) 2010
Earnback — reversal of "$57.3 million of these accruals because seven customers
did not achieve their LTA targets" while side agreements promised the rebates
anyway ("The accrual reversal boosted Monsanto’s reported revenues", ¶24;
$20.2M/$24.3M to Customers A/B, ¶26-33); (c) 2011 Earnback — ~$48M paid to
Customers B/C that belonged in FY2010 (¶34-36); (d) LBP Canada — ~$43M of
rebates booked FY2010 not FY2009 (¶37-41); (e) Canada SG&A conversion — ~$14M
booked as SG&A, not contra-revenue (¶42-49); (f) France/Germany SG&A programs,
no evidence of services performed (¶50-54; amounts in §9).

GAAP topic per the order: EITF 01-9 / ASC 605-50 (pre-codification standard
stated as such) — rebate obligations as "a reduction of revenue based on a
systematic or rational" allocation (Issue 6 / ASC 605-50-25-7), timing (Issue 4
/ ASC 605-50-25-3), SG&A-vs-contra-revenue classification (Issue 1 /
ASC 605-50-45-1) (¶10-11). Registered summary (`data/candidates/candidates.json`
T07 `scheme_summary`): deferred rebate-cost recognition (incl. side agreements)
plus SG&A misclassification, overstating FY2009-2011 earnings and Roundup gross
profit; `scheme_type` revenue_recognition + liability_understatement;
manipulation period 2009-06 to 2011-08; first revelation 2011-06-29
(secondary-sourced, medium confidence per candidates notes). Company civil money
"penalty of $80,000,000" (§IV.K).

## 3. SIGNALS AVAILABLE PRE-CUTOFF

Cutoff 2011-06-28. Sealed basis: `~/aaer-data/MON/xbrl/CIK0001110783.json` and
`~/aaer-data/MON/edgar/CIK0001110783*.json`. Pre-cutoff, as-reported, at
accession level (all cited facts filed ≤ 2011-06-28):

- **Gross-margin collapse across the scheme boundary**: GrossProfit $6,762M /
  SalesRevenueNet $11,724M FY2009 (57.7%) → $5,086M / $10,502M FY2010 (48.4%) —
  FY2010 10-K accn 0000950123-10-096537 (filed 2010-10-27), repeated in 8-K accn
  0000950123-11-034037 (2011-04-08). This is the arithmetic footprint of the
  mechanism: FY2009 gross profit held up by deferred/reversed rebate accruals,
  FY2010 absorbing the cost.
- **SG&A rising on falling revenue**: $2,037M FY2009 → $2,064M FY2010 (+1.3%)
  against revenue −10.4% (same accessions) — direction consistent with rebates
  parked in SG&A; magnitude (~$46M of programs per §2) ~2% of the base.
- **Quarter-end AR spike in the prepayment year**: AccountsReceivableNetCurrent
  $2,093M (2010-02-28) → $3,233M (2010-05-31; Q3 FY2010 10-Q accn
  0000950123-10-063363, filed 2010-07-02) → $1,590M (2010-08-31).
- **No account-level rebate-accrual series**: no us-gaap rebate/incentive tag
  exists pre-cutoff in the sealed company facts; the first dedicated tag,
  AccruedMarketingCostsCurrent ($887M at 2010-08-31), appears only in the FY2011
  10-K accn 0000950123-11-098240 filed 2011-11-14 — post-cutoff.
- **Chronology**: two 8-Ks of 2011-04-08 (accns 0000950123-11-034037/-034042)
  recasting historical statements, followed within days by offering documents —
  the order pins the "Form 424B2 prospectus supplement on April 13, 2011" as
  incorporating the misstated FY2010 10-K (¶55-56).
- The revelation (~2011-06-29) and the 2011-11-14 Restatement post-date the
  cutoff — not in the information set.

This section describes the information set — it does not re-score the case.

## 4. WHAT THE LLM CAUGHT (sub-threshold — FN)

Frozen output `runs/main/case_06.json`: `misstatement_probability`: 28 (legacy
v1 key — an uncalibrated ordinal score; see specs/RISK_SCORE_SEMANTICS.md) =
score 28, risk_tier "watch"; CL4 and CL6 flagged; `mechanism_hypotheses` is an
empty list. Quotes grep-verified in the frozen output; values verified against
the sealed XBRL.

| model claim (verbatim) | enforcement/restatement reference | match quality |
|---|---|---|
| "Gross margin compressed sharply (GrossProfit implied margin 57.7% in FY2009 vs 48.4% in FY2010) … plausibly explained by well-known glyphosate/Roundup pricing pressure rather than misstatement, but the direction is unusual enough to watch" (top_signals[1], CL4 flag) | The swing is the footprint of the core scheme: FY2009 revenues/gross profits improperly increased "by approximately $44.5 million when it deferred recording these liabilities" (¶33), the $57.3M accrual reversal (¶24), LBP costs pushed into FY2010 (¶19) | right account wrong mechanism |
| "a pattern consistent with, but not proof of, reserve release used to support earnings" — AR allowance $217M (2007-08-31) → $111M (2011-02-28) (top_signals[0], CL6 flag) | No doubtful-accounts allegation in 33-10037.pdf.txt; the reserve actually released was the LTA rebate accrual (¶24), a different liability | unrelated |
| "No NT filings, 10-K/A, or 10-Q/A restatements appear in the filing chronology through the cutoff, which is a mitigating factor …" (top_signals[3], truncated) | Accurate as of cutoff — the Restatement came 2011-11-14 (¶3); weighed as exculpatory | unrelated |

Main-frame grades: DIM1=0, DIM2=0 (no hypothesis; rationale notes the CL4 flag
"is adjacent to the actual Roundup gross-profit overstatement" but was explained
away), DIM3 null, DIM4=3. Perturbed frame: score 58, "elevated", three
hypotheses on scaled values. Top-ranked bad-debt under-reserving — DIM2=0, "not
the correct account area for either truth mechanism"; the rationale records that
hypothesis 3 ("reclassification of costs between cost-of-sales and operating
expense lines" behind the same 57.7%→48.4% swing) "is the closest to the true
rebate-cost misclassification, but per rubric only the top-ranked hypothesis is
scored"; DIM3 omission-estimate vs key active(cost) = 0; DIM4=3. Perturbed CL7
flagged the recast-8-K + 424B5/FWP/424B2 sequence — the one checklist touch on
the ¶55-56 offering nexus; the main frame answered the same item "no_flag" and
counted the quiet chronology as exculpatory (§4 table, row 3).

## 5. WHAT THE LLM MISSED

From the sealed §3 information set, by truth leg — distinguishing missed
signals from signals not in the information set:

- **Rebate cost deferral (LBP/Earnback → FY2009-2010 gross profit)** — signal
  IN the set, surfaced, then discharged. The 57.7%→48.4% collapse sits in the
  pre-cutoff as-reported series; the output flagged it at CL4, quoted the exact
  figures, then wrote it off as "plausibly explained by well-known
  glyphosate/Roundup pricing pressure rather than misstatement".
  `analysis/error_analysis.md` §1: "신호를 **보고, 인용하고, 회사 정체 지식
  ("well-known … Roundup")으로 설명해 없앴다**". The order makes the discharge
  doubly wrong: the pricing pressure was real — Monsanto was "well short of its
  annual gross profit goals" by Q4 FY2009 (¶13) — and the rebate programs were
  its response; the benign explanation and the misstatement share the same
  underlying economics. A missed (rejected) signal, not an absent one.
- **Rebate liability understatement (account level)** — signal NOT in the
  information set. No rebate-accrual tag pre-cutoff in the sealed facts;
  AccruedMarketingCostsCurrent appears first post-cutoff (§3).
  `analysis/error_analysis.md` §1 records this coexisting partial classification
  (i) — decisive account-level evidence absent from the numeric input space,
  pre-attributed DATA(design), D-series J10 (XBRL tag resolution); that note
  names the payload's `AccruedLiabilitiesCurrent` aggregate, while the sealed
  facts show no pre-cutoff accrual breakout under either name — same
  conclusion, source-level discrepancy flagged in §7.
- **SG&A misclassification (Canada/France/Germany)** — faint signal in the set,
  not surfaced in either frame: SG&A +1.3% on revenue −10.4% is directionally
  right, but the order's amounts (~$14M + $24M + $8.5M + ~$10M, FY2010-2011) are
  ~2% of the consolidated SG&A base; detectability is a §7 judgment question.
- **Chronology/offering nexus** — in the set, inverted in the main frame: the
  recast-8-K + April 2011 offering sequence (¶55-56) was flagged only in the
  perturbed frame; the main frame read the same chronology as mitigating.

## 6. ERROR TAXONOMY

Outcome is FN; `scoring/error_taxonomy.md` buckets, atlas vocabulary:

- **Interpretation** (primary): `analysis/error_analysis.md` §1 classifies T07
  as "분류 (ii): 증거 존재, 추론이 정체 사전확률에 꺾임" — evidence present,
  reasoning bent by the identity prior — with partial (i) for the buried
  liability account (§5). Under the R1→R3 order the margin-signal discharge
  passes R1 (signal in provided data) and R2 (band rubric unambiguous at 28 vs
  ≥50) → MODEL; the liability-account leg is DATA(design) per J10.
- **Computation / Retrieval**: none found — values spot-verified at
  value+date+accession level against `~/aaer-data/MON/xbrl/CIK0001110783.json`
  (allowance $217M→$111M series; AR $1,590M/$2,377M; FY revenue/gross-profit
  figures; §3). The perturbed grade's auditor flag — 193810011.85 appearing as
  both 2010-08-31 allowance and Q4 FY2010 NetIncomeLoss — resolves as coincident
  source values (allowance $143M at 2010-08-31; NetIncomeLoss −$143M for
  2010-06-01 to 2010-08-31, accn 0000950123-10-096537), not a copy artifact.
- **Label-noise**: none — AAER-confirmed; settled order, company "penalty of
  $80,000,000" (§IV.K).
- **Suspected-memorization — both sealed draws agree: not recognized**: Draw 1
  (`scoring/probe_results/recognition/case_06.json`): company_guess "unknown",
  confidence "low". Draw 2 (`analysis/name_probe_results.json`, row case_06):
  guess "unknown", confidence "low", recognized: false. No cross-draw
  disagreement (L-5: verdicts can vary; here they concur).
  memorization_suspect_condition2: false in both grade records — no post-cutoff
  facts cited in either frame. The identity effect ran through the *provided*
  name in the main frame, not recognition of masked numbers: with the name, the
  model imported "well-known … Roundup" context and scored 28; masked, the same
  signals scored 58 (D8 delta +30). Familiarity acted as an exonerating prior —
  the opposite sign from a recognition-boosted hit.

## 7. CPA JUDGMENT — human_finalized: false

Draft, unaudited work product until owner sign-off (PROJECT.md §7).

- The discharge fails on its own accounting terms: real price pressure and
  improper rebate accounting are not alternatives. Under ASC 605-50 the
  question is not *why* margins fell but *when and where* the rebate
  obligations belonged; a margin trajectory shaped by deferred/reversed rebate
  accruals looks exactly like known pricing pressure arriving one year late.
  Treating a plausible business explanation as dispositive, without testing
  cost-recognition timing, is the analytical error. **[OWNER REVIEW]**
- Empty `mechanism_hypotheses` at score 28 is within-rubric (no hypothesis
  required below 40), so the FN is a confidence-setting outcome, not a rubric
  artifact; the perturbed frame shows the same numeric record supporting 58
  with three hypotheses — the binding constraint was the prior, not the
  evidence. **[OWNER REVIEW]**
- Frame-dependence direction: identity knowledge lowered this treatment score
  (+30 masked), where `analysis/error_analysis.md` §2 notes HTZ moved opposite
  (Δ −30.2, imprinted-guilty). Proposed reading: familiarity priors are
  bidirectional score contamination; this FN is the exculpatory arm.
  **[OWNER REVIEW]**
- Attribution split proposed: margin-signal discharge = MODEL; rebate-liability
  invisibility = DATA(design) per J10. The §5 source-level discrepancy
  (`AccruedLiabilitiesCurrent` named in error_analysis vs no pre-cutoff accrual
  breakout in sealed facts) needs owner confirmation against the deck payload
  before the DATA leg is finalized. **[OWNER REVIEW]**
- The SG&A leg (~2% of base) is proposed as below stand-alone detectability
  from consolidated XBRL — not chargeable to the model — but this is a
  materiality-threshold judgment. **[OWNER REVIEW]**

## 8. AUDIT TRANSLATION

Procedures the §3 signals would motivate (procedures, not conclusions):

- Confirmations with major distributors/retailers of incentive-program terms —
  rebate rates, volume targets, clawbacks, waivers, oral or written side
  agreements — reconciled to recorded rebate accruals.
- Rebate-accrual recomputation under ASC 605-50 (systematic allocation to
  incentivized revenue); cutoff testing of Q4 volume surges against program
  communication dates.
- Period-end accrual-reversal testing: corroborate the asserted basis (missed
  targets) against contemporaneous customer correspondence and subsequent
  payments to the same customers.
- Vendor-consideration classification testing: identifiable-benefit and
  fair-value evidence for SG&A-classified payments (ASC 605-50-45), comparing
  program budgets to amounts credited back to customer accounts.
- Product-line gross-margin analytics against price actions and channel
  inventory; quarter-end receivables/prepayment analytics in
  incentive-payment quarters.

## 9. FINANCIAL STATEMENT IMPACT

From the enforcement text actually read (33-10037.pdf.txt): FY2009 revenues and
gross profits overstated "by approximately $44.5 million when it deferred
recording these liabilities" to FY2010 (¶33), on top of the $57.3M LTA accrual
reversal boosting FY2009 "reported revenues" and gross profit (¶24).
Restatement allocations per the order's footnotes: $24M "additional rebate
costs during fiscal year 2009" for the LBP (fn.9); "Earnback rebates in fiscal
year 2009 and approximately $41 million in fiscal year 2010." with ~$20M in
FY2009 (fn.12); "In its Restatement, Monsanto recorded the $48 million as a
reduction of revenue in fiscal year 2010." (fn.13); "Monsanto did not address
the LBP Canada in its Restatement." (fn.14). SG&A misclassification: Canada
~$14M FY2010 (¶49), France/Germany budgets $24M/$8.5M FY2010, Germany ~$10M
FY2011 (¶51-52) — SG&A overstated, revenue not correspondingly reduced,
boosting Roundup gross profit (¶1). Consolidated: earnings and Roundup-line
revenues/earnings materially misstated FY2009-2011; FY2009 consensus EPS met as
a result (¶2). "On November 14, 2011, Monsanto restated its 2009 and 2010
annual reports on" Form 10-K and its FY2011 10-Qs (¶3). Full restated
per-line-item, per-period amounts: not determinable — the sealed order does not
tabulate them, and no restatement filing text is among the sealed sources read.

---
*Entry status: drafted (sections 7–9 pending owner finalization).*
*채점: Claude 보조 + 인간 최종 확정. 교육·정보 목적, 투자 자문 아님.*
