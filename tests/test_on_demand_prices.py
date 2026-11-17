"""An on-demand run fetches its price folder the way the nightly routine does.

The source is a stand-in that is handed in, never the network, and the token is
a made-up string; nothing here reads the real one. The planted EDGAR is the one
`tests/test_on_demand.py` serves: NVIDIA's 10-Q 0001045810-26-000075, filed
2026-08-26, whose SIC code `universe.json` records as 3674.

Expected values, worked by hand:

* the window is the 400 days before the filing date, through it: 2026-08-26
  less 365 days is 2025-08-26 (no leap day lies between), and 35 days more is
  2025-07-22 (26 days to July 31, 9 more);
* SIC 3674 is in division D, Manufacturing, 2000 to 3999, whose sector fund is
  XLI in `src/sic_to_sector_etf_map_v0.1.json`, and the broad market's series
  is SPY, so the symbols are NVDA, SPY, XLI.
"""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

import pytest

from src import agent_inputs, nightly, on_demand
from tests.test_agent_inputs import spec_bundle_names
from tests.test_on_demand import ACCESSION, TICKER, client, server  # noqa: F401

WINDOW = (dt.date(2025, 7, 22), dt.date(2026, 8, 26))
SYMBOLS = ["NVDA", "SPY", "XLI"]
STAND_IN_TOKEN = "stand-in-token"
NO_TOKEN_REASON = "no price series: TIINGO_TOKEN unset"
FETCH_RECORD = {"backend": "tiingo", "fetched_at": "2026-08-27T07:05:00+00:00",
                "asked_for": {"start": "2025-07-22", "end": "2026-08-26"},
                "served": {symbol: {"rows": 270, "first_day": "2025-07-22",
                                    "last_day": "2026-08-26"} for symbol in SYMBOLS}}


class World:
    """The planted run: a stand-in bundle, a stand-in source, a recorded analysis."""

    def __init__(self, tmp_path, server, monkeypatch):
        fetcher = client(tmp_path, server)
        monkeypatch.setattr(on_demand.edgar_client, "EdgarClient", lambda: fetcher)
        self.out = tmp_path / "runs" / TICKER / ACCESSION
        self.asked = []
        self.analysed = []

        def bundle(argv):
            run = Path(argv[argv.index("--out") + 1])
            for name in spec_bundle_names() + ("input_controls.md",):
                (run / name).write_text(f"this is {name}\n", encoding="utf-8")
            (run / "input_manifest.json").write_text(
                json.dumps({"accession": ACCESSION, "ticker": TICKER, "dropped_items": []}),
                encoding="utf-8")
            return 0

        def analysis(argv):
            self.analysed.append(argv)
            return 0

        from src import run_analysis
        monkeypatch.setattr(on_demand.assemble_bundle, "main", bundle)
        monkeypatch.setattr(run_analysis, "main", analysis)

    def fetch(self, **kwargs):
        self.asked.append(kwargs)
        folder = kwargs["into"]
        folder.mkdir(parents=True, exist_ok=True)
        for symbol in kwargs["symbols"]:
            (folder / f"{symbol}.csv").write_text("date,close\n2026-08-26,1.0\n")
        return dict(FETCH_RECORD)

    def main(self, *flags, environ, fetch_prices):
        return on_demand.main(["--ticker", TICKER, "--accession", ACCESSION,
                               "--out", str(self.out), *flags],
                              environ=environ, fetch_prices=fetch_prices)

    def run(self, environ=None):
        return self.main("--run", environ={"TIINGO_TOKEN": STAND_IN_TOKEN}
                         if environ is None else environ, fetch_prices=self.fetch)


@pytest.fixture
def world(tmp_path, server, monkeypatch):  # noqa: F811
    return World(tmp_path, server, monkeypatch)


