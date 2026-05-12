from aiogram.types import Message, CallbackQuery

from app.shared import db
from app.utils import safe_edit
from app.shared.constants import KEY_PRICE_BUYER
from app.db.enums import PaymentStatus
from datetime import timedelta
from app.shared.constants import PAYMENT_DEADLINE_PAY
from app.utils import to_msk
from ..texts import Texts
from ..keyboards import InlineKeyboards
 
texts   = Texts()
buttons = InlineKeyboards()


# ─── Создание платежа ────────────────────────────────────────────────────────

async def create_payment_and_notify(target: Message | CallbackQuery, user, amount: int, **kwargs):
    """
    Создаёт платёж и уведомляет админов.
    kwargs передаются напрямую в upsert_payment (status, bank, network_id, usdt_amount и т.д.)
    """
    
    # Блокируем если amount не валидный или уже есть активный платёж
    if not amount or await show_active_payment(target, user):
        await target.message.delete()
        await target.answer()
        return None

    price = amount * KEY_PRICE_BUYER

    payment = await db.payment.upsert_payment(
        user_id=user.telegram_id,
        amount=amount,
        price=price,
        **kwargs,
    )

    # Показываем экран в зависимости от статуса
    await show_active_payment(target, user)

    return payment


# ─── Показ ожидания реквизитов ───────────────────────────────────────────────

async def show_pending_payment(target: Message | CallbackQuery, amount: int, price: float, bank: str):
    """Показывает экран ожидания реквизитов."""

    text = texts.payment.PENDING_TEXT.format(amount=amount, price=price, bank=bank)

    if isinstance(target, CallbackQuery):
        await safe_edit(target.message, text, reply_markup=buttons.payment.cancel_only)
    else:
        await target.answer(text, reply_markup=buttons.payment.cancel_only)


# ─── Показ ожидания хэша ───────────────────────────────────────────────

async def _show_waiting_hash(msg: Message, payment):
    """Просит прислать хэш с примером формата из JSON."""
    from app.utils import get_network_by_id

    network = get_network_by_id(payment.network_id)

    await msg.answer(
        texts.crypto.WAITING_HASH.format(
            hash_format=network.hash_format if network else "—",
        )
    )


# ─── Показ страницы оплаты ───────────────────────────────────────────────

async def _show_payment_page(target: Message | CallbackQuery, payment) -> None:
    """Показывает страницу оплаты с ссылкой."""

    msk_deadline = to_msk(payment.deadline).strftime("%d.%m.%Y %H:%M")

    text = texts.payment.PAYMENT_PAGE.format(
        payment_id=payment.id,
        price=payment.price,
        minutes=PAYMENT_DEADLINE_PAY,
        deadline=msk_deadline,
    )
    kb   = buttons.payment.payment_page(url=payment.payment_link)

    if isinstance(target, CallbackQuery):
        await safe_edit(target.message, text, reply_markup=kb)
    else:
        await target.answer(text, reply_markup=kb)


# ─── Проверка активного платежа ──────────────────────────────────────────────

async def show_active_payment(msg: Message | CallbackQuery, user) -> bool:
    """Если есть активный платёж — показывает экран и возвращает True. Иначе False."""

    # Если передан CallbackQuery — сохраняем его и извлекаем Message
    call = msg if isinstance(msg, CallbackQuery) else None
    if call: msg = msg.message

    handlers = {
        PaymentStatus.PENDING_HASH: lambda p: _show_waiting_hash(msg, p),
        PaymentStatus.PENDING_PAY:  lambda p: _show_payment_page(call or msg, p),
        PaymentStatus.PENDING_PDF:  lambda p: msg.answer(texts.payment.WAITING_PDF),
    }

    for status, action in handlers.items():
        payment = await db.payment.get_by_status(user.telegram_id, status)
        if payment:
            await action(payment)
            return True

    return False
