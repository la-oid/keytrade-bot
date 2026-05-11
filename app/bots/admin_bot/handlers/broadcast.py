from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from ..states import BroadcastStates
from ..texts import Texts, ButtonTexts
from ..keyboards import InlineKeyboards
from ..utils import broadcast_to_users

r = Router()

texts   = Texts()
buttons = InlineKeyboards()


# ─── Старт ───────────────────────────────────────────────────────────────────

@r.message(F.text == ButtonTexts.menu.BROADCAST)
async def broadcast_start(msg: Message, state: FSMContext):
    """Кнопка меню → просим ввести текст рассылки."""
    await msg.delete()
    await state.set_state(BroadcastStates.waiting_text)
    await msg.answer(texts.broadcast.ENTER_TEXT)


# ─── Ввод текста ─────────────────────────────────────────────────────────────

@r.message(BroadcastStates.waiting_text)
async def broadcast_text(msg: Message, state: FSMContext):
    """Текст введён → показываем превью и просим подтверждение."""
    await state.update_data(text=msg.text)
    await state.set_state(BroadcastStates.confirm)
    await msg.answer(
        texts.broadcast.CONFIRM_PREVIEW.format(text=msg.text),
        reply_markup=buttons.broadcast.confirm(),
    )


# ─── Подтверждение ───────────────────────────────────────────────────────────

@r.callback_query(F.data == "broadcast_confirm")
async def broadcast_confirm(call: CallbackQuery, state: FSMContext):
    """Да → рассылаем сообщение всем пользователям."""
    data = await state.get_data()
    await call.answer()
    await state.clear()

    await call.message.edit_text(texts.broadcast.SENDING)

    sent, failed = await broadcast_to_users(data["text"])

    await call.message.edit_text(
        texts.broadcast.DONE.format(sent=sent, failed=failed)
    )


# ─── Ввести заново ───────────────────────────────────────────────────────────

@r.callback_query(F.data == "broadcast_retry")
async def broadcast_retry(call: CallbackQuery, state: FSMContext):
    """Нет → возвращаемся к вводу текста."""
    await call.answer()
    await state.set_state(BroadcastStates.waiting_text)
    await call.message.edit_text(texts.broadcast.ENTER_TEXT)
