import os
from flask import Flask, request
import telebot

BOT_TOKEN = "8152274542:AAEJoEr6Snxwu6jtM1skSC9W-YQJEtKadJI"
WEBHOOK_URL = "https://six-sinf-bot.onrender.com"   # ❗ Render linkni shu yerga yozasiz

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# --- Webhook route ---
@app.route('/webhook', methods=['POST'])
def webhook():
    json_data = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_data)
    bot.process_new_updates([update])
    return "OK", 200

# --- start ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! Bot webhok bilan ishlayapti 🚀")

# --- Health check ---
@app.route('/', methods=['GET'])
def home():
    return "Bot ishlayapti!", 200


# 🔥🔥🔥 MUHIM QISM — WEBHOOKNI KODDA O‘RNATISH 🔥🔥🔥
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL)    # <<< Webhook shu yerda o‘rnatiladi


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
