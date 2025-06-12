import os
import mysql.connector
from dotenv import load_dotenv


load_dotenv()

conn=mysql.connector.connect(host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"))

cursor=conn.cursor(dictionary=True)

def add_reminder(chat_id,task,reminder_at):
    cursor.execute("insert into reminders(chat_id,task,remind_at) values (%s,%s,%s)",(chat_id,task,reminder_at))
    conn.commit()
    return cursor.lastrowid

def get_pending_reminders():
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM reminders WHERE remind_at > NOW()")
    result = cur.fetchall()
    cur.close()
    return result

def delete_reminder(reminder_id):
    cur = conn.cursor()
    cur.execute("DELETE FROM reminders WHERE id = %s", (reminder_id,))
    conn.commit()
    cur.close()


def get_user_reminders(chat_id):
    cursor.execute("SELECT * FROM reminders WHERE chat_id=%s", (chat_id,))
    return cursor.fetchall()