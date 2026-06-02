import telebot
from telebot import types
import sqlite3
import random

TOKEN = '8981532484:AAGe0CuTyI5W6THRjcz6SkE5-9ao4Jf-C5Y'
CHANNEL_ID = "@NexusXTOP"
bot = telebot.TeleBot(TOKEN)

conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, inviter INTEGER)')
conn.commit()

def check_membership(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except: return False

@bot.message_handler(commands=['start'])
def start(message):
    if not check_membership(message.from_user.id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✅ عضویت در کانال", url="https://t.me/NexusXTOP"))
        bot.send_message(message.chat.id, "⚠️ ابتدا در کانال عضو شوید.", reply_markup=markup)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add("🔥 وایرگارد", "🌐 پنل V2Ray", "🎁 جوایز مرحله‌ای", "📊 لیدربورد", "🎡 چرخونه شانس", "👤 پروفایل")
        bot.send_message(message.chat.id, "خوش آمدید!", reply_markup=markup)

bot.infinity_polling()
