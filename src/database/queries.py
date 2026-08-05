import logging

from sqlalchemy import select, func, delete
from .connection import async_session_maker
from .models import DogProfile


logger = logging.getLogger(__name__)

async def get_row_count() -> int:
    """Получить количество строк в таблице dog_profile"""
    async with async_session_maker() as session:
        stmt = select(func.count()).select_from(DogProfile)
        result = await session.execute(stmt)
        return result.scalar()


async def get_first_profile() -> DogProfile|None:
    """Получить первую запись из таблицы"""
    async with async_session_maker() as session:
        stmt = select(DogProfile).limit(1)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()


async def ensure_one_profile() -> DogProfile:
    """Гарантирует, что в таблице есть ровно одна запись"""
    async with async_session_maker() as session:
        count = await get_row_count()
        try:
            if count == 0:
                new_dog = DogProfile()
                session.add(new_dog)
                await session.commit()
                await session.refresh(new_dog)
                return new_dog
            if count > 1:
                raise ValueError(f"Найдено {count} профилей, ожидается ровно 1")

            stmt = select(DogProfile).limit(1)
            result = await session.execute(stmt)
            return result.scalar_one()
        except ValueError as err:
            logger.warning(f"Обнаружено {count} записей в dog_profile. Выполняется автоматическое восстановление...")

            # Ооставляем первую запись
            stmt = select(DogProfile).order_by(DogProfile.id)
            result = await session.execute(stmt)
            profiles = result.scalars().all()
            profile_to_keep = profiles[0]

            ids_to_delete = [p.id for p in profiles[1:]]
            await session.execute(
                delete(DogProfile).where(DogProfile.id.in_(ids_to_delete))
            )

            await session.commit()
            await session.refresh(profile_to_keep)

            logger.info(f"Восстановление успешно. Оставлена запись с ID={profile_to_keep.id}")
            return profile_to_keep
