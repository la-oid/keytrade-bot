from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.shared import db
from .base import BaseInlineKeyboard


class MenuKeyboards(BaseInlineKeyboard):
    """Клавиатуры основного меню."""

    async def profile(self, user_id: int) -> InlineKeyboardMarkup:
        """Кнопки профиля. Кнопка 'Спец предложение' — только если есть активный оффер."""
        rows = [
            [InlineKeyboardButton(
                text=self.texts.profile.ORDERS,
                callback_data="my_orders",
            )]
        ]

        offer = await db.special_offer.get_active(user_id)
        if offer:
            rows.append([InlineKeyboardButton(
                text=self.texts.profile.SPECIAL_OFFER,
                callback_data="offer_view",
            )])

        return InlineKeyboardMarkup(inline_keyboard=rows)