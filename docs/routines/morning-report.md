# Daily — the morning report

The owner's decision of 2026-09-24 (`docs/structure_changes.md`): results
arrive as one morning report, and a model only reads and triages them. The night
itself is `.github/workflows/nightly.yml`, Python with no model. This routine
reads what it left on its pull request and writes the report.

A Claude Code cloud scheduled task, daily at 07:30 US Eastern. Its final message
is the report, and the final message is the notification: there is no
`osascript` in the cloud. It builds nothing, fixes no parser and judges nothing
(`docs/HOW_WE_WORK.md` §4, "routines do not build"). It never touches EDGAR: the
cloud environment may not reach sec.gov, and every EDGAR request happens in
Actions.

---

## 0. Set up

A cloud session has no `.venv`. Without one the Stop hook's `make check` does
not run and says nothing, which has happened in this repository once already.

```sh
python3.12 -m venv .venv && .venv/bin/pip install -q -r requirements.txt
```

## 1. Did last night run?

List the runs of `nightly.yml` (GitHub `actions_list`, `list_workflow_runs`,
resource `nightly.yml`). Last night's run is a run started after 06:00 UTC
**today** -- the schedule fires at 07:00 UTC, and this routine runs hours after
it. A run from yesterday is not last night's, however recent it is.

- **No such run: that is the first line of the report**, before anything else,
  in these words: `LAST NIGHT DID NOT RUN.` Then the newest run there is, with
  its date. A night that did not run and went unnoticed is the worst failure
  this system can have.
- A run whose conclusion is not `success` is a failure line too, with its
  conclusion and the name of the step that failed.

## 2. Read what the night left

The night commits its run directories and its ledger line on one branch,
`nightly-<date>` (`nightly-<date>-2` for a second run on a date whose branch
is still on the remote), and opens a pull request from it into `main` with
auto-merge on (`src/nightly.py --publish`: `gh pr create`, then `gh pr merge
--auto --merge`). Nothing is pushed to `main` from the night; `main` takes the
line when CI is green. Find last night's pull request by its title, `the
nightly crew's night of <date>` (GitHub `list_pull_requests`, open and merged),
and read the last line of `history/nightly.jsonl` on its branch -- or on `main`,
once it has merged. That line is the night's summary -- `lookups`, `new`,
`not_extracted`, `extractions` (each passed one with its `prices`: the folder
and `price_fetch.json`, or the reason there is none, `no price series:
TIINGO_TOKEN unset` when the secret is not set), `failures`, and `history` --
**only if its `run` is last night's run URL.** A line whose `run` is another
run's is the failure line `the night left no summary line`, and nothing on
that branch is reported as last night's.

If the run happened and there is no pull request of that title, the night's
log says which step stopped the publish (`nightly: the night was not
published: ...`); that is a failure line. A night with nothing to commit opens
no pull request and its log says `nothing to publish`; that is not one.

## 3. See that its pull request will merge

A pull request opened with the Actions token starts no CI, so its auto-merge
never fires; the workflow opens it with the `NIGHTLY_GH_TOKEN` secret when
the repository holds one, and with the Actions token otherwise. If last
night's pull request is open with no CI run on its head, close it and reopen
it with the GitHub tools: `reopened` starts CI. Then turn auto-merge on again
(`enable_pr_auto_merge`, merge method `MERGE`), because closing a pull request
can turn it off; auto-merge lands it once CI is green. If it is open and CI is
red, that is a failure line, with the step that failed. Two nights' lines
appended to `history/nightly.jsonl` on two branches cut from the same `main`
conflict: once one of the two pull requests merges, the other cannot. That
happens only when a night's pull request is still open when the next night
runs; it is a failure line naming both pull requests, and this routine does
not resolve it.

## 4. The report

Readable on a phone in one minute. Plain text, short lines, in this order:

1. **Failures and anomalies.** `LAST NIGHT DID NOT RUN` if it did not. Then
   every entry of the summary's `failures`, one line each, then the run's own
   failure if its conclusion was not `success`, then a red CI or a conflict on
   any open `nightly-<date>` pull request, then every run whose `prices`
   carries a reason instead of a folder. If there are none, say `no failures`.
2. **New filings and what extract did with each**: `lookups 12 of 12`, then one
   line per new filing -- ticker, form, accession, and passed or the stage it
   failed at. `no new filings` if there were none.
3. **Historical collection**: `collected N of M in scope, P passed the four
   checks`, tonight's count, and tonight's failures counted by the stage they
   failed at (the lines are in `history/<ticker>/manifest.jsonl`).
4. **The owner's queue**: the number of `[ ]` rows in `docs/needs_judgment.md`,
   and the open pull requests by number and title (GitHub
   `list_pull_requests`). `tools/daily_summary.sh` prints the rest of what the
   daily summary carries; run it with `sh`, and take the pull requests from the
   GitHub tools rather than from its `gh` line, which prints `(none open)` when
   `gh` is missing.

The report says nothing about signal. The twelve test the pipeline, not the
signal, and no observation about any of them is recorded.

## 5. A new kind of failure

A failure whose kind has not appeared in `history/nightly.jsonl` before gets a
row in `docs/next_cycle_tasks.md` under **Next cycle**, in the file's own
four-field shape, with a judge and an expected value from the source -- the
filing, the index row, the summary line that recorded it. If no judge can be
written, the row goes in `docs/needs_judgment.md` instead. Either way it goes
through its own pull request with auto-merge on. This routine does not fix the
failure.
