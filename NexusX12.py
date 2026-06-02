import telebot
from telebot import types

TOKEN = '8981532484:AAGe0CuTyI5W6THRjcz6SkE5-9ao4Jf-C5Y'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("🚀 دریافت وایرگارد", callback_data='get_vpn')
    btn2 = types.InlineKeyboardButton("🔗 لینک دعوت من", callback_data='my_link')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "سلام! به ربات PUBG NexusX خوش آمدی.\nیکی از گزینه‌ها را انتخاب کن:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'get_vpn':
        bot.send_message(call.chat.id, "⚠️ برای دریافت وایرگارد، باید حداقل ۳ نفر را دعوت کنی.")
    elif call.data == 'my_link':
        user_link = f"https://t.me/PUbgNexusX_bot?start={call.from_user.id}"
        bot.send_message(call.chat.id, f"🔗 لینک اختصاصی شما برای دعوت:\n{user_link}")

bot.infinity_polling()
