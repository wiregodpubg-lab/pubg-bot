import telebot
from telebot import types
import sqlite3

# توکن شما در اینجا قرار دارد
TOKEN = '8981532484:AAG1Z2o1ZJ6QWnRUUpAUz87hbnSwmjBs064'
CHANNEL = "@NexusXTOP"
bot = telebot.TeleBot(TOKEN)

# دیتابیس برای ذخیره تعداد دعوت‌ها
conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS inv_count (id INTEGER PRIMARY KEY, count INTEGER)')
conn.commit()

def is_subscribed(user_id):
    try:
        status = bot.get_chat_member(CHANNEL, user_id).status
        return status in ['member', 'administrator', 'creator']
    except: return False

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    # ثبت دعوت اگر لینک اختصاصی استفاده شده
    if 'inv_' in message.text:
        try:
            inviter_id = int(message.text.split('inv_')[1])
            if inviter_id != user_id:
                cursor.execute('INSERT OR IGNORE INTO inv_count (id, count) VALUES (?, 0)', (inviter_id,))
                cursor.execute('UPDATE inv_count SET count = count + 1 WHERE id = ?', (inviter_id,))
                conn.commit()
        except: pass

    if not is_subscribed(user_id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("عضویت در کانال", url=f"https://t.me/{CHANNEL[1:]}"))
        bot.send_message(user_id, "❌ ابتدا در کانال عضو شو:", reply_markup=markup)
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("وایرگارد پینگ ۲۰🔥", "پنل V2rayNG💫", "DNS مخصوص نت ملی❄️", "openvon👑")
    bot.send_message(user_id, "✅ به ربات Nexus خوش آمدی! یکی را انتخاب کن:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_menu(message):
    user_id = message.from_user.id
    if not is_subscribed(user_id):
        bot.send_message(user_id, "❌ اول عضو کانال شو!")
        return

    options = {
        "وایرگارد پینگ ۲۰🔥": "vless://wg-ping-20-link...",
        "پنل V2rayNG💫": "vless://v2ray-fast-link...",
        "DNS مخصوص نت ملی❄️": "dns://national-net...",
        "openvon👑": "openvpn://config-data..."
    }

    if message.text in options:
        cursor.execute('SELECT count FROM inv_count WHERE id = ?', (user_id,))
        res = cursor.fetchone()
        invites = res[0] if res else 0
        
        if invites >= 3:
            bot.send_message(user_id, f"✅ سرویس {message.text} فعال شد:\n`{options[message.text]}`", parse_mode='Markdown')
        else:
            bot.send_message(user_id, f"⚠️ شما {invites} دعوت داری. برای دریافت {message.text} نیاز به ۳ دعوت داری.\n🔗 لینک تو: https://t.me/NexusX_bot?start=inv_{user_id}")

print("Bot is running...")
bot.infinity_polling()
