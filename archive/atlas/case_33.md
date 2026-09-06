# atlas/case_33.md — Forrester Research, Inc. (FORR) — wave-1 v2-controls V18 (FALSE POSITIVE)

Authored by Claude Code, pending human audit (D15). Analytical document under D106 ② — not a scored output. 본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).

## 1. CASE HEADER

| field | value |
|---|---|
| Case ID (anonymized frame) | case_33 (scoring ID V18) |
| Cohort | wave-1 v2-controls (22-control arm) |
| Outcome class | FP (main frame, flag at score ≥50); one of the three v2-control FPs analyzed in `analysis/error_analysis.md` §5 |
| Ground-truth tier | control (no adverse label) |
| Frozen score | score 55 (`runs/rp09/scores/case_33.json`, run `original-case_33-r1`, model claude-sonnet-5, 2026-07-07) |
| Grade record | `scoring/grades_v2/controls/case_33.json` (human_finalized: true, finalized 2026-07-09 via blanket, decisions_log 참조) — dim1=0 ("output misstatement_probability=55, which is >=50, so per the control banding (p>=50 -> 0)" — raw key `misstatement_probability` quoted verbatim from the record (legacy v1 key — an uncalibrated ordinal score; see specs/RISK_SCORE_SEMANTICS.md)), dim2/dim3 null (control), dim4=2, memorization_suspect_condition2=false |

Company: FORRESTER RESEARCH, INC. (FORR), CIK 0001023313, cutoff 2016-02-28 —
copied from matched treatment T21 SCOR per GP-9 same-snapshot convention
(`data/candidates/candidates_v2_controls.json` V18; `data/evaluatee/cases_v2.json`
case_33, identity metadata only — the payload reaches the model as XBRL series
plus filing chronology, 18 documents from 10-Q filed 2011-08-04 through 10-Q
filed 2015-11-06 per `documents_used`). **This entry documents a model error
on a control company, not a company problem.**

## 2. ACTUAL EVENT

**No adverse event — control** (cleanliness basis per original selection
criteria; formalized at `docs/CONTROL_CRITERIA_v2.md`, inheriting the v1
screens including **E5 무재작성**: zero 8-K Item 4.02 filings in [cutoff −
5y, cutoff + 3y] = [2011-02-28, 2019-02-28] — `docs/CONTROL_CRITERIA_v1.md`
§3 E5). Selection record
`data/candidates/candidates_v2_controls.json` V18: group "control", ticker
FORR, SIC 8700, rev_pit 312,062,000, cutoff 2016-02-28, matched_treatment
T21; mechanics in `runs/rp09/control_group_v2.json` (T21 block): rank 1 of 18
eligible, sic_tier 3 (pool 8700), size_dist 0.0533 (revenue basis),
fye_month_dist 0. The same registrant served as wave-1 control C07,
selection-time verification recorded in `review_packets/RP-01_control_group.md`
C07 row: "색인 음성; 웹: 옵션 조사 **종결·무조치** (기록)" — AAER-index name
search negative, the mid-2000s option review noted as closed with no action.

Within the E5 label window the sealed submissions metadata
(`~/aaer-data/FORR/edgar/CIK0001023313.json` and `-submissions-001.json`,
jointly spanning filing dates 1996-09-26 → 2026-06-02) contains **zero 8-K
filings with Item 4.02**. The full history does contain three filings with
Item 4.02 — 8-K 2006-01-31 (0000950135-06-000400), 8-K/A 2006-02-02
(0000950135-06-000437), 8-K 2007-03-05 (0000950135-07-001388) — all in
2006-2007, **outside the label window and therefore outside the label's
inspection scope**; this window/input mismatch is the structural finding of
`analysis/error_analysis.md` §5 (분류 (iii), §6 below). GP-8 caveat as
recorded (error_analysis §5 공통 노트): non-enforcement is not proof of
cleanliness — an error in that direction would lower measured specificity, so
the FP finding is conservative on that axis.

