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


async def check_expired_payments():
    """Каждые 30 секунд переводит просроченные платежи в следующий статус."""
    for from_status, to_status in EXPIRY_TRANSITIONS.items():
        expired = await db.payment.get_expired(from_status)
        for payment in expired:
            await db.payment.set_status(payment.id, to_status)
            logger.info(f"Payment {payment.id}: {from_status.value} → {to_status.value}")


async def maintain_fakes_job():
    from app.services import order_service
    await order_service.maintain_fakes()


async def send_first_offers_job():
    from app.services import special_offer_service
    await special_offer_service.send_first_offers()
 
 
async def deactivate_expired_offers_job():
    from app.services import special_offer_service
    await special_offer_service.deactivate_expired()


scheduler = AsyncIOScheduler()
scheduler.add_job(check_expired_payments,        "interval", seconds=30, id="check_expired_payments")
scheduler.add_job(maintain_fakes_job,            "interval", minutes=5,  id="maintain_fake_orders")
scheduler.add_job(send_first_offers_job,         "interval", minutes=5,  id="send_first_offers")
scheduler.add_job(deactivate_expired_offers_job, "interval", minutes=5,  id="deactivate_expired_offers")