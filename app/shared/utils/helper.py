from dataclasses import dataclass

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode

from app.shared.config import settings
from app.db import Database


@dataclass(frozen=True, slots=True)
class BotBundle:
    """Бот + его диспетчер. Живут парой, передаются парой."""
    bot: Bot
    dp: Dispatcher


def _make_bundle(token: str) -> BotBundle:
    bot = Bot(
        token=token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    return BotBundle(bot=bot, dp=Dispatcher())


@dataclass(frozen=True, slots=True)
class Bots:
    """Реестр всех ботов приложения."""
    buyer: BotBundle   # покупка ключей
    seller: BotBundle  # продажа ключей в заказы
    admin: BotBundle   # контролер


db = Database(db_url=settings.database.URL)

bots = Bots(
    buyer=_make_bundle(settings.telegram.BUYER_TOKEN.get_secret_value()),
    seller=_make_bundle(settings.telegram.SELLER_TOKEN.get_secret_value()),
    admin=_make_bundle(settings.telegram.ADMIN_TOKEN.get_secret_value()),
)