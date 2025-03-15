from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import our custom modules (LLama-powered models and utilities)
from models import sentiment_model, recommendation_model, customer_query_model, trade_agent, backtesting
from utils import binance_client, file_logging

app = FastAPI()

# Allow CORS for requests coming from our frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/market-data")
async def get_market_data():
    """
    Get real market data for BTC-USDT and ETH-USDT using Binance REST API.
    """
    try:
        btc_data = binance_client.get_ticker("BTCUSDT")
        eth_data = binance_client.get_ticker("ETHUSDT")
        return {"BTCUSDT": btc_data, "ETHUSDT": eth_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-report")
async def generate_report():
    """
    Generate a financial report using the sentiment LLama model.
    Saves the report as "financial_report.txt".
    """
    try:
        btc_data = binance_client.get_ticker("BTCUSDT")
        eth_data = binance_client.get_ticker("ETHUSDT")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching market data: " + str(e))

    report = sentiment_model.generate_financial_report(btc_data, eth_data)
    file_logging.save_to_file("financial_report.txt", report)
    return {"message": "Report generated and saved", "report": report}

@app.post("/api/personalized-recommendation")
async def personalized_recommendation(symbol: str):
    """
    Generate personalized recommendations (risk profiling, advice) using the recommendation LLama model.
    Saves the recommendation as "personalized_recommendation.txt".
    """
    recommendation = recommendation_model.generate_recommendation(symbol)
    file_logging.save_to_file("personalized_recommendation.txt", recommendation)
    return {"message": "Personalized recommendation generated", "recommendation": recommendation}

@app.post("/api/simulate-trade")
async def simulate_trade(data: dict):
    """
    Execute a simulated trade (mock trade) using real market price data but a virtual wallet.
    Note: Only transactions are simulated. The tester sees real price data.
    """
    try:
        symbol = data.get("symbol")
        amount = data.get("amount")
        trade_result = trade_agent.execute_mock_trade(symbol, amount)
        file_logging.append_to_log("transactions_log.txt", trade_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error executing trade: " + str(e))
    return {"message": "Trade executed", "trade": trade_result}

@app.get("/api/transaction-logs")
async def transaction_logs():
    """
    Retrieve the transaction log file.
    """
    try:
        logs = file_logging.read_file("transactions_log.txt")
        return {"logs": logs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
async def chat(payload: dict):
    """
    Process customer chat queries using the customer query LLama model.
    Also scans the financial report for suspicious activity.
    """
    query_str = payload.get("query")
    report = file_logging.read_file("financial_report.txt")
    response = customer_query_model.get_response(query_str, report)
    return {"response": response}

@app.get("/api/backtesting")
async def run_backtesting(symbol: str = Query("BTCUSDT")):
    """
    Run backtesting using historical data (real Binance klines) with two models (XGBoost and LSTM) and simulate A/B testing.
    """
    try:
        result = backtesting.run_backtesting(symbol)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
