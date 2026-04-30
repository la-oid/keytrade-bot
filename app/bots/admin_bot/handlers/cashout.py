from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from app.shared import db, bots
from app.db.enums import CashoutStatus
from ..texts import Texts, ButtonTexts
from ..keyboards import InlineKeyboards

r = Router()

texts = Texts()
buttons = InlineKeyboards()


# ─── Список заявок ───────────────────────────────────────────────────────────

@r.message(F.text == ButtonTexts.menu.PAYOUTS)
async def cashout_list_handler(msg: Message):
    """Кнопка меню → список pending-заявок."""
    await msg.delete()
    await _show_cashout_list(msg)


async def _show_cashout_list(target: Message | CallbackQuery):
    cashouts = await db.cashout.get_all_by_status(CashoutStatus.PENDING)
    text = texts.cashout.CURRENT_CASHOUTS
    keyboard = buttons.cashout.cashout_list(cashouts)

    if isinstance(target, Message):
        await target.answer(text, reply_markup=keyboard)
    else:
        await target.message.edit_text(text, reply_markup=keyboard)


# ─── Назад к списку ──────────────────────────────────────────────────────────

@r.callback_query(F.data == "cashout_back")
async def cashout_back_handler(call: CallbackQuery):
    await call.answer()
    await _show_cashout_list(call)


# ─── Детали заявки ───────────────────────────────────────────────────────────

@r.callback_query(F.data.startswith("cashout_detail_"))
async def cashout_detail_handler(call: CallbackQuery):
    """Нажали на заявку → показываем детали + кнопки."""
    cashout_id = int(call.data.split("_")[2])
    cashout = await db.cashout.get_by_id(cashout_id)

    await call.answer()

    if not cashout or cashout.status != CashoutStatus.PENDING:
        await call.message.edit_text(
            texts.cashout.CASHOUT_NOT_FOUND,
            reply_markup=buttons.cashout.cashout_list([]),
        )
        return

    await call.message.edit_text(
        texts.cashout.CASHOUT_DETAIL.format(
            id=cashout.id,
            user_id=cashout.user_id,
            amount=cashout.amount,
            card=cashout.card_number,
        ),
        reply_markup=buttons.cashout.cashout_detail(cashout.id),
    )


# ─── Выполнить заявку ────────────────────────────────────────────────────────

@r.callback_query(F.data.startswith("cashout_complete_"))
async def cashout_complete_handler(call: CallbackQuery):
    """Отмечаем заявку выполненной и размораживаем баланс юзера."""
    cashout_id = int(call.data.split("_")[2])
    cashout = await db.cashout.get_by_id(cashout_id)

    await call.answer()

    if not cashout or cashout.status != CashoutStatus.PENDING:
        await call.message.edit_text(
            texts.cashout.CASHOUT_NOT_FOUND,
            reply_markup=buttons.cashout.cashout_list([]),
        )
        return

    # Меняем статус
    await db.cashout.set_status(cashout_id, CashoutStatus.COMPLETED)

    # Размораживаем ровно столько сколько было в заявке
    # user = await db.user.get_user_by_telegram_id(cashout.user_id)
    # if user:
    #     new_frozen = max(0, float(user.frozen_balance or 0) - float(cashout.amount))
    #     await db.user.upsert_user(user.telegram_id, frozen_balance=new_frozen)

    # Уведомляем продавца в seller_bot
    await bots.seller.bot.send_message(
        chat_id=cashout.user_id,
        text=texts.cashout.CASHOUT_COMPLETED_NOTIFY.format(
            id=cashout.id,
            amount=cashout.amount,
        )
    )

    await call.message.edit_text(
        texts.cashout.CASHOUT_COMPLETED.format(
            id=cashout.id,
            amount=cashout.amount,
        ),
        reply_markup=buttons.cashout.cashout_list([]),
    )