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

## Decided

A row that has been decided stays on this page with `[x]`, the date, and what
the decision put in force, until the rules version that carries it is cut. A
decision that leaves no trace here reads, a month later, exactly like a default
nobody ever questioned.

[x] **the price source** — *decided 2026-09-21, recorded in `docs/structure_changes.md` the same day* · **CRSP through WRDS for the pattern study; the Tiingo free tier for the forward track; EODHD All World for one paid month if the WRDS account is refused.** CRSP is the only free source that carries the delisting return, which is the question that decides a study drawn from a past date, and Stony Brook subscribes to it — a student registers at `wrds-www.wharton.upenn.edu/register` and the school's representative approves. The forward track is twelve currently-listed companies, so it has no delisting problem at all and the free tier answers it; a company that delists mid-record is retained by Tiingo for anything after about 2015. Stooq is dropped: its download sits behind a browser check the project will not answer. The paid fallback **overrides a line already written**, and is recorded as an override rather than as a silence filled — an earlier draft of this row said the spec "says nothing at all about prices", which is false. `docs/INPUT_SPEC.md` *said* the price source is free three times: the preamble at `:3-4`, the `daily prices` and `sector and market series` rows of §1's own table at `:64-65`, and §4's **Price source** at `:273`. The third of those was amended on 2026-09-22 — §4 now records the decision and names the EODHD fallback as a departure from *free*, which is what this row said would have to happen the day it is used. The second lens caught the tense: a record that cites a line as present-tense evidence, in the same change that rewrites that line, is false about its own diff. The preamble and the §1 table rows are untouched and still say free, which is why this decision is still an override and not a tidy-up. The consensus exclusion at `:6` is about consensus. So EODHD All World for one paid month is a departure from the spec, taken only if the WRDS account is refused, and §4 is what has to be amended the day it is used. Reading the consensus exclusion as a general ban on paying would also have banned the CRSP subscription the university already pays for — but that argument does not reach the word *free* in the price rows, which this decision does override · **what is still in force until the credentials exist:** `$TIINGO_TOKEN` is unset and `~/.pgpass` does not exist — both checked on 2026-09-22, the token's length read as zero rather than its value. An earlier draft of this clause went on to describe behaviour that does not exist, and the second lens found it: there is no `input_prices.json` anywhere in this repository, no file in `src/` contains the word `unconfigured`, and nothing is "written as the literal `unavailable`" — that string belongs to `src/probe_price_sources.py:248` and `:339`, describing rows of the probe's own report. What is true is narrower: **no code in this repository reads a price at all.** `src/prices/` is an unmerged row in This cycle; the only price code on `main` is `src/probe_price_sources.py`, a read-only probe that sends no credentials by design and is not a backend. The market table the comparers read is `input_market.json`, written by `src/market.py` from daily `.csv` files a person places in a directory, and no run produces one. The `priced_in` rule is not in `src/` either — it is an instruction in `.claude/agents/numbers-vs-market.md` and `.claude/agents/notes-vs-market.md`, and it is off because no market table reaches a comparer. That is blocked on a token, not on a judgment. The interface and the three backends are **a row in This cycle** in `docs/next_cycle_tasks.md`, judged against response fixtures hand-written from each provider's published format; until that row's pull request merges, nothing in this repository reads a price at all, and this paragraph is a decision rather than a running default.

[x] **the delisting return when the source carries none** — *decided 2026-09-21, in force from the first pattern-study row* · **`dlret` when CRSP has it. Where it is missing: −30%, and −55% on Nasdaq.** The first is Shumway (1997), the second Shumway and Warther (1999), and they are the literature's own defaults rather than this project's guess. The correction is recorded **per row**, as the value used and the reason it was used, so the study reports the cross-section both with and without it and a reader can see how much of any result is the correction. A missing delisting return left at zero is the survivorship bias the whole universe design exists to avoid, and it is silent: the request succeeds and the row is simply flat. **The judge is the price-interface row in This cycle** — the function that applies the default and records the reason lands with it. Until that merges these are two numbers out of the literature with no code behind them, which is what a decision looks like before it is built.

## Open

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
