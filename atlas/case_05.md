# atlas/case_05.md — Perry Ellis International, Inc. (PERY) — wave-1 control C05 (TN-FLAGGED)

Authored by Claude Code, pending human audit (D15). Analytical document under D106 ② — not a scored output. 본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).

## 1. CASE HEADER

| field | value |
|---|---|
| Case ID (anonymized frame) | case_05 (scoring ID C05) |
| Cohort | wave-1 (8-control arm) |
| Outcome class | TN-flagged (main frame TN at score 48 — below flag at score ≥50; E2 trajectory layer flag: `analysis/decision_table.json` L4, threshold-50 cell, `flagged_control` includes case_05 — also in the T=40 and T=60 cells, not T=70) |
| Ground-truth tier | control (no adverse label) |
| Frozen score | score 48 (`runs/main/case_05.json`, run `original-case_05-r1`); no perturbed main frame — `runs/perturbed/` covers only the 8 wave-1 treatment cases (frozen asymmetric design, RP-05 J14). E2 snapshots are a separate frozen layer (§4) |
| Grade record | `scoring/grades/main/case_05.json` (human_finalized: true, RP-09 Stage 0, commit 986a893, 2026-07-07) — dim1=1 ("misstatement_probability=48 falls in the control band 30<p<50 -> 1"; legacy v1 key — an uncalibrated ordinal score; see specs/RISK_SCORE_SEMANTICS.md), dim2/dim3 null (control), dim4=3, memorization_suspect_condition2=false. E2 snapshots are ungraded — E2 = 146 evaluatee calls, 0 grader calls (`docs/FREEZE_REV4_HARNESS_E2.md` §4) |

Company: Perry Ellis International, Inc. (PERY), CIK 0000900349, cutoff
2015-08-09 — copied, as is `first_revelation_date` 2015-08-10, from matched
treatment T16 ICON per GP-9 (`data/candidates/candidates.json` C05;
`data/evaluatee/cases.json` case_05, identity metadata only). **This entry
documents model behavior across two frozen frames on a control company, not
a company problem.**

## 2. ACTUAL EVENT

