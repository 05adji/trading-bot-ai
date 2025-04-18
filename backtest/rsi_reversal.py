def rsi_reversal_strategy(df, rsi_buy=30, rsi_sell=70):
    position = 0
    entry_price = 0
    returns = []

    for i in range(1, len(df)):
        rsi = df['rsi_14'].iloc[i]
        price = df['close'].iloc[i]

        # Buy signal
        if rsi < rsi_buy and position == 0:
            position = 1
            entry_price = price

        # Sell signal
        elif rsi > rsi_sell and position == 1:
            trade_return = (price - entry_price) / entry_price
            returns.append(trade_return)
            position = 0

    # Optional: exit open position
    if position == 1:
        final_return = (df['close'].iloc[-1] - entry_price) / entry_price
        returns.append(final_return)

    return returns

def rsi_reversal_signal(df, rsi_buy=30, rsi_sell=70):
    signals = [0] * len(df)
    for i in range(1, len(df)):
        rsi = df['rsi_14'].iloc[i]
        if rsi < rsi_buy:
            signals[i] = 1
        elif rsi > rsi_sell:
            signals[i] = -1
    return signals