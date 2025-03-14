from models.model_router import ModelRouter
from utils.logger import get_logger

logger = get_logger(__name__)

class SentimentAnalyzer:
    def __init__(self, model_router):
        self.model_router = model_router
        
    def analyze(self, text):
        prompt = f"""
        [INST] Analyze market sentiment from this text:
        {text}
        
        Return JSON format:
        {{
            "sentiment": "bullish|neutral|bearish",
            "confidence": 0.0-1.0,
            "keywords": ["list", "of", "keywords"]
        }} [/INST]
        """
        return self.model_router.get_response(prompt)