from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.types import BufferedInputFile

from app.shared import db
from app.db.enums import PaymentStatus
from ..texts import Texts
from ..keyboards import InlineKeyboards

r = Router()

texts = Texts()
buttons = InlineKeyboards()


@r.callback_query(F.data == "my_orders")
async def my_orders_handler(call: CallbackQuery, user):
    """Список заказов пользователя."""
    keyboard = await buttons.profile.orders_list(user.telegram_id)
    has_orders = len(keyboard.inline_keyboard) > 1  # больше одной кнопки = есть заказы

    await call.answer()
    await call.message.edit_text(
        texts.profile.ORDERS_LIST if has_orders else texts.profile.NO_ORDERS,
        reply_markup=keyboard,
    )


@r.callback_query(F.data.startswith("order_"))
async def order_detail_handler(call: CallbackQuery):
    payment_id = int(call.data.split("_")[1])
    payment = await db.payment.get_by_id(payment_id)

    await call.answer()
    if not payment:
        return

    if payment.status == PaymentStatus.PENDING_REVIEW:
        await call.message.edit_text(
            texts.profile.ORDER_PENDING,
            reply_markup=buttons.profile.order_pending,
        )
    elif payment.status == PaymentStatus.COMPLETED:
        # Удаляем старое сообщение и шлём документ с подписью + кнопкой
        await call.message.delete()

        keys_text = "\n".join(f"key_{i:05d}" for i in range(payment.amount))
        file = BufferedInputFile(keys_text.encode("utf-8"), filename=f"keys_order_{payment.id}.txt")

        await call.message.answer_document(
            document=file,
            caption=texts.profile.ORDER_COMPLETED.format(amount=payment.amount),
            reply_markup=buttons.profile.back_to_orders,
        )