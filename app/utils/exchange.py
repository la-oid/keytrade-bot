import ccxt.async_support as ccxt

from app.shared.constants import CRYPTO_RATE_DISCOUNT


async def get_usdt_rub_rate() -> float:
    """Получает актуальный курс USDT/RUB с Binance."""
    exchange = ccxt.binance()
    try:
        ticker = await exchange.fetch_ticker("USDT/RUB")
        return float(ticker["last"]) - CRYPTO_RATE_DISCOUNT
    finally:
        await exchange.close()