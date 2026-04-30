from app.shared import bots
from .handlers import include_routers
from .utils import IsNotBlocked
from .._runner import run_bot


async def start_bot() -> None:
    bots.buyer.dp.message.filter(IsNotBlocked())
    bots.buyer.dp.callback_query.filter(IsNotBlocked())
    
    await run_bot(bots.buyer, include_routers, label="buyer")