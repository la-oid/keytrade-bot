from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from app.shared.constants import KEY_PRICE, BANKS
from app.shared.config import settings
from app.shared import db, bots
from app.db.enums import PaymentStatus
from ..utils import create_payment_and_notify, show_pending_payment, notify_admins
from ..texts import Texts
from ..keyboards import InlineKeyboards

r = Router()

texts = Texts()
buttons = InlineKeyboards()

BANK_NAMES = {f"bank_{bank.lower()}": bank for bank in BANKS}


# ─── Выбор метода оплаты ───────────────────────────────────────────────────────

@r.callback_query(F.data == "confirm_order")
async def confirm_order_handler(call: CallbackQuery):
    """Купить → выбор метода оплаты."""
    await call.answer()
    await call.message.edit_text(
        texts.payment.CHOOSE_METHOD,
        reply_markup=buttons.payment.choose_method
    )


@r.callback_query(F.data == "pay_spb")
async def pay_spb_handler(call: CallbackQuery):
    """СБП → выбор банка."""
    await call.answer()
    try:
        await call.message.edit_text(
            texts.payment.CHOOSE_BANK,
            reply_markup=buttons.payment.choose_bank
        )
    except TelegramBadRequest:
        pass


@r.callback_query(F.data.in_(set(BANK_NAMES.keys())))
async def choose_bank_handler(call: CallbackQuery, state: FSMContext, user):
    """Банк выбран → создаём платёж и показываем ожидание."""
    bank   = BANK_NAMES[call.data]
    data   = await state.get_data()
    amount = data.get("amount", 0)

    payment = await create_payment_and_notify(
        call, user, amount,
        status=PaymentStatus.PENDING_LINK,
        bank=bank,
    )
    
    if not payment:
        return

    await state.clear()
    await call.answer()

    # Уведомляем админов
    await notify_admins(texts.payment.ADMIN_NOTIFY.format(
        name=user.first_name or user.username,
        user_id=user.telegram_id,
        bank=bank,
        price=payment.price,
        amount=payment.amount,
    ))


# ─── Отмена оплаты ─────────────────────────────────────────────────────────────

@r.callback_query(F.data == "cancel_payment")
async def cancel_payment_handler(call: CallbackQuery):
    """Отменить → запрос подтверждения."""
    await call.answer()
    await call.message.edit_text(
        texts.payment.CONFIRM_CANCEL_TEXT,
        reply_markup=buttons.payment.confirm_cancel
    )


@r.callback_query(F.data == "back_to_pending")
async def back_to_pending_handler(call: CallbackQuery, user):
    """Передумал → возврат на экран ожидания."""
    pending = await db.payment.get_by_status(user.telegram_id, PaymentStatus.PENDING_LINK)
    await call.answer()
    await show_pending_payment(call, pending.amount, pending.price, pending.bank)


@r.callback_query(F.data == "cancel_active")
async def cancel_active_handler(call: CallbackQuery, state: FSMContext, user):
    """Отмена подтверждена → отменяем в БД, уведомляем админов, возврат в меню."""

    pending = await db.payment.get_by_status(user.telegram_id, PaymentStatus.PENDING_LINK)
    if pending:
        await db.payment.set_status(pending.id, PaymentStatus.CANCELLED)
        
        # Уведомляем админов об отмене
        await notify_admins(texts.payment.ADMIN_CANCELLED.format(
            name=user.first_name or user.username,
            user_id=user.telegram_id,
            bank=pending.bank,
            price=pending.price,
            amount=pending.amount,
        ))

    await state.clear()
    await call.answer()
    await call.message.edit_text(texts.payment.CANCELLED_TEXT)