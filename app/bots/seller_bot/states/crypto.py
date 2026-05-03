from aiogram.fsm.state import State, StatesGroup


class CryptoStates(StatesGroup):
    waiting_wallet_address = State()   # ввод адреса кошелька