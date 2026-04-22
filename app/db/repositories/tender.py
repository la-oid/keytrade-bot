from typing import Optional
from sqlalchemy.future import select

from ..models import Tender


class TenderRepository:
    def __init__(self, db):
        self.db = db

    async def create_tender(self, total_keys: int, price_per_key: float) -> Tender:
        """
        Создаёт новый тендер.
        """
        async with self.db.async_session() as session:
            async with session.begin():
                tender = Tender(
                    total_keys=total_keys,
                    remaining_keys=total_keys,
                    price_per_key=price_per_key,
                    is_active=True
                )
                session.add(tender)
                await session.flush()
                await session.refresh(tender)
                return tender

    async def get_tender_by_id(self, tender_id: int) -> Optional[Tender]:
        """
        Возвращает тендер по ID или None.
        """
        async with self.db.async_session() as session:
            return await self._get_tender(session, tender_id)

    async def get_active_tenders(self) -> list[Tender]:
        """
        Возвращает все активные тендеры.
        """
        async with self.db.async_session() as session:
            return (await session.execute(
                select(Tender).where(Tender.is_active == True)
            )).scalars().all()

    async def update_remaining_keys(self, tender_id: int, keys_sold: int) -> Optional[Tender]:
        """
        Уменьшает количество оставшихся ключей в тендере.
        Если ключей не осталось - закрывает тендер.
        """
        async with self.db.async_session() as session:
            async with session.begin():
                tender = await self._get_tender(session, tender_id)
                if not tender:
                    return None
                tender.remaining_keys -= keys_sold
                if tender.remaining_keys <= 0:
                    tender.is_active = False
                await session.flush()
                await session.refresh(tender)
                return tender

    async def close_tender(self, tender_id: int) -> bool:
        """
        Закрывает тендер по ID.
        Возвращает True - успешно, False - тендер не найден.
        """
        async with self.db.async_session() as session:
            async with session.begin():
                tender = await self._get_tender(session, tender_id)
                if not tender:
                    return False
                tender.is_active = False
                return True

    async def delete_tender(self, tender_id: int) -> bool:
        """
        Удаляет тендер по ID.
        Возвращает True - успешно, False - тендер не найден.
        """
        async with self.db.async_session() as session:
            async with session.begin():
                tender = await self._get_tender(session, tender_id)
                if not tender:
                    return False
                await session.delete(tender)
                return True

    async def _get_tender(self, session, tender_id: int) -> Optional[Tender]:
        """
        Приватный метод для получения тендера по ID.
        """
        return (await session.execute(
            select(Tender).where(Tender.id == tender_id)
        )).scalars().first()