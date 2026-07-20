# atlas/case_40.md — Tangoe, Inc. (TNGO) — wave-2 treatment T22

Authored by Claude Code, pending human audit (D15). Analytical document under D106 ② — not a scored output. 본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).

## 1. CASE HEADER

| field | value |
|---|---|
| Case ID (anonymized frame) | case_40 (scoring ID T22) |
| Cohort | wave-2 |
| Outcome class | TP (main frame, flag at score ≥50) |
| Ground-truth tier | AAER-confirmed (LR-24255; SEC v. Tangoe, Inc. et al., 3:18-cv-01479 (D. Conn.)) |
| Frozen score | score 55 (`runs/wave2/scores/case_40.json`, run `original-case_40-r1`) |
| Grade record | `scoring/grades_wave2/case_40.json` (human_finalized: true, finalized 2026-07-09 via RP-13 workbench) |
| Company | Tangoe, Inc., CIK 0001182325, cutoff 2016-03-06 (`data/candidates/candidates_wave2.json` T22; `data/evaluatee/cases_wave2.json` case_40) |

## 2. ACTUAL EVENT

SEC v. Tangoe, Inc., Subbloie, Martino, Farias, and Beach, Case No. 3:18-cv-01479
(D. Conn., filed September 4, 2018); Litigation Release No. 24255 (September 4, 2018).
Sealed local texts: `~/aaer-data/TNGO/comp24255.pdf.txt` (complaint) and
`~/aaer-data/TNGO/lr-24255.html.txt` (manifest-pinned,
`data/manifests/aaer_data_manifest.json`).

Per the complaint, Tangoe "misstated the existence and/or timing of approximately
$40 million in revenues, out of total revenues of $566 million previously reported"
"from 2013 through the third quarter of 2015" (comp24255.pdf.txt ¶3). ¶5 enumerates
seven violations: "counting customers' prepayments for future services as current
revenue"; "improperly recording a loan from a business partner as revenue"; revenue
"in the wrong reporting periods"; premature contingent-fee revenue; "recording
revenue from customers who were unlikely to pay"; "violating the accounting rules
for bad debt reserves"; and prematurely "counting revenue from long-term contracts"
with ongoing obligations. Farias "fabricated, forged and altered various business
records, including records that were provided to Tangoe's auditors" (¶6). The 8-K
announcing that FY2013–Q3-2015 financial statements could "no longer be relied on"
was filed March 7, 2016, one day after the case cutoff (¶92).

Registered summary (`data/candidates/candidates_wave2.json`, T22 `scheme_summary`)
matches the above allegations; `scheme_type`: revenue_recognition +
document_forgery; manipulation period 2013-01 to 2015-09.

GAAP topics: revenue recognition for 2013–2015 fiscal periods — pre-ASC-606 era,
stated as such. The complaint recites Tangoe's policy of recognizing revenue "when
persuasive evidence of an arrangement exists, pricing is fixed or determinable,
collection is reasonably assured, and delivery or performance of service has
occurred" (¶25) — the four pre-ASC-606 (SAB Topic 13 era) criteria — plus bad-debt
reserve adequacy (¶68, ¶73); it cites no ASC sections.

## 3. SIGNALS AVAILABLE PRE-CUTOFF

Cutoff 2016-03-06. Sealed data basis: `~/aaer-data/TNGO/edgar/CIK0001182325.json`
(filing chronology) and `~/aaer-data/TNGO/xbrl/CIK0001182325.json` (XBRL company
facts). Pre-cutoff, at accession level:

- **Receivables outrunning revenue**: AccountsReceivableNetCurrent $43,273K
  (2013-12-31) → $56,948K (2014-12-31, +31.6%) vs SalesRevenueServicesNet $188,914K
  → $212,476K (+12.5%) (accn 0001047469-15-002289); AR $60,716K (2015-09-30) with
  Q3 revenue $54,481K → $56,573K (+3.8%) (accn 0001104659-15-077269).
- **Allowance static as receivables more than doubled**:
  AllowanceForDoubtfulAccountsReceivableCurrent $245K (2010-12-31) → $102K
  (2011-12-31, both accn 0001047469-12-003496), still $102K at 2012-09-30 while AR
  grew $14,295K → $25,311K → $33,223K (2012-09-30 accn 0001104659-12-077974).
- **Net income vs operating cash flow**: FY2012 NetIncomeLoss $3,038K vs operating
  cash flow $16,688K; FY2013 $4,962K vs $21,413K; FY2014 $2,936K vs $19,546K (accn
  0001047469-15-002289) — OCF consistently above NI (a benign direction; see §6).
- **2015 swing to losses**: NetIncomeLoss +$252K Q1-2015 (accn 0001104659-15-036841),
  -$2,536K Q2-2015 (accn 0001104659-15-058230), -$4,502K Q3-2015 (accn
  0001104659-15-077269); OperatingIncomeLoss $938K / -$1,977K / -$3,584K (same accns).
