from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from app.shared import db
from app.shared.config import settings
from ..texts import Texts, ButtonTexts
from ..keyboards import InlineKeyboards

r = Router()

texts = Texts()
buttons = InlineKeyboards()


# ─── Профиль ─────────────────────────────────────────────────────────────────

@r.callback_query(F.data == "profile")
@r.message(F.text == ButtonTexts.menu.PROFILE)
async def profile_handler(event: Message | CallbackQuery, user):
    text = texts.menu.PROFILE_TEXT.format(user_id=user.telegram_id)

    if isinstance(event, CallbackQuery):
        await event.answer()
        await event.message.edit_text(text)
    else:
        await event.delete()
        await event.answer(text)


# ─── Площадка заказов ────────────────────────────────────────────────────────

@r.callback_query(F.data == "market_back")
@r.message(F.text == ButtonTexts.menu.MARKET)
async def market_handler(event: Message | CallbackQuery, state: FSMContext):
    """Открывает список свободных паёв. Reply при первом входе, callback — при возврате."""
    await state.clear()

    orders = await db.order.get_all_active()
    keyboard = buttons.market.order_list(orders)
    text = texts.market.MARKET_INTRO

    if isinstance(event, CallbackQuery):
        await event.answer()
        await event.message.edit_text(text, reply_markup=keyboard)
    else:
        await event.delete()
        await event.answer(text, reply_markup=keyboard)


# ─── О компании ──────────────────────────────────────────────────────────────

@r.message(F.text == ButtonTexts.menu.ABOUT)
async def about_handler(msg: Message):
    await msg.delete()
    await msg.answer(texts.menu.ABOUT_TEXT)


# ─── Поддержка ───────────────────────────────────────────────────────────────

@r.message(F.text == ButtonTexts.menu.SUPPORT)
async def support_handler(msg: Message):
    await msg.delete()
    await msg.answer(texts.menu.SUPPORT_TEXT.format(url=settings.app.SUPPORT_URL))