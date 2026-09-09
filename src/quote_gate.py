"""Every report item earns its place: a quote that matches, or a citation that resolves.

`CLAUDE.md`: "Every report item carries a verbatim quote or an upstream item id
that Python verifies; a failed item is dropped and counted." This is that
verification, at all three layers. A reader item names a paragraph of that
reader's own committed input and quotes it. A comparer or supervisor item names
an upstream item id. An item that does neither is dropped before the next layer
sees it, and how many were dropped is written into `input_manifest.json`.

**String-match means string-match.** The quote has to be a substring of the
committed paragraph, character for character. Nothing is normalized: not a dash,
not a quotation mark, not a run of whitespace, not the case of a letter. What is
carried over from `archive/tools/memo_verify.py` is the idea and not the
mechanism -- that one lowercases, folds the en and em dash onto the hyphen,
folds curly quotation marks onto straight ones, collapses every whitespace run
to a single space, and only then compares, accepting a difflib ratio of 0.95.
Run over this gate's own planted paragraph it calls the changed dash and the
joined line wrap `VERIFIED` on an exact match, and the ellipsis `ALTERED` at
0.807 rather than a fabrication. Two of the three alterations this gate exists
to catch are invisible to it, so none of its normalizing comes across.

**Computed rows are quotable too.** A trend-table cell, an articulation check
and a numeric fact live in a JSON input rather than in prose, so they are named
in two ways: a numeric fact by the `id` it already carries in
`input_numbers.json`, and any other row by a JSON pointer into the file it lives
in -- `input_trends.json#/quarters/0/ratios/days_sales_outstanding`. The
quotable text is the row as printed: one line, keys sorted, which is what
`printed_row` gives it. The indentation a row wears inside the file is the
file's layout and not part of the row.

**Fail closed.** A paragraph id that resolves to nothing, an item with no id, an
empty quote, a citation that is not a string -- each is a drop and never a pass.
An empty quote is a substring of every text, so it is the one alteration a
substring test cannot see, and it is refused before the test is reached.

**Where the count goes.** `docs/INPUT_SPEC.md` §6 gives `input_manifest.json`
the dropped-item counts. The gate runs inside `read`, `compare` and `decide`,
before `publish` commits the run, so writing the count here is not a change to a
published record. It leaves every other key alone and follows the manifest's own
convention -- the list under `dropped_items`, its length under `counts` -- which
is how `paragraphs` and `exclusions` are already written.

There is no command line here. The on-disk shape of a report file is not settled
-- `docs/INPUT_SPEC.md` names `report_numbers.md` while `docs/CHECKLIST.md` §7
gives the items as JSON -- and a gate that had to guess it would be guessing
about the file it polices. The runner holds the parsed items and calls `gate`.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    from src import assemble_bundle, cutoff_guard
except ImportError:  # invoked as a plain script
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import assemble_bundle, cutoff_guard

MANIFEST = "input_manifest.json"
NUMBERS = "input_numbers.json"

# A pointer that resolves to a JSON `null` and a pointer that resolves to
# nothing are different answers, and only one of them is a paragraph.
_ABSENT = object()


class QuoteGateError(Exception):
    """The gate cannot run. It never turns into a pass."""


# --- what a committed input offers to be quoted ------------------------------

def printed_row(node) -> str:
    """A computed row as printed: one line, keys sorted. A string prints as itself."""
    if isinstance(node, str):
        return node
    return json.dumps(node, sort_keys=True)


def _at_pointer(payload, pointer: str):
    """The node a JSON pointer names, or `_ABSENT`. RFC 6901 and nothing beyond it."""
    if pointer == "":
        return payload
    if not pointer.startswith("/"):
        return _ABSENT
    node = payload
    for token in pointer.split("/")[1:]:
        token = token.replace("~1", "/").replace("~0", "~")
        if isinstance(node, list):
            if not token.isdigit() or int(token) >= len(node):
                return _ABSENT
            node = node[int(token)]
        elif isinstance(node, dict):
            if token not in node:
                return _ABSENT
            node = node[token]
        else:
            return _ABSENT
    return node


def quotable(input_dir) -> dict[str, str]:
    """Paragraph id → the committed text it owns, for one agent's input directory.

    The prose files by their `[id]` lines, and `input_numbers.json` by the id
    each fact already carries. Rows named by a JSON pointer are resolved when a
    quote asks for one, because a pointer names a row that need not be indexed
    in advance.
    """
    folder = Path(input_dir)
    if not folder.is_dir():
        raise QuoteGateError(
            f"{folder} is not a directory — an agent whose committed input is not "
            "on disk has nothing for a quote to be matched against")
    index: dict[str, str] = {}

    def record(identifier: str, text: str, where: str) -> None:
        if identifier in index:
            raise QuoteGateError(
                f"{identifier} is in {where} and already in this input — one id "
                "names one paragraph, and a quote matched against the wrong "
                "paragraph is not a verified quote")
        index[identifier] = text

    for name in cutoff_guard.bundle_files(folder, "*.md"):
        for identifier, body in assemble_bundle.paragraph_blocks(
                cutoff_guard.load_bundle_file(folder, name)):
            record(identifier, body, name)
    if cutoff_guard.bundle_files(folder, NUMBERS):
        payload = json.loads(cutoff_guard.load_bundle_file(folder, NUMBERS))
        for fact in payload.get("facts") or []:
            if isinstance(fact, dict) and isinstance(fact.get("id"), str):
                record(fact["id"], printed_row(fact), NUMBERS)
    return index


def committed_text(input_dir, paragraph_id: str, index: dict | None = None) -> str | None:
    """The text one paragraph id owns, or None when it names nothing in this input."""
    if "#" in paragraph_id:
        name, _, pointer = paragraph_id.partition("#")
        if not name or name != Path(name).name:
            return None
        if not cutoff_guard.bundle_files(input_dir, name):
            return None
        try:
            payload = json.loads(cutoff_guard.load_bundle_file(input_dir, name))
        except ValueError:
            return None
        node = _at_pointer(payload, pointer)
        return None if node is _ABSENT else printed_row(node)
    if index is None:
        index = quotable(input_dir)
    return index.get(paragraph_id)


# --- why one item is dropped -------------------------------------------------

def item_id(item) -> str | None:
    """The item's own id, or None when it has none worth citing."""
    identifier = item.get("id") if isinstance(item, dict) else None
    return identifier if isinstance(identifier, str) and identifier.strip() else None


