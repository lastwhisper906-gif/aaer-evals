# atlas/case_02.md — Orthofix International N.V. (OFIX) — wave-1 treatment T11

Authored by Claude Code, pending human audit (D15). Analytical document under D106 ② — not a scored output. 본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).

## 1. CASE HEADER

| field | value |
|---|---|
| Case ID (anonymized frame) | case_02 (scoring ID T11) |
| Cohort | wave-1 |
| Outcome class | TP (main frame, flag at score ≥50) |
| Ground-truth tier | AAER-confirmed (AAER-3845 / Rel. 33-10281 / 34-79815, File 3-17791) |
| Frozen score | score 60 (`runs/main/case_02.json`, run `original-case_02-r1`); perturbed frame score 45 (`runs/perturbed/case_02.json`, run `perturbed-case_02-r1`) |
| Grade record | `scoring/grades/main/case_02.json` and `scoring/grades/perturbed/case_02.json` (human_finalized: true, RP-09 Stage 0, commit 986a893, 2026-07-07) |

Company: Orthofix International N.V., CIK 0000884624, cutoff 2013-07-28
(`data/candidates/candidates.json` T11; `data/evaluatee/cases.json` case_02).
Perturbation delta: score 60 → 45 (−15). Per D8 the delta measures memorization
contribution — not a robustness pass/fail. As a recorded fact, the perturbed-frame
score falls below the ≥50 flag band (perturbed grade DIM1=0; main grade DIM1=1).

## 2. ACTUAL EVENT

SEC Order Instituting Cease-and-Desist Proceedings, In the Matter of Orthofix
International N.V., Securities Act Rel. 33-10281 / Exchange Act Rel. 34-79815 /
AAER-3845 (January 18, 2017); "Respondent admits the facts set forth in Paragraphs
1 through 93" (§II). Sealed local text: `~/aaer-data/OFIX/33-10281.pdf.txt`
(manifest-pinned, `data/manifests/aaer_data_manifest.json`).

Per the order (Summary): "From at least 2011 to mid-2013", "Orthofix materially
overstated its distributor revenue and operating income". Legs: (a) contingent
sales with its largest international (Brazilian) distributor, including revenue on
implants that "could not be resold" for lack of instrument sets (~$5M FY2011,
¶25-27) and ANVISA-contingent shipments (over $2M, ¶38; ~$1.5M, ¶50-52); (b)
domestic spinal-stimulation sales "treating certain price discounts as expenses
instead of a reduction to revenue" (Summary; ~$1.7M FY2012, ¶78) plus
right-of-exchange sales (over $650,000 FY2012, ¶81); (c) Brazilian
Orthopedics-subsidiary side agreements (¶83-84); (d) "understated its E&O reserve
by $3.4 million and $5.6 million in FY 2011 and 2012, respectively" (¶91).

Registered summary (`data/candidates/candidates.json`, T11 `scheme_summary`):
materially overstated distributor revenue/operating income via improper recognition
on contingent/return-eligible distributor sales and discounts booked as expense;
`scheme_type`: revenue_recognition (single); manipulation period 2011-01 to
2013-03; first revelation 2013-07-29.

GAAP topics, as cited by the order: ASC 605-10-25-1 (¶9); "sell-in" recognition
upon shipment (¶12); ASC 605-50-45-2 (discounts as price reduction, ¶77); ASC
605-15-25-1(f) (returns not reasonably estimable, ¶80); ASC 330 / ASC 330-10-35-14
(¶90, fn.4). No other ASC topics attributed from sealed evidence.

## 3. SIGNALS AVAILABLE PRE-CUTOFF

Cutoff 2013-07-28 (`data/evaluatee/cases.json`, case_02). Sealed deck basis:
`~/aaer-data/OFIX/xbrl/CIK0000884624.json` (XBRL company facts) and
`~/aaer-data/OFIX/edgar/CIK0000884624*.json` (filing chronology). Pre-cutoff, at
accession level:

