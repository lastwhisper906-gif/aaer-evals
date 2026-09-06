# atlas/case_69.md — Artivion, Inc. (AORT) — wave-2 control W18 (FALSE POSITIVE, at-threshold)

Authored by Claude Code, pending human audit (D15). Analytical document under D106 ② — not a scored output. 본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).

## 1. CASE HEADER

| field | value |
|---|---|
| Case ID (anonymized frame) | case_69 (scoring ID W18) |
| Cohort | wave-2 (23-control arm) |
| Outcome class | FP (main frame, flag at score ≥50); one of the 5/23 wave-2 control flags dissected in `analysis/error_analysis_wave2_holdout.md` §1 — the boundary case: score 50 sits exactly at the threshold, and the frozen output's own risk_tier is "watch" |
| Ground-truth tier | control (no adverse label) |
| Frozen score | score 50 (`runs/wave2/scores/case_69.json`, run `original-case_69-r1`, evaluatee claude-sonnet-5, 2026-07-07) |
| Grade record | `scoring/grades_wave2/case_69.json` (human_finalized: true, finalized 2026-07-09 via RP-13 workbench) — dim1=0 ("Control case with misstatement_probability=50; rubric control bands are p<=30 -> 2, 30<p<50 -> 1, p>=50 -> 0, and p=50 falls in the p>=50 band" — legacy v1 key, an uncalibrated ordinal score; see specs/RISK_SCORE_SEMANTICS.md), dim2/dim3 null (control), dim4=3 (no consistency cap: "p=50 with risk_tier='watch' satisfies 40<=p<70 => watch/elevated"), memorization_suspect_condition2=false |

Company: Artivion, Inc. (AORT), CIK 0000784199, SIC 3841, cutoff 2016-12-14
— copied from matched treatment T26 (MDXG) per the same-snapshot convention
(`data/candidates/candidates_wave2.json` W18; `runs/wave2/control_group_v2.json`
T26 selection, rank 1, size_dist 0.2498, revenue basis, rev_pit $145,898,000).
Sealed formerNames (`~/aaer-data/AORT/edgar/CIK0000784199.json`): "CRYOLIFE
INC", registrant name 1996-06-10 → 2022-01-06 — the company filed as CryoLife
Inc. throughout the cutoff window. The deck entry (`data/evaluatee/cases_wave2.json`
case_69) carries identity metadata only; the payload reaches the model as
XBRL series plus filing chronology (frozen output CL8 coverage note). **This
entry documents a model error on a control company, not a company problem.**

**Boundary-score status (recorded fact)**: `analysis/error_analysis_wave2_holdout.md`
§1: "p=50은 **플래그 임계 정확히 위**. 모델 스스로 'watch'만 선언. 1점 차이로
뒤집히는 **경계 인공물** — 5건 중 최경증." The FP status is a threshold
artifact of the pre-registered ≥50 flag rule, applied as frozen.

## 2. ACTUAL EVENT

**No adverse event — control** (cleanliness basis per original selection
criteria; `docs/CONTROL_CRITERIA_v2.md`, whose E4-v2 precise name matching
covers the current name **plus all formerNames** — material given the
CryoLife-era name — and the zero 8-K Item 4.02 screen). Registered answer key
`data/candidates/candidates_wave2.json` W18: group "control", scheme_summary
null, scheme_type null. The sealed submissions metadata
(`~/aaer-data/AORT/edgar/CIK0000784199.json` and `-submissions-001.json`,
jointly 2,375 filings spanning 1996-01-09 → 2026-06-15) contains **zero 8-K
filings with Item 4.02 in the entire history**; no enforcement or
restatement document exists under `~/aaer-data/AORT/` (contents: `edgar/`,
`xbrl/` only). Standing caveat as registered (error_analysis §7): 대조군
라벨="비집행"(무결 아님) — an error in that direction lowers measured
specificity, so the FP finding is conservative on that axis.

## 3. SIGNALS AVAILABLE PRE-CUTOFF

Cutoff 2016-12-14. Sealed basis: the frozen output's quoted deck values,
`~/aaer-data/AORT/xbrl/CIK0000784199.json` (companyfacts), and
`~/aaer-data/AORT/edgar/` (submissions metadata). Filing narrative text
(MD&A, amendment notes, footnotes) is not among the sealed sources —
filing-text quotes: **insufficient sealed evidence**. The frozen output's
`documents_used` spans 2011-07-29 → 2016-10-27, all ≤ cutoff. Contents:

