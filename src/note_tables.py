"""The filing's own facts in each table of its notes that reached the bundle.

The readers see the filing; the accounting and financial analysts see the two
reader reports and `calculator_filings_only.json`, and nothing else (CLAUDE.md).
A table of the notes reached neither analyst whole: the notes reader marks a
table whose change is its amounts "amounts only" and makes no item of it, and
the numbers reader's `input_numbers.json` holds the filing's us-gaap and dei
facts but not the ones the filer tagged in its own namespace. Over the nine
reruns of 2026-10-28, 6 of the analysis-grader's 10 contradictions reported as
unresolved named a row that settled the contradiction and never reached the
analyst: Apple's intangible-assets table, whose non-current line
(`aapl:IntangibleAssetsNetExcludingGoodwillNoncurrent`) is the release's
balance-sheet line, among them.

So this carries, for each table paragraph of the triggering filing's
`input_notes.md`, the facts the filing tagged in that table, each with its
concept, value, unit, period, axes and fact id, under the paragraph's number
(`notes_38` for `<accession>:notes:38`, the id a reader's report names the
table by, which the entry also carries whole). The analyst cites a fact's
path and never adds rows up; Python does the arithmetic.

**How a table is tied to its facts.** The filing's inline XBRL document tags
each number of a note's table with an `ix:nonFraction` element inside the
`<table>`, and the instance carries the same fact under the same id with its
context and unit. A paragraph of `input_notes.md` is tied to a table of the
inline document when that table, rendered by the function that rendered the
paragraph (`clean_text.clean_stream`), reads character for character as the
paragraph. Nothing is matched by value, so a number printed in two tables is
never given to the wrong one. Two tables of the document that render the same
are one table here, and their facts are one list, a fact stated in both
listed once. A table paragraph no table renders to is listed under
`unmatched`, never guessed at.

What is left out, and why: a paragraph of the prior filing (`[same as prior
period ...]` paragraphs carry no table of this filing), a prose paragraph (its
numbers are the readers' to quote), and a text fact inside a table, which is
not a number. A per-share amount the filing states in a note -- the average
price paid in a repurchase, an option's exercise price -- is a fact of the
filing like any other and is carried; the market's price is never in a filing
and never here.
"""

from __future__ import annotations

import copy
import xml.etree.ElementTree as ET

from src import assemble_bundle, clean_text, cutoff_guard, instance_facts

IX = "http://www.xbrl.org/2013/inlineXBRL"
XHTML = "http://www.w3.org/1999/xhtml"
NOTES = "input_notes.md"
# the roles the triggering filing's own two documents are stored under
INLINE_ROLE, INSTANCE_ROLE = "primary_html", "xbrl_instance"


def _bare(element: ET.Element) -> str:
    """An element as plain HTML: the namespaces dropped, as the instance's text
    block carries the same table, so both render through one function."""
    element = copy.deepcopy(element)
    for node in element.iter():
        if isinstance(node.tag, str) and node.tag.startswith("{"):
            node.tag = node.tag.split("}", 1)[1]
        node.attrib = {key.split("}", 1)[-1]: value for key, value in node.attrib.items()}
    return ET.tostring(element, encoding="unicode")


def inline_tables(html: bytes) -> dict[str, list[str]]:
    """Each table of the inline document, rendered, to the ids of the numeric
    facts tagged inside it, in document order. A table with no rendering is
    left out."""
    root = ET.fromstring(html)
    out: dict[str, list[str]] = {}
    for table in root.iter(f"{{{XHTML}}}table"):
        ids = [fact.get("id") for fact in table.iter(f"{{{IX}}}nonFraction")]
        for rendered in clean_text.clean_stream(_bare(table))["paragraphs"]:
            held = out.setdefault(rendered.strip(), [])
            held.extend(one for one in ids if one and one not in held)
    return out


def cell(fact: dict) -> dict:
    """One fact as the analyst reads it: a cell whose `value` is the number."""
    context = fact["context"]
    out = {"concept": fact["name"], "value": fact["value"], "unit": fact["unit"]}
    if "instant" in context:
        out["instant"] = context["instant"]
    else:
        out["start"], out["end"] = context.get("start"), context.get("end")
    axes = instance_facts.members(fact)
    if axes:
        out["axes"] = axes
    if fact["nil"]:
        out["nil"] = True
    out["fact"] = fact["id"]
    return out


