import yaml
import asyncio
from data_ingestion.binance_client import BinanceDataClient
from models.model_router import ModelRouter
from services.sentiment_analysis import SentimentAnalyzer
from services.report_summarizer import ReportSummarizer

def load_config():
    with open('config/settings.yaml') as f:
        return yaml.safe_load(f)

async def main():
    config = load_config()
    
    # Initialize components
    data_client = BinanceDataClient(config)
    model_router = ModelRouter(config)
    sentiment_analyzer = SentimentAnalyzer(model_router)
    report_summarizer = ReportSummarizer(model_router)

    # Start WebSocket listener
    async for market_data in data_client.connect_websocket():
        try:
            # Example analysis flow
            symbol = market_data['s']
            price = float(market_data['p'])
            volume = float(market_data['q'])
            
            # Sentiment analysis
            news_text = "Sample news about market trends..."
            sentiment = sentiment_analyzer.analyze(news_text)
            print(f"Market Sentiment: {sentiment}")
            
            # Report summarization example
            report_text = "Annual financial report..."
            summary = report_summarizer.summarize(report_text)
            print(f"Report Summary:\n{summary}")
            
        except Exception as e:
            print(f"Processing error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())