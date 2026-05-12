from datetime import timedelta

from aiogram.types import Message, CallbackQuery

from app.shared import bots
from app.utils import safe_edit
from app.shared.constants import KEY_PRICE_BUYER
from app.utils import to_msk
from ..texts import Texts
from ..keyboards import InlineKeyboards

texts   = Texts()
buttons = InlineKeyboards()


async def send_offer(target: int | Message | CallbackQuery, keys_count: int, expires_at, custom_text: str | None = None) -> bool:
    """
    Отправляет спецпредложение.
    Используется везде: scheduler, admin, профиль.
    """

    text = (
        (
            (custom_text + "\n\n") if custom_text else
            texts.special_offer.OFFER_TEXT_DEFAULT.format(keys_count=keys_count) 
        ) +
        texts.special_offer.OFFER_FOOTER.format(
            keys_count=keys_count,
            total_price=keys_count * KEY_PRICE_BUYER,
            expires_at=to_msk(expires_at).strftime("%d.%m.%Y %H:%M"),
        )
    )
    keyboard = buttons.special_offer.offer_actions()

    try:
        # target: int — отправляет новое сообщение через buyer bot
        if isinstance(target, int):
            await bots.buyer.bot.send_message(
                chat_id=target,
                text=text,
                reply_markup=keyboard,
            )

        # target: CallbackQuery — редактирует сообщение
        elif isinstance(target, CallbackQuery):
            await safe_edit(target.message, text, reply_markup=keyboard)

        # target: Message — отвечает на сообщение
        else:
            await target.answer(
                text,
                reply_markup=keyboard,
            )

        return True
    
    except Exception:
        return False
