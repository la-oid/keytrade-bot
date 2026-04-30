from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery


class IsNotBlocked(BaseFilter):
    async def __call__(self, event: Message | CallbackQuery, user) -> bool:
        return not user.is_blocked