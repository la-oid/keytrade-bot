from enum import Enum


class PaymentStatus(str, Enum):
    PENDING_LINK   = "pending_link"    # Заказ создан, ждём ссылку от админа
    PENDING_PAY    = "pending_pay"     # Ссылка отправлена, ждём оплату
    PENDING_HASH   = "pending_hash"    # Нажал "Я оплатил", ожидает хэш транзакции (крипта)
    PENDING_PDF    = "pending_pdf"     # Нажал "Перевёл", ждём PDF
    PENDING_REVIEW = "pending_review"  # PDF получен, ждём подтверждения админа
    CANCELLED      = "cancelled"       # Отменён пользователем
    COMPLETED      = "completed"       # Успешно завершён