from datetime import datetime, timedelta
from loguru import logger

from app.shared import db
from app.db import Database
from app.shared.constants import (
    FIRST_OFFER_DELAY_HOURS,
    FIRST_OFFER_KEYS,
    FIRST_OFFER_DURATION_HOURS,
)


class SpecialOfferService:
    """Бизнес-логика для работы со спецпредложениями."""

    def __init__(self, db: Database):
        self.db = db

    async def send_first_offers(self) -> None:
        """
        Проверяет пользователей у которых прошло FIRST_OFFER_DELAY_HOURS
        с момента регистрации и first_offer_sent = False.
        Создаёт спецпредложение и отправляет уведомление.
        Вызывается из scheduler.
        """
        from app.bots.buyer_bot import send_offer
        
        threshold = datetime.utcnow() - timedelta(hours=FIRST_OFFER_DELAY_HOURS)
        users = await self.db.user.get_users_for_first_offer(threshold)

        for user in users:
            expires_at = datetime.utcnow() + timedelta(hours=FIRST_OFFER_DURATION_HOURS)
            offer = await self.db.special_offer.create(
                user_id=user.telegram_id,
                keys_count=FIRST_OFFER_KEYS,
                expires_at=expires_at,
            )
            await self.db.user.upsert_user(user.telegram_id, first_offer_sent=True)

            sent = await send_offer(user.telegram_id, offer.keys_count, offer.expires_at)
            if sent:
                logger.info(f"SpecialOffer: sent first offer to {user.telegram_id}")
            else:
                logger.warning(f"SpecialOffer: failed to send to {user.telegram_id}")

    async def deactivate_expired(self) -> None:
        """Деактивирует истёкшие спецпредложения. Вызывается из scheduler."""
        count = await self.db.special_offer.deactivate_expired()
        if count:
            logger.info(f"SpecialOffer: deactivated {count} expired")


special_offer_service = SpecialOfferService(db)
