# atlas/case_07.md — Xilinx, Inc. (XLNX) — wave-1 control C06 (TN-FLAGGED)

Authored by Claude Code, pending human audit (D15). Analytical document under D106 ② — not a scored output. 본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).

## 1. CASE HEADER

| field | value |
|---|---|
| Case ID (anonymized frame) | case_07 (scoring ID C06) |
| Cohort | wave-1 (8-control arm) |
| Outcome class | TN-flagged (main frame TN at score 25 — well below flag at score ≥50; E2 trajectory layer flag: `analysis/decision_table.json` L4, threshold-50 cell, `flagged_control` includes case_07 — also in the T=40 cell, not T=60 or T=70) |
| Ground-truth tier | control (no adverse label) |
| Frozen score | score 25 (`runs/main/case_07.json`, run `original-case_07-r1`); no perturbed main frame — `runs/perturbed/` covers only the 8 wave-1 treatment cases (frozen asymmetric design, RP-05 J14). E2 snapshots are a separate frozen layer (§4) |
| Grade record | `scoring/grades/main/case_07.json` (human_finalized: true, RP-09 Stage 0, commit 986a893, 2026-07-07) — dim1=2 ("misstatement_probability=25, which for a control case falls in the p<=30 band → 2"; legacy v1 key — an uncalibrated ordinal score; see specs/RISK_SCORE_SEMANTICS.md), dim2/dim3 null (control), dim4=3, memorization_suspect_condition2=false. E2 snapshots are ungraded — E2 = 146 evaluatee calls, 0 grader calls (`docs/FREEZE_REV4_HARNESS_E2.md` §4) |

Company: Xilinx, Inc. (XLNX), CIK 0000743988, cutoff 2015-09-10 — copied, as
is `first_revelation_date` 2015-09-11, from matched treatment T17 MRVL per
GP-9 (`data/candidates/candidates.json` C06; `data/evaluatee/cases.json`
case_07). **This entry documents model behavior, not a company problem.**

## 2. ACTUAL EVENT

**No adverse event — control** (cleanliness basis per original selection
criteria; formalized at `docs/CONTROL_CRITERIA_v1.md`). Selection record
`data/candidates/candidates.json` C06: "Control for T17 MRVL: 4-axis match —
industry SIC 3674 (Semiconductors & Related Devices), size rev=2377344000
assets=4915549000 (point-in-time at matched cutoff) … Selected per D17";
notes: "Non-enforcement verified 2026-07-06: AAER index (3,339 entries, AAER
987-4595) name-search negative for the registrant; secondary web search
(2026-07-06) negative for SEC accounting enforcement."
(`review_packets/RP-01_control_group.md` C06 row: "색인·웹 음성"; industry
match exact — "3674=MRVL 정확 일치 (팹리스 반도체)".) Sealed submissions
metadata (`~/aaer-data/XLNX/edgar/CIK0000743988.json` and
`-submissions-001.json`, jointly spanning 1994-12-09 → 2022-03-11) contains
**zero 8-K filings with Item 4.02**. GP-8 caveat (`review_packets/
RP-05_results.md` §7-1): 대조군 라벨은 "비집행"이지 "무결"이 아니다 — an
error here is conservative for measured specificity.

## 3. SIGNALS AVAILABLE PRE-CUTOFF

Cutoff 2015-09-10. Sealed basis: the frozen outputs' quoted deck values,
`~/aaer-data/XLNX/xbrl/CIK0000743988.json` (companyfacts), and
`~/aaer-data/XLNX/edgar/` (submissions metadata). Filing narrative text
(MD&A, debt footnotes) is not sealed — filing-text quotes: **insufficient
sealed evidence**. Data points the model reacted to, all filed ≤ cutoff:

- InventoryNet $130.628M (2010-04-03) → $264.745M (2011-04-02), +102.7%, vs
  SalesRevenueNet $1,833.554M → $2,369.445M (+29.2%); then normalized
  ($204.866M, 2012-03-31). AR/revenue divergence: FY2013 AR +6.6%
  ($214.965M → $229.175M) vs revenue -3.2% ($2,240.736M → $2,168.652M);
  FY2014 AR +16.9% (→ $267.833M) vs revenue +9.9% (→ $2,382.531M).
  Allowance $3.446M (2012-03-31) → $3.353M (2015-03-28), AR → $246.615M.
