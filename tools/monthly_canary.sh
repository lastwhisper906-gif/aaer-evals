#!/usr/bin/env bash
#
# The monthly seeded-defect canary: plant one known defect on a branch, ask the
# refute lens about it, and write down whether it was caught.
#
#     tools/monthly_canary.sh [base]
#
# A verification layer that has never been shown to catch a defect is not known
# to work. Every other routine in docs/HOW_WE_WORK.md checks the pipeline; this
# one checks the thing that checks the pipeline, and it is the one piece of the
# old harness kept.
#
# What it does, in order: put a worktree on `base`, take the seed, the routine's
# own document and test and the ledger back out of that worktree so the answer
# key is not sitting beside the question, copy the seed in tools/seeded_defect into it,
# commit it as an ordinary-looking change, and start `refute-check` inside that
# tree with tools/lens_prompt.md -- the same prompt and the same answer schema
# both lenses in tools/second_lens.sh read, so the canary measures the lens the
# project actually uses rather than a second one written for the occasion.
#
# Exit codes
#
#     0  hit   -- the lens named a planted file under the planted rule
#     1  miss  -- the lens answered and did not name it
#     3  no lens ran
#     4  the defect could not be planted, so there was nothing to ask about
#
# Only a hit is an approval, and the routine does not decide what to do about
# the other three: it appends one line to the ledger and exits. Every outcome
# leaves a row, exit 4 included, because a month with no row is indistinguishable
# from a month nobody scheduled. The two exceptions are the two failures that
# happen before plant.json can be read -- CANARY_DIR could not be made, or the
# manifest does not describe a plant -- where there is no defect and no rule to
# put in a row. Monthly, as a scheduled task; docs/routines/monthly-canary.md is
# the routine.
#
# The run is the same code whether it is the monthly one or a trial. A dry run
# is this script with CANARY_LEDGER pointed at a file outside every tree, so
# what is exercised is the routine and not a second path written to be safe.
#
# The worktree is removed on a hit and kept on anything else, because a miss is
# the one outcome where the tree the lens read is the evidence.
#
# Nothing of this script's own lands in the tree under review. Its prompt, the
# lens's answer and its log go to CANARY_DIR, outside the worktree: a script
# that drops its machine output into the tree it reviews has already cost this
# repository a red gate once. The one exception is the lens's input,
# `.lens/change.diff`, ignored, written exactly where tools/second_lens.sh
# writes it in every tree it lenses.
#
# Environment, all with defaults, all overridden by the test:
#
#     CANARY_REPO  CANARY_SEED  CANARY_LEDGER  CANARY_PYTHON  CANARY_PROMPT
#     CANARY_DIR   CANARY_WORKTREE  CANARY_TIMEOUT  CANARY_MODEL  CANARY_KEEP

set -u

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

CANARY_REPO="${CANARY_REPO:-$REPO_ROOT}"
CANARY_SEED="${CANARY_SEED:-$REPO_ROOT/tools/seeded_defect}"
CANARY_LEDGER="${CANARY_LEDGER:-$CANARY_REPO/events/ledger.jsonl}"
CANARY_PYTHON="${CANARY_PYTHON:-$REPO_ROOT/.venv/bin/python}"
CANARY_PROMPT="${CANARY_PROMPT:-$REPO_ROOT/tools/lens_prompt.md}"
CANARY_TIMEOUT="${CANARY_TIMEOUT:-1800}"
CANARY_MODEL="${CANARY_MODEL:-fable}"
CANARY_KEEP="${CANARY_KEEP:-}"

# `-m src.canary` has to resolve to this repository's module whatever directory
# the scheduled task was started from.
PYTHONPATH="$REPO_ROOT${PYTHONPATH:+:$PYTHONPATH}"
export PYTHONPATH

LENS="refute-check"
# The two statuses this script decides by itself; the rest come from src/canary.py.
NO_LENS_RAN=3
COULD_NOT_PLANT=4

