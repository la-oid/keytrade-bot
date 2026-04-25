from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.shared import db
from app.db.enums import PaymentStatus
from .base import BaseInlineKeyboard


class VerifyKeyboards(BaseInlineKeyboard):
    """Клавиатуры раздела проверки оплаты."""

    async def orders_list(self, user_id: int) -> InlineKeyboardMarkup:
        """Список заказов пользователя на проверке."""
        payments = await db.payment.get_by_status(user_id, PaymentStatus.PENDING_REVIEW, many=True)
        rows = [
            [InlineKeyboardButton(
                text=self.texts.verify.ORDER.format(id=p.id, amount=p.amount, price=p.price),
                callback_data=f"verify_order_{p.id}",
            )]
            for p in payments
        ]
        rows.append([InlineKeyboardButton(text=self.texts.misc.BACK, callback_data="back_to_menu")])
        return InlineKeyboardMarkup(inline_keyboard=rows)

    def confirm(self, payment_id: int) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text=self.texts.verify.PAYMENT_OK,
                    callback_data=f"verify_confirm_{payment_id}",
                )],
                [InlineKeyboardButton(text=self.texts.misc.BACK, callback_data="back_to_menu")],
            ]
        )