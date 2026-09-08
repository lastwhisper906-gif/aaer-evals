# Input spec — what we fetch and what each layer is allowed to see

Everything comes from EDGAR and is free, except prices and short interest, which
come from a free market source and never reach a reader. A User-Agent header
carrying an email-shaped contact is required on every EDGAR request. There is no
consensus data: it is not on EDGAR and it is not free.

Twelve companies: AAPL · STX · CSCO · PANW · CARR · LFUS · GNRC · CIEN · QCOM ·
ESE · TTMI · NVDA.

Two questions, never merged:

- **accounting reliability** — do these numbers reflect reality?
- **financial pressure** — is this company under pressure?

In fraud-triangle terms the first is opportunity plus traces in the numbers, the
second is incentive.

Three layers, and the two questions stay apart through all of them:

| Layer | Sees | Never sees |
|---|---|---|
| readers | the filing bundle for one company | prices, short interest, any other company |
| comparers | both reader reports plus the market table | any filing |
| supervisor | the four reports | any filing, the market table |

A comparer holds both reader reports because the layer's directory is one
directory, but it **labels only the items of its own report** — numbers versus
market labels `report_numbers.md`, notes versus market labels
`report_notes_text.md`. Labelling an item from the other report is a broken run.

Isolation is enforced by a per-run, per-agent input directory holding only that
agent's files, and a test asserts each directory's contents against the layer
rule. The agent's session is **rooted at that directory**, so a sibling
directory is not merely undeclared, it is unreachable — a prompt that says "you
never see prices" is a statement of intent, and the root is the enforcement.
Worktrees are for parallel execution only — data directories are shared across
them and isolate nothing.

Two files travel with the readers and are named here so they are routed to
somebody: `input_notes_history.md` goes to the notes-text reader, and
`input_prior_predictions.md` goes to both readers with the probability numbers
removed.

---

## 1. What we fetch

| Form | What | How | Goes to |
|---|---|---|---|
| companyfacts | every standard-taxonomy numeric fact ever filed, with the accession that filed it | `https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json`, one JSON per company | numbers reader |
| 10-K, 10-Q, /A | all numeric facts | every `us-gaap` and `dei` numeric element in the XBRL instance | numbers reader |
| 10-K, 10-Q | all notes | every element whose name ends in `TextBlock` (standard tags and company extension tags); unescape the HTML | notes-text reader |
| 10-K Item 7 / 10-Q Part I Item 2 | MD&A | HTML section split, then paragraphs | notes-text reader |
| 10-K | auditor's report including critical audit matters, Item 9A | HTML section split | notes-text reader |
| 10-Q | Item 4 controls | HTML section split | notes-text reader |
| 10-K, 10-Q | Item 1A risk factors, **diff only** | HTML section split, then the prior-period diff | notes-text reader |
| 10-K | Exhibit 21, subsidiaries, every 10-K, diffed | exhibit type from the submission's SGML header, never the filename | notes-text reader |
| Exhibit 10 | credit-agreement amendments and waivers, **on trigger only** — an 8-K 1.01, or the debt note naming one | exhibit type from the SGML header | notes-text reader |
| 8-K, all | item codes and dates | the `items` field of the submissions index | both, and events |
| 8-K 2.02 Ex. 99.1 | earnings release — guidance and outlook, non-GAAP reconciliation | HTML exhibit, then paragraphs and tables | notes-text reader, numbers reader |
| 8-K 1.01 / 4.01 / 4.02 / 5.02 body | covenant amendments, auditor change, non-reliance, officer departure reasons | verbatim full text | notes-text reader, and events |
| other 8-K (5.07 · 7.01 · 8.01 · 9.01) | item codes only | — | — |
| daily prices | open, close, split- and dividend-adjusted close | free market source, one series per ticker | **market module only, never a reader** |
| sector and market series | a broad-market series and one SIC-mapped sector ETF | free market source; SIC from `submissions.json` | **market module only, never a reader** |
| short interest | shares short, twice monthly | FINRA's twice-monthly file | **market module only, never a reader** |

**Not fetched**: business description, legal proceedings, Item 7A market-risk
tables, the bodies of other 8-K items, news, consensus, DEF 14A (a phase-two
candidate), transcripts, Form 4.

