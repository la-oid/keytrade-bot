from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.shared import db
from ..states import BlockStates
from ..texts import Texts, ButtonTexts
from ..keyboards import InlineKeyboards

r = Router()

texts = Texts()
buttons = InlineKeyboards()


# ─── Utils ───────────────────────────────────────────────────────────────────

async def _show_user_status(target: Message | CallbackQuery, user_id: int, is_blocked: bool):
    """Показывает статус пользователя с нужной кнопкой."""
    text = texts.block.USER_STATUS.format(
        user_id=user_id,
        status=texts.block.STATUS_BLOCKED if is_blocked else texts.block.STATUS_ACTIVE,
    )
    keyboard = buttons.block.actions(user_id, is_blocked=is_blocked)

    if isinstance(target, Message):
        await target.answer(text, reply_markup=keyboard)
    else:
        await target.message.edit_text(text, reply_markup=keyboard)


async def _update_block_status(call: CallbackQuery, user_id: int, is_blocked: bool):
    """Меняет статус блокировки и обновляет сообщение."""
    await db.user.upsert_user(user_id, is_blocked=is_blocked)
    await _show_user_status(call, user_id, is_blocked)


# ─── Ввод ID пользователя ────────────────────────────────────────────────────

@r.message(F.text == ButtonTexts.menu.BLOCK_USER)
async def block_start_handler(msg: Message, state: FSMContext):
    """Кнопка меню → просим ввести ID пользователя."""
    await msg.delete()
    await state.set_state(BlockStates.waiting_user_id)
    await msg.answer(texts.block.ENTER_USER_ID)


@r.message(BlockStates.waiting_user_id)
async def block_user_id_handler(msg: Message, state: FSMContext):
    """ID введён → показываем статус и кнопку действия."""
    if not msg.text.isdigit():
        await msg.answer(texts.misc.INVALID_USER_ID)
        return

    user_id = int(msg.text)
    user = await db.user.get_user_by_telegram_id(user_id)

    if not user:
        await msg.answer(texts.block.USER_NOT_FOUND)
        return

    await state.clear()
    await _show_user_status(msg, user.telegram_id, user.is_blocked)


# ─── Заблокировать ───────────────────────────────────────────────────────────

@r.callback_query(F.data.startswith("block_user_"))
async def block_user_handler(call: CallbackQuery):
    await call.answer()
    await _update_block_status(call, int(call.data.split("_")[2]), is_blocked=True)


# ─── Разблокировать ──────────────────────────────────────────────────────────

@r.callback_query(F.data.startswith("unblock_user_"))
async def unblock_user_handler(call: CallbackQuery):
    await call.answer()
    await _update_block_status(call, int(call.data.split("_")[2]), is_blocked=False)