# config/config.py
class Config:
    BINANCE_API_URL = "https://api.binance.com/"
    BINANCE_WS_URL = "wss://stream.binance.com:443"
    BINANCE_API_KEY = "YOUR_BINANCE_API_KEY"  # Replace with your key
    BINANCE_SECRET = "YOUR_BINANCE_SECRET"    # Replace with your secret
    OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"    # Replace with your key (for LLM)
    LLAMA_MODEL_PATH = "C:\\Users\\aryan\\Documents\\Programs\\Projects\\xnl\\fintech-llm-ecosystem\\models\\llama-2-13b-chat.Q4_K_M.gguf"
    ASSETS = {
        "stocks": ["AAPL", "GOOGL"],
        "crypto": ["BTCUSDT", "ETHUSDT"]
    }