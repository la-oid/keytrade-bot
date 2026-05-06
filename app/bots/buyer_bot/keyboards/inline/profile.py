from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.shared import db, settings
from app.shared.constants import TELEGRAM_URL
from app.db.enums import PaymentStatus
from .base import BaseInlineKeyboard


VISIBLE_STATUSES = [PaymentStatus.COMPLETED, PaymentStatus.PENDING_REVIEW]


class ProfileKeyboards(BaseInlineKeyboard):
    """Клавиатуры профиля и заказов."""

    async def orders_list(self, user_id: int) -> InlineKeyboardMarkup:
        """Сама подтягивает заказы пользователя из БД."""
        payments = await db.payment.get_by_status(user_id, VISIBLE_STATUSES, many=True)
        rows = [
            [InlineKeyboardButton(
                text=self.texts.profile.ORDER.format(id=p.id, amount=p.amount, price=p.price),
                callback_data=f"order_{p.id}",
            )]
            for p in payments
        ]
        rows.append([InlineKeyboardButton(text=self.texts.misc.BACK, callback_data="profile")])
        return InlineKeyboardMarkup(inline_keyboard=rows)
    
    @property
    def order_pending(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=self.texts.profile.SUPPORT, url = TELEGRAM_URL + settings.app.SUPPORT_USERNAME )],
                [InlineKeyboardButton(text=self.texts.misc.BACK, callback_data="my_orders")],
            ]
        )

    @property
    def back_to_orders(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=self.texts.misc.BACK, callback_data="my_orders")],
            ]
        )