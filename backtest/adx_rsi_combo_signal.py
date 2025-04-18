def adx_rsi_combo_signal(df, rsi_buy=30, rsi_sell=70, adx_threshold=25):
    signals = [0] * len(df)
    for i in range(1, len(df)):
        rsi = df['rsi_14'].iloc[i]
        adx = df['adx_14'].iloc[i]

        if rsi < rsi_buy and adx > adx_threshold:
            signals[i] = 1
        elif rsi > rsi_sell and adx > adx_threshold:
            signals[i] = -1
    return signals