def key(paragraph: str) -> str:
    """A paragraph's key here: `notes_38` for `<accession>:notes:38`. The
    accession is the triggering filing's, the one every table here is from, and
    a path an analyst writes in braces is lower-case letters, digits, `_`, `.`
    and `-` (`src/analysis_check.py`, `PLACEHOLDER`), so a colon cannot be in it."""
    return "notes_" + paragraph.rsplit(":", 1)[1]


def tables(paragraphs: list[tuple[str, str]], html: bytes, instance: bytes, *,
           accession: str) -> dict:
    """The facts of each table paragraph of this filing, keyed by paragraph id."""
    rendered = inline_tables(html)
    by_id = {fact["id"].split(":", 1)[1]: fact
             for fact in instance_facts.facts(instance, accession=accession)
             if fact["kind"] == "numeric"}
    found, unmatched, untagged = {}, [], []
    for paragraph, text in paragraphs:
        if not paragraph.startswith(f"{accession}:notes:") or not text.startswith("|"):
            continue
        ids = rendered.get(text.strip())
        if ids is None:
            unmatched.append(paragraph)
            continue
        cells, seen = [], set()
        for one in ids:
            fact = by_id.get(one)
            if fact is None:
                untagged.append(f"{paragraph}: {one}")
                continue
            # one fact the document states twice, in two tables that render
            # the same, is one cell
            same = (fact["name"], fact["context_ref"], fact["unit"], fact["value"])
            if same not in seen:
                seen.add(same)
                cells.append(cell(fact))
        if cells:
            found[key(paragraph)] = {"paragraph": paragraph, "facts": cells}
    return {"tables": found, "unmatched": unmatched, "not_in_the_instance": untagged}


WHAT_THIS_IS = ("for each table of the triggering filing's notes that reached the readers "
                "(input_notes.md), the numbers the filing itself tagged in that table, read "
                "from its XBRL instance: concept, value, unit, period, axes and fact id, under "
                "the paragraph's number (notes_38 for <accession>:notes:38, the id a reader's "
                "report names the table by, which `paragraph` carries whole). A table is "
                "tied to its facts when the inline document's table renders character for "
                "character as the paragraph, never by value. Each fact is a cell whose `value` "
                "is the number; cite its path, and never add rows up")


def from_run(ticker: str, accession: str | None, cutoff, *, fixtures_root,
             bundle) -> dict:
    """The note tables of one run, or `missing` with the reason."""
    if bundle is None or not accession:
        return {"missing": "no run bundle or accession was given, so no note table was read"}
    try:
        notes = cutoff_guard.load_bundle_file(bundle, NOTES)
        rows = {row["role"]: row for row in cutoff_guard.documents(
                    ticker, fixtures_root=fixtures_root)
                if row.get("accession") == accession
                and row.get("role") in (INLINE_ROLE, INSTANCE_ROLE)}
        if set(rows) != {INLINE_ROLE, INSTANCE_ROLE}:
            return {"missing": f"the store holds no inline document and instance of "
                               f"{accession} under the roles {INLINE_ROLE} and "
                               f"{INSTANCE_ROLE}; it holds {sorted(rows)}"}
        html = cutoff_guard.load_bytes(rows[INLINE_ROLE]["full_path"], cutoff,
                                       fixtures_root=fixtures_root)
        instance = cutoff_guard.load_bytes(rows[INSTANCE_ROLE]["full_path"], cutoff,
                                           fixtures_root=fixtures_root)
    except cutoff_guard.CutoffGuardError as exc:
        return {"missing": str(exc)}
    try:
        found = tables(assemble_bundle.paragraph_blocks(notes), html, instance,
                       accession=accession)
    except ET.ParseError as exc:
        return {"missing": f"the inline document of {accession} is not well-formed XML: {exc}"}
    return {"what_this_is": WHAT_THIS_IS, **found}
