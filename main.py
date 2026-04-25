import asyncio
import sys
from loguru import logger

from app.shared import db, scheduler
from app.bots import start_buyer_bot, start_seller_bot, start_admin_bot


# Настройка логирования
logger.remove()  # убираем стандартный sink
logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <cyan>{message}</cyan>"
)


async def main():
    """
    Точка входа: инициализирует БД и запускает 3 бота параллельно.
    """

    # Инициализация БД (создаёт таблицы, если их нет)
    await db.init()
    logger.info("База данных инициализирована")

    # Запускаем scheduler
    scheduler.start()
    logger.info("Scheduler запущен")

    try:
        # Запускаем все 3 бота параллельно
        logger.info("Запуск ботов...")
        await asyncio.gather(
            start_buyer_bot(),
            start_seller_bot(),
            start_admin_bot(),
        )
    finally:
        # Останавливаем scheduler
        scheduler.shutdown()
        logger.info("Scheduler остановлен")

        # Закрываем соединения с БД при остановке
        await db.dispose()
        logger.info("Соединения с БД закрыты")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Боты остановлены")