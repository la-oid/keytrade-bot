from .start import r as start_router
from .link import r as link_router
from .verify import r as verify_router

def include_routers(dp):
    dp.include_router(start_router)
    dp.include_router(link_router)
    dp.include_router(verify_router)