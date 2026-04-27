from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.shared import db
from ..texts import Texts
from ..keyboards import ReplyKeyboards

r = Router()

texts = Texts()
reply = ReplyKeyboards()


@r.message(CommandStart())
async def start_handler(msg: Message, user):
    # Отвечаем обычным приветствием с меню
    
    await msg.answer(
        texts.menu.START_TEXT,
        reply_markup=reply.menu.menu
    )