class MenuButtonTexts:
    GET_LINK = "Получение ссылки"
    CREATE_ORDER = "Создание заказа"
    CHECK_PAYMENT = "Проверка оплаты"


class VerifyButtonTexts:
    VERIFY = "Проверка оплаты"
    PAYMENT_OK = "Оплата прошла"
    ORDER = "#{id} — {amount} шт., {price} ₽"


class MiscButtonTexts:
    pass


class ButtonTexts:
    menu = MenuButtonTexts
    verify = VerifyButtonTexts
    misc = MiscButtonTexts