- **AR outgrowing revenue**: AccountsReceivableNetCurrent 15,767,000
  (2011-12-31) → 17,838,000 (2013-12-31) → 23,419,000 (2015-12-31); Revenues
  119,626,000 (FY2011) → 140,763,000 (FY2013) → 145,898,000 (FY2015)
  (10-Ks 0001193125-12-066934 through 0001193125-16-465362).
- **Deferred-revenue step-down**: DeferredRevenueCurrent 2,095,000 (2010-12-31)
  → 1,401,000 (2012-12-31), then a step between Q1 2013 (1,313,000) and Q2
  2013 (354,000), ending 316,000 (2013-12-31) — ~$1.1M vs $140.8M revenue.
- **Accrued-liability decline with an offsetting neighbor**:
  AccruedLiabilitiesCurrent (10-K scope) 5,131,000 (2011-12-31) → 2,411,000
  (2013-12-31), while EmployeeRelatedLiabilitiesCurrent **rose** 3,946,000 →
  4,886,000 and OtherLiabilitiesCurrent held ~2.1-2.5M; the same tag also
  carries a parallel 10-Q-scope series (7,269,000 / 4,579,000, same dates)
  — a presentation-scope split within the sealed facts.
- **A one-time investment gain under the FY2013 income spike**:
  CostMethodInvestmentsRealizedGainLoss = 12,742,000 (FY2013), of which
  **12,700,000 fell in Q4 2013 alone** — first filed in the FY2013 10-K
  (0001193125-14-062525) and repeated in the FY2015 10-K
  (0001193125-16-465362), the very accession the frozen output cites for
  the Q4 2013 NetIncomeLoss spike of 9,026,000. FY2014: 530,000.
- **Inventory growth**: InventoryNet 6,429,000 (2010-12-31) → 14,643,000 (2015-12-31) vs revenue +25.1%.
- **Acquisition footprint straddling Q1 2016 (pre-cutoff)**: Goodwill
  11,365,000 (2015-12-31) → 76,833,000 (2016-03-31); Assets 181,179,000 →
  297,157,000; PaymentsToAcquireBusinessesNetOfCashAcquired = 91,152,000
  (Q1 2016, 10-Q 0001193125-16-567461); sealed 8-Ks 2015-12-23 / 2016-01-25
  / 2016-02-08, Items 1.01/2.01/2.03/3.02/9.01.
- **Filing chronology**: 10-K/A filed 2016-03-25 (accn 0001193125-16-518038),
  five weeks after the original FY2015 10-K (2016-02-16); CORRESP
  2015-09-02, 2016-03-15, 2016-03-25; UPLOAD 2016-03-21. No NT notices
  post-2010.

This section describes the information set — it does not re-score the case.

## 4. WHAT THE LLM CAUGHT (what the model asserted, and on what evidence)

Frozen output `runs/wave2/scores/case_69.json`: `misstatement_probability`:
50 (legacy v1 key — an uncalibrated ordinal score; see
specs/RISK_SCORE_SEMANTICS.md) = score 50, risk_tier "watch". CL1 (high),
CL2 (low), CL4 (medium), CL6 (medium), CL7 (medium) flagged; CL3/CL5
no_flag; CL8 coverage adequate. Hypotheses: "Possible premature or
accelerated revenue recognition"; "Possible reserve/accrual release used
to boost reported earnings"; "Possible deferred inventory
write-downs/obsolescence reserves". Every cited figure was grep-verified:

