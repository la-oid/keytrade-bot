from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties

from ..config.settings import settings
from app.db import Database

# Инициализация подключения к базе данных
db = Database(db_url=settings.database.URL)

# Создание бота с настройками по умолчанию
bot = Bot(
    token=settings.telegram.TOKEN.get_secret_value(),
    default=DefaultBotProperties(parse_mode='Markdown')
)

# Создание диспетчера для обработки событий бота
dp = Dispatcher()