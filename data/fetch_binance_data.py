import ccxt
import pandas as pd
import os

def fetch_binance_ohlcv(symbol='BTC/USDT', timeframe='15m', limit=500):
    exchange = ccxt.binance()
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    
    return df

if __name__ == "__main__":
    df = fetch_binance_ohlcv()
    output_path = os.path.join('data', 'btc_15m.csv')
    df.to_csv(output_path)
    print(f"Data saved to {output_path}")
