from aiogram import Router, F
from aiogram.filters import Command, or_f
from aiogram.types import Message

from keyboards.reply import get_main_keyboard

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    await message.answer(
        "👋 Привет! Я твой личный пет-проект!\nИспользуй кнопки ниже для навигации:",
        reply_markup=get_main_keyboard()
    )


@router.message(or_f(Command("help"), F.text == "🤖 Помощь"))
async def cmd_help(message: Message):
    """Обработчик команды /help"""
    await message.answer(
        "🤖 Доступные команды:\n"
        "/start - приветствие\n"
        "/help - помощь\n"
        "/count - количество записей в БД\n"
        "/dog_profile - показать профиль собаки\n"
        "/stop - остановить бота"
    )


@router.message(Command("stop"))
async def cmd_stop(message: Message):
    """Обработчик команды /stop"""
    await message.answer("🛑 Бот остановлен! До свидания!")