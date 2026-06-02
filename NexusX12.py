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
cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, inviter INTEGER)')
conn.commit()

def check_membership(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except: return False

def get_count(user_id):
    cursor.execute('SELECT COUNT(*) FROM users WHERE inviter = ?', (user_id,))
    return cursor.fetchone()[0]

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    # ثبت دعوت کننده (اگر آیدی داشت)
    if 'inv_' in message.text:
        inviter_id = int(message.text.split('inv_')[1])
        if inviter_id != user_id:
            cursor.execute('INSERT OR IGNORE INTO users (id, inviter) VALUES (?, ?)', (user_id, inviter_id))
            conn.commit()
    
    if not check_membership(user_id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✅ عضویت در کانال", url="https://t.me/NexusXTOP"))
        markup.add(types.InlineKeyboardButton("🔄 عضو شدم (تایید)", callback_data="check_join"))
        bot.send_message(message.chat.id, "⚠️ **برای استفاده از ربات باید در کانال ما عضو باشید:**\n@NexusXTOP", reply_markup=markup)
    else:
        show_menu(message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def check_join(call):
    if check_membership(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ تایید شد!")
        show_menu(call.message.chat.id)
    else:
        bot.answer_callback_query(call.id, "❌ هنوز عضو نشدید!", show_alert=True)

def show_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("🔥 وایرگارد", "🌐 پنل V2Ray", "⚡️ دی‌ان‌اس پینگ ۲۰", "📊 لیدربورد", "👤 پروفایل")
    bot.send_message(chat_id, "✅ به منوی اصلی خوش آمدید، از دکمه‌های زیر استفاده کنید:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_menu(message):
    user_id = message.from_user.id
    if not check_membership(user_id): return start(message)
    
    count = get_count(user_id)
    
    if message.text in ["🔥 وایرگارد", "🌐 پنل V2Ray", "⚡️ دی‌ان‌اس پینگ ۲۰"]:
        if count >= 3:
            bot.send_message(message.chat.id, f"🎁 تبریک! اینم سرویس درخواستی شما:\n`لینک_اختصاصی_شما`", parse_mode='Markdown')
        else:
            needed = 3 - count
            bot.send_message(message.chat.id, f"❌ **دسترسی محدود!**\nشما {count} نفر دعوت کردید.\n\nبرای دریافت این سرویس باید **{needed} نفر دیگه** رو دعوت کنید.\n\nلینک اختصاصی خودتون رو برای دوستانتون بفرستید تا عضو بشن و امتیازتون کامل شه!", parse_mode='Markdown')
    
    elif message.text == "👤 پروفایل":
        bot.send_message(message.chat.id, f"👤 **اطلاعات شما:**\nتعداد دعوت موفق: {count}\n\n🔗 لینک دعوت شما:\nhttps://t.me/PUbgNexusX_bot?start=inv_{user_id}")

    elif message.text == "📊 لیدربورد":
        cursor.execute('SELECT inviter, COUNT(*) as c FROM users WHERE inviter != 0 GROUP BY inviter ORDER BY c DESC LIMIT 5')
        top = cursor.fetchall()
        text = "🏆 **لیدربورد خفن‌ترین دعوت‌کنندگان:**\n\n" + "\n".join([f"{i+1}. کاربر {u[0]} با {u[1]} دعوت" for i, u in enumerate(top)])
        bot.send_message(message.chat.id, text)

bot.infinity_polling()
