from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .base import BaseInlineKeyboard


class MenuKeyboards(BaseInlineKeyboard):
    """Клавиатуры основного меню."""

    @property
    def start(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=self.texts.menu.PROFILE, callback_data="profile")],
                [InlineKeyboardButton(text=self.texts.menu.MEDIUM_WHOLESALE, callback_data="medium_wholesale")],
                [InlineKeyboardButton(text=self.texts.menu.LARGE_WHOLESALE, callback_data="large_wholesale")],
                [InlineKeyboardButton(text=self.texts.menu.ABOUT, callback_data="about")],
                [InlineKeyboardButton(text=self.texts.menu.SUPPORT, callback_data="support")],
            ]
        )