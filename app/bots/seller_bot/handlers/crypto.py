from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.shared import db, bots, settings
from app.shared.constants import CRYPTO_RATE_MARKUP_SELLER
from app.utils import get_usdt_rub_rate, get_network_by_id, notify_admins
from ..states import CryptoStates
from ..texts import Texts
from ..keyboards import InlineKeyboards

r = Router()

texts   = Texts()
buttons = InlineKeyboards()


# ─── Выбор крипты ────────────────────────────────────────────────────────────

@r.callback_query(F.data == "cashout_crypto")
async def cashout_crypto_handler(call: CallbackQuery, state: FSMContext):
    """Крипта → показываем список сетей с курсом и суммой в USDT."""
    data   = await state.get_data()
    amount = data.get("amount", 0)

    try:
        rate        = await get_usdt_rub_rate() + CRYPTO_RATE_MARKUP_SELLER
        usdt_amount = round(amount / rate, 4)
    except Exception:
        await call.answer(texts.crypto.RATE_ERROR, show_alert=True)
        return

    await state.update_data(usdt_amount=usdt_amount)

    await call.answer()
    await call.message.edit_text(
        texts.crypto.CHOOSE_NETWORK.format(
            rate=rate,
            amount=amount,
            usdt_amount=usdt_amount,
        ),
        reply_markup=buttons.crypto.network_list(),
    )


# ─── Выбор сети → ввод адреса кошелька ──────────────────────────────────────

@r.callback_query(F.data.startswith("cashout_network_"))
async def cashout_network_handler(call: CallbackQuery, state: FSMContext):
    """Сеть выбрана → просим ввести адрес кошелька."""
    network_id = call.data.split("_")[2]
    network    = get_network_by_id(network_id)

    if not network:
        await call.answer()
        return

    await state.update_data(network_id=network_id)
    await state.set_state(CryptoStates.waiting_wallet_address)

    await call.answer()
    await call.message.edit_text(
        texts.crypto.ENTER_WALLET.format(network=network.name)
    )


# ─── Ввод адреса кошелька ────────────────────────────────────────────────────

@r.message(CryptoStates.waiting_wallet_address)
async def cashout_wallet_handler(msg: Message, state: FSMContext, user):
    """Адрес введён → создаём заявку и уведомляем админа."""
    wallet = msg.text.strip()

    if not wallet:
        await msg.answer(texts.crypto.INVALID_WALLET)
        return

    data        = await state.get_data()
    amount      = data["amount"]
    network_id  = data["network_id"]
    usdt_amount = data.get("usdt_amount", 0)
    network     = get_network_by_id(network_id)

    # Списываем баланс
    await db.user.upsert_user(user.telegram_id, balance=float(user.balance or 0) - amount)

    # Создаём заявку
    cashout = await db.cashout.upsert_cashout(
        user_id=user.telegram_id,
        amount=amount,
        network_id=network_id,
        wallet_address=wallet,
        usdt_amount=usdt_amount,
    )

    await state.clear()
    await msg.delete()
    await msg.answer(
        texts.crypto.CREATED_CRYPTO.format(
            cashout_id=cashout.id,
            amount=amount,
            usdt_amount=usdt_amount,
            network=network.name if network else network_id,
            wallet=wallet,
        )
    )

    # Уведомляем админов
    await notify_admins(
        texts.crypto.ADMIN_NOTIFY_CRYPTO.format(
            user_id=user.telegram_id,
            amount=amount,
            usdt_amount=usdt_amount,
            network=network.name if network else network_id,
            wallet=wallet,
            cashout_id=cashout.id
        ),
        reply_markup=buttons.cashout.cashout_notify(cashout.id)
    )
