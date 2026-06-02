import telebot
from telebot import types
import sqlite3

TOKEN = '8981532484:AAG1Z2o1ZJ6QWnRUUpAUz87hbnSwmjBs064'
CHANNEL_ID = "@NexusXTOP"
bot = telebot.TeleBot(TOKEN)

# دیتابیس
conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, inviter INTEGER)')
cursor.execute('CREATE TABLE IF NOT EXISTS inv_count (id INTEGER PRIMARY KEY, count INTEGER)')
conn.commit()

def check_membership(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except: return False

def get_invites(user_id):
    cursor.execute('SELECT count FROM inv_count WHERE id = ?', (user_id,))
    res = cursor.fetchone()
    return res[0] if res else 0

def add_invite(inviter_id):
    cursor.execute('INSERT OR IGNORE INTO inv_count (id, count) VALUES (?, 0)', (inviter_id,))
    cursor.execute('UPDATE inv_count SET count = count + 1 WHERE id = ?', (inviter_id,))
    conn.commit()

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if 'inv_' in message.text:
        inviter_id = int(message.text.split('inv_')[1])
        if inviter_id != user_id:
            cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
            if not cursor.fetchone():
                cursor.execute('INSERT INTO users (id, inviter) VALUES (?, ?)', (user_id, inviter_id))
                add_invite(inviter_id)
                conn.commit()
    
    if not check_membership(user_id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✅ عضویت در @NexusXTOP", url="https://t.me/NexusXTOP"))
        markup.add(types.InlineKeyboardButton("🔄 عضو شدم", callback_data="check_join"))
        bot.send_message(message.chat.id, "⚠️ **ابتدا در کانال ما عضو شوید:**\n@NexusXTOP", reply_markup=markup)
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
    # این همان ۴ گزینه‌ای است که خواستی:
    markup.add("🌐 پنل V2Ray", "🔥 وایرگارد پینگ ۲۰", "⚡️ پنل DNS نت ملی", "🛡 OpenVPN")
    bot.send_message(chat_id, "✅ به پنل خدمات خوش آمدید. هر سرویس نیاز به ۳ دعوت دارد:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_menu(message):
    if not check_membership(message.from_user.id): return start(message)
    
    user_id = message.from_user.id
    if message.text in ["🌐 پنل V2Ray", "🔥 وایرگارد پینگ ۲۰", "⚡️ پنل DNS نت ملی", "🛡 OpenVPN"]:
        invites = get_invites(user_id)
        if invites >= 3:
            bot.send_message(message.chat.id, f"✅ تبریک! سرویس {message.text} برای شما فعال شد:\n`لینک_اختصاصی_سرویس`\n\nتعداد دعوت‌های شما صفر شد.", parse_mode='Markdown')
            cursor.execute('UPDATE inv_count SET count = 0 WHERE id = ?', (user_id,))
            conn.commit()
        else:
            needed = 3 - invites
            bot.send_message(message.chat.id, f"❌ شما {invites} دعوت دارید.\nبرای دریافت {message.text} باید {needed} نفر دیگر دعوت کنید.\n\n🔗 لینک اختصاصی شما:\nhttps://t.me/PUbgNexusX_bot?start=inv_{user_id}")

bot.infinity_polling()
