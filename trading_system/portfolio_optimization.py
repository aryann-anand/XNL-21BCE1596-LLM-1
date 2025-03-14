import pandas as pd
import numpy as np
from scipy.optimize import minimize
from config.config import Config
from llama_cpp import Llama

# Initialize the local Llama model (loaded once at module level for efficiency)
llm = Llama(model_path=Config.LLAMA_MODEL_PATH)

def optimize_portfolio_mpt():
    """
    Optimize portfolio weights using Modern Portfolio Theory.
    Assumes historical data is available in CSV files.
    """
    asset_data = {}
    # Load historical data for each asset
    for asset_type, symbols in Config.ASSETS.items():
        for symbol in symbols:
            # Adjust file path based on your data structure
            file_path = (
                f"data\\historical\\{symbol.lower()}_1h.csv"
                if "USDT" in symbol
                else f"data\\historical\\{symbol.lower()}.csv"
            )
            df = pd.read_csv(file_path, index_col="open_time")
            asset_data[symbol] = df["close"].pct_change().dropna()

    # Create returns DataFrame
    returns_df = pd.DataFrame(asset_data)
    mean_returns = returns_df.mean()  # Expected returns
    cov_matrix = returns_df.cov()     # Covariance matrix

    # Define portfolio metrics (negative Sharpe ratio for minimization)
    def portfolio_metrics(weights, returns, cov):
        port_return = np.dot(weights, returns)
        port_vol = np.sqrt(np.dot(weights.T, np.dot(cov, weights)))
        return -port_return / port_vol  # Maximize Sharpe ratio (simplified)

    # Optimization setup
    num_assets = len(mean_returns)
    constraints = ({"type": "eq", "fun": lambda x: np.sum(x) - 1})  # Weights sum to 1
    bounds = tuple((0, 1) for _ in range(num_assets))              # Weights between 0 and 1
    initial_weights = [1.0 / num_assets] * num_assets              # Equal initial weights

    # Run optimization
    result = minimize(
        portfolio_metrics,
        initial_weights,
        args=(mean_returns, cov_matrix),
        method="SLSQP",
        bounds=bounds,
        constraints=constraints
    )
    
    # Return optimized weights as a dictionary
    return dict(zip(Config.ASSETS.keys(), result.x))

def generate_recommendation(user_profile):
    """
    Generate a personalized investment recommendation using the local Llama model.
    """
    weights = optimize_portfolio_mpt()
    prompt = (
        f"You are a financial advisor. Based on the following user profile and portfolio optimization results, "
        f"provide a detailed investment recommendation in natural language.\n\n"
        f"User Profile: {user_profile}\n"
        f"Optimized Portfolio Weights: {weights}\n\n"
        f"Recommendation:"
    )
    
    # Generate response using the local Llama model
    response = llm(prompt, max_tokens=300, temperature=0.7)
    recommendation = response["choices"][0]["text"].strip()
    return recommendation

if __name__ == "__main__":
    # Test the optimization and recommendation
    weights = optimize_portfolio_mpt()
    print("Optimal Portfolio Weights:", weights)
    rec = generate_recommendation("Risk-averse investor")
    print("Recommendation:", rec)