from typing import Optional
from sqlalchemy.future import select

from ..models import Key


class KeyRepository:
    def __init__(self, db):
        self.db = db

    async def create_key(self, key_value: str, owner_id: int) -> Key:
        """
        Создаёт новый ключ и привязывает его к владельцу.
        """
        async with self.db.async_session() as session:
            async with session.begin():
                key = Key(
                    key_value=key_value,
                    owner_id=owner_id,
                    is_sold=False
                )
                session.add(key)
                await session.flush()
                await session.refresh(key)
                return key

    async def get_key_by_value(self, key_value: str) -> Optional[Key]:
        """
        Возвращает ключ по его значению или None.
        """
        async with self.db.async_session() as session:
            return await self._get_key(session, key_value)

    async def get_keys_by_owner(self, owner_id: int) -> list[Key]:
        """
        Возвращает все ключи конкретного владельца.
        """
        async with self.db.async_session() as session:
            return (await session.execute(
                select(Key).where(Key.owner_id == owner_id)
            )).scalars().all()

    async def mark_keys_as_sold(self, key_values: list[str]) -> bool:
        """
        Помечает список ключей как проданные.
        Возвращает True - успешно, False - один из ключей не найден.
        """
        async with self.db.async_session() as session:
            async with session.begin():
                for key_value in key_values:
                    key = await self._get_key(session, key_value)
                    if not key:
                        return False
                    key.is_sold = True
                return True

    async def delete_key(self, key_value: str) -> bool:
        """
        Удаляет ключ по его значению.
        Возвращает True - успешно, False - ключ не найден.
        """
        async with self.db.async_session() as session:
            async with session.begin():
                key = await self._get_key(session, key_value)
                if not key:
                    return False
                await session.delete(key)
                return True

    async def _get_key(self, session, key_value: str) -> Optional[Key]:
        """
        Приватный метод для получения ключа по его значению.
        """
        return (await session.execute(
            select(Key).where(Key.key_value == key_value)
        )).scalars().first()