- **Receivables outrunning (declining) revenue**: AccountsReceivableNetCurrent
  $132,828K at 2011-12-31 → $150,316K at 2012-12-31 (+13.2%) against SalesRevenueNet
  $470,121K (FY2011) → $462,320K (FY2012), −1.7% (accn 0001193125-13-087561, FY2012
  10-K filed 2013-03-01; AR also in accn 0001193125-13-211276).
- **Allowance build-up**: AllowanceForDoubtfulAccountsReceivableCurrent $7,250K at
  2010-12-31 (accn 0001104659-12-014637) → $9,376K at 2011-12-31 → $16,188K at
  2012-12-31, +72.6% in FY2012 (accns 0001193125-13-087561, 0001193125-13-211276).
- **NI vs OCF inversion**: FY2011 NetIncomeLoss −$1,073K vs
  NetCashProvidedByUsedInOperatingActivitiesContinuingOperations $64,781K; FY2012
  NetIncomeLoss $51,295K vs OCF $11,206K (accn 0001193125-13-087561).
- **Inventory vs revenue/margin**: InventoryNet $82,969K (2011-12-31) → $88,744K
  (2012-12-31), +7.0% against the −1.7% revenue decline; GrossProfit $377,502K
  (FY2011) vs $375,828K (FY2012) — margin expanding on falling revenue (accn
  0001193125-13-087561).
- **Filing-chronology friction**: 10-K/A 2012-05-01 (accn 0001104659-12-031395)
  after the FY2011 10-K of 2012-02-29 (accn 0001104659-12-014637); UPLOAD
  2011-07-12/08-25/09-29 (accns 0000000000-11-042212, -11-051191, -11-057969),
  UPLOAD 2013-06-25 (accn 0000000000-13-034527), CORRESP 2013-07-24 (accn
  0001193125-13-300760); prior-period Goodwill $185,175K at 2009-12-31 per the
  FY2011 10-K vs $73,598K at 2010-12-31 per the FY2012 10-K
  (`~/aaer-data/OFIX/edgar/CIK0000884624*.json`). The revelation 8-K of 2013-07-30
  (accn 0001193125-13-308166) post-dates the cutoff — not in the information set.

This section describes the information set — it does not re-score the case.

## 4. WHAT THE LLM CAUGHT

Frozen output `runs/main/case_02.json`: `misstatement_probability`: 60 (legacy v1
key — an uncalibrated ordinal score; see specs/RISK_SCORE_SEMANTICS.md) = score 60,
risk_tier "elevated"; CL1 (AR vs revenue), CL3 (NI vs OCF), CL4 (inventory/margin),
CL7 (chronology), CL8 (coverage) flagged. Original frame primary; quotes
grep-verified in the frozen output, values verified against the sealed XBRL file.

| model claim (verbatim) | enforcement/restatement reference | match quality |
|---|---|---|
| "Possible premature/aggressive revenue recognition (e.g., channel stuffing to distributors) inflating sales and receivables in FY2012 … followed by a sharp build-up in the bad-debt allowance suggesting subsequent recognition that some of the receivable growth was uncollectible" (hypothesis 1, direction "overstated") | 33-10281.pdf.txt Summary: "Orthofix materially overstated its distributor revenue and operating income"; "entered into contingent sales"; ¶61: "did not adequately assess the collectability of the significant receivables it had with the Brazilian Distributor" | exact mechanism |
| "Accrual-heavy earnings recognition in FY2012 not supported by cash generation … inflate reported net income relative to underlying cash operations" (hypothesis 2, direction "overstated") | Summary: overstated "operating income"; ¶37: "a lot of pressure to reduce our ballooning [Days Sales Outstanding]" — the uncollected contingent sales are the revenue leg, not a distinct accrual scheme | right direction only |
| "Potential under-provisioning for excess/obsolete inventory or capitalization of costs into inventory, allowing gross margin to expand" (hypothesis 3, direction "overstated") | ¶88: reserve reversal "resulted in a $1.2 million gross margin increase in the fourth quarter of FY 2012"; ¶91: "understated its E&O reserve by $3.4 million and $5.6 million in FY 2011 and 2012" | exact mechanism |
| "Filing chronology shows a 10-K/A shortly after the FY2011 10-K, materially restated prior-period Goodwill/Assets/Liabilities figures between the 2012 and 2013 10-Ks, and recurring SEC CORRESP/UPLOAD correspondence through 2013" (overall.top_signals) | No goodwill or divestiture allegation in 33-10281.pdf.txt | unrelated |

