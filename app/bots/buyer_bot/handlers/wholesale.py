from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from app.shared.constants import KEY_PRICE, MEDIUM, LARGE
from app.shared import db
from ..states import OrderStates
from ..texts import Texts
from ..keyboards import InlineKeyboards

r = Router()

texts = Texts()
buttons = InlineKeyboards()


@r.callback_query(F.data == "medium_wholesale")
async def medium_wholesale_handler(call: CallbackQuery, state: FSMContext):
    await state.set_state(OrderStates.medium_wholesale)
    await state.update_data(amount=MEDIUM["min"])
    await call.answer()
    await call.message.edit_text(
        texts.wholesale.WHOLESALE_TEXT.format(amount=MEDIUM["min"], price=MEDIUM["min"] * KEY_PRICE),
        reply_markup=buttons.wholesale.wholesale(MEDIUM["min"], MEDIUM["step"])
    )


@r.callback_query(F.data == "large_wholesale")
async def large_wholesale_handler(call: CallbackQuery, state: FSMContext):
    await state.set_state(OrderStates.large_wholesale)
    await state.update_data(amount=LARGE["min"])
    await call.answer()
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


@r.callback_query(F.data == "confirm_order")
async def confirm_order_handler(call: CallbackQuery, state: FSMContext, user):
    data = await state.get_data()
    amount = data["amount"]

    await db.order.create(user_id=user.id, amount=amount, price=amount * KEY_PRICE)
    await state.clear()
    await call.answer()
    await call.message.edit_text(
        texts.wholesale.ORDER_CREATED_TEXT.format(amount=amount),
        reply_markup=buttons.menu.start
    )