- **LiabilitiesCurrent $386.788M (2013-03-30) → $1,402.476M (2013-06-29) →
  $1,482.170M (2013-09-28) → $1,432.077M (2013-12-28) → $989.360M
  (2014-03-29)** — with, in the same sealed companyfacts, the step's
  counterpart: ConvertibleDebtCurrent $926.781M / $930.085M / $934.392M at
  the three interim dates and LongTermDebtCurrent $565.001M at 2014-03-29
  (both zero at 2013-03-30) — a debt classification event, on the record.
- Earnings-quality positives: operating cash flow exceeded net income every
  year FY2010–FY2015 (e.g., $790.780M vs $648.216M FY2015; $826.739M vs
  $530.079M FY2012); gross margin ~63.4% (FY2010) → ~70.2% (FY2015).
- Chronology: NT 10-K 2009-05-28, 10-K/A 2009-06-03, 10-Q/A 2007-02-06, NT
  10-Q 2006-08-10, 10-Q/A 2005-08-12 (all pre-2010, `-submissions-001.json`);
  CORRESP/UPLOAD filings in 2006-2008, 2010-2011, 2013.
This section describes the information set — it does not re-score the case.

## 4. WHAT THE LLM CAUGHT (what the model asserted, in both frames)

**Main frame** (`runs/main/case_07.json`): `misstatement_probability`: 25
(legacy v1 key — an uncalibrated ordinal score; see
specs/RISK_SCORE_SEMANTICS.md) = score 25, risk_tier "watch" — a TN.
CL1/CL4/CL6 flagged ("medium"), the rest no_flag; `mechanism_hypotheses`
empty. top_signals[3] weighs the offsets: "operating cash flow exceeded net
income in every year examined … a strong earnings-quality positive, and no
late filings/amendments were observed in the 2010-2015 window".

**E2 trajectory layer** (perturbed variant, identity-anonymized,
case-constant deterministic perturb factor — `docs/EARLINESS_DESIGN.md` §1;
harness path per `docs/FREEZE_REV4_HARNESS_E2.md`): frozen snapshot scores
in `runs/e2/s1…s8/case_07.json` (run `perturbed-case_07-r1`), assembled in
`analysis/e2_trajectories.json` (j=0 `llm_p: null` — D71 fail-closed;
case_07 in `_s0_llm_unavailable`): j1 28, j2 30, j3 33, j4 35, j5 25, j6
**50** (cutoff 2014-05-17), j7 30, j8 **55** (cutoff 2013-10-29, trajectory
maximum; risk_tier "elevated"). Flag rule as recorded
(`analysis/DECISION_TABLE.md` §4; `decision_table.json` L4 note): "플래그 =
**어느 스냅샷이든** llm_p ≥ T … llm_p null 7 스냅샷은 fail-closed 제외" — at
T=50 two snapshots meet the rule (`runs/e2/s6,s8/case_07.json`), so case_07
enters `flagged_control` (also at T=40; not at T=60 — max 55); the frozen B3
series never flags (b3_score 0 everywhere; threshold ≥2). The rule is cited
as recorded — no recomputation.

