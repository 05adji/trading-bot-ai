def sma_cross_strategy(df):
    position = 0  # 0: no position, 1: long
    entry_price = 0
    returns = []

    for i in range(1, len(df)):
        ma_20_prev = df['ma_20'].iloc[i - 1]
        ma_50_prev = df['ma_50'].iloc[i - 1]
        ma_20_curr = df['ma_20'].iloc[i]
        ma_50_curr = df['ma_50'].iloc[i]
        price = df['close'].iloc[i]

        # Buy Signal
        if ma_20_prev < ma_50_prev and ma_20_curr > ma_50_curr and position == 0:
            position = 1
            entry_price = price

        # Sell Signal
        elif ma_20_prev > ma_50_prev and ma_20_curr < ma_50_curr and position == 1:
            trade_return = (price - entry_price) / entry_price
            returns.append(trade_return)
            position = 0

    # Force exit last position (optional)
    if position == 1:
        final_return = (df['close'].iloc[-1] - entry_price) / entry_price
        returns.append(final_return)

    return returns


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
