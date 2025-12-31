import sys
import logging
from binance.client import Client
from dotenv import load_dotenv
import os

# Load environment variables
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

def validate(symbol, side, quantity, price, stop_price):
    if not symbol.endswith("USDT"):
        raise ValueError("Invalid symbol")
    if side not in ["BUY", "SELL"]:
        raise ValueError("Side must be BUY or SELL")
    if float(quantity) <= 0 or float(price) <= 0 or float(stop_price) <= 0:
        raise ValueError("Quantity, price and stop price must be > 0")
    if side == "SELL" and float(stop_price) > float(price):
        raise ValueError("Stop price should be <= limit price for SELL")
    if side == "BUY" and float(stop_price) < float(price):
        raise ValueError("Stop price should be >= limit price for BUY")

def place_oco_order(symbol, side, quantity, price, stop_price):
    validate(symbol, side, quantity, price, stop_price)
    order = client.futures_create_order(
        symbol=symbol,
        side=side,
        type="OCO",
        quantity=quantity,
        price=price,
        stopPrice=stop_price,
        stopLimitPrice=stop_price,
        stopLimitTimeInForce="GTC"
    )
    logging.info(f"OCO {side} {symbol} {quantity} @ {price} stop {stop_price}")
    print(order)

if __name__ == "__main__":
    try:
        symbol = sys.argv[1]       # BTCUSDT
        side = sys.argv[2]         # BUY or SELL
        quantity = sys.argv[3]     # e.g., 0.01
        price = sys.argv[4]        # take profit price
        stop_price = sys.argv[5]   # stop loss price
        place_oco_order(symbol, side, quantity, price, stop_price)
    except Exception as e:
        logging.error(str(e))
        print("Error:", e)
