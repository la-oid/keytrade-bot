from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .base import BaseInlineKeyboard


class MenuKeyboards(BaseInlineKeyboard):
    """Клавиатуры основного меню."""
    
    @property
    def start(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=self.texts.menu.GET_LINK, callback_data="get_link")],
                [InlineKeyboardButton(text=self.texts.menu.CHECK_PAYMENT, callback_data="check_payment")],
            ]
        )