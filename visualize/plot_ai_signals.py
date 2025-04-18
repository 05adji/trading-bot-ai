
import pandas as pd
import matplotlib.pyplot as plt

def plot_ai_signals(df, ai_sig):
    df = df.copy()
    df['signal'] = ai_sig

    plt.figure(figsize=(14, 6))
    plt.plot(df['close'], label='Close Price', alpha=0.5)

    buy_signals = df[df['signal'] == 1]
    sell_signals = df[df['signal'] == -1]

    plt.scatter(buy_signals.index, buy_signals['close'], marker='^', color='green', label='AI Buy', zorder=5)
    plt.scatter(sell_signals.index, sell_signals['close'], marker='v', color='red', label='AI Sell', zorder=5)

    plt.title('AI Signals vs Market')
    plt.xlabel('Time')
    plt.ylabel('Price (USDT)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
