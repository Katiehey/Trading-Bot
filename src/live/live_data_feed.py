from src.exchange.ccxt_connector import ExchangeConnector
from src.exchange.utils import ohlcv_to_df
from src.system.alerts import send_alert
import time
import logging
import pandas as pd

logger = logging.getLogger(__name__)

class LiveDataFeed:
    def __init__(self, symbol, timeframe="1h", limit=200):
        self.symbol = symbol
        self.timeframe = timeframe
        self.limit = limit
        self.exchange = ExchangeConnector("binance", testnet=False)

    def fetch(self):
        try:
            data = self.exchange.get_ohlcv(
                self.symbol,
                self.timeframe,
                self.limit
            )
            return ohlcv_to_df(data)
        except Exception as e:
            logger.error(f"Data fetch failed: {e}")
            send_alert(f"⚠️ PRICE FEED DOWN — bot running blind\n{e}")
            
            time.sleep(10)
            
            # Return an empty DataFrame so the main bot loop doesn't crash on NoneType errors
            return pd.DataFrame() 

    def stream(self, interval=None):
        while True:
            df = self.fetch()
            
            # Only yield data if fetch was successful and returned a non-empty DF
            if not df.empty:
                yield df
                
            if interval is not None:
                # This sleep only happens if data was successfully fetched/yielded
                time.sleep(interval)