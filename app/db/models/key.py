from sqlalchemy import Column, Integer, String, Boolean, DateTime, BigInteger, ForeignKey
from datetime import datetime

from ..core import Base


class Key(Base):
    __tablename__ = "keys"

    id = Column(Integer, primary_key=True, index=True)
    key_value = Column(String(255), unique=True, nullable=False, index=True)            # Сам ключ
    owner_id = Column(BigInteger, ForeignKey("users.telegram_id"), nullable=False)      # Кто купил ключ
    is_sold = Column(Boolean, default=False)                                            # Продан ли ключ
    created_at = Column(DateTime, default=datetime.utcnow)                              # Дата создания записи
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)    # Дата обновления записи