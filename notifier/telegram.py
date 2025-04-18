
import requests

def send_telegram_message(message):
    token = '7938884765:AAE5m1kCYAPTE5ZFzLxlGKZR0RsWH1LdNMI'
    chat_id = '5088758631'
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("✅ Notifikasi Telegram terkirim.")
    else:
        print("⚠️ Gagal kirim notifikasi:", response.text)
