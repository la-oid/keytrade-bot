from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

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


@r.message(F.text == ButtonTexts.menu.ABOUT)
async def about_reply_handler(msg: Message):
    await msg.delete()
    await msg.answer(texts.menu.ABOUT_TEXT)


@r.message(F.text == ButtonTexts.menu.SUPPORT)
async def support_reply_handler(msg: Message):
    await msg.delete()
    await msg.answer(texts.menu.SUPPORT_TEXT)