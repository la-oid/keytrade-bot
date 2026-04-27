class MenuButtonTexts:
    GET_LINK = "Получение ссылки"
    CHECK_PAYMENT = "Проверка оплаты"
    USER_ACCOUNT = "Управление счетом"
    SPECIAL_OFFERS = "Спецпредложения"
    CREATE_PIE = "Создать/удалить Пай"
    PAYOUTS = "Заявки на выплату"
    BLOCK_USER = "Блокировка"


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