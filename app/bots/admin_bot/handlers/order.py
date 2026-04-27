from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.shared import db
from app.services import order_service
from ..states import OrderStates
from ..texts import Texts, ButtonTexts
from ..keyboards import InlineKeyboards, ReplyKeyboards

r = Router()

texts = Texts()
buttons = InlineKeyboards()
reply = ReplyKeyboards()


# ─── Список паёв ─────────────────────────────────────────────────────────────

@r.message(F.text == ButtonTexts.menu.CREATE_PIE)
async def order_list_handler(msg: Message, state: FSMContext):
    """Кнопка меню → показываем список активных паёв + кнопку 'Создать'."""
    await msg.delete()
    await state.clear()
    await _show_order_list(msg)


async def _show_order_list(target: Message | CallbackQuery):
    """Показывает список паёв. Принимает и Message, и CallbackQuery."""
    orders = await db.order.get_all_active()
    text = texts.order.CURRENT_ORDERS.format(count=len(orders) or "нет активных")
    keyboard = await buttons.order.order_list(orders)

    if isinstance(target, Message):
        await target.answer(text, reply_markup=keyboard)
    else:
        await target.message.edit_text(text, reply_markup=keyboard)


# ─── Детали пая ──────────────────────────────────────────────────────────────

@r.callback_query(F.data.startswith("order_info_"))
async def order_info_handler(call: CallbackQuery):
    """Нажатие на пай → редактируем сообщение с деталями + кнопки Назад/Удалить."""
    order_id = int(call.data.split("_")[2])
    order = await db.order.get_by_id(order_id)

    await call.answer()

    if not order:
        await call.message.edit_text(
            texts.order.ORDER_NOT_FOUND,
            reply_markup=buttons.order.back(),
        )
        return

    await call.message.edit_text(
        texts.order.ORDER_DETAIL.format(
            id=order.id,
            total_keys=order.total_keys,
            price_per_key=order.price_per_key,
            expires_at=order.expires_at.strftime("%d.%m.%Y %H:%M"),
        ),
        reply_markup=buttons.order.order_detail(order.id),
    )


# ─── Назад к списку ──────────────────────────────────────────────────────────

@r.callback_query(F.data == "order_back")
async def order_back_handler(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.clear()
    await _show_order_list(call)


# ─── Удаление пая ────────────────────────────────────────────────────────────

@r.callback_query(F.data.startswith("order_delete_"))
async def order_delete_handler(call: CallbackQuery):
    """Удаляет пай и возвращает к обновлённому списку."""
    order_id = int(call.data.split("_")[2])
    deleted = await db.order.delete(order_id)

    await call.answer()

    if not deleted:
        await call.message.edit_text(
            texts.order.ORDER_NOT_FOUND,
            reply_markup=buttons.order.back(),
        )
        return

    orders = await db.order.get_all_active()
    await call.message.edit_text(
        texts.order.ORDER_DELETED.format(order_id=order_id) +
        texts.order.CURRENT_ORDERS.format(count=len(orders) or "нет активных"),
        reply_markup=await buttons.order.order_list(orders),
    )


# ─── Создание: шаг 1 — количество ключей ─────────────────────────────────────

@r.callback_query(F.data == "order_create")
async def order_create_start(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(OrderStates.waiting_keys_count)
    await call.message.edit_text(texts.order.ENTER_KEYS_COUNT)


@r.message(OrderStates.waiting_keys_count)
async def order_keys_handler(msg: Message, state: FSMContext):
    raw = msg.text.strip()

    if not raw.isdigit() or int(raw) <= 0:
        await msg.answer(texts.order.INVALID_NUMBER)
        return

    await state.update_data(keys_count=int(raw))
    await state.set_state(OrderStates.waiting_price)
    await msg.answer(texts.order.ENTER_PRICE)


# ─── Создание: шаг 2 — цена за ключ ─────────────────────────────────────────

@r.message(OrderStates.waiting_price)
async def order_price_handler(msg: Message, state: FSMContext):
    raw = msg.text.strip().replace(",", ".")

    try:
        price = float(raw)
        if price <= 0:
            raise ValueError
    except ValueError:
        await msg.answer(texts.order.INVALID_PRICE)
        return

    data = await state.get_data()
    order = await order_service.create(
        total_keys=data["keys_count"],
        price_per_key=price,
    )
    await state.clear()

    await msg.answer(
        texts.order.ORDER_CREATED.format(
            order_id=order.id,
            total_keys=order.total_keys,
            price_per_key=order.price_per_key,
            expires_at=order.expires_at.strftime("%d.%m.%Y %H:%M"),
        ),
        reply_markup=buttons.order.order_detail(order.id),
    )