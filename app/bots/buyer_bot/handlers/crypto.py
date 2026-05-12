from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from app.shared import db, bots, settings
from app.shared.constants import KEY_PRICE_BUYER, CRYPTO_RATE_MARKUP_BUYER
from app.db.enums import PaymentStatus
from app.utils import get_network_by_id, get_usdt_rub_rate, notify_admins, validate_tx_hash
from ..texts import Texts
from ..keyboards import InlineKeyboards
from ..utils import create_payment_and_notify, show_active_payment

r = Router()

texts   = Texts()
buttons = InlineKeyboards()


# ─── Выбор крипты ────────────────────────────────────────────────────────────

@r.callback_query(F.data == "pay_crypto")
async def pay_crypto_handler(call: CallbackQuery, state: FSMContext):
    """Крипта → показываем список сетей с текущим курсом."""
    data = await state.get_data()
    amount = data.get("amount", 0)

    try:
        rate = await get_usdt_rub_rate() + CRYPTO_RATE_MARKUP_BUYER
    except Exception:
        await call.answer(texts.crypto.RATE_ERROR, show_alert=True)
        return
    
    usdt_amount = round((KEY_PRICE_BUYER * amount) / rate, 4)
    await state.update_data(usdt_amount=usdt_amount)

    await call.answer()
    await call.message.edit_text(
        texts.crypto.CHOOSE_NETWORK.format(rate=rate, usdt_amount=usdt_amount),
        reply_markup=buttons.crypto.network_list(),
    )


# ─── Выбор сети ──────────────────────────────────────────────────────────────

@r.callback_query(F.data.startswith("crypto_network_"))
async def crypto_network_handler(call: CallbackQuery, state: FSMContext, user):
    """Сеть выбрана → показываем адрес кошелька и сумму в USDT."""
    network_id = call.data.split("_")[2]
    network    = get_network_by_id(network_id)

    if not network:
        await call.answer()
        return

    data        = await state.get_data()
    usdt_amount = data.get("usdt_amount", 0)

    await call.answer()
    await call.message.edit_text(
        texts.crypto.NETWORK_ADDRESS.format(
            network=network.name,
            address=network.address,
            usdt_amount=usdt_amount,
        ),
        reply_markup=buttons.crypto.network_actions(network_id),
    )


# ─── Я оплатил ───────────────────────────────────────────────────────────────

@r.callback_query(F.data.startswith("crypto_paid_"))
async def crypto_paid_handler(call: CallbackQuery, state: FSMContext, user):
    """Я оплатил → создаём платёж в статусе PENDING_HASH и просим хэш."""
    network_id = call.data.split("_")[2]
    network    = get_network_by_id(network_id)

    if not network:
        await call.answer()
        return

    data   = await state.get_data()
    amount = data.get("amount", 0)
    usdt_amount = data.get("usdt_amount", 0)
    special_offer_id = data.get("special_offer_id")

    payment = await create_payment_and_notify(
        call, user, amount,
        status=PaymentStatus.PENDING_HASH,
        network_id=network_id,
        usdt_amount=usdt_amount,
        special_offer_id=special_offer_id,
    )

    if not payment:
        return

    await state.update_data(network_id=network_id, payment_id=payment.id)
    await call.answer()


# ─── Получили хэш ────────────────────────────────────────────────────────────

@r.message(F.text)
async def crypto_hash_handler(msg: Message, state: FSMContext, user):
    """Получили текст → проверяем хэш если юзер в статусе PENDING_HASH."""

    payment = await db.payment.get_by_status(user.telegram_id, PaymentStatus.PENDING_HASH)
    if not payment:
        return

    data       = await state.get_data()
    network_id = data.get("network_id") or payment.network_id
    network    = get_network_by_id(network_id)

    if not network:
        return

    valid, tx_hash = validate_tx_hash(msg.text, network_id)

    # Проверяем длину хэша
    if not valid:
        await msg.answer(texts.crypto.INVALID_HASH.format(
            hash_format=network.hash_format
        ))
        return

    # Сохраняем хэш и переводим в PENDING_REVIEW
    await db.payment.upsert_payment(payment.id, tx_hash=tx_hash)

    await state.clear()

    # Возвращаем покупателя на экран "Мои заказы"
    await msg.answer(
        texts.profile.ORDERS_LIST,
        reply_markup=await buttons.profile.orders_list(user.telegram_id),
    )

    # Уведомляем админов
    await notify_admins(
        texts.crypto.ADMIN_NOTIFY.format(
            name=f"@{user.username}" if user.username else user.first_name,
            user_id=user.telegram_id,
            network=network.name,
            price=payment.price,
            usdt_amount=payment.usdt_amount or "—",
            amount=payment.amount,
            tx_hash=tx_hash,
            payment_id=payment.id
        ),
        reply_markup=buttons.payment.payment_notify(payment.id)
    )
