# atlas/case_12.md — The Kraft Heinz Company (KHC) — wave-1 treatment T28

Authored by Claude Code, pending human audit (D15). Analytical document under D106 ② — not a scored output. 본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).

## 1. CASE HEADER

| field | value |
|---|---|
| Case ID (anonymized frame) | case_12 (scoring ID T28) |
| Cohort | wave-1 |
| Outcome class | TP (main frame, flag at score ≥50) |
| Ground-truth tier | AAER-confirmed (AAER-4248 / Securities Act Rel. 33-10977 / Exchange Act Rel. 34-92874, File 3-20523) |
| Frozen score | score 68 (`runs/main/case_12.json`, run `original-case_12-r1`); perturbed frame score 68 (`runs/perturbed/case_12.json`, run `perturbed-case_12-r1`) |
| Grade record | `scoring/grades/main/case_12.json` and `scoring/grades/perturbed/case_12.json` (human_finalized: true, RP-09 Stage 0, commit 986a893, 2026-07-07) |

Company: The Kraft Heinz Company, CIK 0001637459, cutoff 2019-02-20
(`data/candidates/candidates.json` T28; `data/evaluatee/cases.json` case_12).
Perturbation delta: score 68 → 68 (Δ 0). Per D8 the delta measures memorization
contribution — not a robustness pass/fail; here the identity-masked, rescaled
frame reproduced the identical score and the same "elevated" tier, so the flag
did not depend on the provided name. Both frames are TP at threshold 50 —
`analysis/error_analysis.md` §2 seats KHC among the six detections with the
annotation "점수는 맞고 기제는 틀림" (score right, mechanism wrong; d2=0).

## 2. ACTUAL EVENT

SEC Corrected Order, In the Matter of The Kraft Heinz Co. and Eduardo
Pelleissone, Securities Act Rel. 33-10977 / AAER-4248 (Sept. 3, 2021), settled.
Sealed local text: `~/aaer-data/KHC/33-10977.pdf.txt` (manifest-pinned,
`data/manifests/aaer_data_manifest.json`).

Per the Summary: a "multi-year expense management scheme" by KHC's
"procurement division to improperly reduce KHC’s cost of goods sold" that
"resulted in KHC reporting inflated earnings" before interest, taxes,
depreciation and amortization, "a key performance metric for investors" (¶1).
From Q4 2015 through end of 2018 (the "Relevant Period"), procurement
employees obtained upfront supplier payments and discounts tied to future
commitments while documenting them so as to "prematurely and improperly
recognize the expense savings" (¶1), and "maintained false and misleading
supplier contracts" presenting the savings as earned by past or same-year
events (¶2). Transaction types (¶13): "Prebate Transactions", "Clawback
Transactions", and "Price Phasing Transactions". Of the 295 transactions KHC
ultimately corrected, ~59 were part of the procurement misconduct; properly
accounted, cost of goods sold would have been approximately "$50 million
higher than reported." (¶3). In June 2019 KHC restated: it "corrected a total
of $208 million in cost savings" from 295 transactions and "also corrected its
Adjusted EBITDA" (¶4); 54 of the ~59 procurement transactions were
"manipulated" in 2017-2018 (¶23). GAAP topic: ASC 705-20 (vendor
consideration) — cash consideration contingent on future purchases must be
"recognized as a reduction of the cost of sales" on a systematic and rational
allocation (fn.2); savings given "in exchange for future commitments over the
period of time that KHC performed" them (¶14). KHC reported the related
"material weakness in its annual report on Form 10-K filed on June 7, 2019."
(¶34). Company civil penalty $62,000,000 (§IV.B); Pelleissone $300,000 penalty
plus disgorgement (§IV.D).

Registered summary (`data/candidates/candidates.json` T28 `scheme_summary`):
"improperly/prematurely recognized unearned supplier discounts and rebates
(prebate, clawback and price-phasing transactions)" with false supplier
contracts, understating COGS and inflating adjusted EBITDA; `scheme_type`
other + liability_understatement; manipulation period 2015-10-01 to
2018-12-31; first revelation 2019-02-21 (Q4-2018 earnings release: write-down,
dividend cut, SEC subpoena disclosure), cutoff 2019-02-20.

