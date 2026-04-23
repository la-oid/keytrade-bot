from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from loguru import logger

from .base import Base
from ..repositories import UserRepository, KeyRepository, OrderRepository, PaymentRepository


class Database:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.engine = create_async_engine(self.db_url, echo=False)
        self.async_session = sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

        # Инициализация репозиториев
        self.user = UserRepository(self)
        self.key = KeyRepository(self)
        self.order = OrderRepository(self)
        self.payment = PaymentRepository(self)

    async def init(self):
        """Инициализация базы данных: создание таблиц"""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables created")

    async def dispose(self):
        """Закрытие engine при завершении работы"""
        await self.engine.dispose()
        logger.info("Database engine disposed")
