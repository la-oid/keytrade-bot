import random
from datetime import datetime, timedelta

from app.shared.constants import (
    PIE_MIN_KEYS, PIE_MAX_KEYS, PIE_STEP,
    PIE_MIN_LIFETIME_HOURS, PIE_MAX_LIFETIME_HOURS,
    PIE_FAKE_PRICE_MIN, PIE_FAKE_PRICE_MAX, PIE_FAKE_PRICE_STEP,
)


def random_lifetime() -> datetime:
    """Случайное время истечения пая: от PIE_MIN до PIE_MAX часов от сейчас."""
    hours = random.uniform(PIE_MIN_LIFETIME_HOURS, PIE_MAX_LIFETIME_HOURS)
    return datetime.utcnow() + timedelta(hours=hours)


def random_keys_count() -> int:
    """Случайное количество ключей в диапазоне [PIE_MIN_KEYS, PIE_MAX_KEYS], кратно PIE_STEP."""
    steps = (PIE_MAX_KEYS - PIE_MIN_KEYS) // PIE_STEP
    return PIE_MIN_KEYS + random.randint(0, steps) * PIE_STEP


def random_price() -> float:
    """Случайная цена ключа для фейкового пая."""
    return float(random.randrange(PIE_FAKE_PRICE_MIN, PIE_FAKE_PRICE_MAX + 1, PIE_FAKE_PRICE_STEP))


def validate_keys_count(value: int) -> bool:
    """Проверяет что значение в допустимом диапазоне и кратно шагу."""
    return PIE_MIN_KEYS <= value <= PIE_MAX_KEYS and value % PIE_STEP == 0

def lifetime_from_hours(hours: int) -> datetime:
    """Время истечения пая через заданное количество часов."""
    return datetime.utcnow() + timedelta(hours=hours)