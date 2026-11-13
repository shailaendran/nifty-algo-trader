"""Minimal bar-by-bar backtester for the LONG/SHORT/FLAT signal."""
import pandas as pd

from .broker import PaperBroker
from .risk import RiskManager
from .signals import add_indicators


def run(df: pd.DataFrame, stop_pct: float = 0.004, target_pct: float = 0.008) -> dict:
    d = add_indicators(df)
    broker, risk = PaperBroker(), RiskManager()
    side = entry = None
    for i in range(30, len(d)):
        r = d.iloc[i]
        vol_ok = r["volume"] > r["vol_avg"]
        if side is None and risk.can_trade() and vol_ok:
            if r.ema9 > r.ema21 and r.macd_hist > 0 and r.close > r.vwap:
                side, entry = 1, r.close
            elif r.ema9 < r.ema21 and r.macd_hist < 0 and r.close < r.vwap:
                side, entry = -1, r.close
        elif side is not None:
            move = side * (r.close - entry) / entry
            if move <= -stop_pct or move >= target_pct:
                pnl = side * (r.close - entry) * risk.quantity()
                risk.record(pnl)
                side = entry = None
    return {"trades": risk.trades, "pnl": round(risk.pnl, 2)}
