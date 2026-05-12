from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import BufferedInputFile

from app.shared import db, bots
from app.services import key_service
from app.db.enums import PaymentStatus
from app.utils import get_network_by_id
from ..states import VerifyStates
from ..texts import Texts, ButtonTexts
from ..keyboards import InlineKeyboards

r = Router()

texts = Texts()
buttons = InlineKeyboards()


@r.message(F.text == ButtonTexts.menu.CHECK_PAYMENT)
async def check_payment_handler(msg: Message, state: FSMContext):
    """Проверка оплаты → просим ID пользователя."""
    await msg.delete()
    await state.set_state(VerifyStates.waiting_user_id)
    await msg.answer(texts.misc.ENTER_USER_ID)


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
    payment_id = call.data.split("_")[2]
    payment = await db.payment.get_by_id(payment_id)

    await call.answer()
    if not payment:
        return
    
    if payment.network_id:
        network = get_network_by_id(payment.network_id)

        text = texts.verify.ORDER_DETAIL_CRYPTO.format(
            id=payment.id,
            user_id=payment.user_id,
            network=network.name if network else payment.network_id,
            price=payment.price,
            usdt_amount=payment.usdt_amount or "—",
            amount=payment.amount,
            tx_hash=payment.tx_hash or "—",
        )

    else:
        text = texts.verify.ORDER_DETAIL_SPB.format(
            id=payment.id,
            user_id=payment.user_id,
            price=payment.price,
            amount=payment.amount,
        )

    if call.message.document or call.message.photo:
        await call.message.delete()
        send = call.message.answer
    else:
        send = call.message.edit_text

    await send(text, reply_markup=buttons.verify.confirm(payment.id))


@r.callback_query(F.data.startswith("verify_confirm_"))
async def verify_confirm_handler(call: CallbackQuery):
    """Подтверждение оплаты → COMPLETED + уведомление пользователю с ключами."""
    payment_id = call.data.split("_")[2]
    payment = await db.payment.get_by_id(payment_id)

    await call.answer()
    if not payment or payment.status != PaymentStatus.PENDING_REVIEW:
        return

    # Переводим в COMPLETED
    await db.payment.upsert_payment(payment.id, status=PaymentStatus.COMPLETED)

    # Деактивируем спецпредложение если заказ был по офферу
    if payment.special_offer_id:
        await db.special_offer.deactivate(payment.user_id)

    # Сразу убираем кнопку с сообщения
    await call.message.edit_text(texts.verify.PAYMENT_CONFIRMED)
    
    # Генерируем ключи и сохраняем в БД с привязкой к платежу
    await key_service.generate_for_payment(
        owner_id=payment.user_id,
        payment_id=payment.id,
        count=payment.amount,
    )

    # Берём ключи из БД и формируем файл
    content, filename = await key_service.get_keys_file(payment.id)
    file = BufferedInputFile(content, filename=filename)

    # Отправляем покупателю файл с подписью
    await bots.buyer.bot.send_document(
        chat_id=payment.user_id,
        document=file,
        caption=texts.verify.PAYMENT_COMPLETED.format(amount=payment.amount),
    )

