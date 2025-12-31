# Binance Futures Order Bot

## Setup
- Python 3.9+
- Install dependencies:
  pip install python-binance python-dotenv

## API Setup
- Create Binance Futures Testnet API keys
- Add them to `.env`

## Run
Market Order:
python src/market_orders.py BTCUSDT BUY 0.01

Limit Order:
python src/limit_orders.py BTCUSDT SELL 0.01 70000
