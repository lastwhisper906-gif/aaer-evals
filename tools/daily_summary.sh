# The daily summary: where the project stands, once a day, to the notification
# centre. Status only -- it never asks a question and nothing waits on it.
#
# The full text goes to standard output, because a notification holds two lines
# and the ledger tail does not fit in them. The notification carries the counts
# and the fact that there is a fuller text to read.
#
# Invoked as `sh tools/daily_summary.sh` from the repository root, so a missing
# execute bit cannot silence it -- that has cost a session before.

set -u

cd "$(git rev-parse --show-toplevel 2>/dev/null)" || exit 2

head_line="$(git log --oneline -1 main 2>/dev/null)"
ready="$(grep -c '^\[ \]' docs/next_cycle_tasks.md 2>/dev/null)"
judgment="$(grep -c '^\[ \]' docs/needs_judgment.md 2>/dev/null)"
[ -n "$ready" ] || ready=0
[ -n "$judgment" ] || judgment=0

# What moved in the ledger since yesterday, read out of git rather than out of a
# state file: a state file says what some previous run believed, the history says
# what happened.
moved="$(git log --since=24.hours --oneline -- docs/next_cycle_tasks.md 2>/dev/null)"
[ -n "$moved" ] || moved="(the ledger did not move)"

prs="$(gh pr list --state open --limit 20 \
        --json number,title --jq '.[] | "  #\(.number) \(.title)"' 2>/dev/null)"
pr_count="$(printf '%s' "$prs" | grep -c '^  #')"
[ -n "$prs" ] || prs="  (none open)"

printf 'aaer-evals, %s\n\n' "$(date '+%Y-%m-%d %H:%M')"
printf 'main            %s\n' "$head_line"
printf 'ready to build  %s items\n' "$ready"
printf 'needs judgment  %s rows, in docs/needs_judgment.md\n' "$judgment"
printf 'open pull requests (%s)\n%s\n\n' "$pr_count" "$prs"
printf 'ledger commits in the last day\n%s\n\n' "$moved"
printf 'needs-judgment rows\n'
grep '^\[ \]' docs/needs_judgment.md 2>/dev/null | cut -c1-100

line="$ready to build, $pr_count pull requests open, $judgment for the owner"
osascript -e "display notification \"$line\" with title \"aaer-evals daily summary\"" >/dev/null 2>&1
exit 0
