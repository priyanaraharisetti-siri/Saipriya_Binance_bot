import sys
import logging
from binance.client import Client
from dotenv import load_dotenv
import os

load_dotenv()

logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

client = Client(
    os.getenv("BINANCE_API_KEY"),
    os.getenv("BINANCE_API_SECRET"),
    testnet=True
)

def validate(symbol, side, qty, price):
    if not symbol.endswith("USDT"):
        raise ValueError("Invalid symbol")
    if side not in ["BUY", "SELL"]:
        raise ValueError("Side must be BUY or SELL")
    if float(qty) <= 0 or float(price) <= 0:
        raise ValueError("Quantity/Price must be > 0")

def place_limit_order(symbol, side, qty, price):
    validate(symbol, side, qty, price)
    order = client.futures_create_order(
        symbol=symbol,
        side=side,
        type="LIMIT",
        quantity=qty,
        price=price,
        timeInForce="GTC"
    )
    logging.info(f"LIMIT {side} {symbol} {qty} @ {price}")
    print(order)

if __name__ == "__main__":
    try:
        symbol = sys.argv[1]
        side = sys.argv[2]
        qty = sys.argv[3]
        price = sys.argv[4]
        place_limit_order(symbol, side, qty, price)
    except Exception as e:
        logging.error(str(e))
        print("Error:", e)
