"""Every numeric fact in a company's XBRL instances, as filed.

Numeric means *carries a `unitRef`* — that is what the instance itself says
about a fact, and it is the whole selection rule. There is no curated tag list:
the earlier experiment read roughly sixty tags, and a ratio a reader cannot
recompute because the tag behind it was never extracted is not evidence.

Each fact records the tag's local name and namespace prefix, its context, its
unit, `decimals`, the value as the string exactly as filed, the parsed number,
and the accession and filing date of the document it came from.

**Context is period plus segment.** Filings report the same tag for the same
period against several dimensions — AAPL's `c-2`, `c-3` and `c-4` are one period
differing only by `StatementClassOfStockAxis`. Recording the period alone would
collapse every dimensional fact onto its undimensioned sibling and make the
point-in-time rule choose between facts that are not the same fact, so the
segment members travel with the period and are part of a fact's identity.

**Point in time.** When two filings at or before the cutoff report the same
(tag, period, segment, unit), the later filing wins. The superseded fact stays
in the file carrying `superseded_by` with the winner's accession: ground truth
is the first-reported value, so a restatement has to be visible as a
replacement rather than quietly overwrite the record.

    python3.12 -m src.extract_numbers --ticker AAPL --form 10-K --out numbers.json
"""

from __future__ import annotations

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

try:
    from src import cutoff_guard, interpreter_pin
except ImportError:  # invoked as a plain script
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import cutoff_guard, interpreter_pin

XBRLI = "http://www.xbrl.org/2003/instance"
XBRLDI = "http://xbrl.org/2006/xbrldi"
XSI = "http://www.w3.org/2001/XMLSchema-instance"

# The two namespaces the input spec names. Matched on the URI rather than on a
# prefix, because a filer chooses its own prefixes.
NAMESPACES = {"/us-gaap/": "us-gaap", "/dei/": "dei"}

BAD_INPUT = 2


def _qname(tag: str) -> tuple[str, str]:
    """`{uri}local` → (uri, local)."""
    if tag.startswith("{"):
        uri, _, local = tag[1:].partition("}")
        return uri, local
    return "", tag


def _prefix(uri: str) -> str | None:
    for marker, prefix in NAMESPACES.items():
        if marker in uri:
            return prefix
    return None


def _context(node: ET.Element) -> dict:
    """Period and segment, in the shape the fact record carries them."""
    period = node.find(f"{{{XBRLI}}}period")
    out: dict = {}
    if period is not None:
        instant = period.find(f"{{{XBRLI}}}instant")
        if instant is not None:
            out["instant"] = (instant.text or "").strip()
        else:
            start = period.find(f"{{{XBRLI}}}startDate")
            end = period.find(f"{{{XBRLI}}}endDate")
            out["start"] = (start.text or "").strip() if start is not None else None
            out["end"] = (end.text or "").strip() if end is not None else None
    members = [
        {"dimension": member.get("dimension"), "member": (member.text or "").strip()}
        for member in node.iter(f"{{{XBRLDI}}}explicitMember")
    ]
    out["segment"] = sorted(members, key=lambda m: (m["dimension"] or "", m["member"]))
    return out


def _unit(node: ET.Element) -> str:
    """The unit as written: `iso4217:USD`, or `shares/iso4217:USD` for a divide."""
    def measures(parent: ET.Element) -> list[str]:
        return [(m.text or "").strip() for m in parent.findall(f"{{{XBRLI}}}measure")]

    divide = node.find(f"{{{XBRLI}}}divide")
    if divide is not None:
        numerator = divide.find(f"{{{XBRLI}}}unitNumerator")
        denominator = divide.find(f"{{{XBRLI}}}unitDenominator")
        top = "*".join(measures(numerator)) if numerator is not None else ""
        bottom = "*".join(measures(denominator)) if denominator is not None else ""
        return f"{top}/{bottom}"
    return "*".join(measures(node))


