# atlas/case_71.md — Hub Group, Inc. (HUBG) — holdout treatment

Authored by Claude Code, pending human audit (D15). Analytical document under D106 ② — not a scored output. 본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).

## 1. CASE HEADER

| field | value |
|---|---|
| Case ID (anonymized frame) | case_71 |
| Cohort | holdout |
| Outcome class | TP-provisional (main frame, flag at score ≥50; ground truth provisional, see tier row) |
| Ground-truth tier | provisional-4.02/restatement — NOT AAER-confirmed; upgrade monitoring until 2030-02-05 (`analysis/LABEL_REPORT.md` §3, `analysis/label_tags_holdout.json`) |
| Frozen score | score 70 (`runs/holdout/scores/case_71.json`, run `original-case_71-r1`, risk_tier "elevated") |
| Grade record | `scoring/grades_holdout/case_71.json` (human_finalized: true, finalized 2026-07-09 via RP-13 workbench; dim1=2, dim2=1, dim3 mapped_genre "omission-estimate" / score null, dim4=3, memorization_suspect_condition2: false) |

Company: Hub Group, Inc., CIK 0000940942, cutoff 2026-02-04 (`data/evaluatee/cases_holdout.json`
case_71) — the day before the 2026-02-05 Item 4.02 8-K. Redraws as recorded:
`runs/holdout/mainscore_redraw/draw_{2,3,4,5}/case_71.json` = score 76 / 60 / 58 / 60 (all
risk_tier "elevated"); draw-to-draw range across main + redraws is score 58–76, every draw above
the 50 flag threshold. Primary remains the main draw (D85 median-of-3 co-report context).
`analysis/error_analysis_wave2_holdout.md` §3 verdict: "점수는 맞고 기제는 빗나감" — tier hit,
mechanism miss.

## 2. ACTUAL EVENT

Provisional tier — no AAER exists for this event; the anchor document is the restatement 8-K,
accession `0001193125-26-039396` (8-K, filed 2026-02-05, items "2.02,4.02,9.01"), verified in the
sealed EDGAR submissions chronology `~/aaer-data/HUBG/edgar/CIK0000940942.json` (manifest-pinned,
`data/manifests/aaer_data_manifest.json`). `analysis/LABEL_REPORT.md` §1 tags the case **bigR**
(Item 4.02 non-reliance within revelation ±90d); `analysis/label_tags_holdout.json` case_71 records
revelation_date 2026-02-05 and, outside the neighborhood, a second 4.02 8-K
`0001193125-26-218141` (2026-05-12) — observed, judgment unchanged.

Restatement mechanism as registered in the sealed grade record
(`scoring/grades_holdout/case_71.json`, answer-key join): "purchased transportation costs ~$77M
understated / unrecorded accounts payable, FY2023-24 10-Ks misstated (8-K Item 4.02, 2026-02-05)";
`analysis/error_analysis_wave2_holdout.md` §3 concurs: "매입운송비 ~$77M 과소·미기록 AP,
FY2023-24 10-K 오기재, CFO·COO 해임". GAAP topic area implicated by that summary: completeness of
accrued liabilities / cost-of-services expense recognition; ASC-level mapping from primary 8-K
text: **insufficient sealed evidence** (the 8-K full text is not sealed locally — see §9). The
answer key's genre_tag_row is null: per the grade record, "G2 PROVISIONAL, non-confirmed-fraud
restatement event". Provisional caveat (LABEL_REPORT learning note): a 4.02 non-reliance
declaration "과거 재무제표를 쓰지 말라는 회사 자신의 판정일 뿐, 의도성(fraud)도 집행 가능성도
확정하지 않는다" — this entry alleges nothing beyond the company's own disclosure posture.

## 3. SIGNALS AVAILABLE PRE-CUTOFF

Cutoff 2026-02-04. Sealed basis: the deck entry `data/evaluatee/cases_holdout.json` case_71
carries exactly five identity fields (case_id, ticker, cik, company_name, cutoff_date); the
frozen output's documents_used spans 63 filings, 2010-07-28 through 2025-11-05. From the sealed
companyfacts `~/aaer-data/HUBG/xbrl/CIK0000940942.json` and the frozen output's cited values
(spot re-verified):

- **Pre-cutoff restatement history**: the 2018-01-05 amendment cluster — 10-K/A
  `0001564590-18-000122` (FY2015) plus 10-Q/A `0001564590-18-000123` / `-000124` / `-000126`
  (Q1–Q3 2017), all filed the same day.
- **Goodwill/intangible growth vs revenue**: Goodwill 262,376,000 (2016-12-31, accn
  `0001564590-19-005778`) → 733,695,000 (2023-12-31, accn `0000950170-25-026866`); revenue
  2,750,449,000 FY2016 → 4,202,585,000 FY2023, then declining 5,340,490,000 FY2022 →
  3,946,390,000 FY2024 (same accessions as cited in the frozen output).
