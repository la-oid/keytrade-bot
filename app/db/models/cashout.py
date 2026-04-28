from sqlalchemy import Column, Integer, String, DateTime, BigInteger, Numeric, ForeignKey
from datetime import datetime

from ..core import Base
from ..enums import CashoutStatus


class Cashout(Base):
    __tablename__ = "cashouts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.telegram_id"), nullable=False, index=True)   # Кто создал заявку
    amount = Column(Numeric(15, 2), nullable=False)                                             # Сумма вывода
    card_number = Column(String(32), nullable=False)                                            # Номер карты
    status = Column(String(20), default=CashoutStatus.PENDING, nullable=False)                  # Статус заявки
    created_at = Column(DateTime, default=datetime.utcnow)                                      # Дата создания
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)            # Дата обновления