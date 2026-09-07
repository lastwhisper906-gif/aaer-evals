"""A second, deliberately naive tag stripper, written for the tests alone.

`src/html_text.py` is the canonical stripper, so asserting that its own output
contains its own output proves nothing. This module strips tags the obvious
way — delete everything between angle brackets, unescape once — and imports
nothing from `src/`. Every containment assertion in the parser tests is made
twice: once against the canonical text (exact, catching any mutation the
pipeline makes) and once against this one (catching a canonical stripper that
invents or loses characters).

The two strippers cannot agree on whitespace, and no rule makes them: one marks
block boundaries with a newline and the other does not, so
`<td>a</td><td>b</td>` is `a\\nb` here and `ab` there — one has whitespace the
other lacks, in both directions depending on the tag. So the cross-check
compares the two texts with **all** whitespace removed: the claim it tests is
that the sequence of non-whitespace characters a parser emits is a contiguous
run of the source's own non-whitespace characters. An invented word, a
normalised quote mark, a fixed hyphen, a dropped clause, two distant paragraphs
welded together — every one of those still fails. Only whitespace is forgiven,
and only because the alternative is a test that asserts `src/html_text.py`
agrees with itself.

The whitespace-sensitive half of the property is not given up; it is asserted
separately, exactly, against the canonical stripper.
"""

from __future__ import annotations

import html
import re

_TAG = re.compile(r"<[^>]*>", re.DOTALL)
_DROPPED = re.compile(r"<(script|style)\b.*?</\1\s*>", re.DOTALL | re.IGNORECASE)
_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)


def strip(html_source: str) -> str:
    """Delete the tags, unescape once. Nothing clever."""
    text = _COMMENT.sub("", html_source)
    text = _DROPPED.sub("", text)
    return html.unescape(_TAG.sub("", text))


def flat(text: str) -> str:
    """One space for every run of whitespace. For readable failure messages."""
    return re.sub(r"\s+", " ", text).strip()


def squeeze(text: str) -> str:
    """The non-whitespace characters, in order. What the two strippers share."""
    return re.sub(r"\s+", "", text)


def contains(source_html: str, emitted: str) -> bool:
    """Is `emitted` a contiguous run of the source's own characters?"""
    return squeeze(emitted) in squeeze(strip(source_html))