- **NI vs OCF**: FY2023 NetIncomeLoss 167,528,000 vs OCF 422,158,000 (accn `0000950170-25-026866`).
- **As-filed AP series through the misstated period**: AccountsPayableCurrent 349,378,000
  (2023-12-31, accn `0000950170-24-021432`, 10-K filed 2024-02-27) and 279,982,000 (2024-12-31,
  accn `0000950170-25-026866`, 10-K filed 2025-02-25) — present in sealed companyfacts (132
  observations through 2025-09-30). These are the as-filed figures; per the registered mechanism
  (§2) the FY2023-24 statements were later declared non-reliable, i.e., an unrecorded liability
  leaves no positive anomaly in the reported balance itself.
- **Coverage limits recorded by the model itself** (CL8): receivables series last delivered at
  443,539,000 (end 2019-12-31, accn `0001564590-20-007787`); GrossProfit last at 889,505,000
  (FY2022, accn `0000950170-23-004358`).

This section describes the information set — it does not re-score the case.

## 4. WHAT THE LLM CAUGHT

Frozen output `runs/holdout/scores/case_71.json`: `misstatement_probability`: 70 (legacy v1 key —
an uncalibrated ordinal score; see specs/RISK_SCORE_SEMANTICS.md) = score 70, risk_tier
"elevated" — above the 50 threshold, hence the provisional-TP outcome. Checklist flags: CL2
(soft-asset growth) and CL7 (filing-chronology irregularities); top signal (verbatim):
"Simultaneous 10-K/A (FY2015) and three 10-Q/A filings (Q1-Q3 2017) plus companion 8-K/8-K/A, all
filed on 2018-01-05, indicating a confirmed material restatement covering roughly FY2013-2017
periods".

| model claim (verbatim) | enforcement/restatement reference | match quality |
|---|---|---|
| Hypothesis 1: "Restatement/correction of an error under ASC 250 in previously issued financial statements" — the 2018-01-05 cluster as "a classic pattern associated with an Item 4.02 non-reliance disclosure and subsequent restatement"; direction "timing_shift"; affected items incl. "Operating income/cost of services (quarterly 2016-2017)" | Registered mechanism (§2): purchased transportation costs ~$77M understated / unrecorded accounts payable, FY2023-24 — wrong period (2013-2017 vs 2023-24), wrong direction ("timing_shift" vs understatement), wrong treatment (generic error correction vs unrecorded AP); account area overlaps (grade record: "'operating income/cost of services' overlaps the correct account area (purchased transportation is a cost-of-services expense line for this issuer)") | right account wrong mechanism |
| Hypothesis 2: Goodwill/IntangibleAssetsNetExcludingGoodwill "overstated" — "raising the risk of a future or currently understated impairment" | Grade record: "the second-ranked hypothesis (goodwill/intangible impairment risk) is unrelated to the truth" | unrelated |
| CL7 flag: "10-K/A filing_date 2018-01-05" + three "10-Q/A filing_date 2018-01-05" — filing-chronology irregularity | Restatement-propensity signal pointing at elevated non-reliance risk generally; carries no content about the 2026 mechanism, period, or accounts | right direction only |
| CL2 flag: Goodwill "262376000" (2016) → "733695000" (2023) vs revenue growth | No counterpart in the registered restatement mechanism | unrelated |

The dim2=1 grade is the "tier hit, mechanism miss" verdict in numeric form: correct account area
only — per the grade record, "no case-specific fact from the key ($77M, FY2023-24 scope, CFO/COO
termination) appears". dim1=2 (score 70 meets the ≥70 band on a treatment case); dim4=3 (evidence
cited to accessions present in documents_used; consistency rule score-70/"elevated" satisfied).

## 5. WHAT THE LLM MISSED

The current-period leg entirely. Grade record coverage note: "Coverage note (multi-mechanism
truth: expense understatement + liability understatement): neither leg is explicitly covered."
Both hypotheses anchor pre-2018; neither touches FY2023-24. Within §3's sealed information set:

- The as-filed FY2023/FY2024 AP balances (349,378,000 → 279,982,000) and the cost-of-services
  expense family were in sealed companyfacts, and CL6 examined a liability-adequacy question — but
  an understatement by omission is, by construction, invisible as a positive anomaly in the
  reported series; the reported AP decline tracks the revenue decline the model itself cited
  (FY2022 5,340,490,000 → FY2024 3,946,390,000). No sealed artifact demonstrates a delivered
  pre-cutoff series in which the ~$77M understatement was visible. **None identified from sealed
  evidence** beyond this: the model treated the 2018 amendment cluster as the event rather than as
  a base-rate prior, and asserted no current-period completeness hypothesis at all.
- Whether an AP series was in the delivered payload (vs the sealed companyfacts superset) is not
  re-derivable from the frozen output, which cites no AccountsPayable concept — insufficient
  sealed evidence on that sub-question.

## 6. ERROR TAXONOMY

Per `scoring/error_taxonomy.md` (R1→R2→R3), atlas vocabulary:

