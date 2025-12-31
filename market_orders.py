import sys
import logging
from binance.client import Client
from dotenv import load_dotenv
import os
print("Bot is starting...")


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

def validate(symbol, side, qty):
    if not symbol.endswith("USDT"):
        raise ValueError("Invalid symbol")
    if side not in ["BUY", "SELL"]:
        raise ValueError("Side must be BUY or SELL")
    if float(qty) <= 0:
        raise ValueError("Quantity must be > 0")

def place_market_order(symbol, side, qty):
    validate(symbol, side, qty)
    order = client.futures_create_order(
        symbol=symbol,
        side=side,
        type="MARKET",
        quantity=qty
    )
    logging.info(f"MARKET {side} {symbol} {qty}")
    print(order)

if __name__ == "__main__":
    try:
        symbol = sys.argv[1]
        side = sys.argv[2]
        qty = sys.argv[3]
        place_market_order(symbol, side, qty)
    except Exception as e:
        logging.error(str(e))
        print("Error:", e)
