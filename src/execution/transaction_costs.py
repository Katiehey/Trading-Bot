import numpy as np

class TransactionCostModel:
    def __init__(
        self,
        maker_fee=0.0002,
        taker_fee=0.0006,
        base_slippage=0.0003,
        vol_slippage_mult=2.0,
        spread=0.0004,
    ):
        self.maker_fee = maker_fee
        self.taker_fee = taker_fee
        self.base_slippage = base_slippage
        self.vol_slippage_mult = vol_slippage_mult
        self.spread = spread

    def apply(self, price, size, side, volatility):
        # Spread adjustment
        effective_price = price * (
            1 + self.spread / 2 if side == "buy"
            else 1 - self.spread / 2
        )

        # Slippage increases with volatility
        slippage = self.base_slippage * (1 + volatility * self.vol_slippage_mult)

        if side == "buy":
            effective_price *= 1 + slippage
        else:
            effective_price *= 1 - slippage

        # Assume taker orders for safety
        fee = effective_price * size * self.taker_fee

        return effective_price, fee
