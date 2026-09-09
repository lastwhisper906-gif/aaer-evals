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

**A computed row is the committed file's own characters.** A trend cell and a
numeric fact live in a JSON input rather than in prose, and the text they offer
to be quoted is the slice of the committed file they occupy -- indentation, line
breaks and key order as the file wrote them. `printed_row` re-renders a node and
then *locates* it in the file, so what comes back is a slice and not a rendering
that merely looks like one. Matching against a re-rendering is matching against
text the reader never saw: `{"days": 91, "value": 51.7}` appears in no committed
input, because `input_trends.json` writes those two keys on two lines under a
two-space indent, and a gate that accepted that string would be accepting a
quote of nothing while refusing the same characters copied out of the file.

**A row's id is one its reader can write.** `docs/INPUT_SPEC.md` §2.2 gives a
trend cell `{accession}:trends:{metric}:{period}`: the metric is the ratio's own
key and the period is the row's own `label`, both printed in `input_trends.json`
where the reader can read them. A numeric fact is named by the `id` the fact
already carries and the file already prints. The spec's other spelling for a
fact, `{accession}:facts:{tag}:{period}`, is not resolved here: a fact's period
has no printed spelling in the committed input -- a context is a start and an
end, or an instant -- and tag-and-period is not unique across segments, so the
gate would be minting a name that neither the writer of the file nor its reader
could produce. That divergence between the spec and the file is the spec's to
settle. Articulation checks have no committed input yet -- `src/articulation.py`
is unwritten -- so their ids resolve to nothing and an item quoting one is
dropped, which is the fail-closed direction and reverses itself the day the
input exists.

**Only what the input declares is quotable.** The index holds the ids the
committed files carry: the `[id]` lines of the prose, the facts of
`input_numbers.json`, the cells of `input_trends.json`. There is no way to name
an arbitrary file and an arbitrary depth inside it. An earlier draft had one, a
JSON pointer, and it made every JSON file that happened to sit in the directory
quotable -- `input_manifest.json`, which carries the text of the paragraphs the
pipeline *excluded* from that reader's input, and `input_market.json` if a
broken run put one there. Certifying a quote of text the reader was never given
is the failure this gate exists to catch, not one for it to commit.

**One id names one item.** An item id carried by more than one item in the run
-- twice in one report, or once in each of two -- is dropped everywhere it
appears and resolves for nobody. A citation is meant to name one upstream claim;
against a repeated id it names a set, and a dropped item's id would go on being
citable through its twin.

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

There is no command line here, and nothing calls `gate` yet because there is no
stage runner to call it: `docs/HOW_WE_WORK.md` names the stages and no module
runs them. The on-disk shape of a report file is unsettled too --
`docs/INPUT_SPEC.md` names `report_numbers.md` while `docs/CHECKLIST.md` §7
gives the items as JSON -- and a gate that had to guess it would be guessing
about the file it polices. The runner holds the parsed items and calls `gate`.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

try:
    from src import assemble_bundle, cutoff_guard
except ImportError:  # invoked as a plain script
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import assemble_bundle, cutoff_guard

MANIFEST = "input_manifest.json"
NUMBERS = "input_numbers.json"
TRENDS = "input_trends.json"

# The indent every committed JSON input is written under.
INDENT = 2

# How deep a computed row sits in the file that holds it: a fact is the `n`th
# entry of `facts`, a trend cell the `metric` of the `n`th period's `ratios`.
# The depth is what tells the row's own indentation from the file's.
FACT_DEPTH = 2
RATIO_DEPTH = 4


class QuoteGateError(Exception):
    """The gate cannot run. It never turns into a pass."""


# --- what a committed input offers to be quoted ------------------------------

def printed_row(file_text: str, node, depth: int) -> str | None:
    """The slice of a committed file one computed row occupies, or None.

    `json.dumps` lays a node out from the node alone, so the only things the
    file adds are the indent the row's depth carries and whether whoever wrote
    the file sorted the keys -- `src/trends.py:509` does and
    `src/assemble_bundle.py:499` does not. Both are settled by finding the
    result in the file rather than by being told, and a row that is not found
    there is not quotable at all.
    """
    for sort_keys in (False, True):
        block = json.dumps(node, indent=INDENT, sort_keys=sort_keys)
        block = block.replace("\n", "\n" + " " * (INDENT * depth))
        if block in file_text:
            return block
    return None


