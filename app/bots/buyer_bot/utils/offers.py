from aiogram.types import Message, CallbackQuery

from app.shared import bots
from app.shared.constants import KEY_PRICE
from ..texts import Texts
from ..keyboards import InlineKeyboards

texts   = Texts()
buttons = InlineKeyboards()


async def send_offer(target: int | Message | CallbackQuery, keys_count: int, expires_at, custom_text: str | None = None) -> bool:
    """
    Отправляет спецпредложение.
    Используется везде: scheduler, admin, профиль.
    """

    text = custom_text or texts.special_offer.OFFER_TEXT.format(
        keys_count=keys_count,
        total_price=keys_count * KEY_PRICE,
        expires_at=expires_at.strftime("%d.%m.%Y %H:%M"),
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
            await target.message.edit_text(
                text,
                reply_markup=keyboard,
            )

        # target: Message — отвечает на сообщение
        else:
            await target.answer(
                text,
                reply_markup=keyboard,
            )

        return True
    
    except Exception:
        return False