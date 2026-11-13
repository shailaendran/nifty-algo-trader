import numpy as np
import pandas as pd

from src.backtest import run
from src.broker import PaperBroker
from src.risk import RiskConfig, RiskManager
from src.signals import add_indicators, ema, latest_signal


def frame(prices, vol=1000):
    idx = pd.date_range("2026-01-05 09:15", periods=len(prices), freq="5min")
    p = np.array(prices, dtype=float)
    return pd.DataFrame({"open": p, "high": p + 1, "low": p - 1, "close": p,
                         "volume": np.linspace(vol, vol * 3, len(p))}, index=idx)


def test_ema_constant():
    assert ema(pd.Series([5.0] * 10), 3).iloc[-1] == 5.0


def test_uptrend_is_long():
    assert latest_signal(frame(np.linspace(100, 200, 80))) == "LONG"


def test_downtrend_is_short():
    assert latest_signal(frame(np.linspace(200, 100, 80))) == "SHORT"


def test_short_history_is_flat():
    assert latest_signal(frame([100] * 10)) == "FLAT"


def test_indicator_columns():
    assert {"ema9", "ema21", "vwap", "macd_hist"} <= set(add_indicators(frame(np.linspace(1, 50, 60))).columns)


def test_risk_stops_after_loss_cap():
    r = RiskManager(RiskConfig(max_daily_loss=1500))
    assert r.can_trade()
    r.record(-1600)
    assert not r.can_trade()


def test_risk_stops_after_target():
    r = RiskManager(RiskConfig(daily_target=4000))
    r.record(4100)
    assert not r.can_trade()


def test_paper_broker_pnl():
    b = PaperBroker()
    b.buy("NIFTY", 75, 100)
    assert b.sell("NIFTY", 75, 110) == 750


def test_backtest_runs():
    out = run(frame(np.linspace(100, 300, 200)))
    assert set(out) == {"trades", "pnl"}
