from aiogram.fsm.state import State, StatesGroup


class CashoutStates(StatesGroup):
    waiting_amount      = State()   # ввод своей суммы
    waiting_card_number = State()   # ввод номера карты