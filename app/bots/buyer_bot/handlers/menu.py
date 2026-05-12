from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, FSInputFile

from app.shared.images import BuyerImages
from ..texts import Texts, ButtonTexts
from ..keyboards import InlineKeyboards

r = Router()

texts = Texts()
buttons = InlineKeyboards()


@r.callback_query(F.data == "profile")
@r.message(F.text == ButtonTexts.menu.PROFILE)
async def profile_handler(event: Message | CallbackQuery, user):
    text = texts.menu.PROFILE_TEXT.format(user_id=user.telegram_id)
    kb = await buttons.menu.profile(user.telegram_id)
    photo = FSInputFile(BuyerImages.PROFILE)

    if isinstance(event, CallbackQuery):
        await event.answer()
        await event.message.delete()
        await event.message.answer_photo(photo=photo, caption=text, reply_markup=kb)
    else:
        await event.delete()
        await event.answer_photo(photo=photo, caption=text, reply_markup=kb)


@r.message(F.text == ButtonTexts.menu.ABOUT)
async def about_reply_handler(msg: Message):
    await msg.delete()
    await msg.answer(texts.menu.ABOUT_TEXT)


@r.message(F.text == ButtonTexts.menu.SUPPORT)
async def support_reply_handler(msg: Message):
    await msg.delete()
    await msg.answer(texts.menu.SUPPORT_TEXT, reply_markup=buttons.menu.support)
