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
#from src.bot.risk import volatility_target_position

# The volatility_target_position is no longer used here, 
# as risk management is handled externally by RiskManager.

def ma_crossover_strategy(df: pd.DataFrame, fast: int = 12, slow: int = 26) -> pd.DataFrame:
    """Generate EMA crossover signals and compute strategy returns for a given OHLCV DataFrame."""
    df = df.copy()
    
    # 1. Calculate EMAs
    df[f'ema_{fast}'] = df['close'].ewm(span=fast, adjust=False).mean()
    df[f'ema_{slow}'] = df['close'].ewm(span=slow, adjust=False).mean()
    
    # 2. Calculate the difference
    df['diff'] = df[f'ema_{fast}'] - df[f'ema_{slow}']
    
    # 3. Identify Crossovers
    df['crossover'] = (df['diff'].shift(1) < 0) & (df['diff'] >= 0)  # Buy Cross (Fast above Slow)
    df['crossunder'] = (df['diff'].shift(1) > 0) & (df['diff'] <= 0) # Sell Cross (Fast below Slow)
    
    # 4. Generate Signal: Only 1, -1, or 0 on the *day of the cross*
    df['signal'] = 0
    df.loc[df['crossover'], 'signal'] = 1  # Buy signal
    df.loc[df['crossunder'], 'signal'] = -1 # Sell/Short signal
    
    # 5. Determine Position: Position holds the last non-zero signal (The Unit Position)
    # FIX: Removed .shift(1) to allow the bot to act on the current candle's signal.
    df['position'] = df['signal'].replace(0, np.nan).ffill().fillna(0) 

    # 6. Calculate Returns (The returns are unscaled by size here)
    df["strategy_return"] = df["position"] * df["return"]

    # We do NOT return the 'size' column here; it's calculated in RiskManager

    return df