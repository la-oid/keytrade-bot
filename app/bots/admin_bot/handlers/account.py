from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.shared import db
from ..states import AccountStates
from ..texts import Texts, ButtonTexts
from ..keyboards import InlineKeyboards

r = Router()

texts = Texts()
buttons = InlineKeyboards()


# ─── Utils ───────────────────────────────────────────────────────────────────

async def _show_account(target: Message | CallbackQuery, user_id: int):
    """Показывает текущий счёт пользователя + кнопки действий."""
    user = await db.user.get_user_by_telegram_id(user_id)
    if not user:
        text = texts.account.USER_NOT_FOUND
        if isinstance(target, Message):
            await target.answer(text)
        else:
            await target.message.edit_text(text)
        return

    text = texts.account.ACCOUNT_INFO.format(
        user_id=user.telegram_id,
        balance=user.balance or 0,
        frozen=user.frozen_balance or 0,
    )
    keyboard = buttons.account.account_menu(user.telegram_id)

    if isinstance(target, Message):
        await target.answer(text, reply_markup=keyboard)
    else:
        await target.message.edit_text(text, reply_markup=keyboard)


# ─── Ввод ID пользователя ────────────────────────────────────────────────────

@r.message(F.text == ButtonTexts.menu.USER_ACCOUNT)
async def account_start_handler(msg: Message, state: FSMContext):
    """Кнопка меню → просим ввести ID пользователя."""
    await msg.delete()
    await state.set_state(AccountStates.waiting_user_id)
    await msg.answer(texts.misc.ENTER_USER_ID)


@r.message(AccountStates.waiting_user_id)
async def account_user_id_handler(msg: Message, state: FSMContext):
    """ID введён → показываем счёт и кнопки."""
    if not msg.text.isdigit():
        await msg.answer(texts.misc.INVALID_USER_ID)
        return

    await state.clear()
    await _show_account(msg, int(msg.text))


# ─── Назад к вводу ID ────────────────────────────────────────────────────────

@r.callback_query(F.data == "account_back")
async def account_back_handler(call: CallbackQuery, state: FSMContext):
    """Назад → редактируем сообщение на ввод ID."""
    await call.answer()
    await state.set_state(AccountStates.waiting_user_id)
    await call.message.edit_text(texts.misc.ENTER_USER_ID)


# ─── Назад к меню счёта ──────────────────────────────────────────────────────

@r.callback_query(F.data.startswith("account_menu_"))
async def account_menu_handler(call: CallbackQuery, state: FSMContext):
    """Назад к меню счёта пользователя."""
    await call.answer()
    await state.clear()
    user_id = int(call.data.split("_")[2])
    await _show_account(call, user_id)


# ─── Добавить средства ───────────────────────────────────────────────────────

@r.callback_query(F.data.startswith("account_add_"))
async def account_add_handler(call: CallbackQuery, state: FSMContext):
    """Кнопка Добавить → просим ввести сумму."""
    user_id = int(call.data.split("_")[2])
    await call.answer()
    await state.set_state(AccountStates.waiting_amount)
    await state.update_data(action="add", user_id=user_id)
    await call.message.edit_text(texts.account.ENTER_AMOUNT)


# ─── Отнять средства ─────────────────────────────────────────────────────────

@r.callback_query(F.data.startswith("account_subtract_"))
async def account_subtract_handler(call: CallbackQuery, state: FSMContext):
    """Кнопка Отнять → просим ввести сумму."""
    user_id = int(call.data.split("_")[2])
    await call.answer()
    await state.set_state(AccountStates.waiting_amount)
    await state.update_data(action="subtract", user_id=user_id)
    await call.message.edit_text(texts.account.ENTER_AMOUNT)


@r.message(AccountStates.waiting_amount)
async def account_amount_handler(msg: Message, state: FSMContext):
    """Сумма введена → показываем подтверждение."""
    raw = msg.text.strip().replace(",", ".")

    try:
        amount = float(raw)
        if amount <= 0:
            raise ValueError
    except ValueError:
        await msg.answer(texts.account.INVALID_AMOUNT)
        return

    data = await state.get_data()
    action = data["action"]
    user_id = data["user_id"]

    await msg.delete()
    await msg.answer(
        texts.account.CONFIRM_TEXT.format(
            action=texts.account.ACTION_ADD if action == "add" else texts.account.ACTION_SUBTRACT,
            amount=amount,
            user_id=user_id,
        ),
        reply_markup=buttons.account.confirm(user_id, action, amount),
    )


# ─── Подтверждение добавить/отнять ───────────────────────────────────────────

@r.callback_query(F.data.startswith("account_confirm_"))
async def account_confirm_handler(call: CallbackQuery, state: FSMContext):
    """Подтверждение → применяем изменение баланса."""
    parts = call.data.split("_")
    action  = parts[2]
    user_id = int(parts[3])
    amount  = float(parts[4])

    await call.answer()

    user = await db.user.get_user_by_telegram_id(user_id)
    if not user:
        await call.message.edit_text(texts.account.USER_NOT_FOUND)
        return

    balance = float(user.balance or 0)
    new_balance = balance + amount if action == "add" else balance - amount

    await db.user.upsert_user(user_id, balance=new_balance)
    await state.clear()
    await _show_account(call, user_id)


# ─── Заморозить все средства ─────────────────────────────────────────────────

@r.callback_query(F.data.startswith("account_freeze_"))
async def account_freeze_handler(call: CallbackQuery):
    """Заморозить весь баланс → balance = 0, frozen = всё."""
    user_id = int(call.data.split("_")[2])
    await call.answer()

    user = await db.user.get_user_by_telegram_id(user_id)
    if not user:
        await call.message.edit_text(texts.account.USER_NOT_FOUND)
        return

    balance = float(user.balance or 0)
    frozen  = float(user.frozen_balance or 0)

    await db.user.upsert_user(
        user_id,
        balance=0,
        frozen_balance=frozen + balance,
    )
    await _show_account(call, user_id)


# ─── Разморозить все средства ────────────────────────────────────────────────

@r.callback_query(F.data.startswith("account_unfreeze_"))
async def account_unfreeze_handler(call: CallbackQuery):
    """Разморозить всё → frozen = 0, balance = всё."""
    user_id = int(call.data.split("_")[2])
    await call.answer()

    user = await db.user.get_user_by_telegram_id(user_id)
    if not user:
        await call.message.edit_text(texts.account.USER_NOT_FOUND)
        return

    balance = float(user.balance or 0)
    frozen  = float(user.frozen_balance or 0)

    await db.user.upsert_user(
        user_id,
        balance=balance + frozen,
        frozen_balance=0,
    )
    await _show_account(call, user_id)