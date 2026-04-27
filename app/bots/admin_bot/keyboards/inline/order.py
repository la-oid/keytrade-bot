from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .base import BaseInlineKeyboard


class OrderKeyboards(BaseInlineKeyboard):
    """Клавиатуры раздела паёв."""

    def order_menu(self) -> InlineKeyboardMarkup:
        """Главное меню паёв: Создать и Удалить."""
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=self.texts.order.CREATE, callback_data="order_create")],
                [InlineKeyboardButton(text=self.texts.order.DELETE, callback_data="order_delete_menu")],
            ]
        )

    def delete_list(self, orders: list) -> InlineKeyboardMarkup:
        """Список паёв для удаления — каждый одной кнопкой."""
        rows = [
            [InlineKeyboardButton(
                text=self.texts.order.ORDER_ROW.format(
                    id=o.id,
                    total_keys=o.total_keys,
                    price_per_key=o.price_per_key,
                ),
                callback_data=f"order_delete_{o.id}",
            )]
            for o in orders
        ]
        return InlineKeyboardMarkup(inline_keyboard=rows)

    def back_to_delete_list(self) -> InlineKeyboardMarkup:
        """Назад к списку паёв на удаление."""
        return InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(
                    text=self.texts.order.BACK,
                    callback_data="order_delete_menu",
                )
            ]]
        )

    def back_to_menu(self) -> InlineKeyboardMarkup:
        """Назад к меню паёв."""
        return InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(
                    text=self.texts.order.BACK,
                    callback_data="order_back",
                )
            ]]
        )