## 3. SIGNALS AVAILABLE PRE-CUTOFF

Cutoff 2016-02-28. Sealed basis: the frozen output's quoted deck values,
`~/aaer-data/FORR/xbrl/CIK0001023313.json` (companyfacts), and
`~/aaer-data/FORR/edgar/` (submissions metadata). Filing narrative text
(amendment explanatory notes, NT-form reasons, deferred-revenue footnotes) is
not among the sealed sources — filing-text quotes: **insufficient sealed
evidence**. The data points the model reacted to, all filed ≤ cutoff and
verified genuine (§4):

- A 2006-2007 chronology cluster (sealed submissions): three 10-Q/A filings —
  two on 2006-02-24 (0000950135-06-001171, -001170), one on 2006-02-28
  (0000950135-06-001229); NT 10-K 2007-03-16; NT 10-Q 2007-05-10/08-09/11-09;
  the FY2006 10-K filed 2007-11-05 (0000950135-07-006703, ~8 months after the
  customary March window for a 12-31 FYE) with catch-up 10-Qs 2007-11-19/20;
  and the three Item-4.02 filings in §2. All ≥9 years before cutoff, outside
  the E5 window.
- One 10-K/A filed 2012-03-12 (0001193125-12-110072), three days after the
  10-K filed 2012-03-09 (0001193125-12-106588). Zero XBRL facts in the sealed
  companyfacts are sourced to this 10-K/A accession.
- DeferredRevenueCurrent $152.903M (2013-12-31) → $144.568M (2014-12-31),
  against SalesRevenueServicesNet $297.650M (FY2013) → $312.062M (FY2014)
  (sealed companyfacts) — a −5.5% deferred-revenue move against +4.8% revenue.
- AccountsPayableCurrent $3.644M (2010-12-31) → $1.223M (2011-12-31) →
  $0.772M (2012-12-31) → $1.024M (2013-12-31) → $0.912M (2014-12-31), against
  revenue $250.726M (FY2010) → $312.062M (FY2014).

This section describes the information set — it does not re-score the case.

## 4. WHAT THE LLM CAUGHT (what the model asserted, and on what evidence)

Frozen output `runs/rp09/scores/case_33.json`: `misstatement_probability`: 55
(legacy v1 key — an uncalibrated ordinal score; see
specs/RISK_SCORE_SEMANTICS.md) = score 55, risk_tier "elevated"; CL6 (medium)
and CL7 (high) flagged; CL1/CL2/CL3/CL5/CL8 no_flag, CL4 insufficient_data.
Top hypothesis: "Likely understatement of stock-based compensation expense in
periods prior to 2007 (consistent with the era's widespread stock-option
backdating investigations), requiring restatement of prior quarterly
financials" — a model assertion about a control company, resting entirely on
chronology metadata. Every cited figure was grep-verified against sealed
companyfacts/submissions:

| model claim (verbatim) | evidence genuine? (sealed record) | correspondence |
|---|---|---|
| "10-Q/A, filing_date=2006-02-24" … "10-Q/A, filing_date=2006-02-28" (CL7, hypotheses[0]) | genuine — sealed submissions in fact hold **three** 10-Q/A accessions on those dates (§3); all `source_accession_no` fields are "n/a" (filing-chronology metadata, not accession-cited) | n/a — control |
| "NT 10-K, filing_date=2007-03-16" + three NT 10-Q notices + "10-K, filing_date=2007-11-05 (fiscal year 2006 10-K filed ~8 months late)" (CL7, top_signals[0]) | genuine — all five dates and forms match sealed submissions | n/a — control |
| "10-K/A, filing_date=2012-03-12 (three days after 10-K filed 2012-03-09)" (CL7, top_signals[4]) | genuine dates and forms; zero XBRL facts sourced to the /A in sealed companyfacts — no financial-figure revision footprint | n/a — control |
| "DeferredRevenueCurrent=152903000 (2013-12-31)" → "=144568000 (2014-12-31)" vs "SalesRevenueServicesNet=312062000 (2014…)" (CL6, hypotheses[1]) | genuine — all three values at cited dates/accessions in sealed companyfacts | n/a — control |
| "AccountsPayableCurrent=3644000 (2010-12-31)" → "=1223000 (2011-12-31)" → "=772000 (2012-12-31)" (CL6, hypotheses[2]) | genuine — values and accession attributions verified | n/a — control |

