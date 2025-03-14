# api/app.py
from fastapi import FastAPI, WebSocket
import websockets
from rl_trading import TradingEnv
from stable_baselines3 import PPO
from execution.order_execution import place_order
from config.config import Config
import pandas as pd
import asyncio

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    async with websockets.connect(f"{Config.BINANCE_WS_URL}/ws/btcusdt@kline_1h") as ws:
        while True:
            data = await ws.recv()
            # Process real-time data and trade (simplified)
            df = pd.read_csv("data\\historical\\btcusdt_1h.csv", index_col="open_time")
            env = TradingEnv(df)
            model = PPO.load("models\\rl_agents\\ppo_btcusdt")
            obs, _ = env.reset()
            action, _ = model.predict(obs)
            if action == 1:
                place_order("BTCUSDT", "buy", 0.001)  # Example amount
            elif action == 2:
                place_order("BTCUSDT", "sell", 0.001)
            await websocket.send_text(f"Action taken: {action}")
            await asyncio.sleep(1)