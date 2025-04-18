import pandas as pd
import ta

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def compute_bb_width(series, period=20):
    sma = series.rolling(window=period).mean()
    std = series.rolling(window=period).std()
    upper = sma + 2 * std
    lower = sma - 2 * std
    return (upper - lower) / sma

def add_features(df):
    df['return'] = df['close'].pct_change()
    df['ma_20'] = df['close'].rolling(window=20).mean()
    df['ma_50'] = df['close'].rolling(window=50).mean()
    df['rsi_14'] = compute_rsi(df['close'], period=14)
    df['bb_width'] = compute_bb_width(df['close'], period=20)
    df['adx_14'] = ta.trend.adx(df['high'], df['low'], df['close'], window=14)

    df.dropna(inplace=True)  # Hilangin baris awal yang NaN
    return df
