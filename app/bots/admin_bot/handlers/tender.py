from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.services import tender_service
from ..states import TenderStates
from ..texts import Texts, ButtonTexts
from ..keyboards import InlineKeyboards

r = Router()

texts   = Texts()
buttons = InlineKeyboards()


# ─── Меню тендера ────────────────────────────────────────────────────────────

@r.message(F.text == ButtonTexts.menu.TENDER)
async def tender_menu(msg: Message, state: FSMContext):
    """Кнопка меню → показываем текущий статус и действия."""
    await msg.delete()
    await state.clear()
    tender = await tender_service.get_active()
    status = (
        texts.tender.STATUS.format(current=tender.current_keys, total=tender.total_keys)
        if tender else texts.tender.NO_ACTIVE
    )
    await msg.answer(status, reply_markup=buttons.tender.actions())


# ─── Добавить вручную ─────────────────────────────────────────────────────────

@r.callback_query(F.data == "tender_add")
async def tender_add_start(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(TenderStates.waiting_add)
    await call.message.edit_text(texts.tender.ENTER_ADD)


@r.message(TenderStates.waiting_add)
async def tender_add_submit(msg: Message, state: FSMContext):
    if not msg.text.isdigit() or int(msg.text) <= 0:
        await msg.answer(texts.tender.INVALID_COUNT)
        return

    amount = int(msg.text)
    await state.clear()
    tender = await tender_service.add_manually(amount)

    await msg.answer(
        texts.tender.ADDED.format(
            amount=amount,
            current=tender.current_keys if tender else 0,
            total=tender.total_keys if tender else 0,
        )
    )


# ─── Поставить в очередь ──────────────────────────────────────────────────────

@r.callback_query(F.data == "tender_queue")
async def tender_queue_start(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(TenderStates.waiting_queue)
    await call.message.edit_text(texts.tender.ENTER_COUNT)


@r.message(TenderStates.waiting_queue)
async def tender_queue_submit(msg: Message, state: FSMContext):
    if not msg.text.isdigit() or int(msg.text) <= 0:
        await msg.answer(texts.tender.INVALID_COUNT)
        return

    total_keys = int(msg.text)
    await state.clear()
    await tender_service.add_to_queue(total_keys)

    await msg.answer(texts.tender.QUEUED.format(total=total_keys))


# ─── Запустить сейчас ─────────────────────────────────────────────────────────

@r.callback_query(F.data == "tender_launch")
async def tender_launch_start(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(TenderStates.waiting_launch)
    await call.message.edit_text(texts.tender.ENTER_COUNT)


@r.message(TenderStates.waiting_launch)
async def tender_launch_submit(msg: Message, state: FSMContext):
    if not msg.text.isdigit() or int(msg.text) <= 0:
        await msg.answer(texts.tender.INVALID_COUNT)
        return

    total_keys = int(msg.text)
    await state.clear()
    tender = await tender_service.launch_now(total_keys)

    await msg.answer(texts.tender.LAUNCHED.format(total=tender.total_keys))
