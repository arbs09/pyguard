import init_db
from db import check_db
from main import bot
from uptime import start

print("Starting bot...")

init_db()
check_db()
start()
bot.run()