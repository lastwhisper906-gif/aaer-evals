"""Every fact in one filing's XBRL instance, fetched when a run needs it:
dimensional, extension and non-numeric facts included.

The fourth item of the build order in `docs/HEDGE_FUND_ANALYSIS.md` §5.1.
companyfacts holds a company's entity-wide numeric facts in the standard
taxonomies and nothing else, so three kinds of fact the analysis needs are only
in the filing's own instance:

* **dimensional** facts: a concentration percentage is stated against a
  customer axis (NVIDIA's largest direct customer, its share of revenue), a
  segment's revenue against a segment axis;
* **extension** facts: a number the filer tagged in its own namespace because no
  standard element fit (Arista's remaining performance obligations);
* **non-numeric** facts: the auditor's name, firm ID and location and whether it
  attested to internal control, in `dei`; a policy's text block.

`src/extract_numbers.py` reads the numeric us-gaap and dei facts of the committed
fixtures, and its context and unit readers are reused here, so a context reads
the same either way. This module reads every element that carries a
`contextRef`, in any namespace, and says of each whether it is numeric (it
carries a `unitRef`) and whether its namespace is the filer's own.

The instance is fetched from the EDGAR Archives through
`src/edgar_client.py`'s hash-checked cache: an accession's documents never
change, so the first fetch is the only one. A filing whose `filing_date` is
after the run's cutoff is refused before any request (CLAUDE.md: nothing filed
later enters the input).
"""

from __future__ import annotations

import io
import re
import xml.etree.ElementTree as ET

from src import cutoff_guard
from src.edgar_client import EdgarClient, EdgarError, archive_url  # noqa: F401 (archive_url is read through this module too)
from src.extract_numbers import XBRLI, XSI, _context, _number, _qname, _unit

# the hosts the standard taxonomies are published under: FASB (us-gaap, srt),
# the SEC (dei, country, currency, exch, ecd and the rest), XBRL US (the us-gaap
# and dei taxonomies of 2009 and 2010, `http://xbrl.us/us-gaap/2009-01-31`),
# XBRL International and the IFRS Foundation; any other namespace is a filer's
# extension
STANDARD = re.compile(r"https?://(?:[\w.-]*\.)?(?:fasb\.org|xbrl\.sec\.gov|xbrl\.us|"
                      r"xbrl\.org|xbrl\.ifrs\.org|w3\.org)/")
# XML Schema's two spellings of true
NIL = ("true", "1")


def instance_name(primary_document: str) -> str:
    """An inline XBRL filing's instance: `aapl-20250927.htm` → `aapl-20250927_htm.xml`."""
    stem, dot, extension = primary_document.rpartition(".")
    if not dot or extension.lower() not in ("htm", "html"):
        raise EdgarError(f"{primary_document!r} is not an inline XBRL document's name")
    return f"{stem}_{extension.lower()}.xml"


def is_extension(uri: str) -> bool:
    return not STANDARD.match(uri)


def _prefixes(xml_bytes: bytes) -> dict[str, str]:
    """Each namespace URI and the prefix the filer first declared it under."""
    found: dict[str, str] = {}
    for _, (prefix, uri) in ET.iterparse(io.BytesIO(xml_bytes), events=("start-ns",)):
        found.setdefault(uri, prefix)
    return found


def facts(xml_bytes: bytes, *, accession: str) -> list[dict]:
    """Every element with a `contextRef`, in document order, one record each."""
    prefixes = _prefixes(xml_bytes)
    root = ET.fromstring(xml_bytes)
    contexts = {node.get("id"): _context(node) for node in root.iter(f"{{{XBRLI}}}context")}
    units = {node.get("id"): _unit(node) for node in root.iter(f"{{{XBRLI}}}unit")}
    found = []
    for position, element in enumerate(root.iter()):
        context_ref = element.get("contextRef")
        if not context_ref:
            continue
        uri, local = _qname(element.tag)
        nil = (element.get(f"{{{XSI}}}nil") or "").strip() in NIL
        raw = None if nil else "".join(element.itertext())
        unit_ref = element.get("unitRef")
        numeric = unit_ref is not None
        found.append({
            "id": f"{accession}:{element.get('id') or f'n{position}'}",
            "name": f"{prefixes.get(uri, uri)}:{local}",
            "uri": uri,
            "extension": is_extension(uri),
            "kind": "numeric" if numeric else "text",
            "context": contexts.get(context_ref, {}),
            "context_ref": context_ref,
            "unit": units.get(unit_ref, unit_ref) if numeric else None,
            "decimals": element.get("decimals"),
            "raw": raw,
            "value": (_number(raw.strip()) if raw is not None else None) if numeric
            else (raw.strip() if raw is not None else None),
            "nil": nil,
            "source_accession": accession,
        })
    return found


def named(found: list[dict], name: str) -> list[dict]:
    return [fact for fact in found if fact["name"] == name]


def members(fact: dict) -> dict[str, str]:
    """A fact's explicit dimensions, axis to member."""
    return {m["dimension"]: m["member"] for m in fact["context"].get("segment", [])}


def fetch(client: EdgarClient, cik, filing: dict, name: str, *, cutoff,
          expected_sha256: str | None = None) -> list[dict]:
    """One filing's instance, through the cache, as fact records.

    `filing` is the filing's submissions row (`src/submissions.py`), whose
    `filing_date` is held to the cutoff before anything is asked of EDGAR.
    """
    limit = cutoff_guard.parse_date(cutoff, "cutoff")
    filed = cutoff_guard.parse_date(filing.get("filing_date"), "filing_date")
    if filed > limit:
        raise cutoff_guard.CutoffGuardError(
            f"{filing.get('accession')} was filed {filed.isoformat()}, after the cutoff "
            f"{limit.isoformat()}; nothing filed later enters the input")
    accession = filing["accession"]
    path = client.document(cik=str(int(cik)), accession=accession, name=name,
                           expected_sha256=expected_sha256)
    return facts(path.read_bytes(), accession=accession)
