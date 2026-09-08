# Checklist — what we look at, what we try to get right, how we score it

"Indicator" means three different things. Always say which.

| Kind | Meaning | Example |
|---|---|---|
| **input indicator** | a signal read from the filing | receivables growing faster than revenue; the revenue-policy wording changed |
| **prediction target** | something to be checked in the future | next quarter's operating cash flow; an immaterial error correction within 12 months |
| **evaluation metric** | how right the prediction was | forecast error, direction hit rate, alert precision, lead time, Brier |

This document is the readable version. The frozen, machine-read copy lives under
`rules/` and is versioned: `rules/checklist_v0.1.md`, `rules/targets_v0.1.md`,
`rules/thresholds_v0.1.json`. Each prediction is scored against its own rules
version. An improvement applies from the next version. Nothing is retroactive.

The `rules/` files do not exist yet — they are written once the flag distribution
over the 30 past cases has been produced. Until then this document is the draft.

---

## 1. Input indicators — accounting reliability (33)

Thirty-two from the filing and its filed history, plus one that compares the
earnings release with the 10-Q. "Computed by" is Python where a number decides it
and the model where a sentence decides it. An LLM answer is always `flag` /
`no_flag` / `insufficient`, plus a confidence and a verbatim quote with its
paragraph id.

### Estimates and discretion

| Key | Where | Computed by | Flags when |
|---|---|---|---|
| `estimate_change_favorable` | critical accounting estimates note, MD&A | LLM | an estimate or assumption changed and the change raised income or lowered a liability |
| `bad_debt_reserve_thinning` | XBRL allowance and receivables, reserve note | Python | allowance over gross receivables falls while receivables grow |
| `inventory_reserve_thinning` | XBRL inventory reserve and gross inventory | Python | reserve over gross inventory falls while inventory grows or DSI rises |
| `goodwill_headroom_shrinking` | goodwill and intangibles note | LLM | headroom, the discount rate or the growth assumption moved against the company, or a reporting unit is called out as near its carrying value |
| `tax_items_propping_income` | tax note, XBRL effective rate | Python then LLM | the effective rate falls materially and the note attributes it to discrete items or a valuation-allowance release |
| `warranty_reserve_thinning` | warranty rollforward | Python | accrual over revenue falls while the ending balance falls faster than revenue |

### Revenue recognition

| Key | Where | Computed by | Flags when |
|---|---|---|---|
| `revenue_policy_changed` | revenue recognition policy note, note change history | LLM | the policy wording changed in substance, not just formatting |
| `receivables_outrun_revenue` | trend table | Python | receivables growth exceeds revenue growth, or DSO rises, beyond the threshold |
| `deferred_revenue_diverging` | contract liabilities in XBRL, trend table | Python | contract liabilities over revenue moves opposite to revenue growth |
| `backlog_diverging` | MD&A, notes | LLM | disclosed backlog moves opposite to reported revenue |
| `revenue_judgment_area_new` | revenue note, critical audit matters | LLM | a new area of judgment appears — variable consideration, principal versus agent, standalone selling price, contract modification |

### Earnings quality

| Key | Where | Computed by | Flags when |
|---|---|---|---|
| `accruals_high` | trend table | Python | accruals over total assets is high against the company's own history |
| `soft_assets_rising` | trend table | Python | soft assets over total assets rises beyond the threshold |
| `capitalization_expanding` | cash-flow statement, policy notes | Python then LLM | capitalized cost rises relative to the expensed equivalent, or a policy note widens what gets capitalized |
| `rnd_capitalization_shift` | cash-flow statement, research and development note | Python | capitalized development cost over research and development expense moves against the company's own history |
| `asset_growth_high` | trend table, companyfacts | Python | total-asset growth is high against the company's own history — the numbers side of serial-acquisition masking |
| `nonrecurring_recurring` | MD&A, non-GAAP reconciliation | LLM | an item labeled non-recurring has appeared in several consecutive periods |
| `non_gaap_gap_widening` | trend table, 8-K 2.02 reconciliation | Python | the gap between non-GAAP and GAAP earnings widens |
| `earnings_too_smooth` | trend table | Python | reported earnings vary far less than cash flow over the trailing window |

### Articulation and the filed history

