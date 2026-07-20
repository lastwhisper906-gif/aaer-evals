# atlas/case_14.md — Garmin Ltd. (GRMN) — wave-1 control C03 (TN-FLAGGED)

Authored by Claude Code, pending human audit (D15). Analytical document under D106 ② — not a scored output. 본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).

## 1. CASE HEADER

| field | value |
|---|---|
| Case ID (anonymized frame) | case_14 (scoring ID C03) |
| Cohort | wave-1 (8-control arm) |
| Outcome class | TN-flagged (main frame TN at score 32 — well below flag at score ≥50; E2 trajectory layer flag: `analysis/decision_table.json` L4, threshold-50 cell, `flagged_control` includes case_14 — also in the T=40 cell, not T=60 or T=70) |
| Ground-truth tier | control (no adverse label) |
| Frozen score | score 32 (`runs/main/case_14.json`, run `original-case_14-r1`); no perturbed main frame — `runs/perturbed/` covers only the 8 wave-1 treatment cases (frozen asymmetric design, RP-05 J14). E2 snapshots are a separate frozen layer (§4) |
| Grade record | `scoring/grades/main/case_14.json` (human_finalized: true, RP-09 Stage 0, commit 986a893, 2026-07-07) — dim1=1 ("misstatement_probability=32; control band 30<p<50 → 1 (misses the p<=30 band for a 2 by a small margin)"; legacy v1 key — an uncalibrated ordinal score; see specs/RISK_SCORE_SEMANTICS.md), dim2/dim3 null (control), dim4=3, memorization_suspect_condition2=false. E2 snapshots are ungraded — E2 = 146 evaluatee calls, 0 grader calls (`docs/FREEZE_REV4_HARNESS_E2.md` §4) |

Company: Garmin Ltd. (GRMN), CIK 0001121788, cutoff 2013-08-06 — copied, as
is `first_revelation_date` 2013-08-07, from matched treatment T12 per GP-9
(`data/candidates/candidates.json` C03; `data/evaluatee/cases.json`
case_14). **This entry documents model behavior across two frozen frames on
a control company, not a company problem.**

## 2. ACTUAL EVENT

