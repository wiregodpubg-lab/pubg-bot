import os
from telegram.ext import Updater

# خواندن توکن از تنظیمات رندر (Environment Variable)
TOKEN = os.getenv('API_TOKEN')

# شروع ربات
updater = Updater(TOKEN)
# ... بقیه کدهای ربات خودت را اینجا بنویس ...
