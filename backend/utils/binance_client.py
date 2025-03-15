import requests

BASE_URL = "https://api.binance.com"

def get_ticker(symbol: str):
    url = f"{BASE_URL}/api/v3/ticker/price"
    params = {"symbol": symbol}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Error fetching ticker data: {response.text}")
    return response.json()

def get_klines(symbol: str, interval: str = "1h", limit: int = 100):
    url = f"{BASE_URL}/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Error fetching klines: {response.text}")
    return response.json()
