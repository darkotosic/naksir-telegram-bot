# main.py
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
import os
from dotenv import load_dotenv
from commands.analyze import handle_analysis

load_dotenv()

bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Dobrodošao u NAKSIR VIP bota! Koristi /analyze <fixture_id> za dubinsku analizu meča.")

@dp.message(Command("analyze"))
async def analyze(message: Message):
    try:
        fid = int(message.text.split(" ")[1])
        reply = await handle_analysis(fid)
        await message.answer(reply)
    except:
        await message.answer("⚠️ Unesi validan fixture ID. Primer: /analyze 215402")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
