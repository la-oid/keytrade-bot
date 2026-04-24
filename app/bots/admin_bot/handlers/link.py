from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from app.shared.config import settings
from app.shared import bots
from ..states import LinkStates
from ..texts import Texts
from ..keyboards import InlineKeyboards

r = Router()

texts = Texts()
buttons = InlineKeyboards()


@r.callback_query(F.data == "get_link")
async def get_link_handler(call: CallbackQuery, state: FSMContext):
    """Получение ссылки → просим ввести данные."""
    await state.set_state(LinkStates.waiting_data)
    await call.answer()
    await call.message.answer(texts.link.ENTER_DATA)


@r.message(LinkStates.waiting_data)
async def enter_data_handler(msg: Message, state: FSMContext):
    """Данные введены → парсим и просим ID пользователя."""
    raw = msg.text.replace(" ", "")
    parts = raw.split(",")

    if len(parts) != 3:
        await msg.answer(texts.link.INVALID_DATA)
        return

    bank, amount, requisite = parts
    await state.update_data(bank=bank, amount=amount, requisite=requisite)
    await state.set_state(LinkStates.waiting_user_id)
    await msg.answer(texts.link.ENTER_USER_ID)


@r.message(LinkStates.waiting_user_id)
async def enter_user_id_handler(msg: Message, state: FSMContext):
    """ID введён → генерируем ссылку и отправляем пользователю."""
    if not msg.text.isdigit():
        await msg.answer(texts.link.INVALID_USER_ID)
        return

    user_id = int(msg.text)
    data = await state.get_data()
    bank = data["bank"]
    amount = data["amount"]
    requisite = data["requisite"]

    url = f"{settings.app.PAYMENT_URL}?bank={bank}&amount={amount}&requisite={requisite}"

    await bots.buyer.bot.send_message(
        chat_id=user_id,
        text=texts.link.PAYMENT_LINK.format(url=url)
    )

    await state.clear()
    await msg.answer(
        texts.link.LINK_SENT.format(user_id=user_id),
        reply_markup=buttons.menu.start
    )