from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.shared import db
from ..texts import Texts
from ..keyboards import InlineKeyboards

r = Router()


@r.message(CommandStart())
async def start_handler(msg: Message):
    
    # Получаем пользователя из базы и его язык
    user = await db.user.upsert_user (
        telegram_id=msg.from_user.id,
        username=msg.from_user.username,
        first_name=msg.from_user.first_name,
        last_name=msg.from_user.last_name,
    )
    
    texts = Texts()
    buttons = InlineKeyboards()

    # Отвечаем обычным приветствием с меню
    await msg.answer(
        texts.menu.START_TEXT,
        reply_markup=buttons.menu.start
    )