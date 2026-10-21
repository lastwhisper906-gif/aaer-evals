#!/bin/sh
# One pass of the improvement loop (docs/improve_loop.md): a nested session on
# Opus, told the improve skill, under the fences and a budget.
#
#   sh tools/improve.sh [BUDGET_USD] [PROMPT]   # default 60, list price; the prompt
#                                              # defaults to the skill's text, a probe may name another
#
# The session reads no project settings and no project skills (`--restricted`
# is not used, because the pass runs tests and measurements; `--setting-sources`
# is left empty for the same effect, checked on 2026-10-21: the session listed
# no project skill), so the improve skill is sent as the message itself, its
# front matter cut and $ARGUMENTS replaced by the budget, and the session takes
# its whole configuration from `--settings` built here: the Edit and Write tools denied on every fence (the list is in
# `.claude/hooks/guard_fences.py`, printed by `--deny-rules`), the Bash guards
# for evals/ and the fences before every command, the plain-name check after
# every write, and the tools it may use without asking. The model is an alias.
# The CLI's own `--max-budget-usd` stops the session at the budget; `measure
# plan` refuses a measurement that would exceed it before any call is made.
set -eu
cd "$(dirname "$0")/.."
BUDGET="${1:-60}"
SKILL="$(python3 - "$BUDGET" <<'EOF'
import re, sys
text = open(".claude/skills/improve/SKILL.md", encoding="utf-8").read()
print(re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.S).replace("$ARGUMENTS", sys.argv[1]))
EOF
)"
PROMPT="${2:-$SKILL}"
DENY="$(python3 .claude/hooks/guard_fences.py --deny-rules)"
SETTINGS="$(python3 - "$DENY" <<'EOF'
import json, sys
deny = json.loads(sys.argv[1])
print(json.dumps({
    "permissions": {
        "allow": ["Read(**)", "Edit(**)", "Write(**)", "Glob(**)", "Grep(**)", "Bash(*)",
                  "Agent(*)", "Skill(*)"],
        "deny": deny},
    "hooks": {
        "PreToolUse": [{"matcher": "Bash", "hooks": [
            {"type": "command", "command": "python3 .claude/hooks/guard_evals.py", "timeout": 15},
            {"type": "command", "command": "python3 .claude/hooks/guard_fences.py", "timeout": 15}]}],
        "PostToolUse": [{"matcher": "Write|Edit", "hooks": [
            {"type": "command",
             "command": "test -f src/plain_name_check.py || exit 0; python3.12 -m src.plain_name_check --changed",
             "timeout": 30}]}]}}))
EOF
)"
exec env -u CLAUDECODE -u CLAUDE_CODE_ENTRYPOINT claude -p \
  --model fable --effort xhigh \
  --permission-mode dontAsk \
  --setting-sources "" \
  --settings "$SETTINGS" \
  --max-budget-usd "$BUDGET" \
  --output-format stream-json --verbose \
  "$PROMPT" < /dev/null
