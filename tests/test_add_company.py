"""`src/add_company.py`: the mechanical part of adding a company, and the one
part it refuses to do. Expected values are read off the fixtures the twelve
already carry (AAPL's key set, OMCL's baseline) and off the command's own
stated rules; nothing here touches the network.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src import add_company

REPO = Path(__file__).resolve().parent.parent


def test_the_baseline_holds_the_six_counts_and_the_note_the_twelve_carry():
    counts = {"10-Q": {"controls": 9, "eight_k": 100, "mdna": 158, "note_history": 68,
                       "notes": 171, "paragraphs": 506, "exclusions": 3},
              "10-K": {"controls": 51, "eight_k": 0, "mdna": 120, "note_history": 0,
                       "notes": 322, "paragraphs": 493, "exclusions": 1}}
    out = add_company.baseline(counts)
    omcl = json.loads((REPO / "tests/fixtures/OMCL/expected.json").read_text())
    assert out["_what_this_is"] == omcl["_what_this_is"]
    assert out["bundle"] == omcl["bundle"]              # OMCL's counts, typed above, round-trip
    assert "exclusions" not in out["bundle"]["10-K"] and list(out["bundle"]) == ["10-K", "10-Q"]


def test_the_checklist_names_every_key_the_twelve_carry_and_no_value():
    keys = add_company.reference_keys()
    assert len(keys) == 43
    todo = add_company.checklist(keys)
    assert list(todo) == keys
    assert all(entry["value"] is None and entry["from"] == "" for entry in todo.values())
    assert todo["auditors_report.10-K.audit_firm"]["read_as"] == "read by eye"
    assert todo["numbers.10-K.fact_count"]["with"] == "tests/test_extract_numbers.py::_count_by_hand"
    # every reader the checklist names is a file in this repository, so the note
    # it suggests passes tests/expected_values.py's citation rule
    for entry in todo.values():
        for word in entry["with"].split():
            if word.startswith("tests/"):
                assert (REPO / word.split("::")[0].rstrip(",")).is_file(), word


def test_every_source_kind_in_the_table_is_one_the_reader_accepts():
    from tests import expected_values
    kinds = {kind for kind, _ in add_company.HOW_TO_READ.values()}
    assert kinds <= set(expected_values.SOURCE_KINDS)


def test_the_row_is_appended_once_and_a_known_ticker_or_cik_is_refused():
    document = {"companies": [{"ticker": "AAPL", "cik": "0000320193", "sic": "3571",
                               "added_on": "2026-09-22"}]}
    out = add_company.row_appended(document, "mu", "0000723125", "3674", "2026-10-21")
    assert out["companies"][-1] == {"ticker": "MU", "cik": "0000723125", "sic": "3674",
                                    "added_on": "2026-10-21"}
    assert document["companies"] == document["companies"][:1]        # the input untouched
    with pytest.raises(add_company.AddError, match="already in the universe"):
        add_company.row_appended(document, "aapl", "0000000001", "3674", "2026-10-21")
    with pytest.raises(add_company.AddError, match="CIK 0000320193"):
        add_company.row_appended(document, "ZZZZ", "0000320193", "3674", "2026-10-21")


class _Fetcher:
    def __init__(self, answers: dict):
        self.answers, self.asked = answers, []

    def get(self, url: str) -> bytes:
        self.asked.append(url)
        return self.answers[url]


def test_the_cik_comes_from_the_tickers_file_and_the_sic_from_the_index():
    fetcher = _Fetcher({
        add_company.TICKERS_URL: json.dumps({"0": {"cik_str": 723125, "ticker": "MU"}}).encode(),
        add_company.SUBMISSIONS_URL.format(cik="0000723125"): json.dumps({"sic": "3674"}).encode()})
    assert add_company.cik_for(fetcher, "mu") == "0000723125"
    assert add_company.sic_for(fetcher, "0000723125") == "3674"
    with pytest.raises(add_company.AddError, match="--cik"):
        add_company.cik_for(fetcher, "NOPE")


def test_add_refuses_a_known_ticker_before_any_fetch(tmp_path, monkeypatch):
    universe = tmp_path / "universe.json"
    universe.write_text(json.dumps({"companies": [{"ticker": "MU", "cik": "0000723125",
                                                   "sic": "3674", "added_on": "2026-10-21"}]}))
    fetcher = _Fetcher({})
    with pytest.raises(add_company.AddError, match="already in the universe"):
        add_company.add("MU", "2026-10-22", cik="0000723125", fetcher=fetcher,
                        universe_path=universe, fixtures_root=tmp_path)
    assert fetcher.asked == []


def test_add_runs_the_steps_in_order_and_never_writes_expected_values(tmp_path, monkeypatch):
    universe = tmp_path / "universe.json"
    universe.write_text(json.dumps({"companies": []}))
    fixtures = tmp_path / "fixtures"
    (fixtures / "AAPL").mkdir(parents=True)
    (fixtures / "AAPL" / "expected_values.json").write_text(json.dumps(
        {"numbers.10-K.fact_count": {"value": 1, "from": "x"}, "mdna.10-K.opens_at": {"value": "a", "from": "y"}}))
    order = []
    monkeypatch.setattr(add_company, "sic_for", lambda f, c: order.append("sic") or "3674")
    monkeypatch.setattr(add_company.fetch_fixtures, "fetch_company",
                        lambda f, t, c, a, out: (order.append("store") or ({}, [])))
    monkeypatch.setattr(add_company.fetch_companyfacts, "fetch_company",
                        lambda f, t, a, out: (order.append("facts") or []))
    monkeypatch.setattr(add_company, "record_headers", lambda f, d: order.append("headers") or [1, 2, 3, 4])
    monkeypatch.setattr(add_company, "bundle_counts", lambda t, r: order.append("bundles") or {
        "10-K": dict.fromkeys(add_company.BASELINE_KEYS, 1), "10-Q": dict.fromkeys(add_company.BASELINE_KEYS, 2)})
    (fixtures / "MU").mkdir()
    record = add_company.add("MU", "2026-10-21", cik="0000723125", fetcher=_Fetcher({}),
                             universe_path=universe, fixtures_root=fixtures)
    assert order == ["sic", "store", "facts", "headers", "bundles"]
    assert record["headers_recorded"] == 4 and record["sic"] == "3674"
    assert json.loads(universe.read_text())["companies"][-1]["ticker"] == "MU"
    assert json.loads((fixtures / "MU" / "expected.json").read_text())["bundle"]["10-Q"]["notes"] == 2
    todo = json.loads((fixtures / "MU" / "expected_values.todo.json").read_text())
    assert list(todo) == ["numbers.10-K.fact_count", "mdna.10-K.opens_at"]
    assert not (fixtures / "MU" / "expected_values.json").exists()
    assert "never an expectation moved" in add_company.next_steps(record)


def test_a_store_problem_stops_before_the_row_is_written(tmp_path, monkeypatch):
    universe = tmp_path / "universe.json"
    universe.write_text(json.dumps({"companies": []}))
    monkeypatch.setattr(add_company, "sic_for", lambda f, c: "3674")
    monkeypatch.setattr(add_company.fetch_fixtures, "fetch_company",
                        lambda f, t, c, a, out: ({}, ["the index lists no 10-Q"]))
    with pytest.raises(add_company.AddError, match="no 10-Q"):
        add_company.add("MU", "2026-10-21", cik="0000723125", fetcher=_Fetcher({}),
                        universe_path=universe, fixtures_root=tmp_path)
    assert json.loads(universe.read_text())["companies"] == []
