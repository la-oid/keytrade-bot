from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from ..texts import Texts
from ..keyboards import ReplyKeyboards

r = Router()

texts = Texts()
reply = ReplyKeyboards()


@r.message(CommandStart())
async def start_handler(msg: Message, user):
    """Приветствие + reply-меню."""
    
    await msg.answer(
        texts.menu.START_TEXT,
        reply_markup=reply.menu.menu,
    )