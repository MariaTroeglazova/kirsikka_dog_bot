from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Создает главную клавиатуру с кнопками"""
    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text="🐕 Профиль собаки"))
    builder.add(KeyboardButton(text="🤖 Помощь"))

    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)