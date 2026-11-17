# The accounting and financial analysis pipeline: the target and the build plan

The owner's direction of 2026-11-17: build the pipeline first, to the level of a
frontier fundamental and forensic fund, so that analysing a company is only a
matter of naming it. This page is the target. `docs/HEDGE_FUND_ANALYSIS.md` is
the method catalogue it draws on (every method with its source);
`docs/research/report_2026-11-08_hedge_fund_analysis_practice.md` and
`docs/research/gap_list_2026-11-08.md` are the research it was checked against.
What this page adds is the shape: which stage does what, where the two frames
meet, what is built, and the order the rest is built in. Where it goes beyond
the research, it says so.

## 1. What "frontier level" means here

Five properties, each held by code rather than by a prompt:

1. **Every number is Python's.** The analysts read and judge; they never add,
   subtract or round (`src/analysis_check.py` refuses a digit in their own
   words; the definitions forbid the same number in words).
2. **Every judgment stands on the filing.** A claim carries a verbatim quote or
   a calculator path, and the gate drops what does not verify.
3. **The evidence standard is graded.** A difference in direction is a
   question; a residual after management's own quantified cause is an
   unexplained residual; a failed reversal or an independent series that
   disagrees is a contradiction. Python computes the residual and the reversal;
   the analyst names the label.
4. **The two frames meet in one place, and it is Python's.** The accounting
   analyst's findings move the financial numbers through named adjustments,
   each with an effect class, and Python applies them: to free cash flow, to
   operating income, to debt.
5. **Point in time, against the company's own past.** Nothing filed after the
   cutoff enters; the baseline is the company's own history, not peers; no
   composite score, no rank, no paper threshold turned into a flag.

## 2. The stages

