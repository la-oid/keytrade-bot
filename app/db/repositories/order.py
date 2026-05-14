from typing import Optional
from datetime import datetime
from sqlalchemy.future import select
from sqlalchemy import func

from ..models.order import Order

from app.utils import (
    generate_unique_code, 
    generate_numeric_code
)


class OrderRepository:
    def __init__(self, db):
        self.db = db

    # ─── CREATE ──────────────────────────────────────────────────────────────

    async def create(self, total_keys: int, expires_at: datetime, is_fake: bool = False) -> Order:
        """Создаёт новый пай."""
        async with self.db.async_session() as session, session.begin():

            code = await generate_unique_code(session, Order, lambda: generate_numeric_code(6))

            order = Order(
                id=code,
                total_keys=total_keys,
                expires_at=expires_at,
                is_fake=is_fake,
            )

            session.add(order)
            await session.flush()
            await session.refresh(order)
            return order

    # ─── GET ─────────────────────────────────────────────────────────────────

    async def get_by_id(self, order_id: int) -> Optional[Order]:
        """Возвращает пай по ID или None."""
        async with self.db.async_session() as session:
            return (await session.execute(
                select(Order).where(Order.id == order_id)
            )).scalars().first()

    async def get_all_active(self) -> list[Order]:
        """Возвращает все активные паи (и реальные, и фейковые) у которых не истёк срок."""
        async with self.db.async_session() as session:
            return (await session.execute(
                select(Order)
                .where(Order.is_active == True)
                .order_by(Order.created_at.desc())
            )).scalars().all()

    async def count_active_fakes_by_range(self, min_keys: int, max_keys: int) -> int:
        """Считает активные фейки в заданном диапазоне ключей."""
        async with self.db.async_session() as session:
            result = await session.execute(
                select(func.count()).select_from(Order).where(
                    Order.is_fake == True,
                    Order.is_active == True,
                    Order.total_keys >= min_keys,
                    Order.total_keys <= max_keys,
                )
            )
            return result.scalar() or 0

    # ─── UPDATE ──────────────────────────────────────────────────────────────

    async def set_active(self, order_id: int, is_active: bool) -> bool:
        """Открывает или закрывает пай. True — успешно, False — не найден."""
        async with self.db.async_session() as session, session.begin():
            order = await self._get(session, order_id)
            if not order:
                return False
            order.is_active = is_active
            return True
        
    async def deactivate_expired(self) -> list[Order]:
        """Деактивирует все истёкшие паи и возвращает их список. Вызывается из scheduler."""
        async with self.db.async_session() as session, session.begin():
            expired = (await session.execute(
                select(Order).where(
                    Order.expires_at <= datetime.utcnow(),
                    Order.is_active == True,
                )
            )).scalars().all()
            for order in expired:
                order.is_active = False
            return list(expired)

    # ─── DELETE ──────────────────────────────────────────────────────────────

    async def delete(self, order_id: int) -> bool:
        """Удаляет пай по ID. True — успешно, False — не найден."""
        async with self.db.async_session() as session, session.begin():
            order = await self._get(session, order_id)
            if not order:
                return False
            await session.delete(order)
            return True

    # ─── PRIVATE ─────────────────────────────────────────────────────────────

    async def _get(self, session, order_id: int) -> Optional[Order]:
        return (await session.execute(
            select(Order).where(Order.id == order_id)
        )).scalars().first()