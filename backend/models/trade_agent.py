from datetime import datetime
from utils import binance_client

# Simulated mock wallet balances. (Transactions are simulated behind the scenes.)
MOCK_WALLET = {
    "BTCUSDT": 10.0,
    "ETHUSDT": 100.0
}

def execute_mock_trade(symbol: str, amount: float):
    # Check available balance in the simulated wallet
    if symbol not in MOCK_WALLET:
        raise ValueError("Invalid symbol.")
    if amount > MOCK_WALLET[symbol]:
        raise ValueError("Insufficient funds in mock wallet.")
    
    # Use the real market price from Binance API
    ticker_data = binance_client.get_ticker(symbol)
    price = ticker_data.get("price", ticker_data.get("lastPrice", "N/A"))

    MOCK_WALLET[symbol] -= amount

    trade_record = {
        "symbol": symbol,
        "amount": amount,
        "price": price,
        "timestamp": datetime.now().isoformat(),
        "balance_after": MOCK_WALLET[symbol]
    }
    return trade_record
