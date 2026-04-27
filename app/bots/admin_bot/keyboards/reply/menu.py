from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from .base import BaseReplyKeyboard


class MenuReplyKeyboards(BaseReplyKeyboard):
    """Reply-клавиатуры — всегда видны внизу экрана."""

    @property
    def menu(self) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=self.texts.menu.GET_LINK),
                    KeyboardButton(text=self.texts.menu.CHECK_PAYMENT),
                ],
                [
                    KeyboardButton(text=self.texts.menu.CREATE_PIE),
                    KeyboardButton(text=self.texts.menu.PAYOUTS),
                ],
                [
                    KeyboardButton(text=self.texts.menu.USER_ACCOUNT),
                    KeyboardButton(text=self.texts.menu.BLOCK_USER),
                ],
                [
                    KeyboardButton(text=self.texts.menu.SPECIAL_OFFERS),
                ],
            ],
            resize_keyboard=True,
        )