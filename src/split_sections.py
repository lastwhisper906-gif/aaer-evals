"""The sections of a filing that carry no XBRL tag, cut out of the HTML.

MD&A, the auditor's report and the controls items are not tagged, so there is
no element to look up: the boundaries have to be found in the document. The
trap is stated in the dispatch — *picking the first match is the classic way to
extract three lines of index* — because the table of contents names every one
of these sections before the section itself appears.

The rule, validated against all twelve 10-Ks in the fixture set: a heading is a
**line of its own** in the stripped text, never a substring of running prose,
and the section's real heading is the **last** line matching it. Twelve of
twelve resolve to exactly two candidates, the table-of-contents entry and the
body heading, in that order; ESE and STX carry no matching table-of-contents
entry and resolve on a single candidate. Nothing here needs a per-company case.

One clause is load-bearing. CSCO and four others put the item marker and the
section title in adjacent table cells, so the body heading's own line is just
`Item 7.` — the same string as its table-of-contents entry. A marker alone
counts as a heading when the next non-empty line begins with the section title.

An earlier discriminator — *a table-of-contents entry sits inside an `<a href>`
and a heading does not* — was tried and rejected on the data: GNRC's real
heading is inside an anchor and CSCO's table-of-contents entry is not. It is
recorded here because it is the obvious rule and it is wrong.

    python3.12 -m src.split_sections --ticker AAPL --form 10-K --section mdna \\
        --out input_mdna.md
"""

from __future__ import annotations

import argparse
import functools
import re
import sys
from pathlib import Path

try:
    from src import cutoff_guard, html_text, interpreter_pin
except ImportError:  # invoked as a plain script
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import cutoff_guard, html_text, interpreter_pin

BAD_INPUT = 2

# `.{0,3}` spans the apostrophe a filer used: ', ’ or an entity that unescaped
# to one. Item numbers may be followed by a period, colon or any dash.
_MDNA_TITLE = r"management.{0,3}s discussion and analysis"
_MARKER = r"[.:\-–—]?\s*"


def _item(number: str, title: str = "") -> str:
    return rf"^item\s*{number}\s*{_MARKER}{title}"


class SectionNotFound(Exception):
    """The section's heading is not in this document. Never a silent empty result."""


# start:  patterns whose match on a line makes it a candidate heading.
# marker: the same item number alone on its line, promoted to a heading when
#         the next non-empty line starts with `title`.
# end:    the first line after the start matching any of these ends the section.
# select: "last" (the default rule: the table of contents comes first, the
#         section comes last) or a pattern, meaning *the first candidate whose
#         section matches it*. See `bounds` for why the auditor's report needs
#         the second rule and every item heading needs the first.
SECTIONS = {
    ("10-K", "mdna"): {
        "start": [_item("7", _MDNA_TITLE)],
        "marker": (_item("7") + r"$", rf"^{_MDNA_TITLE}"),
        "end": [_item("7a"), _item("8")],
    },
    ("10-Q", "mdna"): {
        "start": [_item("2", _MDNA_TITLE)],
        "marker": (_item("2") + r"$", rf"^{_MDNA_TITLE}"),
        "end": [_item("3"), _item("4")],
    },
    ("10-K", "auditors_report"): {
        "start": [r"^report of independent registered public accounting firm"],
        "marker": None,
        "end": [r"^consolidated statements? of operations\b",
                r"^consolidated balance sheets?\b",
                r"^consolidated statements? of income\b",
                r"^consolidated and combined statements? of operations\b",
                _item("8"), _item("9")],
        "select": r"critical audit matter",
    },
    ("10-K", "item_9a"): {
        "start": [_item("9a", r"controls and procedures")],
        "marker": (_item("9a") + r"$", r"^controls and procedures"),
        "end": [_item("9b"), _item("10")],
    },
    ("10-Q", "item_4_controls"): {
        "start": [_item("4", r"controls and procedures")],
        "marker": (_item("4") + r"$", r"^controls and procedures"),
        "end": [_item("1", r"legal proceedings"), r"^part ii\b", _item("1a")],
    },
}


def _compiled(patterns):
    return [re.compile(pattern) for pattern in patterns]


