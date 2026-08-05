import json

import pytest

from tools.multiple_testing import SOURCES, holm_adjust, load_confirmatory


REPO_ROOT = __import__("pathlib").Path(__file__).resolve().parents[1]


def test_holm_hand_computable():
    # Sorted raw values .01, .03, .04 give cumulative maxima .03, .06, .06.
    assert holm_adjust([0.04, 0.01, 0.03]) == pytest.approx([0.06, 0.03, 0.06])


def test_missing_frozen_artifact_fails_closed(tmp_path):
    artifact = tmp_path / "analysis"
    artifact.mkdir()
    with pytest.raises(FileNotFoundError, match="required frozen artifact missing"):
        load_confirmatory(tmp_path)


def test_committed_sources_and_published_adjustments():
    rows = load_confirmatory(REPO_ROOT)
    assert len(rows) == len(SOURCES) == 6
    for (_, relative, keys), (_, source, value) in zip(SOURCES, rows):
        artifact = json.loads((REPO_ROOT / relative).read_text(encoding="utf-8"))
        expected = artifact
        for key in keys:
            expected = expected[key]
        assert source == relative + ":" + ".".join(keys)
        assert value == expected

    # Literal values bind the generated Holm output to the annex table.
    assert holm_adjust([row[2] for row in rows]) == pytest.approx(
        [0.00684, 0.009435, 0.00828, 0.059613, 0.00684, 0.009435]
    )
