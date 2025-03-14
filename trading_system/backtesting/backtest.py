# backtesting/backtest.py
from rl_trading import TradingEnv
from stable_baselines3 import PPO
from utils.metrics import calculate_sharpe_ratio, calculate_sortino_ratio, calculate_drawdown
import pandas as pd
import numpy as np
from config.config import Config

def backtest_strategy(symbol):
    file_path = f"data\\historical\\{symbol.lower()}_1h.csv" if "USDT" in symbol else f"data\\historical\\{symbol.lower()}.csv"
    df = pd.read_csv(file_path, index_col=Config.INDEX_COL)
    env = TradingEnv(df)
    model = PPO.load(f"models\\rl_agents\\ppo_{symbol.lower()}")
    obs, _ = env.reset()
    portfolio_values = []
    returns = []

    done = False
    while not done:
        action, _ = model.predict(obs)
        obs, reward, done, _, _ = env.step(action)
        total_value = env.cash + (env.asset_value * env.df.iloc[env.current_step]["close"] if env.position != 0 else 0)
        portfolio_values.append(total_value)
        if len(portfolio_values) > 1:
            returns.append((portfolio_values[-1] - portfolio_values[-2]) / portfolio_values[-2])

    sharpe = calculate_sharpe_ratio(np.array(returns))
    sortino = calculate_sortino_ratio(np.array(returns))
    drawdown = calculate_drawdown(np.array(portfolio_values))
    return {"sharpe": sharpe, "sortino": sortino, "drawdown": drawdown}

if __name__ == "__main__":
    for asset_type, symbols in Config.ASSETS.items():
        for symbol in symbols:
            metrics = backtest_strategy(symbol)
            print(f"{symbol} - Sharpe: {metrics['sharpe']:.2f}, Sortino: {metrics['sortino']:.2f}, Drawdown: {metrics['drawdown']:.2f}")