def headings(text: str, spec: dict) -> list[tuple[int, int]]:
    """Every line of `text` that is a candidate heading, as (start, end)."""
    line_spans = html_text.lines(text)
    normals = [html_text.normalized(text[start:end]) for start, end in line_spans]
    starts = _compiled(spec["start"])
    marker = None
    if spec.get("marker"):
        marker = (re.compile(spec["marker"][0]), re.compile(spec["marker"][1]))

    found = []
    for index, normal in enumerate(normals):
        if any(pattern.search(normal) for pattern in starts):
            found.append(line_spans[index])
            continue
        if marker is not None and marker[0].search(normal):
            following = normals[index + 1] if index + 1 < len(normals) else ""
            if marker[1].search(following):
                found.append(line_spans[index])
    return found


def _end_of(text: str, start: int, ends) -> int:
    for line_start, line_end in html_text.lines(text):
        if line_start <= start:
            continue
        if any(pattern.search(html_text.normalized(text[line_start:line_end]))
               for pattern in ends):
            return line_start
    return len(text)


def bounds(text: str, form: str, section: str) -> tuple[int, int, int, str]:
    """(start, end, candidate count, the rule that chose the start).

    Two selection rules, because the documents need two. An **item heading**
    (`Item 7`, `Item 9A`, `Item 4`) is named by the table of contents before
    the section appears, and the index entry always comes first, so the *last*
    candidate is the section — twelve of twelve 10-Ks resolve that way.

    The **auditor's report** does not work like that. A 10-K carries the report
    on the financial statements and, separately, the report on internal control
    over financial reporting, both under the identical heading, and it is the
    first one that carries the critical audit matters. Taking the last
    candidate there lands on the internal-control opinion every time. So this
    section is selected by content: the first candidate whose body discusses a
    critical audit matter, which is the defining content of the report the
    input spec asks for. Any table-of-contents entry is excluded by the same
    test, because an index line's "section" ends at the next index line.
    """
    spec = SECTIONS[(form, section)]
    candidates = headings(text, spec)
    if not candidates:
        raise SectionNotFound(f"{form} {section}: no heading matched")
    ends = _compiled(spec["end"])
    wanted = spec.get("select")

    if wanted and wanted != "last":
        pattern = re.compile(wanted)
        for line_start, _ in candidates:
            stop = _end_of(text, line_start, ends)
            if pattern.search(html_text.normalized(text[line_start:stop])):
                return line_start, stop, len(candidates), f"first candidate matching {wanted!r}"
        raise SectionNotFound(
            f"{form} {section}: {len(candidates)} candidate headings, none whose "
            f"body matches {wanted!r}")

    start = candidates[-1][0]
    return start, _end_of(text, start, ends), len(candidates), "last candidate"


@functools.lru_cache(maxsize=4)
def _blocks(html: str) -> tuple[dict, ...]:
    """The document's prose-and-table stream, kept for the next section asked for.

    Four sections come out of one 10-K and the stream costs a pass over every
    table in it, so the last few documents are held. The list is returned as a
    tuple to make the cached value unmodifiable by a caller.
    """
    return tuple(html_text.blocks(html))


def split(html: str, form: str, section: str) -> dict:
    """The section's text and its paragraphs, cut from the stripped document."""
    text = html_text.strip_tags(html)
    start, end, candidates, rule = bounds(text, form, section)
    body = text[start:end].strip()
    found = {
        "section": section,
        "form": form,
        "text": body,
        "paragraphs": [body[a:b] for a, b in html_text.spans(body)],
        # The same section as an ordered stream of prose and whole tables. The
        # paragraph list above is what the section *says*; this is what a
        # reader is handed, and it is where a table stays a table.
        "blocks": [block for block in _blocks(html)
                   if start <= block["start"] and block["end"] <= end],
        "heading_candidates": candidates,
        "selected_by": rule,
        "start": start,
        "end": end,
    }
    if section == "auditors_report":
        found["critical_audit_matters"] = critical_audit_matters(body)
    return found


