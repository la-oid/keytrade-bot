from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import BufferedInputFile

from app.shared import db, bots
from app.db.enums import PaymentStatus
from ..states import VerifyStates
from ..texts import Texts
from ..keyboards import InlineKeyboards

r = Router()

texts = Texts()
buttons = InlineKeyboards()


@r.callback_query(F.data == "check_payment")
async def check_payment_handler(call: CallbackQuery, state: FSMContext):
    """Проверка оплаты → просим ID пользователя."""
    await state.set_state(VerifyStates.waiting_user_id)
    await call.answer()
    await call.message.edit_text(texts.misc.ENTER_USER_ID)


@r.message(VerifyStates.waiting_user_id)
async def enter_user_id_handler(msg: Message, state: FSMContext):
    """ID введён → показываем список заказов на проверке."""
    if not msg.text.isdigit():
        await msg.answer(texts.misc.INVALID_USER_ID)
        return

    user_id = int(msg.text)
    keyboard = await buttons.verify.orders_list(user_id)
    has_orders = len(keyboard.inline_keyboard) > 0

    await state.clear()
    await msg.answer(
        texts.verify.ORDERS_LIST.format(user_id=user_id) if has_orders else texts.verify.NO_PAYMENTS,
        reply_markup=keyboard,
    )


@r.callback_query(F.data.startswith("verify_order_"))
async def verify_order_handler(call: CallbackQuery):
    """Детали заказа + кнопка подтверждения."""
    payment_id = int(call.data.split("_")[2])
    payment = await db.payment.get_by_id(payment_id)

    await call.answer()
    if not payment:
        return

    await call.message.edit_text(
        texts.verify.ORDER_DETAIL.format(
            id=payment.id,
            user_id=payment.user_id,
            bank=payment.bank,
            price=payment.price,
            amount=payment.amount,
        ),
        reply_markup=buttons.verify.confirm(payment.id),
    )


@r.callback_query(F.data.startswith("verify_confirm_"))
async def verify_confirm_handler(call: CallbackQuery):
    """Подтверждение оплаты → COMPLETED + уведомление пользователю с ключами."""
    payment_id = int(call.data.split("_")[2])
    payment = await db.payment.get_by_id(payment_id)

    await call.answer()
    if not payment or payment.status != PaymentStatus.PENDING_REVIEW:
        return

    # Переводим в COMPLETED
    await db.payment.set_status(payment.id, PaymentStatus.COMPLETED)

    # Уведомляем админа
    await call.message.edit_text(texts.verify.PAYMENT_CONFIRMED)

    # Генерируем файл с ключами (пока заглушка)
    keys_text = "\n".join(f"key_{i:05d}" for i in range(payment.amount))
    file = BufferedInputFile(keys_text.encode("utf-8"), filename=f"keys_order_{payment.id}.txt")

    # Отправляем покупателю файл с подписью
    await bots.buyer.bot.send_document(
        chat_id=payment.user_id,
        document=file,
        caption=texts.verify.PAYMENT_COMPLETED,
    )
