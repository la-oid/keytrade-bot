from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from app.shared.config import settings
from ..texts import Texts, ButtonTexts
from ..keyboards import InlineKeyboards

r = Router()

texts = Texts()
buttons = InlineKeyboards()


@r.callback_query(F.data == "profile")
@r.message(F.text == ButtonTexts.menu.PROFILE)
async def profile_handler(event: Message | CallbackQuery, user):
    text = texts.menu.PROFILE_TEXT.format(user_id=user.telegram_id)
    kb = buttons.menu.profile

    if isinstance(event, CallbackQuery):
        await event.answer()
        await event.message.edit_text(text, reply_markup=kb)
    else:
        await event.delete()
        await event.answer(text, reply_markup=kb)


@r.message(F.text == ButtonTexts.menu.MARKET)
async def market_handler(msg: Message):
    """Площадка заказов."""
    await msg.delete()
    await msg.answer(texts.menu.MARKET_STUB)


@r.message(F.text == ButtonTexts.menu.ABOUT)
async def about_handler(msg: Message):
    """О компании — статичный текст."""
    await msg.delete()
    await msg.answer(texts.menu.ABOUT_TEXT)


@r.message(F.text == ButtonTexts.menu.SUPPORT)
async def support_handler(msg: Message):
    """Поддержка — ссылка на саппорт."""
    await msg.delete()
    await msg.answer(texts.menu.SUPPORT_TEXT)