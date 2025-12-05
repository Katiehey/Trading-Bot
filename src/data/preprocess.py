#Clean & Prepare Market Data
import pandas as pd
from src.features.technical import add_technical_features

def load_raw_data(path: str) -> pd.DataFrame:
    df = pd.read_parquet(path)
    df = df.sort_values("datetime")
    df = df.drop_duplicates(subset=["datetime"])
    return df


def clean_ohlcv(df: pd.DataFrame) -> pd.DataFrame:
    # Ensure datetime
    df["datetime"] = pd.to_datetime(df["datetime"])

    # Remove rows with bad prices
    df = df[(df["open"] > 0) & (df["high"] > 0)]
    
    # Forward-fill volumes if missing
    df["volume"] = df["volume"].fillna(0)

    return df


def add_returns(df: pd.DataFrame) -> pd.DataFrame:
    df["return"] = df["close"].pct_change()
    df["log_return"] = (df["close"]
                         .apply(lambda x: 0 if x <= 0 else x)
                         .apply(lambda x: x)
                        )
    return df


def prepare_dataset(raw_path: str, output_path: str):
    df = load_raw_data(raw_path)
    df = clean_ohlcv(df)
    df = add_returns(df)
    df = df.dropna()

    df = add_technical_features(df)
    df = df.dropna()


    df.to_parquet(output_path, index=False)
    print(f"Saved clean dataset → {output_path}")
