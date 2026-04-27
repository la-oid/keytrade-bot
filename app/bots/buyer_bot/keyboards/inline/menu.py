from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .base import BaseInlineKeyboard
from app.shared.constants import KEY_PRICE


class MenuKeyboards(BaseInlineKeyboard):
    """Клавиатуры основного меню."""

    @property
    def profile(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=self.texts.profile.ORDERS, callback_data="my_orders")]
            ]
        )