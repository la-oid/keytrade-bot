from sqlalchemy import Column, Integer, String, DateTime, BigInteger, Numeric, ForeignKey, Float
from datetime import datetime

from ..core import Base


class Payment(Base):
    __tablename__ = "payments"

    id               = Column(String(7), primary_key=True, index=True)                                  # Буквенно-цифровой код: N394E36
    user_id          = Column(BigInteger, ForeignKey("users.telegram_id"), nullable=False, index=True)  # Telegram ID пользователя

    amount           = Column(Integer, nullable=False)                                                  # Количество ключей
    price            = Column(Numeric(15, 2), nullable=True)                                            # Сумма к оплате в рублях

    payment_link     = Column(String(512), nullable=True)                                               # Ссылка на оплату (cardlink)
    pdf_path         = Column(String(512), nullable=True)                                               # Путь к сохранённому PDF

    network_id       = Column(String(16), nullable=True)                                                # ID крипто сети
    usdt_amount      = Column(Float, nullable=True)                                                     # Сумма в USDT
    tx_hash          = Column(String(256), nullable=True)                                               # Хэш транзакции

    special_offer_id = Column(Integer, ForeignKey("special_offers.id"), nullable=True)                  # ID специального предложения
    status           = Column(String(20), nullable=True)                                                # Статус платежа
    deadline         = Column(DateTime, nullable=True)                                                  # Время истечения текущего статуса

    created_at       = Column(DateTime, default=datetime.utcnow)
    updated_at       = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)