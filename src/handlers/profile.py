from aiogram import Router
from aiogram.filters import Command, or_f
from aiogram.types import Message
from aiogram import F

from services.profile_service import DogProfile

router = Router()
dog_profile = DogProfile()


@router.message(Command("count"))
async def cmd_count(message: Message):
    """Показать количество записей в БД"""
    try:
        count = await dog_profile.get_row_count()
        await message.answer(f"📊 В таблице dog_profile {count} записей")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")


@router.message(or_f(Command("dog_profile"), F.text == "🐕 Профиль собаки"))
async def cmd_dog_profile(message: Message):
    """Показать профиль собаки"""
    try:
        dog = await dog_profile.get_first()

        if dog:
            await message.answer(
                f"🐕 Профиль собаки:\n"
                f"ID: {dog.id}\n"
                f"Имя: {dog.name}\n"
                f"Дата рождения: {dog.birth_date.strftime('%d.%m.%Y')}\n"
                f"Вес: {dog.weight} кг\n"
                f"Порода: {dog.breed}\n"
                f"Создан: {dog.created_at}"
            )
        else:
            await message.answer("❌ Нет записей в БД!")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")