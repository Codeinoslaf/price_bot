import asyncio
import time
import os
import requests

from aiogram import Bot
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
INTERVAL = 180


def get_mcap_number() -> int | None:
    url = "https://api.dexscreener.com/tokens/v1/ton/EQDxE8C4-R53ol4InsjyVedmfI9xMF6lpJko2p90PAR0U5NT"

    try:
        response = requests.get(url, headers={"Accept": "*/*"}, timeout=10)
        response.raise_for_status()

        data = response.json()
        if not data:
            print("[!] Пары не найдены")
            return None

        market_cap = data[0]["marketCap"]
        return int(market_cap)

    except requests.exceptions.RequestException as e:
        print(f"[!] Сетевая ошибка: {e}")
    except (KeyError, IndexError, TypeError, ValueError):
        print("[!] Ошибка парсинга ответа API")

    return None


async def send_mcap(bot: Bot, value: int, last_mcap: int):
    if value > last_mcap:
        text = '🟢📈'
    elif value < last_mcap:
        text = '🔴📉'

    if value >= 1_000_000:
        text += f"<b>MCAP:</b> {value // 1_000:,} млн. $"
    else:
        text += f"<b>MCAP:</b> {value // 1_000:,} тыс. $"

    await bot.send_message(chat_id=CHAT_ID, text=text, parse_mode="HTML")


async def monitor():
    bot = Bot(token=BOT_TOKEN)
    last_mcap = 0

    print("Бот запущен. Мониторинг MCAP...")

    try:
        while True:
            mcap = get_mcap_number()
            if mcap is None:
                print(f"[{time.strftime('%H:%M:%S')}] Нет данных")

            elif mcap != last_mcap:
                await send_mcap(bot, mcap, last_mcap)
                print(f"[{time.strftime('%H:%M:%S')}] Отправлено: {mcap:,.2f} $")
                last_mcap = mcap

            else:
                print(f"[{time.strftime('%H:%M:%S')}] Без изменений: {mcap:,.2f} $")

            await asyncio.sleep(INTERVAL)

    except KeyboardInterrupt:
        print("\nОстановлено вручную.")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(monitor())
