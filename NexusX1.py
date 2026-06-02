# -*- coding: utf-8 -*-
import telebot

# Your bot token
BOT_TOKEN = '8981532484:AAge0CuTyI5W6THRjcz6'
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Text is in English to avoid encoding errors
    bot.reply_to(message, "The bot is working correctly.")

print("Bot is running...")
bot.infinity_polling()