**No adverse event — control** (cleanliness basis per original selection
criteria; formalized at `docs/CONTROL_CRITERIA_v1.md`). Selection record
`data/candidates/candidates.json` C03: "Control for T12 LOGI: 4-axis match —
industry SIC 3812 … size rev=2715675000 assets=4570420000 … period FYE 1226
… Selected per D17"; notes: "Non-enforcement verified 2026-07-06: AAER
index (3,339 entries, AAER 987-4595) name-search negative for the
registrant; secondary web search (2026-07-06) negative for SEC accounting
enforcement." (`review_packets/RP-01_control_group.md` C03 row: "색인·웹
음성", with an FYE-mismatch caveat vs T12 — "12월 (LOGI 3월 — 불일치
주석)".) The sealed submissions metadata (`~/aaer-data/GRMN/edgar/
CIK0001121788.json` + `-submissions-001.json`, spanning 2000-09-11 →
2026-06-25) contains **zero 8-K filings with Item 4.02**. GP-8 caveat as
recorded (`review_packets/RP-05_results.md` §7-1): 대조군 라벨은
"비집행"이지 "무결"이 아니다 — an error there is conservative for measured
specificity.

## 3. SIGNALS AVAILABLE PRE-CUTOFF

Cutoff 2013-08-06. Sealed basis: the frozen outputs' quoted deck values,
`~/aaer-data/GRMN/xbrl/CIK0001121788.json` (companyfacts), and
`~/aaer-data/GRMN/edgar/` (submissions metadata). Filing narrative text is
not among the sealed sources — filing-text quotes: **insufficient sealed
evidence**. Data points the model reacted to, all filed ≤ cutoff (§4):

- ProductWarrantyAccrualClassifiedCurrent $87.424M (2009-12-26) → $49.885M
  → $46.773M → $37.301M (2012-12-29) while SalesRevenueNet stayed in the
  $2.69-2.95B range (≈3.0% → ≈1.4% of revenue per the frozen main output).
- GrossProfit/revenue ~48.5% FY2011 ($1,338.592M/$2,758.569M) → ~53.0%
  FY2012 ($1,438.480M/$2,715.675M) on roughly flat revenue; Goodwill
  $136.548M (2010-12-25) → $179.475M (2011-12-31), +31%, vs total assets
  +12% ($3,988.688M → $4,471.338M).
- AccountsReceivableNetCurrent $741.321M (2008-12-27) → $874.110M
  (2009-12-26) → $747.249M → $607.450M → $603.673M (2012-12-29) — a FY2009
  year-end rise that reversed — against FY2009 revenue $2,946.440M (vs
  FY2008 $3,494.077M); AllowanceForDoubtfulAccountsReceivableCurrent
  $42.409M → $36.673M → $31.822M → … → $30.596M (2008-2012); CFO > NI every
  year (FY2012 $684.745M vs $542.403M); InventoryNet $309.938M → $387.577M
  in FY2010 as revenue fell to $2,689.911M.
- Chronology: two pre-cutoff 10-Q/A (2009-09-01, 0001144204-09-046684;
  2011-08-30, 0001144204-11-050441); two 15-12G (2010-05-04, 2010-06-28)
  and a 25-NSE (2010-06-25), all in the sealed submissions record.
This section describes the information set — it does not re-score the case.

## 4. WHAT THE LLM CAUGHT (what the model asserted, in both frames)

**Main frame** (`runs/main/case_14.json`): `misstatement_probability`: 32
(legacy v1 key — an uncalibrated ordinal score; see
specs/RISK_SCORE_SEMANTICS.md) = score 32, risk_tier "watch",
`mechanism_hypotheses` empty (score <40 — no hypothesis required). CL4/CL6
flagged ("medium"), CL2/CL7 flagged ("low"), CL1/CL3/CL5/CL8 no_flag. Top
signals: warranty-accrual decline "a potential reserve-release earnings
lever though could reflect genuine product quality improvement"; FY2012
margin expansion; FY2011 goodwill growth "consistent with acquisition
activity"; two 10-Q/A "a mild process-quality flag"; and "Positive quality
indicators: operating cash flow consistently exceeded net income every
year … and receivables grew slower than/in line with revenue".

**E2 trajectory layer** (perturbed variant, identity-anonymized,
case-constant deterministic perturb factor — `docs/EARLINESS_DESIGN.md` §1;
harness path per `docs/FREEZE_REV4_HARNESS_E2.md`): frozen snapshot scores
in `runs/e2/s1…s8/case_14.json` (run `perturbed-case_14-r1`), assembled in
`analysis/e2_trajectories.json` (j=0 `llm_p: null` — D71 fail-closed):
j1 32 (cutoff 2013-05-09), j2 30, j3 48, j4 33, j5 **52** (2012-05-10), j6
**55** (2012-03-01), j7 **58** (2011-11-03, trajectory maximum), j8 **55**
(2011-05-05). Flag rule as recorded (`analysis/DECISION_TABLE.md` §4):
"플래그 = **어느 스냅샷이든** llm_p ≥ T … llm_p null 스냅샷 fail-closed
제외" — at T=50 four snapshots (s5-s8) meet the rule, so case_14 enters
`flagged_control`; cited as recorded, no recomputation. The frozen B3
series never reaches its flag (b3_score = 1 at every snapshot; threshold
≥2). Shape note: the score **falls as the window lengthens** — 55/58/55/52
at the 2011-2012 cutoffs, 33-48 through 2012-11, 30-32 at the 2013
cutoffs, 32 in the full-deck main frame.

| model claim (verbatim) | evidence genuine? (sealed record) | correspondence |
|---|---|---|
| Main CL6: "ProductWarrantyAccrualClassifiedCurrent=87424000 (2009-12-26) declining to 49885000 … 46773000 … and 37301000 (2012-12-29) while SalesRevenueNet remained in the 2.7-2.9B range" | genuine — all values in `~/aaer-data/GRMN/xbrl/CIK0001121788.json` at the cited dates | n/a — control |
| Main CL4/top_signals: FY2012 gross margin ~53.0% vs FY2011 ~48.5%; CL2: Goodwill 136,548,000→179,475,000 (+~31%) vs Assets +~12%; top_signals[4]: "operating cash flow consistently exceeded net income every year (e.g., FY2012 OCF=684745000 > NI=542403000)" | genuine — all figures verified at value+date in sealed companyfacts | n/a — control |
| E2 j7 CL1 (score 58): AR "+17.9% increase" (2008-12-27→2009-12-26) vs revenue "-15.7% decline" (FY2008→FY2009); j7 CL6: allowance ratio "5.7% -> 4.2% -> 4.3%", warranty accrual "~43% decline" FY2009→FY2010 | perturbed-frame values are scaled by design; the scale-invariant ratios match the sealed-frame paths ($741.321M→$874.110M AR vs $3,494.077M→$2,946.440M revenue; 42,409/741,321, 36,673/874,110, 31,822/747,249; 87,424→49,885) | n/a — control |
| E2 j7 hypotheses[1]: "AccruedLiabilitiesCurrent … fell … a 71% one-quarter drop" (2009-09-26→2009-12-26); E2 s3 (score 48): "Anomalous Q3 2010 quarter where net income … exceeded operating income" | both accrued-liability endpoints back out to genuine sealed tag values ($141.021M, 10-Q; $40.373M, 10-K) — a cross-form tag comparison; sealed-frame NetIncomeLoss does exceed OperatingIncomeLoss for 2010-06-27→2010-09-25, cause not in sealed sources | n/a — control |

## 5. WHAT THE LLM MISSED

n/a — control: there is no adverse mechanism to miss. The main frame itself
kept CL1/CL3/CL5 at no_flag and held the composite at score 32.

## 6. ERROR TAXONOMY (classification of the E2-layer flag)

- **No first-pass MECE attribution exists on record for E2-layer control
  flags**: RP-05 §6 covers main-frame error units only; case_14 was not one
  (`review_packets/RP-06_grading_workbench.md` case_14: "본 분석 오류 단위
  아님"). Below is atlas-level draft classification.
- **Interpretation (primary, draft)** — truncated-window over-reading: the
  breaching snapshots re-read the FY2009 AR rise and FY2009-FY2010 reserve
  declines as active concerns, without the later data (AR at $603.673M by
  FY2012, CFO>NI every year) the main frame weighed as mitigants. Notably
  the FY2010 AR reversal ($874.110M→$747.249M, filed in the 2011-02-23
  10-K) was **inside j7's own window**, yet j7's CL1 quotes only the
  FY2008→FY2009 leg. Same axis as the Ryder over-reading in RP-05 §6 and
  the case_05 E2 flag.
- **Design/measurement context (recorded, not recomputed)** —
  `analysis/DECISION_TABLE.md` §4 states the rule's own cost: "리드타임의
  대가로 오탐 기회도 스냅샷 수만큼 늘어난다" (any-snapshot rule; T=50
  control row 5/7). Draw-noise on record: main-frame k=5 re-draws scored
  32,27,45,42,30 (mean 35.2, σ 7.0; `review_packets/RP-06_hardening.md`
  §3-2) — all five below 50: the full-deck frame never crosses on any
  recorded draw; the breaches (52-58) appear only on truncated 2011-2012
  windows. Against RP-07's median per-case σ 6.3pp reference band
  (`docs/EARLINESS_DESIGN.md` §4), j5 (52) sits within one band of the
  threshold, j7 (58) above it. L-2/L-3 inherited limitations apply
  (`docs/FREEZE_REV4_HARNESS_E2.md` §3).
- **Computation** — none found: every quoted main-frame figure verified
  value+date against sealed companyfacts; E2 ratios consistent (§4).
- **Label-noise** — none within the design: control label verified per §2;
  GP-8 residual conservative. RP-01's FYE-mismatch caveat is a
  matching-quality note, not a label defect.
- **Suspected-memorization** — no probe row exists for case_14. The
  registrant does appear under the separate v2-controls frame (case_25,
  `scoring/id_mapping_v2.json` → V09): recognized=true, guess "Garmin Ltd."
  on the v1 draw (`analysis/name_probe_results.json`) but recognized=false
  on the v2ds draw (`analysis/name_probe_results_v2ds.json` wave1) — run on
  the v2-controls deck, not the case_14 deck; verdicts vary across draws
  (L-5). Grade record: memorization_suspect_condition2=false.

## 7. CPA JUDGMENT — human_finalized: false

Draft, unaudited until owner sign-off (PROJECT.md §7). Benign readings:
- **A warranty accrual is measured against expected claims, not revenue.**
  A decline from ~3.0% to ~1.4% of revenue over four years is consistent
  with mix shift or improved claims experience — the main frame carried
  this alternative ("could reflect genuine product quality improvement");
  claims history is not in sealed tags. **[OWNER REVIEW]**
- **The FY2009 AR rise against falling revenue reversed** — $874.110M
  (2009) → $747.249M (2010) → $603.673M (2012). Sustained premature-
  recognition schemes leave receivables persistently elevated; the full
  deck shows the opposite, part of the reversal was already inside j7's
  window (§6), and year-end AR at a December FYE carries Q4 seasonality.
  The companion allowance drift (5.7%→~4.3%) tracked a shrinking
  receivables base, explainable as utilization/release. **[OWNER REVIEW]**
- **Margin expansion on flat revenue (FY2012 ~53.0%) is a mix/cost
  question**; the main frame framed it as "warranting scrutiny of …
  mix-shift explanations", not as a mechanism. **[OWNER REVIEW]**
- **The "71% one-quarter drop" in accrued liabilities compares a 10-Q tag
  to a 10-K tag** — cross-presentation composition differences are a
  candidate benign mechanism. The Q3 2010 NI>OI quarter and the 2010
  15-12G/25-NSE cluster are unexplained in sealed sources; sealed
  submissions show reporting under the same CIK continued through
  2026-06-25 — the deregistration forms did not end it. **[OWNER REVIEW]**
- **Net shape**: the full-deck main frame integrated the reversals and
  CFO>NI into score 32 with zero hypotheses; the E2-layer flag arises from
  re-reading the FY2009-FY2010 legs on truncated windows under an
  any-snapshot rule (§6). **[OWNER REVIEW]**

## 8. AUDIT TRANSLATION

Procedures that would clear the E2-layer flag (procedures, not conclusions):
- Obtain the warranty reserve rollforward (provisions vs claims paid vs
  changes in estimate) FY2009-FY2012; test the accrual rate against claims
  experience by product line.
- Confirm FY2009 year-end receivables and test subsequent cash receipts;
  sales cutoff testing at 2009-12-26; allowance rollforward and aging.
- Gross margin analytics by product line/mix for FY2012; review FY2011
  acquisition purchase-price allocations (goodwill +31%).
- Read the two 10-Q/A filings for the amended items (content outside
  sealed sources — insufficient sealed evidence here); search the 8-K
  record for Item 4.02/auditor-change items (sealed metadata already
  answers: zero 4.02); inquire into the 2010 15-12G/25-NSE filings and
  the Q3 2010 non-operating item.

## 9. FINANCIAL STATEMENT IMPACT

n/a — no restatement (control). No restated line items exist; the sealed
record contains no Item 4.02 8-K and no enforcement or restatement document
for this registrant (§2).

---
*Entry status: drafted (sections 7–9 pending owner finalization).*
*채점: Claude 보조 + 인간 최종 확정. 교육·정보 목적, 투자 자문 아님.*
