from typing import Optional
from sqlalchemy.future import select

from ..models import Payment


class PaymentRepository:
    def __init__(self, db):
        self.db = db

    async def create_payment(self, user_id: int, amount: int, price: float, bank: str) -> Payment:
        """Создаёт новый платёж со статусом pending."""
        async with self.db.async_session() as session:
            async with session.begin():
                payment = Payment(user_id=user_id, amount=amount, price=price, bank=bank)
                session.add(payment)
                await session.flush()
                await session.refresh(payment)
                return payment

    async def get_pending_payment(self, user_id: int) -> Optional[Payment]:
        """Возвращает активный платёж пользователя или None."""
        async with self.db.async_session() as session:
            return (await session.execute(
                select(Payment).where(
                    Payment.user_id == user_id,
                    Payment.status == "pending"
                )
            )).scalars().first()
        
    async def set_payment_link(self, payment_id: int, link: str) -> bool:
        """Привязывает ссылку к уже созданному платежу."""
        async with self.db.async_session() as session:
            async with session.begin():
                payment = (await session.execute(
                    select(Payment).where(Payment.id == payment_id)
                )).scalars().first()
                if not payment:
                    return False
                payment.payment_link = link
                return True

    async def set_payment_link(self, payment_id: int, link: str) -> bool:
        """Привязывает ссылку к уже созданному платежу."""
        async with self.db.async_session() as session:
            async with session.begin():
                payment = (await session.execute(
                    select(Payment).where(Payment.id == payment_id)
                )).scalars().first()
                if not payment:
                    return False
                payment.payment_link = link
                return True

    async def cancel_payment(self, user_id: int) -> bool:
        """Отменяет активный платёж пользователя. Возвращает True если был найден."""
        async with self.db.async_session() as session:
            async with session.begin():
                payment = await self._get_pending(session, user_id)
                if not payment:
                    return False
                payment.status = "cancelled"
                return True

    async def complete_payment(self, payment_id: int) -> bool:
        """Помечает платёж как выполненный. Вызывается из админ-бота."""
        async with self.db.async_session() as session:
            async with session.begin():
                payment = (await session.execute(
                    select(Payment).where(Payment.id == payment_id)
                )).scalars().first()
                if not payment:
                    return False
                payment.status = "completed"
                return True

    async def _get_pending(self, session, user_id: int) -> Optional[Payment]:
        """Приватный метод для получения активного платежа."""
        return (await session.execute(
            select(Payment).where(
                Payment.user_id == user_id,
                Payment.status == "pending"
            )
        )).scalars().first()