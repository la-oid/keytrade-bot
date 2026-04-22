from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, Update
from typing import Callable, Awaitable, Dict, Any
from loguru import logger


class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        user = None

        if hasattr(event, "message") and event.message:
            user = event.message.from_user
            logger.info(f"[MSG] {user.id} ({user.full_name}) -> {event.message.text}")

        elif hasattr(event, "callback_query") and event.callback_query:
            user = event.callback_query.from_user
            logger.info(f"[CALLBACK] {user.id} ({user.full_name}) -> {event.callback_query.data}")

        else:
            logger.warning(f"[UNKNOWN EVENT TYPE] {event}")

        return await handler(event, data)
