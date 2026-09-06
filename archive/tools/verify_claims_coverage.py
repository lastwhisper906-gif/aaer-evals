#!/usr/bin/env python3
"""Verify that the claims ledger covers RESULTS and names usable evidence."""
import argparse
import json
import re
import shlex
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROW = re.compile(r"^\|\s*(\d+)\s*\|")


def _results_ids(root: Path) -> set[int]:
    return {int(match.group(1)) for line in (root / "RESULTS.md").read_text(
        encoding="utf-8").splitlines() if (match := ROW.match(line))}


def _referenced_path(command: str) -> str | None:
    if command.startswith("artifact-read: "):
        return command.removeprefix("artifact-read: ").strip()
    try:
        tokens = shlex.split(command)
    except ValueError:
        return None
    for token in tokens:
        if token.startswith(("tools/", "analysis/", "runs/")):
            return token.rstrip("/:,;)")
    return None


def verify(root: Path = REPO, claims_path: Path | None = None) -> list[str]:
    failures = []
    path = claims_path or root / "CLAIMS.json"
    try:
        claims = json.loads(path.read_text(encoding="utf-8"))["claims"]
    except (OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
        return [f"{path}: {exc}"]
    claim_ids = {claim.get("id") for claim in claims}
    for row_id in sorted(_results_ids(root) - claim_ids):
        failures.append(f"RESULTS row {row_id}: missing from CLAIMS.json")
    for claim in claims:
        label = f"claim {claim.get('id', '?')}"
        recompute = claim.get("recompute")
        if not isinstance(recompute, dict):
            failures.append(f"{label}: missing recompute object")
            continue
        artifacts = recompute.get("artifacts")
        if not isinstance(artifacts, list) or not artifacts:
            failures.append(f"{label}: recompute.artifacts must be nonempty")
        else:
            for artifact in artifacts:
                if not isinstance(artifact, str) or not (root / artifact.rstrip("/")).exists():
                    failures.append(f"{label}: missing artifact {artifact!r}")
        command = recompute.get("command")
        reference = _referenced_path(command) if isinstance(command, str) else None
        if reference is None or not (root / reference).exists():
            failures.append(f"{label}: recompute command has no existing tool/artifact")
        if not isinstance(claim.get("limitation_ref"), str):
            failures.append(f"{label}: missing limitation_ref")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--claims", type=Path)
    args = parser.parse_args()
    failures = verify(claims_path=args.claims)
    if failures:
        print("\n".join(f"FAIL: {failure}" for failure in failures), file=sys.stderr)
        return 1
    print("claims coverage: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
