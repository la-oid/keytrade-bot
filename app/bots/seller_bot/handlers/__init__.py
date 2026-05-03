from .start import r as start_router
from .menu import r as menu_router
from .market import r as market_router
from .cashout import r as cashout_router
from .crypto import r as crypto_router

def include_routers(dp):
    dp.include_router(start_router)
    dp.include_router(menu_router)
    dp.include_router(market_router)
    dp.include_router(cashout_router)
    dp.include_router(crypto_router)