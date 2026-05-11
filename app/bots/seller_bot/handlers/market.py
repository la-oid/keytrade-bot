import asyncio
import time

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.shared import db
from app.shared.constants import KEY_PRICE_SELLER, KEY_CHECK_DURATION
from app.services import key_service, tender_service
from ..states import MarketStates
from ..texts import Texts
from ..keyboards import InlineKeyboards
from ..utils import parse_keys_file, is_text_file, download_text_file

r = Router()

texts = Texts()
buttons = InlineKeyboards()


# ─── Выбор пая → подтверждение ───────────────────────────────────────────────

@r.callback_query(F.data.startswith("market_take_"))
async def market_take_handler(call: CallbackQuery):
    """Нажали на пай → редактируем сообщение, спрашиваем подтверждение."""
    order_id = call.data.split("_")[2]
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
    order_id = call.data.split("_")[2]
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


# ─── Utils ───────────────────────────────────────────────────────────────────

async def _process_keys(state: FSMContext, order, user, content: str) -> str:
    """
    Валидирует и продаёт ключи из файла.
    Возвращает текст результата — успех или ошибку.
    """
    keys = parse_keys_file(content)

    if not keys or len(keys) != order.total_keys:
        return texts.market.INVALID_FORMAT

    sold = await key_service.sell(keys, owner_id=user.telegram_id, order_id=order.id)
    if not sold:
        return texts.market.INVALID_FORMAT
    
    
    # Начисляем баланс продавцу — при 2-й продаже замораживаем
    payout = order.total_keys * KEY_PRICE_SELLER
    is_second_sale = (user.completed_orders_count or 0) == 1

    if is_second_sale:
        await db.user.upsert_user(
            user.telegram_id,
            frozen_balance=(user.frozen_balance or 0) + payout,
            completed_orders_count=(user.completed_orders_count or 0) + 1,
        )
    else:
        await db.user.upsert_user(
            user.telegram_id,
            balance=(user.balance or 0) + payout,
            completed_orders_count=(user.completed_orders_count or 0) + 1,
        )


    # Деактивируем пай после успешной продажи
    await db.order.set_active(order.id, False)

    # Учитываем в тендере (паи > TENDER_MAX_PIE_KEYS игнорируются внутри сервиса)
    await tender_service.add_keys_from_order(order.total_keys)

    await state.clear()
    return texts.market.SUCCESS.format(payout=payout)


# ─── Получили .txt → проверяем и продаём ─────────────────────────────────────

@r.message(MarketStates.waiting_keys_file, F.document)
async def market_keys_received(msg: Message, state: FSMContext, user):
    """Получили файл → показываем статус, проверяем, показываем результат."""
    data  = await state.get_data()
    order = await db.order.get_by_id(data["order_id"])

    # Пай мог истечь пока пользователь готовил файл
    if not order or not order.is_active:
        await state.clear()
        await msg.answer(texts.market.ORDER_NOT_FOUND)
        return

    # Принимаем только .txt файлы
    if not is_text_file(msg.document):
        await msg.answer(texts.market.INVALID_FORMAT)
        return

    status_msg = await msg.answer(texts.market.CHECKING)
    started    = time.monotonic()

    content = await download_text_file(msg)
    result  = await _process_keys(state, order, user, content)

    # Добиваем до KEY_CHECK_DURATION секунд если проверка была быстрее
    elapsed = time.monotonic() - started
    if elapsed < KEY_CHECK_DURATION:
        await asyncio.sleep(KEY_CHECK_DURATION - elapsed)

    await status_msg.edit_text(result)


@r.message(MarketStates.waiting_keys_file)
async def market_keys_not_document(msg: Message):
    """Прислали что-то кроме документа — просим .txt."""
    await msg.answer(texts.market.INVALID_FORMAT)
