import os
import csv
from datetime import datetime
import numpy as np
from src.execution.transaction_costs import TransactionCostModel

class PaperExchange:
    def __init__(self, starting_balance=500, log_path="logs/trades.csv", cost_model=None):
        self.balance = starting_balance
        self.position = 0
        self.trade_log = []
        self.log_path = log_path
        self.cost_model = TransactionCostModel()

        # Only write header if file doesn't exist yet
        if not os.path.exists(self.log_path):
            with open(self.log_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "side", "price", "size", "balance"])

    def _log_trade(self, side, price, size):
        with open(self.log_path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.utcnow().isoformat(),
                side,
                price,
                size,
                self.balance
            ])

    def buy(self, price, size):
        vol = np.random.uniform(0.005, 0.02)
        price, fee = self.cost_model.apply(price, size, "buy", vol)

        cost = price * size + fee
        if self.balance >= cost:
            self.balance -= cost
            self.position += size
            self._log_trade("BUY", price, size)

    def sell(self, price, size):
        vol = np.random.uniform(0.005, 0.02)
        price, fee = self.cost_model.apply(price, size, "sell", vol)

        proceeds = price * size - fee
        if self.position >= size:
            self.position -= size
            self.balance += proceeds
            self._log_trade("SELL", price, size)

    def equity(self, market_price):
        return self.balance + self.position * market_price
