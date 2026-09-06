import json
import sys

from analysis import fig_tradeoff


def _run_main(monkeypatch, out):
    monkeypatch.setattr(sys, "argv", ["fig_tradeoff.py", "--out", str(out)])
    return fig_tradeoff.main()


def test_main_writes_nonempty_png(tmp_path, monkeypatch):
    out = tmp_path / "tradeoff.png"
    assert _run_main(monkeypatch, out) == 0
    assert out.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")


def test_committed_png_exists_and_is_nonempty():
    assert fig_tradeoff.DEFAULT_OUT.is_file()
    assert fig_tradeoff.DEFAULT_OUT.stat().st_size > 0


def test_layer_selection_fails_closed_without_match(tmp_path, monkeypatch):
    fixture = tmp_path / "decision_table.json"
    fixture.write_text(json.dumps({"layers": {"only": {"n_treatment": 8}}}),
                       encoding="utf-8")
    monkeypatch.setattr(fig_tradeoff, "DATA_PATH", fixture)
    assert _run_main(monkeypatch, tmp_path / "absent.png") != 0


def test_top_level_exploratory_match_is_rejected(tmp_path, monkeypatch):
    fixture = tmp_path / "decision_table.json"
    out = tmp_path / "exploratory.png"
    fixture.write_text(json.dumps({
        "layers": {"only": {"n_treatment": 8}},
        "exploratory_combo": {
            "n_treatment": 12,
            "cells": [
                {"threshold": 40, "detected": 8, "n_treatment": 12,
                 "detected_ci95": [0.3489, 0.9008],
                 "false_positives": 0, "n_control": 7,
                 "fpr_ci95": [0.0, 0.4096]},
                {"threshold": 50, "detected": 7, "n_treatment": 12,
                 "detected_ci95": [0.2767, 0.8483],
                 "false_positives": 0, "n_control": 7,
                 "fpr_ci95": [0.0, 0.4096]},
                {"threshold": 60, "detected": 5, "n_treatment": 12,
                 "detected_ci95": [0.1517, 0.7233],
                 "false_positives": 0, "n_control": 7,
                 "fpr_ci95": [0.0, 0.4096]},
                {"threshold": 70, "detected": 1, "n_treatment": 12,
                 "detected_ci95": [0.0021, 0.3848],
                 "false_positives": 0, "n_control": 7,
                 "fpr_ci95": [0.0, 0.4096]},
            ],
        },
    }), encoding="utf-8")
    monkeypatch.setattr(fig_tradeoff, "DATA_PATH", fixture)
    assert _run_main(monkeypatch, out) != 0
    assert not out.exists()


def test_figure_vocabulary_is_ordinal_and_neutral():
    rendered_text = " ".join(fig_tradeoff.TEXT_STRINGS).casefold()
    barred = {"fraud", "분식", "조작", "manipulat", "probability", "확률"}
    assert not any(term in rendered_text for term in barred)
    assert "ordinal score threshold (0–100)" in rendered_text
