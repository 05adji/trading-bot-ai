def sma_cross_signal(df):
    signals = [0] * len(df)
    for i in range(1, len(df)):
        ma20_prev = df['ma_20'].iloc[i - 1]
        ma50_prev = df['ma_50'].iloc[i - 1]
        ma20_curr = df['ma_20'].iloc[i]
        ma50_curr = df['ma_50'].iloc[i]

        if ma20_prev < ma50_prev and ma20_curr > ma50_curr:
            signals[i] = 1  # BUY
        elif ma20_prev > ma50_prev and ma20_curr < ma50_curr:
            signals[i] = -1  # SELL
    return signals
