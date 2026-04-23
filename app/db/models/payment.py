from sqlalchemy import Column, Integer, String, DateTime, BigInteger, Numeric, ForeignKey
from datetime import datetime

from ..core import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.telegram_id"), nullable=False, index=True)       # Telegram ID пользователя
    amount = Column(Integer, nullable=False)                                                        # Количество ключей
    price = Column(Numeric(15, 2), nullable=False)                                                  # Сумма к оплате
    bank = Column(String(50), nullable=False)                                                       # Банк (Сбербанк/Тинькофф)
    status = Column(String(20), default="pending")                                                  # pending / cancelled / completed
    created_at = Column(DateTime, default=datetime.utcnow)                                          # Дата создания
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)                # Дата обновления