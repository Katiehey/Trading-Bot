#Create walk-forward backtest module
import pandas as pd
from src.backtest.metrics import performance_summary
from src.backtest.ma_crossover import ma_crossover_strategy


def walk_forward_test(
    df: pd.DataFrame,
    train_size: float = 0.6,
    test_size: float = 0.2,
    fast: int = 12,  # Expects a single integer
    slow: int = 26   # Expects a single integer
):
    """Run a single walk-forward split and return out-of-sample performance metrics."""
    n = len(df)
    train_end = int(n * train_size)
    test_end = int(n * (train_size + test_size))

    train = df.iloc[:train_end]
    test = df.iloc[train_end:test_end]

    test = ma_crossover_strategy(test, fast=fast, slow=slow)

    stats = performance_summary(test)

    return stats
