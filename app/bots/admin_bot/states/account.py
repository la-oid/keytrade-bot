from aiogram.fsm.state import State, StatesGroup


class AccountStates(StatesGroup):
    waiting_user_id = State()   # ввод Telegram ID пользователя
    waiting_amount  = State()   # ввод суммы (добавить/отнять)