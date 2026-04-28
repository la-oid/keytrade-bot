from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .base import BaseInlineKeyboard


class MarketKeyboards(BaseInlineKeyboard):
    """Клавиатуры площадки заказов."""

    def order_list(self, orders: list) -> InlineKeyboardMarkup:
        """Список свободных паёв — каждый одной кнопкой."""
        rows = [
            [InlineKeyboardButton(
                text=self.texts.market.ORDER_ROW.format(
                    id=o.id,
                    total_keys=o.total_keys,
                ),
                callback_data=f"market_take_{o.id}",
            )]
            for o in orders
        ]
        return InlineKeyboardMarkup(inline_keyboard=rows)

    def confirm(self, order_id: int) -> InlineKeyboardMarkup:
        """Принять / Подумаю."""
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text=self.texts.market.ACCEPT,
                    callback_data=f"market_accept_{order_id}",
                )],
                [InlineKeyboardButton(
                    text=self.texts.market.REJECT,
                    callback_data="market_back",
                )],
            ]
        )