BASE="${1:-${CANARY_BASE:-main}}"
STAMP="$(date -u '+%Y-%m-%d-%H%M%S')"
# The routine's own scratch -- the prompt, the list of planted paths, the lens's
# answer, the log -- goes under the checkout's ignored `logs/`, not beside the
# tree. Both used to default to `$TMPDIR` with the same stamp, so `ls ..` from
# inside the planted tree showed `seeded-defect-<stamp>/planted.txt`: the three
# landing paths, one directory up, with no git and no guessing. The second lens
# found it. The checkout is reachable from the tree by a deliberate question
# (`git worktree list`), and by the `.venv` link below, which `ls -la` prints:
# the class docs/routines/monthly-canary.md §6 already names, and the reason
# its logs are one of the places §6 lists.
CANARY_DIR="${CANARY_DIR:-$CANARY_REPO/logs/monthly-canary-$STAMP}"

mkdir -p "$CANARY_DIR" || exit "$COULD_NOT_PLANT"
LOG="$CANARY_DIR/canary.log"

# The interpreter before anything is asked of it: every row is written through
# it, and a fresh clone has no .venv. Without this the first call to it failed
# inside the manifest read and the month ended saying plant.json did not
# describe the plant -- the wrong cause, and no row.
if [ ! -x "$CANARY_PYTHON" ]; then
    echo "monthly_canary: there is no interpreter at $CANARY_PYTHON, so no row can be written; make the repository's .venv or set CANARY_PYTHON" | tee -a "$LOG" >&2
    exit "$COULD_NOT_PLANT"
fi

# One place the run says what went wrong, and the ledger line is written before
# the script can exit on any path that had a lens to report on.
note() {
    echo "$*" >> "$LOG"
    echo "$*" >&2
}

# A month that could not plant still leaves a row. docs/routines/monthly-canary.md
# calls the ledger the whole history of whether this layer has ever been shown
# to work, and a month with no row in it is indistinguishable from a month the
# task was never scheduled -- which is the one reading that must not be the
# quiet default, because it is the reading under which nobody comes back.
#
# It takes a reason rather than a verdict: nothing was asked, so there is no
# lens and no model to name. The rows before the manifest is readable are the
# exception, and they are the two the routine cannot write: with no plant.json
# there is no defect and no rule to put in the row.
could_not_plant() {
    note "monthly_canary: $1"
    "$CANARY_PYTHON" -m src.canary ledger \
        --ledger "$CANARY_LEDGER" \
        --seed "$CANARY_SEED" \
        --result "not_planted" \
        --lens "none" \
        --model "none" \
        --findings 0 \
        --planted-on "${PLANTED_ON:-unrecorded}" \
        --reason "$1" >>"$LOG" 2>&1 \
        || note "monthly_canary: and the row saying so could not be written either"
    echo "monthly canary: none · none · not_planted · $1"
    exit "$COULD_NOT_PLANT"
}

# --- what the plant says about itself --------------------------------------
#
# The cover story, the branch it goes on and the rule it breaks all come out of
# the manifest rather than being written a second time here: the plant is
# replaced when it stops being interesting, and a copy of its description in the
# routine would be the half that did not move.
#
# The branch and the directory are named after the change, not after this
# routine. A worktree called `canary` in a prompt that names its own path is the
# answer handed to the lens in the question.
DESCRIBED="$("$CANARY_PYTHON" -c 'import json,sys
plant = json.load(open(sys.argv[1]))
for key in ("commit_subject", "item", "rule", "branch", "worktree"):
    print(plant[key])' "$CANARY_SEED/plant.json" 2>>"$LOG")"
{
    IFS= read -r SUBJECT
    IFS= read -r ITEM
    IFS= read -r RULE
    IFS= read -r BRANCH_NAME
    IFS= read -r TREE_NAME
} <<< "$DESCRIBED"

if [ -z "${SUBJECT:-}" ] || [ -z "${ITEM:-}" ] || [ -z "${RULE:-}" ] \
        || [ -z "${BRANCH_NAME:-}" ] || [ -z "${TREE_NAME:-}" ]; then
    note "monthly_canary: $CANARY_SEED/plant.json does not describe the plant"
    exit "$COULD_NOT_PLANT"
