# Speak when a turn shipped something. Stay silent otherwise.
#
# "Shipped" is one of two things: a pull request now exists for this branch that
# did not before, or docs/next_cycle_tasks.md gained a "needs judgment" line.
# Both are read back out of the repository, because a hook cannot see what the
# session did -- only what it left behind.
#
# Neither a Slack workspace nor an iMessage bridge is configured on this
# machine, so the line goes to the macOS notification centre. When one of those
# exists, replace the osascript line and nothing else.
#
# Invoked as `sh notify_if_shipped.sh` so a missing execute bit cannot silence
# it -- that has cost a session before.

set -u

git_dir="$(git rev-parse --git-dir 2>/dev/null)" || exit 0
state="$git_dir/shipped-state"
branch="$(git branch --show-current 2>/dev/null)"
[ -n "$branch" ] || exit 0

pr="$(gh pr list --head "$branch" --state all --limit 1 --json number --jq '.[0].number' 2>/dev/null)"
[ -n "$pr" ] || pr="none"

judged="$(grep -c 'needs judgment$' docs/next_cycle_tasks.md 2>/dev/null)"
[ -n "$judged" ] || judged=0

now="$pr $judged"
prev="$(cat "$state" 2>/dev/null)"
printf '%s' "$now" > "$state"

# The first run on a branch records the baseline and says nothing. Announcing
# the state of the world on arrival is how a notifier teaches you to ignore it.
[ -n "$prev" ] || exit 0
[ "$now" != "$prev" ] || exit 0

prev_pr="${prev%% *}"
prev_judged="${prev##* }"

line=""
if [ "$pr" != "$prev_pr" ] && [ "$pr" != "none" ]; then
  line="pull request #$pr open on $branch"
fi
if [ "$judged" -gt "$prev_judged" ]; then
  [ -z "$line" ] || line="$line; "
  line="$line$((judged - prev_judged)) needs-judgment item added"
fi
[ -n "$line" ] || exit 0

osascript -e "display notification \"$line\" with title \"aaer-evals\"" >/dev/null 2>&1
exit 0
