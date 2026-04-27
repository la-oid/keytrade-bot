from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.shared import db
from ..texts import Texts
from ..keyboards import InlineKeyboards, ReplyKeyboards

r = Router()

texts = Texts()
buttons = InlineKeyboards()
reply = ReplyKeyboards()


@r.message(CommandStart())
async def start_handler(msg: Message, user):
    await msg.answer(
        texts.menu.START_TEXT,
        reply_markup=reply.menu.menu
    )