# Weekly — re-lens what only one lens read

A pull request that merged behind a same-family fallback, or behind no second
lens at all, is not confirmed. It is recorded as what it is and it is re-read
here, once the Codex quota returns. This routine is the only thing that closes
that gap; nothing else in the loop goes back to a merged commit.

Weekly, as a scheduled task. It builds, judges and decides nothing — it runs one
lens and writes down what came back.

---

## 1. Find the rows

Two sources, and a row in either one qualifies:

```sh
# every lens run that answered on the fallback
grep '"lens": "claude-fable-fallback"' events/ledger.jsonl

# every lens run where neither lens answered
grep '"lens": "none"' events/ledger.jsonl

# every lens run whose judge came from the tree it judged, because the ref it
# pins out of did not carry the lens yet — the change that builds the lens
grep '"judge_from": "tree"' events/ledger.jsonl

# every pull request that opened with the label because no lens read it
gh pr list --state all --label one-lens --json number,title,mergeCommit,state
```

A `one-lens` pull request that is still open is not this routine's to merge. Run
the lens on it, append the verdict, and leave the merge to the build skill's own
step 6 — a routine that merges is a routine that builds.

## 2. Re-run the lens on the merged commit

Not on `main`, and not on the branch: on the commit the work merged at, so the
verdict names the change that actually landed.

```sh
git worktree add --detach .claude/worktrees/relens-<number> <merge commit>
ln -s ../../../.venv .claude/worktrees/relens-<number>/.venv
LENS_JUDGE_BASE=<merge commit>^1 \
    tools/second_lens.sh .claude/worktrees/relens-<number> "<item title>"
```

`LENS_JUDGE_BASE` is the ref the script pins its judge out of, and it must be
**the merge commit's first parent**, not the default `main`. The script also
refuses to answer when the tree it is reading changes what a lens takes as its
own definition — `CLAUDE.md`, `AGENTS.md`, `.claude/agents/refute-check.md`, the
settings files — and that comparison is against the pinned ref. Left at `main`,
every old merge commit would differ from a `main` that has moved since (the
weekly fold edits `CLAUDE.md` by design), so every row would come back
*no lens ran* forever and the *pass* row below would be unreachable. The first
parent is what `main` held the moment that work landed, which is the comparison
the question actually asks.

The script appends its own ledger line, so the record of the re-run is written
by the same code that wrote the record of the first run. Remove the worktree
afterwards.

## 3. What each verdict does

| Verdict | Exit | What happens |
|---|---|---|
| pass | 0 | the row in `docs/next_cycle_tasks.md` moves from *done, not confirmed* to **done**, naming the lens and the date |
| fail | 1 | open an issue marked **needs judgment** naming the merged pull request, the rule number and the file and line. Do not fix it here |
| needs judgment | 2 | the same issue, marked the same way, carrying what a judge would have to decide |
| no lens ran | 3 | nothing changes. The row stays unconfirmed and comes back next week |

A row that comes back *no lens ran* three weeks running is not waiting for a
quota any more. Open an issue marked **needs judgment** naming the reason the
script printed — the pinned ref could not be resolved, the tree changes what a
lens reads as its own definition, an answer file could not be cleared — because
a row that can never be confirmed has to become somebody's question rather than
a permanent line in a weekly report.


A fail here is not a revert and not a hotfix. It is an issue with a number on
it, because the change is merged and a routine that edits merged work at three
in the morning is worse than the hole it found.

## 4. Leave the record

One line in `docs/structure_changes.md` per week the routine changed a row's
state, naming how many rows were re-read, how many moved to done, and how many
opened an issue. A week where nothing moved gets no line.

---

**Why the merged commit and not `main`.** A row marked *done, not confirmed*
carries the commit it merged at for exactly this reason: `main` has moved, and a
lens reading `main` would answer about a tree the item never produced. Six of
wave E's rows were re-read this way on 2026-09-13 and every one of them was read
at its own merge commit.

**Why it is weekly and not on quota-restore.** Nothing watches the quota, and a
routine that fires on a signal nobody emits never fires. Weekly is slower and it
runs.
