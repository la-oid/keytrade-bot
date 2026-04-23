from aiogram.fsm.state import State, StatesGroup


class OrderStates(StatesGroup):
    medium_wholesale = State()
    large_wholesale = State()