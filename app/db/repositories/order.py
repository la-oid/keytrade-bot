from typing import Optional
from datetime import datetime
from sqlalchemy.future import select
from sqlalchemy import func

from ..models.order import Order


class OrderRepository:
    def __init__(self, db):
        self.db = db

    # ─── CREATE ──────────────────────────────────────────────────────────────

    async def create(self, total_keys: int, expires_at: datetime, is_fake: bool = False) -> Order:
        """Создаёт новый пай."""
        async with self.db.async_session() as session, session.begin():
            order = Order(
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
                .where(
                    Order.is_active == True,
                    Order.expires_at > datetime.utcnow())
                .order_by(Order.created_at.desc())
            )).scalars().all()

    async def count_active_fakes(self) -> int:
        """Считает активные фейковые паи. Нужно scheduler'у для поддержания их числа."""
        async with self.db.async_session() as session:
            result = await session.execute(
                select(func.count()).select_from(Order).where(
                    Order.is_fake == True,
                    Order.is_active == True,
                    Order.expires_at > datetime.utcnow(),
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

    # ─── DELETE ──────────────────────────────────────────────────────────────

    async def delete(self, order_id: int) -> bool:
        """Удаляет пай по ID. True — успешно, False — не найден."""
        async with self.db.async_session() as session, session.begin():
            order = await self._get(session, order_id)
            if not order:
                return False
            await session.delete(order)
            return True

    async def delete_expired(self) -> int:
        """Удаляет все истёкшие паи. Вызывается из scheduler. Возвращает количество удалённых."""
        async with self.db.async_session() as session, session.begin():
            expired = (await session.execute(
                select(Order).where(Order.expires_at <= datetime.utcnow())
            )).scalars().all()
            for order in expired:
                await session.delete(order)
            return len(expired)

    # ─── PRIVATE ─────────────────────────────────────────────────────────────

    async def _get(self, session, order_id: int) -> Optional[Order]:
        return (await session.execute(
            select(Order).where(Order.id == order_id)
        )).scalars().first()
