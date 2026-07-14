# src/database/queries.py
from sqlalchemy import select, func
from .connection import async_session_maker
from .models import DogProfile


async def get_row_count() -> int:
    """Получить количество строк в таблице dog_profile"""
    async with async_session_maker() as session:
        stmt = select(func.count()).select_from(DogProfile)
        result = await session.execute(stmt)
        return result.scalar()


async def get_first_profile():
    """Получить первую запись из таблицы"""
    async with async_session_maker() as session:
        stmt = select(DogProfile).limit(1)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()


async def ensure_one_profile():
    """Гарантирует, что в таблице есть ровно одна запись"""
    async with async_session_maker() as session:
        count = await get_row_count()

        if count == 0:
            new_dog = DogProfile()
            session.add(new_dog)
            await session.commit()
            await session.refresh(new_dog)
            return new_dog

        # Получаем первую запись
        stmt = select(DogProfile).limit(1)
        result = await session.execute(stmt)
        return result.scalar_one()