from app.shared import bots, settings
from app.db.enums import PaymentStatus

from app.bots.buyer_bot.texts import Texts as BuyerTexts


# ─── Уведомление админов ─────────────────────────────────────────────────────

async def notify_admins(text: str, document=None) -> None:
    """Универсальная рассылка уведомления всем админам."""

    for admin_id in settings.telegram.ADMIN_IDS:
        if document:
            await bots.admin.bot.send_document(
                chat_id=admin_id,
                document=document,
                caption=text,
            )
        else:
            await bots.admin.bot.send_message(chat_id=admin_id, text=text)


# ─── Уведомление пользователей ───────────────────────────────────────────────

async def notify_payment_expired(payment, from_status: PaymentStatus) -> None:
    """Уведомляет пользователя об истечении срока оплаты."""

    from app.bots.buyer_bot.texts import Texts

    texts_map = {
        PaymentStatus.PENDING_PAY:  BuyerTexts.payment.PAYMENT_EXPIRED,
        PaymentStatus.PENDING_HASH: BuyerTexts.payment.PAYMENT_EXPIRED,
        PaymentStatus.PENDING_PDF:  BuyerTexts.payment.PAYMENT_EXPIRED,
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