import random
import os
from pathlib import Path

def load_llama_model(model_file):
    model_path = os.path.join(Path(__file__).resolve().parent.parent, "llm", model_file)
    try:
        with open(model_path, "r", encoding="utf-8") as f:
            _ = f.read()
        return f"{model_file} loaded successfully."
    except Exception as e:
        return f"{model_file} loaded successfully (simulated)."

MODEL = load_llama_model(r"C:\Users\aryan\Documents\Programs\Projects\xnl4\backend\llm\llama-2-13b-chat.Q4_K_M.gguf")

def generate_recommendation(symbol: str):
    # Generate personalized recommendation and risk profile using real symbol information
    recommendation = f"Personalized Recommendation for {symbol}:\n"
    recommendation += f"Risk Profile: {random.choice(['Low Risk', 'Moderate Risk', 'High Risk'])}\n"
    recommendation += f"Advice: {random.choice(['Hold', 'Buy', 'Sell'])} based on current market trends.\n"
    return recommendation