- **Filing chronology**: 10-K/A filed 2012-04-26 (accn 0001047469-12-004775); 8-K/A
  filed 2012-03-05, 2012-10-24, 2015-08-14; no NT 10-K/NT 10-Q pre-cutoff — the first
  NT 10-K (2016-03-15) and the non-reliance 8-K (2016-03-07, accn 0001104659-16-102988)
  fall after the cutoff (`~/aaer-data/TNGO/edgar/CIK0001182325.json`, filings.recent).

This section describes the information set — it does not re-score the case.

## 4. WHAT THE LLM CAUGHT

Frozen output `runs/wave2/scores/case_40.json`: `misstatement_probability`: 55
(legacy v1 key — an uncalibrated ordinal score; see specs/RISK_SCORE_SEMANTICS.md)
= score 55, risk_tier "watch"; CL1 (AR vs revenue), CL3 (NI vs OCF), CL6 (allowance
decline) flagged. Checklist evidence re-verified against sealed XBRL at
value+date+accession level: all values genuine; one mis-attribution in CL2 (§6).

| model claim (verbatim) | enforcement/restatement reference | match quality |
|---|---|---|
| "Potential premature or aggressive revenue recognition (e.g., billing ahead of service delivery, extended customer payment terms, or channel-stuffing) combined with an under-provisioned bad debt allowance, causing accounts receivable and revenue to be overstated relative to collectible amounts" (hypothesis 1, direction "overstated") | comp24255.pdf.txt ¶5: premature/uncollectible revenue categories incl. "recording revenue from customers who were unlikely to pay" and "violating the accounting rules for bad debt reserves"; ¶59: "recognizing revenue for Bill Audit services as soon as Tangoe sent an analysis to the customer" | exact mechanism |
| "Accounts receivable growing materially faster than revenue in FY2014 (31.6% vs 12.5%) and Q3 2015 (16.3% vs 3.8%)" (top_signals 1) | ¶67: revenue recognition practices produced an ever-growing "backlog of unpaid bills, sums that had already been counted as revenue but that were now carried on the company's books as 'receivables.'" | exact mechanism |
| "Bad debt reserve/allowance for doubtful accounts was reduced or held flat while receivables grew rapidly (2010-2012), likely understating bad debt expense and overstating net income" (hypothesis 2, direction "understated") | ¶73: Beach recommended Martino "increase its bad debt reserve" at various times during 2014–2015; Martino rejected the advice, reserve left unchanged. Same account and direction, but the sealed complaint locates the reserve violations in 2014–2015, not 2010–2012 (manipulation period registered 2013-01 to 2015-09) | exact mechanism |
| "Abrupt swing from consistent quarterly profitability (2013-early 2015) to sizable losses in Q2 and Q3 2015, potentially reflecting one-time charges, write-offs, or catch-up adjustments related to previously recognized revenue/receivables" (hypothesis 3, "timing_shift") | ¶90–91: internal investigation began after an August 17, 2015 demand letter; ¶95: in nine straight quarters Q1-2013 through Q1-2015 Tangoe "falsely claimed" profitability. No allegation that the Q2–Q3 2015 reported losses were catch-up adjustments | right direction only |

Notes: row 1 matches the mechanism family but pinpoints no case-specific fact (no
prepayments-as-revenue, loan-as-revenue, contingent-fee, or forgery detail) —
consistent with grade DIM2=2, not 3, whose rationale also records row 3's period
misplacement ("places it in 2010-2012, before the 2013-01 manipulation start")
(`scoring/grades_wave2/case_40.json`).

## 5. WHAT THE LLM MISSED

From the sealed §3 information set: none identified — the frozen checklist surfaced
the receivables/revenue divergence, allowance stasis, 2015 loss swing, and
amendment-only chronology. The loan-as-revenue, prepayment round-trip, and
document_forgery legs (`candidates_wave2.json` T22; comp24255.pdf.txt ¶¶27–48,
74–89) have no distinct footprint in the sealed XBRL/chronology data — insufficient
sealed evidence to name a missed signal for those legs.

## 6. ERROR TAXONOMY

Outcome is TP; taxonomy applies to residual grading gaps (`scoring/error_taxonomy.md`
buckets, atlas vocabulary). `analysis/error_analysis_wave2_holdout.md` does not
mention this case — no FP/FN context to import.

- **Computation / Retrieval**: one mis-attribution in unflagged CL2 — the 2013-12-31
  Goodwill $65,963K and IntangibleAssetsNetExcludingGoodwill $36,637K values are
  attributed to accn 0001104659-15-077269, but the sealed facts file carries them
  only under FY2013/FY2014-era filings (e.g., accn 0001047469-14-002521). Values
  genuine; CL2 was no_flag, so no outcome effect.
