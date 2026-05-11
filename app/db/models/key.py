from sqlalchemy import Column, Integer, String, DateTime, BigInteger, ForeignKey
from datetime import datetime

from ..core import Base


class Key(Base):
    __tablename__ = "keys"

    id          = Column(Integer, primary_key=True, index=True)
    key_value   = Column(String(255), unique=True, nullable=False, index=True)                # Сам ключ
    owner_id    = Column(BigInteger, ForeignKey("users.telegram_id"), nullable=False)         # Кто купил ключ
    payment_id  = Column(String(7), ForeignKey("payments.id"), nullable=False, index=True)    # К какому платежу привязан (откуда взялся)
    order_id    = Column(String(6), ForeignKey("orders.id"), nullable=True, index=True)       # В какой заказ продан (NULL = не продан)
    created_at  = Column(DateTime, default=datetime.utcnow)                                   # Дата создания записи
    updated_at  = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)         # Дата обновления записи