from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .base import BaseInlineKeyboard


class OrderKeyboards(BaseInlineKeyboard):
    """Клавиатуры раздела паёв."""

    async def order_list(self, orders: list) -> InlineKeyboardMarkup:
        """
        Список паёв — каждый одной кнопкой.
        Последней строкой кнопка 'Создать'.
        """
        rows = [
            [InlineKeyboardButton(
                text=self.texts.order.ORDER_ROW.format(
                    id=o.id,
                    total_keys=o.total_keys,
                    price_per_key=o.price_per_key,
                ),
                callback_data=f"order_info_{o.id}",
            )]
            for o in orders
        ]

        rows.append([
            InlineKeyboardButton(
                text=self.texts.order.CREATE,
                callback_data="order_create",
            )
        ])

        return InlineKeyboardMarkup(inline_keyboard=rows)

    def order_detail(self, order_id: int) -> InlineKeyboardMarkup:
        """Детали пая: кнопки Назад и Удалить."""
        return InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(
                    text=self.texts.order.BACK,
                    callback_data="order_back",
                ),
                InlineKeyboardButton(
                    text=self.texts.order.DELETE,
                    callback_data=f"order_delete_{order_id}",
                ),
            ]]
        )

    def back(self) -> InlineKeyboardMarkup:
        """Только кнопка Назад — для ошибочных состояний."""
        return InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(
                    text=self.texts.order.BACK,
                    callback_data="order_back",
                )
            ]]
        )