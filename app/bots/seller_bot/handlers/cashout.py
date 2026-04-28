import random
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.shared import db
from app.shared.constants import CASHOUT_STEP
from app.db.enums import CashoutStatus
from ..states import CashoutStates
from ..texts import Texts, ButtonTexts
from ..keyboards import InlineKeyboards

r = Router()

texts = Texts()
buttons = InlineKeyboards()


# ─── Открыть вывод средств ───────────────────────────────────────────────────

@r.callback_query(F.data == "profile_withdraw")
async def cashout_start(call: CallbackQuery, user):
    """Кнопка 'Вывод средств' → редактируем на экран выбора суммы."""
    await call.answer()
    await call.message.edit_text(
        texts.cashout.CHOOSE_AMOUNT.format(balance=user.balance or 0),
        reply_markup=buttons.cashout.amount_choice(),
    )


# ─── Вся сумма ───────────────────────────────────────────────────────────────

@r.callback_query(F.data == "cashout_all")
async def cashout_all_handler(call: CallbackQuery, state: FSMContext, user):
    """Вся сумма → сразу к выбору метода."""
    await call.answer()
    balance = float(user.balance or 0)

    if balance <= 0:
        await call.message.edit_text(
            texts.cashout.NOT_ENOUGH,
            reply_markup=buttons.cashout.amount_choice(),
        )
        return

    await state.update_data(amount=balance)
    await call.message.edit_text(
        texts.cashout.CHOOSE_METHOD,
        reply_markup=buttons.cashout.method_choice(),
    )


# ─── Другая сумма ────────────────────────────────────────────────────────────

@r.callback_query(F.data == "cashout_custom")
async def cashout_custom_handler(call: CallbackQuery, state: FSMContext):
    """Другая сумма → просим ввести."""
    await call.answer()
    await state.set_state(CashoutStates.waiting_amount)
    await call.message.edit_text(texts.cashout.ENTER_AMOUNT.format(step=CASHOUT_STEP))


@r.message(CashoutStates.waiting_amount)
async def cashout_amount_handler(msg: Message, state: FSMContext, user):
    """Ввод суммы → валидируем и переходим к методу."""
    raw = msg.text.strip().replace(",", ".")

    try:
        amount = float(raw)
    except ValueError:
        await msg.answer(texts.cashout.INVALID_AMOUNT.format(step=CASHOUT_STEP))
        return

    balance = float(user.balance or 0)

    if amount <= 0 or amount > balance or amount % CASHOUT_STEP != 0:
        await msg.answer(texts.cashout.INVALID_AMOUNT.format(step=CASHOUT_STEP))
        return

    await msg.delete()
    await state.update_data(amount=amount)
    await state.set_state(None)
    await msg.answer(
        texts.cashout.CHOOSE_METHOD,
        reply_markup=buttons.cashout.method_choice(),
    )


# ─── Назад к выбору суммы ────────────────────────────────────────────────────

@r.callback_query(F.data == "cashout_back_to_amount")
async def cashout_back_to_amount(call: CallbackQuery, state: FSMContext, user):
    await call.answer()
    await state.clear()
    await call.message.edit_text(
        texts.cashout.CHOOSE_AMOUNT.format(balance=user.balance or 0),
        reply_markup=buttons.cashout.amount_choice(),
    )


# ─── Метод: карта → ввод номера ──────────────────────────────────────────────

@r.callback_query(F.data == "cashout_card")
async def cashout_card_handler(call: CallbackQuery, state: FSMContext):
    """Выбрана карта → просим ввести номер."""
    await call.answer()
    await state.set_state(CashoutStates.waiting_card_number)
    await call.message.edit_text(texts.cashout.ENTER_CARD)


@r.message(CashoutStates.waiting_card_number)
async def cashout_card_number_handler(msg: Message, state: FSMContext, user):
    """Номер карты введён → создаём заявку, замораживаем баланс."""
    card = msg.text.strip().replace(" ", "")

    if not card.isdigit() or len(card) != 16:
        await msg.answer(texts.cashout.INVALID_CARD)
        return

    data = await state.get_data()
    amount = data["amount"]

    # Замораживаем баланс
    new_balance = float(user.balance or 0) - amount
    new_frozen = float(user.frozen_balance or 0) + amount
    await db.user.upsert_user(
        user.telegram_id,
        balance=new_balance,
        frozen_balance=new_frozen,
    )

    # Создаём заявку
    cashout = await db.cashout.create(
        user_id=user.telegram_id,
        amount=amount,
        card_number=card,
    )

    await state.clear()
    await msg.delete()

    # Показываем статус заявки (пока рандом ID)
    await msg.answer(
        texts.cashout.CREATED.format(
            cashout_id=cashout.id,
            amount=amount,
            card=f"**** **** **** {card[-4:]}",
        )
    )