## 3. SIGNALS AVAILABLE PRE-CUTOFF

Cutoff 2019-02-20. Sealed basis: `~/aaer-data/KHC/xbrl/CIK0001637459.json` and
`~/aaer-data/KHC/edgar/CIK0001637459.json`. Pre-cutoff, as-reported, at
accession level (all cited facts filed ≤ 2019-02-20):

- **2018 receivables ramp**: AccountsReceivableNetCurrent $1,044M (2018-03-31,
  10-Q accn 0001637459-18-000099, filed 2018-05-03) → $1,950M (2018-06-30,
  accn 0001637459-18-000116) → $2,032M (2018-09-29, accn 0001637459-18-000124)
  against quarterly SalesRevenueGoodsNet $6,304M → $6,686M.
- **NI/OCF divergence**: FY2017 NetIncomeLoss $10,999M (of which Q4 2017
  $8,003M) vs NetCashProvidedByUsedInOperatingActivities $527M (10-K accn
  0001637459-18-000015). FY2016 OCF appears as $5,238M in the FY2016 10-K
  (accn 0001637459-17-000007) but $2,649M in the FY2017 10-K's comparative —
  a presentation inconsistency inside the information set.
- **Allowance decline**: AllowanceForDoubtfulAccountsReceivableCurrent $32M
  (2016-01-03) → $20M (2016-12-31, accn 0001637459-17-000007); no allowance
  tag appears for any later period pre-cutoff.
- **Chronology**: two 10-Q/A amendments for Q1 and Q2 2017 (accns
  0001637459-17-000116 / -000117) filed 2017-11-07, the same day as the
  original Q3 2017 10-Q (accn 0001637459-17-000118).
