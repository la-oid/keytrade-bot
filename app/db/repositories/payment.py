from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy.future import select

from ..models import Payment
from ..enums import PaymentStatus


DEADLINES: dict[PaymentStatus, int | None] = {
    PaymentStatus.PENDING_LINK:   None,   # Заказ создан, ждём ссылку от админа — без таймера
    PaymentStatus.PENDING_PAY:    15,     # Ссылка отправлена, у пользователя A мин чтобы нажать "Перевёл"
    PaymentStatus.PENDING_PDF:    10,     # Нажал "Перевёл", у него B мин чтобы прислать PDF
    PaymentStatus.FROZEN:         240,    # Заморозка на C мин, после — отмена
    PaymentStatus.PENDING_REVIEW: None,   # PDF получен, ждём проверки админа — без таймера
    PaymentStatus.COMPLETED:      None,   # Финальный успех — без таймера
    PaymentStatus.CANCELLED:      None,   # Финальная отмена — без таймера
}


def _deadline_for(status: PaymentStatus) -> datetime | None:
    minutes = DEADLINES.get(status)
    return datetime.utcnow() + timedelta(minutes=minutes) if minutes else None


class PaymentRepository:
    def __init__(self, db):
        self.db = db

    async def create_payment(self, user_id: int, amount: int, price: float, bank: str, payment_link: str | None = None) -> Payment:
        """Создаёт платёж со статусом pending_link."""
        async with self.db.async_session() as session, session.begin():
            payment = Payment(user_id=user_id, amount=amount, price=price, bank=bank, payment_link=payment_link)
            session.add(payment)
            await session.flush()
            await session.refresh(payment)
            return payment

    async def get_by_id(self, payment_id: int) -> Optional[Payment]:
        """Возвращает платёж по ID."""
        async with self.db.async_session() as session:
            return await self._get(session, payment_id)

    async def get_by_status(self, user_id: int, status: PaymentStatus, many: bool = False) -> Payment | list[Payment] | None:
        """Возвращает платёж(и) пользователя по статусу."""
        async with self.db.async_session() as session:
            result = (await session.execute(
                select(Payment).where(Payment.user_id == user_id, Payment.status == status)
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

    async def set_status(self, payment_id: int, status: PaymentStatus) -> bool:
        """Меняет статус и автоматически проставляет/обнуляет дедлайн."""
        async with self.db.async_session() as session, session.begin():
            payment = await self._get(session, payment_id)
            if not payment:
                return False
            payment.status = status
            payment.deadline = _deadline_for(status)
            return True

    async def set_payment_link(self, payment_id: int, link: str) -> bool:
        """Привязывает ссылку и переводит в статус pending_pay."""
        async with self.db.async_session() as session, session.begin():
            payment = await self._get(session, payment_id)
            if not payment:
                return False
            payment.payment_link = link
            payment.status = PaymentStatus.PENDING_PAY
            payment.deadline = _deadline_for(PaymentStatus.PENDING_PAY)
            return True
        
    async def set_pdf_path(self, payment_id: int, path: str) -> bool:
        """Привязывает PDF и переводит в статус pending_review."""
        async with self.db.async_session() as session, session.begin():
            payment = await self._get(session, payment_id)
            if not payment:
                return False
            payment.pdf_path = path
            payment.status = PaymentStatus.PENDING_REVIEW
            return True

    async def _get(self, session, payment_id: int) -> Optional[Payment]:
        return (await session.execute(select(Payment).where(Payment.id == payment_id))).scalars().first()