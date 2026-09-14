# Needs judgment — the owner's inbox

This is the only place the owner is asked for anything. Nothing here is waiting:
every row names the default that is already in force, and the work went on under
it. The owner reads the whole file in one sitting when a rules version is bumped,
and reads the daily summary otherwise.

One line per item:

`what is unsettled · the default in force today · what changes when the owner decides`

A row leaves this file when the owner decides it, and the decision is recorded in
`docs/structure_changes.md` on the same day. A row is never a state the pipeline
waits in.

---

## Decided elsewhere and named in `docs/HOW_WE_WORK.md`

The six decisions that are the owner's and only the owner's — the two-by-two
thresholds, a rules-version bump, a universe change, the price source, a model
change for the predictors, and placing or lifting a stop. Everything else on this
page has a default that runs without an answer.

---

## Open

[ ] **the price source** · comparers and the `priced_in` rule are disabled, `input_prices.json` is written as the literal `unavailable`, and the first predictions publish on EDGAR inputs alone; the market module stays built and tested against the frozen price fixture · deciding turns both comparers on and lets the pattern study run, which needs fifteen years of prices and cannot start without a source. Three candidates, in this order: the **Stooq daily bulk zip**, a file download rather than an API call, blocked today by a browser check on the download link and by a password prompt on the static host; **CRSP through a Stony Brook account**, the only candidate that answers the delisted question the way the literature does, behind a login the owner would have to open; **a low-cost provider such as Tiingo or EODHD**, each of which refused the delisted ticker on a token nobody has yet. `src/probe_price_sources.py` put Lehman Brothers Holdings to all three and none served the history. The no-paid-data rule named consensus data, not prices.

[ ] **thresholds for the four numeric indicators** — `articulation_gap`, `asset_growth_high`, `rnd_capitalization_shift`, `net_stock_issuance` · all four report their value and flag nothing until rules v0.1, so they measure from the first run and contribute to no tier · deciding lets them raise a flag, which needs the distribution over the past cases first.

[ ] **the two-by-two flag thresholds** · "4 or more" on accounting and "3 or more" on pressure stand as written while the accounting count has grown from 26 to 33 keys and the pressure count from 16 to 17, which loosens both tiers · deciding tightens or keeps them; the historical distribution is what the numbers should be read off.

[ ] **the map from SIC code to sector ETF** · one ETF per SIC division, shipped with the market module, so the table computes from the first run · deciding narrows it to major group, which is a modelling choice no test can settle.

[ ] **whether the review-response branch's published results merge into this history** · they do not; the branch is closed and preserved whole at the tag `archive-review-response` · deciding either merges two published-results histories, which is a claim about the record, or leaves the tag as the only copy.

[ ] **whether the post-write plain-name hook should block the writer** · it does not: it names the code on stderr and exits 1, which Claude Code hands to the person at the keyboard and not to the agent that wrote the line · deciding buys an earlier correction at the price of an interrupted turn. Nothing waits either way — `make check` runs the same check and CI runs `make check`, so a pull request carrying a code is red.

[ ] **whether the plain-name check should read source files and directory names** · it reads `.py` and `.sh` by name only and reads a file's own name but not the directories above it, because code quotes vocabulary that is not ours · deciding widens it, which needs a rule for which quoted vocabulary is exempt.

[ ] **the letter-number codes the archived project left in `CITATION.cff`, `LICENSE` and `LICENSE-docs`** · they stay; the check reads what a branch changed and nothing changes those files · deciding would edit a published citation record and two licence texts that are not ours to edit.

[ ] **the judge line that reads "companyfacts for every numeric expectation"** · the re-judge sourced every parser expectation from the document instead and said so value by value, because no parser expectation is a financial figure · deciding restates the line for the items still to be built.

[ ] **whether the supervisor may see `docs/CHECKLIST.md`** · it does not; both supervisor prompts name the schema in a document their session root cannot reach · deciding routes a file that is not a report into a supervisor's directory, which is a change to the layer table. Nothing waits: rules v0.1 does not exist yet.

[ ] **the section fallbacks that fire on no committed filing** · the annual Item 2 fallback and the quarterly Item 3 through Item 6 fallbacks stand unjudged, exercised by none of the twelve filings on record · deciding either accepts them unjudged or sanctions a constructed filing to judge them, which is inventing the filing rather than reading it.

[ ] **whether the bundle's catalogue exception is keyed on the route or on the role** · on the role: nothing records how a document was opened, so a catalogue read through the ordinary gate and handed out unfiltered would still write a manifest row claiming its rows were filtered · deciding moves the key to the route, which changes what the manifest means. Latent today because the bundle assembler imports neither companyfacts reader.

[ ] **where the acceptance time comes from** · a free-form argument on the command line, justified by the caller; no fixture carries one and the manifests hold the filing date only · deciding either fetches and commits it per filing or leaves it an argument. It decides reaction day zero, the reaction window and the market cutoff.

[ ] **whether the pilot side of the scorecard may print a comparative verdict** · it prints one, and the suite requires those sentences · deciding reads `docs/CHECKLIST.md` on whether a labelled comparative sentence is a number or an observation.

[ ] **whether an explanation's `id` is a citation** · it is: both controls resolve it against the reports they were handed and drop and count it when it resolves against nothing. `docs/CHECKLIST.md` §7 spells the field `id` where every other citation is an `upstream_item_id`, and says only that explanations are assembled from what the supervisors say about the management explanations upstream — so the reading is inferred from that sentence and not stated · deciding either writes the sentence into §7, or names the field something the gate leaves alone, in which case an explanation about an item the crossing removed is written standing and the explanations file carries ids that resolve for nobody.

[ ] **a judge for the three dated checks that run after the model call** · the hash check, the trend-period check and the accession check all run twice, before the call and after it, and only the before-call run has tests: a test of the after-call run has to change both copies of a file while the call is in flight, which the stub model makes possible and no test does · deciding either writes that test — the stub rewrites the directory from inside `ask` — or says the second run is defence against a race nobody can reach and drops it. Today it is code with no judge, which `CLAUDE.md` calls not a task.

[ ] **the shuffled control's twelve fixed pairings against the cutoff** · `run()` never calls `partner()`: the pairing is given on the command line, and of the twelve pairings `docs/HOW_WE_WORK.md` §8 names, seven are refused because the partner's triggering report was filed after the company's own — so the crossing runs on five companies (CARR←CIEN, CIEN←CSCO, NVDA←PANW, STX←TTMI, TTMI←AAPL) and the test pair CARR/AAPL is none of the twelve · deciding either re-pairs the twelve so every pairing survives the cutoff, which changes a published table in `docs/HOW_WE_WORK.md`, or states that the crossing is a five-company control and says so where the control's coverage is reported. Nothing waits: the five run today and the seven refuse loudly rather than silently reading a later filing.
