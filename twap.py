import sys
import time
import logging
from binance.client import Client
from dotenv import load_dotenv
import os

# Load env
load_dotenv()

# Logging
logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# Binance Testnet client
client = Client(
    os.getenv("BINANCE_API_KEY"),
    os.getenv("BINANCE_API_SECRET"),
    testnet=True
)

def validate(symbol, side, total_qty, chunks, interval):
    if not symbol.endswith("USDT"):
        raise ValueError("Invalid symbol")
    if side not in ["BUY", "SELL"]:
        raise ValueError("Side must be BUY or SELL")
    if float(total_qty) <= 0:
        raise ValueError("Quantity must be > 0")
    if int(chunks) <= 0 or float(interval) < 0:
        raise ValueError("Chunks and interval must be positive")

def twap_order(symbol, side, total_qty, chunks, interval):
    validate(symbol, side, total_qty, chunks, interval)
    qty_per_order = float(total_qty) / int(chunks)

    for i in range(int(chunks)):
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=qty_per_order
        )
        logging.info(f"TWAP {side} {symbol} {qty_per_order} (order {i+1}/{chunks})")
        print(f"Placed order {i+1}/{chunks}: {order['orderId']}")
        if i < int(chunks) - 1:
            time.sleep(float(interval))

if __name__ == "__main__":
    try:
        symbol = sys.argv[1]        # e.g., BTCUSDT
        side = sys.argv[2]          # BUY or SELL
        total_qty = sys.argv[3]     # e.g., 1
        chunks = sys.argv[4]        # e.g., 5
        interval = sys.argv[5]      # seconds between orders, e.g., 60
        twap_order(symbol, side, total_qty, chunks, interval)
    except Exception as e:
        logging.error(str(e))
        print("Error:", e)
