# atlas/case_11.md — NuVasive, Inc. (NUVA) — wave-1 control C02 (TN-FLAGGED)

Authored by Claude Code, pending human audit (D15). Analytical document under D106 ② — not a scored output. 본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).

## 1. CASE HEADER

| field | value |
|---|---|
| Case ID (anonymized frame) | case_11 (scoring ID C02) |
| Cohort | wave-1 (8-control arm) |
| Outcome class | TN-flagged (main frame TN at score 45 — below flag at score ≥50; E2 trajectory layer flag: `analysis/decision_table.json` L4, threshold-50 cell, `flagged_control` includes case_11 — also in the T=40 and T=60 cells, not T=70) |
| Ground-truth tier | control (no adverse label) |
| Frozen score | score 45 (`runs/main/case_11.json`, run `original-case_11-r1`); no perturbed main frame — `runs/perturbed/` covers only the 8 wave-1 treatment cases (frozen asymmetric design, RP-05 J14). E2 snapshots are a separate frozen layer (§4) |
| Grade record | `scoring/grades/main/case_11.json` (human_finalized: true, RP-09 Stage 0, commit 986a893, 2026-07-07) — dim1=1 ("output p=45 falls in 30<p<50 control band -> 1"; `misstatement_probability` is the legacy v1 key — an uncalibrated ordinal score; see specs/RISK_SCORE_SEMANTICS.md), dim2/dim3 null (control), dim4=3, memorization_suspect_condition2=false. E2 snapshots are ungraded — E2 = 146 evaluatee calls, 0 grader calls (`docs/FREEZE_REV4_HARNESS_E2.md` §4) |

Company: NuVasive, Inc. (NUVA), CIK 0001142596, cutoff 2013-07-28 — copied,
as is `first_revelation_date` 2013-07-29, from matched treatment T11 OFIX
per GP-9 (`data/candidates/candidates.json` C02; `data/evaluatee/cases.json`
case_11). **This entry documents model behavior across two frozen frames
on a control company, not a company problem.**

## 2. ACTUAL EVENT

**No adverse event — control** (cleanliness basis per original selection
criteria; formalized at `docs/CONTROL_CRITERIA_v1.md`). Selection record
`data/candidates/candidates.json` C02: "Control for T11 OFIX: 4-axis match —
industry SIC 3841 … size rev=620255000 assets=1101452000 (point-in-time at
matched cutoff) … Selected per D17"; notes: "Non-enforcement verified
2026-07-06: AAER index (3,339 entries, AAER 987-4595) name-search negative
for the registrant; secondary web search (2026-07-06) negative for SEC
accounting enforcement."
(`review_packets/RP-01_control_group.md` C02 row: "색인·웹 음성 (2015 DOJ
FCA는 헬스케어 청구건 — 회계 아님, 주석)" — a post-cutoff, non-accounting
annotation, not an adverse accounting label.) The sealed submissions metadata
(`~/aaer-data/NUVA/edgar/CIK0001142596.json` and `-submissions-001.json`,
jointly spanning 2003-07-01 → 2023-09-11) contains **zero 8-K filings with
Item 4.02** across 276 8-K entries. GP-8 caveat as recorded
(`review_packets/RP-05_results.md` §7-1): 대조군 라벨은 "비집행"이지
"무결"이 아니다 — an error there is conservative for measured specificity.

## 3. SIGNALS AVAILABLE PRE-CUTOFF

Cutoff 2013-07-28. Sealed basis: the frozen output's quoted deck values,
`~/aaer-data/NUVA/xbrl/CIK0001142596.json` (companyfacts), and
`~/aaer-data/NUVA/edgar/` (submissions metadata). Filing narrative text is
not among the sealed sources — filing-text quotes: **insufficient sealed
evidence**. Data points the model reacted to, all filed ≤ cutoff (§4):