### Why companyfacts

One request per company returns every period's value from every filing, with the
accession and the filing date that reported it. That fills the trend table over
8 quarters and 5 years without fetching older filings, and it is a free
as-filed point-in-time record. It is also the independent expected value for
every trend fixture: an expected value must come from the source, never from the
first run of the code it is meant to judge.

Rules that come with it:

- **Q4 is derived**, never reported: the annual figure minus the nine-month
  year-to-date figure. Python does it.
- **The same period under several filings is a record.** A later value that
  differs from the first-reported one is a quiet-restatement trace: it goes into
  the numbers reader's input and into `events/ledger.jsonl`.
- **Company-extension tags are absent from companyfacts.** For those the XBRL
  instance stays the source.
- **Fiscal years differ** — AAPL ends in September. Any comparison across
  companies uses calendar frames (`CY2025Q3`), never the company's own quarter
  label.
- **Annual total against the sum of the quarters** is an indicator, not a
  reconciliation error to silence. Python computes it.

### Note tagging

Item 8 notes are under four-level tagging — the whole note, each policy, each
table, each number — so all of them exist as `TextBlock` elements. Do not select
from a fixed tag list. Take every element whose name ends in `TextBlock`.

MD&A, the auditor's report body, Item 9A, Item 4 and Item 1A are not tagged, so
they need an HTML section split.

**Each numeric fact records whether it came from inside a note.** A fact whose
element sits within a `TextBlock` is marked as such when it is extracted. Without
that mark the numbers reader's "seen in the notes" heading has no source and the
reader would be sorting by memory.

Companies renumber and retitle their notes, and they change tags. Match across
periods by tag name first; fall back to title similarity when an extension tag
changes. A **tag-continuity map** lives in `src/` as data and is versioned with
the rules: it names the tag pairs that are the same series under different
names, so a company that switched revenue tags still yields an unbroken series.

### Cutoff

One filing date per document. The cutoff is the filing date of the report that
triggered the run. Nothing filed later may enter the input. When a period is
reported more than once, the latest filing before the cutoff wins.

**Market data is bounded separately, and it is keyed to reaction day zero, not
to the filing date.**

> **Reaction day zero** is the filing date when EDGAR accepted the filing before
> the close, and the next trading day when it accepted after the close. Every
> market bound below counts from it.

An agent may see market data through **reaction day two**. That is the reaction
window, and it is already public by the time the run happens. Nothing beyond it
enters any input.

**Outcomes are measured outside the input.** The 60-trading-day outcome window
starts on **reaction day three** and is never visible to any layer. It is read
only by the scorer, after the horizon expires.

Keying both to reaction day zero is what keeps them from colliding. If the
window were counted from the filing date while an after-close acceptance pushed
its start forward, the window would end on the same day the outcome window
begins, and the cutoff and the score would be reading the same day.

**The read stage waits.** A full run's readers do not start until reaction day
two has closed. Running earlier hands the comparers a truncated window and makes
`not_priced` mean "the market has not finished reacting" instead of "the market
did not react".

No anonymization. No perturbation. This is forward prediction — the company's
identity is not a leak, it is the point.

### Triggers

| Trigger | Run |
|---|---|
| 10-K, 10-Q | full run, both questions, all three layers |
| 8-K 2.02 | light run, financial pressure only |
| 8-K 1.01 / 4.01 / 4.02 / 5.02 | no run — event ledger entry, and an input to the next full run |

The unit of execution is (company, accession).

**What a light run is**, exactly, because "financial pressure only" does not say
which layers wake: both readers run on the earnings release alone; the
numbers-versus-market comparer runs on the earnings-release window;
`supervisor-pressure` runs and `supervisor-accounting` does not. The
notes-versus-market comparer is skipped, because the notes are not public yet —
that is the whole reason the filing window is the interesting one. A light run
therefore produces three reports, not four, and `prediction_pressure.json`
alone.

---

## 2. Shrinking the text — the deterministic layer

Python only. No model touches this stage.

1. **Clean.** Strip headers, footers, table-of-contents links, page numbers and
   boilerplate forward-looking disclaimers. HTML becomes text; tables become
   `|`-delimited rows.
