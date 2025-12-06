import pandas as pd
import numpy as np

def volatility_target_position(
    df: pd.DataFrame,
    target_vol: float = 0.02  # 2% per period
) -> pd.Series:
    vol = df["return"].rolling(20).std()

    position_size = target_vol / vol
    position_size = position_size.clip(0, 1)

    return position_size.fillna(0)


def apply_risk_management(
    df: pd.DataFrame,
    max_drawdown: float = -0.25
) -> pd.DataFrame:
    df = df.copy()

    equity = (1 + df["net_return"]).cumprod()
    drawdown = equity / equity.cummax() - 1

    df.loc[drawdown < max_drawdown, "position"] = 0
    df.loc[drawdown < max_drawdown, "net_return"] = 0

    return df
