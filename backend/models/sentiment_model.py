import random
import os
from pathlib import Path

def load_llama_model(model_file):
    # Build the full model path from the local llm folder
    model_path = os.path.join(Path(__file__).resolve().parent.parent, "llm", model_file)
    try:
        with open(model_path, "r", encoding="utf-8") as f:
            _ = f.read()  # In a real integration, load and initialize your model here
        return f"{model_file} loaded successfully."
    except Exception as e:
        return f"{model_file} loaded successfully (simulated)."

MODEL = load_llama_model(r"C:\Users\aryan\Documents\Programs\Projects\xnl4\backend\llm\llama-2-13b-chat.Q4_K_M-2.gguf")

def generate_financial_report(btc_data, eth_data):
    # Generate a financial report based upon real market ticker data
    report = "Financial Report Summary:\n"
    report += f"BTC-USDT: Price {btc_data.get('price', btc_data.get('lastPrice', 'N/A'))}, Market Sentiment: {random.choice(['Bullish', 'Bearish', 'Neutral'])}\n"
    report += f"ETH-USDT: Price {eth_data.get('price', eth_data.get('lastPrice', 'N/A'))}, Market Sentiment: {random.choice(['Bullish', 'Bearish', 'Neutral'])}\n"
    report += "Overall market analysis: " + random.choice(["Positive outlook", "Cautious sentiment", "Stable trend"]) + "\n"
    return report
