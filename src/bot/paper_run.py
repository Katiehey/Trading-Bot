# Create paper trading runner; this stitches everything together.
import time
import pandas as pd
import numpy as np # Ensure numpy is imported if used in RiskManager

# Assuming the required imports are correctly available in src/bot and src/risk
from src.bot.paper_exchange import PaperExchange
from src.bot.market_data import fetch_latest_candle
from src.backtest.ma_crossover import ma_crossover_strategy
from src.features.technical import add_technical_features
from src.bot.logger import setup_logger
from src.bot.config import load_config
from src.risk.risk_manager import RiskManager

# Initialize components
risk = RiskManager()
config = load_config("configs/ma_crossover.yaml")
logger = setup_logger()
exchange = PaperExchange()
history = []

SYMBOL = config["symbol"]
TIMEFRAME = config["timeframe"]
# TRADE_SIZE is now ignored, as the risk manager dictates size

def step():
    candle = fetch_latest_candle(SYMBOL, TIMEFRAME)
    history.append(candle)

    if len(history) < 30:
        print(f"Fetching data... {len(history)} of 30 candles collected.")
        return

    # Prepare DataFrame
    df = pd.DataFrame(
        history,
        columns=["datetime", "open", "high", "low", "close", "volume"]
    )
    df["datetime"] = pd.to_datetime(df["datetime"], unit="ms")
    df["return"] = df["close"].pct_change()
    
    # Run strategy and features
    df = add_technical_features(df)
    df = ma_crossover_strategy(df)

    last = df.iloc[-1]
    price = last["close"]
    signal_pos = last["position"] # Unit signal: 1, -1, or 0

    current_equity = exchange.equity(price)
    price_history = df['close']
    realized_pnl = None
    
    # --- RISK MANAGEMENT: Check if a trade is allowed and get size ---
    allowed, info = risk.risk_check(price_history, current_equity)

    if not allowed:
        logger.info(f"[RISK BLOCKED]: {info}")
        with open("logs/bot.log", "a") as f:
            f.write(f"RISK EVENT: {info}\n")
        # print(f"[RISK BLOCKED]: {info}") # Optional: keep print for console visibility
        return  # skip trade entirely if blocked

    # If allowed, info is the calculated position size
    position_size = info 
    
    # --- TRADE EXECUTION ---
    
    current_exchange_position = exchange.position 

    # 1. LONG ENTRY/REVERSAL (Signal > 0, Position <= 0)
    if signal_pos > 0 and current_exchange_position <= 0:
        # Close opposite position first (if short)
        if current_exchange_position < 0:
            pnl_result = exchange.buy(price, size=abs(current_exchange_position))
            if pnl_result is not None:
                realized_pnl = pnl_result
        
        # Enter new long position
        exchange.buy(price, size=position_size)

    # 2. SHORT ENTRY/REVERSAL (Signal < 0, Position >= 0)
    elif signal_pos < 0 and current_exchange_position >= 0:
        # Close opposite position first (if long)
        if current_exchange_position > 0:
            pnl_result = exchange.sell(price, size=abs(current_exchange_position))
            if pnl_result is not None:
                realized_pnl = pnl_result

        # Enter new short position
        exchange.sell(price, size=position_size)

    # 3. PNL Registration (Register PnL if a position was closed in this step)
    if realized_pnl is not None and realized_pnl != 0:
        risk.register_trade_result(realized_pnl)
        logger.info(f"Registered trade result with PnL: {realized_pnl:.2f}")

    # --- FINAL LOGGING ---
    logger.info(
        f"Price={price:.2f} "
        f"Position={exchange.position} "
        f"Equity={exchange.equity(price):.2f}"
    )


if __name__ == "__main__":
    while True:
        try:
            step()
            time.sleep(1)
        except Exception as e:
            logger.exception("Bot error")
            time.sleep(60)

