"""Indicator and signal logic for Nifty intraday strategies.

Input frames need columns: open, high, low, close, volume and a DatetimeIndex.
"""
from __future__ import annotations

import pandas as pd


def ema(series: pd.Series, span: int) -> pd.Series:
    return series.ewm(span=span, adjust=False).mean()


def macd(close: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
    line = ema(close, fast) - ema(close, slow)
    sig = ema(line, signal)
    return pd.DataFrame({"macd": line, "signal": sig, "hist": line - sig})


def vwap(df: pd.DataFrame) -> pd.Series:
    """Session VWAP, reset every calendar day."""
    typical = (df["high"] + df["low"] + df["close"]) / 3
    pv = typical * df["volume"]
    day = df.index.date
    return pv.groupby(day).cumsum() / df["volume"].groupby(day).cumsum()


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["ema9"] = ema(out["close"], 9)
    out["ema21"] = ema(out["close"], 21)
    m = macd(out["close"])
    out["macd_hist"] = m["hist"]
    out["vwap"] = vwap(out)
    out["vol_avg"] = out["volume"].rolling(20, min_periods=5).mean()
    return out


def latest_signal(df: pd.DataFrame) -> str:
    """Return LONG, SHORT or FLAT for the last candle.

    LONG needs every filter to agree: fast EMA above slow, MACD histogram
    positive, price above VWAP and volume above its 20 bar average.
    SHORT is the mirror image.
    """
    if len(df) < 30:
        return "FLAT"
    row = add_indicators(df).iloc[-1]
    vol_ok = row["volume"] > row["vol_avg"]
    if row["ema9"] > row["ema21"] and row["macd_hist"] > 0 and row["close"] > row["vwap"] and vol_ok:
        return "LONG"
    if row["ema9"] < row["ema21"] and row["macd_hist"] < 0 and row["close"] < row["vwap"] and vol_ok:
        return "SHORT"
    return "FLAT"
