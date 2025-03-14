# config/config.py
class Config:
    # Path to your local Llama GGUF model (if using)
    LLAMA_MODEL_PATH = "models/llama/llama-7b.gguf"
    
    # API keys (replace with your own)
    BINANCE_API_URL = "https://api.binance.com/"
    BINANCE_WS_URL = "wss://stream.binance.com:443"
    BINANCE_API_KEY = "ORRQYICkGSettsnRoAa0hfLK5dJ8ho0KHKX0bxLgDbHDYqUflPvA7ixpM0ecszqm"
    BINANCE_SECRET = "YjMMX7BRFZ1V4WZCrDKMI1fqcjIjKeSa9vfB4Q35zAb0tdM9ScRteDrM3euwlq4o"
    
    # Asset configuration
    ASSETS = {
        "crypto": ["BTCUSDT", "ETHUSDT"],
        "stocks": ["AAPL", "MSFT"],
        "forex": ["EURUSD"],
        "commodities": ["GC=F"]
    }
    
    # Standardized index column name for all historical data
    INDEX_COL = "timestamp"