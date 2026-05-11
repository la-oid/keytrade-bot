from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from ..core import Base
from ..enums.tender import TenderStatus


class Tender(Base):
    __tablename__ = "tenders"

    id           = Column(Integer, primary_key=True, autoincrement=True)
    total_keys   = Column(Integer, nullable=False)                                        # Максимальная ёмкость
    current_keys = Column(Integer, nullable=False, default=0)                             # Текущее заполнение
    status       = Column(String, nullable=False, default=TenderStatus.queued)            # Статус тендера
    created_at   = Column(DateTime, default=datetime.utcnow)                              # Дата создания
    completed_at = Column(DateTime, nullable=True)                                        # Дата завершения
