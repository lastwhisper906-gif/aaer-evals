# atlas/TEMPLATE.md — Accounting Error Atlas entry template (v1)

> **Authority: D106 ② (ERROR_ATLAS_v1, `governance/FEEDBACK_RESPONSE_v1.md`,
> owner-signed 2026-07-20).** Atlas entries are **analytical documents, not
> scored outputs** — they alter no frozen metric, touch no graded record, and
> feed no metric recomputation. Base template: `output/GIL_memo_v1.md`
> (citation discipline, facts-vs-hypothesis separation, sign-off format).

## Entry conventions (binding for every entry)

- **Header line (every entry, verbatim)**: "Authored by Claude Code, pending
  human audit (D15). Analytical document under D106 ② — not a scored output.
  본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5)."
- **Score language**: `score NN` only (RP-16/D91). Probability language
  (%, "probability", "likelihood" applied to model scores) is banned. The
  frozen output field name `misstatement_probability` may appear only when
  citing the raw JSON key verbatim, immediately glossed as "(legacy v1 key —
  an uncalibrated ordinal score; see specs/RISK_SCORE_SEMANTICS.md)".
- **Citation rule**: every factual claim cites (a) a frozen repo artifact by
  path, (b) a filing at accession-number level, or (c) an enforcement/
  restatement document in `~/aaer-data/{TICKER}/` (manifest-pinned,
  `data/manifests/aaer_data_manifest.json`). Quotes are verbatim and must be
  grep-verifiable in the cited source. If sealed evidence does not support a
  section, write **"insufficient sealed evidence"** — never reconstruct from
  memory, never fresh-search.
- **Vocabulary**: for control companies (FP entries) and any post-cutoff
  company state, PROJECT.md §6 applies — facts/hypothesis separation, no
  fraud vocabulary directed at the company; an FP entry documents a **model
  error**, not an allegation. Holdout labels are provisional (restatement/
  4.02) — never conflate with AAER-confirmed fraud.
- **Ground-truth tier vocabulary**: `AAER-confirmed` (Task 1 cohorts) vs
  `provisional-4.02/restatement` (holdout). State the tier in every header.

---

## 1. CASE HEADER

| field | value |
|---|---|
| Case ID (anonymized frame) | case_NN / hc_NN |
| Cohort | wave-1 / wave-1 v2-controls / wave-2 / holdout |
| Outcome class | TP / FP / FN / TN-flagged (state frame + threshold: main frame, flag at score ≥50 unless noted) |
| Ground-truth tier | AAER-confirmed / provisional-4.02 / control (no adverse label) |
| Frozen score | score NN (`runs/<cohort>/.../case_NN.json`) |
| Grade record | `scoring/grades*/.../case_NN.json` (human_finalized: value as recorded) |

## 2. ACTUAL EVENT

AAER allegation or restatement mechanism. Specific GAAP topics implicated
(e.g., ASC 606, ASC 450, ASC 330 — or pre-codification equivalents for older
cases, stated as such). Cite: AAER no. + document file in
`~/aaer-data/{TICKER}/` with paragraph reference where the text is sealed
locally; `data/candidates/*.json` `scheme_summary` as the registered summary;
restatement 8-K accession for holdout. Controls: "No adverse event — control
(cleanliness basis per original selection criteria; see
docs/CONTROL_CRITERIA_v1/v2)".

## 3. SIGNALS AVAILABLE PRE-CUTOFF

What a diligent analyst could have seen before the case cutoff date, quoting
filing text with accession-level citations (sources: the frozen evaluatee
input deck `data/evaluatee/cases*.json` and sealed filings under
`~/aaer-data/{TICKER}/edgar/`). This section describes the information set —
it does not re-score the case.

## 4. WHAT THE LLM CAUGHT

Verbatim quotes from the model's frozen output (`runs/...`), then the
correspondence table:

| model claim (verbatim) | enforcement/restatement reference | match quality |
|---|---|---|
| ... | AAER ¶ / order §, or scheme_summary | exact mechanism / right account wrong mechanism / right direction only / unrelated |

Match-quality enum is closed (4 values). For FP/control entries this section
records what the model asserted and against what evidence, with no
ground-truth counterpart ("n/a — control").

## 5. WHAT THE LLM MISSED

Pre-cutoff signals (from §3's sealed information set) not surfaced in the
frozen output. "None identified from sealed evidence" is a valid answer.

## 6. ERROR TAXONOMY

Classification per `scoring/error_taxonomy.md` families, expressed in the
atlas vocabulary: computation / retrieval / interpretation / label-noise /
suspected-memorization. The memorization column cites contamination probe
results only (`analysis/name_probe_results*.json`,
`scoring/probe_results*/`, `analysis/gate_k5_results.json`) — with the
specific draw named (probe verdicts vary across draws; L-5).

## 7. CPA JUDGMENT — human_finalized: false

Draft accounting analysis of WHY the model was right or wrong in accounting
terms. Every judgment call is flagged inline with **[OWNER REVIEW]**. This
section is unaudited work product until owner sign-off (PROJECT.md §7).

## 8. AUDIT TRANSLATION

Substantive procedures the flag would motivate (confirmations, cutoff
testing, reserve recomputation, segment margin analytics, etc.) — framed as
procedures, not conclusions.

## 9. FINANCIAL STATEMENT IMPACT

Restated line items and direction **where determinable from sealed source
documents** (enforcement order text, restatement 8-K); otherwise
**"not determinable"** — never estimate, never compute new figures.

---
*Entry status: drafted (sections 7–9 pending owner finalization).*
*채점: Claude 보조 + 인간 최종 확정. 교육·정보 목적, 투자 자문 아님.*
