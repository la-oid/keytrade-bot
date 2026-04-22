from app.shared import bots
from .handlers import include_routers
from .._runner import run_bot


async def start_bot() -> None:
    await run_bot(bots.admin, include_routers, label="admin")