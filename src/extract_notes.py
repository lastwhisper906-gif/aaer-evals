"""Every note in the filing, taken by the rule the filing itself states.

Selection is one line: an element whose local name ends in `TextBlock`. Not a
list of standard tags — Item 8 notes are tagged at four levels (the whole note,
each policy, each table, each number), companies invent their own extension
tags, and a note that never reached `input_notes.md` is a quote the predictor
cannot make and a fact it cannot see. So: take all of them, in document order,
and let the diff layer shrink later.

A `TextBlock` element's content is escaped HTML. It is unescaped by the XML
parser, stripped by `src/html_text.py` — the one canonical stripper — and
written under a `## {prefix}:{name}` heading. The prefix comes from the
instance's own namespace declarations, so a company extension tag is visible as
such rather than flattened into a bare local name.

    python3.12 -m src.extract_notes --ticker AAPL --form 10-K --out input_notes.md
"""

from __future__ import annotations

import argparse
import io
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

try:
    from src import cutoff_guard, html_text, interpreter_pin
except ImportError:  # invoked as a plain script
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import cutoff_guard, html_text, interpreter_pin

BAD_INPUT = 2

# Namespaces every filer shares. Anything else in a tag's namespace is the
# filer's own extension taxonomy, which is what criterion (d) is about.
STANDARD_NAMESPACE_MARKERS = ("/us-gaap/", "/dei/", "/srt/", "xbrl.sec.gov", "fasb.org")


def _prefixes(xml_bytes: bytes) -> dict[str, str]:
    """uri → prefix, read from the instance's own xmlns declarations."""
    found: dict[str, str] = {}
    for event, payload in ET.iterparse(io.BytesIO(xml_bytes), events=("start-ns",)):
        prefix, uri = payload
        found.setdefault(uri, prefix or "")
    return found


def is_extension(uri: str) -> bool:
    return not any(marker in uri for marker in STANDARD_NAMESPACE_MARKERS)


def sections_from_instance(xml_bytes: bytes, *, accession: str,
                           filing_date: str, form: str = "") -> list[dict]:
    """One record per TextBlock element, in document order. Nothing deduplicated."""
    prefixes = _prefixes(xml_bytes)
    root = ET.fromstring(xml_bytes)
    sections = []
    for position, element in enumerate(root.iter()):
        uri, _, local = element.tag[1:].partition("}") if element.tag.startswith("{") \
            else ("", "", element.tag)
        if not local.endswith("TextBlock"):
            continue
        prefix = prefixes.get(uri, "")
        source_html = "".join(element.itertext())
        sections.append({
            "id": f"{accession}:notes:{len(sections) + 1}",
            "tag": local,
            "prefix": prefix,
            "namespace": uri,
            "name": f"{prefix}:{local}" if prefix else local,
            "extension": is_extension(uri),
            "element_id": element.get("id") or f"t{position}",
            "context_ref": element.get("contextRef"),
            "html": source_html,
            "text": html_text.strip_tags(source_html),
            "form": form,
            "source_accession": accession,
            "filing_date": filing_date,
        })
    return sections


def extract(ticker: str, form: str = "10-K", *, role: str = "xbrl_instance",
            cutoff=None, fixtures_root=cutoff_guard.FIXTURES) -> dict:
    """`role` is `xbrl_instance` for the current filing; the prior period's
    instance is stored under `prior_period_xbrl_instance` and is read the same
    way, which is what the note change history pairs."""
    cutoff = cutoff or cutoff_guard.default_cutoff(ticker, fixtures_root=fixtures_root)
    row = cutoff_guard.one_document(ticker, form, role, fixtures_root=fixtures_root)
    raw = cutoff_guard.load_bytes(row["full_path"], cutoff, fixtures_root=fixtures_root)
    sections = sections_from_instance(raw, accession=row["accession"],
                                      filing_date=row["filing_date"], form=form)
    return {
        "ticker": ticker,
        "form": form,
        "role": role,
        "cutoff": str(cutoff),
        "accession": row["accession"],
        "filing_date": row["filing_date"],
        "sections": sections,
    }


def render(payload: dict) -> str:
    """`input_notes.md`: one `## ` heading per TextBlock, then its text."""
    lines = [f"# {payload['ticker']} {payload['form']} notes "
             f"— {payload['accession']} filed {payload['filing_date']}", ""]
    for section in payload["sections"]:
        lines.append(f"## {section['name']}")
        lines.append("")
        lines.append(section["text"])
        lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="every TextBlock note, unescaped")
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--form", default="10-K")
    parser.add_argument("--cutoff", default=None)
    parser.add_argument("--fixtures", default=str(cutoff_guard.FIXTURES))
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)

    try:
        payload = extract(args.ticker.upper(), args.form, cutoff=args.cutoff,
                          fixtures_root=Path(args.fixtures))
    except cutoff_guard.CutoffGuardError as exc:
        print(f"extract_notes: {exc}", file=sys.stderr)
        return BAD_INPUT
    Path(args.out).write_text(render(payload), encoding="utf-8")
    extensions = sum(1 for section in payload["sections"] if section["extension"])
    print(f"extract_notes: {args.ticker.upper()} {args.form} "
          f"{len(payload['sections'])} notes ({extensions} on extension tags) → {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(interpreter_pin.enforce() or main())
