from typing import Optional
from sqlalchemy.future import select

from ..models import Order


class OrderRepository:
    def __init__(self, db):
        self.db = db

    async def create_order(self, keys_count: int, price_per_key: float) -> Order:
        """
        Создаёт новый заказ на фиксированное количество ключей.
        Вызывается админом при добавлении заказа через админ-бот.
        """
        async with self.db.async_session() as session:
            async with session.begin():
                # Создаём запись заказа в БД
                order = Order(
                    keys_count=keys_count,
                    price_per_key=price_per_key,
                    is_completed=False
                )
                session.add(order)
                await session.flush()
                await session.refresh(order)
                return order


    async def get_order_by_id(self, order_id: int) -> Optional[Order]:
        """
        Возвращает заказ по ID или None, если не найден.
        """
        async with self.db.async_session() as session:
            return await self._get_order(session, order_id)


    async def get_active_orders(self) -> list[Order]:
        """
        Возвращает все невыполненные заказы для отображения на площадке.
        """
        async with self.db.async_session() as session:
            return (await session.execute(
                select(Order).where(Order.is_completed == False)
            )).scalars().all()


    async def complete_order(self, order_id: int, user_telegram_id: int) -> Optional[Order]:
        """
        Закрывает заказ: помечает как выполненный и записывает исполнителя.
        Вызывается после успешной проверки ключей пользователя.
        Возвращает обновлённый заказ или None (если заказ не найден или уже выполнен).
        """
        async with self.db.async_session() as session:
            async with session.begin():
                order = await self._get_order(session, order_id)
                # Если заказ не найден или уже выполнен - ничего не делаем
                if not order or order.is_completed:
                    return None
                order.is_completed = True
                order.completed_by = user_telegram_id
                await session.flush()
                await session.refresh(order)
                return order


    async def delete_order(self, order_id: int) -> bool:
        """
        Удаляет заказ по ID.
        Возвращает True - успешно, False - заказ не найден.
        """
        async with self.db.async_session() as session:
            async with session.begin():
                order = await self._get_order(session, order_id)
                if not order:
                    return False
                await session.delete(order)
                return True


    async def _get_order(self, session, order_id: int) -> Optional[Order]:
        """
        Приватный метод для получения заказа по ID.
        """
        return (await session.execute(
            select(Order).where(Order.id == order_id)
        )).scalars().first()