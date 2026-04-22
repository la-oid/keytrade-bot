import random
import string


def _random_segment(length: int) -> str:
    """Генерирует случайный сегмент из букв и цифр"""
    chars = string.ascii_uppercase + string.digits
    return "".join(random.choices(chars, k=length))


def generate_key() -> str:
    """
    Генерирует один уникальный ключ в формате XXXX-XXXX-XXXX-XXXX.
    Пример: A1B2-C3D4-E5F6-G7H8
    """
    return "-".join(_random_segment(4) for _ in range(4))


def generate_keys(count: int) -> list[str]:
    """
    Генерирует список уникальных ключей.
    Гарантирует уникальность внутри одной генерации.
    """
    keys = set()

    while len(keys) < count:
        keys.add(generate_key())

    return list(keys)