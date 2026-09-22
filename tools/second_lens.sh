#!/usr/bin/env bash
#
# The second lens on one change: Codex first, Claude Fable when Codex cannot run.
#
#     tools/second_lens.sh <worktree> <item-title>
#
# Both lenses read the same file, tools/lens_prompt.md, and answer the same
# file, tools/lens_verdict.schema.json. They are handed the same composed
# prompt, byte for byte, so a verdict from one is comparable with a verdict from
# the other and neither can drift from the five rules.
#
# Codex is the cross-vendor lens: the builder and the first refute lens are both
# Claude, so a blind spot in that family is a blind spot in both. When Codex
# cannot run -- no binary, a quota that is out, a crash, an answer that is not a
# verdict -- the fallback is Claude Fable in a fresh context. That is a weaker
# check and it is recorded as one: the ledger line says which lens answered, and
# the weekly re-lens routine re-reads every fallback row once the quota returns.
#
# Exit codes
#
#     0  pass
#     1  fail
#     2  needs judgment
#     3  no lens ran
#
# Three is never an approval. It is the one outcome that says nothing about the
# change, and the build skill opens the pull request with the label "one-lens"
# and leaves auto-merge off when it sees it.
#
# The lens having failed to run is judged by whether a file came back that
# validates against the schema, never by matching a string in the output. A
# quota message, a refusal, a truncated answer and a crash all carry no verdict,
# and they all have to land in the same place. src/lens_verdict.py is what
# decides that, and the exit codes above are written there too.
#
# The ledger line carries the model as well as the lens, because they are not
# the same fact: LENS_FALLBACK_MODEL can put a different model behind the name
# `claude-fable-fallback`, and a record that says only the name would not show
# it. The fallback's model is read out of the answer's own usage record, and
# Codex's out of the banner its run prints, so both are what served rather than
# what was asked for.
#
# Environment, all with defaults, all overridden by the test:
#
#     LENS_PROMPT  LENS_SCHEMA  LENS_LEDGER  LENS_PYTHON  LENS_TIMEOUT
#     LENS_FALLBACK_MODEL

set -u

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

LENS_PROMPT="${LENS_PROMPT:-$REPO_ROOT/tools/lens_prompt.md}"
LENS_SCHEMA="${LENS_SCHEMA:-$REPO_ROOT/tools/lens_verdict.schema.json}"
LENS_LEDGER="${LENS_LEDGER:-$REPO_ROOT/events/ledger.jsonl}"
LENS_PYTHON="${LENS_PYTHON:-$REPO_ROOT/.venv/bin/python}"
LENS_TIMEOUT="${LENS_TIMEOUT:-1800}"

# `-m src.lens_verdict` has to resolve to this repository's module whatever
# directory the caller ran from -- a worktree, the repository root, or neither.
PYTHONPATH="$REPO_ROOT${PYTHONPATH:+:$PYTHONPATH}"
export PYTHONPATH

CODEX_LENS="codex"
FALLBACK_LENS="claude-fable-fallback"
NO_LENS_RAN=3

if [ "$#" -ne 2 ]; then
    echo "usage: tools/second_lens.sh <worktree> <item-title>" >&2
    exit "$NO_LENS_RAN"
fi

WORKTREE="$1"
ITEM="$2"

if [ ! -d "$WORKTREE" ]; then
    echo "second_lens: no worktree at $WORKTREE" >&2
    exit "$NO_LENS_RAN"
fi
WORKTREE="$(cd "$WORKTREE" && pwd)"
LENS_DIR="$WORKTREE/.lens"
mkdir -p "$LENS_DIR"

# One composed prompt, handed to both lenses unchanged. The item and the tree it
# is in are the only thing added to tools/lens_prompt.md, and they are added
# once rather than per lens, so the two cannot be given different work.
PROMPT="$LENS_DIR/prompt.md"
{
    printf 'The change under the lens is the task-list item titled:\n\n    %s\n\n' "$ITEM"
    printf 'Its worktree is %s. Call yourself `%%LENS%%` in the `lens` key.\n\n---\n\n' "$WORKTREE"
    cat "$LENS_PROMPT"
} > "$PROMPT"

run_with_timeout() {
    if command -v timeout >/dev/null 2>&1; then
        timeout "$LENS_TIMEOUT" "$@"
    else
        "$@"
    fi
}

# The lens's own name is the one thing that differs between the two prompts, and
# it is written to a file rather than piped: a pipeline's exit status is its last
# command's, and a red run has been committed through one before.
prompt_for() {
    sed "s/%LENS%/$1/" "$PROMPT" > "$LENS_DIR/prompt.$1.md"
    echo "$LENS_DIR/prompt.$1.md"
}

# --- the cross-vendor lens -------------------------------------------------

CODEX_FILE="$LENS_DIR/codex.json"
rm -f "$CODEX_FILE"
CODEX_LOG="$LENS_DIR/codex.log"

