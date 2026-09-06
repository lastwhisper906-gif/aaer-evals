# Input spec — what we fetch and what the predictor is allowed to see

Everything comes from EDGAR and is free. A User-Agent header is required on every
request. There is no consensus data: it is not on EDGAR and it is not free.

Twelve companies: AAPL · STX · CSCO · PANW · CARR · LFUS · GNRC · CIEN · QCOM ·
ESE · TTMI · NVDA.

Two questions, never merged:

- **accounting reliability** — do these numbers reflect reality?
- **financial pressure** — is this company under pressure?

In fraud-triangle terms the first is opportunity plus traces in the numbers, the
second is incentive.

---

## 1. What we fetch

| Form | What | How | Used by |
|---|---|---|---|
| 10-K, 10-Q, /A | all numeric facts | every `us-gaap` and `dei` numeric element in the XBRL instance | both |
| 10-K, 10-Q | all notes | every element whose name ends in `TextBlock` (standard tags and company extension tags); unescape the HTML | accounting reliability |
| 10-K Item 7 / 10-Q Part I Item 2 | MD&A | HTML section split, then paragraphs | both |
| 10-K | auditor's report including critical audit matters, Item 9A | HTML section split | accounting reliability |
| 10-Q | Item 4 controls | HTML section split | accounting reliability |
| 8-K, all | item codes and dates | the `items` field of the submissions index | both, and events |
| 8-K 2.02 Ex. 99.1 | earnings release — guidance and outlook, non-GAAP reconciliation | HTML exhibit, then paragraphs and tables | financial pressure |
| 8-K 1.01 / 4.01 / 4.02 / 5.02 body | covenant amendments, auditor change, non-reliance, officer departure reasons | verbatim full text | both, and events |
| other 8-K (5.07 · 7.01 · 8.01 · 9.01) | item codes only | — | — |

**Not fetched**: risk factors, business description, legal proceedings, Item 7A
market-risk tables, the bodies of other 8-K items, prices, news, consensus,
DEF 14A (a phase-two candidate).

### Note tagging

Item 8 notes are under four-level tagging — the whole note, each policy, each
table, each number — so all of them exist as `TextBlock` elements. Do not select
from a fixed tag list. Take every element whose name ends in `TextBlock`.

MD&A, the auditor's report body and Item 9A are not tagged, so they need an HTML
section split.

Companies renumber and retitle their notes. Match across periods by tag name
first; fall back to title similarity when an extension tag changes.

### Cutoff

One filing date per document. The cutoff is the filing date of the report that
triggered the run. Nothing filed later may enter the input. When a period is
reported more than once, the latest filing before the cutoff wins.

No anonymization. No perturbation. This is forward prediction — the company's
identity is not a leak, it is the point.

### Triggers

| Trigger | Run |
|---|---|
| 10-K, 10-Q | full run, both questions |
| 8-K 2.02 | light run, financial pressure only |
| 8-K 1.01 / 4.01 / 4.02 / 5.02 | no run — event ledger entry, and an input to the next full run |

The unit of execution is (company, accession).

---

## 2. Shrinking the text — the deterministic layer

Python only. No model touches this stage.

1. **Clean.** Strip headers, footers, table-of-contents links, page numbers and
   boilerplate forward-looking disclaimers. HTML becomes text; tables become
   `|`-delimited rows.
2. **Paragraph ids** of the form `{accession}:{section}:{n}`.
3. **Prior-period diff.** Match paragraphs against the previous report of the
   same kind: replace numbers with placeholders, then compare similarity. A new
   or changed paragraph goes in verbatim. An unchanged one is replaced by a
   single line, `[same as prior period, n periods running]`. The first run for a
   company carries the full text.
4. **Drop tables already present in XBRL.** Keep only tables that are not — the
   non-GAAP reconciliation and the guidance table.
5. **8-K 2.02** diffs against the prior quarter's release. Outlook paragraphs go
   in verbatim, always.
6. **Always verbatim, never diffed away**: contingencies and litigation,
   subsequent events, related parties, debt and covenants, accounting changes
   and corrections.

---

## 3. Shrinking the text — paragraph selection (optional)

A cheap model labels paragraphs and nothing else:

`critical_estimates` · `liquidity` · `results_narrative` · `controls` ·
`management_explanation` · `boilerplate` · `numeric_restatement` · `other`

Its output is a mapping of paragraph id to label. **It writes no sentences.**

The first run uses the deterministic diff layer alone. Add this layer only if
noise turns out to be high.

---

## 4. History-comparison sections

Three in the first version; the fourth comes later.

1. **Trend table.** Python computes, over 8 quarters and 5 years: receivables
   over revenue, DSO, DSI, accruals over total assets, gross margin, reserve
   ratios (bad debt, inventory, warranty), soft-asset share, contract
   liabilities over revenue, and the non-GAAP gap — each with year-over-year and
   quarter-over-quarter change. The model never does arithmetic.
2. **Note change history.** For the key notes — revenue recognition policy,
   critical accounting estimates, contingencies, debt, related parties,
   subsequent events — only the added, removed and changed paragraphs per
   period, in date order. Never several periods of full text. Contingencies,
   related parties and subsequent events may be carried in full for 4 to 8
   periods, because they are short.
3. **Our own prior predictions and outcomes for this company.** Flag lists from
   previous runs, management explanations and whether they materialized, and
   events that occurred. **Omit the probability numbers** — otherwise the model
   copies its own past scores.
4. *(next version)* Proximity to the 30 past cases, computed by Python from the
   trend-table ratios. A hint, nothing more.

---

## 5. The committed bundle

Everything the predictor saw is committed under `runs/{ticker}/{accession}/`:

```
input_numbers.json            every numeric XBRL fact
input_trends.json             the trend table
input_notes.md                the notes after the diff layer
input_notes_history.md        the note change history
input_mdna.md                 MD&A after the diff layer
input_8k.md                   8-K item codes, and bodies for 1.01/4.01/4.02/5.02
input_prior_predictions.md    prior flags and outcomes, probabilities removed
input_manifest.json           paragraph ids, exclusion reasons, rules version,
                              cutoff, served model
prediction_accounting.json    the accounting reliability output
prediction_pressure.json      the financial pressure output
explanations.json             management explanations and their judgments
```

Size target: roughly 20–30k tokens for a 10-K, about half that for a 10-Q, and
2–3k for an 8-K 2.02.

---

## 6. Code carried over from the archived repo

These are the only pieces worth reusing. They stay under `archive/` until they
are ported into `src/`.

| Piece | Where it is now | What we want from it |
|---|---|---|
| cutoff guard | `archive/pipeline/cutoff_guard.py` | the date gate; needs a text loader added |
| quote matching | `archive/tools/memo_verify.py` | string-matching a quote against committed input |
| hash and timestamp | `archive/tools/forward_seal.py` | the hash and OpenTimestamps part only |
| 8-K item codes | `archive/pipeline/payload_v2_extract.py` | parsing the submissions-index `items` field |
| fingerprint and model pin | `archive/pipeline/runner.py` | the served-model check |
