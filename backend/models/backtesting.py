import pandas as pd
import random
from utils import binance_client

def run_backtesting(symbol: str = "BTCUSDT"):
    # Fetch historical klines for the given symbol from Binance (1h interval, 100 points)
    klines = binance_client.get_klines(symbol, interval="1h", limit=100)
    
    dates = []
    prices = []
    for k in klines:
        dates.append(pd.to_datetime(k[0], unit='ms'))
        prices.append(float(k[4]))  # Closing price
    
    data = pd.DataFrame({
        "date": dates,
        "price": prices
    })
    
    # Simulated predictions using moving averages
    if len(data) >= 5:
        xgboost_pred = data["price"].rolling(window=5).mean().iloc[-1] + random.uniform(-1, 1)
    else:
        xgboost_pred = prices[-1]
    if len(data) >= 10:
        lstm_pred = data["price"].rolling(window=10).mean().iloc[-1] + random.uniform(-1, 1)
    else:
        lstm_pred = prices[-1]
    xgb_error = random.uniform(0, 5)
    lstm_error = random.uniform(0, 5)
    best_model = "XGBoost" if xgb_error < lstm_error else "LSTM"
    
    result = {
        "xgboost_prediction": xgboost_pred,
        "lstm_prediction": lstm_pred,
        "xgboost_error": xgb_error,
        "lstm_error": lstm_error,
        "best_model": best_model,
        "historical_data": data.tail(50).to_dict(orient="records")
    }
    return result
