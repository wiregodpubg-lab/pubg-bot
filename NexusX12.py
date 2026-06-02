import telebot
from telebot import types
import sqlite3

TOKEN = '8981532484:AAGe0CuTyI5W6THRjcz6SkE5-9ao4Jf-C5Y'
CHANNEL_ID = "@NexusXTOP"
bot = telebot.TeleBot(TOKEN)

# دیتابیس برای ذخیره دعوت‌ها
conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, inviter INTEGER)')
conn.commit()

# لیست سرویس‌های شما (اینجا لینک‌های واقعی خودت را بگذار)
WIREGUARD_LINK = "vless://your-wireguard-config-here"
V2RAY_PANEL_LINK = "https://your-panel-url.com/link"

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
        bot.send_message(message.chat.id, "❌ برای استفاده، ابتدا عضو کانال شو و دوباره /start بزن.", reply_markup=markup)
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add("🔥 وایرگارد پینگ پایین", "🌐 پنل اختصاصی V2Ray", "👤 پروفایل و لینک دعوت")
    bot.send_message(message.chat.id, "خوش آمدید! یکی از سرویس‌ها را انتخاب کن (نیاز به ۳ دعوت):", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_menu(message):
    user_id = message.from_user.id
    cursor.execute('SELECT COUNT(*) FROM users WHERE inviter = ?', (user_id,))
    count = cursor.fetchone()[0]

    if message.text in ["🔥 وایرگارد پینگ پایین", "🌐 پنل اختصاصی V2Ray"]:
        if count >= 3:
            link = WIREGUARD_LINK if "وایرگارد" in message.text else V2RAY_PANEL_LINK
            bot.send_message(message.chat.id, f"✅ **سرویس درخواستی شما:**\n\n`{link}`\n\nنوش جان!", parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, f"⚠️ **دسترسی محدود!**\n\nشما {count} نفر دعوت کردید. برای دریافت، باید ۳ نفر دعوت کنید.\n🔗 لینک اختصاصی:\nhttps://t.me/PUbgNexusX_bot?start=inv_{user_id}")

    elif message.text == "👤 پروفایل و لینک دعوت":
        bot.send_message(message.chat.id, f"👤 وضعیت: {count}/3 دعوت\n\nلینک دعوت:\nhttps://t.me/PUbgNexusX_bot?start=inv_{user_id}")
