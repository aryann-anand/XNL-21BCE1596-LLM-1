import websockets
import json
from binance import AsyncClient
from utils.logger import get_logger

logger = get_logger(__name__)

class BinanceDataClient:
    def __init__(self, config):
        self.config = config
        self.ws_url = config['binance']['ws_url']
        self.streams = config['binance']['streams']
        self.client = None

    async def connect_websocket(self):
        """Connect to Binance WebSocket"""
        stream_url = f"{self.ws_url}/{'/'.join(self.streams)}"
        try:
            async with websockets.connect(stream_url) as ws:
                logger.info("Connected to Binance WebSocket")
                while True:
                    message = await ws.recv()
                    yield json.loads(message)
        except Exception as e:
            logger.error(f"WebSocket error: {str(e)}")

    async def get_historical_data(self, symbol, interval):
        """Fetch historical market data"""
        client = await AsyncClient.create()
        try:
            klines = await client.get_klines(
                symbol=symbol,
                interval=interval,
                limit=1000
            )
            return klines
        finally:
            await client.close_connection()