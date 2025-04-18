
# 🤖 Trading Bot AI - Auto Retrain + Telegram Alert (Cloud Deployed)

An intelligent crypto trading bot that retrains itself daily using AI/ML and sends performance reports to Telegram — all fully automated in the cloud.

## 🚀 Features

- ✅ **Daily Auto-Retrain:** XGBoost model retrains every 24 hours on the latest market data
- ✅ **Smart Feature Engineering:** Includes RSI, SMA, Bollinger Bands, ADX, and more
- ✅ **Performance Tracking:** Sharpe ratio, drawdown, winrate computed after each retrain
- ✅ **📬 Telegram Notifications:** Receive real-time updates via Telegram after each retrain
- ✅ **🌩️ Cloud Deployed via Render.com:** Set it once, forget forever

## 🧠 Tech Stack

- **Python 3**
- **XGBoost** for modeling
- **pandas** for data processing
- **Render.com** for cloud automation
- **Telegram Bot API** for alert system

## 🛠️ Deployment Guide

1. **Fork or clone this repo**
2. Add your Binance historical data to `data/btc_15m.csv`
3. Setup a Telegram bot via [@BotFather](https://t.me/BotFather)
4. Deploy to [Render.com](https://render.com) as a Cron Job with:
    - Build command: `pip install -r requirements.txt`
    - Run command: `python retrain_daily.py`
    - Environment Variables:
        - `TELEGRAM_BOT_TOKEN` = `your-bot-token`
        - `TELEGRAM_CHAT_ID` = `your-chat-id`

## 📈 Model Metrics (after retrain)

Example output:
```
✅ Model retrained (2025-04-18 03:00)
Sharpe Ratio: 1.42
Winrate     : 68.2%
Drawdown    : -0.97%
```

## 🧩 Project Roadmap

- [x] Auto retrain model
- [x] Telegram integration
- [x] Cloud deployment
- [ ] Real-time Binance signal execution
- [ ] Backtesting with portfolio simulation
- [ ] Live trading on Binance Testnet
- [ ] Web dashboard analytics

## 👤 Author

Built by [`05adji`](https://github.com/05adji) — a future Blockchain AI Engineer 💻🚀  
_“Automate or evaporate.”_

---

> ⚠️ Use at your own risk. This repo is for educational purposes only and not financial advice.
