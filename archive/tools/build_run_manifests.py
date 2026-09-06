#!/usr/bin/env python3
"""Deterministically build hash-pinned manifests for result experiments."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from collections import OrderedDict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from aaer_eval.manifest import EXPERIMENT_SPECS  # noqa: E402


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fingerprint_hash(path: Path) -> str | None:
    record = json.loads(path.read_text(encoding="utf-8"))
    if "fingerprint" not in record:
        return None
    canonical = json.dumps(record["fingerprint"], ensure_ascii=False, sort_keys=True,
                           separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def case_key(root: Path, path: Path) -> str:
    rel = path.relative_to(root)
    return str(rel.with_suffix("")) if len(rel.parts) > 1 else path.stem


def generated_commit(repo: Path) -> str:
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, check=True,
                          text=True, capture_output=True).stdout.strip()


def build(experiment_id: str, repo: Path, commit: str) -> dict:
    root_rel, pattern = EXPERIMENT_SPECS[experiment_id]
    root = repo / root_rel
    paths = (sorted(p for p in root.glob(pattern) if p.name != "MANIFEST.json")
             if root.is_dir() else [])
    cases = OrderedDict()
    for path in paths:
        key = case_key(root, path)
        if key in cases:
            raise RuntimeError(f"duplicate case id: {experiment_id}: {key}")
        cases[key] = {"path": path.relative_to(repo).as_posix(), "sha256": sha256(path),
                      "fingerprint_sha256": fingerprint_hash(path)}
    return {"experiment_id": experiment_id, "generated_from_commit": commit, "cases": cases}


def render(doc: dict) -> str:
    return json.dumps(doc, ensure_ascii=False, indent=2) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    commit = generated_commit(REPO)
    changed = []
    for experiment_id in EXPERIMENT_SPECS:
        target = REPO / "runs" / experiment_id / "MANIFEST.json"
        doc = build(experiment_id, REPO, commit)
        if target.is_file():
            old = json.loads(target.read_text(encoding="utf-8"))
            dropped = set(old.get("cases", {})) - set(doc["cases"])
            if dropped:
                raise SystemExit(f"refusing to drop cases from {experiment_id}: {sorted(dropped)}")
        content = render(doc)
        if not target.is_file() or target.read_text(encoding="utf-8") != content:
            changed.append(target.relative_to(REPO).as_posix())
            if not args.check:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content, encoding="utf-8")
    if changed:
        print("run manifests differ: " + ", ".join(changed), file=sys.stderr)
        return 1 if args.check else 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
