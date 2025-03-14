# execution/order_execution.py
import ccxt
from config.config import Config

exchange = ccxt.binance({
    "apiKey": Config.BINANCE_API_KEY,
    "secret": Config.BINANCE_SECRET,
})

def place_order(symbol, side, amount):
    try:
        order = exchange.create_market_order(symbol, side, amount)
        print(f"Order placed: {side} {amount} of {symbol}")
        return order
    except Exception as e:
        print(f"Error placing order: {e}")
        return None

# Note: Forex and commodities would require different exchange APIs