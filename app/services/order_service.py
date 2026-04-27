import random
from loguru import logger

from app.shared import db
from app.db import Database
from app.db.models.order import Order
from app.shared.constants import PIE_FAKE_COUNT_MIN, PIE_FAKE_COUNT_MAX
from app.utils import random_keys_count, random_lifetime, lifetime_from_hours


class OrderService:
    """Бизнес-логика для работы с паями (тендерами)."""

    def __init__(self, db: Database):
        self.db = db

    async def create(self, total_keys: int, lifetime_hours: int) -> Order:
        """Создаёт реальный пай с заданными параметрами."""
        return await self.db.order.create(
            total_keys=total_keys,
            expires_at=lifetime_from_hours(lifetime_hours),
            is_fake=False,
        )

    async def create_fake(self) -> Order:
        """Создаёт один фейковый пай со случайными параметрами."""
        return await self.db.order.create(
            total_keys=random_keys_count(),
            expires_at=random_lifetime(),
            is_fake=True,
        )

    async def maintain_fakes(self) -> None:
        """
        Удаляет истёкшие паи и досоздаёт фейки до случайного числа
        в диапазоне [PIE_FAKE_COUNT_MIN, PIE_FAKE_COUNT_MAX].
        Вызывается из scheduler каждые 5 минут.
        """
        deleted = await self.db.order.delete_expired()
        if deleted:
            logger.info(f"Orders: removed {deleted} expired")

        current = await self.db.order.count_active_fakes()

        if current < PIE_FAKE_COUNT_MIN:
            target = random.randint(PIE_FAKE_COUNT_MIN, PIE_FAKE_COUNT_MAX)
            need = target - current
            for _ in range(need):
                await self.create_fake()
            logger.info(f"Orders: +{need} fakes created (was {current}, target {target})")


order_service = OrderService(db)