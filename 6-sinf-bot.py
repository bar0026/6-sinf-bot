import telebot
from telebot import types
from flask import Flask, request
import os

TOKEN = os.getenv("8152274542:AAEJoEr6Snxwu6jtM1skSC9W-YQJEtKadJI")
bot = telebot.TeleBot(TOKEN, threaded=False)

app = Flask(__name__)

# Render domening: https://kod.onrender.com
WEBHOOK_URL = os.getenv("https://six-sinf-bot.onrender.com")

CHANNEL_ID = "@bsb_chb_javoblari1"   # yoki -100...

# --- Inline tugmali kanal post funksiyasi ---
def send_post():
    markup = types.InlineKeyboardMarkup()

    btn1 = types.InlineKeyboardButton("Obuna bo‘lish", url="https://t.me/bsb_chsb_larbot")
    btn2 = types.InlineKeyboardButton("Admin bilan aloqa", url="https://t.me/bsb_chsb_larbot")

    markup.add(btn1, btn2)

    bot.send_message(
        CHANNEL_ID,
        "Bu kanal uchun test post 😊",
        reply_markup=markup
    )

# --- Webhook handler ---
@app.route("/", methods=['POST'])
def webhook():
    json_data = request.stream.read().decode("utf-8")
    update = telebot.types.Update.de_json(json_data)
    bot.process_new_updates([update])
    return "OK", 200


# /start komandasi
@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(msg, "Webhook ishlayapti 😊\n\n/sendpost - kanalga xabar tashlash")


# Admin tomonidan kanalga tugmali post tashlash
@bot.message_handler(commands=['sendpost'])
def admin_send(msg):
    send_post()
    bot.reply_to(msg, "Kanalga yuborildi!")


# --- Webhook o‘rnatish ---
@app.route("/setwebhook", methods=['GET'])
def set_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    return "Webhook o‘rnatildi!", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
