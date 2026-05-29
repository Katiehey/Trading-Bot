import pandas as pd
import datetime
from src.system.alerts import send_alert

def send_daily_summary():
    try:
        # Load trades from CSV
        df = pd.read_csv("logs/trades.csv")

        # Drop any accidental header rows or bad values
        df = df[df["timestamp"].astype(str).str.lower() != "timestamp"]

        # Parse timestamps safely
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df = df.dropna(subset=["timestamp"])

        today = datetime.datetime.utcnow().date()

        # Filter today's trades
        todays_trades = df[df["timestamp"].dt.date == today]

        if todays_trades.empty:
            send_alert("📊 Daily Summary: No trades today")
            return

        # Calculate PnL = last balance - first balance of the day
        pnl_today = todays_trades["balance"].iloc[-1] - todays_trades["balance"].iloc[0]

        # Win rate = % of trades where balance increased
        balance_changes = todays_trades["balance"].diff().fillna(0)
        win_rate = (balance_changes > 0).mean()

        summary_msg = (
            f"📊 Daily Summary {today}\n"
            f"PnL={pnl_today:.2f}\n"
            f"WinRate={win_rate:.2%}\n"
            f"Trades={len(todays_trades)}"
        )

        send_alert(summary_msg)
    except Exception as e:
        send_alert(f"❌ Daily summary failed: {e}")

if __name__ == "__main__":
    send_daily_summary()

