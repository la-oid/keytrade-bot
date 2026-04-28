class MenuButtonTexts:
    PROFILE  = "Профиль"
    MARKET   = "Площадка заказов"
    ABOUT    = "О компании"
    SUPPORT  = "Поддержка"


class MarketButtonTexts:
    ACCEPT    = "Принять"
    REJECT    = "Подумаю"
    ORDER_ROW = "#{id} — {total_keys} ключей"


class ProfileButtonTexts:
    WITHDRAW        = "Вывод средств"
    WITHDRAW_STATUS = "Узнать статус заявки"


class CashoutButtonTexts:
    ALL_AMOUNT    = "Вся сумма"
    CUSTOM_AMOUNT = "Другая сумма"
    CARD          = "На карту"


class MiscButtonTexts:
    BACK = "← Назад"


class ButtonTexts:
    menu = MenuButtonTexts
    market = MarketButtonTexts
    profile = ProfileButtonTexts
    cashout = CashoutButtonTexts
    misc = MiscButtonTexts