import asyncio
import os
import sys

from aiogram import Bot, Dispatcher

from handlers import common_router, profile_router
from handlers.debug import router as debug_router
from services.profile_service import DogProfileService

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
src_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(src_dir)

with open(os.path.join(project_dir, 'tgtoken'), 'r', encoding='utf-8') as file:
    TOKEN = file.read().strip()

bot = Bot(token=TOKEN)
dp = Dispatcher()

dog_profile = DogProfileService()


async def on_startup() -> None:
    """Действия при запуске бота"""
    print("🔄 Инициализация БД...")

    await dog_profile.init_db()

    # Гарантируем, что есть одна запись
    dog = await dog_profile.ensure_one()
    print(f"✅ БД готова. Запись: {dog.name}, {dog.birth_date}")

    print("🚀 Бот запущен и слушает...")


async def main():
    dp.include_router(common_router)
    dp.include_router(profile_router)
    dp.include_router(debug_router)

    await on_startup()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())