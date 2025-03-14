# ab_testing.py
from backtesting.backtest import backtest_strategy
from config.config import Config

def run_ab_testing():
    model_metrics = {}
    for asset_type, symbols in Config.ASSETS.items():
        for symbol in symbols:
            metrics = backtest_strategy(symbol)  # Only RL for now, extend to XGBoost/LSTM
            model_metrics[symbol] = {"PPO": metrics}
    best_models = {symbol: max(metrics.items(), key=lambda x: x[1]["sharpe"])[0] for symbol, metrics in model_metrics.items()}
    return best_models

if __name__ == "__main__":
    best_models = run_ab_testing()
    print("Best Models per Asset:", best_models)