def _json_input(bundle_root, name: str) -> tuple[str, dict]:
    """One committed JSON file of a bundle, as its text and its object."""
    text = cutoff_guard.load_bundle_file(bundle_root, name)
    try:
        payload = json.loads(text)
    except ValueError as exc:
        raise QuoteGateError(f"{name} does not parse as JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise QuoteGateError(f"{name} is not an object, so it holds nothing to quote")
    return text, payload


def _computed_rows(folder: Path, accession: str):
    """(id, printed row, file) for every computed row a committed input declares.

    A numeric fact by the `id` it already carries; a trend cell by the id
    `docs/INPUT_SPEC.md` §2.2 gives it, `{accession}:trends:{metric}:{period}`,
    whose metric is the ratio's own key and whose period is the row's own
    `label` — both printed in the file, so the reader can write the id it
    quotes. A row the file does not print as this module expects yields
    nothing, and an item quoting it is dropped.
    """
    if cutoff_guard.bundle_files(folder, NUMBERS):
        text, payload = _json_input(folder, NUMBERS)
        for fact in payload.get("facts") or []:
            if not isinstance(fact, dict) or not isinstance(fact.get("id"), str):
                continue
            row = printed_row(text, fact, FACT_DEPTH)
            if row is not None:
                yield fact["id"], row, NUMBERS

    if cutoff_guard.bundle_files(folder, TRENDS):
        text, payload = _json_input(folder, TRENDS)
        for section in ("quarters", "years"):
            for period in payload.get(section) or []:
                if not isinstance(period, dict):
                    continue
                label, ratios = period.get("label"), period.get("ratios")
                if not isinstance(label, str) or not isinstance(ratios, dict):
                    continue
                for metric, cell in ratios.items():
                    row = printed_row(text, cell, RATIO_DEPTH)
                    if row is not None:
                        yield f"{accession}:trends:{metric}:{label}", row, TRENDS


def quotable(input_dir, accession: str) -> dict[str, str]:
    """Paragraph id → the committed text it owns, for one agent's input directory.

    The prose files by their `[id]` lines, and the computed rows by the ids
    `_computed_rows` gives them. A file that declares no ids of its own — the
    market table, the manifest, anything else that lands in the directory —
    offers nothing here for a quote to be matched against.
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

    for identifier, row, where in _computed_rows(folder, accession):
        record(identifier, row, where)
    return index


# --- why one item is dropped -------------------------------------------------

def item_id(item) -> str | None:
    """The item's own id, or None when it has none worth citing."""
    identifier = item.get("id") if isinstance(item, dict) else None
    return identifier if isinstance(identifier, str) and identifier.strip() else None


def quote_drop_reason(item, index: dict) -> str | None:
    """Why this reader item is dropped, or None when it stands."""
    if item_id(item) is None:
        return "the item carries no id, so nothing downstream could cite it"
    paragraph_id = item.get("paragraph_id")
    if not isinstance(paragraph_id, str) or not paragraph_id:
        return "the item names no paragraph id"
    quote = item.get("quote")
    if not isinstance(quote, str) or not quote:
        return "the item carries no quote, and an empty quote matches every text"
    if paragraph_id not in index:
        return f"paragraph id {paragraph_id} is not in this reader's committed input"
    if quote not in index[paragraph_id]:
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

def _write_counts(bundle_root, manifest: dict, dropped: list[dict]) -> None:
    """The drop count into `input_manifest.json`. Every other key is left alone."""
    manifest = dict(manifest)
    manifest["dropped_items"] = [dict(row) for row in dropped]
    counts = manifest.get("counts")
    manifest["counts"] = dict(counts) if isinstance(counts, dict) else {}
    manifest["counts"]["dropped_items"] = len(dropped)
    (Path(bundle_root) / MANIFEST).write_text(
        json.dumps(manifest, indent=INDENT, sort_keys=True) + "\n", encoding="utf-8")


def _repeated_ids(reports: list[dict]) -> set[str]:
    """Every item id that more than one item in the run carries."""
    counted = Counter(item_id(item) for entry in reports
                      for item in entry.get("items") or [])
    return {identifier for identifier, count in counted.items()
            if identifier is not None and count > 1}


def gate(reports: list[dict], bundle_root) -> dict:
    """Every report in layer order: what stands, what was dropped, and the count on disk.

    `reports` is one entry per report, in the order the layers ran:

        {"report": "report_notes_text.md", "items": [...], "input": <directory>}
        {"report": "report_notes_vs_market.md", "items": [...],
         "cites": ["report_notes_text.md"]}

    A report naming an `input` is a reader's and its items are quoted against
    that directory; a report naming what it `cites` is a comparer's or a
    supervisor's and its items cite. `cites` is what the report is allowed to
    label, not what its layer can see — `docs/INPUT_SPEC.md` gives a comparer
    both reader reports and lets it label only its own. A citation resolves
    against the ids the upstream report **kept**, so an item dropped at one
    layer cannot be cited at the next — which is what "dropped before the next
    layer sees it" means.
    """
    manifest = _json_input(bundle_root, MANIFEST)[1]
    accession = manifest.get("accession")
    if not isinstance(accession, str) or not accession:
        raise QuoteGateError(
            f"{MANIFEST} names no accession, and a computed row's id begins with one")
    repeated = _repeated_ids(reports)

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

        index, upstream_ids = None, set()
        if "input" in entry:
            index = quotable(entry["input"], accession)
        else:
            for upstream in entry["cites"]:
                if upstream not in kept_ids:
                    raise QuoteGateError(
                        f"{name} cites {upstream}, which has not been gated yet — a "
                        "citation resolves against what the upstream report kept")
                upstream_ids |= kept_ids[upstream]

        standing, standing_ids = [], set()
        for item in entry.get("items") or []:
            identifier = item_id(item)
            if identifier in repeated:
                why = (f"the item id {identifier} is on more than one item in this "
                       "run, so a citation naming it would not name one item")
            elif index is not None:
                why = quote_drop_reason(item, index)
            else:
                why = citation_drop_reason(item, upstream_ids)
            if why is None:
                standing.append(item)
                standing_ids.add(identifier)
            else:
                dropped.append({"report": name, "item_id": identifier, "reason": why})
        kept[name], kept_ids[name] = standing, standing_ids

    _write_counts(bundle_root, manifest, dropped)
    return {"kept": kept, "dropped": dropped}
