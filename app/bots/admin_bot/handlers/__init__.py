from .start import r as start_router
from .link import r as link_router
from .verify import r as verify_router
from .order import r as order_router
from .cashout import r as cashout_router
from .block import r as block_router

def include_routers(dp):
    dp.include_router(start_router)
    dp.include_router(link_router)
    dp.include_router(verify_router)
    dp.include_router(order_router)
    dp.include_router(cashout_router)
    dp.include_router(block_router)