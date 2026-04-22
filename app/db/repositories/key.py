from typing import Optional
from sqlalchemy.future import select

from ..models import Key


class KeyRepository:
    def __init__(self, db):
        self.db = db

    async def create(self, key_value: str, owner_id: int) -> Key:
        """Создаёт ключ и привязывает к владельцу"""
        async with self.db.async_session() as session, session.begin():
            key = Key(key_value=key_value, owner_id=owner_id)
            session.add(key)
            await session.flush()
            await session.refresh(key)
            return key

    async def get(self, key_value: str) -> Optional[Key]:
        """Возвращает ключ по значению или None"""
        async with self.db.async_session() as session:
            return await self._get(session, key_value)

    async def mark_as_sold(self, key_value: str) -> bool:
        """Помечает ключ как проданный. True - успешно, False - не найден"""
        async with self.db.async_session() as session, session.begin():
            key = await self._get(session, key_value)
            if not key:
                return False
            key.is_sold = True
            return True

    async def delete(self, key_value: str) -> bool:
        """Удаляет ключ. True - успешно, False - не найден"""
        async with self.db.async_session() as session, session.begin():
            key = await self._get(session, key_value)
            if not key:
                return False
            await session.delete(key)
            return True
        
    async def _get(self, session, key_value: str) -> Optional[Key]:
        """Получает ключ по значению"""
        return (await session.execute(select(Key).where(Key.key_value == key_value))).scalars().first()