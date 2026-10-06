"""The golden case files: a strict subset of YAML, read without a YAML library.

What is accepted, and nothing else:
- `key: value` mappings, nested by two-space indentation;
- `- ` list items, holding a scalar or a mapping;
- scalars: `true`, `false`, `null`, a number, a bare string, or a string in double
  quotes; an inline list `[a, b, "c, d"]` of scalars;
- `#` comments, on their own line or after a value.

Anything else raises `GoldenFormatError` with the line number, so a case the owner
mistyped is refused rather than read as something else.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


class GoldenFormatError(ValueError):
    pass


def _scalar(text: str, line: int):
    text = text.strip()
    if text == "":
        return None
    if text.startswith('"'):
        try:
            return json.loads(text)
        except ValueError:
            raise GoldenFormatError(f"line {line}: a quoted string does not close: {text}") from None
    if text.startswith("["):
        if not text.endswith("]"):
            raise GoldenFormatError(f"line {line}: an inline list does not close: {text}")
        inner, items, current, quoted = text[1:-1], [], "", False
        for ch in inner:
            if ch == '"':
                quoted = not quoted
            if ch == "," and not quoted:
                items.append(current)
                current = ""
            else:
                current += ch
        if current.strip():
            items.append(current)
        return [_scalar(item, line) for item in items]
    if text in ("true", "false"):
        return text == "true"
    if text == "null":
        return None
    if re.fullmatch(r"-?\d+(\.\d+)?", text):
        return float(text) if "." in text else int(text)
    if text[0] in "{&*!|>'%@`":
        raise GoldenFormatError(f"line {line}: not in the accepted subset: {text}")
    return text


def _strip_comment(raw: str) -> str:
    """A `#` after whitespace, outside double quotes, starts a comment."""
    quoted = False
    for index, ch in enumerate(raw):
        if ch == '"':
            quoted = not quoted
        elif ch == "#" and not quoted and index and raw[index - 1] in " \t":
            return raw[:index].rstrip()
    return raw


def loads(text: str):
    lines = []
    for number, raw in enumerate(text.splitlines(), 1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if "\t" in raw[: len(raw) - len(raw.lstrip())]:
            raise GoldenFormatError(f"line {number}: indentation is spaces, never a tab")
        raw = _strip_comment(raw)
        indent = len(raw) - len(raw.lstrip(" "))
        if indent % 2:
            raise GoldenFormatError(f"line {number}: indentation is in steps of two spaces")
        lines.append((indent, raw.strip(), number))
    value, rest = _block(lines, 0, 0)
    if rest != len(lines):
        raise GoldenFormatError(f"line {lines[rest][2]}: unexpected indentation")
    return value


def _block(lines, start, indent):
    if start >= len(lines):
        return None, start
    if lines[start][1].startswith("- ") or lines[start][1] == "-":
        return _list(lines, start, indent)
    return _mapping(lines, start, indent)


def _mapping(lines, index, indent):
    out = {}
    while index < len(lines) and lines[index][0] == indent:
        _, text, number = lines[index]
        if text.startswith("-"):
            raise GoldenFormatError(f"line {number}: a list item where a key was expected")
        key, sep, rest = text.partition(":")
        if not sep or not re.fullmatch(r"[a-z_][a-z0-9_]*", key):
            raise GoldenFormatError(f"line {number}: expected `key: value`, got {text}")
        if key in out:
            raise GoldenFormatError(f"line {number}: key {key} is given twice")
        index += 1
        if rest.strip():
            out[key] = _scalar(rest, number)
        elif index < len(lines) and lines[index][0] > indent:
            out[key], index = _block(lines, index, lines[index][0])
        else:
            out[key] = None
    return out, index


def _list(lines, index, indent):
    out = []
    while index < len(lines) and lines[index][0] == indent and lines[index][1].startswith("-"):
        _, text, number = lines[index]
        body = text[1:].strip()
        index += 1
        if not body:
            if index < len(lines) and lines[index][0] > indent:
                value, index = _block(lines, index, lines[index][0])
                out.append(value)
            else:
                out.append(None)
            continue
        key, sep, rest = body.partition(":")
        if sep and re.fullmatch(r"[a-z_][a-z0-9_]*", key):
            # a mapping that starts on the dash line: its keys sit two spaces in
            first_indent = indent + 2
            synthetic = [(first_indent, body, number)]
            while index < len(lines) and lines[index][0] > indent:
                synthetic.append(lines[index])
                index += 1
            value, used = _mapping(synthetic, 0, first_indent)
            if used != len(synthetic):
                raise GoldenFormatError(f"line {synthetic[used][2]}: unexpected indentation")
            out.append(value)
        else:
            out.append(_scalar(body, number))
    return out, index


def load_case(path: Path) -> dict:
    case = loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(case, dict):
        raise GoldenFormatError(f"{path}: a case is a mapping")
    for key in ("filing", "frame", "must_find", "approved_by_owner"):
        if key not in case:
            raise GoldenFormatError(f"{path}: no `{key}`")
    if case["frame"] not in ("accounting", "finance"):
        raise GoldenFormatError(f"{path}: frame is accounting or finance")
    if not isinstance(case["filing"], dict) or not case["filing"].get("accession"):
        raise GoldenFormatError(f"{path}: filing names an accession")
    return case
