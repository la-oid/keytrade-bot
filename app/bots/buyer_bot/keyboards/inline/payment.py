from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .base import BaseInlineKeyboard
from app.shared.constants import BANKS


class PaymentKeyboards(BaseInlineKeyboard):

    @property
    def choose_method(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=self.texts.payment.SPB, callback_data="pay_spb")],
                [InlineKeyboardButton(text=self.texts.misc.BACK, callback_data="back_to_menu")],
            ]
        )

    @property
    def choose_bank(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=bank, callback_data=f"bank_{bank.lower()}")
                    for bank in BANKS
                ],
                [InlineKeyboardButton(text=self.texts.misc.BACK, callback_data="pay_spb")],
            ]
        )
    
    @property
    def cancel_only(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=self.texts.payment.CANCEL_ACTIVE, callback_data="cancel_active")],
                [InlineKeyboardButton(text=self.texts.misc.BACK, callback_data="back_to_menu")],
            ]
        )
