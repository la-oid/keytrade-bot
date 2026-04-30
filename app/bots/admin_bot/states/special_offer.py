from aiogram.fsm.state import State, StatesGroup


class SpecialOfferStates(StatesGroup):
    waiting_user_id = State()   # ввод Telegram ID пользователя
    waiting_data    = State()   # ввод кол-во ключей + время жизни (через запятую)
    waiting_text    = State()   # ввод текста предложения
    confirm         = State()   # подтверждение