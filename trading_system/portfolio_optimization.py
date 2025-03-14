# portfolio_optimization.py
import pandas as pd
import numpy as np
from scipy.optimize import minimize
from config.config import Config
from llama_cpp import Llama

# Initialize the local Llama model (if using)
llm = Llama(model_path=Config.LLAMA_MODEL_PATH)

def optimize_portfolio_mpt():
    asset_data = {}
    for asset_type, symbols in Config.ASSETS.items():
        for symbol in symbols:
            file_path = f"data\\historical\\{symbol.lower()}_1h.csv" if "USDT" in symbol else f"data\\historical\\{symbol.lower()}.csv"
            df = pd.read_csv(file_path, index_col=Config.INDEX_COL)
            asset_data[symbol] = df["close"].pct_change().dropna()

    returns_df = pd.DataFrame(asset_data)
    mean_returns = returns_df.mean()
    cov_matrix = returns_df.cov()

    def portfolio_metrics(weights, returns, cov):
        port_return = np.dot(weights, returns)
        port_vol = np.sqrt(np.dot(weights.T, np.dot(cov, weights)))
        return -port_return / port_vol  # Maximize Sharpe ratio (simplified)

    num_assets = len(mean_returns)
    constraints = ({"type": "eq", "fun": lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for _ in range(num_assets))
    initial_weights = num_assets * [1. / num_assets]
    result = minimize(portfolio_metrics, initial_weights, args=(mean_returns, cov_matrix),
                      method="SLSQP", bounds=bounds, constraints=constraints)
    return dict(zip(Config.ASSETS.keys(), result.x))

def generate_recommendation(user_profile):
    weights = optimize_portfolio_mpt()
    prompt = (
        f"You are a financial advisor. Based on the following user profile and portfolio optimization results, "
        f"provide a detailed investment recommendation in natural language.\n\n"
        f"User Profile: {user_profile}\n"
        f"Optimized Portfolio Weights: {weights}\n\n"
        f"Recommendation:"
    )
    response = llm(prompt, max_tokens=300, temperature=0.7)
    recommendation = response["choices"][0]["text"].strip()
    return recommendation

if __name__ == "__main__":
    weights = optimize_portfolio_mpt()
    print("Optimal Portfolio Weights:", weights)
    rec = generate_recommendation("Risk-averse investor")
    print("Recommendation:", rec)