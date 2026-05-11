import random

from loguru import logger

from app.shared import db
from app.db import Database
from app.db.models.order import Order
from app.utils import random_lifetime, lifetime_from_hours
from app.shared.constants import PIE_RANGES, PIE_KEYS_STEP


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
        Деактивирует истёкшие паи и досоздаёт фейки до нужного количества.
        Поддерживает нужное кол-во паёв в каждом диапазоне из PIE_RANGES.
        Вызывается из scheduler каждые 5 минут.
        """
        deactivated = await self.db.order.deactivate_expired()
        if deactivated:
            logger.info(f"Orders: deactivated {deactivated} expired")

        total_added = 0

        for pie_range in PIE_RANGES:
            min_keys = pie_range["min"]
            max_keys = pie_range["max"]
            target   = pie_range["count"]

            current = await self.db.order.count_active_fakes_by_range(min_keys, max_keys)
            need    = max(0, target - current)

            for _ in range(need):
                # Генерируем случайное кол-во ключей кратное PIE_KEYS_STEP
                low  = min_keys // PIE_KEYS_STEP
                high = max_keys // PIE_KEYS_STEP
                total_keys = random.randint(low, high) * PIE_KEYS_STEP

                await self.db.order.create(
                    total_keys=total_keys,
                    expires_at=random_lifetime(),
                    is_fake=True,
                )

            if need:
                logger.info(
                    f"Orders: +{need} fakes [{min_keys}-{max_keys}] "
                    f"(now={current + need}/{target})"
                )
                total_added += need

        if not total_added:
            logger.debug("Orders: all fake ranges are full")


order_service = OrderService(db)