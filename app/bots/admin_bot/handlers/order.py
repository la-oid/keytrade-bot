from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.shared import db
from app.services import order_service
from ..states import OrderStates
from ..texts import Texts, ButtonTexts
from ..keyboards import InlineKeyboards
from ..utils import parse_order_create

r = Router()

texts = Texts()
buttons = InlineKeyboards()


# ─── Меню паёв ───────────────────────────────────────────────────────────────

@r.message(F.text == ButtonTexts.menu.CREATE_PIE)
async def order_menu_handler(msg: Message, state: FSMContext):
    """Кнопка меню → текст с кол-вом паёв + кнопки Создать/Удалить."""
    await msg.delete()
    await state.clear()
    await _show_order_menu(msg)


async def _show_order_menu(target: Message | CallbackQuery):
    """Показывает меню паёв. Принимает и Message, и CallbackQuery."""
    orders = await db.order.get_all_active()
    text = texts.order.CURRENT_ORDERS.format(
        count=len(orders) if orders else "нет активных"
    )

    if isinstance(target, Message):
        await target.answer(text, reply_markup=buttons.order.order_menu())
    else:
        await target.message.edit_text(text, reply_markup=buttons.order.order_menu())


@r.callback_query(F.data == "order_back")
async def order_back_handler(call: CallbackQuery, state: FSMContext):
    """Назад → возвращаем к меню паёв."""
    await call.answer()
    await state.clear()
    await _show_order_menu(call)


# ─── Создание пая ────────────────────────────────────────────────────────────

@r.callback_query(F.data == "order_create")
async def order_create_start(call: CallbackQuery, state: FSMContext):
    """Кнопка Создать → редактируем сообщение, просим ввести данные."""
    await call.answer()
    await state.set_state(OrderStates.waiting_create_data)
    await call.message.edit_text(texts.order.ENTER_CREATE_DATA)


@r.message(OrderStates.waiting_create_data)
async def order_create_handler(msg: Message, state: FSMContext):
    """Данные введены → парсим, создаём пай, показываем результат."""
    parsed = parse_order_create(msg.text)

    if not parsed:
        await msg.answer(texts.order.INVALID_DATA)
        return

    keys_count, price, lifetime_hours = parsed
    order = await order_service.create(
        total_keys=keys_count,
        price_per_key=price,
        lifetime_hours=lifetime_hours,
    )
    await state.clear()

    await msg.answer(
        texts.order.ORDER_CREATED.format(
            order_id=order.id,
            total_keys=order.total_keys,
            price_per_key=order.price_per_key,
            expires_at=order.expires_at.strftime("%d.%m.%Y %H:%M"),
        ),
        reply_markup=buttons.order.back_to_menu(),
    )


# ─── Удаление пая ────────────────────────────────────────────────────────────

@r.callback_query(F.data == "order_delete_menu")
async def order_delete_menu_handler(call: CallbackQuery):
    """Кнопка Удалить → редактируем сообщение, показываем список паёв."""
    await call.answer()
    orders = await db.order.get_all_active()
    await call.message.edit_text(
        texts.order.DELETE_LIST,
        reply_markup=buttons.order.delete_list(orders),
    )


@r.callback_query(F.data.startswith("order_delete_"))
async def order_delete_handler(call: CallbackQuery):
    """Нажатие на пай → удаляем, показываем подтверждение + кнопку Назад."""
    order_id = int(call.data.split("_")[2])
    order = await db.order.get_by_id(order_id)

    await call.answer()

    if not order:
        await call.message.edit_text(
            texts.order.ORDER_NOT_FOUND,
            reply_markup=buttons.order.back_to_delete_list(),
        )
        return

    total_sum = float(order.total_keys * order.price_per_key)
    await db.order.delete(order_id)

    await call.message.edit_text(
        texts.order.ORDER_DELETED.format(
            order_id=order_id,
            total_sum=total_sum,
        ),
        reply_markup=buttons.order.back_to_delete_list(),
    )