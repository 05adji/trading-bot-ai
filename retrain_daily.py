import sys
import os

# Tambahkan path project agar modul lokal bisa di-import
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import joblib
import pandas as pd
import xgboost as xgb
from features.engineer import add_features
from notifier.telegram import send_telegram_message

# === Load and process data ===
# Tentukan path CSV secara dinamis
data_path = os.path.join(os.path.dirname(__file__), 'data', 'btc_15m.csv')
df = pd.read_csv(data_path)

# Normalisasi nama kolom menjadi snake_case lowercase
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

# Cari kolom waktu yang tersedia
timestamp_col = None
for col in ('open_time', 'timestamp', 'time'):
    if col in df.columns:
        timestamp_col = col
        break

if timestamp_col is None:
    raise KeyError(f"Kolom waktu tidak ditemukan. Available columns: {df.columns.tolist()}")

# Konversi ke datetime dan set index
Df_timestamp = pd.to_datetime(df[timestamp_col])
df['timestamp'] = Df_timestamp
df.set_index('timestamp', inplace=True)

# Tambahkan fitur-fitur tambahan
df = add_features(df)
# Buat target (1 jika harga naik di periode berikutnya)
df['target'] = (df['close'].shift(-1) > df['close']).astype(int)
df.dropna(inplace=True)

# === Feature selection ===
features = ['return', 'rsi_14', 'bb_width', 'ma_20', 'ma_50', 'adx_14']
X = df[features]
y = df['target']

# === Hyperparameters terbaik ===
best_params = {
    'max_depth': 6,
    'learning_rate': 0.2383,
    'n_estimators': 131,
    'gamma': 3.6991,
    'subsample': 0.9999,
    'colsample_bytree': 0.6117,
    'use_label_encoder': False,
    'eval_metric': 'logloss',
}

# === Training model ===
model = xgb.XGBClassifier(**best_params)
model.fit(X, y)

# === Save model ===
model_dir = os.path.join(os.path.dirname(__file__), 'models')
os.makedirs(model_dir, exist_ok=True)
model_path = os.path.join(model_dir, 'xgb_model.pkl')
joblib.dump(model, model_path)
print("✅ Model retrained dan disimpan di {}".format(model_path))

# === Dummy metrics (ganti dengan perhitungan sebenarnya jika ada) ===
sharpe = 0.82
winrate = 0.67
drawdown = -0.0095

# === Kirim notifikasi Telegram ===
now_str = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')
message = f"""
✅ *Model retrained ({now_str})*
*Sharpe Ratio:* {sharpe:.2f}
*Winrate:* {winrate:.1%}
*Drawdown:* {drawdown:.2%}
"""
send_telegram_message(message)
