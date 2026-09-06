# How we work — who does what

## 1. Principles

1. **Plain names.** No letter-number codes. A code in a report, ledger, issue
   title, filename or commit message is a bug. Machine keys are readable slugs
   like `receivables_outrun_revenue`.
2. **The owner's signature is never a bottleneck.** No sign-off queue, no
   pending-decisions file, no "owner decision required" state. Work with no
   judge — no test, no schema, no check — is not defined as a task. It is left in
   the work ledger as "needs judgment", and the owner reads those in one sitting
   at the next rules version.
3. **Everything has a default.** If the owner has not decided, proceed with the
   default. The only stop is one the owner placed personally.
4. **Text goes through verbatim.** A model may select paragraphs; it never
   rewrites or summarizes text for the predictor. Commit exactly the text the
   predictor saw. Every quote is string-matched against the committed input.
5. **Python does the arithmetic.** Ratios, trends, diffs, baselines — all
   deterministic code. The model judges text only.
6. **Append-only under `runs/`, `rules/` and `events/`:** existing content is
   never changed or deleted; appending to the end of a ledger file is allowed.
   A correction is a new file plus one ledger line.
7. **The seal is nothing more than** auto-commit, pull request, auto-merge on
   green CI, and one timestamp command. No manifest, no signature gate, no seal
   window, no launch approval.
8. **Rules are versioned.** Each prediction is scored against its own rules
   version. Improvements apply from the next version; nothing is retroactive.
9. **Infrastructure and harness changes are capped at one day.** Past that, build
   the parsers in an interactive session without the harness. No new
   methodology, no new governance layer, no new document system. The old repo is
   archived, not rewritten — this is a thin layer on top.
10. **Never soften an adverse result.** If no event happened, say so. If the
    model underperformed the baseline, say so.
11. **Mistakes compound.** When a session ends, its mistakes go into
    `lessons.md`, one line each. A weekly routine folds rules into `CLAUDE.md`
    and procedures into skills.

## 2. Vocabulary

**Two questions**, never merged: **accounting reliability** — do these numbers
reflect reality? **financial pressure** — is this company under pressure?

**Pipeline stages**: detect filing → extract → predict → publish → record events
→ score.

**Work states**: assigned → done → confirmed / blocked / rejected / deferred /
caught by audit / needs judgment.

**Finding weight**: severe / moderate / minor.
**Finding kind**: threatens the prediction record / quality / cosmetic / needs
judgment.

**Stop conditions**: nothing left to find / cost exceeded / prediction record
damaged / the owner placed it.

---

## 3. The pipeline

Prediction is a routine, not a loop. There is no iterative improvement pass over
a prediction.

| Stage | Does | Passes when |
|---|---|---|
| detect filing | daily: new filings for the twelve, from the EDGAR submissions index | 12 of 12 lookups succeed |
| extract | the input spec, plus the diff, the trend table and the histories | schema passes, paragraph counts in the normal range, zero cutoff violations, at least one `TextBlock` found |
| predict | one model call per question; on failure, retry once with identical input, then record a failure | output schema valid, every quote exists in the input, served model equals the pin |
| publish | commit → pull request → auto-merge on green CI → `ots stamp input_manifest.json` | the merge succeeded and the `.ots` file exists |
| record events | 8-K 4.01 / 4.02 / 1.01 / 5.02, late filings, amendments, comment letters, material-weakness language, explanation materialization → `events/ledger.jsonl` | the append succeeded |
| score | on horizon expiry or event occurrence, recompute the metrics and regenerate the results document | deterministic match |

**Publish merges itself.** `main` requires the CI check and nothing else — no
reviewer, no approval. Every pull request from the pipeline or a routine sets
`gh pr merge --auto --squash` the moment it is opened, so it lands as soon as CI
goes green and nobody clicks anything. A pull request sitting open waiting for
the owner is the bottleneck the rules forbid, not a safety measure.

Scheduled-task sessions start from a clone, sparse-checked-out to that company's
`runs/` only. A model fallback is possible, so the served model is recorded; if
it differs from the pin the run is recorded as a failure. There is no metered
billing path — subscription authentication only.

---

## 4. Routines

These start from the errors actually hit in the ten months of the archived
project: the "documents used" list was really "documents provided"; the cache
checked fingerprints but not output validity; rows without accession numbers
passed the loader; perturbation was applied to one arm only; experiment labels
leaked into inputs; a cycle closed with empty result files; cross-references
dangled; verdicts were wrong on shallow clones; figure labels drifted; README
numbers disagreed with recomputation. Every one was found by a human later, and
every one could have been checked by a machine daily.

### Daily

- **cutoff re-check** — every date and accession in published inputs
- **quote re-check** — every prediction quote against the input text
- **missing-filing check** — the EDGAR list against `runs/`
- **prediction-tamper check** — any change to existing content, or deletion, of
  a `runs/`, `rules/` or `events/` file that exists on `origin/main` fails CI and
  blocks the merge; appending to the end of a ledger file passes, and so does a
  `README.md` at the root of one of those directories, which is documentation
  and not a record
- **rules-precedence check** — the rules-version commit is an ancestor of the
  prediction commit
- **event-gap check** — EDGAR events against the ledger

### Weekly

- **extraction drift** — re-extract the latest filing for each of the twelve;
  paragraph, note or number counts outside ±20% raise a harness task
- **schema and hash**
- **unreferenced code**
- **dependencies** — update, hash-lock, test, pull request
- **document numbers recomputed**
- **broken links and paragraph ids**
- **fold lessons** — `lessons.md` into `CLAUDE.md` for rules and into skills for
  procedures; merge duplicates; strengthen anything seen three or more times;
  open a pull request

### On red CI

