from datetime import datetime, timedelta

MSK_OFFSET = timedelta(hours=3)

def to_msk(dt: datetime) -> datetime:
    """Конвертирует UTC время в МСК (+3)."""
    return dt + MSK_OFFSET

def msk_now() -> datetime:
    """Текущее время в МСК."""
    return datetime.utcnow() + MSK_OFFSET