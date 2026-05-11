import random
from datetime import datetime, timedelta

from app.shared.constants import PIE_MIN_LIFETIME_HOURS, PIE_MAX_LIFETIME_HOURS


def random_lifetime() -> datetime:
    """Случайное время истечения пая: от PIE_MIN до PIE_MAX часов от сейчас."""
    hours = random.uniform(PIE_MIN_LIFETIME_HOURS, PIE_MAX_LIFETIME_HOURS)
    return datetime.utcnow() + timedelta(hours=hours)


def lifetime_from_hours(hours: int) -> datetime:
    """Время истечения пая через заданное количество часов."""
    return datetime.utcnow() + timedelta(hours=hours)