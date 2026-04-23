from aiogram import BaseMiddleware


class UserMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        from app.shared import db
        
        from_user = data.get("event_from_user")
        data["user"] = await db.user.upsert_user(
            telegram_id=from_user.id,
            username=from_user.username,
            first_name=from_user.first_name,
            last_name=from_user.last_name,
        )

        return await handler(event, data)
