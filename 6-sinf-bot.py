from flask import Flask, request
import telebot
from telebot import types

# -----------------------------
# BOT TOKEN va WEBHOOK URL
# -----------------------------
TOKEN = "8152274542:AAEJoEr6Snxwu6jtM1skSC9W-YQJEtKadJI"  # Bot tokeningizni shu yerga qo'ying
WEBHOOK_URL = "https://six-sinf-bot.onrender.com/" + TOKEN  # Render URL + token
CHANNEL_ID = "@bsb_chsb_javoblari1"  # Kanal username yoki private kanal bo'lsa -100XXXXXXXXX
# -----------------------------

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# /start komandasi (foydalanuvchiga tugmalarni ko'rsatish)
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("Websaytga o'tish", url="https://t.me/bsb_chsb_larbot")
    btn2 = types.InlineKeyboardButton("YouTube kanal", url="https://youtube.com/")
    markup.add(btn1, btn2)
    
    bot.send_message(chat_id, "Salom! Bu xabar inline tugmalar bilan:", reply_markup=markup)

# Kanalga ishga tushganda xabar yuborish
def post_to_channel():
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Chsb javoblari", url="https://t.me/bsb_chsb_larbot")
    btn2 = types.InlineKeyboardButton("Bsb javoblari", url="https://t.me/bsb_chsb_larbot")
    btn3 = types.InlineKeyboardButton("Botga o'tish", url="https://t.me/bsb_chsb_larbot")
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    
    bot.send_message(CHANNEL_ID, 
    """✅ Barcha Fanlardan BSB va CHSB
    javoblari yetib kelmoqda endi yana 
    qulay BOTdan javoblarini topishingiz 
    mumkin ✅👇

    Botdan Toʻliq foydalanish uchun 
    kanallarga obuna boʻlish kerak 🛑
    ⏬⏬⏬⏬⏬⏬⏬⏬⏬⏬""", reply_markup=markup)

# Webhook endpoint
@app.route(f"/{TOKEN}", methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

# Flask server ishga tushishi
if __name__ == "__main__":
    # Avval webhookni o‘rnatish
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    
    # Bot ishga tushganda kanalga xabar yuborish
    post_to_channel()
    
    # Flask server ishga tushishi
    app.run(host="0.0.0.0", port=5000)
