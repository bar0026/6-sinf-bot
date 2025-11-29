from flask import Flask, request
import telebot
from telebot import types

# -----------------------------
# BOT TOKEN va WEBHOOK URL
# -----------------------------
TOKEN = "8152274542:AAEJoEr6Snxwu6jtM1skSC9W-YQJEtKadJI"  # Bot tokeningizni shu yerga qo'ying
WEBHOOK_URL = "https://six-sinf-bot.onrender.com/" + TOKEN  # Sizning Render URL + token
# -----------------------------

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# /start komandasi
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    
    # Inline tugmalar yaratish
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("Tugma 1", callback_data="btn1")
    btn2 = types.InlineKeyboardButton("Tugma 2", callback_data="btn2")
    btn3 = types.InlineKeyboardButton("Tugma 3", callback_data="btn3")
    markup.add(btn1, btn2, btn3)
    
    bot.send_message(chat_id, "Salom! Tugmalardan birini tanlang:", reply_markup=markup)

# Inline tugmalarni boshqarish
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "btn1":
        bot.answer_callback_query(call.id, "Siz Tugma 1 ni bosdingiz!")
    elif call.data == "btn2":
        bot.answer_callback_query(call.id, "Siz Tugma 2 ni bosdingiz!")
    elif call.data == "btn3":
        bot.answer_callback_query(call.id, "Siz Tugma 3 ni bosdingiz!")

# Webhook endpoint
@app.route(f"/{TOKEN}", methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

# Flask server start
if __name__ == "__main__":
    # Avval webhookni o‘rnatish
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    
    # Flask server ishga tushishi
    app.run(host="0.0.0.0", port=5000)
