from datetime import timedelta

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from app.shared import db
from app.shared.constants import KEY_PRICE_BUYER
from app.utils import to_msk
from .payment import confirm_order_handler
from ..utils import send_offer
from ..texts import Texts
from ..keyboards import InlineKeyboards

r = Router()

texts = Texts()
buttons = InlineKeyboards()


# ─── Просмотр предложения ────────────────────────────────────────────────────

@r.callback_query(F.data == "offer_view")
async def offer_view_handler(call: CallbackQuery, user):
    """Кнопка 'Спец предложение' в профиле → показываем текст и кнопки."""
    offer = await db.special_offer.get_active(user.telegram_id)

    await call.answer()

    if not offer:
        await call.message.edit_text(
            texts.special_offer.NO_OFFER,
            reply_markup=buttons.special_offer.back_to_profile(),
        )
        return
    
    await send_offer(call, offer.keys_count, offer.expires_at, offer.custom_text)


# ─── Подумаю ─────────────────────────────────────────────────────────────────

@r.callback_query(F.data == "offer_decline")
async def offer_decline_handler(call: CallbackQuery, user):
    """Подумаю → показываем текст с временем действия и кнопку назад."""
    offer = await db.special_offer.get_active(user.telegram_id)

    await call.answer()

    await call.message.edit_text(
        texts.special_offer.OFFER_DECLINED.format(
            expires_at=to_msk(offer.expires_at).strftime("%d.%m.%Y %H:%M") if offer else "—",
        ),
        reply_markup=buttons.special_offer.back_to_profile(),
    )


# ─── Принять ─────────────────────────────────────────────────────────────────

@r.callback_query(F.data == "offer_accept")
async def offer_accept_handler(call: CallbackQuery, state: FSMContext, user):
    """Принять → деактивируем оффер и кидаем к выбору метода оплаты."""
    offer = await db.special_offer.get_active(user.telegram_id)

    await call.answer()

    if not offer:
        await call.message.edit_text(
            texts.special_offer.NO_OFFER,
            reply_markup=buttons.special_offer.back_to_profile(),
        )
        return

    # Деактивируем оффер — он использован
    # await db.special_offer.deactivate(user.telegram_id)

    # Кладём кол-во ключей в state как обычный заказ и добавляем id оффера
    await state.update_data(amount=offer.keys_count, special_offer_id=offer.id)

    # Редиректим на выбор метода оплаты
    await confirm_order_handler(call)
