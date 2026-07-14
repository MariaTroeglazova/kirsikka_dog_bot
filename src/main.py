import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, or_f
from aiogram.types import Message, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import F

from services.profile_service import DogProfile

src_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(src_dir)

with open(os.path.join(project_dir, 'tgtoken'), 'r', encoding='utf-8') as file:
    TOKEN = file.read().strip()

bot = Bot(token=TOKEN)
dp = Dispatcher()

dog_profile = DogProfile()


def get_main_keyboard():
    """Создает главную клавиатуру с кнопками"""
    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text="🐕 Профиль собаки"))
    builder.add(KeyboardButton(text="🤖 Помощь"))

    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


@dp.message(Command("start"))
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    await message.answer(
        "👋 Привет! Я твой личный пет-проект!\nИспользуй кнопки ниже для навигации:",
        reply_markup=get_main_keyboard() # <- Прикрепляем клавиатуру
    )


@dp.message(or_f(Command("help"), F.text == "🤖 Помощь"))
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


@dp.message(Command("stop"))
async def cmd_stop(message: Message):
    """Обработчик команды /stop"""
    await message.answer("🛑 Бот остановлен! До свидания!")


@dp.message(Command("count"))
async def cmd_count(message: Message):
    """Показать количество записей в БД"""
    try:
        count = await dog_profile.get_row_count()
        await message.answer(f"📊 В таблице dog_profile {count} записей")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")


@dp.message(or_f(Command("dog_profile"), F.text == "🐕 Профиль собаки"))
async def cmd_dog_profile(message: Message):
    """Показать профиль собаки"""
    try:
        dog = await dog_profile.get_first()

        if dog:
            await message.answer(
                f"🐕 Профиль собаки:\n"
                f"ID: {dog.id}\n"
                f"Имя: {dog.name}\n"
                f"Дата рождения: {dog.birth_date.strftime("%d.%m.%Y")}\n"
                f"Вес: {dog.weight} кг\n"
                f"Порода: {dog.breed}\n"
                f"Создан: {dog.created_at}"
            )
        else:
            await message.answer("❌ Нет записей в БД!")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")


@dp.message()
async def handle_other(message: Message):
    """Обработчик всех остальных сообщений"""
    user_text = message.text
    await message.answer(f"Ты написал: {user_text}")


async def on_startup():
    """Действия при запуске бота"""
    print("🔄 Инициализация БД...")

    # Создаём таблицы
    await dog_profile.init_db()

    # Гарантируем, что есть одна запись
    dog = await dog_profile.ensure_one()
    print(f"✅ БД готова. Запись: {dog.name}, {dog.birth_date}")

    print("🚀 Бот запущен и слушает...")


async def main():
    """Главная функция"""
    await on_startup()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())