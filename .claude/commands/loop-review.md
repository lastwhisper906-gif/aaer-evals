---
description: Review a finished sprint and advise on merging
allowed-tools: Read, Grep, Glob, Bash(git:*), Bash(~/tools/loop-status.sh:*)
---

The sprint has finished. Help me decide.

1. `~/tools/loop-status.sh .`
2. In the worktree: `git log --oneline main..HEAD`, `git diff --stat main..HEAD`
3. Per commit (one per finding, F-xx): one line — what changed, which
   finding, and whether the diff size matches the finding's stated scope
4. Flag: diffs larger than their finding warrants; files touched in ≥3
   commits; every OWNER DECISION REQUIRED item with its anchor
5. Walk the STRATEGIC items one by one. For each: adopt / reject (→ add to
   Rejected approaches in DIRECTION_CONTEXT.md) / investigate — with reasons
6. Recommend: merge all / cherry-pick (name F-xx and SHAs) / discard
7. Remind me which BOTTLENECKS.md and DIRECTION_CONTEXT.md updates the
   accepted changes require

Do not merge, cherry-pick, or delete anything. Recommend only — I decide.
