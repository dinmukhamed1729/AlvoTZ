from os import getenv

from aiogram import Dispatcher, types
from aiogram.filters import Command
from bot.bitrix import get_overdue_leads, add_comment, create_task_for_lead
from bot.keyboards import lead_keyboard
from bot.loggers import logger

dp = Dispatcher()
MANAGER = int(getenv("MANAGER_CHAT_ID"))


@dp.message(Command("start"))
async def start(msg: types.Message):
    await msg.answer("Бот запущен. Команда: /leads")


@dp.message(Command("leads"))
async def send_leads(msg: types.Message):
    leads = get_overdue_leads()
    logger.info(f"<UNK> <UNK> <UNK>: {len(leads)}")
    if not leads:
        return await msg.answer("Нет просроченных лидов.")

    for lead in leads:
        text = (
            f"📌 Лид #{lead['ID']}\n"
            f"Имя: {lead.get('TITLE')}\n"
            f"Тел: {lead.get('PHONE')[0]['VALUE'] if lead.get('PHONE') else '-'}\n"
        )
        await msg.answer(text, reply_markup=lead_keyboard(lead["ID"], lead["TITLE"]))


@dp.callback_query()
async def callbacks(cb: types.CallbackQuery):
    action, lead_id, lead_title = cb.data.split(":")
    lead_id = int(lead_id)

    if action == "call":
        add_comment(lead_id, "Менеджер позвонил.")
        await cb.answer("Комментарий добавлен.")
        await cb.message.edit_text(f"Лид {lead_title} — Позвонил")

    elif action == "write":
        add_comment(lead_id, "Менеджер написал клиенту.")
        await cb.answer("Комментарий добавлен.")
        await cb.message.edit_text(f"Лид {lead_title} — Написал")

    elif action == "delay":
        create_task_for_lead(lead_id=lead_id, lead_title=lead_title)
        await cb.answer("Задача создана.")
        await cb.message.edit_text(f"Лид {lead_title} — отложен на 2 часа")
