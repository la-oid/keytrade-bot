from typing import Optional
from datetime import datetime
from sqlalchemy.future import select

from ..models import User


class UserRepository:
    def __init__(self, db):
        self.db = db

    # ─── CREATE / UPDATE ─────────────────────────────────────────────────────

    async def upsert_user(self, telegram_id: int, **kwargs) -> User:
        """Создаёт или обновляет пользователя по telegram_id."""
        kwargs = {k: None if v == "" else v for k, v in kwargs.items()}

        async with self.db.async_session() as session, session.begin():
            user = await self._get_user(session, telegram_id)

            if user:
                for key, value in kwargs.items():
                    setattr(user, key, value)
            else:
                user = User(telegram_id=telegram_id, **kwargs)
                session.add(user)

            await session.flush()
            await session.refresh(user)
            return user

    # ─── GET ─────────────────────────────────────────────────────────────────

    async def get_user_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """Возвращает пользователя по telegram_id или None."""
        async with self.db.async_session() as session:
            return await self._get_user(session, telegram_id)

    async def get_users_for_first_offer(self, registered_before: datetime) -> list[User]:
        """
        Возвращает пользователей которым нужно отправить первое спецпредложение:
        - зарегистрировались раньше чем registered_before
        - first_offer_sent = False
        """
        async with self.db.async_session() as session:
            return (await session.execute(
                select(User).where(
                    User.first_offer_sent == False,
                    User.created_at <= registered_before,
                )
            )).scalars().all()

    # ─── DELETE ──────────────────────────────────────────────────────────────

    async def delete_user(self, telegram_id: int) -> bool:
        """Удаляет пользователя по telegram_id."""
        async with self.db.async_session() as session, session.begin():
            user = await self._get_user(session, telegram_id)
            if not user:
                return False
            await session.delete(user)
            return True

    # ─── PRIVATE ─────────────────────────────────────────────────────────────

    async def _get_user(self, session, telegram_id: int) -> Optional[User]:
        return (await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )).scalars().first()