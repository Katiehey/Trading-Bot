import pandas as pd

def apply_transaction_costs(
    df: pd.DataFrame,
    fee_rate: float = 0.00075,  # 0.075% typical crypto taker fee
    slippage: float = 0.0005    # 0.05% slippage
) -> pd.DataFrame:
    df = df.copy()

    # Detect trades (position changes)
    df["trade"] = df["position"].diff().abs().fillna(0)

    # Cost paid only on trades
    df["cost"] = df["trade"] * (fee_rate + slippage)

    # Apply costs to returns
    df["net_return"] = df["strategy_return"] - df["cost"]

    return df
