#Data ingestion code (Python script)
import ccxt
import pandas as pd
import time
from datetime import datetime, timedelta
import os

# -----------------------------
# Config
# -----------------------------
EXCHANGE_ID = "binance"
SYMBOL = "BTC/USDT"
TIMEFRAME = "1h"
YEARS = 6
OUTPUT_PATH = "Trading-Bot/data/raw/btc_1h.csv"

os.makedirs("Trading-Bot/data/raw", exist_ok=True)

# -----------------------------
# Setup Exchange
# -----------------------------
exchange = getattr(ccxt, EXCHANGE_ID)({
    "enableRateLimit": True
})

# -----------------------------
# Time range
# -----------------------------
end_time = datetime.utcnow()
start_time = end_time - timedelta(days=365 * YEARS)

since = int(start_time.timestamp() * 1000)
now = int(end_time.timestamp() * 1000)

all_candles = []
limit = 1000

print(f"Fetching {SYMBOL} {TIMEFRAME} from {start_time} → {end_time}")

# -----------------------------
# Fetch loop
# -----------------------------
while since < now:
    ohlcv = exchange.fetch_ohlcv(
        SYMBOL,
        timeframe=TIMEFRAME,
        since=since,
        limit=limit
    )

    if not ohlcv:
        break

    all_candles.extend(ohlcv)
    since = ohlcv[-1][0] + 1

    last_dt = datetime.utcfromtimestamp(ohlcv[-1][0] / 1000)
    print("Fetched up to:", last_dt)

    time.sleep(0.3)

# -----------------------------
# DataFrame
# -----------------------------
df = pd.DataFrame(
    all_candles,
    columns=["timestamp", "open", "high", "low", "close", "volume"]
)

df["datetime"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
df.set_index("datetime", inplace=True)
df = df.drop(columns=["timestamp"])
df = df[~df.index.duplicated(keep="last")]
df = df.sort_index()

df.to_csv(OUTPUT_PATH)
print(f"Saved {len(df)} rows to {OUTPUT_PATH}")