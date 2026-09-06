"""R9-3: 가공 티커 스크린 — 역사적 상장 티커 거부 (CALA/L-10 선례 회귀 잠금)."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen_fict_names as gfn


def _ref(tmp_path, historical=None):
    ref = tmp_path / "reference"
    ref.mkdir()
    (ref / "company_tickers.json").write_text(json.dumps(
        {"0": {"ticker": "AAPL"}, "1": {"ticker": "MSFT"}}), encoding="utf-8")
    if historical is not None:
        (ref / "historical_tickers.txt").write_text(
            "\n".join(historical) + "\n", encoding="utf-8")
    return ref


def test_screen_unions_historical_tickers(tmp_path):
    tickers = gfn.load_ticker_screen(_ref(tmp_path, historical=["cala", "ENRNQ"]))
    # 심은 상폐 티커가 집합에 있어야 채택 조건(not tick_hit)이 차단한다
    assert {"CALA", "ENRNQ", "AAPL"} <= tickers


def test_missing_historical_reference_fails_closed(tmp_path):
    with pytest.raises(SystemExit, match="역사적 티커 참조 부재"):
        gfn.load_ticker_screen(_ref(tmp_path, historical=None))


def test_frozen_names_file_untouched_and_l10_disclosed():
    """R9-3의 조치는 미래 추첨 스크린 + 공개 — 동결 파일은 CALA 행 그대로
    (재생성 금지), 공개는 L-10."""
    repo = Path(__file__).resolve().parents[1]
    names = json.loads((repo / "data/evaluatee/fict_names_wave2.json")
                       .read_text(encoding="utf-8"))["names"]
    assert names["case_52"]["ticker"] == "CALA"  # 동결 그대로 — 공개로만 한정
    lim = (repo / "docs/methodology_limitations.md").read_text(encoding="utf-8")
    assert "## L-10." in lim and "CALA" in lim and "case_52" in lim
