
import pandas as pd
import os

def log_ai_signals(df, ai_sig, output_path='logs/ai_signals.csv'):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    df = df.copy()
    df['signal'] = ai_sig
    df = df[df['signal'] != 0]  # Only log Buy/Sell

    df['action'] = df['signal'].map({1: 'BUY', -1: 'SELL'})
    df['price'] = df['close']
    df = df[['action', 'price']]
    df.index.name = 'timestamp'
    df.to_csv(output_path)
    print(f'✅ AI signals saved to {output_path}')

def log_voting_signals(df, final_sig, output_path='logs/voting_signals.csv'):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    df = df.copy()
    df['signal'] = final_sig
    df = df[df['signal'] != 0]  # Only log Buy/Sell

    df['action'] = df['signal'].map({1: 'BUY', -1: 'SELL'})
    df['price'] = df['close']
    df = df[['action', 'price']]
    df.index.name = 'timestamp'
    df.to_csv(output_path)
    print(f'✅ Voting signals saved to {output_path}')
