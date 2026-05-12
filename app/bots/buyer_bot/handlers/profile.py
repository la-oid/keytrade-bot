from aiogram import Router, F
from aiogram.types import CallbackQuery, BufferedInputFile, FSInputFile

from app.shared import db
from app.shared.images import BuyerImages
from app.services import key_service
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
    has_orders = len(keyboard.inline_keyboard) > 1

    await call.answer()

    text = texts.profile.ORDERS_LIST if has_orders else texts.profile.NO_ORDERS

    # Если сообщение с документом или фото — удаляем и шлём новое
    if call.message.document or call.message.photo:
        await call.message.delete()
        await call.message.answer(text, reply_markup=keyboard)
    else:
        await call.message.edit_text(text, reply_markup=keyboard)


@r.callback_query(F.data.startswith("order_"))
async def order_detail_handler(call: CallbackQuery):
    payment_id = call.data.split("_")[1]
    payment = await db.payment.get_by_id(payment_id)

    await call.answer()
    if not payment:
        return

    if payment.status == PaymentStatus.PENDING_REVIEW:
        await call.message.delete()
        await call.message.answer_photo(
            photo=FSInputFile(BuyerImages.ORDER_PENDING),
            caption=texts.profile.ORDER_PENDING,
            reply_markup=buttons.profile.order_pending,
        )
    elif payment.status == PaymentStatus.COMPLETED:
        await call.message.delete()
        await call.message.answer_photo(
            photo=FSInputFile(BuyerImages.ORDER_COMPLETED),
            caption=texts.profile.ORDER_COMPLETED.format(amount=payment.amount),
        )
        content, filename = await key_service.get_keys_file(payment.id)
        await call.message.answer_document(
            document=BufferedInputFile(content, filename=filename),
            reply_markup=buttons.profile.back_to_orders,
        )