2. **Paragraph ids** of the form `{accession}:{section}:{n}`. Computed rows need
   an id too, or the numbers reader has nothing to quote: a trend-table cell is
   `{accession}:trends:{metric}:{period}`, an articulation check is
   `{accession}:articulation:{account}:{period}`, and a numeric fact is
   `{accession}:facts:{tag}:{period}`. The quote is the row as printed, and the
   gate string-matches it like any other.
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

### Alignment

Pair first, then compare. Pair a section against its prior-period counterpart by
tag name, falling back to title similarity; only then diff the paragraphs inside
the pair. Match one paragraph list against the other as a **multiset** — a table
of a hundred identical cells must not collapse onto cell one and report
ninety-nine removals. Score each paragraph for boilerplate before it counts as a
change, so a reordered or retitled section yields zero changes.

### Text depth

- **Last two years and forward**: every 10-K and every 10-Q, each diffed against
  the prior period of the same kind.
- **Older than that**: 10-K only, diffed year over year.
- **The first filing for a company** is read whole.

Everything is downloaded and committed. Only the diff reaches a reader.

---

## 3. Shrinking the text — paragraph selection (optional)

A cheap model labels paragraphs and nothing else:

`critical_estimates` · `liquidity` · `results_narrative` · `controls` ·
`management_explanation` · `boilerplate` · `numeric_restatement` · `other`

Its output is a mapping of paragraph id to label. **It writes no sentences.**

The first run uses the deterministic diff layer alone. Add this layer only if
noise turns out to be high.

---

## 4. The market table

Pure Python. One row per company per trading day.

| Column | How |
|---|---|
| raw return | close over prior close, split- and dividend-adjusted |
| market return | the broad-market series, same day |
| sector return | the SIC-mapped sector ETF, same day |
| beta | over the 250 trading days before the filing date |
| abnormal return | raw − beta × market − sector |
| reaction window | the sum of abnormal returns from reaction day zero through reaction day two |
| short-interest ratio | shares short over shares outstanding |
| short-interest two-year median | the median of that ratio over the company's own trailing two years |
| short interest above median | the ratio against that median, as a true or false |

The last two columns exist because the crowded-signal rule needs them and the
comparers do no arithmetic. A rule a comparer cannot evaluate from the table is
a rule that will be evaluated by guessing.

- **Sector** comes from the SIC code in `submissions.json`, mapped to an ETF. The
  map is data in `src/`, versioned with the rules. Its default is one ETF per
  SIC division, so the market table computes from the first run; narrowing the
  map to major groups is an improvement, not a precondition.
- **Acceptance time decides reaction day zero**, and every market bound counts
  from there. See the cutoff rule above.
- **Two windows are recorded separately** and never added together: the
  8-K 2.02 reaction day zero and the 10-Q or 10-K reaction day zero. The 8-K day is where an earnings
  surprise gets priced; the 10-Q day is where the notes first become public.
- **Short interest** comes from FINRA's twice-monthly file and is attached by
  **publication date** — settlement plus about eight business days — never by
  settlement date. Attaching it by settlement date would hand an agent a number
  the market did not have. The denominator is
  `dei:EntityCommonStockSharesOutstanding` from companyfacts.
- **Price source**: free, split- and dividend-adjusted, and it must retain
  delisted tickers, because the expansion universe keeps companies that stopped
  trading. The source is not yet chosen — see `docs/structure_changes.md` for
  the probe result — and the market module is built and tested against a frozen
  price fixture, so the choice does not block it.
- **Fama-French factor adjustment** is deferred to the first scorecard.

**Who sees it**: the comparers, and nothing else. Not a reader, not the
supervisor, not the scorer's inputs to any agent.

---

## 5. History-comparison sections

Six in the first version; the seventh comes later.

1. **Trend table.** Python computes from companyfacts, over 8 quarters and
   5 years: receivables over revenue, DSO, DSI, accruals over total assets,
   gross margin, reserve ratios (bad debt, inventory, warranty), soft-asset
   share, contract liabilities over revenue, and the non-GAAP gap — each with
   year-over-year and quarter-over-quarter change. One further column: **book
   value and earnings with research and development capitalized**, because four
   of the twelve are companies whose reported book value carries little
   information. The model never does arithmetic.