The grade record concurs on the evidence split (dim4=2): "the top-ranked
hypothesis … is supported only by filing-chronology metadata … plus a generic
era inference, with no financial data content tied to that mechanism; the
multi-point evidence therefore does not cohere around the leading claim."

## 5. WHAT THE LLM MISSED

n/a — control: there is no adverse mechanism to miss. The model itself read
four axes benignly (CL1/CL2/CL3/CL5 no_flag) — the error is confined to
promoting the out-of-window 2006-07 chronology (CL7) and small liability
drifts (CL6) into an elevated tier (§4).

## 6. ERROR TAXONOMY

- **Label-noise / label-window (primary)** — `analysis/error_analysis.md` §5
  분류 (iii) "라벨 창 문제": "E5 무재작성 조건은 [컷오프−5y, +3y] = [2011,
  2019]만 검사하는데 페이로드 filing_chronology는 전 이력을 노출한다. …
  이 플래그는 라벨 정의와 입력 범위의 불일치를 짚은 것." The flagged 2006-07
  markers are genuine sealed history (§2-§3) the control label, by
  definition, never inspected. Under `scoring/error_taxonomy.md` MECE R1→R3
  this does not land cleanly in the MODEL bucket — a design-boundary
  attribution question; owner call. 1차 분류는 Claude, 확정은 인간.
- **Interpretation (secondary — template reuse)** — error_analysis §5 ②:
  "MRVL 실험군에서도 동일한 '10-Q/A 군집 + 2006-07 → 백데이팅' **템플릿**이
  등장 (거기서도 정답 기제와 무관) — 모델의 재사용 서사이며, 이 표본에서
  2/2 모두 판정에 도움이 되지 않았다."
- **Computation** — none found: all quoted values verified at
  value+date+accession level, chronology dates against sealed submissions
  (§4).
- **Retrieval/data boundary** — no misquoted data; every CL7/hypotheses[0]
  evidence item carries `source_accession_no: "n/a"` (chronology metadata,
  not an accession-backed quote) — the grade record's reason dim4 stops at 2.
- **Suspected-memorization** — not established on the sealed draws; probes
  split. `analysis/name_probe_results.json` row case_33 (truth_ticker
  "FORR"): guess "Forrester Research, Inc.", "medium", **recognized: true**;
  `scoring/probe_results_v2/recognition/case_33.json`: "Forrester Research,
  Inc.", "medium"; `scoring/probe_results_v2ds_wave1/recognition/case_33.json`:
  "Advent Software, Inc.", "medium" — 2 of 3 sealed probe draws name the
  registrant; probe verdicts vary across draws (L-5). Grade record:
  memorization_suspect_condition2=false ("the 'era's widespread stock-option
  backdating investigations' reference is generic historical context, not a
  case-specific disclosure"). Sealed re-draws
  `runs/draw_k3/w1_controls/draw_2/case_33.json` score 18 ("watch"),
  `.../draw_3/case_33.json` score 28 ("watch"): frozen draw-1 score 55 is the
  maximum of three, 2/3 re-draws below 50 — draw-unstable (contrast case_30,
  3/3 ≥50). Same-registrant wave-1 frame (case_15/C07): frozen score 22
  (`review_packets/RP-05_results.md` 표), k=5 re-draws 22,25,32,32,25
  (`review_packets/RP-06_hardening.md` §case_15) — 0/5 above 50 in that
  frame. Scoring stays fixed to the frozen v2 draw 1.

## 7. CPA JUDGMENT — human_finalized: false

Draft, unaudited work product until owner sign-off (PROJECT.md §7). Why each
flagged pattern is explainable in benign terms:

- **A resolved decade-old episode is not a current-period risk mechanism.**
  The 2006-07 amendment/NT cluster is real, but ended ≥9 years before the
  2016-02-28 cutoff: filings run back on cycle from 2007-11-19 onward, zero
  Item 4.02 filings appear anywhere in [2011, 2019], and the selection-time
  record notes the era's option review as closed with no action (RP-01 C07:
  "종결·무조치"). The model dated its own top hypothesis to "periods prior
  to 2007" yet let it lead a score about the cutoff-era company.
  **[OWNER REVIEW]**