fi

BRANCH="$BRANCH_NAME-$STAMP"
# Outside the checkout, not under `.claude/worktrees/` beside it. A planted
# tree three directories under a checkout whose `main` carries the seed on disk
# is a tree where `ls ../../../tools/seeded_defect` hands the lens the manifest
# and the .planted files, with no command more suspicious than `ls` -- and the
# siblings of that directory are the other worktrees of this repository, one of
# which is where the plant is being written. Found by the first lens, which
# planted into a throwaway clone and ran the `ls`.
#
# What stays reachable is the checkout itself: `git worktree add` writes a
# `.git` file naming it, and `git worktree list` prints it. That is the same
# class of reach as `git show HEAD:<path>` -- a deliberate question -- and it is
# written down in docs/routines/monthly-canary.md §6 rather than claimed away.
TREE="${CANARY_WORKTREE:-${TMPDIR:-/tmp}/$TREE_NAME-$STAMP}"

# --- plant -----------------------------------------------------------------

# The base as a commit, resolved once in the repository it was named for. A name
# read later inside the planted tree can mean something else there: `HEAD` --
# what a detached checkout such as `actions/checkout` on a pull request reports
# as its branch -- is the plant's own commit once the plant commits, so the diff
# below came back empty and the routine said `not_planted` on CI only.
BASE_COMMIT="$(git -C "$CANARY_REPO" rev-parse --verify --quiet "$BASE^{commit}" 2>>"$LOG")"
if [ -z "$BASE_COMMIT" ]; then
    could_not_plant "$BASE does not name a commit in $CANARY_REPO"
fi

if ! git -C "$CANARY_REPO" worktree add -b "$BRANCH" "$TREE" "$BASE_COMMIT" >>"$LOG" 2>&1; then
    could_not_plant "could not put a worktree on $BASE at $TREE"
fi

# The lens is started with Claude Code's own hooks, the same as every other lens
# run here, and the Stop hook runs the gate under .venv/bin/python. A worktree
# with no .venv makes that hook fail on every turn.
if [ -d "$CANARY_REPO/.venv" ] && [ ! -e "$TREE/.venv" ]; then
    ln -s "$CANARY_REPO/.venv" "$TREE/.venv" >>"$LOG" 2>&1
fi

# --- take the answer key out of the tree before anything is planted --------
#
# The seed ships on `main` and the plant grows on a worktree off `main`, so
# without this the tree under review holds the answer beside the question:
# plant.json names the rule and the landing paths, the .planted files are
# byte-identical to what lands, and the routine's document and test say in words
# what is wrong with it. `grep -rl` on the planted file's own name -- the first
# thing a lens does -- returns all of them. A lens that never applies the rule
# would still score a hit, and the month would be recorded as the layer having
# been shown to work when nothing of the sort was shown.
#
# `update-index --skip-worktree` and then `rm`, rather than a plain `rm` or a
# sparse checkout. The paths stay in the commit, so `git status` is clean and
# `git diff` against the base is the three planted files and nothing else: a
# tree missing files it has committed is a tree whose deletions are themselves
# a marker.
#
# Not sparse-checkout, which was the first thing written here and announces
# itself twice over. Plain `git status` in a sparse worktree prints "You are in
# a sparse checkout with N% of tracked files present", and `git sparse-checkout
# list` then hands over the four paths -- which is the answer key's table of
# contents, read off by a lens doing nothing more suspicious than `git status`.
# Skip-worktree is the same effect with no notice: `git sparse-checkout list`
# answers "this worktree is not sparse".
#
# What this does not reach: `git ls-tree -r HEAD` and `git show HEAD:<path>`
# still hold the seed, and docs/HOW_WE_WORK.md in the tree still says this
# routine exists -- the repository documents its own routines and that is not
# something a plant can hide. What it removes is everything a lens reaches by
# reading and grepping the working tree, which is how both lenses in
# tools/second_lens.sh actually read a change.
KEPT_OUT="$("$CANARY_PYTHON" -m src.canary keep-out --seed "$CANARY_SEED" 2>>"$LOG")"
if [ -z "$KEPT_OUT" ]; then
    # No row: `ledger` reads the same manifest and would fail the same way, so
    # there is no defect and no rule to write one with.
    note "monthly_canary: $CANARY_SEED/plant.json names nothing to keep out of the tree"
    exit "$COULD_NOT_PLANT"
