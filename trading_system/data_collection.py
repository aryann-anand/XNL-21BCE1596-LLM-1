# data_collection.py
import requests
import pandas as pd
import yfinance as yf
from config.config import Config

def fetch_binance_data(symbol, interval="1h", start_time="2020-01-01", end_time="2023-01-01"):
    url = f"{Config.BINANCE_API_URL}api/v3/klines"
    start_ts = int(pd.Timestamp(start_time).timestamp() * 1000)
    end_ts = int(pd.Timestamp(end_time).timestamp() * 1000)
    params = {
        "symbol": symbol,
        "interval": interval,
        "startTime": start_ts,
        "endTime": end_ts,
        "limit": 1000
    }
    response = requests.get(url, params=params)
    data = response.json()
    df = pd.DataFrame(data, columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
    ])
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    df.set_index("open_time", inplace=True)
    df.index.name = Config.INDEX_COL  # Standardized to "timestamp"
    df = df[["open", "high", "low", "close", "volume"]].astype(float)
    return df

def fetch_stock_data(symbol, start_date="2020-01-01", end_date="2023-01-01"):
    stock = yf.Ticker(symbol)
    df = stock.history(start=start_date, end=end_date)
    df = df[["Open", "High", "Low", "Close", "Volume"]]
    df.columns = ["open", "high", "low", "close", "volume"]
    df.index.name = Config.INDEX_COL  # Standardized to "timestamp"
    return df

def collect_all_data():
    for asset_type, symbols in Config.ASSETS.items():
        for symbol in symbols:
            if asset_type == "crypto":
                df = fetch_binance_data(symbol)
                df.to_csv(f"data\\historical\\{symbol.lower()}_1h.csv")
            else:  # stocks, forex, commodities
                df = fetch_stock_data(symbol)
                df.to_csv(f"data\\historical\\{symbol.lower()}.csv")
            print(f"Collected data for {symbol}")

if __name__ == "__main__":
    collect_all_data()