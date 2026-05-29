import numpy as np
import pandas as pd

class RiskManager:
    def __init__(
        self,
        max_daily_loss_pct=0.03,
        max_drawdown_pct=0.20,
        risk_per_trade_pct=0.01,
        cooldown_after_losses=3,
    ):
        self.max_daily_loss_pct = max_daily_loss_pct
        self.max_drawdown_pct = max_drawdown_pct
        self.risk_per_trade_pct = risk_per_trade_pct
        self.cooldown_after_losses = cooldown_after_losses

        self.daily_start_equity = None
        self.peak_equity = None
        self.loss_streak = 0

    def update_equity(self, equity):
        if self.daily_start_equity is None:
            self.daily_start_equity = equity
        if self.peak_equity is None:
            self.peak_equity = equity

        # update peak equity
        self.peak_equity = max(self.peak_equity, equity)

    def daily_loss_exceeded(self, equity):
        max_loss = self.daily_start_equity * (1 - self.max_daily_loss_pct)
        return equity < max_loss

    def drawdown_exceeded(self, equity):
        dd = (equity - self.peak_equity) / self.peak_equity
        return dd < -self.max_drawdown_pct

    def volatility_position_size(self, price_series, equity):
        # ATR-like volatility (simple version)
        vol = price_series.pct_change().rolling(20).std().iloc[-1]

        if vol == 0 or np.isnan(vol):
            return 0

        risk_dollar = equity * self.risk_per_trade_pct
        position_size = risk_dollar / (vol * price_series.iloc[-1])
        return position_size

    def register_trade_result(self, pnl):
        if pnl < 0:
            self.loss_streak += 1
        else:
            self.loss_streak = 0

    def cooldown_needed(self):
        return self.loss_streak >= self.cooldown_after_losses

    def risk_check(self, price_series, equity):
        # Update internal state
        self.update_equity(equity)

        if self.daily_loss_exceeded(equity):
            return False, "Daily loss limit hit"

        if self.drawdown_exceeded(equity):
            return False, "Max drawdown exceeded"

        if self.cooldown_needed():
            return False, "Cooldown active after losing streak"

        # position size suggestion
        size = self.volatility_position_size(price_series, equity)
        return True, size
