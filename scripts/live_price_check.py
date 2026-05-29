from src.exchange.ccxt_connector import ExchangeConnector
import time

exchange = ExchangeConnector("binance", testnet=True)
symbol = "BTC/USDT"

while True:
    ticker = exchange.get_ticker(symbol)
    print(
        f"Price: {ticker['last']} | "
        f"Time: {ticker['datetime']} | "
        f"Volume: {ticker['baseVolume']}"
    )
    time.sleep(5)
