from aiogram.utils.keyboard import InlineKeyboardBuilder


def lead_keyboard(lead_id: int, lead_title:str):
    kb = InlineKeyboardBuilder()

    kb.button(text="✅ Позвонил", callback_data=f"call:{lead_id}:{lead_title}")
    kb.button(text="💬 Написал", callback_data=f"write:{lead_id}:{lead_title}")
    kb.button(text="⏳ Отложить на 2 часа", callback_data=f"delay:{lead_id}:{lead_title}")

    kb.adjust(1)
    return kb.as_markup()
