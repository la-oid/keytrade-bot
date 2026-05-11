from aiogram.fsm.state import State, StatesGroup


class TenderStates(StatesGroup):
    waiting_add    = State()    # ввод кол-ва для ручного добавления
    waiting_queue  = State()    # ввод кол-ва для постановки в очередь
    waiting_launch = State()    # ввод кол-ва для немедленного запуска
