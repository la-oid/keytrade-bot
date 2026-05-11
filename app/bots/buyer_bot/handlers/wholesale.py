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
    
    await _show_wholesale(msg, state, MEDIUM, texts.wholesale.MEDIUM_TEXT, MEDIUM["min"])



@r.message(F.text == ButtonTexts.menu.LARGE_WHOLESALE)
async def large_wholesale_handler(msg: Message, state: FSMContext, user):
    await msg.delete()
    
    # Проверяем есть ли активный платёж
    if await show_active_payment(msg, user):
        return
    
    await state.set_state(OrderStates.large_wholesale)
    await state.update_data(amount=LARGE["min"])

    await _show_wholesale(msg, state, LARGE, texts.wholesale.LARGE_TEXT, LARGE["min"])



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

    is_medium = current_state == OrderStates.medium_wholesale
    text = texts.wholesale.MEDIUM_TEXT if is_medium else texts.wholesale.LARGE_TEXT
    cfg  = MEDIUM if is_medium else LARGE

    await state.update_data(amount=new_amount)
    await _show_wholesale(call, state, cfg, text, new_amount)


async def _show_wholesale(target: Message | CallbackQuery, state: FSMContext, cfg: dict, text_template: str, amount: int):
    """Показывает экран выбора количества ключей."""
    text = text_template.format(
        min=cfg["min"],
        max=cfg["max"],
        amount=amount,
        price=amount * KEY_PRICE_BUYER,
    )
    kb = buttons.wholesale.wholesale(amount, cfg["step"])

    if isinstance(target, CallbackQuery):
        await target.message.edit_text(text, reply_markup=kb)
    else:
        await target.answer(text, reply_markup=kb)