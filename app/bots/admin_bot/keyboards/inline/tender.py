from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .base import BaseInlineKeyboard


class TenderKeyboards(BaseInlineKeyboard):
    """Клавиатуры раздела тендеров."""

    def actions(self) -> InlineKeyboardMarkup:
        """Три действия с тендером."""
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text=self.texts.tender.ADD,
                    callback_data="tender_add",
                )],
                [InlineKeyboardButton(
                    text=self.texts.tender.QUEUE,
                    callback_data="tender_queue",
                )],
                [InlineKeyboardButton(
                    text=self.texts.tender.LAUNCH,
                    callback_data="tender_launch",
                )],
            ]
        )
