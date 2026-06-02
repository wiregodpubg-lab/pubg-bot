import telebot
from telebot import types
import sqlite3

TOKEN = '8981532484:AAGe0CuTyI5W6THRjcz6SkE5-9ao4Jf-C5Y'
bot = telebot.TeleBot(TOKEN)

# لینک وایرگارد عالی خودت را اینجا جایگذاری کن
MY_VPN_LINK = "vless://..." 

# اتصال به دیتابیس
conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, inviter INTEGER)')
conn.commit()

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    cursor.execute('INSERT OR IGNORE INTO users (id, inviter) VALUES (?, 0)', (user_id,))
    
    args = message.text.split()
    if len(args) > 1:
        inviter_id = args[1]
        if inviter_id.isdigit() and int(inviter_id) != user_id:
            # بررسی کن که قبلا کسی دعوتش نکرده باشه
            cursor.execute('SELECT inviter FROM users WHERE id = ?', (user_id,))
            if cursor.fetchone()[0] == 0:
                cursor.execute('UPDATE users SET inviter = ? WHERE id = ?', (inviter_id, user_id))
                conn.commit()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🚀 دریافت وایرگارد"), types.KeyboardButton("🔗 لینک دعوت من"))
    bot.send_message(message.chat.id, "خوش آمدید! با دعوت ۳ نفر، وایرگارد پرسرعت هدیه بگیر.", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle(message):
    user_id = message.from_user.id
    if message.text == "🔗 لینک دعوت من":
        bot.send_message(message.chat.id, f"🔗 لینک اختصاصی شما:\nhttps://t.me/PUbgNexusX_bot?start={user_id}\n\nبه ۳ نفر بده تا وایرگارد بگیری!")
    
    elif message.text == "🚀 دریافت وایرگارد":
        cursor.execute('SELECT COUNT(*) FROM users WHERE inviter = ?', (user_id,))
        count = cursor.fetchone()[0]
        
        if count >= 3:
            bot.send_message(message.chat.id, f"تبریک! 🎉\nاین هم وایرگارد اختصاصی شما:\n\n`{MY_VPN_LINK}`", parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, f"هنوز به حد نصاب نرسیدی!\nتعداد دعوت‌های فعلی: {count} نفر.\nفقط {3 - count} نفر دیگه دعوت کن.")

bot.infinity_polling()
