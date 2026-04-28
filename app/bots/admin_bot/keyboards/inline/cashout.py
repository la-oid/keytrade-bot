from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .base import BaseInlineKeyboard


class CashoutKeyboards(BaseInlineKeyboard):
    """Клавиатуры раздела заявок на выплату."""

    def cashout_list(self, cashouts: list) -> InlineKeyboardMarkup:
        """Список pending-заявок — каждая одной кнопкой."""
        rows = [
            [InlineKeyboardButton(
                text=self.texts.cashout.CASHOUT_ROW.format(
                    id=c.id,
                    amount=c.amount,
                ),
                callback_data=f"cashout_detail_{c.id}",
            )]
            for c in cashouts
        ]
        return InlineKeyboardMarkup(inline_keyboard=rows)

    def cashout_detail(self, cashout_id: int) -> InlineKeyboardMarkup:
        """Детали заявки: Выполнен и Назад."""
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text=self.texts.cashout.COMPLETE,
                    callback_data=f"cashout_complete_{cashout_id}",
                )],
                [InlineKeyboardButton(
                    text=self.texts.misc.BACK,
                    callback_data="cashout_back",
                )],
            ]
        )