# Each firm lays a critical audit matter out its own way, and the layout is the
# only thing that says where one matter ends and the next begins.
#   Deloitte  a "Critical Audit Matter Description" heading, then
#             "How the Critical Audit Matter Was Addressed in the Audit"
#   EY        "Description of the Matter", then
#             "How We Addressed the Matter in Our Audit"
#   PwC/KPMG/GT  no headings: one sentence per matter saying it was identified
#             as, or determined to be, a critical audit matter
#
# The two families are counted separately and the larger wins, because a
# Deloitte report carries markers from both and adding them double-counts.
_CAM_ADDRESSED = re.compile(
    r"how the critical audit matter was addressed in the audit"
    r"|how we addressed the matter in our audit")
_CAM_IDENTIFIED = re.compile(
    r"(?:is|as) a critical audit matter")
_CAM_ONE = re.compile(r"the critical audit matter communicated below is a matter")
_CAM_MANY = re.compile(r"the critical audit matters communicated below are matters")
_CAM_NONE = re.compile(r"(?:are|were) no critical audit matters")


class CriticalAuditMatterCountUnclear(Exception):
    """The count and the report's own singular/plural sentence disagree."""


def critical_audit_matters(section_text: str) -> dict:
    """How many critical audit matters the report states, and how that is known.

    The report says in its own words whether there is one matter or several.
    That sentence is not used to produce the count; it is used to check it, and
    a disagreement raises rather than resolving itself quietly.
    """
    flat = html_text.normalized(section_text)
    addressed = len(_CAM_ADDRESSED.findall(flat))
    identified = len(_CAM_IDENTIFIED.findall(flat))
    count = max(addressed, identified)
    stated = ("none" if _CAM_NONE.search(flat) else
              "many" if _CAM_MANY.search(flat) else
              "one" if _CAM_ONE.search(flat) else "unstated")

    if stated == "none" and count:
        raise CriticalAuditMatterCountUnclear(
            f"the report says there are no critical audit matters, found {count}")
    if stated == "one" and count != 1:
        raise CriticalAuditMatterCountUnclear(
            f"the report states one critical audit matter, found {count}")
    if stated == "many" and count < 2:
        raise CriticalAuditMatterCountUnclear(
            f"the report states several critical audit matters, found {count}")
    return {"count": 0 if stated == "none" else count,
            "stated": stated,
            "matched_by": "addressed_headings" if addressed >= identified else
                          "identification_sentences"}


def extract(ticker: str, form: str, section: str, *, cutoff=None,
            fixtures_root=cutoff_guard.FIXTURES) -> dict:
    cutoff = cutoff or cutoff_guard.default_cutoff(ticker, fixtures_root=fixtures_root)
    row = cutoff_guard.one_document(ticker, form, "primary_html",
                                    fixtures_root=fixtures_root)
    html = cutoff_guard.load_document(row["full_path"], cutoff,
                                      fixtures_root=fixtures_root)
    found = split(html, form, section)
    accession = row["accession"]
    found.update({
        "ticker": ticker,
        "cutoff": str(cutoff),
        "accession": accession,
        "filing_date": row["filing_date"],
        "paragraph_ids": [f"{accession}:{section}:{index}"
                          for index in range(1, len(found["paragraphs"]) + 1)],
    })
    return found


def render(payload: dict) -> str:
    lines = [f"# {payload['ticker']} {payload['form']} {payload['section']} "
             f"— {payload['accession']} filed {payload['filing_date']}", ""]
    for paragraph_id, paragraph in zip(payload["paragraph_ids"], payload["paragraphs"]):
        lines.append(f"[{paragraph_id}]")
        lines.append(paragraph)
        lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="cut an untagged section out of the HTML")
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--form", default="10-K")
    parser.add_argument("--section", default="mdna")
    parser.add_argument("--cutoff", default=None)
    parser.add_argument("--fixtures", default=str(cutoff_guard.FIXTURES))
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)

    try:
        payload = extract(args.ticker.upper(), args.form, args.section,
                          cutoff=args.cutoff, fixtures_root=Path(args.fixtures))
    except (cutoff_guard.CutoffGuardError, SectionNotFound, KeyError) as exc:
        print(f"split_sections: {exc}", file=sys.stderr)
        return BAD_INPUT
    Path(args.out).write_text(render(payload), encoding="utf-8")
    print(f"split_sections: {args.ticker.upper()} {args.form} {args.section} "
          f"{len(payload['paragraphs'])} paragraphs "
          f"({payload['heading_candidates']} heading candidates) → {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(interpreter_pin.enforce() or main())
