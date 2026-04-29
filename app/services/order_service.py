from loguru import logger

from app.shared import db
from app.db import Database
from app.db.models.order import Order
from app.utils import random_keys_low, random_keys_high, random_lifetime, lifetime_from_hours
from app.shared.constants import (
    PIE_FAKE_LOW_COUNT, PIE_FAKE_HIGH_COUNT,
    PIE_KEYS_MIN, PIE_KEYS_MID, PIE_KEYS_MAX,
)


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

    async def maintain_fakes(self) -> None:
        """
        Удаляет истёкшие паи и досоздаёт фейки до нужного количества.
        Всегда поддерживает ровно PIE_FAKE_LOW_COUNT паёв в нижнем диапазоне
        и PIE_FAKE_HIGH_COUNT в верхнем.
        Вызывается из scheduler каждые 5 минут.
        """
        deleted = await self.db.order.delete_expired()
        if deleted:
            logger.info(f"Orders: removed {deleted} expired")

        # Считаем отдельно для каждого диапазона
        current_low  = await self.db.order.count_active_fakes_by_range(PIE_KEYS_MIN, PIE_KEYS_MID)
        current_high = await self.db.order.count_active_fakes_by_range(PIE_KEYS_MID, PIE_KEYS_MAX)

        need_low  = max(0, PIE_FAKE_LOW_COUNT  - current_low)
        need_high = max(0, PIE_FAKE_HIGH_COUNT - current_high)

        for _ in range(need_low):
            await self.db.order.create(
                total_keys=random_keys_low(),
                expires_at=random_lifetime(),
                is_fake=True,
            )
        for _ in range(need_high):
            await self.db.order.create(
                total_keys=random_keys_high(),
                expires_at=random_lifetime(),
                is_fake=True,
            )

        if need_low or need_high:
            logger.info(
                f"Orders: +{need_low} low fakes, +{need_high} high fakes "
                f"(low now={current_low + need_low}, high now={current_high + need_high})"
            )


order_service = OrderService(db)