| model claim (verbatim) | evidence genuine? (sealed record) | correspondence |
|---|---|---|
| "AccountsReceivableNetCurrent=17,838,000 (2013-12-31); =21,064,000 (2014-12-31); =23,419,000 (2015-12-31)" vs "Revenues=140,763,000 (FY2013); =144,641,000 (FY2014); =145,898,000 (FY2015)" (CL1) | genuine — all six values at the cited dates in sealed companyfacts | n/a — control |
| "receivables grew far faster than revenue in 2013-2015 (AR +48.5% vs revenue +22% over the period)" (hypotheses[0]; top_signals[0]) | **period label does not recompute**: from the quoted 2013-2015 values, AR +31.3% and revenue +3.6%; the stated 48.5%/22.0% recompute only from a **2011-12-31 baseline** (AR 15,767,000; FY2011 revenue 119,626,000). The divergence direction survives either window; the "2013-2015" label is wrong | n/a — control |
| "DeferredRevenueCurrent=1,401,000 (2012-12-31) fell sharply to 316,000 (2013-12-31), a 77% decline, while revenue grew 6.9% in the same year" (CL6) | genuine — values, −77.4%, and +6.9% all verify in sealed companyfacts | n/a — control |
| "AccruedLiabilitiesCurrent=5,131,000 (2011-12-31) declined to 2,411,000 (2013-12-31) even as revenue grew" (CL6) | genuine as the 10-K-scope series; the sealed record also carries a parallel 10-Q-scope series (7,269,000 → 4,579,000) and a **rising** EmployeeRelatedLiabilitiesCurrent (3,946,000 → 4,886,000) the output did not weigh | n/a — control |
| "NetIncomeLoss for Q4 2013 alone was 9,026,000, far above the typical quarterly run-rate … coincident with the reserve/deferred-revenue declines noted above" (CL6; hypotheses[1]) | value genuine; the "coincident" causal framing is contradicted by the sealed record: the same accession carries CostMethodInvestmentsRealizedGainLoss = 12,700,000 for Q4 2013 — a disclosed one-time gain larger than the entire quarter's net income | n/a — control |
| "InventoryNet=6,429,000 (2010-12-31) growing to 14,643,000 (2015-12-31), a 128% increase" vs revenue +25% (CL4) | genuine — +127.8% and +25.1% recompute exactly | n/a — control |
| "Goodwill=11,365,000 (2015-12-31) jumped to 76,833,000 (2016-03-31) coincident with a large acquisition (Assets roughly doubled from 181,179,000 to 297,157,000 …)" (CL2) | values genuine; "roughly doubled" overstates a +64% asset increase; the acquisition attribution is corroborated by sealed 8-K items and the 91,152,000 Q1 2016 acquisition cash outflow | n/a — control |
| "10-K/A filed 2016-03-25, roughly five weeks after the original 10-K filed 2016-02-16" + "Multiple CORRESP filings … (e.g., 2016-03-15, 2016-03-25)" (CL7) | dates genuine (sealed submissions; 10-K/A accn 0001193125-16-518038). The inference is not corroborated: **zero** XBRL values in sealed companyfacts are sourced to that 10-K/A — no restated figure traces to it | n/a — control |

The grade record concurs on evidence quality: "Evidence is specific and
grounded: exact provided figures with dates/accessions … each cited data point
arithmetically supports the claimed divergence" (dim4=3; the error is carried
entirely by dim1=0 under the control rubric).

## 5. WHAT THE LLM MISSED

n/a — control: there is no adverse mechanism to miss. Two benign-side
observations: (a) the model itself supplied benign readings on the
strongest axes — CL3 no_flag (OCF exceeded NI in every cited year), CL5
no_flag (earnings volatile, not smooth), CL2's acquisition attribution for
the goodwill jump; (b) the sealed set contains the benign resolver for the
signal the score leaned on hardest — the Q4 2013 income spike is fully
covered by the disclosed $12.7M one-time CostMethodInvestmentsRealizedGainLoss
in the same quarter (§3), filed pre-cutoff in accessions listed in
`documents_used`, and never mentioned in the frozen output. Whether the
concept reached the delivered payload is not determinable (§6 caveat).

## 6. ERROR TAXONOMY

- **Interpretation (primary)** — evidence-exists / reasoning-failure, benign
  over-reading at the threshold boundary: `analysis/error_analysis_wave2_holdout.md`
  §1 classifies AORT "(ii-a) 경계". RP-13 disposition
  (`review_packets/RP-13_grading_workbench.md` case_69): "finalize (오탐이나
  채점 d1=0 정확 — trust boundary 데이터. §1 오류해부 참조)" — MODEL-side
  under the R1→R3 order of `scoring/error_taxonomy.md`.
- **Computation** — one labeling defect: the headline "AR +48.5% vs revenue
  +22%" pair is real arithmetic but belongs to a 2011-2015 window, not the
  stated "2013-2015" (§4); "Assets roughly doubled" (+64%) is a second,
  minor overshoot. All other quoted values verified at value+date+accession
  level.
- **Retrieval/data boundary (caveat, not a reclassification)** — whether
  CostMethodInvestmentsRealizedGainLoss was among the delivered payload
  concepts is not determinable from entry-level sealed sources; if absent,
  the missed benign resolver in §5 would be a DATA-side gap under R1, not a
  model omission. The registered §1 attribution (MODEL, ii-a) stands as
  recorded. Owner call. **[OWNER REVIEW]**
