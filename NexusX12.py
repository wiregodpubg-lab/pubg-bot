import telebot
from telebot import types
import sqlite3

TOKEN = '8981532484:AAGe0CuTyI5W6THRjcz6SkE5-9ao4Jf-C5Y'
CHANNEL_ID = "@NexusXTOP"  # آیدی کانال شما
bot = telebot.TeleBot(TOKEN)

# دیتابیس برای ذخیره دعوت‌ها
conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, inviter INTEGER)')
conn.commit()

def is_member(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    # ثبت کاربر
    cursor.execute('INSERT OR IGNORE INTO users (id, inviter) VALUES (?, 0)', (user_id,))
    
    # ثبت معرف
    args = message.text.split()
    if len(args) > 1 and "inv_" in args[1]:
        inviter_id = args[1].replace("inv_", "")
        if inviter_id.isdigit() and int(inviter_id) != user_id:
            cursor.execute('UPDATE users SET inviter = ? WHERE id = ?', (inviter_id, user_id))
            conn.commit()

    # دکمه‌های کیبورد پایین صفحه
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(types.KeyboardButton("پنل وایرگارد ورود به گیم"), types.KeyboardButton("ویتوری پینگ پایین💙💙"))
    bot.send_message(message.chat.id, "خوش آمدید! برای استفاده از امکانات از منو انتخاب کنید.", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_menu(message):
    user_id = message.from_user.id
    
    # چک کردن عضویت در کانال (شیشه‌ای)
    if not is_member(user_id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("عضویت در کانال NexusXTOP", url="https://t.me/NexusXTOP"))
        bot.send_message(message.chat.id, "⚠️ برای استفاده از ربات ابتدا باید در کانال ما عضو باشید:", reply_markup=markup)
        return

    # سیستم امتیازدهی
    cursor.execute('SELECT COUNT(*) FROM users WHERE inviter = ?', (user_id,))
    count = cursor.fetchone()[0]

    if message.text == "پنل وایرگارد ورود به گیم":
        if count >= 3:
            # وایرگارد بسیار خفن
            bot.send_message(message.chat.id, "✅ تبریک! وایرگارد اختصاصی شما:\n`vless://...خفن...`", parse_mode='Markdown')
        else:
            response = (
                f"کاربر عزیز، برای استفاده از این دکمه نیاز به ۳ امتیاز دارید.\n"
                f"🟢 امتیاز فعلی شما: {count}\n"
                f"🌐 لینک مخصوص شما برای دعوت:\nhttps://t.me/PUbgNexusX_bot?start=inv_{user_id}"
            )
            bot.send_message(message.chat.id, response)

bot.infinity_polling()
