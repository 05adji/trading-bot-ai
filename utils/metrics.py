import numpy as np

def sharpe_ratio(returns, risk_free_rate=0.0):
    if len(returns) == 0:
        return 0
    excess_returns = np.array(returns) - risk_free_rate
    return np.mean(excess_returns) / (np.std(excess_returns) + 1e-8)

def max_drawdown(returns):
    if len(returns) == 0:
        return 0
    equity_curve = np.cumprod([1 + r for r in returns])
    peak = np.maximum.accumulate(equity_curve)
    drawdowns = (equity_curve - peak) / peak
    return drawdowns.min()

def winrate(returns):
    if len(returns) == 0:
        return 0
    wins = sum(1 for r in returns if r > 0)
    return wins / len(returns)
