import os,re
from telegram import Update
from telegram.ext import Updater,CallbackContext,CommandHandler
from dateutil.parser import parse as dt_parse
from db import add_reminder, get_user_reminders, delete_reminder
from scheduler import load_all, schedule_job
from dotenv import load_dotenv
from datetime import datetime, timedelta




load_dotenv()
TOKEN=os.getenv("TELEGRAM_TOKEN")

def start(update: Update, ctx: CallbackContext):
    update.message.reply_text("👋 Hi! Please use /remindme \"Task\" at YYYY-MM-DD HH:MM or /remindme \"Task\" in XhXXm to set reminders")

def reminder(update:Update, ctx:CallbackContext):
    from pytz import timezone
    ist = timezone("Asia/Kolkata")
    text=update.message.text
    match = re.match(r'/remindme\s+"(.+)"\s+(?:at\s+(.+)|in\s+(.+))', text)
    if not match:
        update.message.reply_text("❌ Invalid format. Use: /remindme \"task\" at <YYYY-MM-DD HH:MM> or in <2h30m>")
        return
    task, at_time, in_time = match.groups()
    if in_time:
    # Parse "1h30m", "2m", etc.
        pattern = re.match(r"(?:(\d+)h)?(?:(\d+)m)?", in_time)
        hours = int(pattern.group(1) or 0)
        minutes = int(pattern.group(2) or 0)
        remind_at = datetime.now(ist) + timedelta(hours=hours, minutes=minutes)
    else:
        remind_at = dt_parse(at_time)
        remind_at = ist.localize(remind_at)
    rid=add_reminder(update.effective_chat.id,task,remind_at)
    schedule_job({'id': rid, 'chat_id': update.effective_chat.id, 'task': task, 'remind_at': remind_at})
    update.message.reply_text(f"✅ Reminder set for {task} at {remind_at}")

def list_reminders(update: Update, ctx: CallbackContext):
    rows=get_user_reminders(update.effective_chat.id)
    if not rows:
        return update.message.reply_text("No reminders found.")
    reply = "\n".join(f"{r['id']}: {r['task']} at {r['remind_at']}" for r in rows)
    update.message.reply_text(reply)

def delete(update: Update, ctx: CallbackContext):
    args = ctx.args
    if not args or not args[0].isdigit():
        return update.message.reply_text("❌ Usage: /delete <ID>")
    rid = int(args[0])
    delete_reminder(rid)
    try:
        from scheduler import scheduler
        scheduler.remove_job(str(rid))
    except Exception:
        pass
    update.message.reply_text(f"🗑️ Deleted reminder {rid}")

def main():
    load_all()
    updater=Updater(TOKEN)
    print("🚀 Bot is starting...")
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start",start))
    dp.add_handler(CommandHandler("remindme",reminder))
    dp.add_handler(CommandHandler("list",list_reminders))
    dp.add_handler(CommandHandler("delete",delete))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
