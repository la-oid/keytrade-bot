from sqlalchemy import Column, Integer, String, DateTime, BigInteger, Numeric, ForeignKey, Float
from datetime import datetime

from ..core import Base
from ..enums import PaymentStatus


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.telegram_id"), nullable=False, index=True)       # Telegram ID пользователя
    
    amount = Column(Integer, nullable=False)                                                        # Количество ключей
    price = Column(Numeric(15, 2), nullable=True)                                                   # Сумма к оплате
    
    bank = Column(String(50), nullable=True)                                                        # Банк (Сбербанк/Тинькофф)
    payment_link = Column(String(512), nullable=True)                                               # URL страницы оплаты
    pdf_path = Column(String(512), nullable=True)                                                   # Путь к сохранённому PDF
    
    network_id = Column(String(16), nullable=True)                                                  # ID крипто сети
    usdt_amount = Column(Float, nullable=True)                                                      # Сумма в USDT
    tx_hash = Column(String(256), nullable=True)                                                    # Хэш транзакции
    
    special_offer_id = Column(Integer, ForeignKey("special_offers.id"), nullable=True)              # ID специального предложения
    status = Column(String(20), default=PaymentStatus.PENDING_LINK)                                 # Статус платежа
    deadline = Column(DateTime, nullable=True)                                                      # Время истечения текущего статуса
    
    created_at = Column(DateTime, default=datetime.utcnow)                                          # Дата создания
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)                # Дата обновления
