from app.shared import db
from app.db import Database
from app.utils.key_generator import generate_keys


class KeyService:
    """Бизнес-логика для работы с ключами"""

    def __init__(self, db: Database):
        self.db = db

    async def generate_and_save(self, owner_id: int, count: int) -> list[str]:
        """Генерирует ключи и сохраняет в БД"""
        keys = generate_keys(count)
        for key in keys:
            await self.db.key.create(key_value=key, owner_id=owner_id)
        return keys

    async def validate(self, keys: list[str], owner_id: int) -> bool:
        """Проверяет что ключи существуют, принадлежат владельцу и не проданы"""
        for key_value in keys:
            key = await self.db.key.get(key_value)
            if not key or key.owner_id != owner_id or key.is_sold: return False
        return True

    async def sell(self, keys: list[str], owner_id: int, order_id: int) -> bool:
        """Продаёт ключи в заказ: проверяет, помечает проданными"""
        if not await self.validate(keys, owner_id): return False
        for key in keys: await self.db.key.mark_as_sold(key)
        return True
    

key_service = KeyService(db)