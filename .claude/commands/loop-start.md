---
description: Start the direction-review loop detached (one sprint)
allowed-tools: Bash(~/tools/*), Bash(tmux:*), Bash(git:*)
argument-hint: [--review-only N] [--cycles N]
---

Start one sprint of the direction-review loop as a detached process.
Pass through arguments: $ARGUMENTS

1. Start detached (the harness runs its own preflight gate — do NOT run
   preflight separately, it burns six live canary calls):
   `tmux new-session -d -s dloop "~/tools/direction-loop.sh $(git rev-parse --show-toplevel) $ARGUMENTS"`
   If tmux is unavailable:
   `nohup ~/tools/direction-loop.sh $(git rev-parse --show-toplevel) $ARGUMENTS > ~/dloop.log 2>&1 &`
2. Wait ~30 seconds, run `~/tools/loop-status.sh .` once.
3. If it failed at the preflight or sign-off gate, report exactly which gate
   and stop. Do not work around a gate.
4. Otherwise report worktree, branch, and that /loop-stop halts it.

Do not run the loop in the foreground. Do not tail logs.
