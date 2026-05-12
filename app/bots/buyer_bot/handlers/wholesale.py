from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, FSInputFile, InputMediaPhoto
from aiogram.fsm.context import FSMContext

from app.shared.constants import KEY_PRICE_BUYER, MEDIUM, LARGE
from app.shared.images import BuyerImages
from ..utils import show_active_payment
from ..states import OrderStates
from ..texts import Texts, ButtonTexts
from ..keyboards import InlineKeyboards

r = Router()

texts   = Texts()
buttons = InlineKeyboards()


# ─── Средний опт ─────────────────────────────────────────────────────────────

@r.message(F.text == ButtonTexts.menu.MEDIUM_WHOLESALE)
async def medium_wholesale_handler(msg: Message, state: FSMContext, user):
    await msg.delete()

    # Блокируем если есть активный платёж
    if await show_active_payment(msg, user):
        return

    await state.set_state(OrderStates.medium_wholesale)
    await state.update_data(amount=MEDIUM["min"])
    await _show_wholesale(msg, state, MEDIUM, texts.wholesale.MEDIUM_TEXT, MEDIUM["min"])


# ─── Крупный опт ─────────────────────────────────────────────────────────────

@r.message(F.text == ButtonTexts.menu.LARGE_WHOLESALE)
async def large_wholesale_handler(msg: Message, state: FSMContext, user):
    await msg.delete()

    # Блокируем если есть активный платёж
    if await show_active_payment(msg, user):
        return

    await state.set_state(OrderStates.large_wholesale)
    await state.update_data(amount=LARGE["min"])
    await _show_wholesale(msg, state, LARGE, texts.wholesale.LARGE_TEXT, LARGE["min"])


# ─── Изменение количества ─────────────────────────────────────────────────────

@r.callback_query(F.data.in_({"amount_minus", "amount_plus"}))
async def change_amount_handler(call: CallbackQuery, state: FSMContext):
    data          = await state.get_data()
    current_state = await state.get_state()
    amount        = data["amount"]

    is_medium = current_state == OrderStates.medium_wholesale
    cfg       = MEDIUM if is_medium else LARGE
    text      = texts.wholesale.MEDIUM_TEXT if is_medium else texts.wholesale.LARGE_TEXT

    step       = cfg["step"]
    new_amount = amount + step if call.data == "amount_plus" else amount - step
    # Ограничиваем в пределах диапазона
    new_amount = max(cfg["min"], min(cfg["max"], new_amount))

    await call.answer()

    # Если значение не изменилось — ничего не делаем
    if new_amount == amount:
        return

    await state.update_data(amount=new_amount)
    await _show_wholesale(call, state, cfg, text, new_amount)


# ─── Helpers ─────────────────────────────────────────────────────────────────

async def _show_wholesale(target: Message | CallbackQuery, state: FSMContext, cfg: dict, text_template: str, amount: int):
    """Показывает экран выбора количества ключей."""
    text = text_template.format(
        min=cfg["min"],
        max=cfg["max"],
        amount=amount,
        price=amount * KEY_PRICE_BUYER,
    )
    kb = buttons.wholesale.wholesale(amount, cfg["step"])

    current_state = await state.get_state()
    image = BuyerImages.MEDIUM_WHOLESALE if current_state == OrderStates.medium_wholesale else BuyerImages.LARGE_WHOLESALE

    if isinstance(target, CallbackQuery):
        await target.message.edit_media(
            media=InputMediaPhoto(media=FSInputFile(image), caption=text),
            reply_markup=kb,
        )
    else:
        await target.answer_photo(photo=FSInputFile(image), caption=text, reply_markup=kb)
