import telebot
from telebot import types
from flask import Flask, request
import os

# --- TOKEN va Webhook URL ni Environment Variable orqali oling ---
TOKEN = os.getenv("BOT_TOKEN")  # Render’da BOT_TOKEN qo‘shing
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Render’da WEBHOOK_URL qo‘shing

bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

CHANNEL_ID = "@bsb_chb_javoblari1"  # yoki -1001234567890

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

# --- /start komandasi: ishlayotganini tekshirish uchun ---
@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(msg, "Salom! Bot ishlayapti 😊\n\n/sendpost - kanalga xabar tashlash")

# --- /sendpost komandasi: admin kanalga tugmali post yuboradi ---
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

# --- Flask serverni ishga tushirish ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
