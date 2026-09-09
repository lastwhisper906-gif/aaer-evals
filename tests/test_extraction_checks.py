"""Four gates, and four bundles damaged one way each to prove they close.

A check that has only ever been run on good input is not a check. Every gate
here is exercised twice: once on all twelve real bundles, where it must pass,
and once on a bundle damaged in exactly the way that gate exists to catch,
where it must fail, exit non-zero, and say which gate it was.
"""

from __future__ import annotations

import functools
import json
from pathlib import Path

import pytest

from src import assemble_bundle, extraction_checks
from src.fetch_fixtures import TICKERS


@functools.lru_cache(maxsize=None)
def _built(ticker: str, form: str) -> dict:
    return assemble_bundle.build(ticker, form)


def good_bundle(tmp_path: Path, ticker: str = "AAPL", form: str = "10-Q") -> Path:
    out = tmp_path / f"{ticker}-{form}"
    assemble_bundle.write(_built(ticker, form), out)
    return out


def rewrite(bundle: Path, name: str, change) -> None:
    payload = json.loads((bundle / name).read_text(encoding="utf-8"))
    change(payload)
    (bundle / name).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                               encoding="utf-8")


def gate_lines(lines: list[str], gate: str) -> list[str]:
    return [line for line in lines if line.startswith(f"{gate}: ")]


# --- (e) every real bundle passes -------------------------------------------

@pytest.mark.parametrize("ticker", TICKERS)
def test_a_real_bundle_passes_every_gate(ticker, tmp_path):
    code, lines = extraction_checks.run(good_bundle(tmp_path, ticker))
    assert code == 0, "\n".join(lines)
    assert [line.split(":")[0] for line in lines] == \
        ["schema", "paragraph counts", "cutoff", "notes"]
    assert all(": pass — " in line for line in lines)


def test_a_ten_k_bundle_passes_too(tmp_path):
    code, lines = extraction_checks.run(good_bundle(tmp_path, "AAPL", "10-K"))
    assert code == 0, "\n".join(lines)


# --- (b) the command ---------------------------------------------------------

def test_the_command_prints_one_line_per_gate(tmp_path, capsys):
    assert extraction_checks.main([str(good_bundle(tmp_path))]) == 0
    printed = capsys.readouterr().out.strip().split("\n")
    assert len(printed) == 4
    for gate in ("schema", "paragraph counts", "cutoff", "notes"):
        assert gate_lines(printed, gate), gate


def test_the_command_refuses_something_that_is_not_a_directory(tmp_path):
    assert extraction_checks.main([str(tmp_path / "nowhere")]) == 2


