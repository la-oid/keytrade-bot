from sqlalchemy import Column, Integer, Boolean, DateTime, BigInteger, Numeric
from datetime import datetime

from ..core import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    keys_count = Column(Integer, nullable=False)                                        # Сколько ключей нужно внести (фиксировано, без дроблений)
    price_per_key = Column(Numeric(15, 2), nullable=False)                              # Цена за один ключ
    is_completed = Column(Boolean, default=False)                                       # Выполнен ли заказ
    completed_by = Column(BigInteger, nullable=True)                                    # Telegram ID того, кто выполнил заказ
    created_at = Column(DateTime, default=datetime.utcnow)                              # Дата создания
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)    # Дата обновления