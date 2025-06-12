from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import os
from db import get_pending_reminders
from telegram import Bot
from dotenv import load_dotenv
from pytz import timezone

load_dotenv()
bot=Bot(os.getenv("TELEGRAM_TOKEN"))
ist = timezone("Asia/Kolkata")
scheduler = BackgroundScheduler(timezone=ist)
scheduler.start()
def schedule_job(rem):
    run_date=rem['remind_at']
    scheduler.add_job(
        lambda: bot.send_message(rem['chat_id'],f"⏰ Reminder : {rem['task']}"),
        trigger='date',
        run_date=run_date,
        id=str(rem['id'])
    )

def load_all():
    print("Loaded reminders:", get_pending_reminders())
    for rem in get_pending_reminders():
        if not scheduler.get_job(str(rem['id'])):
            schedule_job(rem)  