import aiohttp
from loguru import logger


async def get_usdt_rub_rate() -> float:
    """Получает курс USD/RUB через ЦБ РФ (USDT ≈ 1 USD)."""
    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.cbr-xml-daily.ru/daily_json.js") as resp:
            data = await resp.json(content_type=None)
            rate = float(data["Valute"]["USD"]["Value"])
            return rate
