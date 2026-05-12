from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from app.shared.constants import KEY_PRICE_BUYER
from app.shared.config import settings
from app.shared import db, bots
from app.db.enums import PaymentStatus
from app.services import payment_service
from app.utils import notify_admins
from ..utils import create_payment_and_notify, show_pending_payment, safe_edit
from ..texts import Texts
from ..keyboards import InlineKeyboards

r = Router()

texts = Texts()
buttons = InlineKeyboards()


# ─── Выбор метода оплаты ───────────────────────────────────────────────────────

@r.callback_query(F.data == "confirm_order")
async def confirm_order_handler(call: CallbackQuery):
    """Купить → выбор метода оплаты."""
    await call.answer()
    await safe_edit(call.message, texts.payment.CHOOSE_METHOD, reply_markup=buttons.payment.choose_method)


@r.callback_query(F.data == "pay_spb")
async def pay_spb_handler(call: CallbackQuery, state: FSMContext, user):
    """СБП → создаём invoice через cardlink и сразу показываем ссылку."""
    data             = await state.get_data()
    amount           = data.get("amount", 0)
    special_offer_id = data.get("special_offer_id")
    price            = amount * KEY_PRICE_BUYER

    url = await payment_service.create_payment_url(price)

    payment = await create_payment_and_notify(
        call, user, amount,
        payment_link=url,
        special_offer_id=special_offer_id,
    )

    if not payment:
        return
    
    await state.clear()
    await call.answer()


# ─── Отмена оплаты ─────────────────────────────────────────────────────────────

@r.callback_query(F.data == "cancel_payment")
async def cancel_payment_handler(call: CallbackQuery):
    """Отменить → запрос подтверждения."""
    await call.answer()
    await safe_edit(call.message, texts.payment.CONFIRM_CANCEL_TEXT, reply_markup=buttons.payment.confirm_cancel)


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
        await db.payment.upsert_payment(pending.id, status=PaymentStatus.CANCELLED)
        
        # Уведомляем админов об отмене
        await notify_admins(texts.payment.ADMIN_CANCELLED.format(
            name=f"@{user.username}" if user.username else user.first_name,
            user_id=user.telegram_id,
            bank=pending.bank,
            price=pending.price,
            amount=pending.amount,
        ))

    await state.clear()
    await call.answer()
    await safe_edit(call.message, texts.payment.CANCELLED_TEXT)