**No adverse event — control** (cleanliness basis per original selection
criteria; formalized at `docs/CONTROL_CRITERIA_v1.md`). Selection record
`data/candidates/candidates.json` C05: "Control for T16 ICON: 4-axis match —
industry SIC 2320 … size rev=889972000 assets=662815000 (point-in-time at
matched cutoff) … Selected per D17"; notes: "Non-enforcement verified
2026-07-06: AAER index (3,339 entries, AAER 987-4595) name-search negative
for the registrant; secondary web search (2026-07-06) negative for SEC
accounting enforcement."
(`review_packets/RP-01_control_group.md` C05 row: "색인·웹 음성"; same
packet §4-1 records C05 as the **weakest industry match** in the control set
— apparel manufacture/brand vs ICON's pure licensing.) The sealed
submissions metadata (`~/aaer-data/PERY/edgar/CIK0000900349.json` and
`-submissions-001.json`, jointly spanning 1996-06-14 → 2018-11-01) contains
**zero 8-K filings with Item 4.02** in their entire history. GP-8 caveat as
recorded (`review_packets/RP-05_results.md` §7-1): 대조군 라벨은
"비집행"이지 "무결"이 아니다 — non-enforcement is not proof of cleanliness;
an error there is conservative for measured specificity.

## 3. SIGNALS AVAILABLE PRE-CUTOFF

Cutoff 2015-08-09. Sealed basis: the frozen output's quoted deck values,
`~/aaer-data/PERY/xbrl/CIK0000900349.json` (companyfacts), and
`~/aaer-data/PERY/edgar/` (submissions metadata). Filing narrative text
(MD&A, impairment footnotes, proxy-contest content) is not among the sealed
sources — filing-text quotes: **insufficient sealed evidence**. Data points
the model reacted to, all filed ≤ cutoff, all verified genuine (§4):

- AccountsReceivableNetCurrent $145.563M (2012-01-28) → $174.484M
  (2013-02-02) → $146.392M (2014-02-01) — a year-end spike that reversed —
  against SalesRevenueNet $955.549M → $942.451M → $882.573M (FY2011-FY2013);
  AllowanceForDoubtfulAccountsReceivableCurrent $27.752M → $25.843M →
  $21.421M at the same dates (net-AR ratios ~19.1%/~14.8%/~14.6% as computed
  in the frozen output).
- InventoryNet $183.127M (2013-02-02) → $206.602M (2014-02-01); Goodwill
  $13.794M → $6.022M and intangibles $246.681M → $211.485M over the same
  dates; NetIncomeLoss +$25.517M (FY2011) → -$22.779M (FY2013) → -$37.175M
  (FY2014) with operating cash flow positive throughout ($0.712M FY2011;
  $0.220M / $55.143M continuing-ops FY2013/FY2014).
- 2015 proxy-contest filing cluster in the deck chronology (DFAN14A,
  PREC14A, DEFA14A ×6, SC 13D/A ×4 — `runs/main/case_05.json` CL7).
This section describes the information set — it does not re-score the case.

## 4. WHAT THE LLM CAUGHT (what the model asserted, in both frames)

**Main frame** (`runs/main/case_05.json`): `misstatement_probability`: 48
(legacy v1 key — an uncalibrated ordinal score; see
specs/RISK_SCORE_SEMANTICS.md) = score 48, risk_tier "watch" — below the
frozen flag line (score ≥50), so a TN in the main analysis. CL1/CL3/CL4/CL6
flagged ("medium"), CL7 flagged ("low"), CL2/CL5/CL8 no_flag. Top
hypothesis: "Potential aggressive revenue recognition / channel stuffing
near period-end combined with an under-provisioned allowance for doubtful
accounts"; hypotheses[1] delayed markdown/obsolescence reserves;
hypotheses[2] "timing_shift" on FY2013 goodwill/intangible impairments.

**E2 trajectory layer** (perturbed variant, identity-anonymized,
case-constant deterministic perturb factor — `docs/EARLINESS_DESIGN.md` §1;
harness path per `docs/FREEZE_REV4_HARNESS_E2.md`): frozen snapshot scores
in `runs/e2/s1…s8/case_05.json` (run `perturbed-case_05-r1`), assembled in
`analysis/e2_trajectories.json` (j=0 `llm_p: null` — D71 fail-closed):
j1 42, j2 42, j3 **50** (cutoff 2014-12-10), j4 **52** (2014-09-12), j5
**52** (2014-06-11), j6 45, j7 **62** (2013-12-10, trajectory maximum), j8
**52** (2013-09-07). Flag rule as recorded (`analysis/DECISION_TABLE.md`
§4; `decision_table.json` L4 note): "플래그 = **어느 스냅샷이든** llm_p ≥ T
… llm_p null 7 스냅샷은 fail-closed 제외" — at T=50 five snapshots meet the
rule (files `runs/e2/s3,s4,s5,s7,s8/case_05.json`), so case_05 enters
`flagged_control`. The frozen B3 series on the same grid never reaches its
flag (b3_score ≤1 at every snapshot; threshold ≥2). The rule is cited as
recorded — no recomputation.

| model claim (verbatim) | evidence genuine? (sealed record) | correspondence |
|---|---|---|
| Main: "AccountsReceivableNetCurrent=174,484,000 (2013-02-02) vs 145,563,000 (2012-01-28), +19.9% growth" vs "SalesRevenueNet=942,451,000 (FY2012) vs 955,549,000 (FY2011), -1.4% decline" | genuine — all values in `~/aaer-data/PERY/xbrl/CIK0000900349.json` at the cited dates/accessions | n/a — control |
| Main: "AllowanceForDoubtfulAccountsReceivableCurrent/AR ratio fell from ~19.1% (2012-01-28) to ~14.8% (2013-02-02) to ~14.6% (2014-02-01)" | genuine — 27,752/145,563, 25,843/174,484, 21,421/146,392 recompute to the stated ratios (allowance over **net** receivables) | n/a — control |
| Main: "InventoryNet=206,602,000 (2014-02-01) vs 183,127,000 (2013-02-02), +12.8% growth" vs revenue "-6.4% decline"; "Goodwill 13,794,000→6,022,000; Intangibles 246,681,000→211,485,000" with NI/CFO divergence (top_signals[2]-[3]) | genuine — all figures verified, incl. CFO continuing-ops 220,000 (FY2013) and 55,143,000 (FY2014) | n/a — control |
| Main CL7: "DFAN14A … PREC14A … DEFA14A … SC 13D/A" 2015 cluster, called "circumstantial" in top_signals[4] | genuine as deck chronology; content not in sealed sources | n/a — control |
| E2 j7 (score 62): "Persistent and rising ratio of AccountsReceivableNetCurrent to quarterly Revenues across FY2011-FY2013 (e.g., ~51%→61%→66% in Q2 …)" | perturbed-frame values are scaled by design; the companion allowance ratio path (~19.1%→~14.3%) is consistent with the sealed-frame verified ratios | n/a — control |
| E2 j4 (score 52): "accounts payable jumped +64.5% … then reversed", AR "spike-and-reversal pattern"; j3 (score 50): "Receivables grew 19.9% … allowance … ratio fell from ~19.1% to ~14.8%" | same underlying ratio facts as the main frame, re-narrated per snapshot; the j4 output itself records the reversal of the AR spike | n/a — control |

## 5. WHAT THE LLM MISSED

n/a — control: there is no adverse mechanism to miss. In the main frame the
model itself kept CL2/CL5 at no_flag and held the composite at score 48.

## 6. ERROR TAXONOMY (classification of the E2-layer flag)

- **No first-pass MECE attribution exists on record for E2-layer control
  flags**: RP-05 §6 covers main-frame error units only; case_05's main-frame
  grade (dim1=1) was not an error unit (`review_packets/
  RP-06_grading_workbench.md` case_05: "본 분석 오류 단위 아님"). What
  follows is atlas-level draft classification.
- **Interpretation (primary, draft)** — evidence-exists over-reading: the
  flagged snapshots promote the same genuine ratio facts the main frame
  scored at 48 into scores 50-62 on shallower point-in-time windows,
  without the later-period reversal data the full deck contains (§4 j4 row
  — the reversal is visible even inside the E2 layer). Same axis as the
  Ryder over-reading recorded in RP-05 §6.
- **Design/measurement context (recorded, not recomputed)** —
  `analysis/DECISION_TABLE.md` §4 states the rule's own cost: "리드타임의
  대가로 오탐 기회도 스냅샷 수만큼 늘어난다" (any-snapshot rule over ≤8
  snapshots). Draw-noise on record: main-frame k=5 re-draws scored
  48,45,45,32,42 (mean 42.4, σ 5.5; `review_packets/RP-06_hardening.md`
  §3-2); RP-07's median per-case σ 6.3pp is the E2 design's "no change"
  reference band (`docs/EARLINESS_DESIGN.md` §4). Scores hover near the
  threshold, so single-snapshot exceedances sit inside the recorded noise
  environment. L-2/L-3 inherited limitations apply to the E2 layer
  (`docs/FREEZE_REV4_HARNESS_E2.md` §3: harness system-reminder/currentDate
  injection; no temperature pin — draw-noise bands are the resolution limit).
