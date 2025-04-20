
import os
import pandas as pd
from features.engineer import add_features
from backtest.sma_cross_signal import sma_cross_signal
from backtest.rsi_reversal_signal import rsi_reversal_signal
from backtest.bb_breakout_signal import bb_breakout_signal
from models.xgb_predictor import predict_proba_with_model
from strategy_engine.voting_engine import majority_vote
from binance.order_executor import execute_order
from utils.metrics import sharpe_ratio, max_drawdown, winrate
from notifier.telegram import send_telegram_message

# === Load data and apply features ===
df = pd.read_csv('data/btc_15m.csv')
df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
df['timestamp'] = pd.to_datetime(df['open_time'])
df = add_features(df)

# === Generate signals from strategies ===
sma_sig = sma_cross_signal(df)
rsi_sig = rsi_reversal_signal(df)
bb_sig  = bb_breakout_signal(df)
ai_sig  = predict_proba_with_model(df)
ai_sig_final = [1 if p > 0.6 else -1 if p < 0.4 else 0 for p in ai_sig]

# === Combine all into final vote ===
signals = majority_vote([sma_sig, rsi_sig, bb_sig, ai_sig_final])

# === Get the latest signal only ===
latest_signal = signals[-1]
print(f"📤 Latest final signal: {latest_signal}")

# === Execute order if any ===
execute_order(latest_signal)

# === Evaluate backtest performance
returns = []
position = 0
entry = 0
for i in range(len(signals)):
    if signals[i] == 1 and position == 0:
        entry = df['close'].iloc[i]
        position = 1
    elif signals[i] == -1 and position == 1:
        ret = (df['close'].iloc[i] - entry) / entry
        returns.append(ret)
        position = 0
if position == 1:
    returns.append((df['close'].iloc[-1] - entry) / entry)

# === Print & Send Result
msg = f"""🚨 AI Trading Bot Report ({df['timestamp'].iloc[-1]})
Signal: {'BUY' if latest_signal==1 else 'SELL' if latest_signal==-1 else 'HOLD'}
Trades: {len(returns)}
Sharpe: {sharpe_ratio(returns):.2f}
Winrate: {winrate(returns):.2%}
Drawdown: {max_drawdown(returns):.2%}
"""
send_telegram_message(msg)
