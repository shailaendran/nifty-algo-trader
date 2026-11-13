"""Risk manager: daily loss cap, daily target, trade count and lot sizing."""
from dataclasses import dataclass


@dataclass
class RiskConfig:
    daily_target: float = 4000.0
    max_daily_loss: float = 1500.0
    max_trades: int = 2
    lots: int = 2
    lot_size: int = 75


class RiskManager:
    def __init__(self, cfg: RiskConfig | None = None):
        self.cfg = cfg or RiskConfig()
        self.pnl = 0.0
        self.trades = 0

    def record(self, pnl: float) -> None:
        self.pnl += pnl
        self.trades += 1

    def can_trade(self) -> bool:
        c = self.cfg
        return self.pnl > -c.max_daily_loss and self.pnl < c.daily_target and self.trades < c.max_trades

    def quantity(self) -> int:
        return self.cfg.lots * self.cfg.lot_size
