# utils/metrics.py
import numpy as np

def calculate_sharpe_ratio(returns, risk_free_rate=0.01):
    excess_returns = returns - risk_free_rate
    return np.mean(excess_returns) / np.std(excess_returns)

def calculate_sortino_ratio(returns, risk_free_rate=0.01):
    downside_returns = returns[returns < 0]
    return (np.mean(returns) - risk_free_rate) / np.std(downside_returns) if len(downside_returns) > 0 else 0

def calculate_drawdown(portfolio_values):
    peak = np.maximum.accumulate(portfolio_values)
    drawdown = (peak - portfolio_values) / peak
    return np.max(drawdown)