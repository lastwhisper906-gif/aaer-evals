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
from html.parser import HTMLParser

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
    return Source(source_html).contains(emitted)


class Source:
    """One document, stripped once, then asked about many paragraphs.

    A 10-K is a megabyte and a section can hold fifteen hundred paragraphs, so
    re-stripping per paragraph turns a containment test into a coffee break.
    """

    def __init__(self, source_html: str) -> None:
        self.squeezed = squeeze(strip(source_html))

    def contains(self, emitted: str) -> bool:
        return squeeze(emitted) in self.squeezed

    def missing(self, emitted: list[str]) -> list[str]:
        """The paragraphs that are not runs of this source. Empty is the pass."""
        return [text for text in emitted if not self.contains(text)]


# --- a second implementation of "strip tags, split on blank lines" ----------
#
# `strip()` above cannot answer a *paragraph count*: it deletes block tags
# along with everything else, so there are no blank lines left to split on.
# This one is built on html.parser instead of a regex — a different mechanism
# reading the same specification — so a paragraph count taken through it is an
# independent recount of src/html_text.py, not a restatement of it.

BLOCK = frozenset("""
    address article aside blockquote br caption center dd div dl dt fieldset
    figcaption figure footer form h1 h2 h3 h4 h5 h6 header hr li main nav ol p
    pre section table tbody td tfoot th thead tr ul
""".split())

_BLANK = re.compile(r"\n[^\S\n]*(?:\n[^\S\n]*)+")


class _Blocks(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self._skip += 1
        elif tag in BLOCK:
            self.out.append("\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self._skip = max(0, self._skip - 1)
        elif tag in BLOCK:
            self.out.append("\n")

    def handle_startendtag(self, tag, attrs):
        if tag in BLOCK:
            self.out.append("\n")

    def handle_data(self, data):
        if not self._skip:
            self.out.append(data)

    def text(self) -> str:
        return _BLANK.sub("\n\n", "".join(self.out)).strip()


def block_text(source_html: str) -> str:
    """Tag-stripped text with block boundaries kept, built on html.parser."""
    parser = _Blocks()
    parser.feed(source_html)
    parser.close()
    return parser.text()


def block_paragraphs(source_html: str) -> list[str]:
    """The same text, split on blank lines and trimmed. The recount."""
    return [chunk.strip() for chunk in block_text(source_html).split("\n\n")
            if chunk.strip()]
