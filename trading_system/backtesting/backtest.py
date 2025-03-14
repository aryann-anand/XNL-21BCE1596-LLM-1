# backtesting/backtest.py
# from rl_trading import TradingEnv
from stable_baselines3 import PPO
from utils.metrics import calculate_sharpe_ratio, calculate_sortino_ratio, calculate_drawdown
import pandas as pd
import numpy as np
from config.config import Config
import gymnasium as gym
from gymnasium import spaces

class TradingEnv(gym.Env):
    def __init__(self, df):
        super(TradingEnv, self).__init__()
        self.df = df
        self.current_step = 0
        self.max_steps = len(df) - 1
        self.action_space = spaces.Discrete(3)  # 0: hold, 1: buy, 2: sell
        self.observation_space = spaces.Box(low=0, high=np.inf, shape=(5,), dtype=np.float32)
        self.position = 0  # 0: no position, 1: long, -1: short
        self.cash = 10000
        self.initial_cash = self.cash
        self.asset_value = 0

    def reset(self, seed=None):
        self.current_step = 0
        self.position = 0
        self.cash = self.initial_cash
        self.asset_value = 0
        return self._get_observation(), {}

    def step(self, action):
        prev_value = self.cash + self.asset_value
        current_price = self.df.iloc[self.current_step]["close"]

        if action == 1:  # Buy
            if self.position == 0:
                self.position = 1
                self.asset_value = self.cash / current_price
                self.cash = 0
            elif self.position == -1:
                self.cash += self.asset_value * current_price
                self.position = 0
                self.asset_value = 0
        elif action == 2:  # Sell
            if self.position == 0:
                self.position = -1
                self.asset_value = self.cash / current_price
                self.cash = 0
            elif self.position == 1:
                self.cash += self.asset_value * current_price
                self.position = 0
                self.asset_value = 0

        self.current_step += 1
        obs = self._get_observation()
        current_value = self.cash + (self.asset_value * self.df.iloc[self.current_step]["close"] if self.position != 0 else 0)
        reward = current_value - prev_value
        done = self.current_step >= self.max_steps
        truncated = False
        return obs, reward, done, truncated, {}

    def _get_observation(self):
        start = max(0, self.current_step - 5)
        prices = self.df.iloc[start:self.current_step]["close"].values
        prices = np.pad(prices, (5 - len(prices), 0), "constant")
        return prices

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