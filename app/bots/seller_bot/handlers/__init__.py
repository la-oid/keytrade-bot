from .start import r as start_router
from .menu import r as menu_router
from .market import r as market_router

def include_routers(dp):
    dp.include_router(start_router)
    dp.include_router(menu_router)
    dp.include_router(market_router)