Row 1 carries the grade: DIM2=2 both frames — "Account area, direction, and
treatment type substantially match"; not 3 because "no key-pinpointed case-specific
fact is named" and "'distributors' alone is generic … though borderline given the
key's 'distributor revenue' language (flag for auditor)"
(`scoring/grades/main/case_02.json` rationale). Genre "active" vs key
"active(revenue)": exact match, DIM3=2; DIM4=3, both frames. Row 3 is graded
off-scheme ("extraneous but not graded" — single registered scheme_type; see §7).
Perturbed frame (`runs/perturbed/case_02.json`): score 45, risk_tier "watch"; same
top hypothesis on perturbation-scaled values; CL7/CL8 flip to no_flag, CL2 to
insufficient_data.

## 5. WHAT THE LLM MISSED

From the sealed §3 information set: none identified — the frozen checklist and
hypotheses surfaced the AR/revenue divergence, allowance build-up, NI/OCF
inversion, inventory/margin trend, and chronology signals the sealed deck supports.
The scheme's distinguishing features (contingent distributor terms, implants
shipped without instrument sets, discounts booked as expense, Brazilian-subsidiary
side agreements) left no distinct pre-cutoff footprint in the XBRL-only deck —
insufficient sealed evidence to name a missed signal for those legs. Segment-level
Spine revenue, which the order centers on, is not in the sealed deck series.

## 6. ERROR TAXONOMY

Outcome is TP; taxonomy applies to residual gaps (`scoring/error_taxonomy.md`
buckets, atlas vocabulary):

- **Computation / Retrieval**: none found — checklist and hypothesis values verified
  at value+date+accession level against `~/aaer-data/OFIX/xbrl/CIK0000884624.json`
  and the two edgar chronology files (§3).
- **Interpretation**: (a) DIM2=2 not 3 — the case-specific mechanism facts were
  invisible in the XBRL-only deck, so whether the residual gap is DATA or MODEL
  under R1 is an owner call. (b) Cross-frame divergence (60 vs 45) straddles the
  flag band; the perturbed grade records DIM1=0 "despite the fraud being real"
  (`scoring/grades/perturbed/case_02.json` rationale). (c) CL7's goodwill/asset-drop
  reasoning has no counterpart in the order (§4 row 4).
- **Label-noise**: none — AAER-confirmed tier; an admissions order (§II) with an
  $8,250,000 civil money penalty (33-10281.pdf.txt §IV.B).
- **Suspected-memorization**: the two sealed probe draws disagree on the guess
  (L-5: probe verdicts vary across draws) but agree on non-recognition. Draw 1,
  `scoring/probe_results/recognition/case_02.json`: company_guess "unknown",
  confidence "low". Draw 2, `analysis/name_probe_results.json` row case_02: guess
  "Taro Pharmaceutical Industries Ltd.", confidence "medium", recognized: false.
  Both grade records: memorization_suspect_condition2 false. The −15 delta is the
  D8 memorization-contribution measurement; no pass/fail reading is applied.

