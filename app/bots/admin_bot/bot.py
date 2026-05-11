from app.shared import bots
from .handlers import include_routers
from .utils import IsAdmin
from .._runner import run_bot


async def start_bot() -> None:
    bots.admin.dp.message.filter(IsAdmin())
    bots.admin.dp.callback_query.filter(IsAdmin())

    await run_bot(bots.admin, include_routers, label="admin")