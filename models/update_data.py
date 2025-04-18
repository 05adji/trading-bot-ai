
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from data.fetch_binance_data import fetch_binance_ohlcv

# Fetch 7 days of 15-minute candles = 7 * 24 * 4 = 672 candles
df = fetch_binance_ohlcv(
    symbol='BTC/USDT',
    timeframe='15m',
    limit=672
)

# Save to CSV
df.to_csv('data/btc_15m.csv')
print('✅ Data terbaru berhasil di-fetch dan disimpan ke data/btc_15m.csv')
