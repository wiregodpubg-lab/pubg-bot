import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = '8981532484:AAGe0CuTyI5W6THRjcz6SkE5-9ao4Jf-C5Y'
bot = telebot.TeleBot(BOT_TOKEN)

CHANNEL_ID = '@NexusXTOP'  

def is_user_subscribed(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
        return False
    except Exception:
        return False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    
    if is_user_subscribed(user_id):
        bot.send_message(user_id, "✅ عضویت شما تایید شده است! به ربات خوش آمدید.")
    else:
        markup = InlineKeyboardMarkup()
        btn_link = InlineKeyboardButton("📢 عضویت در چنل Nexus", url="https://t.me/NexusXTOP")
        btn_check = InlineKeyboardButton("✅ تایید عضویت", callback_data="check_sub")
        markup.add(btn_link)
        markup.add(btn_check)
        
        text = "⚠️ **عضویت اجباری**\n\nبرای استفاده از امکانات ربات, ابتدا باید عضو چنل زیر شوید و سپس روی دکمه تایید عضویت بزنید:"
        bot.send_message(user_id, text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_subscription_callback(call):
    user_id = call.from_user.id
    
    if is_user_subscribed(user_id):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(user_id, "🎉 تشکر! عضویت شما تایید شد و ربات فعال گردید.")
    else:
        bot.answer_callback_query(call.id, "❌ شما هنوز عضو چنل NexusXTOP نشده‌اید!", show_alert=True)

bot.infinity_polling()