- **Label-noise** — none within the design: control status verified per §2
  screens (E4-v2 covers the former name); 비집행 ≠ 무결 residual, conservative.
- **Suspected-memorization** — not indicated on the sealed draws.
  `scoring/probe_results_wave2/recognition/case_69.json`: company_guess
  "unknown", confidence "low"; `scoring/probe_results_v2ds_wave2/recognition/case_69.json`:
  "Digirad Corporation (best guess …) — identification uncertain",
  confidence "low" — two draws, one non-recognition, one wrong-company
  guess; probe verdicts vary across draws (L-5). Grade record:
  memorization_suspect_condition2=false ("mentions no post-cutoff facts
  such as revelation, enforcement, or outcomes").

## 7. CPA JUDGMENT — human_finalized: false

Draft, unaudited work product until owner sign-off (PROJECT.md §7). Why
each flagged pattern is explainable in benign terms:

- **The Q4 2013 spike has a disclosed one-time cause.** A $12.7M realized
  gain on a cost-method investment sits in the same quarter and sealed
  accessions, exceeding the quarter's entire $9.0M net income; the FY2013 NI
  step-up over FY2012 (16,172,000 vs 7,946,000) is fully absorbed by it net
  of the higher FY2013 tax expense. Hypotheses[1] treats the spike as
  corroborating a reserve release without weighing this. **[OWNER REVIEW]**
- **The deferred-revenue "collapse" is ~$1.1M against $140.8M revenue** —
  ≤1.5% of annual revenue at its peak, too small to carry a premature-
  revenue narrative alone; footnote text that could identify the change
  behind the mid-2013 step-down is not sealed. **[OWNER REVIEW]**
- **The accrual decline is one component, partly offset next door.**
  AccruedLiabilitiesCurrent fell ~$2.7M while EmployeeRelatedLiabilitiesCurrent
  rose ~$0.9M and OtherLiabilitiesCurrent held flat; the tag's parallel
  10-Q-scope series at materially different levels is a scope split the
  output did not address before reading a reserve release. **[OWNER REVIEW]**
- **Margins did not confirm the inventory hypothesis.** The model's own
  CL4 evidence shows gross margin drifting 64.5% → 62.2% — the wrong
  direction for deferred write-downs — and OCF exceeded NI in every cited
  year (CL3 no_flag). **[OWNER REVIEW]**
- **10-K/A ≠ restatement (same decisive test as case_10/case_49).** The
  2016 amendment contributes zero values to sealed companyfacts; the
  adjacent CORRESP/UPLOAD cluster is comment-letter correspondence whose
  content is not in the sealed metadata. **[OWNER REVIEW]**
- **Net shape of the error**: genuine, individually small or self-explained
  signals compounded to exactly 50 — the model's own tier word was "watch";
  the FP exists only because the pre-registered ≥50 rule bites at the
  boundary. Grounded-but-over-read, the wave-2 (ii-a) family signature (§1),
  in its mildest recorded form. **[OWNER REVIEW]**

## 8. AUDIT TRANSLATION

Procedures the flag would motivate (procedures, not conclusions):

- Read the 2016 10-K/A and diff against the original FY2015 10-K: identify
  amended items (cover/Part III/exhibits vs financial statements); confirm
  absence of any ASC 250 restatement or Item 4.02 disclosure. Obtain the
  2015-2016 comment letters (UPLOAD/CORRESP, §3); confirm the review
  closed without restatement.
- Vouch the Q4 2013 investment gain to disposition documentation and its
  classification; recompute FY2013 earnings excluding it for the run-rate.
- Test revenue cutoff and the deferred-revenue roll-forward around the
  Q1→Q2 2013 step-down; tie AR growth to customer/distributor aging;
  reconcile the accrued-liability 10-K vs 10-Q presentation scopes.
- Test inventory obsolescence/shelf-life reserves against expiry data and
  subsequent usage; corroborate the gross-margin trend by product line;
  vouch the Q1 2016 goodwill addition to the ASC 805 purchase price
  allocation and the 91,152,000 acquisition cash outflow.

## 9. FINANCIAL STATEMENT IMPACT

n/a — no restatement (control). No restated line items exist; the sealed
record contains no Item 4.02 8-K in the registrant's entire filing history
and no enforcement/restatement document under `~/aaer-data/AORT/` (§2).

---
*Entry status: drafted (sections 7–9 pending owner finalization).*
*채점: Claude 보조 + 인간 최종 확정. 교육·정보 목적, 투자 자문 아님.*
