import json
import asyncio
import os
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# ==== ВСТАВЬ СВОИ ДАННЫЕ ====
TOKEN = os.getenv("TELEGRAM_TOKEN")
MY_ID = int(os.getenv("MY_ID"))
# ============================

bot = Bot(token=TOKEN)
dp = Dispatcher()

with open("schedule.json", "r", encoding="utf-8") as f:
    SCHEDULE = json.load(f)

DAYS = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]

def format_day(day_name):
    pairs = SCHEDULE.get(day_name, [])
    if not pairs:
        return f"📅 {day_name.capitalize()}: пар нет 🎉"
    text = f"📅 {day_name.capitalize()}:\n"
    for p in pairs:
        text += f"  🕐 {p['время']} — {p['пара']}\n"
    return text

async def send_today():
    today = DAYS[datetime.now().weekday()]
    await bot.send_message(MY_ID, "☀️ Сегодня:\n" + format_day(today))

async def send_tomorrow():
    tomorrow = DAYS[(datetime.now() + timedelta(days=1)).weekday()]
    await bot.send_message(MY_ID, "🌙 Завтра:\n" + format_day(tomorrow))

@dp.message(Command("today"))
async def cmd_today(message: types.Message):
    today = DAYS[datetime.now().weekday()]
    await message.answer(format_day(today))

@dp.message(Command("tomorrow"))
async def cmd_tomorrow(message: types.Message):
    tomorrow = DAYS[(datetime.now() + timedelta(days=1)).weekday()]
    await message.answer(format_day(tomorrow))

async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_today, "cron", hour=7, minute=30)
    scheduler.add_job(send_tomorrow, "cron", hour=21, minute=25)
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
