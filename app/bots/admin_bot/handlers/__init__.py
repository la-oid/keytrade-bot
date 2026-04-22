from .start import r as start_router

def include_routers(dp):
    dp.include_router(start_router)
