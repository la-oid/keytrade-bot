from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from .helper import db
from app.db.enums import PaymentStatus


# Куда переходят просроченные статусы
EXPIRY_TRANSITIONS: dict[PaymentStatus, PaymentStatus] = {
    PaymentStatus.PENDING_PAY:    PaymentStatus.PENDING_REVIEW,
    PaymentStatus.PENDING_PDF:    PaymentStatus.PENDING_REVIEW,
    PaymentStatus.PENDING_REVIEW: PaymentStatus.CANCELLED,
}


async def check_expired():
    """Каждые 30 секунд переводит просроченные платежи в следующий статус."""
    for from_status, to_status in EXPIRY_TRANSITIONS.items():
        expired = await db.payment.get_expired(from_status)
        for payment in expired:
            await db.payment.set_status(payment.id, to_status)
            logger.info(f"Payment {payment.id}: {from_status.value} → {to_status.value}")


scheduler = AsyncIOScheduler()
scheduler.add_job(check_expired, "interval", seconds=30, id="check_expired_payments")
