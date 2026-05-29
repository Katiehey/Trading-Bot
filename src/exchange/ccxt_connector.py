#make exchange calls retry and never crash the system.
import ccxt
import time
import os

class ExchangeConnector:
    """CCXT wrapper that handles credentials, sandbox mode, and automatic retries."""

    def __init__(self, exchange_name="binance", testnet=True):
        """Initialise the exchange connection. Reads API keys from environment variables."""
        exchange_class = getattr(ccxt, exchange_name)

        LIVE_API_KEY = os.environ.get("LIVE_API_KEY")
        LIVE_SECRET = os.environ.get("LIVE_SECRET")
        TEST_API_KEY = os.environ.get("TEST_API_KEY")
        TEST_SECRET = os.environ.get("TEST_SECRET")

        config = {
            "enableRateLimit": True,
            "apiKey": TEST_API_KEY if testnet else LIVE_API_KEY,
            "secret": TEST_SECRET if testnet else LIVE_SECRET,
        }

        self.exchange = exchange_class(config)

        if testnet and exchange_name == "binance":
            self.exchange.set_sandbox_mode(True)
        elif not testnet and exchange_name == "binance":
            self.exchange.set_sandbox_mode(False) 

    def safe_call(self, func, *args, retries=5, delay=2, **kwargs):
        """Call a CCXT function with exponential-free retry; returns None after all retries fail."""
        for attempt in range(retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"[ERROR] Exchange call failed: {e}")
                time.sleep(delay)
        return None

    def get_ohlcv(self, symbol, timeframe, limit=200):
        return self.safe_call(self.exchange.fetch_ohlcv, symbol, timeframe, limit=limit)

    def get_ticker(self, symbol):
        return self.safe_call(self.exchange.fetch_ticker, symbol)
