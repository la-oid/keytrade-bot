from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.shared import db, settings
from app.shared.constants import TELEGRAM_URL
from .base import BaseInlineKeyboard


class MenuKeyboards(BaseInlineKeyboard):
    """Клавиатуры основного меню."""

    async def profile(self, user_id: int) -> InlineKeyboardMarkup:
        """Кнопки профиля. Кнопка 'Спец предложение' — только если есть активный оффер."""
        rows = []
    
        offer = await db.special_offer.get_active(user_id)
        if offer:
            rows.append([InlineKeyboardButton(
                text=self.texts.profile.SPECIAL_OFFER,
                callback_data="offer_view",
            )])
    
        rows.append([InlineKeyboardButton(
            text=self.texts.profile.ORDERS,
            callback_data="my_orders",
        )])

        return InlineKeyboardMarkup(inline_keyboard=rows)

    @property
    def support(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text=self.texts.menu.CONTACT_SUPPORT,
                    url=TELEGRAM_URL + settings.app.SUPPORT_USERNAME,
                )],
            ]
        )
