from aiogram.fsm.state import State, StatesGroup


class CashoutStates(StatesGroup):
    waiting_amount      = State()   # ввод своей суммы
    waiting_card_number = State()   # ввод номера карты
    waiting_status_id   = State()   # ввод ID заявки для проверки статуса