- **COGS side (the truth mechanism's account)**: CostOfGoodsSold is present
  (49 pre-cutoff facts); GrossProfit $9,586M FY2016 → $9,703M FY2017 on
  revenue $26,487M → $26,232M (accn 0001637459-18-000015) — margin stable to
  slightly rising while the post-merger cost-savings strategy was, per the
  order, publicly touted (¶9). No vendor-consideration / rebate / supplier
  tag of any kind exists in the sealed company facts. The corrected amount
  ($208M across FY2015-Q3 FY2018) is ~0.4% of one year's COGS (~$16.9B).

This section describes the information set — it does not re-score the case.

## 4. WHAT THE LLM CAUGHT

Frozen output `runs/main/case_12.json`: `misstatement_probability`: 68 (legacy
v1 key — an uncalibrated ordinal score; see specs/RISK_SCORE_SEMANTICS.md) =
score 68, risk_tier "elevated"; CL1/CL3/CL4/CL6/CL7 flagged, CL8
insufficient_data; three mechanism hypotheses. Quotes grep-verified in the
frozen outputs; values verified against the sealed XBRL.

| model claim (verbatim) | enforcement/restatement reference | match quality |
|---|---|---|
| "Potential premature revenue recognition, extended customer payment terms, or use of receivables factoring/securitization not matched by a corresponding rise in bad-debt reserves" (top hypothesis, direction "overstated") | Order alleges a procurement-side COGS scheme (¶1-3); no revenue, receivables, or factoring allegation appears in 33-10977.pdf.txt | unrelated |
| "bad-debt reserves may not have kept pace with receivables growth, understating the allowance and overstating net receivables" (hypothesis 2) | No allowance/receivables allegation in the order | unrelated |
| "raises questions about the timing and accuracy of interim tax and other accrual entries during 2017" (hypothesis 3, direction "timing_shift") | Truth is premature (timing) recognition of cost savings, concentrated 2017-2018: 54 of ~59 transactions "manipulated" then (¶23) — timing genre overlaps, accounts do not | right direction only |
| "Two 10-Q/A restatements of Q1 and Q2 2017 filed on the same date as the Q3 2017 10-Q" (top_signals[1], CL7) | The order narrates only the June 2019 restatement (¶4, ¶34); it is silent on the 2017-11-07 amendments | unrelated |

Main-frame grades: DIM1=1 (score 68 in the 50-70 band), DIM2=0 (rationale:
top hypothesis targets "unrelated accounts (revenue/AR side, not
COGS/supplier rebates)"; coverage note — "no hypothesis touches the true
mechanism"), DIM3 mapped "mixed" = 1 vs key genre active(cost), DIM4=3.
Perturbed frame: score 68, "elevated", top hypothesis "Possible premature
revenue recognition, extended customer credit terms, or channel stuffing" —
DIM1=1, DIM2=0, DIM3 mapped "active" = 2 (genre-level match despite wrong
account), DIM4=3. The two frames flag the same core signals on rescaled
values; the only checklist-level divergence is CL2/CL4/CL8 (no_flag/flag
swaps on soft assets, inventory, and data sufficiency).

## 5. WHAT THE LLM MISSED

From the sealed §3 information set, against the truth mechanism (COGS
understatement via supplier prebates/clawbacks/price phasing):

- **Account-level rebate signal — NOT in the information set**: no
  vendor-consideration, rebate, supplier, or incentive tag exists anywhere in
  the sealed company facts (§3), and the order locates the falsity in contract
  documentation given to controllers (¶2, ¶13) — invisible at XBRL
  granularity. Absence is a world fact of the public data, not a
  collection/build defect (taxonomy R1 branch).
- **Margin trace — in the set, read as unremarkable**: the model quoted the
  exact GrossProfit series and concluded "margins stable ~36-37%" (CL4
  evidence). In hindsight the stability-on-flat-revenue is the direction the
  scheme pushed (savings inflating EBITDA, ¶1), but at ~0.4% of annual COGS
  (§3) the sealed evidence cannot isolate it; classing this as "missed" would
  overstate detectability — see §7.
- No other truth-mechanism footprint identified from sealed evidence.

`analysis/error_analysis.md` §4 records the flag's decisive evidence as the
2018-05 / 2018-08 10-Qs, 3q/2q before revelation — annotated "d2=0 — 틀린
기제의 조기성" (earliness of a wrong mechanism).

## 6. ERROR TAXONOMY

Outcome is TP at threshold; the recorded error is dimension-level — DIM2=0 in
both frames (`scoring/grades/{main,perturbed}/case_12.json`). Buckets per
`scoring/error_taxonomy.md`, atlas vocabulary:

- **Interpretation (with a data-limit caveat)**: the score rests on
  revenue/AR and tax-timing narratives with no counterpart in the order —
  `analysis/error_analysis.md` §2: "동상 — 매출/AR 서사; 정답은 조달 COGS
  스킴"; §3 counts KHC in the cost/rebate stratum (MON·KHC, detected 1/2).
  Under R1→R3, the truth-mechanism signal was absent from the provided data
  as a world fact (R1 pass-through), so charging the wrong mechanism to the
  model as pure MODEL/interpretation is contestable — flagged in §7 rather
  than finalized here.
- **Computation / Retrieval**: none found — every cited value spot-verified
  at value+date+accession level against `~/aaer-data/KHC/xbrl/CIK0001637459.json`
  (AR $1,044M/$1,950M/$2,032M; FY2017 NI $10,999M vs OCF $527M; allowance
  $32M→$20M; the 2017-11-07 amendment accessions; §3).
- **Label-noise**: none — AAER-confirmed, settled order; company penalty
  $62,000,000 (§IV.B).
- **Suspected-memorization — both sealed draws agree: recognized**: Draw 1
  (`scoring/probe_results/recognition/case_12.json`): company_guess "The
  Kraft Heinz Company", confidence "high". Draw 2
  (`analysis/name_probe_results.json`, row case_12): guess "The Kraft Heinz
  Company", confidence "high", recognized: true. No cross-draw disagreement
  (L-5: verdicts can vary; here they concur). memorization_suspect_condition2:
  false in both grade records — neither frame cites post-cutoff facts (no
  mention of the June 2019 restatement, the $208M correction, or the SEC
  order), and the D8 delta is 0: the masked frame reproduced score 68, so
  recognition of the identity added no measurable score contribution.

## 7. CPA JUDGMENT — human_finalized: false

Draft, unaudited work product until owner sign-off (PROJECT.md §7).

- This TP is a right-score/wrong-reason hit. The 2018 AR ramp the model built
  its top hypothesis on has no counterpart in the order; the scheme lived in
  vendor consideration (ASC 705-20) — supplier payments recognized before the
  future commitments they purchased were performed. A flag that triggers
  audit attention is operationally useful, but its mechanism content would
  have pointed fieldwork at the wrong account. **[OWNER REVIEW]**
- Detectability: ~$50M of improper COGS reduction attributable to the 59
  transactions (¶3), $208M total corrections, against ~$16.9B annual COGS —
  roughly 0.4% per year at consolidated granularity, with no rebate-accrual
  disclosure line pre-cutoff. Proposed reading: DIM2=0 here reflects an
  information-set limit at least as much as a model shortfall; the mechanism
  was arguably not inferable from the sealed numeric inputs. **[OWNER REVIEW]**
- The §4 enum call for hypothesis 3 ("right direction only" on the timing
  genre) is a judgment; the grade rationale's coverage note reads all three
  hypotheses as missing COGS/rebates entirely, which would support
  "unrelated" instead. **[OWNER REVIEW]**
- Identity effect: name recognized at high confidence in both draws, yet
  Δ = 0 across frames — contrast MON (Δ +30, exculpatory prior) and HTZ
  (Δ −30.2, imprinted-guilty; `analysis/error_analysis.md` §2). Proposed
  reading: for KHC the score was signal-driven in both frames; recognition
  neither helped nor hurt the number, though it did not supply the true
  mechanism either — a data point against treating recognition alone as
  score contamination. **[OWNER REVIEW]**
- The FY2016 OCF presentation split ($5,238M vs $2,649M for the same period
  across consecutive 10-Ks, §3) was not surfaced by the model in either
  frame; whether it was a reasonably expectable catch from the payload is a
  judgment call. **[OWNER REVIEW]**

## 8. AUDIT TRANSLATION

Procedures the flag and the §3 signals would motivate (procedures, not
conclusions):

- Supplier confirmations of rebate/prebate/discount terms — including
  contract extensions, future volume commitments, clawback and repayment
  provisions, and side arrangements — reconciled to the contract
  documentation provided to the controller group.
- Vendor-consideration recomputation under ASC 705-20: recognition period of
  each material supplier credit tested against the commitment period; recompute
  amortization of upfront payments tied to multi-year contracts.
- Price-trend testing for phasing: pair each in-year supplier price decrease
  with subsequent price increases from the same supplier to detect offsetting
  structures that net to zero savings.
- Journal-entry testing of period-end and post-close rebate entries,
  including changes to previously determined deferral treatments made after
  the books closed.
- Fraud-risk-factor evaluation of procurement incentive structures
  (savings-linked targets and bonuses) and of sub-certification /
  disclosure-committee sign-off controls.
- Receivables procedures for the model's own top signal: confirmations,
  factoring/securitization terms, and allowance recomputation for the 2018
  balances.

## 9. FINANCIAL STATEMENT IMPACT

From the enforcement text actually read (33-10977.pdf.txt): cost of goods
sold understated — had the ~59 procurement transactions been properly
documented and accounted for, COGS during the Relevant Period "would have
been approximately" "$50 million higher than reported." (¶3). The June 2019
restatement "corrected a total of $208 million in cost savings" arising from
295 transactions and "also corrected its Adjusted EBITDA" (¶4). Restatement
scope: financial data for FY2015 and the financial statements in the Forms
10-Q and 10-K for FYs 2016-2017 and the first three quarters of FY2018 (¶4);
material weakness reported in the Form 10-K filed June 7, 2019 (¶34).
Per-line-item, per-period restated amounts: not determinable — the sealed
order does not tabulate them, and no restatement filing text is among the
sealed sources read.

---
*Entry status: drafted (sections 7–9 pending owner finalization).*
*채점: Claude 보조 + 인간 최종 확정. 교육·정보 목적, 투자 자문 아님.*
