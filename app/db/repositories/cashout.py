from typing import Optional
from sqlalchemy.future import select

from ..models import Cashout
from ..enums import CashoutStatus

from app.utils import (
    generate_unique_code, 
    generate_numeric_code
)


class CashoutRepository:
    def __init__(self, db):
        self.db = db

    # ─── CREATE ──────────────────────────────────────────────────────────────

    async def upsert_cashout(self, cashout_id: int = None, **kwargs) -> Cashout:
        """Создаёт или обновляет заявку. Если cashout_id не передан — создаёт новую."""
        async with self.db.async_session() as session, session.begin():
            cashout = await self._get(session, cashout_id) if cashout_id else None

            if cashout:
                for key, value in kwargs.items():
                    setattr(cashout, key, value)
            else:
                code = await generate_unique_code(session, Cashout, lambda: generate_numeric_code(6))
                cashout = Cashout(id=code, **kwargs)
                session.add(cashout)

            await session.flush()
            await session.refresh(cashout)
            return cashout

    # ─── GET ─────────────────────────────────────────────────────────────────

    async def get_by_id(self, cashout_id: int) -> Optional[Cashout]:
        """Возвращает заявку по ID или None."""
        async with self.db.async_session() as session:
            return (await session.execute(
                select(Cashout).where(Cashout.id == cashout_id)
            )).scalars().first()

    async def get_by_status(self, user_id: int, status: CashoutStatus | list[CashoutStatus], many: bool = False) -> Cashout | list[Cashout] | None:
        """Возвращает заявку(и) пользователя по статусу или списку статусов."""
        statuses = status if isinstance(status, list) else [status]
        async with self.db.async_session() as session:
            result = (await session.execute(
                select(Cashout).where(
                    Cashout.user_id == user_id,
                    Cashout.status.in_(statuses),
                ).order_by(Cashout.created_at.desc())
            )).scalars()
            return result.all() if many else result.first()
        
    async def get_all_by_status(self, status: CashoutStatus) -> list[Cashout]:
        """Возвращает все заявки по статусу — для админа."""
        async with self.db.async_session() as session:
            return (await session.execute(
                select(Cashout).where(Cashout.status == status)
                .order_by(Cashout.created_at.desc())
            )).scalars().all()

    # ─── UPDATE ──────────────────────────────────────────────────────────────

    async def set_status(self, cashout_id: int, status: CashoutStatus) -> bool:
        """Меняет статус заявки. True — успешно, False — не найдена."""
        async with self.db.async_session() as session, session.begin():
            cashout = await self._get(session, cashout_id)
            if not cashout:
                return False
            cashout.status = status
            return True

    # ─── PRIVATE ─────────────────────────────────────────────────────────────

    async def _get(self, session, cashout_id: int) -> Optional[Cashout]:
        return (await session.execute(
            select(Cashout).where(Cashout.id == cashout_id)
        )).scalars().first()