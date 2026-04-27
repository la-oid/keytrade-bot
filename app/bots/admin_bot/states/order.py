from aiogram.fsm.state import State, StatesGroup


class OrderStates(StatesGroup):
    waiting_keys_count = State()    # шаг 1: количество ключей
    waiting_price      = State()    # шаг 2: цена за ключ