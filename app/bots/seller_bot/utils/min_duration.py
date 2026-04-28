import asyncio
import time
from functools import wraps


def min_duration(seconds: float):
    """Декоратор: гарантирует что хендлер выполнится не быстрее чем за N секунд."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            started = time.monotonic()
            result = await func(*args, **kwargs)
            elapsed = time.monotonic() - started
            if elapsed < seconds:
                await asyncio.sleep(seconds - elapsed)
            return result
        return wrapper
    return decorator