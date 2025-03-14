# main.py
from data_collection import collect_all_data
from rl_trading import train_rl_agent
from backtesting.backtest import backtest_strategy
from portfolio_optimization import optimize_portfolio_mpt, generate_recommendation
from ab_testing import run_ab_testing
from config.config import Config
import uvicorn

def main():
    print("1. Collecting Data...")
    collect_all_data()

    print("2. Training RL Agents...")
    for asset_type, symbols in Config.ASSETS.items():
        for symbol in symbols:
            train_rl_agent(symbol)

    print("3. Backtesting Strategies...")
    for asset_type, symbols in Config.ASSETS.items():
        for symbol in symbols:
            metrics = backtest_strategy(symbol)
            print(f"{symbol}: {metrics}")

    print("4. Optimizing Portfolio...")
    weights = optimize_portfolio_mpt()
    print("Portfolio Weights:", weights)

    print("5. Generating Recommendation...")
    rec = generate_recommendation("Moderate risk investor")
    print(rec)

    print("6. Running A/B Testing...")
    best_models = run_ab_testing()
    print("Best Models:", best_models)

    print("7. Starting API Server...")
    uvicorn.run("api.app:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()