- AllowanceForDoubtfulAccountsReceivableCurrent $4.163M (2009-12-31) →
  $2.780M (2012-12-31) against AccountsReceivableNetCurrent $58.462M →
  $88.958M — the ~7.1% → ~3.1% coverage decline the frozen output computes;
  AccruedLiabilitiesCurrent $25.989M (2010-12-31) → $20.880M (2012-12-31)
  while SalesRevenueGoodsNet grew $478.237M (FY2010) → $620.255M (FY2012).
- NetIncomeLoss +$78.285M (FY2010) → -$69.849M (FY2011) → +$3.144M (FY2012)
  with NetCashProvidedByUsedInOperatingActivities positive throughout
  ($65.827M / $62.965M / $130.082M); quarterly NetIncomeLoss +$61.932M
  (Q4 2010) and -$67.552M (Q3 2011).
- Goodwill $103.070M (2010-12-31) → $159.349M (2011-12-31);
  OtherAssetsNoncurrent $7.260M (2009-12-31) → $25.463M (2012-12-31); gross
  margin 83.5% (FY2009) → 75.3% (FY2012) as computed in the frozen output.
- Chronology: 10-K/A filed 2010-05-26; SEC UPLOAD/CORRESP clusters in 2010
  (07-30 → 10-28) and 2012 (09-14, 09-27, 10-18) — verified in the sealed
  submissions metadata.
This section describes the information set — it does not re-score the case.

## 4. WHAT THE LLM CAUGHT (what the model asserted, in both frames)

**Main frame** (`runs/main/case_11.json`): `misstatement_probability`: 45
(legacy v1 key — an uncalibrated ordinal score; see
specs/RISK_SCORE_SEMANTICS.md) = score 45, risk_tier "watch" — below the
frozen flag line (score ≥50), so a TN in the main analysis. CL3 flagged
("high"), CL2/CL6/CL7 ("medium"), CL4 ("low"), CL1/CL5/CL8 no_flag. Top
hypothesis: "Potential under-reserving: allowance for doubtful accounts as
a percentage of gross receivables fell from ~7.1% (2009) to ~3.1% (2012)";
hypotheses[1] "timing_shift" on the NI/OCF divergence; hypotheses[2]
one-off quarterly swings plus goodwill/soft-asset growth.

**E2 trajectory layer** (perturbed variant, identity-anonymized,
case-constant deterministic perturb factor — `docs/EARLINESS_DESIGN.md` §1;
harness per `docs/FREEZE_REV4_HARNESS_E2.md`): frozen snapshot scores in
`runs/e2/s1…s7/case_11.json` (run `perturbed-case_11-r1`), assembled in
`analysis/e2_trajectories.json` (j=0 `llm_p: null` — D71 fail-closed): j1
**55** (cutoff 2013-05-02), j2 45, j3 **55** (2012-10-26), j4 45, j5 **60**
(2012-05-02, trajectory maximum), j6 **58** (2012-02-28), j7 **55**
(2011-11-05). Flag rule as recorded
(`analysis/DECISION_TABLE.md` §4; `decision_table.json` L4 note): "플래그 =
**어느 스냅샷이든** llm_p ≥ T … null 스냅샷 fail-closed 제외" — at T=50
five snapshots meet the rule (files `runs/e2/s1,s3,s5,s6,s7/case_11.json`),
so case_11 enters `flagged_control`; at T=60 only s5. The frozen B3 series
never reaches its flag (b3_score ≤1 at every snapshot; threshold ≥2). The
rule is cited as recorded — no recomputation.

