from sqlalchemy import Column, Integer, String, Boolean, DateTime, BigInteger, Numeric
from datetime import datetime

from ..core import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)           # Уникальный Telegram ID
    username = Column(String, nullable=True)                                            # Username Telegram
    first_name = Column(String(255), nullable=False)                                    # Имя пользователя
    last_name = Column(String(255), nullable=True)                                      # Фамилия пользователя
    is_active = Column(Boolean, default=True)                                           # Активен ли пользователь
    is_blocked = Column(Boolean, default=False)                                         # Заблокирован ли пользователь
    completed_orders_count = Column(Integer, default=0)                                 # Кол-во выполненных заказов 
    balance = Column(Numeric(15, 2), default=0)                                         # Баланс пользователя
    frozen_balance = Column(Numeric(15, 2), default=0)                                  # Замороженный баланс
    first_offer_sent = Column(Boolean, default=False)                                   # Отправлено ли первое спецпредложение
    created_at = Column(DateTime, default=datetime.utcnow)                              # Дата создания записи
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)    # Дата обновления записи
