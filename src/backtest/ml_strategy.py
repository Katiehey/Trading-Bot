#✅ 2. Implement a backtesting function that uses the trained model to generate trading signals and evaluate performance.
import pandas as pd

def ml_strategy(df: pd.DataFrame, model) -> pd.DataFrame:
    df = df.copy()

    features = [
        "EMA_12",
        "EMA_26",
        "SMA_50",
        "SMA_200",
        "MACD_12_26_9",
        "MACDh_12_26_9",
        "MACDs_12_26_9",
        "RSI_14",
        "ATRr_14",
        "BBL_20_2.0_2.0",
        "BBM_20_2.0_2.0",
        "BBU_20_2.0_2.0",
        "BBB_20_2.0_2.0",
        "BBP_20_2.0_2.0",
        "EMA_20",
        "OBV",
        "hour",
        "day_of_week",
        "is_weekend"
    ]

    df["signal"] = model.predict(df[features])
    df["position"] = df["signal"].shift(1)

    df["strategy_return"] = df["position"] * df["return"]
    return df