A fix pull request, at most three attempts. Never touch `runs/`, `rules/` or
`events/`. Never change a test expectation. After three failures, open an issue
marked "needs judgment" — not a signature request.

### Monthly

- **doc-bloat ratio** — markdown words over Python lines. The archived repo sat
  at 11.1. If the ratio rises and no external claim got stronger, open an issue.
- **monthly scorecard** — the evaluation metric tables, with no judgment added.

### Hooks

- **session start** — read `lessons.md`.
- **session end** — write this session's CI failures, test failures, quote
  verification failures and owner corrections to `lessons.md`, one line each, no
  judgment.

Routines do not run the pipeline, do not build parsers, and do not judge.

---

## 5. The harness

Kept: the reviewer and builder pair, the work ledger, reproduce verification and
refute verification, the write restriction with its self-test and session-start
hook, the cycle audit, the planted-defect test, the stop conditions, the
claim-strength review, the doc-bloat penalty, no push, and no metered billing.

Removed: the seal machinery — the sealed manifest, the seal check, the seal stop
condition, the November seal success criterion, the per-finding causal path to
the seal, the launch-gate language. In its place, `src/append_check.py`: fail if
the diff changes or deletes existing content in any `runs/`, `rules/` or
`events/` file that exists on `origin/main`, while letting an append to the end
of a ledger file through. It runs inside the test command, and a violation stops the
cycle immediately as "prediction record damaged". The success criterion is now
the one line at the bottom of `CLAUDE.md`, and each finding carries one line
tying it to one of its three conditions.

Also removed: the signature machinery — owner-signature gates, pending-decisions
drafts, owner-queue aging backpressure, and "any restart is the owner's decision
only". In its place: a finding with no judge is left in the work ledger as
"needs judgment" and never assigned; there is no pending file; writing "owner
decision required" is itself an audit violation; and a stop from "nothing left to
find" or "cost exceeded" restarts on its own when a new task file appears.

Renamed, reporting layer first: structure-change record, severe / moderate /
minor, threatens the prediction record / quality / cosmetic / needs judgment,
cycle N item i, assigned / done / confirmed, blocked / rejected / deferred /
caught by audit, work ledger / cycle audit / planted-defect test, reproduce
verification / refute verification, full review / claim-strength review, nothing
left to find / cost exceeded / prediction record damaged, write restriction /
restriction self-test / changes test expectations.

The harness builds parsers, where a fixture pass is the judge; repairs extraction
drift; and produces the flag distribution over the 30 past cases. It does not
propose thresholds. Otherwise it does not wake.

---

## 6. Which model does what

| Role | Model | Why |
|---|---|---|
| harness builder, reviewer, full review, reproduce verification | Opus, effort xhigh | the existing pins |
| harness refute verification, claim-strength review | Fable, effort max | heavy judgment, where a mistake is expensive |
| **pipeline predictor** | **Fable, pinned for one year together with rules v0.1** | keeping the pin matters more than raw capability — a track record only means something as quarter-to-quarter comparison under the same model and the same rules. Check subscription-path stability from the served-model record on the first run; if fallbacks are frequent, drop the pin to Opus. |
| when a model change is needed | run both models in parallel for one quarter, then switch | a switch without a bridge quarter contaminates the record |
| paragraph classifier | Haiku class | labels only |
| routines | Haiku to Sonnet class | reads script output and opens pull requests |

Pins are recorded in `input_manifest.json` and in the harness config.

---

## 7. The sequence

1. **Dispose of the old.** Done when `archive/` exists, the supersession commit
   exists, and the tags exist.
2. **Repo skeleton, `CLAUDE.md`, `lessons.md`, the three `docs/` files.** Done
   when the tree exists and CI is green.
3. **Harness minimization and the reporting-layer renames.** Done when the
   restriction self-test passes, `append_check.py` works, and the status output
   contains no codes. One-day cap.
4. **Parser build.** The `TextBlock` extractor, the MD&A section splitter, the
   auditor's report and Item 9A splitter, the 8-K 2.02 parser, the 8-K event
   bodies, the paragraph diff, the note change history, the trend table, and the
   extraction pass checks. Thirty-six fixture expected-value files — twelve
   companies by 10-K, 10-Q and 8-K 2.02 — drafted by the harness; if the owner
   does not look at them, they stand. Done when 36 of 36 pass. Two weeks.
5. **Detect-filing and extract scheduled tasks, plus CI.** Done when the first
   automatic extraction lands in `runs/` as a pull request.
6. **The 30 past cases, then rules v0.1 in force.** The harness runs the input
   spec and the input indicators over the archived cases at their cutoff dates
   and produces the flag distribution table. The owner adjusts the thresholds or
   does not. Commit `rules/*_v0.1`. Done when the rules files exist.
7. **Enable predict and publish.** Done when the next filing produces the first
   prediction pull request, auto-merged, with its timestamp file.
8. **Register the routines.** Daily, then weekly, then monthly, plus the
   session-start and session-end hooks. Done when each scheduled task has one run
   log.

Each step starts when the previous step's condition is met. Never wait for owner
confirmation.

---

## 8. Do not

- Rewrite or refactor the archived repo. It is an archive.
- Create new identifier families, new ledgers, new approval procedures, new
  document systems.
- Hand summaries to the predictor.
- Change or delete existing content under `runs/`, `rules/` or `events/`.
  Appending to the end of a ledger file is fine.
- Change a cycle's rules or thresholds after seeing its results.
- Stop and wait for the owner. Take the default and leave one line.
- Spend more than one day on harness or infrastructure changes.
- Write "AI detects accounting fraud". Write "reads filings, predicts two
  questions, and leaves a verifiable record".
- Hide that accounting-reliability events were zero in year one.
