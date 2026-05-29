#Create live data fetcher (safe polling); use ccxt without API keys.
import ccxt

exchange = ccxt.binance({
    'timeout': 20000,  # Set timeout to 20 seconds (20000 milliseconds)
})

def fetch_latest_candle(symbol="BTC/USDT", timeframe="1h"):
    candles = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=2)
    return candles[-1]  # most recent closed candle
