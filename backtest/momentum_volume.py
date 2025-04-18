def momentum_volume_strategy(df, window=20, volume_multiplier=1.5):
    position = 0
    entry_price = 0
    returns = []

    for i in range(window, len(df)):
        high_window = df['high'].iloc[i-window:i].max()
        low_window = df['low'].iloc[i-window:i].min()
        avg_vol = df['volume'].iloc[i-window:i].mean()

        price = df['close'].iloc[i]
        volume = df['volume'].iloc[i]

        # Entry breakout with volume confirmation
        if price > high_window and volume > avg_vol * volume_multiplier and position == 0:
            position = 1
            entry_price = price

        # Exit breakdown
        elif price < low_window and position == 1:
            trade_return = (price - entry_price) / entry_price
            returns.append(trade_return)
            position = 0

    # Exit if still holding
    if position == 1:
        final_return = (df['close'].iloc[-1] - entry_price) / entry_price
        returns.append(final_return)

    return returns
