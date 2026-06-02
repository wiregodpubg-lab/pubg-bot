import telebot
from telebot import types
import sqlite3
import random

TOKEN = '8981532484:AAGe0CuTyI5W6THRjcz6SkE5-9ao4Jf-C5Y'
CHANNEL_ID = "@NexusXTOP"
bot = telebot.TeleBot(TOKEN)

# دیتابیس
conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, inviter INTEGER, points INTEGER DEFAULT 0, level INTEGER DEFAULT 1)')
conn.commit()

def check_membership(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except: return False

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    args = message.text.split()
    inviter = int(args[1].replace("inv_", "")) if len(args) > 1 and "inv_" in args[1] else 0
    
    cursor.execute('INSERT OR IGNORE INTO users (id, inviter) VALUES (?, ?)', (user_id, inviter))
    conn.commit()

    if not check_membership(user_id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✅ عضویت در کانال", url="https://t.me/NexusXTOP"))
        bot.send_message(message.chat.id, "❌ ابتدا عضو کانال شوید.", reply_markup=markup)
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("🎁 جوایز مرحله‌ای", "📊 لیدربورد", "🎡 چرخونه شانس", "👤 پروفایل")
    bot.send_message(message.chat.id, "خوش آمدید! از منو استفاده کنید.", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_menu(message):
    user_id = message.from_user.id
    
    if message.text == "📊 لیدربورد":
        cursor.execute('SELECT id, COUNT(*) as count FROM users GROUP BY inviter ORDER BY count DESC LIMIT 5')
        top = cursor.fetchall()
        text = "🏆 **لیدربورد دعوت‌کنندگان:**\n\n" + "\n".join([f"{i+1}. کاربر {u[0]}: {u[1]} دعوت" for i, u in enumerate(top)])
        bot.send_message(message.chat.id, text, parse_mode='Markdown')

    elif message.text == "🎡 چرخونه شانس":
        reward = random.choice(["+1 دعوت", "هیچ", "+2 دعوت", "شانس مجدد"])
        bot.send_message(message.chat.id, f"🎡 نتیجه چرخونه: {reward}")

    elif message.text == "🎁 جوایز مرحله‌ای":
        cursor.execute('SELECT COUNT(*) FROM users WHERE inviter = ?', (user_id,))
        count = cursor.fetchone()[0]
        msg = f"شما {count} دعوت دارید.\nجوایز: ۳ دعوت (وایرگارد)، ۵ دعوت (پنل)، ۱۰ دعوت (ویژه)، ۲۰ دعوت (اکانت رایگان)."
        bot.send_message(message.chat.id, msg)

    elif message.text == "👤 پروفایل":
        cursor.execute('SELECT COUNT(*) FROM users WHERE inviter = ?', (user_id,))
        count = cursor.fetchone()[0]
        level = (count // 5) + 1
        bot.send_message(message.chat.id, f"👤 پروفایل\nتعداد دعوت: {count}\nسطح فعلی: {level}\nلینک: https://t.me/PUbgNexusX_bot?start=inv_{user_id}")

bot.infinity_polling()