- **Computation** — none found: every quoted main-frame figure verified at
  value+date+accession level against sealed companyfacts (§4); ratios
  recompute.
- **Label-noise** — none within the design: control label verified per §2;
  GP-8 residual noted, direction conservative. RP-01 §4-1's "weakest
  industry match" caveat is a matching-quality note, not a label defect.
- **Suspected-memorization** — not indicated on the sealed draws. No probe
  row exists for this registrant (`analysis/name_probe_results.json` and
  `analysis/name_probe_results_v2ds.json` contain no PERY/case_05 row;
  `scoring/probe_results/recognition/` covers only the 8 wave-1 treatment
  cases). Grade record: memorization_suspect_condition2=false ("contains no
  post-cutoff facts"). Probe verdicts vary across draws (L-5).

## 7. CPA JUDGMENT — human_finalized: false

Draft, unaudited work product until owner sign-off (PROJECT.md §7). Benign
accounting readings of each flagged pattern:
- **AR spike that reverses is not a channel-stuffing footprint.** The
  FY2012 year-end step-up ($145.6M→$174.5M) fully reversed by FY2013
  year-end ($146.4M) — sustained premature-recognition schemes leave
  receivables persistently elevated; the E2 j4 output itself describes a
  "spike-and-reversal pattern". **[OWNER REVIEW]**
- **The allowance level (~15-19% of net receivables) is far above a
  bad-debt-only reserve**, consistent with a wholesale-apparel allowance
  bundling customer chargebacks/trade allowances; a decline to ~14.6%
  alongside falling receivables and sales is explainable as utilization/
  release rather than under-provisioning. Composition is not determinable
  from the sealed tag values alone. **[OWNER REVIEW]**
- **FY2013 goodwill/intangible declines with positive operating cash flow
  are the accounting shape of ASC 350 impairment in a declining-revenue
  year** — recognizing the write-down is the mechanism working, not
  evidence of a prior misstatement; the model's own hypotheses[2] labels
  the direction "timing_shift" and concedes the non-cash add-back
  mechanics. **[OWNER REVIEW]**
- **Inventory build (+12.8%) against falling sales is a markdown business
  risk, not by itself a misstatement signal**; the same deck shows the
  subsequent loss recognition (-$37.175M FY2014). **[OWNER REVIEW]**
- **Proxy-contest filings are governance activity**; the main frame itself
  called this "circumstantial" (CL7 confidence "low"). **[OWNER REVIEW]**
- **Net shape**: the main frame weighed these benign-side readings into a
  below-threshold score 48; the E2-layer flag arises when the same signals
  are re-read on truncated windows under an any-snapshot rule, near the
  threshold, inside the recorded draw-noise band (§6). **[OWNER REVIEW]**

## 8. AUDIT TRANSLATION

Procedures that would clear the E2-layer flag (procedures, not conclusions):

- Confirm year-end receivables (FY2012 spike period) and test subsequent
  cash receipts; sales cutoff testing at the 2013-02-02 period end.
- Obtain the allowance rollforward and composition (bad debt vs chargebacks/
  trade allowances); recompute coverage on gross receivables with aging.
- Test inventory obsolescence/markdown reserves against aging and
  sell-through; review the FY2013 ASC 350 impairment tests (units,
  assumptions, timing) for timeliness of recognition.
- Search the 8-K record for Item 4.02 and auditor-change items (sealed
  metadata already answers: zero 4.02 across 1996-2018); read the 2015
  proxy-contest materials for any accounting allegations (content outside
  sealed sources — insufficient sealed evidence here).

## 9. FINANCIAL STATEMENT IMPACT

n/a — no restatement (control). No restated line items exist; the sealed
record contains no Item 4.02 8-K and no enforcement or restatement document
for this registrant (§2).

---
*Entry status: drafted (sections 7–9 pending owner finalization).*
*채점: Claude 보조 + 인간 최종 확정. 교육·정보 목적, 투자 자문 아님.*
