"""One tag stripper, used by every parser that reads HTML.

The success criterion this file exists for is *every quote exists in those
inputs*, which the dispatch operationalises as: every paragraph a parser emits
is a contiguous substring of the tag-stripped source. That property is only
meaningful against **one** canonical stripper. Two strippers that disagree make
the assertion pass in each parser and mean nothing across the bundle, which is
exactly the defect the property exists to catch — so the notes extractor, the
section splitters, the 8-K parser, the cleaner and the differ all call this.

The contract, and the reason for each half of it:

- Comments and the contents of `<script>` and `<style>` are dropped. They are
  not text a reader sees and they are not quotable.
- A **block-level** tag becomes a single `\\n`. That newline is the only
  character this module introduces, and it never lands inside a block, so it
  can never appear inside a paragraph.
- Every **other** tag is deleted, replaced by nothing at all. Not by a space:
  a space would be a character that is not in the filing, and SEC inline-XBRL
  documents wrap individual words in `<span>`, so replacing those with spaces
  invents whitespace in the middle of sentences.
- Entities are unescaped once, after the tags are gone (unescaping first would
  turn an escaped `&lt;p&gt;` in the body text into a tag).
- `&#160;` stays `\\xa0`. It is **not** normalised to a space. Trap 2 says
  nothing inside a paragraph may change, and a non-breaking space is a
  character the filer wrote. `str.strip()` and `\\s` in a regex both treat it
  as whitespace, so nothing downstream has to care.
- Runs of newlines collapse to one. Only newlines this module inserted are
  affected; no source character is touched.

So `strip_tags(html)` is the filing's own characters, in the filing's own
order, with block boundaries marked. `paragraphs(html)` is that text split on
those boundaries and trimmed at the edges, which trap 2 allows.
"""

from __future__ import annotations

import html as html_module
import re

BLOCK_TAGS = frozenset("""
    address article aside blockquote br caption center dd div dl dt fieldset
    figcaption figure footer form h1 h2 h3 h4 h5 h6 header hr li main nav ol p
    pre section table tbody td tfoot th thead tr ul
""".split())

_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
_DROPPED = re.compile(r"<(script|style)\b.*?</\1\s*>", re.DOTALL | re.IGNORECASE)
_TAG = re.compile(r"<[^>]*>", re.DOTALL)
_TAG_NAME = re.compile(r"^</?\s*([A-Za-z][A-Za-z0-9:_.-]*)")
# Newlines this module inserted, run together. [^\S\n] is whitespace that is
# not a newline, which includes the non-breaking space.
_BLANK_RUN = re.compile(r"\n[^\S\n]*(?:\n[^\S\n]*)+")


def _replace_tag(match: re.Match) -> str:
    name = _TAG_NAME.match(match.group(0))
    if name is not None and name.group(1).lower() in BLOCK_TAGS:
        return "\n"
    return ""


def strip_tags(html: str) -> str:
    """The canonical tag-stripped text of an HTML document."""
    text = _COMMENT.sub("", html)
    text = _DROPPED.sub("", text)
    text = _TAG.sub(_replace_tag, text)
    text = html_module.unescape(text)
    return _BLANK_RUN.sub("\n", text).strip("\n")


def spans(text: str) -> list[tuple[int, int]]:
    """(start, end) of every non-empty block in already-stripped text.

    The offsets are into `text` itself, so `text[start:end]` is the block and
    the containment property is true by construction rather than by comparison.
    """
    out = []
    position = 0
    for line in text.split("\n"):
        start = position + len(line) - len(line.lstrip())
        end = position + len(line.rstrip())
        if end > start:
            out.append((start, end))
        position += len(line) + 1
    return out


def paragraphs(html: str) -> list[str]:
    """Every non-empty block of the document, edge-trimmed, in document order."""
    text = strip_tags(html)
    return [text[start:end] for start, end in spans(text)]


def normalized(text: str) -> str:
    """Whitespace-flattened text, for *matching* only — never for emitting.

    Heading detection and paragraph similarity compare through this; nothing
    that reaches a bundle file passes through it.
    """
    return re.sub(r"\s+", " ", text).strip().lower()
