from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.shared import db
from app.shared.constants import KEY_PRICE
from app.services import key_service
from ..states import MarketStates
from ..texts import Texts
from ..keyboards import InlineKeyboards
from ..utils import parse_keys_file

r = Router()

texts = Texts()
buttons = InlineKeyboards()


# ─── Выбор пая → подтверждение ───────────────────────────────────────────────

@r.callback_query(F.data.startswith("market_take_"))
async def market_take_handler(call: CallbackQuery):
    """Нажали на пай → редактируем сообщение, спрашиваем подтверждение."""
    order_id = int(call.data.split("_")[2])
    order = await db.order.get_by_id(order_id)

    await call.answer()

    if not order or not order.is_active:
        await call.message.edit_text(texts.market.ORDER_NOT_FOUND)
        return

    await call.message.edit_text(
        texts.market.CONFIRM.format(id=order.id, total_keys=order.total_keys),
        reply_markup=buttons.market.confirm(order.id),
    )


# ─── Принять → ждём .txt ─────────────────────────────────────────────────────

@r.callback_query(F.data.startswith("market_accept_"))
async def market_accept_handler(call: CallbackQuery, state: FSMContext):
    """Нажали Принять → переходим в ожидание файла."""
    order_id = int(call.data.split("_")[2])
    order = await db.order.get_by_id(order_id)

    await call.answer()

    if not order or not order.is_active:
        await call.message.edit_text(texts.market.ORDER_NOT_FOUND)
        return

    await state.set_state(MarketStates.waiting_keys_file)
    await state.update_data(order_id=order.id)
    await call.message.edit_text(
        texts.market.SEND_KEYS.format(total_keys=order.total_keys)
    )


# ─── Получили .txt → проверяем и продаём ─────────────────────────────────────

@r.message(MarketStates.waiting_keys_file, F.document)
async def market_keys_received(msg: Message, state: FSMContext, user):
    """Получили файл → парсим, валидируем, продаём."""
    data = await state.get_data()
    order = await db.order.get_by_id(data["order_id"])

    if not order or not order.is_active:
        await state.clear()
        await msg.answer(texts.market.ORDER_NOT_FOUND)
        return

    if not msg.document.file_name.lower().endswith(".txt"):
        await msg.answer(texts.market.INVALID_FORMAT)
        return
    
    # Удаляем сообщение пользователя с файлом
    # await msg.delete()

    # Отправляем "идёт проверка" и запоминаем чтобы потом редактировать
    status_msg = await msg.answer(texts.market.CHECKING)

    # Скачиваем и парсим файл
    file = await msg.bot.get_file(msg.document.file_id)
    buffer = await msg.bot.download_file(file.file_path)
    content = buffer.read().decode("utf-8", errors="ignore")
    keys = parse_keys_file(content)

    # Количество не совпадает или парсинг провалился
    if not keys or len(keys) != order.total_keys:
        await status_msg.edit_text(texts.market.INVALID_FORMAT)
        return

    # Атомарно: validate + sell внутри key_service
    sold = await key_service.sell(keys, owner_id=user.telegram_id, order_id=order.id)
    if not sold:
        await status_msg.edit_text(texts.market.INVALID_FORMAT)
        return

    # Закрываем пай и зачисляем баланс
    await db.order.set_active(order.id, False)
    payout = order.total_keys * KEY_PRICE
    new_balance = (user.balance or 0) + payout
    new_count = (user.completed_orders_count or 0) + 1
    
    await db.user.upsert_user(
        user.telegram_id,
        balance=new_balance,
        completed_orders_count=new_count,
    )

    await state.clear()
    await status_msg.edit_text(texts.market.SUCCESS.format(payout=payout))


@r.message(MarketStates.waiting_keys_file)
async def market_keys_not_document(msg: Message):
    """Прислали что-то кроме документа — просим .txt."""
    await msg.answer(texts.market.INVALID_FORMAT)
