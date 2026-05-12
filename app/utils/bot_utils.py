from aiogram.types import Message

from app.db.enums import PaymentStatus


# ─── Безопасное редактирование ───────────────────────────────────────────────

async def safe_edit(message: Message, text: str, reply_markup=None):
    """edit_text, но если сообщение с фото — удаляет и отправляет новое."""
    if message.photo:
        await message.delete()
        await message.answer(text, reply_markup=reply_markup)
    else:
        await message.edit_text(text, reply_markup=reply_markup)


# ─── Уведомление админов ─────────────────────────────────────────────────────

async def notify_admins(text: str, document=None, reply_markup=None) -> None:
    """Универсальная рассылка уведомления всем админам."""

    from app.shared import bots, settings

    for admin_id in settings.telegram.ADMIN_IDS:
        if document:
            await bots.admin.bot.send_document(
                chat_id=admin_id,
                document=document,
                caption=text,
                reply_markup=reply_markup,
            )
        else:
            await bots.admin.bot.send_message(chat_id=admin_id, text=text, reply_markup=reply_markup)


# ─── Уведомление пользователей ───────────────────────────────────────────────

async def notify_payment_expired(payment, from_status: PaymentStatus) -> None:
    """Уведомляет пользователя об истечении срока оплаты."""

    from app.shared import bots, settings
    from app.bots.buyer_bot.texts import Texts

    texts_map = {
        PaymentStatus.PENDING_PAY:  Texts.payment.PAYMENT_EXPIRED,
        PaymentStatus.PENDING_HASH: Texts.payment.PAYMENT_EXPIRED,
        PaymentStatus.PENDING_PDF:  Texts.payment.PAYMENT_EXPIRED,
    }

    text_template = texts_map.get(from_status)
    if not text_template:
        return

    await bots.buyer.bot.send_message(
        chat_id=payment.user_id,
        text=text_template.format(
            payment_id=payment.id,
            support=settings.app.SUPPORT_USERNAME,
        ),
    )
