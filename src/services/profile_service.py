# src/services/profile_service.py
from database import queries
from database import connection


class DogProfile:
    """Сервис для работы с профилями собак"""

    async def init_db(self):
        """Инициализация БД"""
        await connection.init_db()

    async def get_row_count(self) -> int:
        """Получить количество записей"""
        return await queries.get_row_count()

    async def get_first(self):
        """Получить первую запись"""
        return await queries.get_first_profile()

    async def ensure_one(self):
        """Гарантирует одну запись в БД"""
        return await queries.ensure_one_profile()