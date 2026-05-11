from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .base import BaseInlineKeyboard


class BroadcastKeyboards(BaseInlineKeyboard):
    """Клавиатуры раздела рассылки."""

    def confirm(self) -> InlineKeyboardMarkup:
        """Подтверждение отправки — Да / Ввести заново."""
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text=self.texts.broadcast.CONFIRM,
                    callback_data="broadcast_confirm",
                )],
                [InlineKeyboardButton(
                    text=self.texts.broadcast.RETRY,
                    callback_data="broadcast_retry",
                )],
            ]
        )
