from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .base import BaseInlineKeyboard
from app.shared import settings


class CashoutKeyboards(BaseInlineKeyboard):
    """Клавиатуры вывода средств."""

    def amount_choice(self) -> InlineKeyboardMarkup:
        """Выбор суммы вывода."""
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text=self.texts.cashout.ALL_AMOUNT,
                    callback_data="cashout_all",
                )],
                [InlineKeyboardButton(
                    text=self.texts.cashout.CUSTOM_AMOUNT,
                    callback_data="cashout_custom",
                )],
                [InlineKeyboardButton(
                    text=self.texts.misc.BACK,
                    callback_data="profile",
                )],
            ]
        )

    def method_choice(self) -> InlineKeyboardMarkup:
        """Выбор метода получения."""
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text=self.texts.cashout.CARD,
                    callback_data="cashout_card",
                )],
                [InlineKeyboardButton(
                    text=self.texts.misc.BACK,
                    callback_data="cashout_back_to_amount",
                )],
            ]
        )
    
    def status_actions(self) -> InlineKeyboardMarkup:
        """Кнопки после показа статуса заявки: Поддержка и Назад."""
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text=self.texts.cashout.SUPPORT,
                    url=settings.app.SUPPORT_URL,
                )],
                [InlineKeyboardButton(
                    text=self.texts.misc.BACK,
                    callback_data="profile",
                )],
            ]
        )