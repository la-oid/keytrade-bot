from typing import Optional
from datetime import datetime
from sqlalchemy.future import select

from ..models.special_offer import SpecialOffer
from ..models import Payment
from ..enums import PaymentStatus


class SpecialOfferRepository:
    def __init__(self, db):
        self.db = db


    # ─── CREATE ──────────────────────────────────────────────────────────────

    async def create(self, user_id: int, keys_count: int, expires_at: datetime, custom_text: str | None = None) -> SpecialOffer:
        """Создаёт спецпредложение для пользователя."""
        async with self.db.async_session() as session, session.begin():
            offer = SpecialOffer(
                user_id=user_id,
                keys_count=keys_count,
                expires_at=expires_at,
                custom_text=custom_text,
            )
            session.add(offer)
            await session.flush()
            await session.refresh(offer)
            return offer


    # ─── GET ─────────────────────────────────────────────────────────────────

    async def get_active(self, user_id: int) -> Optional[SpecialOffer]:
        async with self.db.async_session() as session:
            offer = (await session.execute(
                select(SpecialOffer).where(
                    SpecialOffer.user_id == user_id,
                    SpecialOffer.is_active == True,
                )
            )).scalars().first()

            if not offer:
                return None

            # Проверяем нет ли активного заказа по этому офферу
            active_payment = (await session.execute(
                select(Payment).where(
                    Payment.special_offer_id == offer.id,
                    Payment.status.not_in([
                        PaymentStatus.CANCELLED,
                    ])
                )
            )).scalars().first()

            return None if active_payment else offer


    # ─── UPDATE ──────────────────────────────────────────────────────────────

    async def deactivate(self, user_id: int) -> bool:
        """Деактивирует спецпредложение пользователя."""
        async with self.db.async_session() as session, session.begin():
            offer = (await session.execute(
                select(SpecialOffer).where(
                    SpecialOffer.user_id == user_id,
                    SpecialOffer.is_active == True,
                )
            )).scalars().first()
            if not offer:
                return False
            offer.is_active = False
            return True

    async def deactivate_expired(self) -> int:
        """Деактивирует все истёкшие спецпредложения. Вызывается из scheduler."""
        async with self.db.async_session() as session, session.begin():
            expired = (await session.execute(
                select(SpecialOffer).where(
                    SpecialOffer.is_active == True,
                    SpecialOffer.expires_at <= datetime.utcnow(),
                )
            )).scalars().all()
            for offer in expired:
                offer.is_active = False
            return len(expired)