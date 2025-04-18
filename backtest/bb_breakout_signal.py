def bb_breakout_signal(df, window=20):
    signals = [0] * len(df)
    sma = df['close'].rolling(window).mean()
    std = df['close'].rolling(window).std()
    upper = sma + 2 * std
    lower = sma - 2 * std

    for i in range(window, len(df)):
        price = df['close'].iloc[i]
        if price > upper.iloc[i]:
            signals[i] = 1  # Buy breakout
        elif price < lower.iloc[i]:
            signals[i] = -1  # Sell breakdown
    return signals
