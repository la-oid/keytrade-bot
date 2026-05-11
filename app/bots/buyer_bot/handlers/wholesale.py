from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from app.shared.constants import KEY_PRICE_BUYER, MEDIUM, LARGE
from ..utils import show_active_payment
from ..states import OrderStates
from ..texts import Texts, ButtonTexts
from ..keyboards import InlineKeyboards

r = Router()

texts = Texts()
buttons = InlineKeyboards()


@r.message(F.text == ButtonTexts.menu.MEDIUM_WHOLESALE)
async def medium_wholesale_handler(msg: Message, state: FSMContext, user):
    await msg.delete()

    # Проверяем есть ли активный платёж
    if await show_active_payment(msg, user):
        return
    
    await state.set_state(OrderStates.medium_wholesale)
    await state.update_data(amount=MEDIUM["min"])
    
    await msg.answer( 
        texts.wholesale.MEDIUM_TEXT.format(
            min=MEDIUM["min"],
            max=MEDIUM["max"],
            amount=MEDIUM["min"],
            price=MEDIUM["min"] * KEY_PRICE_BUYER,
        ),
        reply_markup=buttons.wholesale.wholesale(LARGE["min"], LARGE["step"])
    )


@r.message(F.text == ButtonTexts.menu.LARGE_WHOLESALE)
async def large_wholesale_handler(msg: Message, state: FSMContext, user):
    await msg.delete()
    
    # Проверяем есть ли активный платёж
    if await show_active_payment(msg, user):
        return
    
    await state.set_state(OrderStates.large_wholesale)
    await state.update_data(amount=LARGE["min"])

    await msg.answer( 
        texts.wholesale.LARGE_TEXT.format(
            min=MEDIUM["min"],
            max=MEDIUM["max"],
            amount=MEDIUM["min"],
            price=MEDIUM["min"] * KEY_PRICE_BUYER,
        ),
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
        texts.wholesale.WHOLESALE_TEXT.format(amount=new_amount, price=new_amount * KEY_PRICE_BUYER),
        reply_markup=buttons.wholesale.wholesale(new_amount, step)
    )