def quote_drop_reason(item, input_dir, index: dict | None = None) -> str | None:
    """Why this reader item is dropped, or None when it stands."""
    if item_id(item) is None:
        return "the item carries no id, so nothing downstream could cite it"
    paragraph_id = item.get("paragraph_id")
    if not isinstance(paragraph_id, str) or not paragraph_id:
        return "the item names no paragraph id"
    quote = item.get("quote")
    if not isinstance(quote, str) or not quote:
        return "the item carries no quote, and an empty quote matches every text"
    text = committed_text(input_dir, paragraph_id, index)
    if text is None:
        return f"paragraph id {paragraph_id} is not in this reader's committed input"
    if quote not in text:
        return f"the quote does not string-match {paragraph_id} in the committed input"
    return None


def citations(item) -> list:
    """Every upstream item id this item leans on, from the three places a schema puts one.

    `docs/CHECKLIST.md` §7: a comparer item carries `upstream_item_id`, a
    supervisor checklist entry carries `evidence[].upstream_item_id`, and
    `market_direction.basis` is a list of them.
    """
    found: list = []
    if not isinstance(item, dict):
        return found
    if "upstream_item_id" in item:
        found.append(item["upstream_item_id"])
    evidence = item.get("evidence")
    if isinstance(evidence, list):
        for entry in evidence:
            found.append(entry.get("upstream_item_id")
                         if isinstance(entry, dict) else entry)
    basis = item.get("basis")
    if isinstance(basis, list):
        found.extend(basis)
    return found


def citation_drop_reason(item, upstream_ids) -> str | None:
    """Why this comparer or supervisor item is dropped, or None when it stands."""
    if item_id(item) is None:
        return "the item carries no id, so nothing downstream could cite it"
    cited = citations(item)
    if not cited:
        return "the item cites no upstream item"
    for one in cited:
        if not isinstance(one, str) or one not in upstream_ids:
            return f"the citation {one!r} does not resolve to an upstream item"
    return None


# --- the gate over a whole run -----------------------------------------------

def write_counts(bundle_root, dropped: list[dict]) -> dict:
    """The drop count into `input_manifest.json`. Every other key is left alone."""
    try:
        manifest = json.loads(cutoff_guard.load_bundle_file(bundle_root, MANIFEST))
    except ValueError as exc:
        raise QuoteGateError(f"{MANIFEST} does not parse as JSON: {exc}") from exc
    if not isinstance(manifest, dict):
        raise QuoteGateError(f"{MANIFEST} is not an object, so it has no counts to write")
    manifest["dropped_items"] = [dict(row) for row in dropped]
    if not isinstance(manifest.get("counts"), dict):
        manifest["counts"] = {}
    manifest["counts"]["dropped_items"] = len(dropped)
    (Path(bundle_root) / MANIFEST).write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def gate(reports: list[dict], bundle_root) -> dict:
    """Every report in layer order: what stands, what was dropped, and the count on disk.

    `reports` is one entry per report, in the order the layers ran:

        {"report": "report_notes_text.md", "items": [...], "input": <directory>}
        {"report": "report_notes_vs_market.md", "items": [...],
         "cites": ["report_notes_text.md"]}

    A report naming an `input` is a reader's and its items are quoted against
    that directory; a report naming what it `cites` is a comparer's or a
    supervisor's and its items cite. A citation resolves against the ids the
    upstream report **kept**, so an item dropped at one layer cannot be cited at
    the next — which is what "dropped before the next layer sees it" means.
    """
    kept: dict[str, list[dict]] = {}
    kept_ids: dict[str, set[str]] = {}
    dropped: list[dict] = []
    for entry in reports:
        name = entry["report"]
        if name in kept:
            raise QuoteGateError(f"{name} is gated twice; one report is gated once")
        if ("input" in entry) == ("cites" in entry):
            raise QuoteGateError(
                f"{name} has to name either the input its items quote or the "
                "reports its items cite, and exactly one of the two")
        items = list(entry.get("items") or [])
        if "input" in entry:
            index = quotable(entry["input"])
            reasons = [quote_drop_reason(item, entry["input"], index) for item in items]
        else:
            upstream_ids: set[str] = set()
            for upstream in entry["cites"]:
                if upstream not in kept_ids:
                    raise QuoteGateError(
                        f"{name} cites {upstream}, which has not been gated yet — a "
                        "citation resolves against what the upstream report kept")
                upstream_ids |= kept_ids[upstream]
            reasons = [citation_drop_reason(item, upstream_ids) for item in items]

        standing, standing_ids = [], set()
        for item, why in zip(items, reasons):
            if why is None:
                standing.append(item)
                standing_ids.add(item_id(item))
            else:
                dropped.append({"report": name, "item_id": item_id(item), "reason": why})
        kept[name], kept_ids[name] = standing, standing_ids

    write_counts(bundle_root, dropped)
    return {"kept": kept, "dropped": dropped}
