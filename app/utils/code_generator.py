import random
import string


def generate_payment_code() -> str:
    """Генерирует буквенно-цифровой код для платежа: 7 символов, буквы+цифры. Пример: N394E36"""
    chars = string.ascii_uppercase + string.digits
    return "".join(random.choices(chars, k=7))


def generate_numeric_code(length: int = 6) -> str:
    """Генерирует числовой код заданной длины. Пример: 483920"""
    return str(random.randint(10 ** (length - 1), 10 ** length - 1))


async def generate_unique_code(session, model, generator_func) -> str:
    """Генерирует уникальный код для модели с retry при коллизии."""

    from sqlalchemy.future import select

    for _ in range(10):
        code = generator_func()

        exists = (
            await session.execute( select(model).where(model.id == code) )
        ).scalars().first()

        if not exists:
            return code
        
    raise RuntimeError("Не удалось сгенерировать уникальный код")