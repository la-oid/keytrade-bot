from .start import r as start_router
from .menu import r as menu_router

def include_routers(dp):
    dp.include_router(start_router)
    dp.include_router(menu_router)