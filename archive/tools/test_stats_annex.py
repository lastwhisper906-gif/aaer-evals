import importlib.util
import json
import math
import re
import subprocess
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "tools/stats_annex.py"
SPEC = importlib.util.spec_from_file_location("stats_annex", SCRIPT)
ANNEX = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ANNEX)


def run(*args):
    return subprocess.check_output([sys.executable, str(SCRIPT), *args], text=True)


def artifact_value(document, key):
    value = document
    for part in key.split("."):
        value = value[part]
    return value


def test_output_is_deterministic():
    assert run() == run()
    assert run("--json") == run("--json")


def test_mc_se_formula_spot_check():
    row = ANNEX.build_annex()["mc_p_values"][0]
    expected = math.sqrt(0.00114 * (1 - 0.00114) / 100_000)
    assert math.isclose(row["mc_se"], expected, rel_tol=0, abs_tol=1e-18)


def test_every_reported_p_equals_committed_artifact():
    documents = {}
    rows = ANNEX.build_annex()["mc_p_values"]
    assert len(rows) == 9
    for row in rows:
        documents.setdefault(row["artifact"], json.loads((REPO / row["artifact"]).read_text()))
        assert row["p"] == artifact_value(documents[row["artifact"]], row["key"])


def test_json_matches_printed_numbers():
    data = json.loads(run("--json"))
    printed = run()
    for row in data["mc_p_values"]:
        lo, hi = row["mc_interval_95"]
        assert repr(row["p"]) in printed
        assert f'{row["mc_se"]:.12g}' in printed
        assert f'[{lo:.12g}, {hi:.12g}]' in printed
    for row in data["exact_permutation_feasibility"]:
        assert f'{row["design"]} | {row["permutations"]}' in printed


def test_source_citations_point_to_real_files():
    source = SCRIPT.read_text()
    citations = re.findall(r"analysis/[A-Za-z0-9_./]+\.py:\d+", source)
    assert citations
    for citation in citations:
        path, line = citation.rsplit(":", 1)
        lines = (REPO / path).read_text().splitlines()
        assert 1 <= int(line) <= len(lines)
