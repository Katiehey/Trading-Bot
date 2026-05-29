from src.live.live_data_feed import LiveDataFeed
from src.bot.paper_exchange import PaperExchange
from src.risk.risk_manager import RiskManager
from src.backtest.ma_crossover import ma_crossover_strategy
#from src.bot.logger import setup_logger as setup_bot_logger
#from src.system.logger import setup_logger as setup_sys_logger
from src.system.heartbeat import Heartbeat
from src.system.heartbeat_writer import HeartbeatWriter
from src.system.alerts import send_alert 
from src.system.backup import create_backup

import time
import pandas as pd
import logging
import logging.config
from datetime import datetime, UTC

heartbeat = Heartbeat()
bot_heartbeat = HeartbeatWriter(file_path="runtime/heartbeat.txt")

#logging.config.fileConfig("configs/logging.conf")
try:
    # This reads logging.conf and configures the 'root', 'bot', and 'system' loggers
    logging.config.fileConfig("configs/logging.conf", disable_existing_loggers=False)
except FileNotFoundError:
    print("CRITICAL ERROR: logging.conf file not found in configs/ directory.")
    # Fallback to basic configuration if file is missing (optional)
    logging.basicConfig(level=logging.INFO) 

logger = logging.getLogger("bot")         # Name configured in logging.conf
system_logger = logging.getLogger("system") # Name configured in logging.conf

#logger = setup_logger()
#system_logger = system_logger()

send_alert("BOT STARTED 🚀")

SYMBOL = "BTC/USDT"

exchange = PaperExchange()
risk = RiskManager()
feed = LiveDataFeed(SYMBOL)

FETCH_INTERVAL = 60 # Check every minute

last_backup_day = None

try:
    for df in feed.stream(interval=None):
        # Daily Backup Check
        now = datetime.now(UTC).day 
        if last_backup_day != now:
            path = create_backup()
            logger.info(f"[BACKUP] Daily backup created: {path}")
            system_logger.info(f"[BACKUP] Daily backup created: {path}")
            send_alert(f"[BACKUP] Daily backup created: {path.name}")
            last_backup_day = now

        bot_heartbeat.ping()
        
        heartbeat.ping()

        if not heartbeat.check():
            system_logger.info("[HEARTBEAT FAILURE] Bot frozen. Exiting safely.")
            logger.info("[HEARTBEAT FAILURE] Bot frozen. Exiting safely.")
            send_alert("BOT STOPPED 🛑 (heartbeat failure)")
            break

        # Ensure the timestamp column is datetime objects for comparison (renamed from 'datetime' in prev input)
        #df["timestamp"] = pd.to_datetime(df["datetime"], utc=True) 

        # --- DEBUGGING PRINT STATEMENTS ---
        current_time = pd.Timestamp.now(tz='UTC')
        candle_time = df["datetime"].iloc[-1]
        time_difference = current_time - candle_time
        system_logger.info(f"Current Time: {current_time}, Candle Time: {candle_time}, Difference: {time_difference.total_seconds():.0f} seconds")
        logger.info(f"Current Time: {current_time}, Candle Time: {candle_time}, Difference: {time_difference.total_seconds():.0f} seconds")
        # --- END DEBUGGING PRINTS ---

        # --- STALE DATA CHECK (commented out for debugging) ---
        is_stale = df["datetime"].iloc[-1] < pd.Timestamp.now(tz='UTC') - pd.Timedelta(minutes=5)
        
        if is_stale:
            logger.info("[STALE DATA] No new candles. Skipping trade.")
            system_logger.info("[STALE DATA] No new candles. Skipping trade.")
            time.sleep(FETCH_INTERVAL) # <--- Force sleep if stale
            continue
        # --- END STALE DATA CHECK ---


        # --- INSERT STALE DATA CHECK HERE ---
        #if df["timestamp"].iloc[-1] < pd.Timestamp.utcnow() - pd.Timedelta(minutes=5):
            #logger.info("[STALE DATA] No new candles. Skipping trade.")
            #continue


        df["return"] = df["close"].pct_change()
        df = ma_crossover_strategy(df)

        price = df["close"].iloc[-1]
        equity = exchange.equity(price)
        price_series = df["close"]

        allowed, size_or_msg = risk.risk_check(price_series, equity)
        if not allowed:
            logger.info(f"[RISK BLOCKED] {size_or_msg}")
            system_logger.info(f"[RISK BLOCKED] {size_or_msg}")
            continue

        signal = df["signal"].iloc[-1]
        size = min(size_or_msg, 0.001)

        if signal == 1:
            exchange.buy(price, size)
            send_alert(f"🟢 BUY Order Executed:\nSymbol: {SYMBOL}\nPrice: {price:.2f}\nSize: {size:.4f}")
        elif signal == -1:
            exchange.sell(price, size)
            send_alert(f"🔴 SELL Order Executed:\nSymbol: {SYMBOL}\nPrice: {price:.2f}\nSize: {size:.4f}")

        logger.info(
            f"Price={price:.2f} "
            f"Position={exchange.position:.4f} | "
            f"Equity={exchange.equity(price):.2f}"
        )

        system_logger.info(
            f"Price={price:.2f} "
            f"Position={exchange.position:.4f} | "
            f"Equity={exchange.equity(price):.2f}"
        )        

        #time.sleep(300) # <--- Add a sleep here when trade logic has completed
        # Ping every 30 seconds while waiting for the next main loop iteration
        for _ in range(0, 300, 30):
            bot_heartbeat.ping() # Need 'self.' here if called from a class method
            time.sleep(30)


except Exception as e:
    # This block runs if any error occurs inside the loop
    send_alert(f"BOT CRASHED ❌\n{e}")
    system_logger.error(f"[CRITICAL ERROR] Bot halted safely: {e}")
    #print(f"[CRITICAL ERROR] Bot halted safely: {e}")
        # --- END STALE DATA CHECK ---
finally: # This runs whether the loop breaks or an exception occurs 
    send_alert("BOT STOPPED 🛑") 
    system_logger.info("Bot stopped cleanly") 
    logger.info("Bot stopped cleanly")