| model claim (verbatim) | evidence genuine? (sealed record) | correspondence |
|---|---|---|
| Main CL6/hyp[0]: "AllowanceForDoubtfulAccountsReceivableCurrent=4,163,000 (2009-12-31) representing 7.1% of AccountsReceivableNetCurrent=58,462,000 … by 2012 … 2,780,000 … only 3.1% of … 88,958,000" | genuine — all values in `~/aaer-data/NUVA/xbrl/CIK0001142596.json` at the cited dates/accessions; ratios recompute | n/a — control |
| Main CL3: "NetIncomeLoss=-69,849,000 (FY2011) while NetCashProvidedByUsedInOperatingActivities=62,965,000 (FY2011)"; FY2012 $3.144M NI vs $130.082M OCF; FY2010 $78.285M NI vs $65.827M OCF | genuine — all three year-pairs verified in sealed companyfacts | n/a — control |
| Main CL2/hyp[2]: "Goodwill=103,070,000 (2010-12-31) increased to Goodwill=159,349,000 (2011-12-31)"; "OtherAssetsNoncurrent=7,260,000 (2009-12-31)" → "25,463,000 (2012-12-31)"; quarterly NI +$61.932M (Q4 2010) / -$67.552M (Q3 2011) | genuine — all figures verified at value+date level | n/a — control |
| Main CL7: "10-K/A filing_date=2010-05-26 shortly after original 10-K"; "Multiple SEC UPLOAD/CORRESP filings in 2010 (2010-07-30, 2010-08-11, 2010-08-20, …)"; 2012 round (09-14, 09-27, 10-18) | genuine with one nuance — 10-K/A and all listed dates verified in sealed submissions **except 2010-08-20, which the sealed chronology records as a CT ORDER** (SEC-issued, but not an UPLOAD/CORRESP form); 2012 dates exact | n/a — control |
| E2 j5 (score 60): "Goodwill and other non-current 'soft' assets grew far faster (54.6% and 90.8%) than revenue (13.0%) in 2011"; "Q4 2010 NI spike of 36.9M vs Q3 2011 NI crash of -40.2M" | perturbed-frame values are scaled by design; the growth-rate and volatility shapes match the sealed-frame verified series | n/a — control |
| E2 j1 (score 55): allowance "7.1% in 2009 to 3.1% in 2012, suggesting potential under-reserving"; j7 (score 55): "a classic reserve-release earnings-boost pattern" on the 2009→2010 coverage decline | same underlying coverage-ratio facts as the main frame, re-narrated per snapshot with escalating characterization on shorter windows | n/a — control |

## 5. WHAT THE LLM MISSED

n/a — control: there is no adverse mechanism to miss. The main frame itself
kept CL1/CL5 at no_flag and held the composite at score 45.

## 6. ERROR TAXONOMY (classification of the E2-layer flag)

