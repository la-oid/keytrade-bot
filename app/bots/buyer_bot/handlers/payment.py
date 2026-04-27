from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from app.shared.constants import KEY_PRICE, BANKS
from app.shared.config import settings
from app.shared import db, bots
from app.db.enums import PaymentStatus
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
    """Банк выбран → сразу создаём платёж и показываем ожидание."""
    bank = BANK_NAMES[call.data]
    data = await state.get_data()
    amount = data.get("amount", 0)
    price = amount * KEY_PRICE

    await db.payment.create_payment(
        user_id=user.telegram_id,
        amount=amount,
        price=price,
        bank=bank,
    )

    await state.clear()
    await call.answer()
    await show_pending_payment(call, amount, price, bank)

    for admin_id in settings.telegram.ADMIN_IDS:
        await bots.admin.bot.send_message(
            chat_id=admin_id,
            text=texts.payment.ADMIN_NOTIFY.format(
                name=user.first_name or user.username,
                user_id=user.telegram_id,
                bank=bank,
                price=price,
                amount=amount,
            )
        )


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
        for admin_id in settings.telegram.ADMIN_IDS:
            await bots.admin.bot.send_message(
                chat_id=admin_id,
                text=texts.payment.ADMIN_CANCELLED.format(
                    name=user.first_name or user.username,
                    user_id=user.telegram_id,
                    bank=pending.bank,
                    price=pending.price,
                    amount=pending.amount,
                )
            )

    await state.clear()
    await call.answer()
    await call.message.edit_text(texts.payment.CANCELLED_TEXT)


# ─── Helpers ───────────────────────────────────────────────────────────────────

async def show_pending_payment(target: Message | CallbackQuery, amount: int, price: float, bank: str):
    """Показывает экран ожидания реквизитов."""

    text = texts.payment.PENDING_TEXT.format(amount=amount, price=price, bank=bank)

    if isinstance(target, CallbackQuery): 
        await target.message.edit_text(
            text, 
            reply_markup=buttons.payment.cancel_only
        )
    else: 
        await target.answer(
            text, 
            reply_markup=buttons.payment.cancel_only
        )

async def show_active_payment(msg: Message, user) -> bool:
    """Если есть активный платёж — показывает экран и возвращает True. Иначе False."""

    handlers = {
        PaymentStatus.PENDING_LINK: lambda p: show_pending_payment(msg, p.amount, p.price, p.bank),
        PaymentStatus.PENDING_PAY:  lambda p: msg.answer(
            texts.payment.PAYMENT_PAGE.format(payment_id=p.id),
            reply_markup=buttons.payment.payment_page(url=p.payment_link)
        ),
        PaymentStatus.PENDING_PDF:  lambda p: msg.answer(texts.payment.WAITING_PDF),
    }

    for status, action in handlers.items():
        payment = await db.payment.get_by_status(user.telegram_id, status)
        if payment:
            await action(payment)
            return True

    return False