from app.shared import bots, db


async def broadcast_to_users(text: str) -> tuple[int, int]:
    """
    Рассылает сообщение всем не заблокированным пользователям в buyer bot.
    Возвращает (sent, failed).
    """
    users = await db.user.get_all_users()
    sent = failed = 0

    for user in users:
        try:
            await bots.buyer.bot.send_message(chat_id=user.telegram_id, text=text)
            sent += 1
        except Exception:
            failed += 1

    return sent, failed
