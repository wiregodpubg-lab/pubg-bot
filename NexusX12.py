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
        markup.add(types.InlineKeyboardButton("🔄 تایید عضویت", callback_data="check_join"))
        bot.send_message(message.chat.id, "⚠️ **ابتدا در کانال ما عضو شوید تا ربات فعال شود.**", reply_markup=markup)
    else:
        show_main_menu(message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def callback_join(call):
    if check_membership(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ عضویت تایید شد!")
        show_main_menu(call.message.chat.id)
    else:
        bot.answer_callback_query(call.id, "❌ هنوز عضو نشدید!", show_alert=True)

def show_main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("🔥 وایرگارد", "🌐 پنل V2Ray", "🎁 جوایز مرحله‌ای", "📊 لیدربورد", "🎡 چرخونه شانس", "👤 پروفایل")
    bot.send_message(chat_id, "✅ عضویت تایید شد!\nبه منوی اصلی خوش آمدید:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_menu(message):
    if not check_membership(message.from_user.id):
        return start(message)

    user_id = message.from_user.id
    cursor.execute('SELECT COUNT(*) FROM users WHERE inviter = ?', (user_id,))
    count = cursor.fetchone()[0]

    if message.text in ["🔥 وایرگارد", "🌐 پنل V2Ray"]:
        if count >= 3:
            bot.send_message(message.chat.id, f"✅ سرویس شما آماده است:\n`لینک_اختصاصی_سرویس`", parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, f"❌ برای دسترسی به این سرویس باید ۳ نفر را دعوت کنید.\nتعداد دعوت شما: {count}")
    
    elif message.text == "📊 لیدربورد":
        cursor.execute('SELECT inviter, COUNT(*) as count FROM users WHERE inviter != 0 GROUP BY inviter ORDER BY count DESC LIMIT 5')
        top = cursor.fetchall()
        text = "🏆 **لیدربورد دعوت‌کنندگان:**\n\n" + "\n".join([f"{i+1}. کاربر {u[0]}: {u[1]} دعوت" for i, u in enumerate(top)])
        bot.send_message(message.chat.id, text, parse_mode='Markdown')

    elif message.text == "🎡 چرخونه شانس":
        bot.send_message(message.chat.id, f"🎡 نتیجه چرخونه: {random.choice(['+1 دعوت', 'شانس مجدد', 'هیچ'])}")

    elif message.text == "👤 پروفایل":
        bot.send_message(message.chat.id, f"👤 پروفایل شما\nتعداد دعوت: {count}\nلینک دعوت:\nhttps://t.me/PUbgNexusX_bot?start=inv_{user_id}")

    elif message.text == "🎁 جوایز مرحله‌ای":
        bot.send_message(message.chat.id, "🎁 جوایز:\n۳ دعوت: دریافت سرویس‌های V2Ray و وایرگارد")

bot.infinity_polling()