fi

# One index entry at a time, because `--skip-worktree` takes paths and not
# patterns, and a keep-out entry naming a directory covers every file under it.
# A path the base does not carry is not an error -- nothing there can leak --
# but a run that marked nothing at all did not work, whatever git said.
MARKED=0
while IFS= read -r out; do
    [ -n "$out" ] || continue
    while IFS= read -r entry; do
        [ -n "$entry" ] || continue
        if ! git -C "$TREE" update-index --skip-worktree -- "$entry" >>"$LOG" 2>&1; then
            could_not_plant "$entry could not be kept out of $TREE"
        fi
        # Emptied, not deleted. A tracked file that is gone from a worktree is
        # a fact something reads out loud: `.claude/settings.json` runs
        # `cat lessons.md` at SessionStart, so deleting it put
        # "cat: lessons.md: No such file or directory" in the lens's first turn
        # -- a missing tracked path, named to the reader, by the step whose
        # whole purpose is to say nothing. An empty file says nothing and reads
        # as nothing. Skip-worktree is what keeps `git status` clean either way.
        : > "$TREE/$entry" 2>>"$LOG" || could_not_plant "$entry could not be emptied in $TREE"
        MARKED=$((MARKED + 1))
    done <<< "$(git -C "$TREE" ls-files -- "$out" 2>>"$LOG")"
done <<< "$KEPT_OUT"

if [ "$MARKED" -eq 0 ]; then
    could_not_plant "nothing was kept out of $TREE, so the base holds the answer key"
fi

# Checked rather than trusted. A keep-out step that silently did nothing -- an
# older git, a flag that moved, a path that stopped resolving -- leaves the key
# in the tree, and the run that follows would look like a hit and mean nothing.
# This is the one place the routine refuses to ask.
while IFS= read -r out; do
    [ -n "$out" ] || continue
    while IFS= read -r entry; do
        [ -n "$entry" ] || continue
        if [ -s "$TREE/$entry" ]; then
            could_not_plant "$entry still has its contents in $TREE, which would hand the lens the answer"
        fi
    done <<< "$(git -C "$TREE" ls-files -- "$out" 2>>"$LOG")"
done <<< "$KEPT_OUT"

PLANTED="$CANARY_DIR/planted.txt"
if ! "$CANARY_PYTHON" -m src.canary plant \
        --seed "$CANARY_SEED" --into "$TREE" > "$PLANTED" 2>>"$LOG"; then
    could_not_plant "the seed in $CANARY_SEED did not plant"
fi

# Exactly the files the manifest named, never `git add --all`: the worktree also
# holds a .venv symlink and whatever the repository leaves untracked, and a
# commit carrying those is not the change the lens was meant to read.
PLANT_FAILED=""
while IFS= read -r landed; do
    [ -n "$landed" ] || continue
    git -C "$TREE" add -- "$landed" >>"$LOG" 2>&1 || PLANT_FAILED="$landed"
done < "$PLANTED"

if [ -n "$PLANT_FAILED" ]; then
    could_not_plant "$PLANT_FAILED could not be added to the branch"
fi

