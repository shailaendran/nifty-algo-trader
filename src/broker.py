"""Broker interface with a paper implementation. Live trading is deliberately not wired in."""
from dataclasses import dataclass, field
from typing import Protocol


class Broker(Protocol):
    def buy(self, symbol: str, qty: int, price: float) -> None: ...
    def sell(self, symbol: str, qty: int, price: float) -> float: ...


@dataclass
class PaperBroker:
    positions: dict = field(default_factory=dict)
    log: list = field(default_factory=list)

    def buy(self, symbol, qty, price):
        self.positions[symbol] = (qty, price)
        self.log.append(("BUY", symbol, qty, price))

    def sell(self, symbol, qty, price):
        _, entry = self.positions.pop(symbol)
        pnl = (price - entry) * qty
        self.log.append(("SELL", symbol, qty, price, pnl))
        return pnl