Three checks that need no model and no threshold to be worth reading. All three
come from companyfacts and the three statements.

| Key | Where | Computed by | Flags when |
|---|---|---|---|
| `articulation_gap` | cash-flow statement against balance sheet | Python | the cash-flow change in receivables, inventory or payables does not match the balance-sheet change in the same account, net of disclosed acquisitions and foreign exchange |
| `fourth_quarter_dump` | companyfacts | Python | the derived fourth quarter — annual minus nine-month year-to-date — carries a disproportionate share of the year's charges, reserves or margin move |
| `quiet_restatement` | companyfacts | Python | a period reported in an earlier filing comes back with a different value in a later one, with no amendment and no correction note |

### Controls, audit and filings

| Key | Where | Computed by | Flags when |
|---|---|---|---|
| `control_weakness_disclosed` | Item 9A, 10-Q Item 4 | LLM | a material weakness or significant deficiency is disclosed, or remediation language weakens |
| `new_critical_audit_matter` | auditor's report | LLM | a critical audit matter is added, or an existing one widens |
| `auditor_changed` | 8-K 4.01, auditor's report signature | Python | the audit firm changed |
| `filing_irregularity` | submissions index | Python | a late filing, an NT 10-K or NT 10-Q, or an amendment that changes numbers |
| `finance_officer_turnover` | 8-K 5.02 | Python then LLM | the CFO, chief accounting officer or controller departed; the stated reason is read for substance |

### Related parties, contingencies and subsequent events

| Key | Where | Computed by | Flags when |
|---|---|---|---|
| `related_party_expanding` | related party note | LLM | related-party balances or transactions grow, or a new counterparty appears |
| `accounting_litigation_new` | contingencies note, 8-K | LLM | new litigation, an investigation or a comment letter touching an accounting topic |
| `subsequent_event_correction` | subsequent events note | LLM | a subsequent event corrects, reverses or restates a reported figure |

### Structure and disclosure changes

| Key | Where | Computed by | Flags when |
|---|---|---|---|
| `subsidiaries_list_shift` | Exhibit 21, diffed against the prior 10-K | LLM | subsidiaries are added, removed or renamed in a pattern the filing does not explain — a new holding entity, a jurisdiction shift, an entity that disappears without a disposal |
| `risk_factor_new_item` | Item 1A, diff only | LLM | a new adverse risk factor appears, or an existing one widens in substance rather than wording |

### Across documents

| Key | Where | Computed by | Flags when |
|---|---|---|---|
| `release_vs_10q_gap` | 8-K 2.02 release against the 10-Q for the same period | Python | a headline figure differs between the release and the filed statement |

---

## 2. Input indicators — financial pressure (17)

### Results against expectations

| Key | Where | Computed by | Flags when |
|---|---|---|---|
| `missed_own_outlook` | prior 8-K 2.02 outlook against the reported figure | Python | the company came in below the range it published for the same period |
| `gross_margin_falling` | trend table | Python | gross margin falls year over year beyond the threshold |
| `operating_leverage_bite` | trend table | Python | operating expenses grow faster than revenue |
| `guidance_cut` | 8-K 2.02 outlook paragraphs | LLM | the outlook is lowered, narrowed downward or withdrawn |
| `non_gaap_adjustment_new` | non-GAAP reconciliation | LLM | a new adjustment line appears |

### Liquidity and capital

| Key | Where | Computed by | Flags when |
|---|---|---|---|
| `cash_runway_short` | XBRL cash and operating cash flow | Python | cash plus undrawn facilities against the trailing burn falls under the threshold |
| `maturity_wall` | debt note | Python then LLM | a large maturity falls inside the next four quarters |
| `covenant_pressure` | debt note, 8-K 1.01, Exhibit 10 | LLM | covenant headroom is discussed, a covenant is amended, or a waiver is obtained |
| `new_financing` | cash-flow statement, debt note, 8-K 1.01 | Python then LLM | new borrowing or an equity issuance on terms worse than the last one |
| `net_stock_issuance` | cash-flow statement, companyfacts shares outstanding | Python | shares outstanding rise net of buybacks — issuance predicts weak returns, and a company issuing into weakness is under pressure |
| `shareholder_return_cut` | cash-flow statement, MD&A | Python | the dividend is cut or the buyback is suspended or sharply reduced |
| `going_concern_language` | liquidity discussion, notes, auditor's report | LLM | substantial-doubt or going-concern language appears |

