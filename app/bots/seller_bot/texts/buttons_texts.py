class MenuButtonTexts:
    PROFILE         = "Личный кабинет"
    MARKET          = "Текущие заказы"
    ABOUT           = "О компании"
    SUPPORT         = "Поддержка"
    CONTACT_SUPPORT = "Поддержка TCG."


class MarketButtonTexts:
    ACCEPT    = "Принять"
    REJECT    = "Назад"
    ORDER_ROW = "#{id} — {total_keys} Prov"


class ProfileButtonTexts:
    WITHDRAW        = "Вывод средств"
    WITHDRAW_STATUS = "Статус заявки"
    WITHDRAW_HISTORY = "История операций"


class CashoutButtonTexts:
    ALL_AMOUNT    = "Вся сумма"
    CUSTOM_AMOUNT = "Другая сумма"
    CARD          = "Банковская карта"
    CRYPTO        = "Crypto Transfer"
    SUPPORT       = "Поддержка"
    HISTORY_ROW   = "#{id} — {amount:.2f} ₽"


class MiscButtonTexts:
    BACK = "Назад"


class ButtonTexts:
    menu = MenuButtonTexts
    market = MarketButtonTexts
    profile = ProfileButtonTexts
    cashout = CashoutButtonTexts
    misc = MiscButtonTexts