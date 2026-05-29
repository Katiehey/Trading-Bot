import pandas as pd
import numpy as np

def compute_drawdown(equity: pd.Series) -> pd.Series:
    """Return the rolling drawdown series (negative fraction from peak) for an equity curve."""
    peak = equity.cummax()
    drawdown = (equity - peak) / peak
    return drawdown


def performance_summary(df: pd.DataFrame, periods_per_year: int = 24 * 252):
    """Compute total return, annualised Sharpe, win rate, max drawdown, and trade count."""
    returns = df["strategy_return"].dropna()

    equity = (1 + returns).cumprod()
    drawdown = compute_drawdown(equity)

    total_return = equity.iloc[-1] - 1
    sharpe = np.sqrt(periods_per_year) * returns.mean() / returns.std()

    win_rate = (returns > 0).mean()
    max_drawdown = drawdown.min()

    return {
        "total_return": total_return,
        "sharpe": sharpe,
        "win_rate": win_rate,
        "max_drawdown": max_drawdown,
        "num_trades": (df["position"].diff().abs() > 0).sum()
    }
