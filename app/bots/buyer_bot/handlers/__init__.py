from .start import r as start_router
from .menu import r as menu_router
from .wholesale import r as wholesale_router
from .payment import r as payment_router
from .check import r as check_router

def include_routers(dp):
    dp.include_router(start_router)
    dp.include_router(menu_router)
    dp.include_router(wholesale_router)
    dp.include_router(payment_router)
    dp.include_router(check_router)