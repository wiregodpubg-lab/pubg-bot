import telebot
from telebot import types
import sqlite3

# توکن و آیدی کانال شما
TOKEN = '8981532484:AAGe0CuTyI5W6THRjcz6SkE5-9ao4Jf-C5Y'
CHANNEL_ID = "@NexusXTOP"
bot = telebot.TeleBot(TOKEN)

# دیتابیس
conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, inviter INTEGER)')
conn.commit()

# --- لینک‌های خود را اینجا قرار دهید ---
WIREGUARD_LINK = "vless://لینک_وایرگارد_اختصاصی_شما"
V2RAY_PANEL_LINK = "vless://لینک_پنل_ویتوری_شما"
# -------------------------------------

def check_membership(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except: return False

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    args = message.text.split()
    
    # ثبت معرف
    if len(args) > 1 and "inv_" in args[1]:
        inviter_id = int(args[1].replace("inv_", ""))
        cursor.execute('INSERT OR IGNORE INTO users (id, inviter) VALUES (?, ?)', (user_id, inviter_id))
    else:
        cursor.execute('INSERT OR IGNORE INTO users (id, inviter) VALUES (?, 0)', (user_id, 0))
    conn.commit()

    # چک عضویت
    if not check_membership(user_id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✅ عضویت در کانال NexusXTOP", url="https://t.me/NexusXTOP"))
        bot.send_message(message.chat.id, "⚠️ **ابتدا در کانال ما عضو شوید**\n\nبرای دسترسی به سرویس‌ها، عضو کانال ما شوید و دوباره /start را بزنید:", reply_markup=markup)
        return

    # منوی اصلی
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add("🔥 وایرگارد پینگ پایین", "🌐 پنل اختصاصی V2Ray", "👤 وضعیت دعوت‌ها")
    bot.send_message(message.chat.id, "خوش آمدید! از منو انتخاب کنید.\nبا دعوت ۳ نفر، سرویس اختصاصی هدیه بگیرید.", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_menu(message):
    user_id = message.from_user.id
    cursor.execute('SELECT COUNT(*) FROM users WHERE inviter = ?', (user_id,))
    count = cursor.fetchone()[0]

    if message.text in ["🔥 وایرگارد پینگ پایین", "🌐 پنل اختصاصی V2Ray"]:
        if count >= 3:
            link = WIREGUARD_LINK if "وایرگارد" in message.text else V2RAY_PANEL_LINK
            bot.send_message(message.chat.id, f"✅ **سرویس شما:**\n\n`{link}`\n\nنوش جان!", parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, f"⚠️ **دسترسی محدود!**\nشما {count} نفر دعوت کردید. برای دریافت، باید ۳ نفر دعوت کنید.\n\n🔗 لینک دعوت شما:\nhttps://t.me/PUbgNexusX_bot?start=inv_{user_id}")

    elif message.text == "👤 وضعیت دعوت‌ها":
        bot.send_message(message.chat.id, f"👤 تعداد دعوت‌های شما: {count}/3\n\n🔗 لینک اختصاصی برای دعوت دوستان:\nhttps://t.me/PUbgNexusX_bot?start=inv_{user_id}")

bot.infinity_polling()