- **R1 (DATA-first)**: partially indeterminate — the answer-key signal (unrecorded AP) does not
  exist as a visible anomaly in as-filed data even in principle (§5), and whether an AP series was
  delivered at all is not re-derivable from frozen artifacts (UNCLASSIFIED on that sub-question).
  R2: dim1/dim2 anchors applied mechanically; no criteria ambiguity identified. R3: the mechanism
  miss, to the extent attributable, is **interpretation** — anchoring the 4.02-shaped hypothesis
  on the historical 2018-01-05 cluster instead of the current period. The sealed analysis frames
  it "부분 (ii-b): 옳은 방향의 리스크 신호, 특정 사건 기제는 미상"
  (`analysis/error_analysis_wave2_holdout.md` §3).
- **Computation / retrieval**: none identified — dim4=3; cited accessions and values re-verified
  against sealed companyfacts (§3).
- **Label-noise**: inherent to the tier — provisional-4.02/restatement, not AAER-confirmed;
  LABEL_REPORT §2 records the base-rate caveat and §3 the symmetric upgrade/expiry protocol
  (monitoring until 2030-02-05). Not an error in this entry, a known uncertainty of the label.
- **Suspected-memorization**: no. `analysis/gate_k5_results.json` HUBG: draws_knows_event
  [false ×5], band_true_of_5 = 0, verdict "ELIGIBLE" (positive control HTZ knows_event true).
  Main draw `runs/holdout/recognition/HUBG.json`: knows_event false, confidence "none" — "I have
  no specific knowledge of Hub Group, Inc. (HUBG) ever announcing an accounting restatement";
  draws 2–5 `runs/holdout/recognition_k5/draw_{2,3,4,5}/HUBG.json`: knows_event false, confidence
  "low" each. Grade memorization_suspect_condition2: false — "the output never references the
  2026-02-05 Item 4.02 8-K, the ~$77M purchased-transportation understatement, or the CFO/COO
  terminations".

## 7. CPA JUDGMENT — human_finalized: false

Draft, unaudited work product until owner sign-off (PROJECT.md §7).

- The flag is best read as risk screening, not forensic detection: the model scored a company with
  a real amendment history and rapid goodwill accretion as "elevated" — a defensible prior — but
  supplied no hypothesis about the period the non-reliance actually covers.
  `analysis/error_analysis_wave2_holdout.md` §3: the HUBG hit "리스크 스크리닝 능력의 증거 ...
  이지 2026 기제의 forensic 탐지 증거가 아니다"; any narrative of this case must stay within
  "tier 적중/기제 빗나감". **[OWNER REVIEW]**
- Liability-completeness misstatements are the canonical blind spot of balance-trend screening:
  the anomaly is an absence. CL6 asks whether reserves "decline(d) ... despite growing business
  activity," which presumes visibility of the balance that should have been recorded; a
  completeness-oriented analytic (e.g., purchased-transportation expense vs volume/linehaul
  proxies, AP-to-cost-of-services ratio) is a different instrument. Whether that is a checklist
  gap or an input-scope limit is an attribution call. **[OWNER REVIEW]**
- The account-area overlap credited by dim2=1 (cost of services) arises from the 2016-2017
  hypothesis, not from any FY2023-24 reasoning — the partial credit is coincidental to the
  current event's period. Whether "right account wrong mechanism" overstates the correspondence
  is a judgment on the enum's granularity, not on the grade. **[OWNER REVIEW]**
- Score stability (58–76 across five draws, all flagging) suggests the elevated tier is driven by
  the durable facts (amendment history, goodwill trend), not draw noise. **[OWNER REVIEW]**

## 8. AUDIT TRANSLATION

Substantive procedures an elevated flag on this profile would motivate — procedures, not
conclusions:

- Search for unrecorded liabilities: examine subsequent cash disbursements and unmatched carrier
  invoices/receiving records after period end; test the completeness of purchased-transportation
  accruals (cut-off testing around year end for services rendered not yet billed).
- Reconcile carrier/vendor statements to recorded AP for major transportation providers; confirm
  balances with a completeness-oriented (zero-balance-inclusive) selection.
- Analytics on purchased transportation expense against load volume, linehaul rates, and revenue
  mix by segment; investigate ratio movements inconsistent with operational drivers.
- Journal-entry testing over accrual releases and top-side adjustments to cost of services near
  period end.
- Given the model's second hypothesis: goodwill impairment procedures — reporting-unit
  identification, cash-flow projection support against the FY2022→FY2024 revenue decline, and
  sensitivity of headroom (ASC 350 area).

## 9. FINANCIAL STATEMENT IMPACT

**Not determinable from sealed source documents.** The Item 4.02 8-K `0001193125-26-039396` is
sealed locally only at metadata level — `~/aaer-data/HUBG/edgar/CIK0000940942.json` records form,
date, and items ("2.02,4.02,9.01"), but the 8-K body text is not present under
`~/aaer-data/HUBG/` (manifest entries: two edgar JSONs + one xbrl JSON). The sealed grade record
registers the answer-key summary — purchased transportation costs ~$77M understated / unrecorded
accounts payable, FY2023-24 10-Ks — but restated line items and directions as stated in the 8-K
text itself cannot be quoted here; per the template rule, no figures are estimated or computed.

---
*Entry status: drafted (sections 7–9 pending owner finalization).*
*채점: Claude 보조 + 인간 최종 확정. 교육·정보 목적, 투자 자문 아님.*
