from typing import Optional
from sqlalchemy.future import select

from ..models import Cashout
from ..enums import CashoutStatus


class CashoutRepository:
    def __init__(self, db):
        self.db = db

    # ─── CREATE ──────────────────────────────────────────────────────────────

    async def create(self, user_id: int, amount: float, card_number: str) -> Cashout:
        """Создаёт заявку на вывод."""
        async with self.db.async_session() as session, session.begin():
            cashout = Cashout(
                user_id=user_id,
                amount=amount,
                card_number=card_number,
            )
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