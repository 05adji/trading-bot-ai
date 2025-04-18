def rsi_reversal_signal(df, rsi_buy=30, rsi_sell=70):
    signals = [0] * len(df)
    for i in range(1, len(df)):
        rsi = df['rsi_14'].iloc[i]
        if rsi < rsi_buy:
            signals[i] = 1
        elif rsi > rsi_sell:
            signals[i] = -1
    return signals
