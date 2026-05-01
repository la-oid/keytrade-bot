from .start import r as start_router
from .menu import r as menu_router
from .profile import r as profile_router
from .wholesale import r as wholesale_router
from .payment import r as payment_router
from .check import r as check_router
from .special_offer import r as special_offer_router
from .crypto import r as crypto_router

def include_routers(dp):
    dp.include_router(start_router)
    dp.include_router(menu_router)
    dp.include_router(profile_router)
    dp.include_router(wholesale_router)
    dp.include_router(payment_router)
    dp.include_router(check_router)
    dp.include_router(special_offer_router)
    dp.include_router(crypto_router)