`analysis/error_analysis.md` context: §2 table — "OFIX | 60 | 2 | 계정·방향·처리유형
실질 일치 (채널 스터핑 가설 vs 조건부 유통사 매출)"; §3 — revenue-recognition cases
4/4 detected; §4 — decisive evidence first/complete at the 2013-03 10-K, 1 quarter
pre-revelation, d2=2.

## 7. CPA JUDGMENT — human_finalized: false

Draft, unaudited work product until owner sign-off (PROJECT.md §7).

- The flag landed for substantially the right reason: distributor revenue
  recognized ahead of collectability, read off DSO divergence plus the allowance
  build-up — telltales the order's own facts echo (¶37 "ballooning [Days Sales
  Outstanding]"; ¶42 allowance at "only $1.6 million (or 40% of accounts receivable
  over 360 days old)" against a full-reserve policy). The grader's DIM2 borderline
  note (2 vs 3) is already flagged for the auditor. **[OWNER REVIEW]**
- Hypothesis 3 (E&O under-provisioning) was graded "extraneous" because the
  registered scheme_type is single revenue_recognition, yet order ¶85-91 describes
  exactly that conduct ($3.4M/$5.6M E&O understatement; $1.2M Q4-FY2012
  gross-margin lift from the FORZA reversal). Whether the single-mechanism answer
  key undercounts this hit is a CRITERIA-side question. **[OWNER REVIEW]**
- Score 60 vs 45 straddles the threshold: TP exists only in the main frame. Per D8
  the −15 delta is memorization-contribution evidence; with both probe draws
  showing non-recognition (unknown/low; Taro/false), the recorded picture is a
  near-band case rather than a recognition-driven one. **[OWNER REVIEW]**
- The CL7 flag partially rests on goodwill/asset swings consistent with a
  divestiture the order never mentions — a right-answer-partly-wrong-evidence
  strand within an otherwise supported flag. **[OWNER REVIEW]**

## 8. AUDIT TRANSLATION

Procedures the flag would motivate (framed as procedures, not conclusions):

- Distributor confirmations of payment terms, contingencies, side agreements, and
  return/exchange rights; compare confirmed terms against the terms used for
  revenue recognition.
- Sell-in vs sell-through analysis; quarter-end cutoff testing of shipments against
  delivery of all interconnected products and regulatory-approval contingencies.
- AR aging and DSO analytics by distributor; recompute the bad-debt reserve against
  the stated aging policy and investigate exceptions.
- Classification testing of wholesaler discounts/commissions (ASC 605-50-45-2);
  E&O reserve recomputation, testing reversals and methodology changes against
  ASC 330-10-35-14.
- Segment margin analytics (Spine vs Orthopedics); inquiry into sales-target
  pressure and approval controls over distributor-term modifications.

## 9. FINANCIAL STATEMENT IMPACT

From the enforcement text actually read (33-10281.pdf.txt): "In late March 2014,
Orthofix restated its financial statements for the first quarter of fiscal year
2013, all quarterly and annual periods in fiscal years 2012 and 2011, and the
annual period for fiscal year 2010" (¶92). Direction and magnitude, as stated:
"overstated – for example – fiscal year 2011 net sales by approximately 6% and
operating income by over 430%" (¶93); revenue overstated "by approximately $1.7
million in FY 2012" from discounts-as-expense (¶78) and "by over $650,000 in FY
2012" from right-of-exchange sales (¶81); ~$5M FY2011 implants-without-instruments
revenue (¶25-26), over $2M summer-2012 Firebird revenue (¶38), ~$1.5M fall-2012
revenue (¶50-52); E&O reserve understated "$3.4 million and $5.6 million in FY 2011
and 2012, respectively" (¶91). Full restated per-line-item, per-period amounts:
not determinable — the sealed order does not tabulate them, and no restatement
filing text is among the sealed sources read.

---
*Entry status: drafted (sections 7–9 pending owner finalization).*
*채점: Claude 보조 + 인간 최종 확정. 교육·정보 목적, 투자 자문 아님.*