| Stage | Does | Who | Built |
|---|---|---|---|
| fetch | the filing and what stood around it, on demand from EDGAR, held to the cutoff | Python (`src/on_demand.py`, `src/fetch_fixtures.py`, `src/cutoff_guard.py`) | yes, with the event filings (#183); not yet Form 4, the proxy statement, the 4.02 and 5.02 bodies, the financial statement data sets for segments |
| day-one checks | the release against the report, the cash-flow lines against the balance-sheet deltas, revisions of prior periods | Python | partly: articulation gaps and the revision trace exist; neither is decomposed |
| read | the numbers and the notes, verbatim | the two readers | yes |
| accounting fields | everything the accounting analyst cites, by technique family (§3) | Python (`src/calculator.py`, `src/trends.py`, `src/note_tables.py`) | about half |
| financial fields | everything the financial analyst cites (§4) | Python | about a third |
| judge | the two analysts, never merged, each on its own question | the analysts | yes |
| gate | quotes, paths and numbers verified, failures dropped and counted | Python | yes |
| bridge | the accounting adjustments applied to the financial numbers (§5) | Python | **broken**: see §5 |
| explanations over time | each explanation management gave, checked when its horizon arrives | Python | no |
| value | the DCF and the reverse DCF from free cash flow | Python and the valuation analyst | built, but idle without a price series |
| show | both analyses on one page | Python (`src/analysis_page.py`) | yes |
| measure | the grader against the owner's golden cases | the owner's `evals/` | the grader runs; no golden case is approved, so its agreement is unmeasured |

## 3. The accounting frame: can these numbers be trusted?

Grouped as practitioners group the techniques (Schilit's families, the SEC
staff's comment-letter questions, Dechow et al. on where misstatement lands:
revenue first). Built means the fields reach the analyst today.

| Family | Fields | Built |
|---|---|---|
| earnings against cash | operating cash flow over net income; three accrual measures and their gap; quarterly operating cash flow; smoothness | yes (#184) |
| day-one: statements agree | the articulation gap per account, **decomposed** into acquired balances, translation and the unexplained rest | gap yes, decomposition no |
| day-one: release against report | each statement line of the release against the report's tagged fact | no |
| revenue | days sales outstanding on average **and ending** balance; receivables, contract assets and billings against revenue; contract liabilities and their duration; concentration; receivables sold added back | average days and the extension yes; ending days and the add-back no |
| expenses held back | capitalised costs, soft assets, depreciation rate, **useful lives as data**, capex against depreciation, inventory composition | composition yes; useful lives and the capitalisation fields no |
| reserves | **one rollforward identity for every reserve family** (begin + provision − usage ± other = end), provision against usage, the release flagged; goodwill headroom as a field | ratios yes; rollforwards no |
| cash flow engineering | supplier finance, factoring, classification between operating and investing, capitalised interest | supplier finance balance yes; the rest no |
| one-time and non-GAAP | special items by year, the non-GAAP reconciliation as rows, recurring "one-time" items | no |
| acquisitions | organic against acquired growth, goodwill over consideration, earn-outs | no |
| tax | book tax against cash tax, valuation allowance and unrecognised benefits | no |
| controls and filing behaviour | auditor change and its letter, late notices, comment letters (#183); critical audit matters as fields; officer departures; non-reliance | event filings yes; the rest no |
| published models | the Beneish, Dechow and Piotroski components handed to the analyst, never the composite | baselines only |

## 4. The financial frame: how healthy is it, and what is it worth?

| Family | Fields | Built |
|---|---|---|
| normalised earnings | special items removed; share-based pay as a cost | partly |
| **earnings quality bridge** (beyond the research: the waterfall a fund's model opens with) | reported net income → normalised operating income → operating cash flow → free cash flow → free cash flow after the accounting adjustments, each step a field with its parts | the ends exist; the steps between are not one table |
| returns | return on invested capital on a lease-adjusted base, its history, incremental return on capital, DuPont in three and **five** factors, gross profitability | three-factor DuPont and current ROIC yes; the rest no |
| growth | organic against acquired, segments, order book (remaining performance obligations against next year's revenue) | no |
| efficiency | the cash conversion cycle in both conventions | average only |
| liquidity | sources and uses over a year, runway with the undrawn revolver, the **maturity ladder** | runway yes; the rest no |
| solvency | **adjusted debt** (leases, receivables sold, supplier finance, pension deficit), funds from operations over adjusted debt, coverage, covenant headroom | plain debt and coverage yes; adjusted debt no |
| capital allocation | buybacks against share-based pay, net dilution, acquisitions over the deal cycle, reinvestment rate | no |
| free cash flow, several ways | simple, after share-based pay, after acquisitions, **after lease principal**, after the accounting adjustments | four of five |
| delivery | each guided range against the first-reported actual | no |
| distress path | what would turn pressure into distress, each condition tied to a field | yes, in the analyst's reading |
| value | DCF with growth equal to reinvestment times the return on new capital; reverse DCF | built; needs a price series (the `TIINGO_TOKEN` secret, set by the owner in the environment's settings) |

## 5. The bridge between the frames

The design (`CLAUDE.md`: "the one bridge between the frames is the accounting
analyst's adjustments, which Python applies to free cash flow") is right and
the implementation stopped carrying it. The gate takes an adjustment's amount
only from a dollar cell under `terms.` or `earnings_versus_cash.`
(`ADJUSTMENT_ROOTS`, `src/calculator.py`). The note tables and the new
sections put the amounts an analyst would cite elsewhere, so the analysts'
adjustments are dropped (counted over `runs/` on 2026-11-17):

| Runs | Analyst wrote an adjustment | Python applied one |
|---|---|---|
| the first published run of a company, where the analyst wrote one | 11 | 11 |
| the 14 published reruns of 2026-10-28 to 2026-11-14 | 4 | 1 |
| the four unpublished reruns of 2026-11-15, from main with every new input | 2 | 0 |

The target, beyond the research:

- **Any dollar cell of the analysts' own view** may carry an adjustment's
  amount, except the valuation and market sections, which the analysts never
  see.
- **Each adjustment names its effect**: free cash flow (as today), operating
  income (feeding normalised operating income) or debt (feeding adjusted debt:
  receivables sold, supplier finance, a guarantee). Python applies each to its
  own field and prints the before and after.
- **A stock cannot move a flow.** A balance (an instant) may adjust debt; only a
  flow or a change between two balances may adjust free cash flow or income.
- **A free cash flow adjustment comes from the company's statement of cash flows
  or from three named items.** Earnings and debt adjustments may come from any
  dollar cell that passes the rules above (a flow or change of the trailing
  year, never cash, never a balance for a flow). A `cash_flow` amount is a line
  of the company's own statement of cash flows inside operating activities, as
  the calculator reads it (`terms.trailing_four_quarters.<line>` and the
  statement's change in a working-capital line), or the change in the supplier
  finance obligation, receivables sold or factored, or deferred or contingent
  acquisition consideration, each from the filing's own note. The statement's
  lines are disjoint and sum to operating cash flow, so each line is taken once
  and each named item once (`calculator.cash_flow_source`); a balance-sheet
  change, a total, a reserve or any other note-table change is refused as a
  `cash_flow` amount ("a cash_flow amount is a line of the statement of cash
  flows or a named off-statement item") and stays available as an earnings or
  debt adjustment. Families inferred from names could not be made disjoint in
  nine rounds of review; the statement already is.

## 6. Build plan

Each wave is a few modules, one pull request each, built in parallel. Every
row below is already in `docs/next_cycle_tasks.md` or the catalogue's build
order (§5 of `docs/HEDGE_FUND_ANALYSIS.md`), except where marked new.

1. **Wave one: the bridge and the day-one checks.**
   - the bridge of §5 (new);
   - one rollforward identity over every reserve family, with the release flag; the goodwill headroom field;
   - the earnings release's statement lines diffed against the report; the articulation gap decomposed; days on the ending balance; receivables sold added back.
2. **Wave two: the financial frame.** Adjusted debt and funds from operations;
   liquidity sources and uses and the maturity ladder; the earnings quality
   bridge (new); return on capital history and incremental return; five-factor
   DuPont; free cash flow after lease principal; buybacks against share-based
   pay; special items and normalised operating income.
3. **Wave three: the evidence standard.** The residual after management's
   quantified cause; the reversal check; the four defects of an explanation;
   every anomaly names what would resolve it.
4. **Wave four: the rest of the accounting frame.** Non-GAAP reconciliation
   rows; critical audit matters as fields; useful lives; book against cash tax;
   organic growth and acquisitions; segments (needs the financial statement
   data sets); the guidance ledger.
5. **Wave five: the filings not yet fetched.** Form 4; the proxy statement's
   pay metrics and related parties; 4.02 and 5.02 bodies.

What stays out is the research's list of practices not to adopt (peer
percentiles, management contact, paid data, composites, paper thresholds as
flags, model arithmetic, prices in the accounting frame).

## 7. How the work is done

- **Models by task** (the owner's direction of 2026-11-17, `docs/HOW_WE_WORK.md` §6):
  the specification, the expected values' sources and every review are a
  higher model's; writing the code and tests to a written specification, and
  mechanical work (fetching fixtures, moving rows, running checks), are
  Sonnet's.
- **One module per pull request**, the expected values named in the brief
  before the code exists, each from a filing read by eye, companyfacts through
  `tests/companyfacts_source.py`, or a hand computation in the test.
- **Facts first, then words.** A field that carries a sentence (a label, a
  reason) builds the sentence from a structure of facts that a test checks
  against the source, so the sentence cannot contradict itself (the lesson of
  the cost-of-debt label, eight refute rounds, #184).
- **The builder mutates its own clauses** before review and says which mutant
  each test kills, so the refute check spends its round on what the builder
  could not see.
