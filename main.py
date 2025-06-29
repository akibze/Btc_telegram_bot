import os
import asyncio
import logging
import requests
from flask import Flask
from threading import Thread
from telegram import Bot
from telegram.constants import ParseMode

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
PRICE_URL = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
DELAY = 60

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TELEGRAM_TOKEN)

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ BTC Telegram Bot is Alive!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    Thread(target=run_flask).start()

async def fetch_price():
    try:
        res = requests.get(PRICE_URL)
        res.raise_for_status()
        return float(res.json()['price'])
    except Exception as e:
        await bot.send_message(chat_id=CHAT_ID, text=f"⚠️ Error: {e}")
        return None

async def price_loop():
    while True:
        price = await fetch_price()
        if price:
            msg = f"💰 *BTC/USDT Price:*\n`{price:.2f}` USD"
            await bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode=ParseMode.MARKDOWN)
        await asyncio.sleep(DELAY)

if __name__ == '__main__':
    keep_alive()
    asyncio.run(price_loop())
