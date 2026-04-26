from app.shared import db
from app.db import Database
from app.utils.key_generator import generate_keys


class KeyService:
    """Бизнес-логика для работы с ключами"""

    def __init__(self, db: Database):
        self.db = db

    async def generate_for_payment(self, owner_id: int, payment_id: int, count: int) -> list[str]:
        """Генерирует ключи и сохраняет в БД с привязкой к платежу."""
        keys = generate_keys(count)
        for key in keys:
            await self.db.key.create(key_value=key, owner_id=owner_id, payment_id=payment_id)
        return keys

    async def get_keys_file(self, payment_id: int) -> tuple[bytes, str]:
        """Возвращает содержимое txt-файла с ключами и имя файла."""
        keys = await self.db.key.get_by_payment(payment_id)
        content = "\n".join(k.key_value for k in keys).encode("utf-8")
        filename = f"keys_order_{payment_id}.txt"
        return content, filename

    async def validate(self, keys: list[str], owner_id: int) -> bool:
        """Проверяет что ключи существуют, принадлежат владельцу и ещё не проданы."""
        for key_value in keys:
            key = await self.db.key.get(key_value)
            if not key or key.owner_id != owner_id or key.order_id is not None:
                return False
        return True

    async def sell(self, keys: list[str], owner_id: int, order_id: int) -> bool:
        """Продаёт ключи в заказ: проверяет и привязывает к заказу."""
        if not await self.validate(keys, owner_id):
            return False
        for key in keys:
            await self.db.key.sell(key, order_id)
        return True


key_service = KeyService(db)