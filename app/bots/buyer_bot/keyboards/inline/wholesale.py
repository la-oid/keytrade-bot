from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.shared.constants import KEY_PRICE_BUYER
from .base import BaseInlineKeyboard


class WholesaleKeyboards(BaseInlineKeyboard):
    """Клавиатуры для оптовых заказов."""

    def wholesale(self, amount: int, step: int) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=self.texts.wholesale.AMOUNT_MINUS.format(step=step), callback_data="amount_minus"),
                    InlineKeyboardButton(text=self.texts.wholesale.AMOUNT_PLUS.format(step=step), callback_data="amount_plus"),
                ],
                [InlineKeyboardButton(text=self.texts.wholesale.CONFIRM_ORDER.format(price=amount * KEY_PRICE_BUYER), callback_data="confirm_order")]
            ]
        )