# The commit message is the one a builder would have written for this change. It
# does not say the change is planted: a defect that announces itself measures
# the announcement.
#
# The identity is passed rather than assumed. A developer's machine has one in
# `~/.gitconfig` and `ubuntu-latest` does not, so this line committed here and
# refused in CI -- `not_planted`, exit 4, on a routine whose whole purpose is to
# find out whether the lens still catches a defect. And it is the base commit's
# own author and committer, not a name of the routine's: `git log -1` on the
# change under review printed the routine's name to the lens, which is the
# announcement the commit message above is written not to make.
IDENTITY="$(git -C "$CANARY_REPO" log -1 --format='%an%n%ae%n%cn%n%ce' "$BASE_COMMIT" 2>>"$LOG")"
{
    IFS= read -r AUTHOR_NAME
    IFS= read -r AUTHOR_EMAIL
    IFS= read -r COMMITTER_NAME
    IFS= read -r COMMITTER_EMAIL
} <<< "$IDENTITY"
if ! GIT_AUTHOR_NAME="$AUTHOR_NAME" GIT_AUTHOR_EMAIL="$AUTHOR_EMAIL" \
        GIT_COMMITTER_NAME="$COMMITTER_NAME" GIT_COMMITTER_EMAIL="$COMMITTER_EMAIL" \
        git -C "$TREE" commit -q -m "$SUBJECT" >>"$LOG" 2>&1; then
    could_not_plant "the plant did not commit on $BRANCH"
fi

# A plant the lens cannot see in the diff is not a plant. Checked against the
# base the branch came from, which is what the lens reads the change against.
SEEN="$(git -C "$TREE" diff --name-only "$BASE_COMMIT" 2>>"$LOG")"
while IFS= read -r landed; do
    [ -n "$landed" ] || continue
    case "
$SEEN
" in
        *"
$landed
"*) ;;
        *) PLANT_FAILED="$landed" ;;
    esac
done < "$PLANTED"

if [ -n "$PLANT_FAILED" ]; then
    could_not_plant "$PLANT_FAILED is not in the diff against $BASE"
fi

# The base rather than the plant. On a hit the branch is deleted and its commit
# is reachable from nothing, so a row naming it names an object that will be
# pruned -- which is the reading this repository already refuses elsewhere. The
# base is a commit of `main` and resolves for as long as the history does.
PLANTED_ON="$(git -C "$TREE" rev-parse --short "$BASE_COMMIT" 2>>"$LOG")"
[ -n "$PLANTED_ON" ] || PLANTED_ON="unrecorded"

# --- ask the lens ----------------------------------------------------------

# The same preamble tools/second_lens.sh composes, and the diff it names. The
# rules in tools/lens_prompt.md open with "the diff written out for you at the
# path named above. Read that file first. Do not work out a merge base
# yourself." A prompt that names no path sends the lens to compute its own base,
# which is what the sixth dry run recorded; the second lens found the gap. The
# file goes where tools/second_lens.sh puts it, `.lens/` in the tree, which is
# ignored, so `git status` stays clean.
DIFF_RANGE="$BASE_COMMIT...HEAD"
CHANGE_DIFF="$TREE/.lens/change.diff"
if ! mkdir -p "$TREE/.lens" 2>>"$LOG" \
   || ! git -C "$TREE" diff "$DIFF_RANGE" > "$CHANGE_DIFF" 2>>"$LOG" \
   || [ ! -s "$CHANGE_DIFF" ]; then
    could_not_plant "the diff for $DIFF_RANGE could not be written to $CHANGE_DIFF"
fi

PROMPT="$CANARY_DIR/prompt.md"
{
    printf 'The change under the lens is the task-list item titled:\n\n    %s\n\n' "$ITEM"
    printf 'Its worktree is %s.\n\n' "$TREE"
    printf 'The change is `git diff %s`, and it is already written out for you\n' "$DIFF_RANGE"
    printf 'at %s -- read that file first. Do not work out a\n' "$CHANGE_DIFF"
    printf 'merge base yourself: on a commit already on the pinned ref that base is\n'
    printf 'the commit itself, which is an empty diff and a pass nobody earned.\n\n'
    printf 'Call yourself `%s` in the `lens` key.\n\n---\n\n' "$LENS"
    cat "$CANARY_PROMPT"
} > "$PROMPT"

