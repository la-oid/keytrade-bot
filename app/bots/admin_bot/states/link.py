from aiogram.fsm.state import State, StatesGroup


class LinkStates(StatesGroup):
    waiting_data = State()    # ввод банк, сумма, телефон/карта
    waiting_user_id = State() # ввод ID пользователя