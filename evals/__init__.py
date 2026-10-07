"""The owner's evaluation code. Claude reads it and never writes it (CLAUDE.md).

Graders read run directories, never how an agent got there. They import nothing
from `src/` except where a check is about `src/` itself, so a change to the
pipeline cannot quietly change what the pipeline is graded against.
"""
