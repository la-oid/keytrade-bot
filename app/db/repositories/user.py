from typing import Optional
from sqlalchemy.future import select

from ..models import User


class UserRepository:
    def __init__(self, db):
        self.db = db

    async def upsert_user(self, telegram_id: int, **kwargs) -> User:
        """
        Создаёт или обновляет пользователя по telegram_id.
        Пустые строки в kwargs преобразуются в None.
        """
        kwargs = {k: None if v == "" else v for k, v in kwargs.items()}
        
        async with self.db.async_session() as session:
            async with session.begin():
                user = await self._get_user(session, telegram_id)

                if user:
                    # Обновляем поля существующего пользователя
                    for key, value in kwargs.items():
                        setattr(user, key, value)
                else:
                    # Создаём нового пользователя
                    user = User(telegram_id=telegram_id, **kwargs)
                    session.add(user)

                await session.flush()
                await session.refresh(user)
                return user


    async def get_user_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """
        Возвращает пользователя по telegram_id или None.
        """
        async with self.db.async_session() as session:
            return await self._get_user(session, telegram_id)


    async def delete_user(self, telegram_id: int) -> bool:
        """
        Удаляет пользователя по telegram_id.
        Возвращает True - успешно, False - пользователь не найден.
        """
        async with self.db.async_session() as session:
            async with session.begin():
                user = await self._get_user(session, telegram_id)
                if not user:
                    return False
                await session.delete(user)
                return True
            

    async def _get_user(self, session, telegram_id: int) -> Optional[User]:
        """
        Приватный метод для получения пользователя по telegram_id.
        """
        return (await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )).scalars().first()
