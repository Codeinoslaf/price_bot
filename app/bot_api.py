import asyncio
import time
import os

from aiogram import Bot
from parser_html import get_mcap_number
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
INTERVAL = 15


async def send_mcap(bot: Bot, value: float):
    text = f"<b>MCAP:</b> {value:,.2f} тыс. $"
    await bot.send_message(chat_id=CHAT_ID, text=text, parse_mode="HTML")


async def monitor():
    bot = Bot(token=BOT_TOKEN)
    last_mcap = None

    print("Бот запущен. Мониторинг MCAP...")
    try:
        while True:
            mcap = get_mcap_number()
            if mcap is None:
                print(f"[{time.strftime('%H:%M:%S')}] Нет данных")
            elif mcap != last_mcap:
                await send_mcap(bot, mcap)
                print(f"[{time.strftime('%H:%M:%S')}] Отправлено: {mcap:,.2f} тыс. $")
                last_mcap = mcap
            else:
                print(f"[{time.strftime('%H:%M:%S')}] Без изменений: {mcap:,.2f} тыс. $")

            await asyncio.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("\nОстановлено вручную.")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(monitor())
