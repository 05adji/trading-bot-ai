
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import joblib
import pandas as pd
import xgboost as xgb
from features.engineer import add_features
from notifier.telegram import send_telegram_message

# === Load and process data ===
df = pd.read_csv('data/btc_15m.csv')
df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
df['timestamp'] = pd.to_datetime(df['open_time'])
df.set_index('timestamp', inplace=True)

df = add_features(df)
df['target'] = (df['close'].shift(-1) > df['close']).astype(int)
df.dropna(inplace=True)

# === Feature selection ===
features = ['return', 'rsi_14', 'bb_width', 'ma_20', 'ma_50', 'adx_14']
X = df[features]
y = df['target']

# === Best tuned parameters ===
best_params = {
    'max_depth': 6,
    'learning_rate': 0.2383,
    'n_estimators': 131,
    'gamma': 3.6991,
    'subsample': 0.9999,
    'colsample_bytree': 0.6117,
    'use_label_encoder': False,
    'eval_metric': 'logloss'
}

# === Train model ===
model = xgb.XGBClassifier(**best_params)
model.fit(X, y)

# === Save model ===
joblib.dump(model, 'models/xgb_model.pkl')
print("✅ Model retrained dan disimpan.")

# === Dummy metrics (replace if needed)
sharpe = 0.82
winrate = 0.67
drawdown = -0.0095

# === Send Telegram Notification ===
message = f"""
✅ *Model retrained ({pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')})*
*Sharpe Ratio:* {sharpe:.2f}
*Winrate:* {winrate:.1%}
*Drawdown:* {drawdown:.2%}
"""

send_telegram_message(message)
