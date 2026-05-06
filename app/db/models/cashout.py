from sqlalchemy import Column, Integer, String, DateTime, BigInteger, Numeric, ForeignKey, Float
from datetime import datetime

from ..core import Base
from ..enums import CashoutStatus


class Cashout(Base):
    __tablename__ = "cashouts"

    id               = Column(String(6), primary_key=True, index=True)                                  # Числовой код: 483920
    user_id          = Column(BigInteger, ForeignKey("users.telegram_id"), nullable=False, index=True)  # Кто создал заявку
    
    amount           = Column(Numeric(15, 2), nullable=True)                                            # Сумма вывода
    card_number      = Column(String(32), nullable=True)                                                # Номер карты
    
    network_id       = Column(String(16), nullable=True)                                                # ID крипто сети
    wallet_address   = Column(String(256), nullable=True)                                               # Адрес кошелька
    usdt_amount      = Column(Float, nullable=True)                                                     # Сумма в USDT

    status           = Column(String(20), default=CashoutStatus.PENDING, nullable=False)                # Статус заявки
    
    created_at       = Column(DateTime, default=datetime.utcnow)                                        # Дата создания
    updated_at       = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)              # Дата обновления