A separate `covenant_amendment_filed` is **not** added: `covenant_pressure`
already flags on an amendment or a waiver, and now reads the Exhibit 10 pulled on
that trigger. One indicator, one key.

### Narrative signs of operating pressure

| Key | Where | Computed by | Flags when |
|---|---|---|---|
| `customer_concentration_shift` | segment and concentration notes, MD&A | LLM | a major customer's share moves sharply, or one is lost |
| `inventory_slowing` | trend table | Python | DSI rises while revenue growth falls |
| `backlog_falling` | MD&A, 8-K 2.02 | LLM | disclosed backlog or bookings fall |
| `restructuring_or_pricing_pressure` | MD&A, restructuring note | LLM | a restructuring is announced or widened, or price competition is named as a cause |
| `known_trends_new_item` | MD&A known trends and uncertainties | LLM | a new adverse trend is named that was not there last period |

---

## 3. Market comparison labels

The comparers, and only the comparers, put a filing's findings next to what the
market did. Every item a comparer touches gets exactly one label.

| Label | Means |
|---|---|
| `priced_in` | the reaction window already moved in the direction the item implies |
| `not_priced` | the reaction window shows no move the item can account for |
| `opposite_direction` | the reaction window moved against what the item implies |

Two comparers, two lenses, and neither sees a filing:

- **numbers versus market** — the fundamentals trend against the abnormal-return
  trend. What it is looking for is divergence.
- **notes versus market** — for each notes-reader item, did the market react in
  the **10-Q or 10-K filing window**, not the 8-K window. The 8-K day prices the
  earnings surprise; the filing day is the first time the notes are public.

**The crowded-signal rule.** An item on a company whose short-interest ratio is
already above its own two-year median is labeled `priced_in` unless the reaction
window contradicts it. Short sellers read the notes; a crowded signal is not an
unread one.

**The supervisors weight `not_priced` items first.** An item the market has
already absorbed carries less; an item nobody has reacted to is where a
prediction can still be wrong in a useful way. Neither supervisor sees the market
table itself — it reads the labels the comparers assigned.

---

## 4. Management explanations

A management explanation is a sentence in MD&A or the notes where management
explains the cause of a number.

The first version covers **only explanations about receivables, inventory and
reserves**. Each one is recorded in `explanations.json` with:

- the verbatim text and its paragraph id
- the number being explained
- the observable consequence it implies — for example, "DSO falls next quarter"
- the horizon
- the **accounting reliability** judgment: support sufficient / insufficient /
  cannot judge, with quotes
- the **financial pressure** prediction: the probability that the implied
  consequence materializes

The next run records materialization in the event ledger.

**Non-materialization is not the same as the explanation being false.** The two
questions make different predictions about the same sentence: financial pressure
asks whether the implied consequence materializes; accounting reliability asks
whether the support was sufficient, and whether corrections or control problems
follow in the related accounts. The two scores are never merged.

---

## 5. Prediction targets

Start narrow. A target earns its place by being checkable for all twelve
companies on a fixed clock.

### Both questions — the direction of the abnormal return

Under **each** question, separately, and never merged: the probability that the
60-trading-day abnormal return from the third trading day after the filing is
positive. Every filing produces this value. `insufficient` is an allowed answer,
it is recorded, and the count of `insufficient` answers is reported next to the
score — a model that abstains its way to a good Brier has not predicted
anything.

Scored with **Brier** and **direction hit rate**.

Two things go in the scorecard template next to this row, now, not later:

> Post-2006 drift is close to zero outside small capitalizations (Martineau
> 2022). A coin-flip direction score on these twelve is the expected result, not
> a failure. The drift that survives is what the 8-K day did not price and the
> 10-Q later disclosed, which is exactly the window this pipeline reads.

> Published anomalies lose roughly 58% of their margin after publication (McLean
> and Pontiff 2016). Any margin over a baseline that was measured on past cases
> is reported next to the sentence "expect about half of this forward".

### Financial pressure — three continuous values, every quarter

