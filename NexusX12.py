@bot.message_handler(func=lambda message: True)
def handle_menu(message):
    user_id = message.from_user.id
    if not check_membership(user_id):
        return start(message)

    # گرفتن تعداد دعوت کاربر از دیتابیس
    cursor.execute('SELECT COUNT(*) FROM users WHERE inviter = ?', (user_id,))
    count = cursor.fetchone()[0]

    if message.text == "🔥 وایرگارد":
        if count >= 3:
            bot.send_message(message.chat.id, "سرویس وایرگارد شما:\n`لینک_وایرگارد`", parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, f"❌ برای وایرگارد ۳ دعوت نیاز است. فعلی: {count}")

    elif message.text == "🌐 پنل V2Ray":
        if count >= 3:
            bot.send_message(message.chat.id, "سرویس پنل V2Ray شما:\n`لینک_ویتوری`", parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, f"❌ برای پنل V2Ray ۳ دعوت نیاز است. فعلی: {count}")

    elif message.text == "📊 لیدربورد":
        cursor.execute('SELECT inviter, COUNT(*) as count FROM users WHERE inviter != 0 GROUP BY inviter ORDER BY count DESC LIMIT 5')
        top = cursor.fetchall()
        text = "🏆 **لیدربورد دعوت‌کنندگان:**\n\n" + "\n".join([f"{i+1}. کاربر {u[0]}: {u[1]} دعوت" for i, u in enumerate(top)])
        bot.send_message(message.chat.id, text, parse_mode='Markdown')

    elif message.text == "🎡 چرخونه شانس":
        bot.send_message(message.chat.id, f"🎡 نتیجه چرخونه: {random.choice(['+1 دعوت', 'شانس مجدد', 'هیچ'])}")

    elif message.text == "👤 پروفایل":
        bot.send_message(message.chat.id, f"👤 پروفایل شما\nتعداد دعوت: {count}\nلینک دعوت:\nhttps://t.me/PUbgNexusX_bot?start=inv_{user_id}")

    elif message.text == "🎁 جوایز مرحله‌ای":
        bot.send_message(message.chat.id, "🎁 جوایز:\n۳ دعوت: وایرگارد\n۵ دعوت: پنل")
