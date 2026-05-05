from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy.future import select

from ..models import Payment
from ..enums import PaymentStatus


# Дедлайны по статусам (минуты, None — без таймера)
DEADLINES: dict[PaymentStatus, int | None] = {
    PaymentStatus.PENDING_PAY:    15,
    PaymentStatus.PENDING_HASH:   10,
    PaymentStatus.PENDING_PDF:    10,
    PaymentStatus.PENDING_REVIEW: 240,
    PaymentStatus.COMPLETED:      None,
    PaymentStatus.CANCELLED:      None,
}

# При смене этих полей — автоматически меняется статус
STATUS_TRIGGERS: dict[str, PaymentStatus] = {
    "invoice_id": PaymentStatus.PENDING_PAY,
    "pdf_path":   PaymentStatus.PENDING_REVIEW,
    "tx_hash":    PaymentStatus.PENDING_REVIEW,
}


def _deadline_for(status: PaymentStatus) -> datetime | None:
    """Возвращает время истечения для статуса или None."""
    minutes = DEADLINES.get(status)
    return datetime.utcnow() + timedelta(minutes=minutes) if minutes else None


class PaymentRepository:
    def __init__(self, db):
        self.db = db

    # ─── UPSERT ──────────────────────────────────────────────────────────────

    async def upsert_payment(self, payment_id: int = None, **kwargs) -> Payment:
        """
        Создаёт или обновляет платёж.
        При смене статуса — автоматически проставляет дедлайн.
        При установке invoice_id, pdf_path или tx_hash — автоматически меняет статус.
        """
        async with self.db.async_session() as session, session.begin():
            payment = await self._get(session, payment_id) if payment_id else None

            # Проверяем триггеры автосмены статуса
            for field, auto_status in STATUS_TRIGGERS.items():
                if field in kwargs and kwargs[field] is not None:
                    if "status" not in kwargs:
                        kwargs["status"] = auto_status

            # Автоматически проставляем дедлайн при смене статуса
            if "status" in kwargs:
                kwargs["deadline"] = _deadline_for(kwargs["status"])

            if payment:
                for key, value in kwargs.items():
                    setattr(payment, key, value)
            else:
                payment = Payment(**kwargs)
                session.add(payment)

            await session.flush()
            await session.refresh(payment)
            return payment

    # ─── GET ─────────────────────────────────────────────────────────────────

    async def get_by_id(self, payment_id: int) -> Optional[Payment]:
        """Возвращает платёж по ID."""
        async with self.db.async_session() as session:
            return await self._get(session, payment_id)

    async def get_by_status(self, user_id: int, status: PaymentStatus | list[PaymentStatus], many: bool = False) -> Payment | list[Payment] | None:
        """Возвращает платёж(и) пользователя по статусу или списку статусов."""
        statuses = status if isinstance(status, list) else [status]
        async with self.db.async_session() as session:
            result = (await session.execute(
                select(Payment).where(
                    Payment.user_id == user_id,
                    Payment.status.in_(statuses),
                )
            )).scalars()
            return result.all() if many else result.first()

    async def get_expired(self, status: PaymentStatus) -> list[Payment]:
        """Возвращает все платежи с истёкшим дедлайном по статусу."""
        async with self.db.async_session() as session:
            return (await session.execute(
                select(Payment).where(
                    Payment.status == status,
                    Payment.deadline.isnot(None),
                    Payment.deadline <= datetime.utcnow(),
                )
            )).scalars().all()

    # ─── PRIVATE ─────────────────────────────────────────────────────────────

    async def _get(self, session, payment_id: int) -> Optional[Payment]:
        return (await session.execute(
            select(Payment).where(Payment.id == payment_id)
        )).scalars().first()