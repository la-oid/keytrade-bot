from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from app.shared.constants import KEY_PRICE, MEDIUM, LARGE
from app.shared import db
from app.db.enums import PaymentStatus
from .payment import show_active_payment
from ..states import OrderStates
from ..texts import Texts
from ..keyboards import InlineKeyboards

r = Router()

texts = Texts()
buttons = InlineKeyboards()


@r.callback_query(F.data == "medium_wholesale")
async def medium_wholesale_handler(call: CallbackQuery, state: FSMContext, user):
    # Проверяем есть ли активный платёж
    
    await call.answer()
    if await show_active_payment(call, user):
        return
    
    await state.set_state(OrderStates.medium_wholesale)
    await state.update_data(amount=MEDIUM["min"])
    await call.message.edit_text(
        texts.wholesale.WHOLESALE_TEXT.format(amount=MEDIUM["min"], price=MEDIUM["min"] * KEY_PRICE),
        reply_markup=buttons.wholesale.wholesale(MEDIUM["min"], MEDIUM["step"])
    )


@r.callback_query(F.data == "large_wholesale")
async def large_wholesale_handler(call: CallbackQuery, state: FSMContext, user):
    # Проверяем есть ли активный платёж

    await call.answer()
    if await show_active_payment(call, user):
        return
    
    await state.set_state(OrderStates.large_wholesale)
    await state.update_data(amount=LARGE["min"])
    await call.message.edit_text(
        texts.wholesale.WHOLESALE_TEXT.format(amount=LARGE["min"], price=LARGE["min"] * KEY_PRICE),
        reply_markup=buttons.wholesale.wholesale(LARGE["min"], LARGE["step"])
    )


@r.callback_query(F.data.in_({"amount_minus", "amount_plus"}))
async def change_amount_handler(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_state = await state.get_state()
    amount = data["amount"]

    if current_state == OrderStates.medium_wholesale:
        step = MEDIUM["step"]
        new_amount = amount + step if call.data == "amount_plus" else amount - step
        new_amount = max(MEDIUM["min"], min(MEDIUM["max"], new_amount))
    else:
        step = LARGE["step"]
        new_amount = amount + step if call.data == "amount_plus" else amount - step
        new_amount = max(LARGE["min"], new_amount)

    await call.answer()

    if new_amount == amount:
        return

    await state.update_data(amount=new_amount)
    await call.message.edit_text(
        texts.wholesale.WHOLESALE_TEXT.format(amount=new_amount, price=new_amount * KEY_PRICE),
        reply_markup=buttons.wholesale.wholesale(new_amount, step)
    )