from aiogram.fsm.state import State, StatesGroup


class MarketStates(StatesGroup):
    waiting_keys_file = State()  # выбран пай, ждём .txt с ключами