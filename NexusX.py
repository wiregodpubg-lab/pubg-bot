import telebot
from telebot import types
import sqlite3

TOKEN = '8981532484:AAG1Z2o1ZJ6QWnRUUpAUz87hbnSwmjBs064'
CHANNEL = "@NexusXTOP"
bot = telebot.TeleBot(TOKEN)

# دیتابیس
conn = sqlite3.connect('data.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, count INTEGER)')
conn.commit()

def is_sub(uid):
    try: return bot.get_chat_member(CHANNEL, uid).status in ['member', 'administrator', 'creator']
    except: return False

@bot.message_handler(commands=['start'])
def start(m):
    uid = m.from_user.id
    if 'inv_' in m.text:
        inv_id = int(m.text.split('inv_')[1])
        if inv_id != uid:
            cursor.execute('INSERT OR IGNORE INTO users VALUES (?, 0)', (inv_id,))
            cursor.execute('UPDATE users SET count = count + 1 WHERE id = ?', (inv_id,))
            conn.commit()

    if not is_sub(uid):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("عضویت در کانال", url=f"https://t.me/{CHANNEL[1:]}"))
        markup.add(types.InlineKeyboardButton("✅ عضو شدم", callback_data="check"))
        bot.send_message(uid, "❌ برای استفاده از پنل، ابتدا در کانال عضو شو:", reply_markup=markup)
    else:
        show_menu(uid)

def show_menu(uid):
    m = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    m.add("🔥 وایرگارد پینگ ۲۰", "💫 پنل V2rayNG", "❄️ پنل DNS", "👑 openvpn")
    bot.send_message(uid, "✨ **به پنل اختصاصی نکسوس خوش آمدی!**\n\nبرای دریافت هر سرویس، باید ۳ نفر دعوت کنی.\n🔗 لینک اختصاصی شما:\n`https://t.me/PUbgNexusX_bot?start=inv_{uid}`", reply_markup=m, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == "check")
def callback(call):
    if is_sub(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ عضویت تایید شد!")
        show_menu(call.from_user.id)
    else:
        bot.answer_callback_query(call.id, "❌ هنوز عضو نشدی!")

@bot.message_handler(func=lambda m: True)
def panel(m):
    uid = m.from_user.id
    if not is_sub(uid): return
    
    cursor.execute('SELECT count FROM users WHERE id = ?', (uid,))
    res = cursor.fetchone()
    count = res[0] if res else 0

    if count >= 3:
        links = {
            "🔥 وایرگارد پینگ ۲۰": "vless://wg-ping-20-link",
            "💫 پنل V2rayNG": "vless://v2ray-link",
            "❄️ پنل DNS": "dns://national-net",
            "👑 openvpn": "ovpn://openvpn-config"
        }
        bot.send_message(uid, f"✅ سرویس {m.text} برای شما آزاد شد:\n`{links.get(m.text, 'لینک موجود نیست')}`", parse_mode='Markdown')
    else:
        bot.send_message(uid, f"⚠️ شما {count} دعوت دارید. برای دریافت {m.text} باید ۳ نفر دعوت کنی.\n🔗 لینک تو: `https://t.me/PUbgNexusX_bot?start=inv_{uid}`", parse_mode='Markdown')

bot.infinity_polling()
