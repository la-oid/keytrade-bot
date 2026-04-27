from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from .base import BaseReplyKeyboard


class MenuReplyKeyboards(BaseReplyKeyboard):
    """Reply-клавиатуры — всегда видны внизу экрана."""

    @property
    def menu(self) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=self.texts.menu.PROFILE)],
                [KeyboardButton(text=self.texts.menu.MARKET)],
                [
                    KeyboardButton(text=self.texts.menu.ABOUT),
                    KeyboardButton(text=self.texts.menu.SUPPORT),
                ],
            ],
            resize_keyboard=True,
        )