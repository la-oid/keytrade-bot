import asyncio
from art import tprint
from loguru import logger

from shared import db, bot, dp
from .handlers import include_routers
from ..utils import LoggingMiddleware

async def on_startup():
    bot_info = await bot.get_me()
    tprint(f'@{bot_info.username}    online')
    logger.warning(f'bot info: @{bot_info.username} {bot_info.first_name} {bot_info.id}')

async def start_bot():

    include_routers(dp)

    # Регистрируем логгер
    dp.update.middleware(LoggingMiddleware())

    dp.startup.register(on_startup)
    await dp.start_polling(bot)


# if __name__ == "__main__":
#     asyncio.run(start_bot())


