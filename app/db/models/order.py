from sqlalchemy import Column, Integer, Boolean, DateTime, Numeric
from datetime import datetime

from ..core import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    total_keys = Column(Integer, nullable=False)                                        # Всего ключей в тендере
    is_fake = Column(Boolean, default=False, nullable=False)                            # Фейковый тендер (для объёма)
    is_active = Column(Boolean, default=True, nullable=False)                           # Открыт ли тендер
    expires_at = Column(DateTime, nullable=False)                                       # Время жизни тендера
    created_at = Column(DateTime, default=datetime.utcnow)                              # Дата создания
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)    # Дата обновления