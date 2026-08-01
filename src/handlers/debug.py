from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message()
async def handle_other(message: Message):
    """Обработчик всех остальных сообщений"""
    user_text = message.text
    await message.answer(f"Ты написал: {user_text}")