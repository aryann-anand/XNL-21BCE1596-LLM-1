# rl_trading.py
import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pandas as pd
from stable_baselines3 import PPO
from config.config import Config

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

def train_rl_agent(symbol):
    file_path = f"data\\historical\\{symbol.lower()}_1h.csv" if "USDT" in symbol else f"data\\historical\\{symbol.lower()}.csv"
    df = pd.read_csv(file_path, index_col=Config.INDEX_COL)
    env = TradingEnv(df)
    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=10000)
    model.save(f"models\\rl_agents\\ppo_{symbol.lower()}")
    return model

if __name__ == "__main__":
    for asset_type, symbols in Config.ASSETS.items():
        for symbol in symbols:
            train_rl_agent(symbol)