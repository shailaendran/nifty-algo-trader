# nifty-algo-trader

Rule-based intraday signal engine for Nifty 50 with a risk manager, paper broker and a bar-by-bar backtester.

**Paper trading only.** No live order code is included. Broker credentials belong in environment variables (`keys.sh` is git-ignored), never in source.

## Strategy
Signals need agreement from five inputs: EMA 9 over EMA 21, MACD histogram sign, price against session VWAP, and volume above its 20-bar average. Anything less returns `FLAT`.

## Risk rules
Daily target Rs 4,000, max daily loss Rs 1,500, up to 2 trades a day, 2 lots. The risk manager blocks new entries once any limit is hit.

## Layout
```
src/signals.py   indicators and LONG/SHORT/FLAT
src/risk.py      daily limits and sizing
src/broker.py    Broker protocol + PaperBroker
src/backtest.py  simple backtester
tests/           pytest suite
```

## Run
```bash
pip install -r requirements.txt
pytest -q
```

## Roadmap
- Groww API adapter behind the `Broker` protocol, dry-run first
- Options strike selection for the current expiry
- Streamlit dashboard: positions, daily P&L, margin, capital goal ladder
- Scheduled start at 9:16 on market days

Backtest results are not a promise of live results. Trading derivatives carries real risk of loss.
