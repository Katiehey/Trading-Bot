#Create Moving Average Crossover Strategy
#import pandas as pd

#def ma_crossover_strategy(df: pd.DataFrame) -> pd.DataFrame:
    #df = df.copy()

    #df["signal"] = 0
    #df.loc[df["ema_12"] > df["ema_26"], "signal"] = 1
    #df.loc[df["ema_12"] < df["ema_26"], "signal"] = -1

    #df["position"] = df["signal"].shift(1).fillna(0)

    #df["strategy_return"] = df["position"] * df["return"]

    #return df

import numpy as np
import pandas as pd
from src.bot.risk import volatility_target_position

def ma_crossover_strategy(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    
    # 1. Calculate EMAs (Assuming 'close' column exists)
    df['ema_12'] = df['close'].ewm(span=12, adjust=False).mean()
    df['ema_26'] = df['close'].ewm(span=26, adjust=False).mean()
    
    # 2. Calculate the difference and the change in the difference
    df['diff'] = df['ema_12'] - df['ema_26']
    
    # 3. Identify Crossovers (A crossover is when the sign of 'diff' changes)
    # The sign of diff_prev * diff_current is negative when a cross occurs.
    df['crossover'] = (df['diff'].shift(1) < 0) & (df['diff'] >= 0)  # Buy Cross (Fast above Slow)
    df['crossunder'] = (df['diff'].shift(1) > 0) & (df['diff'] <= 0) # Sell Cross (Fast below Slow)
    
    # 4. Generate Signal: Only 1, -1, or 0 on the *day of the cross*
    df['signal'] = 0
    df.loc[df['crossover'], 'signal'] = 1  # Buy signal
    df.loc[df['crossunder'], 'signal'] = -1 # Sell/Short signal
    
    size = volatility_target_position(df)#after creating the function in risk.py, we can call it here to get position sizing based on volatility.

    # 5. Determine Position: Position holds the last non-zero signal
    # This carries the signal forward until the next crossover event.
    df['position'] = df['signal'].replace(to_replace=0, method='ffill').shift(1).fillna(0) * size
    
    # 6. Calculate Returns (Assuming 'return' column exists)
    df["strategy_return"] = df["position"] * df["return"]

    return df