if command -v codex >/dev/null 2>&1; then
    CODEX_PROMPT="$(prompt_for "$CODEX_LENS")"
    run_with_timeout codex exec \
        --sandbox read-only \
        -C "$WORKTREE" \
        --output-schema "$LENS_SCHEMA" \
        -o "$CODEX_FILE" \
        - < "$CODEX_PROMPT" > "$CODEX_LOG" 2>&1
    CODEX_EXIT=$?
else
    echo "second_lens: no codex on PATH" > "$CODEX_LOG"
    CODEX_EXIT=127
fi

VERDICT=""
LENS=""
NORMALISED="$LENS_DIR/verdict.json"
rm -f "$NORMALISED"

# The reading is four fields -- verdict, how many findings, the exit code this
# script answers with, and the model that served it. The code comes from
# src/lens_verdict.py rather than from a mapping written a second time here.
read_verdict() {
    set -- $1
    VERDICT="$1"
    FINDINGS="$2"
    CODE="$3"
    MODEL="$4"
}

# The file is read whatever the exit status was. A verdict that validates
# against the schema is the lens's answer, and the exit status is not part of
# that sentence: Codex can write a complete `fail` and then exit non-zero -- a
# timeout killed after the file was flushed, a cleanup that failed -- and
# throwing that away would let the same-family fallback overwrite a cross-vendor
# fail with a pass, which is the one path this whole design says cannot happen.
# The status is kept for the reason line and for nothing else.
READING="$("$LENS_PYTHON" -m src.lens_verdict codex "$CODEX_FILE" \
    --lens "$CODEX_LENS" --normalised "$NORMALISED" 2>>"$CODEX_LOG")"
if [ $? -eq 0 ]; then
    read_verdict "$READING"
    LENS="$CODEX_LENS"
    # Codex names the model it ran in its own banner. Read from the run rather
    # than assumed, and left unrecorded when the banner is not there.
    FROM_BANNER="$(sed -n 's/^model: //p' "$CODEX_LOG" | head -1)"
    if [ -n "$FROM_BANNER" ]; then
        MODEL="$FROM_BANNER"
    fi
fi

# --- the same-family fallback ----------------------------------------------

if [ -z "$LENS" ]; then
    FABLE_FILE="$LENS_DIR/fable.json"
    rm -f "$FABLE_FILE"
    FABLE_LOG="$LENS_DIR/fable.log"
    if command -v claude >/dev/null 2>&1; then
        # Started *in* the worktree, the way Codex is with -C. The prompt's
        # first instruction is "the working tree you were started in", and this
        # script is called from the repository root against a detached worktree
        # by docs/routines/weekly-relens.md -- so a fallback left in the
        # caller's directory would review main and answer about a tree the item
        # never produced.
        FABLE_PROMPT="$(prompt_for "$FALLBACK_LENS")"
        ( cd "$WORKTREE" && run_with_timeout claude -p \
            --agent refute-check \
            --model "${LENS_FALLBACK_MODEL:-fable}" \
            --output-format json \
            "$(cat "$FABLE_PROMPT")" ) > "$FABLE_FILE" 2>"$FABLE_LOG"
        FABLE_EXIT=$?
    else
        echo "second_lens: no claude on PATH" > "$FABLE_LOG"
        FABLE_EXIT=127
    fi
    # Read whatever the exit status was, for the same reason as above.
    READING="$("$LENS_PYTHON" -m src.lens_verdict claude "$FABLE_FILE" \
        --lens "$FALLBACK_LENS" --normalised "$NORMALISED" 2>>"$FABLE_LOG")"
    if [ $? -eq 0 ]; then
        read_verdict "$READING"
        LENS="$FALLBACK_LENS"
    fi
fi

# --- the record ------------------------------------------------------------

if [ -z "$LENS" ]; then
    LENS="none"
    VERDICT="no_lens_ran"
    FINDINGS=0
    CODE="$NO_LENS_RAN"
    MODEL="none"
fi

# The ledger line is what docs/routines/weekly-relens.md greps for to find the
# rows only one lens read. A pass whose ledger write failed would merge with no
# row, and the routine would never come back to it -- so a ledger that could not
# be written is not an approval either.
if ! "$LENS_PYTHON" -m src.lens_verdict ledger \
    --ledger "$LENS_LEDGER" \
    --item "$ITEM" \
    --lens "$LENS" \
    --verdict "$VERDICT" \
    --findings "$FINDINGS" \
    --model "${MODEL:-unrecorded}"; then
    echo "second lens: $LENS said $VERDICT and the ledger line could not be written" >&2
    echo "second lens: none · no_lens_ran · the record of the run was not written, which is not an approval"
    exit "$NO_LENS_RAN"
fi

case "$VERDICT" in
    pass)           REASON="tried to break it and could not" ;;
    fail)           REASON="$FINDINGS finding(s), see $NORMALISED" ;;
    needs_judgment) REASON="$FINDINGS open question(s), see $NORMALISED" ;;
    *)              REASON="codex exit $CODEX_EXIT, fallback exit ${FABLE_EXIT:-not reached}" ;;
esac

echo "second lens: $LENS · ${MODEL:-unrecorded} · $VERDICT · $REASON"
exit "$CODE"