- **No first-pass MECE attribution exists on record for E2-layer control
  flags**: RP-05 §6 covers main-frame error units only; case_11 was not an
  error unit (`review_packets/RP-06_grading_workbench.md` case_11: "본 분석
  오류 단위 아님"). Below is atlas-level draft classification.
- **Interpretation (primary, draft)** — evidence-exists over-reading: the
  flagged snapshots promote the same genuine coverage-ratio and NI/OCF
  facts the main frame scored at 45 into scores 50-60 on shallower windows
  centered on the 2011 balance-sheet expansion (assets nearly doubling —
  E2 s6 text), without the full deck's FY2012 stabilization data; j7's
  "classic reserve-release earnings-boost pattern" is the same coverage
  decline the main frame held below threshold.
- **Design/measurement context (recorded, not recomputed)** —
  `analysis/DECISION_TABLE.md` §4 states the rule's own cost: "리드타임의
  대가로 오탐 기회도 스냅샷 수만큼 늘어난다". Draw-noise on record:
  main-frame k=5 re-draws scored 45,33,55,58,45 (mean 47.2, σ 8.8, 33–58;
  `review_packets/RP-06_hardening.md` §3-2) — two of five re-draws
  themselves reached ≥50, so the TN/flag distinction sits inside the
  recorded noise environment; RP-07's median per-case σ 6.3pp is the E2
  design's "no change" reference band (`docs/EARLINESS_DESIGN.md` §4).
  L-2/L-3 inherited limitations apply (`docs/FREEZE_REV4_HARNESS_E2.md` §3:
  system-reminder/currentDate injection; no temperature pin).
- **Computation** — none found: every quoted main-frame figure verified at
  value+date+accession level against sealed companyfacts (§4); ratios
  recompute. One retrieval nuance: the 2010-08-20 entry is a CT ORDER
  inside an "UPLOAD/CORRESP" enumeration (§4 CL7 row) — date genuine, form
  label imprecise; immaterial to the score path.
- **Label-noise** — none within the design: control label verified per §2;
  GP-8 residual noted, direction conservative. The RP-01 annotation on a
  2015 non-accounting matter is post-cutoff — not a label defect.
- **Suspected-memorization** — not indicated on the sealed draws. No probe
  row exists for this registrant (`analysis/name_probe_results.json` and
  `_v2ds.json` contain no NUVA/case_11 row; `scoring/probe_results/
  recognition/` covers only the 8 wave-1 treatment cases). Grade record:
  memorization_suspect_condition2=false ("mentions no post-cutoff facts").
  Probe verdicts vary across draws (L-5).

## 7. CPA JUDGMENT — human_finalized: false

Draft, unaudited work product until owner sign-off (PROJECT.md §7). Benign
accounting readings of each flagged pattern:
- **A net loss with positive operating cash flow is the accounting shape of
  large non-cash charge recognition, not of earnings inflation.** FY2011
  (-$69.849M NI vs +$62.965M OCF) coincides with the goodwill step-up and
  the -$67.552M Q3 2011 quarter; recognizing a large charge works in the
  conservative direction — hypotheses[1] itself says "timing_shift".
  **[OWNER REVIEW]**
- **The allowance coverage decline (~7.1% → ~3.1%) is computed on net
  receivables tag values alone**; composition, write-offs, and collections
  experience are not determinable from the sealed tags — a ratio near ~3%
  is not facially deficient without the rollforward. **[OWNER REVIEW]**
- **Goodwill +55% and soft-asset growth in 2011 alongside assets nearly
  doubling is the shape of acquisition purchase accounting (ASC 805)**;
  prospective recoverability is a going-forward valuation question, not
  evidence of an existing misstatement — the frozen output itself says
  "raising questions about … recoverability/valuation support".
  **[OWNER REVIEW]**
- **Two SEC comment-letter cycles ending (final UPLOAD 2010-10-28;
  2012-10-18) with no subsequent Item 4.02 or restatement read as review
  closure**; letter subject matter is outside sealed sources —
  insufficient sealed evidence. **[OWNER REVIEW]**
- **Net shape**: the main frame weighed these benign-side readings into a
  below-threshold score 45; the E2-layer flag arises when the same signals
  are re-read on truncated windows around the 2011 acquisition-period
  volatility, under an any-snapshot rule, near the threshold, inside the
  recorded draw-noise band (§6 — re-draws straddle 33–58). **[OWNER REVIEW]**

## 8. AUDIT TRANSLATION

Procedures that would clear the E2-layer flag (procedures, not conclusions):

- Obtain the allowance rollforward (provisions, write-offs, recoveries) and
  receivables aging; recompute coverage on gross receivables.
- Test completeness of accrued liabilities (search for unrecorded
  liabilities/subsequent disbursements) over the 2010→2012 decline.
- Review 2011 purchase accounting: valuation support for goodwill and
  acquired intangibles, timing/assumptions of subsequent ASC 350 impairment
  assessments; vouch the Q4 2010 gain-quarter and Q3 2011 charge-quarter
  items to underlying agreements/orders.
- Read the 2010 and 2012 SEC comment letters and responses (content outside
  sealed sources — insufficient sealed evidence here); search the 8-K record
  for Item 4.02/auditor-change items (sealed metadata already answers:
  zero 4.02 across 2003-2023).

## 9. FINANCIAL STATEMENT IMPACT

n/a — no restatement (control). No restated line items exist; the sealed
record contains no Item 4.02 8-K and no enforcement or restatement
document for this registrant (§2).

---
*Entry status: drafted (sections 7–9 pending owner finalization).*
*채점: Claude 보조 + 인간 최종 확정. 교육·정보 목적, 투자 자문 아님.*