- **The "backdating era" framing is a reused template, not case analysis.**
  The identical chronology-to-narrative move appears in the MRVL treatment
  case, unrelated to the answer mechanism there (error_analysis §5 — 2/2
  unhelpful in this sample); here it attached a generic era inference to
  a registrant whose review closed without action. **[OWNER REVIEW]**
- **A deferred-revenue dip is ordinary billing mechanics at this scale.**
  −$8.3M (−5.5%) in current deferred revenue against +4.8% revenue growth is
  ~2.7% of annual revenue in a subscription/retainer business, where the
  balance moves with billing timing, contract mix, and translation; the
  disclosed explanation would sit in narrative text not among the sealed
  sources — insufficient sealed evidence either way, and the output cites no
  margin/collections corroboration. **[OWNER REVIEW]**
- **The payables base is too small to carry an under-accrual thesis.** AP of
  $0.8-3.6M against ~$250-312M revenue (≈0.3-1.2%) in a research firm whose
  cost base is predominantly compensation; a $2.4M level shift is immaterial
  to income, and the hypothesis names AccruedLiabilitiesCurrent without
  citing any accrued-liabilities value. **[OWNER REVIEW]**
- **10-K/A three days after the 10-K has no revision footprint.** Zero sealed
  XBRL facts are sourced to the /A — consistent with an exhibit or
  administrative amendment (the ordinary practice recorded for the same
  pattern in case_10); the model still listed it as top_signals[4].
  **[OWNER REVIEW]**
- **Net shape of the error**: genuine but out-of-window chronology plus small
  liability drifts, promoted into an elevated tier; the decisive skipped
  question is temporal — are the flagged events inside the scored period?
  Sealed answer: no. **[OWNER REVIEW]**

## 8. AUDIT TRANSLATION

Procedures that would have cleared the flag (procedures, not conclusions):

- Read the 2006 10-Q/As and the Item-4.02 8-Ks (2006-01-31, 2007-03-05);
  confirm the episode's resolution in the FY2006 10-K (filed 2007-11-05).
- Search the 8-K record for Item 4.02 within [cutoff−5y, cutoff+3y] (sealed
  metadata already answers: zero in the window) and confirm timely filing
  status across 2011-2015 (sealed record: no NT forms after 2007-11-09).
- Diff the 2012 10-K/A against the original 10-K; identify amended items
  (sealed companyfacts: no financial facts re-filed under the /A accession).
- Roll forward FY2014 deferred revenue (opening + billings − revenue
  recognized), isolating currency-translation and contract-mix effects.
- Test AP/accrued-liabilities cutoff at the 2011-2014 year-ends with a search
  for unrecorded liabilities, sizing the $2.4M AP level shift; re-run the
  selection-time enforcement screens (E4-v2 index match plus web backstop).

## 9. FINANCIAL STATEMENT IMPACT

n/a — no restatement (control). No restated line items exist within the
label window: zero Item 4.02 8-Ks in [2011, 2019] and no enforcement or
restatement document for this registrant in the sealed record (§2). The
2006-07 amendments predate the label window and their line-item content is
not among the sealed sources — not determinable, outside the label's scope.

---
*Entry status: drafted (sections 7–9 pending owner finalization).*
*채점: Claude 보조 + 인간 최종 확정. 교육·정보 목적, 투자 자문 아님.*