- next quarter's revenue growth, year over year
- next quarter's operating margin
- next quarter's operating cash flow

Predict direction and magnitude for each.

**A naive baseline is mandatory**: the same quarter last year, scaled by the
trailing-four-quarter average growth. Whether the model beats that baseline is
the first line of the financial-pressure scorecard.

### Financial pressure — events, with horizons

| Event | Horizon |
|---|---|
| guidance cut or withdrawal | 1 quarter |
| impairment charge | 12 months |
| covenant amendment or waiver | 12 months |
| dividend cut or buyback suspension | 12 months |
| equity raise or emergency financing | 12 months |
| going-concern language | 12 months |

### Accounting reliability — primary year-one targets

These are the ones that actually happen inside a year.

| Target | Horizon |
|---|---|
| immaterial error correction, a "little r" | 12 months |
| SEC comment letter on an accounting topic | 12 months |
| numeric gap between the 8-K release and the 10-Q | 1 quarter |
| late filing | 12 months |
| amendment that changes numbers | 12 months |
| post-hoc verdict on whether a management explanation was supported | at the next run |

### Accounting reliability — long horizon, tracked alongside

| Target | Horizon |
|---|---|
| new material weakness | 24 months |
| auditor change | 24 months |
| restatement, non-reliance | 36 months |
| SEC investigation or AAER | open-ended |

Zero of these in year one is the expected outcome, not a failure. Year-one
accounting reliability is read as a specificity test — does the pipeline honestly
say "clear" when nothing is wrong. That sentence goes at the top of the results
document.

Impairment is where the two questions meet. Classify it as a financial-pressure
event, and cross-record whether `goodwill_headroom_shrinking` had been flagged
beforehand.

---

## 6. Ground truth

Ground truth is the **first-reported value** — the figure in that quarter's
8-K 2.02 earnings release.

If the 10-Q differs, record the difference as `release_vs_10q_gap`.

When a later correction arrives — an amendment, a restatement — keep the
corrected value but **never change the original score**. The correction analysis
is written as a separate file, and the correction itself is an accounting
reliability event.

---

## 7. Output schemas

### The two predictions

The same shape for both questions.

```json
{ "question": "accounting_reliability" | "financial_pressure",
  "rules_version": "0.1",
  "checklist": [ {"key": "", "finding": "", "confidence": 0,
                  "evidence": [{"upstream_item_id": ""}]} ],
  "continuous": [ {"key": "", "point": 0, "direction": "", "low": 0, "high": 0} ],
  "events": [ {"key": "", "p_within_horizon": 0} ],
  "explanations": [ {"id": "", "support": "sufficient|insufficient|unknown",
                     "realization_p": 0} ],
  "market_direction": {"p_up": 0, "basis": []},
  "tier": "elevated" | "watch" | "clear",
  "top_signals": [] }
```

`continuous` is financial pressure only. `top_signals` holds at most five keys.
`market_direction.basis` holds the upstream item ids the probability rests on;
`p_up` may be `"insufficient"` instead of a number, and that is recorded and
counted.

### A reader item

Written by the numbers reader and the notes-text reader. The quote is verbatim
and Python string-matches it against that reader's committed input.

```json
{ "id": "", "what_changed": "", "account": "",
  "expected_direction": "up" | "down" | "none",
  "horizon": "", "quote": "", "paragraph_id": "" }
```

The notes-text reader is forbidden from arithmetic; `expected_direction` is what
the prose says the numbers should do, not a computed value. Findings the numbers
reader takes from tables inside the notes go under a separate heading, **seen in
the notes**, so a later split into a separate notes-numbers reader does not have
to re-derive which was which.

### A comparer item

```json
{ "id": "", "upstream_item_id": "",
  "label": "priced_in" | "not_priced" | "opposite_direction",
  "window": "filing" | "earnings_release",
  "abnormal_return": 0, "short_interest_above_median": false,
  "reasoning": "" }
```

`upstream_item_id` is checked against the upstream report. An item whose
citation does not resolve is dropped before the next layer sees it, and the drop
count goes into `input_manifest.json`.

---

## 8. Evaluation metrics