def test_the_run_fetches_the_window_for_the_three_symbols_and_hands_the_folder_on(world):
    environ = {"TIINGO_TOKEN": STAND_IN_TOKEN}
    assert world.run(environ) == 0
    assert world.asked == [{"symbols": SYMBOLS, "start": WINDOW[0], "end": WINDOW[1],
                            "into": world.out / "prices", "environ": environ,
                            "backend": "tiingo"}]
    assert world.asked[0]["environ"] is environ
    assert len(world.analysed) == 1
    argv = world.analysed[0]
    assert argv[argv.index("--prices") + 1] == str(world.out / "prices")
    assert json.loads((world.out / "price_fetch.json").read_text()) == FETCH_RECORD
    assert sorted(p.name for p in (world.out / "prices").iterdir()) == [
        "NVDA.csv", "SPY.csv", "XLI.csv"]


def test_the_token_is_never_written_or_printed(world, capsys):
    assert world.run() == 0
    seen = capsys.readouterr()
    assert STAND_IN_TOKEN not in seen.out + seen.err
    for path in world.out.rglob("*"):
        if path.is_file():
            assert STAND_IN_TOKEN not in path.read_text(), path


def test_no_token_means_the_run_goes_on_without_prices_and_says_why(world, capsys):
    def never(**_):
        pytest.fail("the source was asked with no token")

    assert world.main("--run", environ={}, fetch_prices=never) == 0
    assert "--prices" not in world.analysed[0]
    assert NO_TOKEN_REASON == nightly.NO_PRICES_UNSET
    assert NO_TOKEN_REASON in capsys.readouterr().err
    assert json.loads((world.out / "price_fetch.json").read_text()) == {
        "fetched": False, "reason": NO_TOKEN_REASON}
    assert not (world.out / "prices").exists()


def test_a_source_that_fails_leaves_the_run_without_prices_and_without_the_token(
        world, capsys):
    def fails(**_):
        raise RuntimeError(f"the source refused {STAND_IN_TOKEN}")

    assert world.main("--run", environ={"TIINGO_TOKEN": STAND_IN_TOKEN},
                      fetch_prices=fails) == 0
    assert "--prices" not in world.analysed[0]
    seen = capsys.readouterr()
    assert "RuntimeError: the source refused <TIINGO_TOKEN>" in seen.err
    assert STAND_IN_TOKEN not in seen.out + seen.err + (world.out / "price_fetch.json").read_text()


def test_no_prices_skips_the_fetch_and_passes_nothing(world):
    def never(**_):
        pytest.fail("the fetch ran under --no-prices")

    assert world.main("--run", "--no-prices", environ={"TIINGO_TOKEN": STAND_IN_TOKEN},
                      fetch_prices=never) == 0
    assert "--prices" not in world.analysed[0]
    assert not (world.out / "prices").exists() and not (world.out / "price_fetch.json").exists()


def test_the_price_folder_is_fetched_without_run_too(world):
    assert world.main(environ={"TIINGO_TOKEN": STAND_IN_TOKEN}, fetch_prices=world.fetch) == 0
    assert (world.out / "prices" / "NVDA.csv").is_file()
    assert world.analysed == []


def test_the_sic_is_the_universes_else_the_submissions_indexs_else_none(tmp_path, server):
    held = client(tmp_path, server)
    assert on_demand.sic_of(held, "NVDA", "0001045810") == "3674"      # universe.json's row
    # outside the universe the index answers; the planted one names no SIC
    assert on_demand.sic_of(held, "ZZZZ", "0001045810") is None

    class Named:
        def get_json(self, url):
            return {"sic": "3661"}

    assert on_demand.sic_of(Named(), "ZZZZ", "0001045810") == "3661"
    assert nightly.price_series("ZZZZ", None)["symbols"] is None


AGENTS_WITHOUT_PRICES = ("numbers-reader", "notes-text-reader", "accounting-analyst",
                         "financial-analyst")


def test_no_reader_and_no_accounting_or_financial_analyst_receives_a_price_file(world):
    assert world.run() == 0
    assert (world.out / "prices").is_dir() and (world.out / "price_fetch.json").is_file()
    for agent in AGENTS_WITHOUT_PRICES:
        agent_inputs.build(world.out, agent)
        root = agent_inputs.session_root(world.out, agent)
        held = [str(p.relative_to(root)) for p in root.rglob("*")]
        assert held, agent
        assert [name for name in held
                if "price" in name.lower() or name.endswith(".csv")] == [], agent
        for path in root.rglob("*"):
            if path.is_file():
                assert "2026-08-26,1.0" not in path.read_text(), path
