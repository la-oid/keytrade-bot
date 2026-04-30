from aiogram.fsm.state import State, StatesGroup


class BlockStates(StatesGroup):
    waiting_user_id = State()   # ввод Telegram ID пользователя