| Kind | Metrics |
|---|---|
| continuous | error (MAPE), direction hit rate, improvement over the naive baseline |
| events | Brier, alert precision and recall, **lead time** from flag date to event date |
| market direction | Brier, direction hit rate, share of `insufficient` |
| explanations | post-hoc agreement rate on the support judgment; Brier on materialization |
| across the twelve | ranking, and AUC once events exist |

All of it is recomputed deterministically from `runs/` and `events/`. Nothing is
carried by hand.

### Scorecard rows

Every baseline and control is scored in the same scorecard as the pipeline, on
the same targets, and none of them is ever merged into the pipeline's number.

**Accounting reliability scorecard — in this order:**

| Row | What | Computed by |
|---|---|---|
| `beneish_m_score` | the Beneish M-score. **The first row.** Beneish and Vorst (2022) found it the most useful of seven fraud models; if the layered structure does not beat it on the accounting targets, the scorecard says the structure adds nothing | Python |
| `accruals_over_assets` | accruals over total assets | Python |
| `net_operating_assets` | net operating assets over lagged total assets (Hirshleifer and others, 2004) | Python |
| `note_cosine_similarity` | cosine similarity of consecutive note text — the Lazy Prices signal | Python |
| `loughran_mcdonald_negative` | the negative-word share of the notes and MD&A, on the Loughran and McDonald list, with the dictionary's hash recorded | Python |
| `single_agent_accounting` | the single-agent control | one model call |
| `shuffled_accounting` | the shuffled-report control | one model call |
| `pipeline_accounting` | the three-layer pipeline | the pipeline |

**Financial pressure scorecard:**

| Row | What | Computed by |
|---|---|---|
| `naive_forecast` | same quarter last year, scaled by trailing-four-quarter growth | Python |
| `piotroski_f_score` | the Piotroski F-score | Python |
| `ohlson_o_score` | the Ohlson O-score | Python |
| `altman_z_score` | the Altman Z-score | Python |
| `short_interest_ratio` | the ratio alone, as a signal | Python |
| `single_agent_pressure` | the single-agent control | one model call |
| `shuffled_pressure` | the shuffled-report control | one model call |
| `pipeline_pressure` | the three-layer pipeline | the pipeline |

**The two controls, and what each one falsifies:**

- **single-agent baseline** — one call per question, the same model as the
  supervisor, handed the whole bundle plus the market table, answering the same
  schema. If the layers do not beat it, the structure is decoration, and the
  scorecard says so in those words.
- **shuffled-report control** — the supervisor is fed one company's numbers
  report together with **another company's** notes report, on every pilot
  filing. If its score matches the real run, the supervisor is not reconciling
  the two reports, it is pattern-matching one of them.

**No composite rank.** Indicators are never combined into a single score ranked
across companies. That is the crowded thing factor funds already do, and it is
not what this pipeline is testing. The formula baselines are baselines, not
inputs.

---

## 9. The two-by-two

Thresholds live in `rules/thresholds_v0.1.json`.

- accounting reliability **low** = tier `elevated`, or 4 or more of the 33 flags
- financial pressure **high** = tier `elevated`, or 3 or more of the 17 flags

The flag counts grew from 26 and 16 while these two numbers stayed where they
were, which loosens both tiers. That is deliberate: a threshold is the owner's
to move, and moving one while adding the indicators it counts would hide the
change inside the addition. The drift is named here so it is visible when the
flag distribution over the 30 past cases is read.

The test is whether the event rate in the "low accounting reliability × high
financial pressure" cell is higher than in the other three cells. The "low × low"
cell is reported separately — an accounting anomaly with no pressure behind it.

These are initial values. The owner adjusts them once, after seeing the flag
distribution over the 30 past cases. If the owner does not adjust them, the
initial values take effect as they are.

---

## 10. The twelve are a pipeline test

The twelve are among the most-read filings on earth, and any model reading them
already knows how 2025 and 2026 turned out. Nothing observed on these twelve is
recorded as an observation about signal, anywhere — not in a results document,
not in a scorecard note, not in `lessons.md`. The word for what the twelve
produce is **pipeline check**: the parsers ran, the layers stayed isolated, the
quotes resolved, the scorer computed.

Claims about signal come from the forward cycle only, on filings that did not
exist when the rules version was frozen.
