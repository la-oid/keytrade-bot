from typing import Callable

from aiogram import Dispatcher
from art import tprint
from loguru import logger

from app.shared import BotBundle
from .utils import LoggingMiddleware


RouterIncluder = Callable[[Dispatcher], None]


async def run_bot(bundle: BotBundle, include_routers: RouterIncluder, label: str) -> None:
    """
    Запускает одного бота: подключает роутеры, вешает middleware, стартует polling.
    """
    bot, dp = bundle.bot, bundle.dp

    include_routers(dp)
    dp.update.middleware(LoggingMiddleware())

    async def on_startup() -> None:
        me = await bot.get_me()
        tprint(f"@{me.username}    online")
        logger.warning(f"[{label}] bot info: @{me.username} {me.first_name} {me.id}")

    dp.startup.register(on_startup)
    await dp.start_polling(bot)