| model claim (verbatim) | evidence genuine? (sealed record) | correspondence |
|---|---|---|
| Main CL1: "SalesRevenueNet=2382531000" (FY2014) vs "AccountsReceivableNetCurrent=267833000 (2014-03-29)"; top_signals[2] "FY2013: AR +6.6% vs revenue -3.2%; FY2014: AR +16.9% vs revenue +9.9%" | genuine — all values in `~/aaer-data/XLNX/xbrl/CIK0000743988.json` at the cited dates; ratios recompute | n/a — control |
| Main CL6: allowance "3446000 (2012-03-31)" → "3353000 (2015-03-28)", "declined ~2.7%" while AR "+14.7%" | genuine — 3,446→3,353 (-2.70%); 214,965→246,615 (+14.72%) | n/a — control |
| Main CL4: inventory "+103%" FY2011 vs revenue "~29%"; "a monotonic margin improvement from ~63.4% to ~70.2% over 5 years" | values genuine; the year-by-year margins recompute to ~63.4% → ~65.4% → ~64.9% → ~66.0% → ~68.8% → ~70.2% — endpoints verify, but the path has a ~0.5pp dip in FY2012, so "monotonic" overstates | n/a — control |
| E2 s6 (score 50), top_signals[0]: "Unexplained ~$1.08B spike in LiabilitiesCurrent from FY2013 year-end ($411.8M) to Q1 FY2014 ($1.49B) … with no corroborating movement in accounts payable, long-term debt reclassification, or financing cash flows" | perturbed-frame values scale to the sealed values at the case-constant factor (411,808,775.20 / 386,788,000 ≈ 1.0647, same factor at every quoted date); the spike itself is genuine — but the sealed companyfacts contain its corroboration (ConvertibleDebtCurrent, LongTermDebtCurrent; §3), which the frozen E2 output reports as absent from its inputs | n/a — control |
| E2 s8 (score 55), top_signals[0]: "Abrupt ~3.8x spike in LiabilitiesCurrent (411.8M to 1,578.0M) across FY2014 Q1-Q2 without matching growth in current/total assets"; top_signals[3]: "Recurring multi-year SEC CORRESP/UPLOAD correspondence cycles (2006-2013)" | genuine — 1,578,049,506.02 / 1,482,170,000 ≈ 1.0647 (2013-09-28); CORRESP/UPLOAD filings appear 2006-2008, 2010-2011, 2013 in sealed metadata (gap years 2009/2012) | n/a — control |
| E2 s6 CL8 (no_flag): "Quarterly and annual data provided for Assets, AssetsCurrent, LiabilitiesCurrent, AccountsReceivableNetCurrent, InventoryNet, Revenues/SalesRevenueNet, NetIncomeLoss, and cash flow statement items" | the model's own coverage enumeration lists no debt tags — recorded here as the frozen output's self-description of its input; the actual E2 payload composition is not itself a sealed artifact | n/a — control |

## 5. WHAT THE LLM MISSED

n/a — control: no adverse mechanism to miss. The main frame kept five of
eight items at no_flag and held score 25 with zero mechanism hypotheses.

## 6. ERROR TAXONOMY (classification of the E2-layer flag)

- **No first-pass MECE attribution exists on record for E2-layer control
  flags**: RP-05 §6 covers main-frame error units only; case_07 was not an
  error unit (`review_packets/RP-06_grading_workbench.md` case_07: "본 분석
  오류 단위 아님"). This is atlas-level draft classification.
- **Interpretation (primary, draft) with an open retrieval question** — both
  breaching snapshots ride one pattern: a current-liability step the
  truncated windows see at their leading edge, uncorroborated within the
  deck as the model describes it (§4 s6 row); sealed companyfacts resolve
  the step as a convertible-debt classification event (§3). Whether the
  resolving tags reached the E2 payload cannot be closed from frozen
  artifacts (the s6 CL8 enumeration lists no debt tags; payloads are not
  sealed per-case) — R1 (DATA-first) of `scoring/error_taxonomy.md` is
  **undetermined**: interpretation if present, retrieval/DATA if omitted.
  **[OWNER REVIEW]**
- **Design/measurement context (recorded, not recomputed)** —
  `analysis/DECISION_TABLE.md` §4 states the rule's own cost: "리드타임의
  대가로 오탐 기회도 스냅샷 수만큼 늘어난다" (any-snapshot rule over ≤8
  snapshots). Unlike case_05, this is **not** near-threshold noise:
  main-frame k=5 re-draws scored 25,15,20,18,20 (mean 19.6, σ 3.3, max 25 —
  `review_packets/RP-06_hardening.md` §3-2), ~30pp below the breaching
  snapshots — signal-specific divergence, not draw jitter. L-2/L-3
  inherited limitations apply (`docs/FREEZE_REV4_HARNESS_E2.md` §3).
