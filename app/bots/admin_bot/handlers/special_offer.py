from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.shared import db
from app.bots.buyer_bot import send_offer
from app.utils import to_msk
from ..states import SpecialOfferStates
from ..texts import Texts, ButtonTexts
from ..keyboards import InlineKeyboards
from ..utils import parse_order_create

r = Router()

texts   = Texts()
buttons = InlineKeyboards()


# ─── Старт ───────────────────────────────────────────────────────────────────

@r.message(F.text == ButtonTexts.menu.SPECIAL_OFFERS)
async def special_offer_start(msg: Message, state: FSMContext):
    """Кнопка меню → просим ввести ID пользователя."""
    await msg.delete()
    await state.set_state(SpecialOfferStates.waiting_user_id)
    await msg.answer(texts.misc.ENTER_USER_ID)


# ─── Ввод ID ─────────────────────────────────────────────────────────────────

@r.message(SpecialOfferStates.waiting_user_id)
async def special_offer_user_id(msg: Message, state: FSMContext):
    """ID введён → проверяем и просим ввести кол-во ключей + время жизни."""
    if not msg.text.isdigit():
        await msg.answer(texts.misc.INVALID_USER_ID)
        return

    user_id = int(msg.text)
    user = await db.user.get_user_by_telegram_id(user_id)

    if not user:
        await msg.answer(texts.block.USER_NOT_FOUND)
        return

    await state.update_data(user_id=user_id)
    await state.set_state(SpecialOfferStates.waiting_data)
    await msg.answer(texts.special_offer.ENTER_DATA)


# ─── Ввод кол-ва и времени ───────────────────────────────────────────────────

@r.message(SpecialOfferStates.waiting_data)
async def special_offer_data(msg: Message, state: FSMContext):
    """Кол-во ключей + время жизни → просим ввести текст предложения."""
    parsed = parse_order_create(msg.text)

    if not parsed:
        await msg.answer(texts.order.INVALID_DATA)
        return

    keys_count, lifetime_hours = parsed
    await state.update_data(keys_count=keys_count, lifetime_hours=lifetime_hours)
    await state.set_state(SpecialOfferStates.waiting_text)
    await msg.answer(texts.special_offer.ENTER_TEXT)


# ─── Ввод текста ─────────────────────────────────────────────────────────────

@r.message(SpecialOfferStates.waiting_text)
async def special_offer_text(msg: Message, state: FSMContext):
    """Текст введён → показываем превью и просим подтверждение."""
    await state.update_data(custom_text=msg.text)
    await state.set_state(SpecialOfferStates.confirm)

    data = await state.get_data()
    expires_at = datetime.utcnow() + timedelta(hours=data["lifetime_hours"])

    await msg.answer(
        texts.special_offer.CONFIRM_PREVIEW.format(
            user_id=data["user_id"],
            keys_count=data["keys_count"],
            lifetime_hours=data["lifetime_hours"],
            expires_at=to_msk(expires_at).strftime("%d.%m.%Y %H:%M"),
            custom_text=data["custom_text"],
        ),
        reply_markup=buttons.special_offer.confirm(),
    )


# ─── Подтверждение ───────────────────────────────────────────────────────────

@r.callback_query(F.data == "special_offer_confirm")
async def special_offer_confirm(call: CallbackQuery, state: FSMContext):
    """Да → создаём оффер и отправляем пользователю."""
    data = await state.get_data()
    await call.answer()
    await state.clear()

    expires_at = datetime.utcnow() + timedelta(hours=data["lifetime_hours"])

    offer = await db.special_offer.create(
        user_id=data["user_id"],
        keys_count=data["keys_count"],
        expires_at=expires_at,
        custom_text=data["custom_text"],
    )

    sent = await send_offer(data["user_id"], offer.keys_count, offer.expires_at, offer.custom_text)

    if sent:
        await call.message.edit_text(
            texts.special_offer.SENT.format(user_id=data["user_id"])
        )
    else:
        await call.message.edit_text(
            texts.special_offer.SEND_FAILED.format(user_id=data["user_id"])
        )


# ─── Ввести заново ───────────────────────────────────────────────────────────

@r.callback_query(F.data == "special_offer_retry")
async def special_offer_retry(call: CallbackQuery, state: FSMContext):
    """Нет → возвращаемся к вводу кол-ва и времени."""
    await call.answer()
    await state.set_state(SpecialOfferStates.waiting_data)
    await call.message.edit_text(texts.special_offer.ENTER_DATA)