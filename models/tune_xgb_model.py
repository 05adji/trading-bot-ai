
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import optuna
import xgboost as xgb
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from features.engineer import add_features

def objective(trial):
    df = pd.read_csv('data/btc_15m.csv', index_col='timestamp', parse_dates=True)
    df = add_features(df)
    df['target'] = (df['close'].shift(-1) > df['close']).astype(int)
    df.dropna(inplace=True)

    features = ['return', 'rsi_14', 'bb_width', 'ma_20', 'ma_50', 'adx_14']
    X = df[features]
    y = df['target']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    params = {
        'verbosity': 0,
        'objective': 'binary:logistic',
        'eval_metric': 'logloss',
        'max_depth': trial.suggest_int('max_depth', 3, 10),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
        'n_estimators': trial.suggest_int('n_estimators', 50, 300),
        'gamma': trial.suggest_float('gamma', 0, 5),
        'subsample': trial.suggest_float('subsample', 0.5, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.5, 1.0)
    }

    model = xgb.XGBClassifier(**params)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    return acc

if __name__ == '__main__':
    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=50)

    print("Best trial:")
    print(study.best_trial)

    best_params = study.best_trial.params
    model = xgb.XGBClassifier(
        **best_params,
        use_label_encoder=False,
        eval_metric='logloss'
    )

    # Retrain model on full dataset
    df = pd.read_csv('data/btc_15m.csv', index_col='timestamp', parse_dates=True)
    df = add_features(df)
    df['target'] = (df['close'].shift(-1) > df['close']).astype(int)
    df.dropna(inplace=True)

    features = ['return', 'rsi_14', 'bb_width', 'ma_20', 'ma_50', 'adx_14']
    X = df[features]
    y = df['target']
    model.fit(X, y)

    # Save model
    joblib.dump(model, 'models/xgb_model.pkl')
    print("✅ Model saved to models/xgb_model.pkl")