def _number(text: str | None):
    if text is None:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def facts_from_instance(xml_bytes: bytes, *, accession: str, filing_date: str,
                        form: str = "") -> list[dict]:
    """Every `unitRef`-carrying us-gaap or dei element, in document order.

    One record per element. Nothing is deduplicated here: a filing that reports
    a fact twice reported it twice, and the count of this list is the count an
    independent reader gets from the instance.
    """
    root = ET.fromstring(xml_bytes)
    contexts = {node.get("id"): _context(node)
                for node in root.iter(f"{{{XBRLI}}}context")}
    units = {node.get("id"): _unit(node) for node in root.iter(f"{{{XBRLI}}}unit")}

    facts = []
    for position, element in enumerate(root.iter()):
        unit_ref = element.get("unitRef")
        if not unit_ref:
            continue
        uri, local = _qname(element.tag)
        prefix = _prefix(uri)
        if prefix is None:
            continue
        nil = element.get(f"{{{XSI}}}nil") == "true"
        value = None if nil else (element.text or "").strip()
        element_id = element.get("id") or f"n{position}"
        facts.append({
            "id": f"{accession}:{element_id}",
            "tag": local,
            "prefix": prefix,
            "namespace": uri,
            "context": contexts.get(element.get("contextRef"), {}),
            "context_ref": element.get("contextRef"),
            "unit": units.get(unit_ref, unit_ref),
            "decimals": element.get("decimals"),
            "value": value,
            "number": _number(value),
            "nil": nil,
            "form": form,
            "source_accession": accession,
            "filing_date": filing_date,
        })
    return facts


def identity(fact: dict) -> tuple:
    """What makes two facts from different filings the same fact."""
    context = fact.get("context") or {}
    segment = tuple((m.get("dimension"), m.get("member"))
                    for m in context.get("segment", []))
    return (fact["prefix"], fact["tag"], context.get("start"), context.get("end"),
            context.get("instant"), segment, fact["unit"])


def apply_point_in_time(facts: list[dict]) -> list[dict]:
    """Mark every fact a later filing replaced. Nothing is dropped.

    Facts repeated inside one filing are left alone — a filing does not
    supersede itself, and the count has to stay the count the instance supports.
    """
    winners: dict[tuple, dict] = {}
    for fact in facts:
        key = identity(fact)
        best = winners.get(key)
        if best is None or (fact["filing_date"], fact["source_accession"]) > \
                (best["filing_date"], best["source_accession"]):
            winners[key] = fact
    for fact in facts:
        winner = winners[identity(fact)]
        if winner["source_accession"] != fact["source_accession"]:
            fact["superseded_by"] = winner["source_accession"]
    return facts


def extract(ticker: str, forms=("10-K",), *, cutoff=None,
            fixtures_root=cutoff_guard.FIXTURES) -> dict:
    """Every numeric fact for one company, from the forms asked for."""
    cutoff = cutoff or cutoff_guard.default_cutoff(ticker, fixtures_root=fixtures_root)
    rows = [row for form in forms
            for row in cutoff_guard.documents(ticker, form=form, role="xbrl_instance",
                                              fixtures_root=fixtures_root)]
    rows.sort(key=lambda r: (r["filing_date"], r["accession"]))
    facts, documents = [], []
    for row in rows:
        raw = cutoff_guard.load_bytes(row["full_path"], cutoff, fixtures_root=fixtures_root)
        facts.extend(facts_from_instance(raw, accession=row["accession"],
                                         filing_date=row["filing_date"],
                                         form=row["form"]))
        documents.append({"form": row["form"], "accession": row["accession"],
                          "filing_date": row["filing_date"], "path": row["path"]})
    return {
        "ticker": ticker,
        "cutoff": str(cutoff),
        "documents": documents,
        "facts": apply_point_in_time(facts),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="every numeric XBRL fact, as filed")
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--form", action="append", default=None,
                        help="10-K or 10-Q (repeatable); default is both")
    parser.add_argument("--cutoff", default=None,
                        help="ISO date; default is the fixture set's as-of date")
    parser.add_argument("--fixtures", default=str(cutoff_guard.FIXTURES))
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)

    forms = tuple(args.form) if args.form else ("10-K", "10-Q")
    try:
        payload = extract(args.ticker.upper(), forms, cutoff=args.cutoff,
                          fixtures_root=Path(args.fixtures))
    except cutoff_guard.CutoffGuardError as exc:
        print(f"extract_numbers: {exc}", file=sys.stderr)
        return BAD_INPUT
    Path(args.out).write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n",
                              encoding="utf-8")
    print(f"extract_numbers: {args.ticker.upper()} {'+'.join(forms)} "
          f"{len(payload['facts'])} facts → {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(interpreter_pin.enforce() or main())
