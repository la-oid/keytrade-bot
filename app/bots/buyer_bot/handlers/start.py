from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile

from app.shared.images import BuyerImages
from ..texts import Texts
from ..keyboards import InlineKeyboards, ReplyKeyboards

r = Router()

texts = Texts()
buttons = InlineKeyboards()
reply = ReplyKeyboards()


@r.message(CommandStart())
async def start_handler(msg: Message, user):
    await msg.answer_photo(
        photo=FSInputFile(BuyerImages.START),
        caption=texts.menu.START_TEXT,
        reply_markup=reply.menu.menu,
    )
