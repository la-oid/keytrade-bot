import random
from datetime import datetime, timedelta

from app.shared.constants import (
    PIE_KEYS_MIN, PIE_KEYS_MID, PIE_KEYS_MAX, PIE_KEYS_STEP,
    PIE_MIN_LIFETIME_HOURS, PIE_MAX_LIFETIME_HOURS,
)


def random_lifetime() -> datetime:
    """Случайное время истечения пая: от PIE_MIN до PIE_MAX часов от сейчас."""
    hours = random.uniform(PIE_MIN_LIFETIME_HOURS, PIE_MAX_LIFETIME_HOURS)
    return datetime.utcnow() + timedelta(hours=hours)


def random_keys_low() -> int:
    """Случайное кол-во ключей из нижнего диапазона [PIE_KEYS_MIN, PIE_KEYS_MID]."""
    low  = PIE_KEYS_MIN // PIE_KEYS_STEP
    high = PIE_KEYS_MID // PIE_KEYS_STEP
    return random.randint(low, high) * PIE_KEYS_STEP


def random_keys_high() -> int:
    """Случайное кол-во ключей из верхнего диапазона [PIE_KEYS_MID, PIE_KEYS_MAX]."""
    low  = PIE_KEYS_MID // PIE_KEYS_STEP
    high = PIE_KEYS_MAX // PIE_KEYS_STEP
    return random.randint(low, high) * PIE_KEYS_STEP


def lifetime_from_hours(hours: int) -> datetime:
    """Время истечения пая через заданное количество часов."""
    return datetime.utcnow() + timedelta(hours=hours)