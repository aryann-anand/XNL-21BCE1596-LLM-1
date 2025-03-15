from llama_cpp import Llama
import os
from pathlib import Path

# Define the path to your real GGUF model for customer queries.
MODEL_PATH = r'C:\Users\aryan\Documents\Programs\Projects\xnl4\backend\llm\llama-2-7b-chat.Q4_K_M.gguf'

# Initialize the LLama model.
try:
    llm = Llama(model_path=MODEL_PATH, n_ctx=512)
except Exception as e:
    raise RuntimeError(f"Error loading Llama model from {MODEL_PATH}: {e}")

def get_response(query: str, report: str):
    """
    Generates a response using the loaded LLama model.
    Combines the user's query and financial report context into a prompt.
    """
    prompt = f"User query: {query}\nContext: {report}\nAnswer in a concise manner:"
    try:
        result = llm(prompt, max_tokens=100, temperature=0.7)
        response_text = result["choices"][0]["text"].strip()
        return response_text
    except Exception as e:
        return f"Error generating response: {e}"
