from typing import Optional
from datetime import datetime
from sqlalchemy.future import select

from ..models.tender import Tender
from ..enums.tender import TenderStatus


class TenderRepository:
    def __init__(self, db):
        self.db = db

    # ─── CREATE ──────────────────────────────────────────────────────────────

    async def create(self, total_keys: int, status: TenderStatus) -> Tender:
        """Создаёт тендер с указанным статусом."""
        async with self.db.async_session() as session, session.begin():
            tender = Tender(total_keys=total_keys, status=status)
            session.add(tender)
            await session.flush()
            await session.refresh(tender)
            return tender

    # ─── GET ─────────────────────────────────────────────────────────────────

    async def get_active(self) -> Optional[Tender]:
        """Возвращает активный тендер или None."""
        async with self.db.async_session() as session:
            return (await session.execute(
                select(Tender).where(Tender.status == TenderStatus.active)
            )).scalars().first()

    async def get_next_queued(self) -> Optional[Tender]:
        """Возвращает первый тендер из очереди (по дате создания)."""
        async with self.db.async_session() as session:
            return (await session.execute(
                select(Tender)
                .where(Tender.status == TenderStatus.queued)
                .order_by(Tender.created_at)
            )).scalars().first()

    # ─── UPDATE ──────────────────────────────────────────────────────────────

    async def set_status(self, tender_id: int, status: TenderStatus, completed_at: Optional[datetime] = None) -> None:
        """Обновляет статус тендера."""
        async with self.db.async_session() as session, session.begin():
            tender = await self._get(session, tender_id)
            if tender:
                tender.status = status
                if completed_at:
                    tender.completed_at = completed_at

    async def add_keys(self, tender_id: int, amount: int) -> Optional[Tender]:
        """Добавляет ключи к тендеру, возвращает обновлённый объект."""
        async with self.db.async_session() as session, session.begin():
            tender = await self._get(session, tender_id)
            if tender:
                tender.current_keys += amount
                await session.flush()
                await session.refresh(tender)
            return tender

    # ─── PRIVATE ─────────────────────────────────────────────────────────────

    async def _get(self, session, tender_id: int) -> Optional[Tender]:
        return (await session.execute(
            select(Tender).where(Tender.id == tender_id)
        )).scalars().first()
