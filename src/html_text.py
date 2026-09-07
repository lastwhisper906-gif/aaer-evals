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
- A run of two or more newlines collapses to exactly two. Only newlines this
  module inserted are affected; no source character is touched.

That last rule is what makes a paragraph well defined, and it is chosen to
match the independent recount the dispatch specifies — *strip tags, split on
blank lines*. Any two adjacent blocks are separated by at least a closing tag
and an opening tag, so at least two newlines, so a blank line. A lone `<br>`
contributes one newline and therefore does **not** start a new paragraph: a
line break inside an address or a signature block is part of the paragraph the
filer wrote, and an independent stripper splitting on blank lines reads it the
same way.

So `strip_tags(html)` is the filing's own characters, in the filing's own
order, with block boundaries marked. `paragraphs(html)` is that text split on
blank lines and trimmed at the edges, which trap 2 allows.
"""

from __future__ import annotations

import html as html_module
import re
from html.parser import HTMLParser

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
    return _BLANK_RUN.sub("\n\n", text).strip()


def spans(text: str) -> list[tuple[int, int]]:
    """(start, end) of every non-empty paragraph in already-stripped text.

    The offsets are into `text` itself, so `text[start:end]` is the paragraph
    and the containment property is true by construction, not by comparison.
    """
    out = []
    position = 0
    for chunk in text.split("\n\n"):
        start = position + len(chunk) - len(chunk.lstrip())
        end = position + len(chunk.rstrip())
        if end > start:
            out.append((start, end))
        position += len(chunk) + 2
    return out


def paragraphs(html: str) -> list[str]:
    """Every non-empty paragraph of the document, edge-trimmed, in order."""
    text = strip_tags(html)
    return [text[start:end] for start, end in spans(text)]


def lines(text: str) -> list[tuple[int, int]]:
    """(start, end) of every non-empty line. Headings are lines, not paragraphs.

    A section heading is its own block in every filing in the fixture set, but
    a `<br>`-separated pair of lines is one paragraph, so heading detection
    reads lines and paragraph emission reads paragraphs.
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


def normalized(text: str) -> str:
    """Whitespace-flattened text, for *matching* only — never for emitting.

    Heading detection and paragraph similarity compare through this; no
    paragraph that reaches a bundle file passes through it.
    """
    return re.sub(r"\s+", " ", text).strip().lower()


# --- tables ----------------------------------------------------------------
#
# A table is a `<table>` element. That is the definition an independent reader
# can recount by counting `<table` in the document, so it is the one used here.
# A table nested inside another — filers nest them for layout — is its own
# table, and its text belongs to it rather than to the cell containing it.

_CELLS = ("td", "th")


class _Tables(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tables: list[list[list[str]]] = []
        self._open: list[list[list[str]]] = []
        self._cell: list[str] | None = None
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self._skip += 1
        elif tag == "table":
            self._open.append([])
            self._cell = None
        elif tag == "tr" and self._open:
            self._open[-1].append([])
            self._cell = None
        elif tag in _CELLS and self._open:
            if not self._open[-1]:
                self._open[-1].append([])
            self._open[-1][-1].append("")
            self._cell = []

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self._skip = max(0, self._skip - 1)
        elif tag == "table" and self._open:
            self.tables.append([row for row in self._open.pop() if row])
            self._cell = None
        elif tag in _CELLS and self._cell is not None and self._open:
            self._open[-1][-1][-1] = "".join(self._cell).strip()
            self._cell = None

    def handle_data(self, data):
        if not self._skip and self._cell is not None:
            self._cell.append(data)


def tables(html: str) -> list[list[list[str]]]:
    """Every `<table>` in the document, as rows of cell text, in order."""
    parser = _Tables()
    parser.feed(html)
    parser.close()
    return parser.tables


def pipe_rows(table: list[list[str]]) -> list[str]:
    """One `|`-delimited line per row.

    A rendered row is a *rendering*, not a paragraph: a row has to be one line,
    so whitespace inside a cell is flattened to single spaces. The containment
    guarantee for tables therefore holds at the cell, and the tests assert it
    there. No cell's characters are otherwise touched.
    """
    return ["| " + " | ".join(normalized_spacing(cell) for cell in row) + " |"
            for row in table]


def normalized_spacing(text: str) -> str:
    """Runs of whitespace to one space. Case is left alone, unlike `normalized`."""
    return re.sub(r"\s+", " ", text).strip()
