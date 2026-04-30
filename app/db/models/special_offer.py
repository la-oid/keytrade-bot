from tokenize import String

from sqlalchemy import Column, Integer, Boolean, DateTime, BigInteger, ForeignKey, String
from datetime import datetime

from ..core import Base


class SpecialOffer(Base):
    __tablename__ = "special_offers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.telegram_id"), nullable=False, unique=True, index=True)  # Один оффер на юзера
    keys_count = Column(Integer, nullable=False)                                                            # Кол-во ключей в предложении
    custom_text = Column(String, nullable=True)                                                             # Кастомный текст предложения (опционально)
    expires_at = Column(DateTime, nullable=False)                                                           # До когда действует
    is_active = Column(Boolean, default=True, nullable=False)                                               # Активно или нет
    created_at = Column(DateTime, default=datetime.utcnow)                                                  # Дата создания