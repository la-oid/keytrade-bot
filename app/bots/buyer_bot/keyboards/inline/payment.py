from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .base import BaseInlineKeyboard


class PaymentKeyboards(BaseInlineKeyboard):

    @property
    def choose_method(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=self.texts.payment.SPB, callback_data="pay_spb")],
                [InlineKeyboardButton(text=self.texts.crypto.CRYPTO,  callback_data="pay_crypto")],
            ]
        )
    
    @property
    def cancel_only(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=self.texts.payment.CANCEL_ACTIVE, callback_data="cancel_payment")]
            ]
        )

    @property
    def confirm_cancel(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=self.texts.payment.CHANGED_MIND, callback_data="back_to_pending")],
                [InlineKeyboardButton(text=self.texts.payment.CONFIRM_CANCEL, callback_data="cancel_active")],
            ]
        )
    
    def payment_page(self, url: str) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=self.texts.payment.OPEN_LINK, url=url)],
                [InlineKeyboardButton(text=self.texts.payment.SENT, callback_data="payment_sent")],
            ]
        )
