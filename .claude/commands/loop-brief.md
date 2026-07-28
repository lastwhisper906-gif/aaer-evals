---
description: Show (or regenerate) the executive brief for the latest run
allowed-tools: Read, Bash(git:*), Bash(~/tools/loop-status.sh:*), Bash(cat:*), Bash(ls:*)
---

1. Locate the loop worktree and its latest run directory (.direction/2*).
2. If BRIEF.md exists there: print it verbatim, then one line pointing to
   facts.txt for cross-checking. Do NOT paraphrase or embellish it.
3. If BRIEF.md is missing but facts.txt exists: show facts.txt and say the
   brief generation failed on that run.
4. If I ask you to regenerate: write a brief yourself following
   ~/tools/prompts/brief.md EXACTLY — including its grounding rules. Every
   claim carries a commit SHA or path from facts.txt; nothing invented;
   uncertain items go under "확인 필요".
