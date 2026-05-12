from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.shared import settings
from app.shared.constants import TELEGRAM_URL
from .base import BaseInlineKeyboard


class MenuKeyboards(BaseInlineKeyboard):
    """Клавиатуры основного меню."""

    @property
    def support(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text=self.texts.menu.CONTACT_SUPPORT,
                    url=TELEGRAM_URL + settings.app.SUPPORT_USERNAME,
                )],
            ]
        )