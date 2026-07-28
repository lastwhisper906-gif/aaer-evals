---
description: Stop the direction-review loop cleanly
allowed-tools: Bash(touch:*), Bash(~/tools/loop-status.sh:*), Bash(git:*)
---

1. Locate the loop worktree: <parent>/<repo-name>-loop
2. `touch <worktree>/.direction/STOP`
3. Tell me it halts at the cycle boundary (may take minutes). Never kill the
   process — a hard kill can interrupt a mid-write edit.
4. When it halts, an EXECUTIVE BRIEF prints automatically (and is saved as
   BRIEF.md in the run directory). Point me to it; do not re-summarize it.
