from sqlalchemy import Column, Integer, Boolean, DateTime, BigInteger, Numeric, ForeignKey
from datetime import datetime

from ..core import Base


class Tender(Base):
    __tablename__ = "tenders"

    id = Column(Integer, primary_key=True, index=True)
    total_keys = Column(Integer, nullable=False)                                        # Всего ключей в тендере
    remaining_keys = Column(Integer, nullable=False)                                    # Сколько ключей осталось продать
    price_per_key = Column(Numeric(15, 2), nullable=False)                              # Цена за один ключ
    is_active = Column(Boolean, default=True)                                           # Открыт ли тендер
    created_at = Column(DateTime, default=datetime.utcnow)                              # Дата создания записи
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)    # Дата обновления записи