- **Computation** — no value errors: every quoted main-frame figure verified
  at value+date level against sealed companyfacts; ratios recompute; E2
  values scale at one case-constant factor (§4). One characterization slip:
  "monotonic margin improvement" (main CL4) overstates — FY2012 dip (§4).
- **Label-noise** — none within the design: control label verified per §2
  (exact-SIC match, index and web negative); GP-8 residual, direction
  conservative.
- **Suspected-memorization** — not indicated on the sealed draws. No probe
  row exists for this registrant (`analysis/name_probe_results.json` and
  `analysis/name_probe_results_v2ds.json` contain no XLNX/case_07 row;
  `scoring/probe_results/recognition/` covers only the 8 wave-1 treatment
  cases). Grade: memorization_suspect_condition2=false ("mentions no
  post-cutoff facts"); probe verdicts vary across draws (L-5).

## 7. CPA JUDGMENT — human_finalized: false

Draft, unaudited until owner sign-off (PROJECT.md §7). Benign readings:
- **The current-liability spike is the balance-sheet shape of a debt
  reclassification, not an accrual anomaly.** ConvertibleDebtCurrent
  ($926.8M) appears exactly when LiabilitiesCurrent steps up (2013-06-29),
  and the step partially unwinds by 2014-03-29 with LongTermDebtCurrent
  $565.0M emerging — convertible debt moving into the current
  classification window (ASC 470-10 presentation), with no income-statement
  or cash-flow counterpart. The E2 outputs' own top hypotheses describe
  precisely this ("possible misclassification or reclassification between
  current and non-current liabilities") yet scored it as risk for want of
  corroborating tags in the deck. **[OWNER REVIEW]**
- **The FY2011 inventory build (+102.7%) sits inside a +29.2% revenue
  growth year and normalized the next year** ($204.866M). **[OWNER REVIEW]**
- **The allowance decline is de minimis in absolute terms** (-$0.093M over
  three years; coverage ~1.60% → ~1.36% of net AR) against OCF exceeding NI
  every year; composition not determinable from tags. **[OWNER REVIEW]**
- **NT/amendment history is 2005-2009 only** — the main frame's CL7 placed
  it "outside the 2013-2015 focus window" and stayed no_flag; CORRESP/UPLOAD
  metadata is routine review activity, content outside sealed sources.
  **[OWNER REVIEW]**
- **Net shape**: with the full horizon and the spike's resolution visible,
  the main frame held score 25 with zero hypotheses; the E2 flag arises when
  truncated windows meet an unexplained-looking step at the leading edge
  under an any-snapshot rule — and it is not draw noise (§6).
  **[OWNER REVIEW]**

## 8. AUDIT TRANSLATION

Procedures that would clear the E2-layer flag (procedures, not conclusions):

- Obtain the convertible indenture; re-perform the current/non-current
  classification analysis for the balances reclassified at 2013-06-29
  (conversion/put/maturity windows, ASC 470-10); agree the $926.8M
  ConvertibleDebtCurrent to the indenture and its subsequent settlement.
- Confirm year-end receivables and test subsequent cash receipts for the
  FY2014 AR growth (+16.9% vs revenue +9.9%); sales cutoff at 2014-03-29.
- Obtain the allowance rollforward; recompute coverage on gross receivables
  with aging (only three annual allowance points exist in the sealed tag
  record — the E2 s6 CL8 output notes the same limit). Test FY2011
  excess/obsolete inventory reserves against the +102.7% build and
  subsequent sell-through.
- Search the 8-K record for Item 4.02 and auditor-change items (sealed
  metadata already answers: zero 4.02 across 1994-2022); read the 2006-2013
  SEC comment-letter correspondence for accounting subject matter (content
  outside sealed sources — insufficient sealed evidence).

## 9. FINANCIAL STATEMENT IMPACT

n/a — no restatement (control). No restated line items exist; the sealed
record contains no Item 4.02 8-K and no enforcement or restatement document
for this registrant (§2).

---
*Entry status: drafted (sections 7–9 pending owner finalization).*
*채점: Claude 보조 + 인간 최종 확정. 교육·정보 목적, 투자 자문 아님.*
