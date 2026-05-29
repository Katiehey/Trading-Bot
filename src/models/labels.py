#import pandas as pd

#def add_future_return_label(
    #df: pd.DataFrame,
    #horizon: int = 1,
    #threshold: float = 0.0
#) -> #pd.DataFrame:
    #df = df.copy()

    #df["future_return"] = (
        #df["close"].shift(-horizon) / df["close"] - 1
    #)

    #df["target"] = 0
    #df.loc[df["future_return"] > threshold, "target"] = 1
    #df.loc[df["future_return"] < -threshold, "target"] = -1

    #return df.dropna()

import pandas as pd
import numpy as np
from typing import Literal

def add_future_return_label(
    df: pd.DataFrame,
    horizon: int = 1,
    threshold_percent: float = 0.1, # Default to 0.1% threshold (0.001)
    return_type: Literal["simple", "log"] = "simple"
) -> pd.DataFrame:
    """
    Calculates future returns and generates a ternary (1, 0, -1) classification target
    for financial time-series data, suitable for machine learning training.

    Args:
        df: Input DataFrame which MUST contain a 'close' column.
        horizon: The number of periods/rows to look ahead.
        threshold_percent: The return threshold (in percent) for a move to be
                           considered significant (e.g., 0.1 for 0.1% needed to trade).
        return_type: The method used to calculate returns: 'simple' or 'log'.

    Returns:
        A new DataFrame with 'future_return' and 'target' columns added.
        Note: The last 'horizon' rows will have NaN in the new columns.
    """
    # 1. Input Validation
    if "close" not in df.columns:
        raise ValueError("Input DataFrame must contain a 'close' column.")
    
    df = df.copy(deep=True)
    threshold = threshold_percent / 100.0 # Convert percentage to a decimal

    # 2. Calculate Future Returns
    # Using pct_change(-horizon) is slightly cleaner syntax for future returns
    if return_type == "log":
        # Calculate log returns: log(Future_Close / Current_Close)
        future_close = df["close"].shift(-horizon)
        df["future_return"] = np.log(future_close / df["close"])
    else: # Default to simple returns
        # Calculate simple returns: (Future_Close / Current_Close) - 1
        df["future_return"] = df["close"].pct_change(-horizon)

    # 3. Create 'target' labels based on cost-adjusted threshold
    df["target"] = 0
    
    # Use np.select for slightly more efficient multi-condition assignment than multiple .loc calls
    conditions = [
        (df["future_return"] > threshold),
        (df["future_return"] < -threshold)
    ]
    choices = [1, -1]
    
    df["target"] = np.select(conditions, choices, default=0)
    # 4. Do not drop NaNs here; let the calling ML pipeline handle them
    # for training/live prediction pipeline alignment.
    return df.dropna()