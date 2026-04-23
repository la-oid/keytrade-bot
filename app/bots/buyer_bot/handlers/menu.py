from aiogram import Router, F
from aiogram.types import CallbackQuery

from ..texts import Texts
from ..keyboards import InlineKeyboards

r = Router()

texts = Texts()
buttons = InlineKeyboards()


@r.callback_query(F.data == "profile")
async def profile_handler(call: CallbackQuery, user):
    await call.answer()
    texts.menu.PROFILE_TEXT.format(user_id=user.telegram_id, orders="Заказов пока нет")


@r.callback_query(F.data == "about")
async def about_handler(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(texts.menu.ABOUT_TEXT)


@r.callback_query(F.data == "support")
async def support_handler(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(texts.menu.SUPPORT_TEXT)