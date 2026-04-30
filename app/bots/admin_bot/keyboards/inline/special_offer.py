from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .base import BaseInlineKeyboard


class SpecialOfferKeyboards(BaseInlineKeyboard):
    """Клавиатуры спецпредложений в admin_bot."""

    def confirm(self) -> InlineKeyboardMarkup:
        """Подтверждение отправки — Да / Нет (ввести заново)."""
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text=self.texts.special_offer.CONFIRM,
                    callback_data="special_offer_confirm",
                )],
                [InlineKeyboardButton(
                    text=self.texts.special_offer.RETRY,
                    callback_data="special_offer_retry",
                )],
            ]
        )