- **Interpretation**: (a) CL3 flags an NI-vs-OCF "divergence" in which OCF exceeds
  NI every year — directionally the benign pattern, noted as a weakness in the grade
  rationale ("does not defeat the score"). (b) Hypothesis 2 places the bad-debt
  under-reserving in 2010–2012, before the registered 2013-01 manipulation start (§4
  row 3). (c) DIM2=2 not 3: no case-specific pinpointed fact named. All MODEL-bucket
  under the R1→R2→R3 rules. DIM3 is unscored: mapped_genre "mixed", score null —
  answer-key genre_tag_row is null, deferred to the human auditor.
- **Label-noise**: none — AAER-confirmed tier; settled action, with Tangoe, Subbloie,
  Martino, and Beach agreeing to civil penalties of $1.5 million, $100,000, $50,000,
  and $20,000 respectively (lr-24255.html.txt, final ¶, line 1089).
- **Suspected-memorization**: no. Recognition probe — the single stored draw
  `scoring/probe_results_wave2/recognition/case_40.json` — guessed "ExamWorks
  Group, Inc.", confidence "medium" (wrong company); verbatim probe
  `.../verbatim/case_40.json` returned known: false; grade record
  memorization_suspect_condition2: false ("mentions no post-cutoff facts").

## 7. CPA JUDGMENT — human_finalized: false

Draft, unaudited work product until owner sign-off (PROJECT.md §7).

- Right flag for substantially the right accounting reason: AR/revenue divergence
  plus a static allowance is the balance-sheet residue the complaint itself
  describes — improperly recognized revenue piling up as an unpaid-bill backlog
  "carried on the company's books as 'receivables'" (¶67) while management refused
  reserve increases (¶73). **[OWNER REVIEW]**
- Crediting §4 row 3 as "exact mechanism" despite the 2010–2012 vs 2014–2015 period
  misplacement is a judgment call: same account, direction, and violation family,
  wrong window; a stricter reading would demote it. **[OWNER REVIEW]**
- CL3 is a reasoning blemish — OCF exceeding NI is the benign configuration;
  whether it should have moved DIM4 off 3 is an owner call. **[OWNER REVIEW]**
- Score 55 sits in the lowest flagged band (DIM1=1) with DIM4=3 evidence. The
  quantitatively quiet legs (loan-as-revenue, forgeries, prepayment round-trips)
  are invisible in XBRL, so "watch"-tier hesitance is defensible; under-confidence
  vs appropriate calibration is an owner call. **[OWNER REVIEW]**

## 8. AUDIT TRANSLATION

Procedures the flag would motivate (framed as procedures, not conclusions):

- AR confirmations, including disputed, split, and re-issued invoices; aging with
  subsequent cash-receipts testing on the FY2014–Q3-2015 build.
- Contingent-fee revenue testing: agree recognition dates to third-party
  confirmations (carrier credits, state recoveries), not internal estimates.
- Revenue cutoff testing at quarter-ends: invoices issued on the final day of the
  quarter; credits to the same counterparty in following periods (round-trip/
  prepayment indicators).
- Examine large period-end receipts from business partners: amendments near or
  after the receipt date, repayment terms, revenue-vs-financing classification.
- Recompute the bad-debt reserve against an AR aging; review finance-group
  communications for rejected reserve-increase recommendations and workouts
  (free future services in lieu of credit memos).
- Confirm customer approvals supporting revenue directly with the customer, not
  via forwarded email chains (document-integrity procedures).

## 9. FINANCIAL STATEMENT IMPACT

Determinable from the sealed complaint's reproduction of Tangoe's Form 12b-25
(filed 2016-11-10) unaudited estimates (comp24255.pdf.txt ¶93), $ millions:

| line item ($M) | FY2013 | FY2014 | FY2015 (YTD Q3) | Total | direction |
|---|---|---|---|---|---|
| Revenue (previously reported) | 188.9 | 212.5 | 164.5 | 565.9 | — |
| Revenue (restated, proposed) | 179.6 (-5.2%) | 198.3 (-7.2%) | 157.5 (-4.4%) | 535.4 (-30.5) | revenue overstated |
| Pre-tax net income (previously reported) | 6.0 | 5.3 | (4.9) | 6.4 | — |
| Pre-tax net income (restated, proposed) | (2.7) | (9.6) | (12.3) | (24.6) | income overstated |

Of the estimated $30.5M revenue reduction, ~$14.0M was "a permanent reduction in
revenue" with the $16.5M balance from timing; later internal workpapers showed ~$40M
"either reversed or re-timed in the proposed restatement" (¶94). Restatement turned
all nine quarters Q1-2013 through Q1-2015 from reported profits to pre-tax losses
(¶95). Final audited restatement amounts: not determinable from the sealed sources
read — the complaint records NASDAQ delisting on March 14, 2017 for "inability to
make required Commission filings" (¶17); no audited restated filing is in the sealed set.

---
*Entry status: drafted (sections 7–9 pending owner finalization).*
*채점: Claude 보조 + 인간 최종 확정. 교육·정보 목적, 투자 자문 아님.*