run_with_timeout() {
    if command -v timeout >/dev/null 2>&1; then
        timeout "$CANARY_TIMEOUT" "$@"
    else
        "$@"
    fi
}

ANSWER="$CANARY_DIR/refute.json"
if command -v claude >/dev/null 2>&1; then
    ( cd "$TREE" && run_with_timeout claude -p \
        --agent "$LENS" \
        --model "$CANARY_MODEL" \
        --output-format json \
        "$(cat "$PROMPT")" ) > "$ANSWER" 2>>"$LOG"
    LENS_EXIT=$?
else
    echo "monthly_canary: no claude on PATH" >> "$LOG"
    LENS_EXIT=127
fi

# Read whatever the exit status was, for the reason src/lens_verdict.py gives:
# a file that validates as a verdict is the lens's answer, and a lens can write
# a complete answer and then exit non-zero.
READING="$("$CANARY_PYTHON" -m src.canary read "$ANSWER" \
    --seed "$CANARY_SEED" --normalised "$CANARY_DIR/verdict.json" 2>>"$LOG")"

# `read` with four names, so the model takes everything left on the line rather
# than its first word.
if [ -n "$READING" ]; then
    IFS=' ' read -r RESULT FINDINGS CODE MODEL <<< "$READING"
    # Each value is printed with a closing `.` that is then taken off, because
    # command substitution strips every trailing newline and the row is matched
    # back to verdict.json character for character. The second lens found a
    # reason ending in a newline written without it.
    NAMED="$("$CANARY_PYTHON" -c \
        'import json,sys;sys.stdout.write((json.load(open(sys.argv[1])).get("canary_named") or "") + ".")' \
        "$CANARY_DIR/verdict.json" 2>>"$LOG")"
    NAMED="${NAMED%.}"
    # And why it counted, in the lens's words: a row saying only which file was
    # named cannot tell a lens that found the planted defect from one that
    # found a different one in the same file.
    WHY="$("$CANARY_PYTHON" -c \
        'import json,sys;sys.stdout.write((json.load(open(sys.argv[1])).get("canary_reason") or "") + ".")' \
        "$CANARY_DIR/verdict.json" 2>>"$LOG")"
    WHY="${WHY%.}"
else
    RESULT="no_lens_ran"
    FINDINGS=0
    CODE="$NO_LENS_RAN"
    MODEL="none"
    NAMED=""
    WHY=""
fi

# --- the record ------------------------------------------------------------

if ! "$CANARY_PYTHON" -m src.canary ledger \
        --ledger "$CANARY_LEDGER" \
        --seed "$CANARY_SEED" \
        --result "$RESULT" \
        --lens "$LENS" \
        --model "${MODEL:-unrecorded}" \
        --findings "$FINDINGS" \
        --planted-on "$PLANTED_ON" \
        ${NAMED:+--named "$NAMED"} \
        ${WHY:+--reason "$WHY"} 2>>"$LOG"; then
    note "monthly_canary: $LENS said $RESULT and the ledger line could not be written"
    echo "monthly canary: none · no_lens_ran · the record of the run was not written, which is not an approval"
    exit "$NO_LENS_RAN"
fi

case "$RESULT" in
    hit)  REASON="named $NAMED under rule $RULE" ;;
    miss) REASON="$FINDINGS finding(s) and none of them the planted one, see $CANARY_DIR/verdict.json" ;;
    *)    REASON="lens exit $LENS_EXIT, see $LOG" ;;
esac

if [ "$RESULT" = hit ] && [ -z "$CANARY_KEEP" ]; then
    git -C "$CANARY_REPO" worktree remove --force "$TREE" >>"$LOG" 2>&1
    git -C "$CANARY_REPO" branch -D "$BRANCH" >>"$LOG" 2>&1
else
    echo "monthly canary: the planted tree is kept at $TREE on $BRANCH"
fi

echo "monthly canary: $LENS · ${MODEL:-unrecorded} · $RESULT · $REASON"
exit "$CODE"
