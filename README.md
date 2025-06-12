# Telegram Reminder Bot

A Python Telegram bot that allows users to set reminders using natural language. It uses `python-telegram-bot`, `APScheduler`, and `MySQL`.

## Features
- Add reminders using commands
- Scheduled execution with APScheduler
- MySQL database for persistence

## Setup
1. Clone this repo
2. Run `pip install -r requirements.txt`
3. Create a `.env` file with your bot token and DB config
4. Run the bot with `python bot.py`

## Commands
- `/remindme "task" at 2025-06-12 16:00`
- `/remindme "task" in 2h30m`

## Author
Mukund Nigam
