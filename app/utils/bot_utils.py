from app.shared import bots, settings


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