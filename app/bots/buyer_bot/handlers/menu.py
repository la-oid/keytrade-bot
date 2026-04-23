from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from ..texts import Texts
from ..keyboards import InlineKeyboards

r = Router()

texts = Texts()
buttons = InlineKeyboards()


@r.callback_query(F.data == "profile")
async def profile_handler(call: CallbackQuery, user):
    await call.answer()
    await call.message.edit_text(
        texts.menu.PROFILE_TEXT.format(user_id=user.telegram_id, orders="Заказов пока нет"),
        reply_markup=buttons.menu.profile
    )


@r.callback_query(F.data == "about")
async def about_handler(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(
        texts.menu.ABOUT_TEXT,
        reply_markup=buttons.menu.back_to_menu
    )


@r.callback_query(F.data == "support")
async def support_handler(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(
        texts.menu.SUPPORT_TEXT,
        reply_markup=buttons.menu.back_to_menu
    )


@r.callback_query(F.data == "back_to_menu")
async def back_to_menu_handler(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.answer()
    await call.message.edit_text(
        texts.menu.START_TEXT,
        reply_markup=buttons.menu.start
    )
