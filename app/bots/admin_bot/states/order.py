from aiogram.fsm.state import State, StatesGroup


class OrderStates(StatesGroup):
    waiting_create_data = State()   # ввод: кол-во ключей, часы — одной строкой