2. **Articulation checks.** Python compares the cash-flow statement's changes in
   receivables, inventory and payables against the balance-sheet changes in the
   same accounts, net of disclosed acquisitions and foreign-exchange effects. A
   gap is `articulation_gap`. This is the first new input because it needs no
   model, and because its magnitude is worth reading whether or not it crosses
   the flag threshold — the gap is reported as a number from the first run, and
   what size of gap raises a flag is set at rules v0.1.
3. **Note change history.** For the key notes — revenue recognition policy,
   critical accounting estimates, contingencies, debt, related parties,
   subsequent events — only the added, removed and changed paragraphs per
   period, in date order. Never several periods of full text. Contingencies,
   related parties and subsequent events may be carried in full for 4 to 8
   periods, because they are short.
4. **Our own prior predictions and outcomes for this company.** Flag lists from
   previous runs, management explanations and whether they materialized, and
   events that occurred. **Omit the probability numbers** — otherwise the model
   copies its own past scores.
5. **Derived from companyfacts, alongside the trend table**: the fourth-quarter
   figure and whether it is a dump, and the quiet-restatement trace.
6. **Formula-baseline inputs.** The raw terms every formula baseline needs —
   Beneish M-score, accruals over assets, net operating assets over lagged
   total assets, Piotroski F-score, Ohlson O-score, Altman Z — are assembled
   here so the baselines and the trend table read the same numbers.
7. *(next version)* Proximity to the 30 past cases, computed by Python from the
   trend-table ratios. A hint, nothing more.

---

## 6. The committed bundle

Everything every layer saw is committed under `runs/{ticker}/{accession}/`. Each
agent's input directory is committed as what it saw, and the directory is the
isolation boundary.

```
input_numbers.json            every numeric XBRL fact
input_companyfacts.json       the standard-taxonomy history, as fetched
input_trends.json             the trend table, articulation checks, baselines' inputs
input_notes.md                the notes after the diff layer
input_notes_history.md        the note change history
input_mdna.md                 MD&A after the diff layer
input_exhibits.md             Exhibit 21 diff, and any Exhibit 10 pulled on trigger
input_risk_factors.md         Item 1A, diff only
input_8k.md                   8-K item codes, and bodies for 1.01/4.01/4.02/5.02
input_prior_predictions.md    prior flags and outcomes, probabilities removed
input_market.json             the market table — comparers only
input_manifest.json           paragraph ids, exclusion reasons, dropped-item
                              counts, rules version, cutoff, served models
report_numbers.md             the numbers reader
report_notes_text.md          the notes-text reader
report_numbers_vs_market.md   the numbers-versus-market comparer
report_notes_vs_market.md     the notes-versus-market comparer
prediction_accounting.json    the accounting reliability output
prediction_pressure.json      the financial pressure output
explanations.json             management explanations and their judgments
baselines.json                every formula baseline, computed by Python
control_single_agent_accounting.json
control_single_agent_pressure.json
control_shuffled_accounting.json
control_shuffled_pressure.json
```

Size targets per layer, for a 10-K, and about half of each for a 10-Q:

| Layer | Target |
|---|---|
| numbers reader | 8–12k tokens — the trend table, articulation checks, restatement traces, baseline inputs |
| notes-text reader | 12–20k tokens — the diffed prose only |
| each comparer | 4–8k tokens — two reports plus the market table |
| each supervisor | 3–6k tokens — the four reports |

An 8-K 2.02 light run is 2–3k tokens.

---

## 7. Code carried over from the archived repo

These are the only pieces worth reusing. They stay under `archive/` until they
are ported into `src/`.

| Piece | Where it is now | What we want from it |
|---|---|---|
| cutoff guard | `archive/pipeline/cutoff_guard.py` | the date gate; needs a text loader added |
| quote matching | `archive/tools/memo_verify.py` | string-matching a quote against committed input |
| hash and timestamp | `archive/tools/forward_seal.py` | the hash and OpenTimestamps part only |
| 8-K item codes | `archive/pipeline/payload_v2_extract.py` | parsing the submissions-index `items` field |
| fingerprint and model pin | `archive/pipeline/runner.py` | the served-model check |
