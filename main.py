import sys
import os
from pathlib import Path

import pandas as pd
import joblib
from features.engineer import add_features
from backtest.sma_cross_signal import sma_cross_signal
from backtest.rsi_reversal_signal import rsi_reversal_signal
from backtest.bb_breakout_signal import bb_breakout_signal
from backtest.adx_rsi_combo_signal import adx_rsi_combo_signal
from strategy_engine.voting_engine import majority_vote
from utils.metrics import sharpe_ratio, max_drawdown, winrate
from visualize.plot_ai_signals import plot_ai_signals
from logger.signal_logger import log_ai_signals, log_voting_signals

# 1. Tentukan path data secara dinamis dari lokasi file ini
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / 'data' / 'btc_15m.csv'
if not DATA_FILE.exists():
    sys.exit(f'Error: Data file tidak ditemukan di {DATA_FILE}')

# 2. Baca CSV dan parse tanggal kolom 'open_time' langsung
df = pd.read_csv(DATA_FILE)
# 3. Standardisasi nama kolom: strip, lowercase, spasi→underscore
df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]

# 4. Pastikan kolom timestamp ada; kalau perlu, parse open_time
if 'open_time' in df.columns:
    # Kalau open_time berupa UNIX ms, tambahkan unit='ms'
    df['timestamp'] = pd.to_datetime(df['open_time'])
elif 'timestamp' in df.columns:
    df['timestamp'] = pd.to_datetime(df['timestamp'])
else:
    raise KeyError("Gagal: nggak ada kolom 'open_time' atau 'timestamp' di CSV")

# 5. Set index ke timestamp dan sort (biar EDA & backtest rapi)
df.set_index('timestamp', inplace=True)
df.sort_index(inplace=True)

# 6. Tambah fitur, hitung sinyal, dan load model seperti sebelumnya
df = add_features(df)

sma_sig = sma_cross_signal(df)
rsi_sig = rsi_reversal_signal(df)
bb_sig  = bb_breakout_signal(df)
adx_sig = adx_rsi_combo_signal(df)

model = joblib.load(BASE_DIR / 'models' / 'xgb_model.pkl')
X = df[['return','rsi_14','bb_width','ma_20','ma_50','adx_14']]
proba = model.predict_proba(X)[:,1]
ai_sig = [1 if p > 0.7 else -1 if p < 0.3 else 0 for p in proba]

signals = majority_vote([sma_sig, rsi_sig, bb_sig, adx_sig, ai_sig])

# 7. Fungsi backtest dari sinyal
def backtest_from_signals(df, signals):
    position, entry_price, returns = 0, 0, []
    for i, sig in enumerate(signals):
        price = df['close'].iloc[i]
        if sig==1 and position==0:
            position, entry_price = 1, price
        elif sig==-1 and position==1:
            returns.append((price-entry_price)/entry_price)
            position = 0
    if position==1:
        returns.append((df['close'].iloc[-1]-entry_price)/entry_price)
    return returns

voting_returns = backtest_from_signals(df, signals)

# 8. Cetak metrik
print("\n=== AI-ENHANCED VOTING STRATEGY ===")
print(f"Jumlah trade : {len(voting_returns)}")
print(f"Sharpe       : {sharpe_ratio(voting_returns):.2f}")
print(f"Drawdown     : {max_drawdown(voting_returns):.2%}")
print(f"Winrate      : {winrate(voting_returns):.2%}")

# 9. Visualisasi & logging
plot_ai_signals(df, ai_sig)
log_ai_signals(df, ai_sig)
log_voting_signals(df, signals)
