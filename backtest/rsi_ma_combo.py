def rsi_ma_combo_strategy(df, rsi_buy=30, rsi_sell=70):
    position = 0
    entry_price = 0
    returns = []

    for i in range(1, len(df)):
        rsi = df['rsi_14'].iloc[i]
        ma20 = df['ma_20'].iloc[i]
        ma50 = df['ma_50'].iloc[i]
        price = df['close'].iloc[i]

        # Buy: RSI < 30 + MA20 > MA50 (trend naik)
        if rsi < rsi_buy and ma20 > ma50 and position == 0:
            position = 1
            entry_price = price

        # Sell: RSI > 70
        elif rsi > rsi_sell and position == 1:
            trade_return = (price - entry_price) / entry_price
            returns.append(trade_return)
            position = 0

    # Exit posisi jika masih megang
    if position == 1:
        final_return = (df['close'].iloc[-1] - entry_price) / entry_price
        returns.append(final_return)

    return returns
