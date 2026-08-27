import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_TOP_LEVEL_KEYS = {
    "generated_from",
    "authority",
    "scope",
    "disclaimer",
    "claims",
}
PATH_TOKEN = re.compile(r"`([^`]*(?:/|\.(?:md|json|csv))[^`]*)`")


def collapse_whitespace(value):
    return " ".join(value.split())


def results_rows():
    lines = (ROOT / "RESULTS.md").read_text(encoding="utf-8").splitlines()
    header_index = next(
        index for index, line in enumerate(lines) if line.startswith("| # | [Task]")
    )
    rows = []
    for line in lines[header_index + 2 :]:
        if not line.startswith("|"):
            break
        cells = [
            collapse_whitespace(cell)
            for cell in re.split(r"(?<!\\)\|", line.strip().strip("|"))
        ]
        assert len(cells) == 5
        task_match = re.fullmatch(r"(\[[^]]+\])\s+(.+)", cells[1])
        assert task_match is not None
        rows.append(
            {
                "id": int(cells[0]),
                "task_tag": task_match.group(1),
                "measurement": task_match.group(2),
                "published_value": cells[2],
                "limits": cells[3],
                "source_raw": cells[4],
            }
        )
    return rows


def test_claims_ledger_is_locked_to_results():
    with (ROOT / "CLAIMS.json").open(encoding="utf-8") as ledger_file:
        ledger = json.load(ledger_file)

    assert set(ledger) == EXPECTED_TOP_LEVEL_KEYS
    assert ledger["generated_from"] == "RESULTS.md"
    assert ledger["authority"] == (
        "RESULTS.md is authoritative; this file is a locked machine-readable "
        "rendering (tools/test_claims_ledger.py)"
    )
    assert ledger["scope"] == (
        "Grading: Claude-assisted, human-finalized. All results are scoped to a "
        "single Claude-based pipeline."
    )
    assert ledger["disclaimer"] == (
        "no positions · educational/informational · not investment advice."
    )

    markdown_rows = results_rows()
    claims = ledger["claims"]
    expected_ids = list(range(1, 14))
    assert len(markdown_rows) == len(claims) == 13
    assert [row["id"] for row in markdown_rows] == expected_ids
    assert [claim["id"] for claim in claims] == expected_ids

    for row, claim in zip(markdown_rows, claims):
        assert set(claim) == {
            "id",
            "task_tag",
            "measurement",
            "published_value",
            "limits",
            "source_raw",
            "source_paths",
            "status",
            "recompute",
            "limitation_ref",
        }
        for field in (
            "id",
            "task_tag",
            "measurement",
            "published_value",
            "limits",
            "source_raw",
        ):
            assert claim[field] == row[field]
        assert claim["status"] == "published"
        assert set(claim["recompute"]) == {"command", "artifacts"}
        assert isinstance(claim["recompute"]["command"], str)
        assert claim["recompute"]["artifacts"]
        assert isinstance(claim["limitation_ref"], str)

        source_tokens = PATH_TOKEN.findall(row["source_raw"])
        assert set(source_tokens) <= set(claim["source_paths"])
        for source_path in claim["source_paths"]:
            assert (ROOT / source_path.rstrip("/")).exists()


def test_real_tree_claims_coverage_green():
    """R7-7: verify_claims_coverage의 실수형(green-path)을 실제 트리에 상시 실행 —
    CLAIMS가 참조하는 산출물·recompute.command 도구 경로가 리네임/삭제되면
    verify-public(pytest 단계)과 CI가 여기서 red가 된다. 지금까지 이 도구는
    변이 사본 테스트로만 행사됐고 실트리 green은 어떤 게이트도 단정하지 않았다."""
    sys.path.insert(0, str(ROOT / "tools"))
    import verify_claims_coverage
    assert verify_claims_coverage.verify() == []


def test_claims_coverage_fails_when_results_row_is_missing(tmp_path):
    ledger = json.loads((ROOT / "CLAIMS.json").read_text(encoding="utf-8"))
    ledger["claims"] = [claim for claim in ledger["claims"] if claim["id"] != 13]
    copy = tmp_path / "CLAIMS.json"
    copy.write_text(json.dumps(ledger), encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "tools/verify_claims_coverage.py", "--claims", str(copy)],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    assert result.returncode != 0
    assert "RESULTS row 13: missing" in result.stderr
