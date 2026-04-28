from enum import Enum


class CashoutStatus(str, Enum):
    PENDING   = "pending"     # Создана, ждёт перевода от админа
    CANCELLED = "cancelled"   # Отменена
    COMPLETED = "completed"   # Завершена