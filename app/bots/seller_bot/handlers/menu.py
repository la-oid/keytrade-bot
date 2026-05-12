from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, FSInputFile
from aiogram.fsm.context import FSMContext

from app.shared import db
from app.shared.constants import KEY_PRICE_SELLER
from app.shared.images import SellerImages
from ..texts import Texts, ButtonTexts
from ..keyboards import InlineKeyboards

r = Router()

texts = Texts()
buttons = InlineKeyboards()


# ─── Профиль ─────────────────────────────────────────────────────────────────

@r.callback_query(F.data == "profile")
@r.message(F.text == ButtonTexts.menu.PROFILE)
async def profile_handler(event: Message | CallbackQuery, user):
    """Профиль — ID, баланс, кол-во выполненных заказов + кнопки."""

    text = texts.profile.PROFILE_TEXT.format(
        nickname=f"@{user.username}" if user.username else str(user.telegram_id),
        user_id=user.telegram_id,
        balance=float(user.balance or 0),
        completed=user.completed_orders_count or 0,
    )
    keyboard = buttons.profile.profile()
    photo = FSInputFile(SellerImages.PROFILE)

    if isinstance(event, CallbackQuery):
        await event.answer()
        await event.message.delete()
        await event.message.answer_photo(photo=photo, caption=text, reply_markup=keyboard)
    else:
        await event.delete()
        await event.answer_photo(photo=photo, caption=text, reply_markup=keyboard)


# ─── Площадка заказов ────────────────────────────────────────────────────────

@r.callback_query(F.data == "market_back")
@r.message(F.text == ButtonTexts.menu.MARKET)
async def market_handler(event: Message | CallbackQuery, state: FSMContext):
    """Открывает список свободных паёв. Reply при первом входе, callback — при возврате."""
    await state.clear()

    orders = await db.order.get_all_active()
    keyboard = buttons.market.order_list(orders)

    tender   = await db.tender.get_active()
    filled   = tender.current_keys if tender else 0
    capacity = tender.total_keys   if tender else 0
    progress = round(filled / capacity * 100, 1) if capacity else 0.0

    text = texts.market.MARKET_INTRO.format(rate=KEY_PRICE_SELLER)
    photo = FSInputFile(SellerImages.ORDERS)

    if isinstance(event, CallbackQuery):
        await event.answer()
        await event.message.delete()
        await event.message.answer_photo(photo=photo, caption=text, reply_markup=keyboard)
    else:
        await event.delete()
        await event.answer_photo(photo=photo, caption=text, reply_markup=keyboard)


# ─── О компании ──────────────────────────────────────────────────────────────

@r.message(F.text == ButtonTexts.menu.ABOUT)
async def about_handler(msg: Message):
    await msg.delete()
    await msg.answer_photo(
        photo=FSInputFile(SellerImages.ABOUT),
        caption=texts.menu.ABOUT_TEXT,
    )


# ─── Поддержка ───────────────────────────────────────────────────────────────

@r.message(F.text == ButtonTexts.menu.SUPPORT)
async def support_handler(msg: Message):
    await msg.delete()
    await msg.answer(texts.menu.SUPPORT_TEXT, reply_markup=buttons.menu.support)
