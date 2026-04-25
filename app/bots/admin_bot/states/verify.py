from aiogram.fsm.state import State, StatesGroup


class VerifyStates(StatesGroup):
    waiting_user_id = State()