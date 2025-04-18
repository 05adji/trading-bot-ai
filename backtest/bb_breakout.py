def bb_breakout_strategy(df):
    position = 0
    entry_price = 0
    returns = []

    bb_period = 20
    sma = df['close'].rolling(bb_period).mean()
    std = df['close'].rolling(bb_period).std()
    upper = sma + 2 * std
    lower = sma - 2 * std

    for i in range(bb_period, len(df)):
        price = df['close'].iloc[i]

        # Buy breakout
        if price > upper.iloc[i] and position == 0:
            position = 1
            entry_price = price

        # Sell breakdown
        elif price < lower.iloc[i] and position == 1:
            trade_return = (price - entry_price) / entry_price
            returns.append(trade_return)
            position = 0

    # Exit if still holding
    if position == 1:
        final_return = (df['close'].iloc[-1] - entry_price) / entry_price
        returns.append(final_return)

    return returns
 
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
    