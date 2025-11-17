import asyncio
from os import getenv

from aiogram import Bot
from aiogram import Router
from dotenv import load_dotenv

from bot.bitrix import get_overdue_leads, add_comment, create_task_for_lead
from bot.keyboards import lead_keyboard
from bot.loggers import logger
from bot.handlers import dp

router = Router()
load_dotenv()

bot = Bot(getenv("TELEGRAM_TOKEN"))


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