def test_a_failing_run_prints_to_stderr_and_exits_non_zero(tmp_path, capsys):
    bundle = good_bundle(tmp_path)
    (bundle / "input_notes.md").write_text("# nothing\n", encoding="utf-8")
    assert extraction_checks.main([str(bundle)]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "notes: FAIL" in captured.err


# --- (c) one damaged bundle per gate ----------------------------------------

def test_a_missing_key_fails_the_schema_gate(tmp_path):
    bundle = good_bundle(tmp_path)
    rewrite(bundle, "input_numbers.json", lambda payload: payload.pop("facts"))
    code, lines = extraction_checks.run(bundle)
    assert code != 0
    assert gate_lines(lines, "schema") == ['schema: FAIL — input_numbers.json has no "facts"']


def test_a_document_that_contributed_to_nothing_fails_the_schema_gate(tmp_path):
    """`manifest.documents` is what the build read. A row that names no file it
    fed is the "documents provided" list wearing the other one's name."""
    bundle = good_bundle(tmp_path)

    def damage(payload):
        payload["documents"][0]["contributed_to"] = []
    rewrite(bundle, "input_manifest.json", damage)
    code, lines = extraction_checks.run(bundle)
    assert code != 0
    assert "names no file it contributed to" in "\n".join(gate_lines(lines, "schema"))


def test_a_document_with_no_url_fails_the_schema_gate(tmp_path):
    bundle = good_bundle(tmp_path)

    def damage(payload):
        payload["documents"][0]["url"] = ""
    rewrite(bundle, "input_manifest.json", damage)
    code, lines = extraction_checks.run(bundle)
    assert code != 0
    assert "has no url" in "\n".join(gate_lines(lines, "schema"))


def test_a_missing_file_fails_the_schema_gate(tmp_path):
    bundle = good_bundle(tmp_path)
    (bundle / "input_trends.json").unlink()
    code, lines = extraction_checks.run(bundle)
    assert code != 0
    assert "input_trends.json is not in the bundle" in "\n".join(gate_lines(lines, "schema"))


def test_a_paragraph_count_thirty_percent_low_fails_the_count_gate(tmp_path):
    bundle = good_bundle(tmp_path)

    def damage(payload):
        payload["counts"]["notes"] = int(payload["counts"]["notes"] * 0.70)
    rewrite(bundle, "input_manifest.json", damage)
    code, lines = extraction_checks.run(bundle)
    assert code != 0
    failures = gate_lines(lines, "paragraph counts")
    assert len(failures) == 1
    assert "notes is" in failures[0] and "outside ±20%" in failures[0]


def test_a_count_inside_the_band_still_passes(tmp_path):
    """The band has to be a band, or the check fires on every rebuild."""
    bundle = good_bundle(tmp_path)

    def nudge(payload):
        payload["counts"]["notes"] = int(payload["counts"]["notes"] * 0.90)
    rewrite(bundle, "input_manifest.json", nudge)
    assert extraction_checks.run(bundle)[0] == 0


def test_a_document_dated_after_the_cutoff_fails_the_cutoff_gate(tmp_path):
    bundle = good_bundle(tmp_path)

    def damage(payload):
        payload["documents"][0]["filing_date"] = "2027-01-01"
    rewrite(bundle, "input_manifest.json", damage)
    code, lines = extraction_checks.run(bundle)
    assert code != 0
    failures = gate_lines(lines, "cutoff")
    assert len(failures) == 1
    assert "was filed 2027-01-01, after the cutoff" in failures[0]


def test_an_empty_notes_file_fails_the_notes_gate(tmp_path):
    bundle = good_bundle(tmp_path)
    (bundle / "input_notes.md").write_text("# AAPL notes\n\nnothing here\n",
                                           encoding="utf-8")
    code, lines = extraction_checks.run(bundle)
    assert code != 0
    assert "no TextBlock section" in "\n".join(gate_lines(lines, "notes"))


# --- (d) the cutoff gate is fail-closed --------------------------------------

def test_a_document_with_no_filing_date_fails_the_cutoff_gate(tmp_path):
    bundle = good_bundle(tmp_path)

    def damage(payload):
        payload["documents"][0].pop("filing_date")
    rewrite(bundle, "input_manifest.json", damage)
    code, lines = extraction_checks.run(bundle)
    assert code != 0
    assert "has no date" in "\n".join(gate_lines(lines, "cutoff"))


def test_a_manifest_with_no_cutoff_fails_the_cutoff_gate(tmp_path):
    bundle = good_bundle(tmp_path)
    rewrite(bundle, "input_manifest.json", lambda payload: payload.pop("cutoff"))
    code, lines = extraction_checks.run(bundle)
    assert code != 0
    assert "unusable cutoff" in "\n".join(gate_lines(lines, "cutoff"))


def test_an_unparseable_filing_date_fails_the_cutoff_gate(tmp_path):
    bundle = good_bundle(tmp_path)

    def damage(payload):
        payload["documents"][0]["filing_date"] = "last Tuesday"
    rewrite(bundle, "input_manifest.json", damage)
    assert extraction_checks.run(bundle)[0] != 0


def test_a_cutoff_that_is_not_the_triggering_reports_filing_date_fails(tmp_path):
    """The gate used to compare every document to `manifest.cutoff` and never
    ask what that cutoff was. A bundle built with a later cutoff passed: every
    document it swept in was inside a boundary it had moved for itself. Here the
    cutoff is pushed a year out and every document is still under it."""
    bundle = good_bundle(tmp_path)

    def damage(payload):
        payload["cutoff"] = "2027-01-01"
    rewrite(bundle, "input_manifest.json", damage)
    code, lines = extraction_checks.run(bundle)
    assert code != 0
    failures = gate_lines(lines, "cutoff")
    identity = [line for line in failures
                if "the triggering report's own filing date" in line]
    assert len(identity) == 1
    assert "the cutoff is 2027-01-01" in identity[0]
    assert "was filed 2026-07-31" in identity[0]
    # The submissions index says which cutoff it was read through, so moving the
    # cutoff after the fact contradicts it too. Both lines are true; neither is
    # the gate shading into another one.
    assert len(failures) == 2
    assert "read through the cutoff 2027-01-01" in "\n".join(failures)


def test_a_manifest_with_no_filing_date_for_its_trigger_fails_the_cutoff_gate(tmp_path):
    """Fail-closed the same way as a document with no date: a cutoff that
    cannot be shown to be the report's own date is a violation, not a pass."""
    bundle = good_bundle(tmp_path)
    rewrite(bundle, "input_manifest.json", lambda payload: payload.pop("filing_date"))
    code, lines = extraction_checks.run(bundle)
    assert code != 0
    assert "records no filing date for the report that triggered it" in \
        "\n".join(gate_lines(lines, "cutoff"))


def test_a_manifest_with_no_documents_fails_the_cutoff_gate(tmp_path):
    bundle = good_bundle(tmp_path)

    def damage(payload):
        payload["documents"] = []
    rewrite(bundle, "input_manifest.json", damage)
    code, lines = extraction_checks.run(bundle)
    assert code != 0
    assert "lists no documents" in "\n".join(gate_lines(lines, "cutoff"))


# --- the gates do not shade into each other ----------------------------------

def test_one_kind_of_damage_fails_one_gate(tmp_path):
    """A damaged bundle should say what is wrong with it, not everything."""
    bundle = good_bundle(tmp_path)
    (bundle / "input_notes.md").write_text("# AAPL notes\n\nnothing\n", encoding="utf-8")
    code, lines = extraction_checks.run(bundle)
    assert code != 0
    assert all(": pass — " in line for line in lines if not line.startswith("notes:"))


def test_a_recorded_count_of_zero_has_to_be_zero(tmp_path):
    """Apple's 10-K bundle has no note change history and expected.json records
    none. ±20% of nothing is nothing, so a count that appears is a failure."""
    bundle = good_bundle(tmp_path, "AAPL", "10-K")

    def damage(payload):
        payload["counts"]["note_history"] = 5
    rewrite(bundle, "input_manifest.json", damage)
    code, lines = extraction_checks.run(bundle)
    assert code != 0
    assert "expected.json records none" in "\n".join(gate_lines(lines, "paragraph counts"))


def test_a_company_with_no_recorded_counts_fails_rather_than_passes(tmp_path):
    bundle = good_bundle(tmp_path)
    rewrite(bundle, "input_manifest.json",
            lambda payload: payload.update({"ticker": "NOPE"}))
    code, lines = extraction_checks.run(bundle)
    assert code != 0
    assert "no recorded values for NOPE" in "\n".join(gate_lines(lines, "paragraph counts"))


def test_the_tolerance_is_twenty_percent():
    assert extraction_checks.TOLERANCE == 0.20
